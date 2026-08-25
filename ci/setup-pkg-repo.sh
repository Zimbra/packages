#!/usr/bin/env bash
#
# Path in repo: ci/setup-pkg-repo.sh
#
# Configures the Zimbra package repository inside the CURRENT build container so
# that already-published zimbra-* packages are installed from the repo instead of
# being rebuilt from source.
#
# This mirrors what the genesis builders have baked into their images:
#
#   Ubuntu (u2287)  /etc/apt/sources.list.d/zimbra.list
#                     deb [arch=amd64] http://repo-dev.eng.zimbra.com/apt/1010 jammy zimbra
#
#   RHEL/Rocky      /etc/yum.repos.d/zimbra.repo
#                     [zimbra-1010]
#                     baseurl=https://repo.zimbra.com/rpm/1010/rhel9
#
# Two deliberate differences from the genesis config:
#
#   1. The genesis list hardcodes 'jammy' and enables three release lines (87,
#      1010, 1000) at once. CI fans out over bionic/focal/jammy/noble and
#      el8/el9, so the suite is derived from /etc/os-release per container, and
#      only ONE release line is enabled - the one this pipeline targets. Enabling
#      several lines lets apt silently pick a package from a different release
#      train, which is not something you want in a reproducible build.
#
#   2. priority/pin is chosen so the job-local repo written by
#      ci/register-local-repo.sh (apt Pin-Priority 1001 / yum priority=1) still
#      wins. Packages built earlier in the same job must always beat published
#      ones.
#
# Must run BEFORE anything that calls 'apt-get update', 'apt-cache madison',
# 'yum makecache' or 'yum list available' - i.e. before ci/resolve-build-order.sh
# and before the "Install build tooling" step.
#
# Environment:
#   PKG_REPO_RELEASE  release line to enable                  (default 1010)
#   APT_REPO_BASE     base URL for .deb repos                 (default http://repo-dev.eng.zimbra.com/apt)
#   RPM_REPO_BASE     base URL for .rpm repos                 (default https://repo-dev.eng.zimbra.com/rpm)
#   APT_TRUSTED       'yes' -> [trusted=yes], skip signature verification (default yes)
#   RPM_GPGCHECK      0|1, gpgcheck for the yum repo          (default 0)
#   PROBE_PKGS        space-separated package names to probe and log (optional)
#
# Exit status is 0 even when the repo turns out to be unreachable or the suite is
# not published - a WARNING is logged instead. Failing hard here would break every
# build for a platform that simply has nothing published yet, and the existing
# fallback (build the dependency from source) is still correct, just slow. Read
# the warnings: they tell you which platform is about to take the slow path.

set -euo pipefail

PKG_REPO_RELEASE="${PKG_REPO_RELEASE:-1010}"
APT_REPO_BASE="${APT_REPO_BASE:-http://repo-dev.eng.zimbra.com/apt}"
RPM_REPO_BASE="${RPM_REPO_BASE:-https://repo-dev.eng.zimbra.com/rpm}"
APT_TRUSTED="${APT_TRUSTED:-yes}"
RPM_GPGCHECK="${RPM_GPGCHECK:-0}"
PROBE_PKGS="${PROBE_PKGS:-}"

log() { echo "setup-pkg-repo: $*"; }

# ------------------------------------------------------------- self-bootstrap
# This script is invoked as 'bash ci/setup-pkg-repo.sh', so it does not need the
# executable bit itself. But it is the first step the workflow runs, which makes
# it a convenient place to restore +x on the rest of ci/*.sh - that bit is easily
# lost when a file is added through the GitHub web UI or copied off a checkout on
# a filesystem that does not track modes. Harmless when the bit is already set.
CI_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
for _s in "$CI_DIR"/*.sh; do
  [ -f "$_s" ] || continue
  if [ ! -x "$_s" ]; then
    if chmod +x "$_s" 2>/dev/null; then
      log "restored +x on $_s"
    fi
  fi
done
unset _s

SUDO=""
if [ "$(id -u)" -ne 0 ]; then
  SUDO="sudo"
fi

# HTTP HEAD-ish probe. Returns the status code on stdout, never fails the script.
http_code() {
  local url="$1"
  if command -v curl >/dev/null 2>&1; then
    curl -sS -o /dev/null -w '%{http_code}' --max-time 20 --retry 2 "$url" 2>/dev/null || echo 000
  else
    echo "skipped"
  fi
}

# --------------------------------------------------------------------------- deb
setup_apt() {
  local codename list url code
  # shellcheck disable=SC1091
  . /etc/os-release
  codename="${UBUNTU_CODENAME:-${VERSION_CODENAME:-}}"
  if [ -z "$codename" ]; then
    log "ERROR - cannot determine distro codename from /etc/os-release"
    return 0
  fi

  log "flavour=deb codename=$codename release=$PKG_REPO_RELEASE"

  # Pre-flight: does this release line actually publish a dist for this suite?
  # The genesis config only ever needed 'jammy'; CI also builds bionic, focal and
  # noble, and a missing dist is the difference between a 2-minute build and a
  # from-source OpenSSL compile.
  url="${APT_REPO_BASE}/${PKG_REPO_RELEASE}/dists/${codename}/Release"
  code="$(http_code "$url")"
  log "probe $url -> HTTP $code"
  if [ "$code" != "200" ] && [ "$code" != "skipped" ]; then
    log "WARNING - no '$codename' dist published under release $PKG_REPO_RELEASE"
    log "WARNING - zimbra-* build deps will look unpublished on this platform and their"
    log "WARNING - producers will be rebuilt from source (slow, but correct)"
  fi

  local opts="arch=amd64"
  if [ "$APT_TRUSTED" = "yes" ]; then
    # Internal dev repo, ephemeral container. To verify signatures instead, drop
    # trusted=yes, fetch the Zimbra public key and use:
    #   [arch=amd64 signed-by=/etc/apt/keyrings/zimbra.gpg]
    opts="$opts trusted=yes"
  fi

  list=/etc/apt/sources.list.d/zimbra.list
  echo "deb [$opts] ${APT_REPO_BASE}/${PKG_REPO_RELEASE} ${codename} zimbra" \
    | $SUDO tee "$list" >/dev/null
  log "wrote $list:"
  sed 's/^/setup-pkg-repo:   /' "$list"

  if ! $SUDO apt-get update -qq -o Acquire::Retries=3; then
    log "WARNING - apt-get update reported errors after adding the zimbra source"
  fi
}

# --------------------------------------------------------------------------- rpm
setup_yum() {
  local el repo url code
  el="$(rpm -E '%{rhel}' 2>/dev/null || true)"
  if [ -z "$el" ] || [ "$el" = "%{rhel}" ]; then
    # shellcheck disable=SC1091
    . /etc/os-release
    el="${VERSION_ID%%.*}"
  fi
  if [ -z "$el" ]; then
    log "ERROR - cannot determine EL major version"
    return 0
  fi

  log "flavour=rpm el=$el release=$PKG_REPO_RELEASE"

  url="${RPM_REPO_BASE}/${PKG_REPO_RELEASE}/rhel${el}/repodata/repomd.xml"
  code="$(http_code "$url")"
  log "probe $url -> HTTP $code"
  if [ "$code" != "200" ] && [ "$code" != "skipped" ]; then
    log "WARNING - no rhel${el} tree published under release $PKG_REPO_RELEASE"
    log "WARNING - zimbra-* build deps will look unpublished on this platform and their"
    log "WARNING - producers will be rebuilt from source (slow, but correct)"
  fi

  repo=/etc/yum.repos.d/zimbra.repo
  $SUDO tee "$repo" >/dev/null <<EOF
[zimbra-${PKG_REPO_RELEASE}]
name=Zimbra RPM ${PKG_REPO_RELEASE} Repository (rhel${el})
baseurl=${RPM_REPO_BASE}/${PKG_REPO_RELEASE}/rhel${el}
enabled=1
gpgcheck=${RPM_GPGCHECK}
priority=5
module_hotfixes=1
EOF
  log "wrote $repo:"
  sed 's/^/setup-pkg-repo:   /' "$repo"

  if command -v dnf >/dev/null 2>&1; then
    $SUDO dnf -q makecache -y || log "WARNING - dnf makecache reported errors"
  else
    $SUDO yum -q makecache -y || log "WARNING - yum makecache reported errors"
  fi
}

# ---------------------------------------------------------------------- dispatch
if command -v apt-get >/dev/null 2>&1; then
  setup_apt
elif command -v dnf >/dev/null 2>&1 || command -v yum >/dev/null 2>&1; then
  setup_yum
else
  log "ERROR - neither apt-get nor yum/dnf found, cannot configure a package repo"
  exit 0
fi

# ----------------------------------------------------------------------- probing
# Log what the resolver is about to see. If these come back empty, forward
# expansion in ci/resolve-build-order.sh will add the producing package to the
# build set and compile it from source.
for p in $PROBE_PKGS; do
  if command -v apt-cache >/dev/null 2>&1; then
    v="$(apt-cache madison "$p" 2>/dev/null | awk -F'|' 'NR==1{gsub(/ /,"",$2); print $2}')"
  else
    v="$( { yum --showduplicates list available "$p" 2>/dev/null || true; } \
          | awk -v n="$p" '$1==n || index($1, n".")==1 {v=$2} END{print v}')"
  fi
  if [ -n "${v:-}" ]; then
    log "probe pkg '$p' -> $v (will be INSTALLED, not rebuilt)"
  else
    log "probe pkg '$p' -> NOT AVAILABLE (its producer will be rebuilt from source)"
  fi
done

log "done"
