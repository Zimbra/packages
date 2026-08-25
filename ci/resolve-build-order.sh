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
#   1) EXPAND (reverse): find every OTHER package that CONSUMES a changed
#      package, so it gets rebuilt+republished against the new artifact.
#      Checks BOTH Depends:/Requires: AND Build-Depends:/BuildRequires: -
#      either field mentioning a changed package's produced name is a
#      reason to rebuild the package that mentions it.
#
#      *** HOW FAR THIS WALKS IS CONTROLLED BY REVERSE_DEPS_MODE. ***
#      This is the single biggest lever on how many packages a run
#      builds, because every package reverse-expansion adds ALSO gets
#      its own forward build-time prerequisites pulled in by step (2)
#      below - so reverse-expansion cost compounds at every hop.
#
#        off        (default) Do not reverse-expand at all. Build ONLY the
#                   requested/changed package(s), plus whatever step (2)
#                   says is needed to compile them. Publish only the
#                   requested/changed package(s).
#
#        direct     Reverse-expand ONE level, from the requested/changed
#                   packages only. Their immediate consumers are rebuilt
#                   and republished, but those consumers are NOT
#                   themselves reverse-expanded.
#
#        transitive Full transitive reverse closure - every consumer, and
#                   every consumer OF a consumer, recursively. Correct if
#                   you want the whole dependent stack rebuilt against a
#                   genuine ABI/soname bump, but expensive.
#
#      Reverse-expansion NEVER fires for a package that was itself only
#      pulled in by step (2) as a forward build-time-only prerequisite -
#      see step (2) for when that even happens now.
#
#   2) EXPAND (forward): find every package a to-be-built package itself
#      needs INSTALLED to compile (Build-Depends:/BuildRequires: ONLY -
#      NEVER runtime Depends:/Requires:, which is target-install-time
#      metadata, not something `make` needs).
#
#      *** THIS STEP NO LONGER ASSUMES NEXUS IS UNAVAILABLE MID-BUILD. ***
#      Earlier revisions of this script forward-pulled (rebuilt from
#      source, in this same job) the PRODUCER of every declared build-time
#      dependency unconditionally - on the assumption that Nexus is only
#      ever a publish target, never a fetch source, mid-build. That
#      assumption was wrong: config.yml's own "Install build tooling"
#      step, and a plain `apt-get install zimbra-httpd-devel` run on a
#      genesis box, both prove the base images already have Nexus wired
#      up as a normal apt/yum source - `apt-get install`/`yum install`
#      transparently pulls already-published zimbra-* packages from it,
#      the same as any other package. There is no reason to rebuild
#      openssl/apr/apr-util/httpd from source just because php declares
#      BuildRequires: zimbra-httpd-devel, if zimbra-httpd-devel (and ITS
#      OWN build-time deps) are already sitting in Nexus from a prior
#      build.
#
#      So: before forward-pulling a build-time dependency's producer
#      package to rebuild it from source, first check whether that
#      dependency is already resolvable via the configured package
#      manager (apt-cache madison / yum list available) - i.e. already
#      published. Only forward-pull (and recursively walk ITS build-time
#      deps) if it genuinely is NOT resolvable that way - which is
#      exactly the case where it's part of the SAME unpublished
#      commit/PR as the package being built.
#
#      CAVEAT: this check runs once, in checkout_and_resolve, on a single
#      platform image - it does not re-check per build platform. If a
#      dependency's availability genuinely differs across platforms
#      (uncommon - Nexus is normally kept in sync across all of them
#      together from prior runs), this could miss a per-platform gap.
#
#      A meta/component package like zimbra/mta-components declares its
#      bundled packages (mariadb, opendkim, postfix, cluebringer, ...)
#      under runtime Depends: precisely because it doesn't compile
#      anything - those were never forward-pulled in the first place,
#      resolvable-or-not, since only Build-Depends:/BuildRequires: is
#      inspected here at all.
#
#   3) ORDER: sort the fully expanded list to match the master
#      build-order file's sequence, so dependencies always build before
#      whatever needs them.
#
# Output files:
#   - packages_to_build.txt   : ALL packages to build, in order
#                                (requested + reverse-deps + forward-deps
#                                 that genuinely aren't published yet)
#   - packages_to_publish.txt : SUBSET to actually publish to Nexus/S3
#                                (requested + reverse-deps only)
set -euo pipefail
INPUT="${1:-packages_to_build.txt}"
PUBLISH_FILE="packages_to_publish.txt"
BUILD_ORDER="${BUILD_ORDER_FILE:-build-order}"
REVERSE_DEPS_MODE="${REVERSE_DEPS_MODE:-off}"

case "$REVERSE_DEPS_MODE" in
  off|direct|transitive) ;;
  *)
    echo "resolve-build-order: ERROR - REVERSE_DEPS_MODE='$REVERSE_DEPS_MODE' is not valid."
    echo "                     Expected one of: off | direct | transitive"
    exit 1
    ;;
esac

[ -s "$INPUT" ] || { echo "resolve-build-order: $INPUT is empty, nothing to do"; exit 0; }
[ -f "$BUILD_ORDER" ] || {
  echo "resolve-build-order: ERROR - $BUILD_ORDER not found. This is the master build-order list and is required."
  exit 1
}

echo "resolve-build-order: REVERSE_DEPS_MODE=${REVERSE_DEPS_MODE}"
case "$REVERSE_DEPS_MODE" in
  off)
    echo "resolve-build-order: consumers of the changed package(s) will NOT be rebuilt."
    echo "                     Re-run with REVERSE_DEPS_MODE=direct (or transitive) if this"
    echo "                     change bumps a version/ABI that dependents must relink against."
    ;;
  direct)
    echo "resolve-build-order: immediate consumers WILL be rebuilt; consumers-of-consumers will not."
    ;;
  transitive)
    echo "resolve-build-order: FULL transitive consumer closure will be rebuilt - this can be very large."
    ;;
esac

# --- refresh package-manager metadata before any resolvability checks ---
# checkout_and_resolve (where this script runs) never runs apt-get
# update/yum makecache anywhere else - that only happens later, per
# platform, inside build_and_isolate_steps, in a DIFFERENT job/container.
# The zimbra apt/yum repo IS already configured in this image (same
# zm-base-os:devcore-ubuntu-22.04 tag used by build_u22, same baked-in
# /etc/apt/sources.list.d/zimbra.list a genesis build box has) - but a
# fresh container's apt-cache/yum metadata is empty until something
# populates it. Without this, resolvable_via_package_manager() below
# reports EVERY zimbra-* package as unresolvable regardless of whether
# it's actually published, which is exactly what was observed (openssl,
# apr, apr-util, httpd, aspell, libxml2 ALL showing "NOT found in
# configured repos" for a single php commit that only needs httpd/aspell/
# libxml2 directly).
if command -v apt-get >/dev/null 2>&1; then
  echo "resolve-build-order: refreshing apt metadata before checking build-time dep resolvability..."
  sudo apt-get update -qq || true
elif command -v yum >/dev/null 2>&1; then
  echo "resolve-build-order: refreshing yum metadata before checking build-time dep resolvability..."
  sudo yum makecache -y >/dev/null 2>&1 || true
fi

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

# Is $name already installable via the package manager configured in
# THIS image (which includes the Nexus apt/yum repo baked into the base
# zm-base-os images)? If yes, config.yml's normal "install declared
# build deps" step (plain apt-get/yum install) will pick it up on its
# own - there is no need to rebuild its producer from source in this
# job. Version constraints are intentionally NOT checked here (that is
# ci/verify-build-deps.sh's job, right before the actual build step) -
# this is only a yes/no "does it exist at all in the configured repos"
# probe to decide whether a from-source forward-pull is even needed.
resolvable_via_package_manager() {
  local name="$1"
  if command -v apt-cache >/dev/null 2>&1; then
    apt-cache madison "$name" 2>/dev/null | grep -q .
  elif command -v yum >/dev/null 2>&1; then
    yum list available "$name" 2>/dev/null | awk -v n="$name" '$1==n' | grep -q .
  else
    return 1
  fi
}

declare -A seen=()
declare -A publish_worthy=()
# is_seed marks the packages that were ACTUALLY requested/changed for this
# run, as opposed to anything the expansion below added. It is what makes
# REVERSE_DEPS_MODE=direct one level deep instead of transitive: without
# a separate marker, every reverse-discovered package also becomes
# publish-worthy and therefore re-arms reverse-expansion on the next pass
# of the queue loop, which is exactly how a single changed leaf package
# used to fan out into its entire dependent stack.
declare -A is_seed=()
queue=()
while IFS= read -r p; do
  [ -n "$p" ] || continue
  queue+=("$p"); seen["$p"]=1; publish_worthy["$p"]=1; is_seed["$p"]=1
done < "$INPUT"

i=0
while [ "$i" -lt "${#queue[@]}" ]; do
  pkg="${queue[$i]}"; i=$((i+1))
  [ -d "$pkg" ] || continue

  # ---- REVERSE: who consumes $pkg? (any field) ----------------------
  # Gated by REVERSE_DEPS_MODE - see the header comment.
  #   off        -> never
  #   direct     -> only for the originally requested/changed packages
  #   transitive -> for any publish-worthy package, i.e. recursively
  run_reverse=0
  case "$REVERSE_DEPS_MODE" in
    direct)     [ -n "${is_seed[$pkg]:-}" ]        && run_reverse=1 ;;
    transitive) [ -n "${publish_worthy[$pkg]:-}" ] && run_reverse=1 ;;
  esac

  if [ "$run_reverse" = "1" ]; then
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
              echo "resolve-build-order: auto-adding '$cand_pkg' (consumes '$name', produced by changed package '$pkg') - will be built AND published"
            fi
            break
          fi
        done <<< "$cand_deps"
      done <<< "$master_pkgs"
    fi
  fi

  # ---- FORWARD: what does $pkg need INSTALLED to compile? -----------
  # Build-Depends:/BuildRequires: ONLY - runs for EVERY package in the
  # queue (publish-worthy or not). For each declared build-time dep,
  # first check if it's already resolvable via the configured package
  # manager (already published) - only forward-pull its producer to
  # rebuild from source if it genuinely isn't.
  these_deps="$(declared_build_dep_names "$pkg")"
  if [ -n "$these_deps" ]; then
    while IFS= read -r depname; do
      [ -n "$depname" ] || continue

      if resolvable_via_package_manager "$depname"; then
        echo "resolve-build-order: '$depname' (BUILD-TIME dep of '$pkg') already published/resolvable - will be installed directly, NOT rebuilt from source"
        continue
      fi

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
          echo "resolve-build-order: auto-adding '$cand_pkg' (produces '$depname', a BUILD-TIME dependency of '$pkg' NOT found in configured repos) - build-time ONLY, will NOT be published"
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
