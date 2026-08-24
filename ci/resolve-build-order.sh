#!/usr/bin/env bash
# Path in repo: ci/resolve-build-order.sh
#
# Called as: bash ci/resolve-build-order.sh packages_to_build.txt
#
# NO per-package ci/build-deps.txt file is used anywhere in this script.
# Every internal zimbra-* dependency a package has is ALREADY declared in
# that package's own debian/control (Depends:/Build-Depends:) or .spec
# (Requires:/BuildRequires:) file - that's the single, authoritative
# source of truth the package's real build already relies on.
#
# This script does THREE things and writes TWO output files:
#
#   1) EXPAND (reverse): find every OTHER package that depends on a
#      PUBLISH-WORTHY package (originally-requested, or itself found via
#      an earlier reverse step), so it gets rebuilt too. Checks BOTH
#      Depends:/Requires: AND Build-Depends:/BuildRequires: - either
#      field mentioning a changed package's produced name is a real
#      reason to rebuild+republish the package that mentions it. Runs
#      ONLY for publish-worthy packages: a forward-pulled build-time-only
#      prerequisite (e.g. openssl, pulled in because clamav needs it to
#      compile) never triggers reverse-expansion - openssl itself didn't
#      change, so anything that merely depends on openssl has no reason
#      to be touched.
#
#   2) EXPAND (forward): find every package a to-be-built package itself
#      needs INSTALLED to compile, and if that dependency isn't already
#      in the queue, pull its PRODUCER package into this same job so it
#      gets built and installed locally (via ci/register-local-repo.sh) -
#      WITHOUT requiring it to already be published on Nexus.
#      IMPORTANT: this checks ONLY Build-Depends:/BuildRequires: - NEVER
#      runtime Depends:/Requires:. dpkg-checkbuilddeps (and rpmbuild's
#      BuildRequires check) only ever enforces the build-time field;
#      runtime Depends: is metadata for the package manager to check at
#      INSTALL time on the target system, not something that needs to be
#      present to run `make` here. A meta/component package like
#      zimbra/mta-components declares its bundled packages (mariadb,
#      opendkim, postfix, cluebringer, ...) under Depends: precisely
#      because it doesn't compile anything - forward-pulling those and
#      rebuilding them from source would be enormous unnecessary work.
#      ci/verify-build-deps.sh already checks the runtime field too (see
#      its own "runtime companion prefix" comment) against what's already
#      published/built - that's the right place for that check, not here.
#      This step runs for EVERY package in the queue (publish-worthy or
#      not), since every package needs its own real build deps satisfied.
#
#   3) ORDER: sort the fully expanded list to match the master
#      build-order file's sequence, so dependencies always build before
#      whatever needs them.
#
# Output files:
#   - packages_to_build.txt   : ALL packages to build, in order
#                                (requested + reverse-deps + forward-deps)
#   - packages_to_publish.txt : SUBSET to actually publish to Nexus/S3
#                                (requested + reverse-deps only)
set -euo pipefail
INPUT="${1:-packages_to_build.txt}"
PUBLISH_FILE="packages_to_publish.txt"
BUILD_ORDER="${BUILD_ORDER_FILE:-build-order}"

[ -s "$INPUT" ] || { echo "resolve-build-order: $INPUT is empty, nothing to do"; exit 0; }
[ -f "$BUILD_ORDER" ] || {
  echo "resolve-build-order: ERROR - $BUILD_ORDER not found. This is the master build-order list and is required."
  exit 1
}

master_pkgs="$(grep -vE '^[[:space:]]*(#|$)' "$BUILD_ORDER" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"

find_control_file() { find "$1" -path "*/debian/control" 2>/dev/null | head -1; }
find_spec_file()    { find "$1" -path "*/SPECS/*.spec"    2>/dev/null | head -1; }

produced_names() {
  local pkgpath="$1" cf sf names=""
  cf="$(find_control_file "$pkgpath")"
  if [ -n "$cf" ]; then
    names="$(grep -E '^Package:' "$cf" | awk '{print $2}' || true)"
  fi
  sf="$(find_spec_file "$pkgpath")"
  if [ -n "$sf" ]; then
    base_name="$(grep -E '^Name:' "$sf" | head -1 | awk '{print $2}' || true)"
    sub_names="$base_name"
    while IFS= read -r line; do
      case "$line" in
        *'-n '*) n="$(sed -E 's/.*-n[[:space:]]+([^[:space:]]+).*/\1/' <<<"$line")" ;;
        *)       n="${base_name}-$(awk '{print $2}' <<<"$line")" ;;
      esac
      [ -n "$n" ] && sub_names="$(printf '%s\n%s' "$sub_names" "$n")"
    done < <(grep -E '^%package' "$sf" || true)
    names="$(printf '%s\n%s' "$names" "$sub_names")"
  fi
  printf '%s\n' "$names" | sed '/^$/d' | sort -u || true
}

# ALL declared zimbra-* deps (Depends:/Requires: AND Build-Depends:/
# BuildRequires:) - used for REVERSE matching only: does $cand_pkg
# reference (in ANY field) a name produced by the changed package?
declared_dep_names() {
  local pkgpath="$1" cf sf
  cf="$(find_control_file "$pkgpath")"
  sf="$(find_spec_file "$pkgpath")"
  {
    [ -n "$cf" ] && awk '
        /^(Build-)?Depends:/ { flag=1; sub(/^[A-Za-z-]+:/, ""); print; next }
        flag && /^[A-Za-z][A-Za-z0-9-]*:/ { flag=0 }
        flag { print }
      ' "$cf"
    [ -n "$sf" ] && awk '
        /^(Build)?Requires:/ { flag=1; sub(/^[A-Za-z]+:/, ""); print; next }
        flag && /^[A-Za-z][A-Za-z0-9-]*:/ { flag=0 }
        flag { print }
      ' "$sf"
    true
  } 2>/dev/null \
    | tr ',' '\n' \
    | sed -E 's/\(.*\)//; s/[<>=!].*//; s/^[[:space:]]+//; s/[[:space:]]+$//' \
    | grep -E '^zimbra-' \
    | sort -u \
    || true
}

# ONLY the build-time field (Build-Depends:/BuildRequires:) - used for
# FORWARD expansion only. This is deliberately narrower than
# declared_dep_names() above: runtime Depends:/Requires: does not need
# its producer built in this job (see the big comment block up top).
declared_build_dep_names() {
  local pkgpath="$1" cf sf
  cf="$(find_control_file "$pkgpath")"
  sf="$(find_spec_file "$pkgpath")"
  {
    [ -n "$cf" ] && awk '
        /^Build-Depends:/ { flag=1; sub(/^Build-Depends:/, ""); print; next }
        flag && /^[A-Za-z][A-Za-z0-9-]*:/ { flag=0 }
        flag { print }
      ' "$cf"
    [ -n "$sf" ] && awk '
        /^BuildRequires:/ { flag=1; sub(/^BuildRequires:/, ""); print; next }
        flag && /^[A-Za-z][A-Za-z0-9-]*:/ { flag=0 }
        flag { print }
      ' "$sf"
    true
  } 2>/dev/null \
    | tr ',' '\n' \
    | sed -E 's/\(.*\)//; s/[<>=!].*//; s/^[[:space:]]+//; s/[[:space:]]+$//' \
    | grep -E '^zimbra-' \
    | sort -u \
    || true
}

declare -A seen=()
declare -A publish_worthy=()
queue=()
while IFS= read -r p; do
  [ -n "$p" ] || continue
  queue+=("$p"); seen["$p"]=1; publish_worthy["$p"]=1
done < "$INPUT"

i=0
while [ "$i" -lt "${#queue[@]}" ]; do
  pkg="${queue[$i]}"; i=$((i+1))
  [ -d "$pkg" ] || continue

  # ---- REVERSE: who depends on $pkg? (any field) --------------------
  # ONLY runs for publish-worthy packages - see header comment.
  if [ -n "${publish_worthy[$pkg]:-}" ]; then
    this_names="$(produced_names "$pkg")"
    if [ -n "$this_names" ]; then
      while IFS= read -r cand_pkg; do
        [ -n "$cand_pkg" ] || continue
        [ "$cand_pkg" = "$pkg" ] && continue
        [ -d "$cand_pkg" ] || continue

        cand_deps="$(declared_dep_names "$cand_pkg")"
        [ -n "$cand_deps" ] || continue

        while IFS= read -r name; do
          [ -n "$name" ] || continue
          if grep -qxF "$name" <<<"$this_names"; then
            publish_worthy["$cand_pkg"]=1
            if [ -z "${seen[$cand_pkg]:-}" ]; then
              seen["$cand_pkg"]=1
              queue+=("$cand_pkg")
              echo "resolve-build-order: auto-adding '$cand_pkg' (depends on '$name', produced by changed package '$pkg') - will be built AND published"
            fi
            break
          fi
        done <<< "$cand_deps"
      done <<< "$master_pkgs"
    fi
  fi

  # ---- FORWARD: what does $pkg need INSTALLED to compile? -----------
  # Build-Depends:/BuildRequires: ONLY - runs for EVERY package in the
  # queue (publish-worthy or not).
  these_deps="$(declared_build_dep_names "$pkg")"
  if [ -n "$these_deps" ]; then
    while IFS= read -r depname; do
      [ -n "$depname" ] || continue

      while IFS= read -r cand_pkg; do
        [ -n "$cand_pkg" ] || continue
        [ "$cand_pkg" = "$pkg" ] && continue
        [ -d "$cand_pkg" ] || continue
        [ -n "${seen[$cand_pkg]:-}" ] && continue

        cand_names="$(produced_names "$cand_pkg")"
        [ -n "$cand_names" ] || continue

        if grep -qxF "$depname" <<<"$cand_names"; then
          seen["$cand_pkg"]=1
          queue+=("$cand_pkg")
          echo "resolve-build-order: auto-adding '$cand_pkg' (produces '$depname', a BUILD-TIME dependency of '$pkg') - build-time ONLY, will NOT be published"
          break
        fi
      done <<< "$master_pkgs"
    done <<< "$these_deps"
  fi
done

bad=0
ordered_file="$(mktemp)"
for pkg in "${queue[@]}"; do
  idx="$(grep -nxF "$pkg" <<<"$master_pkgs" | head -1 | cut -d: -f1)"
  if [ -z "$idx" ]; then
    echo "resolve-build-order: ERROR '$pkg' is not listed in $BUILD_ORDER - add it there before it can be built."
    bad=1; continue
  fi
  if [ ! -d "$pkg" ] || [ ! -f "$pkg/Makefile" ]; then
    echo "resolve-build-order: ERROR '$pkg' is not a valid package directory (missing dir or Makefile)."
    bad=1; continue
  fi
  echo "$idx $pkg" >> "$ordered_file"
done

if [ "$bad" -eq 1 ]; then
  echo ""
  echo "ERROR: resolve-build-order found one or more unresolvable packages - aborting before build."
  rm -f "$ordered_file"
  exit 1
fi

sort -n "$ordered_file" | awk '{print $2}' > "$INPUT"
rm -f "$ordered_file"

: > "$PUBLISH_FILE"
while IFS= read -r pkg; do
  [ -n "${publish_worthy[$pkg]:-}" ] && echo "$pkg" >> "$PUBLISH_FILE"
done < "$INPUT"

echo "=== Build order after dependency resolution (ALL - includes build-time-only prerequisites) ==="
cat "$INPUT"
echo ""
echo "=== Package(s) that will be PUBLISHED to Nexus/S3 after this run ==="
cat "$PUBLISH_FILE"
