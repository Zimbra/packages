#!/usr/bin/env bash
# Path in repo: ci/verify-build-deps.sh
set -euo pipefail

FILE="${1:?control/spec file required}"
PREFIX="${2:?Build-Depends or BuildRequires required}"
LOCAL_REPO="${LOCAL_REPO:-/tmp/local-pkg-repo}"

[ -f "$FILE" ] || { echo "verify-build-deps: $FILE not found, skipping"; exit 0; }

# --- self-produced binary packages --------------------------------------
# A single control/spec file commonly builds SEVERAL binary packages from
# one source (e.g. thirdparty/clamav's debian/control produces both
# zimbra-clamav and zimbra-clamav-lib). Those sibling binaries very often
# declare a runtime Depends:/Requires: on EACH OTHER, pinned to the exact
# same version (e.g. "zimbra-clamav-lib Depends: zimbra-clamav (=
# ${binary:Version})") - completely normal split-package practice, and
# both come out of the SAME `make`/dpkg-buildpackage/rpmbuild invocation
# that is about to run.
#
# Those are NOT external prerequisites that need to already be built or
# published - they're produced by this very build step. Without this
# exclusion, verify-build-deps.sh fails a package checking for itself
# (e.g. clamav's build failing because "zimbra-clamav" isn't built yet -
# but it's literally what's about to be built).
#
# So: collect every "Package:" name in a debian/control file (each binary
# stanza), or the base "Name:" + every "%package [-n] <name>" subpackage
# in a .spec file, and skip any dependency that matches one of those.
self_pkgs=""
case "$FILE" in
  */debian/control)
    self_pkgs="$(grep -E '^Package:' "$FILE" | awk '{print $2}' | sort -u || true)"
    ;;
  *.spec)
    base_name="$(grep -E '^Name:' "$FILE" | head -1 | awk '{print $2}')"
    self_pkgs="$base_name"
    while IFS= read -r line; do
      case "$line" in
        *'-n '*)
          name="$(sed -E 's/.*-n[[:space:]]+([^[:space:]]+).*/\1/' <<<"$line")"
          ;;
        *)
          suffix="$(awk '{print $2}' <<<"$line")"
          name="${base_name}-${suffix}"
          ;;
      esac
      [ -n "$name" ] && self_pkgs="$(printf '%s\n%s' "$self_pkgs" "$name")"
    done < <(grep -E '^%package' "$FILE" || true)
    ;;
esac
self_pkgs="$(printf '%s\n' "$self_pkgs" | sed '/^$/d' | sort -u)"

is_self_produced() {
  local name="$1"
  [ -n "$self_pkgs" ] && grep -qxF "$name" <<<"$self_pkgs"
}

extract_deps() {
  local prefix="$1"
  awk -v prefix="$prefix" '
      $0 ~ "^"prefix":" { flag=1; sub("^"prefix":", ""); print; next }
      flag && /^[A-Za-z][A-Za-z0-9-]*:/ { flag=0 }
      flag { print }
    ' "$FILE" \
    | tr ',' '\n' \
    | sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//' \
    | grep -E '^zimbra-' || true
}

# --- ONLY the build-time field is checked here ---------------------------
# Build-Depends:/BuildRequires: is the sole field dpkg-buildpackage /
# rpmbuild actually enforce to run `make` - that's what needs to be
# resolvable before this package's build step runs. It can be satisfied
# three ways, in order of preference:
#
#   1. built EARLIER IN THIS JOB and registered into LOCAL_REPO by
#      ci/register-local-repo.sh (the case where the dep is part of the
#      SAME unpublished commit/PR - resolve-build-order.sh's forward
#      expansion put it in the build list ahead of this package); OR
#   2. already INSTALLED in the base image; OR
#   3. PUBLISHED in the configured repos (the zimbra repo written by
#      ci/setup-pkg-repo.sh), from which config.yml's build-dep install
#      step pulls it directly.
#
# (2) and (3) are now the COMMON case, not an error: resolve-build-order.sh
# only force-builds a dep's producer from source when the dep is NOT already
# published/installed. Before, this script only checked (1), so as soon as
# the resolver correctly stopped rebuilding e.g. zimbra-openssl-dev, this
# step would fail it as MISSING even though it was installed straight from
# the repo. It now falls through 1 -> 2 -> 3 and only fails if ALL miss.
#
# Runtime Depends:/Requires: (e.g. zimbra-base) is metadata consumed by
# the package manager when the FINAL .deb/.rpm is installed on a target
# system - it plays no part in producing that artifact, and is not checked
# here (see thirdparty/rsync, which builds fine with zimbra-base neither
# installed nor referenced at build time).
deps_with_versions="$(extract_deps "$PREFIX")"
[ -z "$deps_with_versions" ] && { echo "verify-build-deps: no internal zimbra- build-time deps declared, skipping"; exit 0; }

# Compare $1 >= $2 for either deb or rpm style versions. Prefers the
# platform-native comparator (both are already installed by config.yml:
# dpkg-dev on Debian images, rpmdevtools on RPM images) so epoch/tilde
# semantics are handled correctly; falls back to `sort -V` only if
# neither is present.
version_ge() {
  local have="$1" want="$2"
  if command -v dpkg >/dev/null 2>&1; then
    dpkg --compare-versions "$have" ge "$want"
  elif command -v rpmdev-vercmp >/dev/null 2>&1; then
    rpmdev-vercmp "$have" "$want" >/dev/null 2>&1
    local rc=$?
    # rpmdev-vercmp exit codes: 0 = equal, 11 = first is newer, 12 = second is newer
    [ "$rc" = "0" ] || [ "$rc" = "11" ]
  else
    [ "$(printf '%s\n%s\n' "$want" "$have" | sort -V | tail -1)" = "$have" ]
  fi
}

# What version of $1 is already INSTALLED in this image (empty if none)?
# dpkg-query prints a Version even for removed-but-config-files packages,
# so gate on the Status actually being "ok installed". rpm -q is only
# queried after confirming the package is installed, otherwise it prints
# "package X is not installed" to stdout, which must not be read as a version.
installed_version() {
  local name="$1" s
  if command -v dpkg-query >/dev/null 2>&1; then
    s="$(dpkg-query -W -f='${Status} ${Version}' "$name" 2>/dev/null || true)"
    case "$s" in
      *"ok installed"*) echo "${s##* }" ;;
    esac
  elif command -v rpm >/dev/null 2>&1; then
    if rpm -q "$name" >/dev/null 2>&1; then
      rpm -q --qf '%{VERSION}-%{RELEASE}' "$name" 2>/dev/null
    fi
  fi
}

# What version of $1 is PUBLISHED (available to install) in the configured
# repos - the zimbra repo from ci/setup-pkg-repo.sh, plus the job-local repo?
# 'yum list available' prints name.arch, so match both "name" and "name.".
published_version() {
  local name="$1"
  if command -v apt-cache >/dev/null 2>&1; then
    apt-cache madison "$name" 2>/dev/null | awk -F'|' 'NR==1{gsub(/ /,"",$2); print $2}'
  elif command -v yum >/dev/null 2>&1; then
    { yum --showduplicates list available "$name" 2>/dev/null || true; } \
      | awk -v n="$name" '$1==n || index($1, n".")==1 {v=$2} END{print v}'
  fi
}

missing=0
while IFS= read -r line; do
  [ -n "$line" ] || continue
  name=$(sed -E 's/[[:space:]]*\(.*//' <<<"$line" | sed -E 's/[[:space:]]*[<>=!].*//')

  if is_self_produced "$name"; then
    echo "verify-build-deps: SKIP  $name (sibling binary package produced by this same build)"
    continue
  fi

  # version + operator: handle BOTH "name (>= 1.2.3)" (deb) and bare
  # "name >= 1.2.3" (rpm) forms. Uses case/sed instead of bash's
  # [[ =~ ]] extended-regex matching, which was tripping the shell's
  # own conditional-expression parser on the "(>= ...)" pattern.
  ver_raw=""
  case "$line" in
    *'('*)
      ver_raw=$(sed -E 's/.*\(>=?[[:space:]]*([^)]+)\).*/\1/' <<<"$line")
      ;;
    *)
      ver_raw=$(sed -E 's/^[^><=!]*[><=!]+[[:space:]]*//' <<<"$line")
      [ "$ver_raw" = "$line" ] && ver_raw=""
      ;;
  esac

  if [ -z "$ver_raw" ]; then
    # No version constraint declared. Satisfy it from any of the three
    # sources (built-in-job -> installed -> published), in that order.
    found_local=0
    if [ -d "$LOCAL_REPO" ]; then
      for f in "$LOCAL_REPO/${name}_"*.deb "$LOCAL_REPO/${name}-"*.rpm; do
        [ -e "$f" ] && { found_local=1; break; }
      done
    fi
    if [ "$found_local" = "1" ]; then
      echo "verify-build-deps: OK    $name (no version constraint, built earlier in this job)"
    elif [ -n "$(installed_version "$name")" ]; then
      echo "verify-build-deps: OK    $name (no version constraint, already installed in image)"
    elif [ -n "$(published_version "$name")" ]; then
      echo "verify-build-deps: OK    $name (no version constraint, published in configured repos)"
    else
      echo "verify-build-deps: MISSING  $name (no version constraint declared) - not built in this job, not installed, not published"
      missing=$((missing + 1))
    fi
    continue
  fi

  ver_want="${ver_raw%%ZAPPEND*}"

  # (1) same-job local-build repo: find ANY built version of $name from
  # earlier in this job, then compare it properly instead of exact-prefix
  # matching.
  found_local=0
  if [ -d "$LOCAL_REPO" ]; then
    for f in "$LOCAL_REPO/${name}_"*.deb "$LOCAL_REPO/${name}-"*.rpm; do
      [ -e "$f" ] || continue
      base="$(basename "$f")"
      ver_have="${base#${name}[-_]}"          # drop "name-" / "name_" prefix
      case "$base" in
        *.deb)
          ver_have="${ver_have%.deb}"         # -> VERSION_arch
          ver_have="${ver_have%_*}"           # drop _<arch>  -> VERSION
          ;;                                   #   (deb versions never contain '_',
          #                                        so the last '_' is the arch sep -
          #                                        this is the fix for the #239
          #                                        "invalid character in revision
          #                                        number: ..._amd64" warning)
        *.rpm)
          ver_have="${ver_have%.rpm}"         # -> version-release.arch
          ver_have="${ver_have%.*}"           # drop .<arch>  -> version-release
          ;;
      esac
      if version_ge "$ver_have" "$ver_want"; then
        found_local=1
        echo "verify-build-deps: OK   $name >= ${ver_want} (built earlier in this job, found ${ver_have})"
        break
      fi
    done
  fi
  [ "$found_local" = "1" ] && continue

  # (2) installed in the base image?
  ver_have="$(installed_version "$name")"
  if [ -n "$ver_have" ] && version_ge "$ver_have" "$ver_want"; then
    echo "verify-build-deps: OK   $name >= ${ver_want} (already installed in image, found ${ver_have})"
    continue
  fi

  # (3) published in the configured repos?
  ver_have="$(published_version "$name")"
  if [ -n "$ver_have" ] && version_ge "$ver_have" "$ver_want"; then
    echo "verify-build-deps: OK   $name >= ${ver_want} (published in configured repos, found ${ver_have})"
    continue
  fi

  echo "verify-build-deps: MISSING  $name >= ${ver_want} - not built in this job, not installed, not published"
  missing=$((missing + 1))
done <<< "$deps_with_versions"

if [ "$missing" -gt 0 ]; then
  echo ""
  echo "ERROR: $missing internal build-time dependency(ies) not resolvable."
  echo "A build-time dep must be satisfiable one of three ways before this package"
  echo "can build: built earlier in THIS job (via ci/resolve-build-order.sh forward"
  echo "expansion + ci/register-local-repo.sh), already installed in the image, or"
  echo "published in the configured repos (ci/setup-pkg-repo.sh). None applied above."
  exit 1
fi
