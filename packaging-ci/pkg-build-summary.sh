#!/usr/bin/env bash
# Runs AFTER packaging-ci/build-packages.sh finishes successfully.
# Prints a clean, separate summary of what was built on OS platform.

set -euo pipefail
: "${PLATFORM_TAG:?PLATFORM_TAG must be set}"
INPUT="${1:-packages_to_build.txt}"
[ -s "$INPUT" ] || { echo "build-summary: $INPUT is empty, nothing was built"; exit 0; }
total="$(grep -c . "$INPUT" || true)"

echo "================================================================"
echo " BUILD SUMMARY - platform: ${PLATFORM_TAG}"
echo "================================================================"
echo " ${total} package(s) built successfully....."
echo ""
n=0
while IFS= read -r pkg; do
  [ -n "$pkg" ] || continue
  n=$((n+1))
  printf "   [%d/%d] %s\n" "$n" "$total" "$pkg"
done < "$INPUT"
echo "================================================================"
