#!/usr/bin/env bash
# Path in repo: ci/register-local-repo.sh
# Called as: bash ci/register-local-repo.sh thirdparty/<pkg>/build
#
# Drops just-built .deb/.rpm into a job-local repo and pins it above
# whatever's already configured (e.g. Nexus repos baked into the base
# image), so any package built LATER IN THE SAME CI JOB - even if it
# was declared as a dependency in the SAME commit/PR - picks up this
# freshly-built artifact instead of an older published version.
#
# Scope: only helps within one job run (one container). Does not solve
# cross-job/cross-pipeline races - that's what ci/verify-build-deps.sh
# is for.
set -euo pipefail

PKG_BUILD_DIR="$1"
LOCAL_REPO="${LOCAL_REPO:-/tmp/local-pkg-repo}"
mkdir -p "$LOCAL_REPO"

DEB_FILES=$(find "$PKG_BUILD_DIR" -maxdepth 1 -name '*.deb' 2>/dev/null || true)
RPM_FILES=$(find "$PKG_BUILD_DIR" -maxdepth 1 -name '*.rpm' ! -name '*.src.rpm' 2>/dev/null || true)

if [ -n "$DEB_FILES" ] && command -v dpkg-scanpackages >/dev/null 2>&1; then
  cp $DEB_FILES "$LOCAL_REPO/"
  ( cd "$LOCAL_REPO" && dpkg-scanpackages . /dev/null 2>/dev/null | gzip -9c > Packages.gz )
  if [ ! -f /etc/apt/sources.list.d/local-build.list ]; then
    echo "deb [trusted=yes] file:$LOCAL_REPO ./" | sudo tee /etc/apt/sources.list.d/local-build.list >/dev/null
    printf 'Package: *\nPin: origin ""\nPin-Priority: 1001\n' | sudo tee /etc/apt/preferences.d/local-build >/dev/null
  fi
  sudo apt-get update -qq
  echo "register-local-repo: added $(wc -w <<<"$DEB_FILES") deb(s) to $LOCAL_REPO"
fi

if [ -n "$RPM_FILES" ] && command -v createrepo >/dev/null 2>&1; then
  cp $RPM_FILES "$LOCAL_REPO/"
  createrepo --update "$LOCAL_REPO" >/dev/null
  if [ ! -f /etc/yum.repos.d/local-build.repo ]; then
    cat <<REPOEOF | sudo tee /etc/yum.repos.d/local-build.repo >/dev/null
[local-build]
name=local-build
baseurl=file://$LOCAL_REPO
enabled=1
gpgcheck=0
priority=1
REPOEOF
  fi
  echo "register-local-repo: added $(wc -w <<<"$RPM_FILES") rpm(s) to $LOCAL_REPO"
fi
