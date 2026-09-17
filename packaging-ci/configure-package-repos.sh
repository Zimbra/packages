#!/usr/bin/env bash
# Add every reachable Zimbra repo line in genesis order: 87, 1000, 1010.
# This lets package managers pick zimbra-base from 87 while newer packages can
# still come from 1000 or 1010 when needed.

set -euo pipefail

PKG_REPO_RELEASE="${PKG_REPO_RELEASE:-87}"
if [ -z "${PKG_REPO_RELEASE_CANDIDATES:-}" ]; then
  PKG_REPO_RELEASE_CANDIDATES="${PKG_REPO_RELEASE} 1000 1010"
fi
APT_REPO_CANDIDATES="${APT_REPO_CANDIDATES:-${APT_REPO_BASE:-https://repo.zimbra.com/apt http://repo-dev.eng.zimbra.com/apt}}"
RPM_REPO_CANDIDATES="${RPM_REPO_CANDIDATES:-${RPM_REPO_BASE:-https://repo.zimbra.com/rpm http://repo-dev.eng.zimbra.com/rpm}}"
REQUIRE_PKGS="${REQUIRE_PKGS:-zimbra-base}"
APT_TRUSTED="${APT_TRUSTED:-yes}"
RPM_GPGCHECK="${RPM_GPGCHECK:-0}"
PROBE_PKGS="${PROBE_PKGS:-}"
REPO_LOG_VERBOSE="${REPO_LOG_VERBOSE:-0}"

APT_LIST=/etc/apt/sources.list.d/zimbra.list
YUM_REPO=/etc/yum.repos.d/zimbra.repo
PROBE_FAILURES=()

log() { echo "configure-package-repo: $*"; }

CI_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
for _s in "$CI_DIR"/*.sh; do
  [ -f "$_s" ] && [ ! -x "$_s" ] && chmod +x "$_s" 2>/dev/null
done
unset _s

SUDO=""
if [ "$(id -u)" -ne 0 ]; then
  SUDO="sudo"
fi

probe_url() {
  local url="$1" code rc
  if ! command -v curl >/dev/null 2>&1; then
    echo "na na"
    return 0
  fi
  code="$(curl -sS -o /dev/null -w '%{http_code}' --max-time 20 "$url" 2>/dev/null)" && rc=0 || rc=$?
  echo "${rc} ${code:-000}"
}

describe_probe() {
  local rc="$1" code="$2" url="$3"
  case "$rc" in
    0)
      if [ "$code" = "200" ]; then
        return 0
      fi
      PROBE_FAILURES+=("HTTP $code $url")
      return 1
      ;;
    6)  PROBE_FAILURES+=("DNS FAILURE $url"); return 1 ;;
    7)  PROBE_FAILURES+=("REFUSED $url"); return 1 ;;
    28) PROBE_FAILURES+=("TIMEOUT $url"); return 1 ;;
    na) PROBE_FAILURES+=("SKIPPED $url"); return 1 ;;
    *)  PROBE_FAILURES+=("FAILED($rc) $url"); return 1 ;;
  esac
}

print_probe_failures() {
  local line
  for line in "${PROBE_FAILURES[@]}"; do
    log "$line"
  done
}

apt_update_zimbra_only() {
  local output
  output="$(
    $SUDO env DEBIAN_FRONTEND=noninteractive apt-get update -qq \
    -o Dir::Etc::sourcelist="sources.list.d/zimbra.list" \
    -o Dir::Etc::sourceparts="-" \
    -o APT::Get::List-Cleanup="0" 2>&1 || true
  )"
  output="$(printf '%s\n' "$output" | grep -Ev "NO_PUBKEY 5234D2B73B6996C7|^$" || true)"
  if [ -n "$output" ]; then
    printf '%s\n' "$output" | sed 's/^/configure-package-repo: apt: /'
  fi
}

available_version() {
  local p="$1"
  if command -v apt-cache >/dev/null 2>&1; then
    apt-cache madison "$p" 2>/dev/null | awk -F'|' 'NR==1{gsub(/ /,"",$2); print $2}' || true
  else
    { yum --showduplicates list available "$p" 2>/dev/null || true; } \
      | awk -v n="$p" '$1==n || index($1, n".")==1 {v=$2} END{print v}' || true
  fi
}

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
  log "WARNING  No usable package repo lines were found for this platform."
  log "WARNING  Tried release lines: $PKG_REPO_RELEASE_CANDIDATES"
  log "WARNING  Required packages:   $REQUIRE_PKGS"
  log "WARNING  Package resolution will fall back to slow source rebuilds."
  log "WARNING  Builds that need zimbra-base will fail later."
  log "WARNING ============================================================"
}

still_missing_warning() {
  local miss="$1"
  log "WARNING ============================================================"
  log "WARNING  These required packages are not in ANY reachable release line:"
  log "WARNING $miss"
  log "WARNING  Every release line that responded has been added anyway -"
  log "WARNING  this only means these specific packages aren't published"
  log "WARNING  under any of them for this platform."
  log "WARNING ============================================================"
}

setup_apt() {
  local codename opts base rel url rc code added=0
  # shellcheck disable=SC1091
  . /etc/os-release
  codename="${UBUNTU_CODENAME:-${VERSION_CODENAME:-}}"
  if [ -z "$codename" ]; then
    log "ERROR - cannot determine distro codename from /etc/os-release"
    return 0
  fi

  opts="arch=amd64"
  if [ "$APT_TRUSTED" = "yes" ]; then
   opts="$opts trusted=yes"
  fi

  log "flavour=deb codename=$codename"
  log "adding reachable release lines for '$codename'"

  $SUDO rm -f "$APT_LIST"
  $SUDO touch "$APT_LIST"

  for base in $APT_REPO_CANDIDATES; do
    for rel in $PKG_REPO_RELEASE_CANDIDATES; do
      url="${base}/${rel}/dists/${codename}/Release"
      # shellcheck disable=SC2046
      set -- $(probe_url "$url"); rc="$1"; code="$2"
      if describe_probe "$rc" "$code" "$url"; then
        echo "deb [$opts] ${base}/${rel} ${codename} zimbra" | $SUDO tee -a "$APT_LIST" >/dev/null
        added=$((added + 1))
      fi
    done
  done

  if [ "$added" -eq 0 ]; then
    $SUDO rm -f "$APT_LIST"
    log "no repo entry serves '$codename'"
    print_probe_failures
    no_repo_warning
    return 0
  fi

  log "enabled apt repo lines:"
  awk '{print "configure-package-repo:   " $3 " " $4}' "$APT_LIST"

  apt_update_zimbra_only

  local miss
  miss="$(missing_required)"
  if [ -n "$miss" ]; then
    still_missing_warning "$miss"
  else
    log "confirmed available across added lines: $REQUIRE_PKGS"
  fi
  if [ "$REPO_LOG_VERBOSE" = "1" ]; then
    print_probe_failures
  fi
}

setup_yum() {
  local el base rel url rc code added=0
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
  log "adding reachable release lines for rhel${el}"

  $SUDO rm -f "$YUM_REPO"
  $SUDO touch "$YUM_REPO"

  for base in $RPM_REPO_CANDIDATES; do
    for rel in $PKG_REPO_RELEASE_CANDIDATES; do
      url="${base}/${rel}/rhel${el}/repodata/repomd.xml"
      # shellcheck disable=SC2046
      set -- $(probe_url "$url"); rc="$1"; code="$2"
      if describe_probe "$rc" "$code" "$url"; then
        $SUDO tee -a "$YUM_REPO" >/dev/null <<EOF
[zimbra-${rel}]
name=Zimbra RPM ${rel} Repository (rhel${el})
baseurl=${base}/${rel}/rhel${el}
enabled=1
gpgcheck=${RPM_GPGCHECK}
priority=5
module_hotfixes=1

EOF
        added=$((added + 1))
      fi
    done
  done

  if [ "$added" -eq 0 ]; then
    $SUDO rm -f "$YUM_REPO"
    log "no repo entry serves rhel${el}"
    print_probe_failures
    no_repo_warning
    return 0
  fi

  log "enabled rpm repo lines:"
  awk -F'[][]|=' '
    /^\[/ { repo=$2 }
    /^baseurl=/ { print "configure-package-repo:   " repo " " $2 }
  ' "$YUM_REPO"

  if command -v dnf >/dev/null 2>&1; then
    $SUDO dnf -q makecache -y >/dev/null 2>&1 || true
  else
    $SUDO yum -q makecache -y >/dev/null 2>&1 || true
  fi

  local miss
  miss="$(missing_required)"
  if [ -n "$miss" ]; then
    still_missing_warning "$miss"
  else
    log "confirmed available across added lines: $REQUIRE_PKGS"
  fi
  if [ "$REPO_LOG_VERBOSE" = "1" ]; then
    print_probe_failures
  fi
}

if command -v apt-get >/dev/null 2>&1; then
  setup_apt
elif command -v dnf >/dev/null 2>&1 || command -v yum >/dev/null 2>&1; then
  setup_yum
else
  log "ERROR - neither apt-get nor yum/dnf found, cannot configure a package repo"
  exit 0
fi

for p in $PROBE_PKGS; do
  v="$(available_version "$p")"
  if [ -n "${v:-}" ]; then
    log "probe pkg '$p' -> $v (will be INSTALLED, not rebuilt)"
  else
    log "probe pkg '$p' -> NOT AVAILABLE"
  fi
done

log "done"
