#!/usr/bin/env bash
# Path in repo: ci/verify-build-deps.sh
set -euo pipefail

FILE="${1:?control/spec file required}"
PREFIX="${2:?Build-Depends or BuildRequires required}"
LOCAL_REPO="${LOCAL_REPO:-/tmp/local-pkg-repo}"

[ -f "$FILE" ] || { echo "verify-build-deps: $FILE not found, skipping"; exit 0; }

deps_with_versions=$(awk -v prefix="$PREFIX" '
    $0 ~ "^"prefix":" { flag=1; sub("^"prefix":", ""); print; next }
    flag && /^[A-Za-z][A-Za-z0-9-]*:/ { flag=0 }
    flag { print }
  ' "$FILE" \
  | tr ',' '\n' \
  | sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//' \
  | grep -E '^zimbra-' || true)

[ -z "$deps_with_versions" ] && { echo "verify-build-deps: no internal zimbra- deps declared, skipping"; exit 0; }

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
    echo "verify-build-deps: SKIP  $name (no version constraint declared)"
    continue
  fi
  ver_want="${ver_raw%%ZAPPEND*}"

  # --- 1) same-job local-build repo: find ANY built version of $name,
  #        then compare it properly instead of exact-prefix matching ---
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

  # --- 2) already-published repo (handles cross-run/older-PR case) ----
  found_remote=0
  if command -v apt-cache >/dev/null 2>&1; then
    pub_ver=$(apt-cache madison "$name" 2>/dev/null | awk '{print $3}' | head -1)
    [ -n "$pub_ver" ] && version_ge "$pub_ver" "$ver_want" && found_remote=1
  elif command -v yum >/dev/null 2>&1; then
    pub_ver=$(yum --disablerepo=local-build list available "$name" 2>/dev/null \
                | awk -v n="$name" '$1==n{print $2}' | head -1)
    [ -n "$pub_ver" ] && version_ge "$pub_ver" "$ver_want" && found_remote=1
  fi

  if [ "$found_remote" = "1" ]; then
    echo "verify-build-deps: OK   $name >= ${ver_want} (already published)"
  else
    echo "verify-build-deps: MISSING  $name >= ${ver_want} - neither built in this job nor published yet"
    missing=$((missing + 1))
  fi
done <<< "$deps_with_versions"

if [ "$missing" -gt 0 ]; then
  echo ""
  echo "ERROR: $missing internal dependency(ies) not resolvable."
  echo "If this dependency was meant to be built in a PRIOR pipeline run,"
  echo "wait for that develop-workflow's publish_packages job to go green"
  echo "and re-run this build. If it should have been built in THIS job,"
  echo "check that its thirdparty/<pkg>/ci/build-deps.txt / build order is correct."
  exit 1
fi
