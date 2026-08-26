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
# NOTE: build output is nested per-platform (e.g. build/UBUNTU18_64/*.deb,
# build/RHEL9_64/<pkg>/rpm/RPMS/x86_64/*.rpm) so we search recursively
# under PKG_BUILD_DIR rather than just its top level.
#
# Scope: only helps within one job run (one container). Does not solve
# cross-job/cross-pipeline races - that's what ci/verify-build-deps.sh
# is for.
set -euo pipefail

PKG_BUILD_DIR="$1"
LOCAL_REPO="${LOCAL_REPO:-/tmp/local-pkg-repo}"
mkdir -p "$LOCAL_REPO"

DEB_FILES=$(find "$PKG_BUILD_DIR" -name '*.deb' 2>/dev/null || true)
RPM_FILES=$(find "$PKG_BUILD_DIR" -name '*.rpm' ! -name '*.src.rpm' 2>/dev/null || true)

if [ -n "$DEB_FILES" ] && command -v dpkg-scanpackages >/dev/null 2>&1; then
  cp $DEB_FILES "$LOCAL_REPO/"
  ( cd "$LOCAL_REPO" && dpkg-scanpackages . /dev/null 2>/dev/null | gzip -9c > Packages.gz )
  if [ ! -f /etc/apt/sources.list.d/local-build.list ]; then
    echo "deb [trusted=yes] file:$LOCAL_REPO ./" | sudo tee /etc/apt/sources.list.d/local-build.list >/dev/null
    printf 'Package: *\nPin: origin ""\nPin-Priority: 1001\n' | sudo tee /etc/apt/preferences.d/local-build >/dev/null
  fi
  # Refresh ONLY the local-build file: repo so the just-added .deb becomes
  # visible to later apt-get install calls in this same job.
  #
  # This is deliberately SCOPED (Dir::Etc::sourcelist + List-Cleanup=0),
  # exactly like ci/setup-pkg-repo.sh's apt_update_zimbra_only:
  #   - it never touches the network (the repo is file://), so it's instant;
  #   - it cannot disturb the zimbra.list index that setup-pkg-repo.sh already
  #     built, which a bare unscoped 'apt-get update' refetches from scratch
  #     and can leave stale (that exact pattern produced a false
  #     'zimbra-openssl-dev not published' verdict in resolve-build-order.sh,
  #     CI #242 - see the comment block in ci/resolve-build-order.sh).
  # NOTE: the previous version also fired a curl probe at
  # https://repo-dev.eng.zimbra.com here (mislabelled with a
  # 'resolve-build-order:' prefix). That host is INTERNAL and never resolves
  # from CircleCI cloud, so the probe added ~10s and a scary failure line to
  # every deb package registered while proving nothing - removed.
  sudo apt-get update -qq \
    -o Dir::Etc::sourcelist="sources.list.d/local-build.list" \
    -o Dir::Etc::sourceparts="-" \
    -o APT::Get::List-Cleanup="0"
  echo "register-local-repo: added $(wc -w <<<"$DEB_FILES") deb(s) to $LOCAL_REPO"
fi

if [ -n "$RPM_FILES" ]; then
  CREATEREPO_BIN=""
  if command -v createrepo_c >/dev/null 2>&1; then
    CREATEREPO_BIN="createrepo_c"
  elif command -v createrepo >/dev/null 2>&1; then
    CREATEREPO_BIN="createrepo"
  fi
  if [ -n "$CREATEREPO_BIN" ]; then
    cp $RPM_FILES "$LOCAL_REPO/"
    "$CREATEREPO_BIN" --update "$LOCAL_REPO" >/dev/null
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
    # force a metadata refresh so the newly-added repo (and newly-added
    # rpms in an already-registered repo) are visible to this same shell's
    # later yum/dnf calls, instead of relying on a stale cache.
    sudo yum makecache -y --disablerepo="*" --enablerepo="local-build" >/dev/null 2>&1 || true
    echo "register-local-repo: added $(wc -w <<<"$RPM_FILES") rpm(s) to $LOCAL_REPO"
  else
    echo "register-local-repo: WARNING - neither createrepo_c nor createrepo found, skipping RPM registration" >&2
  fi
fi
