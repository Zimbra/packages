#!/usr/bin/env bash
#
# Path in repo: ci/setup-pkg-repo.sh
#
# Configures the Zimbra package repository inside the CURRENT build container so
# that already-published zimbra-* packages are installed from the repo instead of
# being rebuilt from source.
#
# WHY CANDIDATE LISTS AND NOT ONE FIXED URL
# -----------------------------------------
# Two independent things vary and both were wrong in earlier runs:
#
# 1. THE HOST. The genesis builders use repo-dev.eng.zimbra.com, which is
#    INTERNAL - it does not resolve from CircleCI cloud (pipeline #236:
#    'curl: (6) Could not resolve host'). circleci_ip_ranges only pins EGRESS
#    IPs for firewall allowlisting; it does not give the container Zimbra DNS.
#
# 2. THE RELEASE LINE. Pipeline #239 showed that a dist existing is NOT the same
#    as a dist being usable. Under release 1010 the public repo serves
#    .../dists/focal/Release (HTTP 200) but does NOT publish zimbra-base or
#    zimbra-heimdal-dev for focal:
#
#      setup-pkg-repo:   OK  https://repo.zimbra.com/apt/1010/dists/focal/Release
#      setup-pkg-repo: probe pkg 'zimbra-base' -> NOT AVAILABLE
#
#    That half-populated dist is what killed build_u20 with exit 100:
#
#      zimbra-openssl-dev : Depends: zimbra-openssl-lib (= 3.5.1-1zimbra8.8b1.20.04)
#                           but it is not going to be installed
#
#    ("not going to be installed", not "not installable" - openssl-lib WAS in the
#    job-local repo; its own dependency on zimbra-base was the unmet link.)
#    zimbra-base is only ever fetched from a repo, never built by this pipeline,
#    so a release line that lacks it cannot work no matter what gets rebuilt.
#
# Hence: probe every (base URL x release line) combination and accept the first
# one that both serves this platform's dist AND actually contains REQUIRE_PKGS.
# Reorder the candidate lists to change precedence.
#
# Must run BEFORE anything that calls 'apt-get update', 'apt-cache madison',
# 'yum makecache' or 'yum list available' - i.e. before ci/resolve-build-order.sh,
# and before the build step that runs verify-build-deps.sh / installs build-deps.
#
# ONE FULL UPDATE PER JOB
# ------------------------
# This script only ever runs a SCOPED apt-get update (against zimbra.list
# alone, via apt_update_zimbra_only()) - once per candidate probed, and that
# scoped refresh is what's still current when a candidate is accepted. It
# deliberately does NOT run a second, unscoped, full 'apt-get update' after
# choosing a candidate - that would just re-fetch archive/security/zimbra a
# second time for no new information. ci/build.sh's install_build_tooling()
# runs immediately after this step and is the job's one and only full
# 'apt-get update' (it needs one anyway, to install non-zimbra baseline
# libs from archive/security). Do not add another full update anywhere
# else in the job.
#
# Environment:
#   PKG_REPO_RELEASE             preferred release line (default 1010); tried first
#   PKG_REPO_RELEASE_CANDIDATES  full ordered list (default "$PKG_REPO_RELEASE 1000 87")
#   APT_REPO_CANDIDATES          ordered .deb base URLs
#   RPM_REPO_CANDIDATES          ordered .rpm base URLs
#   REQUIRE_PKGS                 packages that MUST be present for a release line
#                                to be accepted (default "zimbra-base")
#   APT_TRUSTED                  'yes' -> [trusted=yes], skip sig check (default yes)
#   RPM_GPGCHECK                 0|1 (default 0)
#   PROBE_PKGS                   extra names to probe and log (does not gate anything)
#   APT_REPO_BASE / RPM_REPO_BASE   legacy single-URL forms, still honoured
#
# Always exits 0. A repo problem is reported as a WARNING naming the specific
# cause (DNS vs refused vs timeout vs 404 vs published-but-incomplete) rather
# than failing here, because the real failure is more informative when it lands
# at the actual install step.

set -euo pipefail

PKG_REPO_RELEASE="${PKG_REPO_RELEASE:-1010}"
PKG_REPO_RELEASE_CANDIDATES="${PKG_REPO_RELEASE_CANDIDATES:-${PKG_REPO_RELEASE} 1000 87}"
APT_REPO_CANDIDATES="${APT_REPO_CANDIDATES:-${APT_REPO_BASE:-https://repo.zimbra.com/apt http://repo-dev.eng.zimbra.com/apt}}"
RPM_REPO_CANDIDATES="${RPM_REPO_CANDIDATES:-${RPM_REPO_BASE:-https://repo.zimbra.com/rpm http://repo-dev.eng.zimbra.com/rpm}}"
REQUIRE_PKGS="${REQUIRE_PKGS:-zimbra-base}"
APT_TRUSTED="${APT_TRUSTED:-yes}"
RPM_GPGCHECK="${RPM_GPGCHECK:-0}"
PROBE_PKGS="${PROBE_PKGS:-}"

APT_LIST=/etc/apt/sources.list.d/zimbra.list
YUM_REPO=/etc/yum.repos.d/zimbra.repo

log() { echo "setup-pkg-repo: $*"; }

# ------------------------------------------------------------- self-bootstrap
# Invoked as 'bash ci/setup-pkg-repo.sh', so this file needs no +x itself. It is
# the earliest step in the job though, which makes it a convenient place to
# restore +x on the rest of ci/*.sh - that bit is easily lost when a file is
# added through the GitHub web UI. Harmless when already set.
CI_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
for _s in "$CI_DIR"/*.sh; do
  [ -f "$_s" ] || continue
  if [ ! -x "$_s" ]; then
    chmod +x "$_s" 2>/dev/null && log "restored +x on $_s" || true
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

# Render a probe result. Returns 0 only when the URL genuinely serves content.
# An unresolvable host and a missing dist look identical to a naive check but
# have completely different fixes, so they are reported separately.
describe_probe() {
  local rc="$1" code="$2" url="$3"
  case "$rc" in
    0)
      if [ "$code" = "200" ]; then
        log "  OK          $url"
        return 0
      fi
      log "  HTTP $code    $url (host reachable, this path is not published)"
      return 1
      ;;
    6)  log "  DNS FAILURE $url (host does not resolve here - internal-only hostname?)"; return 1 ;;
    7)  log "  REFUSED     $url (host resolves, nothing listening / blocked)"; return 1 ;;
    28) log "  TIMEOUT     $url (route exists, no response - firewall drop?)"; return 1 ;;
    na) log "  SKIPPED     $url (curl not installed in this image)"; return 1 ;;
    *)  log "  FAILED      $url (curl exit $rc)"; return 1 ;;
  esac
}

# Refresh ONLY the zimbra source. A full 'apt-get update' per candidate would be
# needlessly slow, and List-Cleanup=0 stops apt discarding the other lists.
apt_update_zimbra_only() {
  $SUDO apt-get update -qq \
    -o Dir::Etc::sourcelist="sources.list.d/zimbra.list" \
    -o Dir::Etc::sourceparts="-" \
    -o APT::Get::List-Cleanup="0" 2>&1 \
    | sed 's/^/setup-pkg-repo:   apt: /' || true
}

available_version() {
  local p="$1"
  if command -v apt-cache >/dev/null 2>&1; then
    apt-cache madison "$p" 2>/dev/null | awk -F'|' 'NR==1{gsub(/ /,"",$2); print $2}'
  else
    # 'yum list available' prints name.arch, so an exact $1==name match misses.
    { yum --showduplicates list available "$p" 2>/dev/null || true; } \
      | awk -v n="$p" '$1==n || index($1, n".")==1 {v=$2} END{print v}'
  fi
}

# Echo the subset of REQUIRE_PKGS that is NOT available.
missing_required() {
  local p out=""
  for p in $REQUIRE_PKGS; do
    if [ -z "$(available_version "$p")" ]; then
      out="$out $p"
    fi
  done
  echo "${out# }"
}

no_repo_warning() {
  log "WARNING ============================================================"
  log "WARNING  No usable package repo for this platform."
  log "WARNING  Tried release lines: $PKG_REPO_RELEASE_CANDIDATES"
  log "WARNING  Required packages:   $REQUIRE_PKGS"
  log "WARNING  Consequences, in order of appearance:"
  log "WARNING   1. resolve-build-order.sh reports every zimbra-* build dep as"
  log "WARNING      unpublished and rebuilds its producer from source (slow)."
  log "WARNING   2. The first package whose deps reach zimbra-base then fails at"
  log "WARNING      'apt-get install' / 'yum install' with unmet dependencies,"
  log "WARNING      because zimbra-base is only ever fetched from a repo."
  log "WARNING  Fix repo reachability or pick a release line that publishes this"
  log "WARNING  platform fully - do not just wait out the slow build."
  log "WARNING ============================================================"
}

# --------------------------------------------------------------------------- deb
setup_apt() {
  local codename base rel url rc code opts miss
  local chosen_base="" chosen_rel=""
  # shellcheck disable=SC1091
  . /etc/os-release
  codename="${UBUNTU_CODENAME:-${VERSION_CODENAME:-}}"
  if [ -z "$codename" ]; then
    log "ERROR - cannot determine distro codename from /etc/os-release"
    return 0
  fi

  opts="arch=amd64"
  if [ "$APT_TRUSTED" = "yes" ]; then
    # The public repo IS signed, but the Zimbra keyring is absent from the
    # devcore images, hence the harmless 'NO_PUBKEY 5234D2B73B6996C7' warning.
    # To verify instead of trusting, install the key into /etc/apt/keyrings and
    # use: [arch=amd64 signed-by=/etc/apt/keyrings/zimbra.gpg]
    opts="$opts trusted=yes"
  fi

  log "flavour=deb codename=$codename"
  log "looking for a '$codename' dist that contains: $REQUIRE_PKGS"
  for base in $APT_REPO_CANDIDATES; do
    for rel in $PKG_REPO_RELEASE_CANDIDATES; do
      url="${base}/${rel}/dists/${codename}/Release"
      # shellcheck disable=SC2046
      set -- $(probe_url "$url"); rc="$1"; code="$2"
      describe_probe "$rc" "$code" "$url" || continue

      echo "deb [$opts] ${base}/${rel} ${codename} zimbra" | $SUDO tee "$APT_LIST" >/dev/null
      apt_update_zimbra_only
      miss="$(missing_required)"
      if [ -z "$miss" ]; then
        chosen_base="$base"; chosen_rel="$rel"
        break 2
      fi
      log "  REJECTED    ${base}/${rel} publishes '$codename' but is missing:$( \
            for p in $miss; do printf ' %s' "$p"; done)"
      $SUDO rm -f "$APT_LIST"
    done
  done

  if [ -z "$chosen_base" ]; then
    $SUDO rm -f "$APT_LIST"
    log "no base URL x release line combination serves a complete '$codename' dist"
    log "not writing $APT_LIST (an unreachable or useless source only adds noise"
    log "to every later apt-get update)"
    no_repo_warning
    return 0
  fi

  log "USING       ${chosen_base}/${chosen_rel} (${codename})"
  log "wrote $APT_LIST:"
  sed 's/^/setup-pkg-repo:   /' "$APT_LIST"
  # NOTE: no full 'apt-get update' here. apt_update_zimbra_only() already
  # refreshed this exact list right before this candidate was accepted
  # (last loop iteration before 'break 2'). A full, unscoped update here
  # re-fetches archive/security/zimbra again for no new information -
  # build.sh's install_build_tooling() does the job's one full update,
  # and it runs immediately after this step.
}

# --------------------------------------------------------------------------- rpm
setup_yum() {
  local el base rel url rc code miss
  local chosen_base="" chosen_rel=""
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

  log "flavour=rpm el=$el"
  log "looking for a rhel${el} tree that contains: $REQUIRE_PKGS"
  for base in $RPM_REPO_CANDIDATES; do
    for rel in $PKG_REPO_RELEASE_CANDIDATES; do
      url="${base}/${rel}/rhel${el}/repodata/repomd.xml"
      # shellcheck disable=SC2046
      set -- $(probe_url "$url"); rc="$1"; code="$2"
      describe_probe "$rc" "$code" "$url" || continue

      # priority=5 keeps this BELOW the job-local repo written by
      # ci/register-local-repo.sh (priority=1), so a package built earlier in
      # this same job always wins over a published one.
      $SUDO tee "$YUM_REPO" >/dev/null <<EOF
[zimbra-${rel}]
name=Zimbra RPM ${rel} Repository (rhel${el})
baseurl=${base}/${rel}/rhel${el}
enabled=1
gpgcheck=${RPM_GPGCHECK}
priority=5
module_hotfixes=1
EOF
      if command -v dnf >/dev/null 2>&1; then
        $SUDO dnf -q makecache -y >/dev/null 2>&1 || true
      else
        $SUDO yum -q makecache -y >/dev/null 2>&1 || true
      fi
      miss="$(missing_required)"
      if [ -z "$miss" ]; then
        chosen_base="$base"; chosen_rel="$rel"
        break 2
      fi
      log "  REJECTED    ${base}/${rel} serves rhel${el} but is missing:$( \
            for p in $miss; do printf ' %s' "$p"; done)"
      $SUDO rm -f "$YUM_REPO"
    done
  done

  if [ -z "$chosen_base" ]; then
    $SUDO rm -f "$YUM_REPO"
    log "no base URL x release line combination serves a complete rhel${el} tree"
    log "not writing $YUM_REPO"
    no_repo_warning
    return 0
  fi

  log "USING       ${chosen_base}/${chosen_rel} (rhel${el})"
  log "wrote $YUM_REPO:"
  sed 's/^/setup-pkg-repo:   /' "$YUM_REPO"
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
# Log exactly what resolve-build-order.sh and the build-dep install step will
# see. Note the deb/rpm naming split: on a deb container the '-devel' names are
# EXPECTED to be missing and vice versa - that is not a repo fault, and
# resolve-build-order.sh must not treat it as one.
for p in $PROBE_PKGS; do
  v="$(available_version "$p")"
  if [ -n "${v:-}" ]; then
    log "probe pkg '$p' -> $v (will be INSTALLED, not rebuilt)"
  else
    log "probe pkg '$p' -> NOT AVAILABLE"
  fi
done

log "done"
