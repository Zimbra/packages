#!/usr/bin/env bash
#
# Path in repo: ci/setup-pkg-repo.sh
#
# Configures the Zimbra package repository inside the CURRENT build container so
# that already-published zimbra-* packages are installed from the repo instead of
# being rebuilt from source.
#
# WHY A CANDIDATE LIST AND NOT ONE FIXED URL
# ------------------------------------------
# The genesis builders use repo-dev.eng.zimbra.com. That host is INTERNAL: it does
# not resolve from CircleCI cloud containers. Observed in pipeline #236:
#
#   curl: (6) Could not resolve host: repo-dev.eng.zimbra.com
#   W: Failed to fetch http://repo-dev.eng.zimbra.com/apt/1010/dists/focal/InRelease
#      Could not resolve 'repo-dev.eng.zimbra.com'
#
# curl exit 6 is a DNS failure. 'circleci_ip_ranges: true' only pins the
# container's EGRESS IPs so a firewall can allowlist them - it does not join the
# container to the Zimbra network or hand it private DNS.
#
# So each base URL is probed in order and the first one that actually serves this
# platform's dist (deb) or repodata tree (rpm) is the one written out. Public
# repo.zimbra.com resolves from anywhere; repo-dev is kept in the list so this
# script also does the right thing if it is ever run on a self-hosted runner
# inside the Zimbra network. Reorder the candidates to change precedence.
#
# WHAT HAPPENS IF NOTHING IS REACHABLE
# ------------------------------------
# resolve-build-order.sh falls back to building each dependency from source, which
# is slow but correct FOR THE DEPENDENCY ITSELF. It is not sufficient in general:
# a from-source zimbra-openssl-dev still declares
#
#   Depends: zimbra-openssl-lib (= <ver>)  ->  Depends: zimbra-base
#
# and zimbra-base is only ever fetched from a repo, never built here. That is
# exactly how pipeline #236 died on u20 with exit 100:
#
#   zimbra-openssl-dev : Depends: zimbra-openssl-lib (= 3.5.1-1zimbra8.8b1.20.04)
#                        but it is not going to be installed
#   E: Unable to correct problems, you have held broken packages.
#
# ("not going to be installed", not "not installable" - the package was in the
# job-local repo, its own dependency was the thing that could not be met.)
# So a reachable repo is a hard requirement, not an optimisation.
#
# Must run BEFORE anything that calls 'apt-get update', 'apt-cache madison',
# 'yum makecache' or 'yum list available' - i.e. before ci/resolve-build-order.sh,
# and before the build step that runs verify-build-deps.sh / installs build-deps.
#
# Environment:
#   PKG_REPO_RELEASE      release line, e.g. 1010 / 1000 / 87        (default 1010)
#   APT_REPO_CANDIDATES   space-separated .deb base URLs, in priority order
#   RPM_REPO_CANDIDATES   space-separated .rpm base URLs, in priority order
#   APT_TRUSTED           'yes' -> [trusted=yes], skip sig verification (default yes)
#   RPM_GPGCHECK          0|1, gpgcheck for the yum repo             (default 0)
#   PROBE_PKGS            space-separated package names to probe and log (optional)
#   APT_REPO_BASE / RPM_REPO_BASE   legacy single-URL forms, still honoured
#
# Always exits 0. A repo problem is reported as a WARNING with the specific cause
# (DNS vs refused vs timeout vs 404) rather than failing the job here, because the
# real failure is more informative when it happens at the actual install step.

set -euo pipefail

PKG_REPO_RELEASE="${PKG_REPO_RELEASE:-1010}"
APT_REPO_CANDIDATES="${APT_REPO_CANDIDATES:-${APT_REPO_BASE:-https://repo.zimbra.com/apt http://repo-dev.eng.zimbra.com/apt}}"
RPM_REPO_CANDIDATES="${RPM_REPO_CANDIDATES:-${RPM_REPO_BASE:-https://repo.zimbra.com/rpm http://repo-dev.eng.zimbra.com/rpm}}"
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

# Probe one URL. Echoes "<curl_exit_code> <http_status>".
# NOTE: deliberately no --retry. With --retry, curl prints the -w template once
# per attempt, which produced the nonsense "HTTP 000000" in pipeline #236.
probe_url() {
  local url="$1" code rc
  if ! command -v curl >/dev/null 2>&1; then
    echo "na na"
    return 0
  fi
  code="$(curl -sS -o /dev/null -w '%{http_code}' --max-time 20 "$url" 2>/dev/null)" && rc=0 || rc=$?
  echo "${rc} ${code:-000}"
}

# Turn a probe result into a human-readable line. Returns 0 only when the URL
# genuinely serves content. Distinguishing these cases matters: an unresolvable
# host and a missing dist look identical in a naive check but have completely
# different fixes.
describe_probe() {
  local rc="$1" code="$2" url="$3"
  case "$rc" in
    0)
      if [ "$code" = "200" ]; then
        log "  OK          $url"
        return 0
      fi
      log "  HTTP $code    $url (host reachable, but this path is not published)"
      return 1
      ;;
    6)
      log "  DNS FAILURE $url (host does not resolve from this container - internal-only hostname?)"
      return 1
      ;;
    7)
      log "  REFUSED     $url (host resolves, nothing listening / blocked)"
      return 1
      ;;
    28)
      log "  TIMEOUT     $url (reachable route but no response - firewall drop?)"
      return 1
      ;;
    na)
      log "  SKIPPED     $url (curl not installed in this image)"
      return 1
      ;;
    *)
      log "  FAILED      $url (curl exit $rc)"
      return 1
      ;;
  esac
}

no_repo_warning() {
  log "WARNING ============================================================"
  log "WARNING  No reachable package repo for this platform."
  log "WARNING  Consequences, in order of appearance:"
  log "WARNING   1. resolve-build-order.sh will report every zimbra-* build dep"
  log "WARNING      as unpublished and rebuild its producer from source (slow)."
  log "WARNING   2. The first package whose deps reach zimbra-base will then fail"
  log "WARNING      at 'apt-get install' / 'yum install' with unmet dependencies,"
  log "WARNING      because zimbra-base is only ever fetched from a repo."
  log "WARNING  Fix the repo reachability - do not just wait out the slow build."
  log "WARNING ============================================================"
}

# --------------------------------------------------------------------------- deb
setup_apt() {
  local codename list chosen="" base url rc code opts
  # shellcheck disable=SC1091
  . /etc/os-release
  codename="${UBUNTU_CODENAME:-${VERSION_CODENAME:-}}"
  if [ -z "$codename" ]; then
    log "ERROR - cannot determine distro codename from /etc/os-release"
    return 0
  fi

  log "flavour=deb codename=$codename release=$PKG_REPO_RELEASE"
  log "probing .deb candidates for a '$codename' dist:"
  for base in $APT_REPO_CANDIDATES; do
    url="${base}/${PKG_REPO_RELEASE}/dists/${codename}/Release"
    # shellcheck disable=SC2046
    set -- $(probe_url "$url"); rc="$1"; code="$2"
    if describe_probe "$rc" "$code" "$url"; then
      chosen="$base"
      break
    fi
  done

  if [ -z "$chosen" ]; then
    log "no candidate publishes '$codename' under release $PKG_REPO_RELEASE"
    log "not writing /etc/apt/sources.list.d/zimbra.list (an unreachable source only"
    log "adds noise to every later apt-get update)"
    no_repo_warning
    return 0
  fi

  opts="arch=amd64"
  if [ "$APT_TRUSTED" = "yes" ]; then
    # The public repo IS signed, but the Zimbra keyring is not present in the
    # devcore images. To verify instead of trusting, fetch the key and use:
    #   [arch=amd64 signed-by=/etc/apt/keyrings/zimbra.gpg]
    opts="$opts trusted=yes"
  fi

  list=/etc/apt/sources.list.d/zimbra.list
  echo "deb [$opts] ${chosen}/${PKG_REPO_RELEASE} ${codename} zimbra" \
    | $SUDO tee "$list" >/dev/null
  log "wrote $list:"
  sed 's/^/setup-pkg-repo:   /' "$list"

  if ! $SUDO apt-get update -qq -o Acquire::Retries=3; then
    log "WARNING - apt-get update reported errors after adding the zimbra source"
  fi
}

# --------------------------------------------------------------------------- rpm
setup_yum() {
  local el repo chosen="" base url rc code
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
  log "probing .rpm candidates for a rhel${el} tree:"
  for base in $RPM_REPO_CANDIDATES; do
    url="${base}/${PKG_REPO_RELEASE}/rhel${el}/repodata/repomd.xml"
    # shellcheck disable=SC2046
    set -- $(probe_url "$url"); rc="$1"; code="$2"
    if describe_probe "$rc" "$code" "$url"; then
      chosen="$base"
      break
    fi
  done

  if [ -z "$chosen" ]; then
    log "no candidate publishes a rhel${el} tree under release $PKG_REPO_RELEASE"
    log "not writing /etc/yum.repos.d/zimbra.repo"
    no_repo_warning
    return 0
  fi

  # priority=5 keeps this BELOW the job-local repo written by
  # ci/register-local-repo.sh (priority=1), so a package built earlier in this
  # same job always wins over a published one.
  repo=/etc/yum.repos.d/zimbra.repo
  $SUDO tee "$repo" >/dev/null <<EOF
[zimbra-${PKG_REPO_RELEASE}]
name=Zimbra RPM ${PKG_REPO_RELEASE} Repository (rhel${el})
baseurl=${chosen}/${PKG_REPO_RELEASE}/rhel${el}
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
# Log exactly what resolve-build-order.sh and the build-dep install step are about
# to see. 'zimbra-base' is the one to watch: it is a runtime dep of the zimbra-*
# libs and is never built here, so if it is NOT AVAILABLE the build will fail at
# install time no matter how much gets rebuilt from source.
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
