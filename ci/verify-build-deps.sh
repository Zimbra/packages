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
# resolvable (built earlier in THIS job, via LOCAL_REPO) before this
# package's build step runs.
#
# Runtime Depends:/Requires: (e.g. zimbra-base) is metadata consumed by
# the package manager when the FINAL .deb/.rpm is installed on a target
# system - it plays no part in producing that artifact. This pipeline
# never pulls/fetches from Nexus mid-build; Nexus is only ever a
# publish target, at the very end (publish_packages/deploy_s3), after
# every platform has already built successfully. So there is nothing to
# verify against Nexus here, and a runtime dep that isn't built in this
# job is not an error - see thirdparty/rsync's local `make` run, which
# built and packaged successfully with zimbra-base neither installed
# nor referenced at build time.
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
    # No version constraint declared. Since this is a build-time
    # (Build-Depends:/BuildRequires:) dep, it must have been built
    # earlier in THIS job and registered into LOCAL_REPO by
    # ci/register-local-repo.sh - resolve-build-order.sh's forward
    # expansion is what's responsible for putting it there before this
    # package builds.
    found_local=0
    if [ -d "$LOCAL_REPO" ]; then
      for f in "$LOCAL_REPO/${name}_"*.deb "$LOCAL_REPO/${name}-"*.rpm; do
        [ -e "$f" ] && { found_local=1; break; }
      done
    fi
    if [ "$found_local" = "1" ]; then
      echo "verify-build-deps: OK    $name (no version constraint, built earlier in this job)"
    else
      echo "verify-build-deps: MISSING  $name (no version constraint declared) - not built earlier in this job"
      missing=$((missing + 1))
    fi
    continue
  fi
  ver_want="${ver_raw%%ZAPPEND*}"

  # same-job local-build repo only: find ANY built version of $name from
  # earlier in this job, then compare it properly instead of exact-prefix
  # matching.
  found_local=0
  if [ -d "$LOCAL_REPO" ]; then
    for f in "$LOCAL_REPO/${name}_"*.deb "$LOCAL_REPO/${name}-"*.rpm; do
      [ -e "$f" ] || continue
      base="$(basename "$f")"
      ver_have="${base#${name}[-_]}"
      ver_have="${ver_have%.deb}"
      ver_have="${ver_have%%_*.deb}"
      ver_have="${ver_have%.*.rpm}"
      if version_ge "$ver_have" "$ver_want"; then
        found_local=1
        echo "verify-build-deps: OK   $name >= ${ver_want} (built earlier in this job, found ${ver_have})"
        break
      fi
    done
  fi
  [ "$found_local" = "1" ] && continue

  echo "verify-build-deps: MISSING  $name >= ${ver_want} - not built earlier in this job"
  missing=$((missing + 1))
done <<< "$deps_with_versions"

if [ "$missing" -gt 0 ]; then
  echo ""
  echo "ERROR: $missing internal build-time dependency(ies) not resolvable."
  echo "These must be built EARLIER IN THIS SAME JOB before this package can build."
  echo "Check that ci/resolve-build-order.sh's forward expansion is pulling in the"
  echo "producer package, and that the master build-order file lists it before this one."
  exit 1
fi
