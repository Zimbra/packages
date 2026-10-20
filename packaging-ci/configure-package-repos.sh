#!/usr/bin/env bash
# Configure reachable Zimbra repository releases in the standard order.

set -euo pipefail

if [ "${CONFIGURE_REPO_OUTPUT_FILTERED:-0}" != "1" ]; then
  set +e
  CONFIGURE_REPO_OUTPUT_FILTERED=1 bash "${BASH_SOURCE[0]}" "$@" 2>&1 \
    | tr -d '\000' \
    | sed 's/\^@//g'
  rc="${PIPESTATUS[0]}"
  exit "$rc"
fi

PKG_REPO_RELEASE="${PKG_REPO_RELEASE:-87}"
if [ -z "${PKG_REPO_RELEASE_CANDIDATES:-}" ]; then
  PKG_REPO_RELEASE_CANDIDATES="${PKG_REPO_RELEASE} 1000 1010"
fi
APT_REPO_CANDIDATES="${APT_REPO_CANDIDATES:-${APT_REPO_BASE:-https://repo.zimbra.com/apt http://repo-dev.eng.zimbra.com/apt}}"
RPM_REPO_CANDIDATES="${RPM_REPO_CANDIDATES:-${RPM_REPO_BASE:-https://repo.zimbra.com/rpm http://repo-dev.eng.zimbra.com/rpm}}"
REQUIRE_PKGS="${REQUIRE_PKGS:-zimbra-base}"

# Signature handling.
#  - Every key URL below is downloaded; every valid PGP key is installed (ids are logged).
#  - ZIMBRA_KEY_ID is an OPTIONAL pin: when set, only keys containing that id are accepted.
#  - If signatures still cannot be verified after that, *_GPG_FALLBACK=1 degrades to
#    unsigned repos with a loud warning instead of failing the whole build.
APT_TRUSTED="${APT_TRUSTED:-no}"
APT_GPG_FALLBACK="${APT_GPG_FALLBACK:-1}"
RPM_GPGCHECK="${RPM_GPGCHECK:-1}"
RPM_GPGCHECK_FALLBACK="${RPM_GPGCHECK_FALLBACK:-1}"
ZIMBRA_KEY_ID="${ZIMBRA_KEY_ID:-}"
ZIMBRA_KEY_URLS="${ZIMBRA_KEY_URLS:-https://files.zimbra.com/downloads/security/public-sha-256.key https://files.zimbra.com/downloads/security/public.key}"
APT_KEYRING_PREFIX=/usr/share/keyrings/zimbra-archive-keyring
RPM_KEYFILE_PREFIX=/etc/pki/rpm-gpg/RPM-GPG-KEY-zimbra
PROBE_PKGS="${PROBE_PKGS:-}"
REPO_LOG_VERBOSE="${REPO_LOG_VERBOSE:-0}"

APT_LIST=/etc/apt/sources.list.d/zimbra.list
YUM_REPO=/etc/yum.repos.d/zimbra.repo
PROBE_FAILURES=()
INSTALLED_KEYS=()

log() { echo "configure-package-repo: $*"; }

filter_apt_output() {
  tr -d '\000' \
    | sed 's/\^@//g' \
    | grep -Ev "^$" \
    || true
}

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

# Download one signing key. If an expected key id is given, accept the file only if
# it contains that id; otherwise accept any valid PGP public key and log its ids.
fetch_signing_key() {
  local url="$1" dest="$2" expected="${3:-}" tmp ids
  tmp="$(mktemp)"
  if ! curl -fsSL --max-time 30 -o "$tmp" "$url" 2>/dev/null \
    || ! grep -q "BEGIN PGP PUBLIC KEY BLOCK" "$tmp"; then
    log "[keys] WARNING could not download $(basename "$url")"
    rm -f "$tmp"
    return 1
  fi
  if command -v gpg >/dev/null 2>&1; then
    ids="$(gpg --show-keys --with-colons "$tmp" 2>/dev/null | awk -F: '$1=="pub" || $1=="sub" {print toupper($5)} $1=="fpr" {print toupper($10)}')"
    if [ -z "$ids" ]; then
      log "[keys] WARNING $(basename "$url") is not a readable PGP key, skipped"
      rm -f "$tmp"
      return 1
    fi
    if [ -n "$expected" ]; then
      if ! grep -qi "${expected}$" <<<"$ids"; then
        log "[keys] WARNING $(basename "$url") does not contain pinned key id $expected, skipped"
        rm -f "$tmp"
        return 1
      fi
    else
      if [ "$REPO_LOG_VERBOSE" = "1" ]; then
        log "[keys] ids: $(tr '\n' ' ' <<<"$ids" | sed 's/ *$//')"
      fi
    fi
  else
    log "[keys] WARNING gpg not installed, cannot inspect $(basename "$url")"
  fi
  $SUDO mkdir -p "$(dirname "$dest")"
  $SUDO install -m 0644 "$tmp" "$dest"
  rm -f "$tmp"
  return 0
}

# Fetch every configured key URL. Result: INSTALLED_KEYS (array of file paths).
# Logs ONE summary line, e.g. "[keys] loaded 2 of 2 signing keys (a.key, b.key)".
install_signing_keys() {
  local prefix="$1" suffix="${2:-}" url i=0 dest total=0 names=""
  INSTALLED_KEYS=()
  command -v curl >/dev/null 2>&1 || { log "[keys] WARNING curl not installed, no signing keys loaded"; return 0; }
  for url in $ZIMBRA_KEY_URLS; do
    total=$((total + 1))
    i=$((i + 1))
    dest="${prefix}-${i}${suffix}"
    if fetch_signing_key "$url" "$dest" "$ZIMBRA_KEY_ID"; then
      INSTALLED_KEYS+=("$dest")
      names="${names}${names:+, }$(basename "$url")"
    fi
  done
  log "[keys] loaded ${#INSTALLED_KEYS[@]} of ${total} signing keys${names:+ ($names)}"
  return 0
}

# Run apt-get update for the Zimbra list only. Returns 1 if apt reported a
# signature problem. The missing key id (if any) is stored in APT_MISSING_KEYS.
# Raw apt output is hidden unless REPO_LOG_VERBOSE=1 (other errors are still shown).
APT_MISSING_KEYS=""
apt_update_zimbra_only() {
  local out
  out="$($SUDO env DEBIAN_FRONTEND=noninteractive apt-get update -qq \
    -o Dir::Etc::sourcelist="sources.list.d/zimbra.list" \
    -o Dir::Etc::sourceparts="-" \
    -o APT::Get::List-Cleanup="0" 2>&1 || true)"
  if [ "$REPO_LOG_VERBOSE" = "1" ]; then
    printf '%s\n' "$out" | filter_apt_output | sed 's/^/configure-package-repo: [apt-raw] /' || true
  else
    printf '%s\n' "$out" | filter_apt_output | grep -E '^E:' | grep -v 'is not signed' \
      | sed 's/^/configure-package-repo: [apt] /' || true
  fi
  APT_MISSING_KEYS="$(grep -oE 'NO_PUBKEY [0-9A-F]+' <<<"$out" | awk '{print $2}' | sort -u | tr '\n' ' ' | sed 's/ *$//' || true)"
  if grep -qE 'NO_PUBKEY|is not signed|BADSIG|EXPKEYSIG|REVKEYSIG|The following signatures' <<<"$out"; then
    return 1
  fi
  return 0
}

# Print the newest available version of a package (empty if not available).
# Avoids parsing "yum list" output: long repo ids make it wrap across lines.
available_version() {
  local p="$1"
  if command -v apt-cache >/dev/null 2>&1; then
    apt-cache madison "$p" 2>/dev/null | awk -F'|' 'NR==1{gsub(/ /,"",$2); print $2}' || true
  elif command -v dnf >/dev/null 2>&1; then
    { dnf -q repoquery --latest-limit=1 --qf '%{version}-%{release}' "$p" 2>/dev/null || true; } | head -1 || true
  else
    { yum -q --showduplicates list available "$p" 2>/dev/null || true; } \
      | awk -v n="$p" '
          NF==1 && index($1, n".")==1 { pend=1; next }
          pend { v=$1; pend=0; next }
          $1==n || index($1, n".")==1 { v=$2 }
          END { print v }' || true
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
  log "WARNING no usable Zimbra repo found for this platform (tried releases: $PKG_REPO_RELEASE_CANDIDATES)"
  log "WARNING builds that need $REQUIRE_PKGS will fail later"
}

still_missing_warning() {
  log "WARNING required package(s) not found in any reachable repo: $1"
}

setup_apt() {
  local codename opts base rel url rc code added=0 enabled_repos="" enabled_releases=""
  local signed_by="" signature_mode="verified"
  # shellcheck disable=SC1091
  . /etc/os-release
  codename="${UBUNTU_CODENAME:-${VERSION_CODENAME:-}}"
  if [ -z "$codename" ]; then
    log "[apt] ERROR cannot determine distro codename"
    return 0
  fi

  log "[apt] configuring Zimbra repo for ${ID:-linux}/${codename}"
  opts="arch=amd64"
  if [ "$APT_TRUSTED" = "yes" ]; then
    log "[apt] APT_TRUSTED=yes, signatures NOT verified"
    opts="$opts trusted=yes"
    signature_mode="trusted"
  else
    install_signing_keys "$APT_KEYRING_PREFIX" ".asc"
    if [ "${#INSTALLED_KEYS[@]}" -gt 0 ]; then
      signed_by="$(IFS=,; echo "${INSTALLED_KEYS[*]}")"
      opts="$opts signed-by=$signed_by"
    else
      log "[apt] WARNING no signing key installed, using system keyrings only"
    fi
  fi

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
        enabled_repos="${enabled_repos}${enabled_repos:+, }${base}/${rel}"
        enabled_releases="${enabled_releases}${enabled_releases:+,}${rel}"
      fi
    done
  done

  if [ "$added" -eq 0 ]; then
    $SUDO rm -f "$APT_LIST"
    log "[apt] no repo entry serves '$codename'"
    print_probe_failures
    no_repo_warning
    return 0
  fi

  if [ "$REPO_LOG_VERBOSE" = "1" ]; then
    log "enabled apt repositories for $codename: $enabled_repos"
  fi

  if ! apt_update_zimbra_only; then
    log "[apt] WARNING cannot verify repo signature: signing key ${APT_MISSING_KEYS:-unknown} is not in the downloaded keys"
    if [ "$APT_GPG_FALLBACK" = "1" ] && [ "$APT_TRUSTED" != "yes" ]; then
      log "[apt] continuing with trusted=yes (unsigned allowed). Set APT_GPG_FALLBACK=0 to fail instead"
      $SUDO sed -i -E 's/^deb \[[^]]*\]/deb [arch=amd64 trusted=yes]/' "$APT_LIST"
      signature_mode="NOT VERIFIED (trusted=yes)"
      apt_update_zimbra_only || true
    else
      signature_mode="FAILED"
    fi
  fi

  local miss
  miss="$(missing_required)"
  if [ -n "$miss" ]; then
    still_missing_warning "$miss"
  else
    log "[apt] READY ${ID:-linux}/$codename | releases: $enabled_releases | signatures: $signature_mode | $REQUIRE_PKGS: found"
  fi
  if [ "$REPO_LOG_VERBOSE" = "1" ]; then
    print_probe_failures
  fi
}

setup_yum() {
  local el base rel url rc code repo_id added=0 enabled_repos="" enabled_releases=""
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

  log "[rpm] configuring Zimbra repo for rhel${el}"
  local pm="yum"
  command -v dnf >/dev/null 2>&1 && pm="dnf"

  # Install every usable signing key (classic + SHA-256) and import it into rpm.
  local gpgkey_line="" gpgkey_conf="" gpgcheck="$RPM_GPGCHECK" k
  if [ "$RPM_GPGCHECK" = "1" ]; then
    install_signing_keys "$RPM_KEYFILE_PREFIX" ""
    if [ "${#INSTALLED_KEYS[@]}" -gt 0 ]; then
      for k in "${INSTALLED_KEYS[@]}"; do
        $SUDO rpm --import "$k" >/dev/null 2>&1 || true
        gpgkey_line="${gpgkey_line}${gpgkey_line:+ }file://${k}"
      done
      gpgkey_conf="gpgkey=${gpgkey_line}"
    elif [ "$RPM_GPGCHECK_FALLBACK" = "1" ]; then
      log "[rpm] WARNING no usable signing key, continuing with gpgcheck=0 (signatures NOT verified)"
      gpgcheck=0
    else
      log "[rpm] WARNING no usable signing key and RPM_GPGCHECK_FALLBACK=0, install will likely fail"
    fi
  else
    log "[rpm] RPM_GPGCHECK=0, signatures NOT verified"
  fi

  $SUDO rm -f "$YUM_REPO"
  $SUDO touch "$YUM_REPO"

  for base in $RPM_REPO_CANDIDATES; do
    for rel in $PKG_REPO_RELEASE_CANDIDATES; do
      url="${base}/${rel}/rhel${el}/repodata/repomd.xml"
      # shellcheck disable=SC2046
      set -- $(probe_url "$url"); rc="$1"; code="$2"
      if describe_probe "$rc" "$code" "$url"; then
        added=$((added + 1))
        # Keep repo ids short: long ids make yum/dnf wrap its list output.
        repo_id="zimbra-${rel}-r${added}"
        $SUDO tee -a "$YUM_REPO" >/dev/null <<REPOEOF
[${repo_id}]
name=Zimbra RPM ${rel} Repository (rhel${el})
baseurl=${base}/${rel}/rhel${el}
enabled=1
gpgcheck=${gpgcheck}
${gpgkey_conf}
priority=5
module_hotfixes=1

REPOEOF
        enabled_repos="${enabled_repos}${enabled_repos:+, }${base}/${rel}/rhel${el}"
        enabled_releases="${enabled_releases}${enabled_releases:+,}${rel}"
      fi
    done
  done

  if [ "$added" -eq 0 ]; then
    $SUDO rm -f "$YUM_REPO"
    log "[rpm] no repo entry serves rhel${el}"
    print_probe_failures
    no_repo_warning
    return 0
  fi

  if [ "$REPO_LOG_VERBOSE" = "1" ]; then
    log "enabled rpm repositories for rhel${el}: $enabled_repos"
  fi

  $SUDO "$pm" -q makecache -y >/dev/null 2>&1 || true

  # With gpgcheck on, prove that the installed keys really match the packages by
  # downloading the required packages (the signature check runs at download time).
  if [ "$gpgcheck" = "1" ] && [ -n "$REQUIRE_PKGS" ]; then
    local probe_dir
    probe_dir="$(mktemp -d)"
    # shellcheck disable=SC2086
    if $SUDO "$pm" -q -y install --downloadonly --downloaddir="$probe_dir" $REQUIRE_PKGS >/dev/null 2>&1; then
      log "[rpm] signature check passed for $REQUIRE_PKGS"
    elif [ "$RPM_GPGCHECK_FALLBACK" = "1" ]; then
      log "[rpm] signature check FAILED for $REQUIRE_PKGS with the downloaded keys"
      log "[rpm] continuing with gpgcheck=0 (signatures NOT verified). Set RPM_GPGCHECK_FALLBACK=0 to fail instead"
      $SUDO sed -i 's/^gpgcheck=1/gpgcheck=0/' "$YUM_REPO"
      gpgcheck=0
      $SUDO "$pm" -q makecache -y >/dev/null 2>&1 || true
    else
      log "[rpm] signature check FAILED for $REQUIRE_PKGS (RPM_GPGCHECK_FALLBACK=0)"
    fi
    rm -rf "$probe_dir" 2>/dev/null || $SUDO rm -rf "$probe_dir" || true
  fi

  local miss
  miss="$(missing_required)"
  if [ -n "$miss" ]; then
    still_missing_warning "$miss"
  else
    local sig_state="verified"
    [ "$gpgcheck" = "1" ] || sig_state="NOT VERIFIED (gpgcheck=0)"
    log "[rpm] READY rhel${el} | releases: $enabled_releases | signatures: $sig_state | $REQUIRE_PKGS: found"
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
