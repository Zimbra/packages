#!/usr/bin/env bash
# Path in repo: ci/verify-build-deps.sh
#
# Called as: bash ci/verify-build-deps.sh <control-or-spec-file> <prefix>
#   prefix = "Build-Depends" (debian/control) or "BuildRequires" (*.spec)
#
# Extracts any declared dependency starting with "zimbra-" (i.e. an
# INTERNAL package built by this same thirdparty/ pipeline) along with
# its required version, and verifies a build satisfying that version is
# actually resolvable RIGHT NOW - checking, in order:
#
#   1) THIS JOB's local-build repo (ci/register-local-repo.sh output) -
#      covers the case where the dependency (e.g. openssl) was changed
#      in the SAME commit/PR as this package (e.g. nginx) and already
#      built earlier in this same job's loop.
#   2) Whatever's already configured/published (e.g. Nexus repos baked
#      into the base image) - covers the normal case where the
#      dependency was published in a prior, separate pipeline run.
#
# If neither has it, we fail fast with a clear message instead of
# silently letting apt-get/yum install an older matching version - this
# is the guard against the cross-run race where dependency A's own
# publish_packages job hasn't finished yet when B's build starts.
#
# NOTE on versions: VERSION/ZAPPEND placeholders in control/spec are NOT
# yet substituted at this point in the build (same reason
# install_declared_build_deps in config.yml avoids mk-build-deps/
# yum-builddep). So we match on the version PREFIX up to "ZAPPEND".
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

missing=0
while IFS= read -r line; do
  [ -n "$line" ] || continue
  name=$(sed -E 's/[[:space:]]*\(.*//' <<<"$line")
  ver_raw=$(sed -nE 's/.*\(>=?[[:space:]]*([^)]+)\).*/\1/p' <<<"$line")
  if [ -z "$ver_raw" ]; then
    echo "verify-build-deps: SKIP  $name (no version constraint declared)"
    continue
  fi
  ver_prefix="${ver_raw%%ZAPPEND*}"

  # --- 1) same-job local-build repo (handles same-commit/PR case) -----
  found_local=0
  if [ -d "$LOCAL_REPO" ]; then
    if ls "$LOCAL_REPO/${name}_${ver_prefix}"*.deb >/dev/null 2>&1 \
       || ls "$LOCAL_REPO/${name}-${ver_prefix}"*.rpm >/dev/null 2>&1; then
      found_local=1
    fi
  fi
  if [ "$found_local" = "1" ]; then
    echo "verify-build-deps: OK   $name >= ${ver_prefix}* (built earlier in this job)"
    continue
  fi

  # --- 2) already-published repo (handles cross-run/older-PR case) ----
  found_remote=0
  if command -v apt-cache >/dev/null 2>&1; then
    if apt-cache madison "$name" 2>/dev/null | awk '{print $3}' | grep -q "^${ver_prefix}"; then
      found_remote=1
    fi
  elif command -v yum >/dev/null 2>&1; then
    if yum --disablerepo=local-build list available "$name" 2>/dev/null \
         | awk -v n="$name" '$1==n{print $2}' | grep -q "^${ver_prefix}"; then
      found_remote=1
    fi
  fi

  if [ "$found_remote" = "1" ]; then
    echo "verify-build-deps: OK   $name >= ${ver_prefix}* (already published)"
  else
    echo "verify-build-deps: MISSING  $name >= ${ver_prefix}* - neither built in this job nor published yet"
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
