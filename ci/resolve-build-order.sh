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
#      package which just changed, so it gets rebuilt too. These are
#      PUBLISH-worthy - their own behaviour may have changed.
#
#   2) EXPAND (forward): find every package that a to-be-built package
#      itself depends on (via its own Build-Depends:/BuildRequires:),
#      and if that dependency isn't already in the queue, pull its
#      PRODUCER package into this same job so it gets built and can be
#      installed locally (via ci/register-local-repo.sh) - WITHOUT
#      requiring it to already be published on Nexus. These are
#      BUILD-TIME-ONLY - they get compiled so clamav (etc.) can link
#      against them in this job, but are NOT copied into the publish
#      artifacts. Nexus only ever receives the packages that were
#      actually requested to change (+ their reverse-dependents).
#
#   3) ORDER: sort the fully expanded list to match the master
#      build-order file's sequence, so dependencies always build before
#      whatever needs them (this also naturally puts forward-pulled
#      prerequisites like openssl before clamav, since build-order.txt
#      already encodes the correct topological order).
#
# Output files (both written into the CWD, both get persisted to the
# workspace automatically since the whole ~/packages dir is persisted):
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

# --- every real package path, taken straight from the master order list -
master_pkgs="$(grep -vE '^[[:space:]]*(#|$)' "$BUILD_ORDER" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"

# --- find a package's control/spec files (mirrors config.yml's own find)
find_control_file() { find "$1" -path "*/debian/control" 2>/dev/null | head -1; }
find_spec_file()    { find "$1" -path "*/SPECS/*.spec"    2>/dev/null | head -1; }

# --- every binary package NAME this package produces --------------------
# NOTE: every grep/awk step below is guarded with "|| true" - a control
# file legitimately having zero matching lines makes grep exit 1 even
# though nothing is wrong, and under this script's set -e/pipefail that
# would silently kill the whole script (see the same pattern already
# fixed in config.yml's install_declared_build_deps and in
# verify-build-deps.sh).
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

# --- every zimbra-* dependency NAME this package declares (any field,
#     any stanza - build-time and runtime both count as a relationship) -
# NOTE: final "|| true" is required - a package with NO zimbra-* deps at
# all (e.g. thirdparty/openssl itself) is the normal case, not an error.
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

declare -A seen=()
declare -A publish_worthy=()
queue=()
while IFS= read -r p; do
  [ -n "$p" ] || continue
  queue+=("$p"); seen["$p"]=1; publish_worthy["$p"]=1
done < "$INPUT"

# --- expand: repeat until no new package (either direction) gets pulled in
i=0
while [ "$i" -lt "${#queue[@]}" ]; do
  pkg="${queue[$i]}"; i=$((i+1))
  [ -d "$pkg" ] || continue

  # ---- REVERSE: who depends on $pkg? -> pulled in AND publish-worthy ----
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

  # ---- FORWARD: what does $pkg itself depend on? -> pulled in as       --
  # ---- build-time-ONLY prerequisite, never marked publish_worthy       --
  these_deps="$(declared_dep_names "$pkg")"
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
          echo "resolve-build-order: auto-adding '$cand_pkg' (produces '$depname', a build-time dependency of '$pkg') - build-time ONLY, will NOT be published"
          break
        fi
      done <<< "$master_pkgs"
    done <<< "$these_deps"
  fi
done

# --- order the queue by position in the master build-order list --------
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
