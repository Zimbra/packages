#!/usr/bin/env bash
# Path in repo: ci/build-summary.sh
#
# Called as: bash ci/build-summary.sh packages_to_build.txt
#
# Runs AFTER ci/build.sh finishes successfully. Prints a clean, separate
# summary of what was built on this platform, so it's easy to see at a
# glance in the CircleCI UI without scrolling through the full build log.

set -euo pipefail

: "${PLATFORM_TAG:?PLATFORM_TAG must be set}"
INPUT="${1:-packages_to_build.txt}"

[ -s "$INPUT" ] || { echo "build-summary: $INPUT is empty, nothing was built"; exit 0; }

total="$(grep -c . "$INPUT" || true)"

echo "================================================================"
echo " BUILD SUMMARY - platform: ${PLATFORM_TAG}"
echo "================================================================"
echo " ${total} package(s) built successfully, from this PR/commit:"
echo ""
n=0
while IFS= read -r pkg; do
  [ -n "$pkg" ] || continue
  n=$((n+1))
  printf "   [%d/%d] %s\n" "$n" "$total" "$pkg"
done < "$INPUT"
echo ""
echo " Artifacts are in build/dist_workspace/${PLATFORM_TAG}/ and have been"
echo " uploaded to this job's Artifacts tab."
echo " Once every platform (u24/u22/u20/c9/c8) succeeds, these package(s)"
echo " will be published to Nexus (develop branch) after manual approval"
echo " at the 'publish_packages_hold' step."
echo "================================================================"
