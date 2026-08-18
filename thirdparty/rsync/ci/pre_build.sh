#!/bin/bash
# Path in repo: thirdparty/rsync/ci/pre_build.sh
#
# Package-specific pre-build hook for rsync.
# config.yml only checks IF this file exists and is executable, and calls
# it - it doesn't know what's inside. So this fix can be edited/removed
# without touching config.yml, and can never affect any other package.
#
# Reason this hook exists:
# Ubuntu 18.04 (bionic) ships libzstd 1.3.3, which predates the
# ZSTD_minCLevel symbol (added in zstd 1.4.0) that rsync's ./configure
# requires. We pull just libzstd-dev from the focal (20.04) archive on
# this platform only, then drop the temporary apt source again.
#
# Called as:  thirdparty/rsync/ci/pre_build.sh "$PLATFORM_TAG"
set -eo pipefail

PLATFORM_TAG="$1"

if [ "$PLATFORM_TAG" != "u18" ]; then
  echo "[rsync pre_build hook] platform=${PLATFORM_TAG} -> nothing to do, skipping."
  exit 0
fi

if ! command -v apt-get >/dev/null 2>&1; then
  echo "[rsync pre_build hook] apt-get not found on this image, skipping."
  exit 0
fi

echo "[rsync pre_build hook] bionic detected - pulling libzstd-dev from focal"
echo "deb http://archive.ubuntu.com/ubuntu focal main" \
  | sudo tee /etc/apt/sources.list.d/focal-zstd.list
sudo apt-get update
sudo apt-get install -y -t focal libzstd-dev
sudo rm -f /etc/apt/sources.list.d/focal-zstd.list
sudo apt-get update
echo "[rsync pre_build hook] done."
