#!/usr/bin/env bash
# Path in repo: ci/resolve-build-order.sh
#
# Called as: bash ci/resolve-build-order.sh packages_to_build.txt
#
# PR is the source of truth: packages_to_build.txt, at the point this
# script runs, already contains the EXACT and ONLY packages that should
# be built - whatever "auto" detected via git diff, or whatever the
# package_name pipeline parameter said explicitly.
#
# This script does TWO things:
#   1. Sort that list into the sequence given by the master build-order
#      file, so a package that depends on another changed package (e.g.
#      zimbra/apache-components depends on thirdparty/httpd) always
#      builds after it.
#   2. Print a dry-run summary of the final, sorted build plan - so
#      anyone reading this job's log sees exactly what is about to be
#      built, in what order, BEFORE any compiling starts.
#
# It does NOT discover any extra packages, and does NOT need the zimbra
# package repo configured (no apt-cache/yum lookups here at all) - any
# build-time prerequisite that was NOT itself changed in the PR is
# assumed to already be published; ci/build.sh's verify_build_deps checks
# that assumption right before each package builds and fails clearly if
# it's wrong.
#
# Since every package that gets built here was explicitly part of the PR,
# every package that gets built also gets published - there is no
# build-time-only/unpublished-prerequisite split to track anymore.

set -euo pipefail

INPUT="${1:?path to packages_to_build.txt required}"
BUILD_ORDER="${BUILD_ORDER_FILE:-build-order}"

[ -s "$INPUT" ] || { echo "resolve-build-order: $INPUT is empty, nothing to do"; exit 0; }
[ -f "$BUILD_ORDER" ] || {
  echo "resolve-build-order: ERROR - $BUILD_ORDER not found. This is the master build-order list and is required."
  exit 1
}

master_pkgs="$(grep -vE '^[[:space:]]*(#|$)' "$BUILD_ORDER" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"

bad=0
ordered_file="$(mktemp)"
while IFS= read -r pkg; do
  [ -n "$pkg" ] || continue

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
done < "$INPUT"

if [ "$bad" -eq 1 ]; then
  echo ""
  echo "ERROR: resolve-build-order found one or more unresolvable packages - aborting before build."
  rm -f "$ordered_file"
  exit 1
fi

sort -n "$ordered_file" | awk '{print $2}' > "$INPUT"
rm -f "$ordered_file"

# --- dry-run summary --------------------------------------------------
total="$(grep -c . "$INPUT" || true)"
echo ""
echo "================================================================"
echo " DRY RUN - build plan for this pipeline run"
echo " (${total} package(s), in build order, will be built on EVERY platform)"
echo "================================================================"
n=0
while IFS= read -r pkg; do
  [ -n "$pkg" ] || continue
  n=$((n+1))
  printf "  [%d/%d] %s\n" "$n" "$total" "$pkg"
done < "$INPUT"
echo "================================================================"
