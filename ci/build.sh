#!/usr/bin/env bash
# Path in repo: ci/build.sh
#
# Called as: bash ci/build.sh packages_to_build.txt
#
# Everything needed to build every resolved package on THIS platform
# (PLATFORM_TAG env var). This is the ONE script config.yml's build jobs
# call - every build-behavior change (baseline libs, per-package steps,
# how a fresh build is shared with a later package in the same run)
# happens here, never in .circleci/config.yml.
#
# Flow:
#   1. install_build_tooling   - OS packaging tools + baseline -dev/-devel
#                                 libs every package needs (once per job)
#   2. for each package, in build order:
#        a. run its ci/pre_build.sh hook if present
#        b. verify_build_deps    - its declared zimbra-* build-time deps
#                                   must be resolvable one of 3 ways:
#                                     - built earlier in THIS job (LOCAL_REPO)
#                                     - already installed in the image
#                                     - published in the zimbra repo
#                                   fails clearly here, before `make`, if none apply
#        c. install those build-time deps
#        d. make
#        e. register_local_repo  - drop the freshly-built .deb/.rpm into a
#                                   job-local repo pinned ABOVE the published
#                                   zimbra repo, so a LATER package in this
#                                   same run picks up this fresh build
#        f. copy artifacts into build/dist_workspace/${PLATFORM_TAG}/

set -euo pipefail

: "${PLATFORM_TAG:?PLATFORM_TAG must be set}"
INPUT="${1:-packages_to_build.txt}"
LOCAL_REPO="${LOCAL_REPO:-/tmp/local-pkg-repo}"

[ -s "$INPUT" ] || { echo "build: $INPUT is empty, nothing to build"; exit 0; }

########################################################################
# 1) baseline OS packaging tools + dev libraries (once per job)
########################################################################
install_build_tooling() {
  if command -v apt-get >/dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get install -y --no-install-recommends \
      dpkg-dev build-essential cmake python3 \
      libssl-dev liblz4-dev zlib1g-dev libzstd-dev libexpat1-dev libxml2-dev \
      libcurl4-openssl-dev
  elif command -v yum >/dev/null 2>&1; then
    OS_VERSION=$(rpm -E %{rhel})
    if [ "$OS_VERSION" = "8" ]; then
      sudo sed -i \
        -e 's/^mirrorlist=/#mirrorlist=/' \
        -e 's/^metalink=/#metalink=/' \
        -e 's|^#baseurl=http://mirror.centos.org|baseurl=https://vault.centos.org|' \
        /etc/yum.repos.d/*.repo
    fi
    sudo yum install -y epel-release || true
    sudo yum config-manager --set-enabled powertools 2>/dev/null \
      || sudo yum config-manager --set-enabled PowerTools 2>/dev/null \
      || sudo yum config-manager --set-enabled crb 2>/dev/null \
      || true
    sudo yum install -y \
      rpm-build rpmdevtools createrepo cmake python3 \
      openssl-devel lz4-devel zlib-devel libzstd-devel expat-devel libxml2-devel \
      libcurl-devel \
      perl-libwww-perl perl-LWP-Protocol-https
    sudo yum install -y yum-plugin-priorities 2>/dev/null || true
  fi
}

########################################################################
# 2b) verify a package's declared zimbra-* build-time deps are resolvable
#     (was ci/verify-build-deps.sh) - args: <control/spec file> <field prefix>
########################################################################
verify_build_deps() {
  local file="$1" prefix="$2"
  [ -f "$file" ] || { echo "verify-build-deps: $file not found, skipping"; return 0; }

  # Sibling binaries from the SAME control/spec (e.g. clamav produces both
  # zimbra-clamav and zimbra-clamav-lib) often depend on each other - those
  # are produced by this very build, not external prerequisites.
  local self_pkgs=""
  case "$file" in
    */debian/control)
      self_pkgs="$(grep -E '^Package:' "$file" | awk '{print $2}' | sort -u || true)"
      ;;
    *.spec)
      local base_name
      base_name="$(grep -E '^Name:' "$file" | head -1 | awk '{print $2}')"
      self_pkgs="$base_name"
      while IFS= read -r line; do
        local n
        case "$line" in
          *'-n '*) n="$(sed -E 's/.*-n[[:space:]]+([^[:space:]]+).*/\1/' <<<"$line")" ;;
          *)       n="${base_name}-$(awk '{print $2}' <<<"$line")" ;;
        esac
        [ -n "$n" ] && self_pkgs="$(printf '%s\n%s' "$self_pkgs" "$n")"
      done < <(grep -E '^%package' "$file" || true)
      ;;
  esac
  self_pkgs="$(printf '%s\n' "$self_pkgs" | sed '/^$/d' | sort -u)"
  local is_self_produced_name
  is_self_produced() { [ -n "$self_pkgs" ] && grep -qxF "$1" <<<"$self_pkgs"; }

  local deps_with_versions
  deps_with_versions="$(awk -v prefix="$prefix" '
      $0 ~ "^"prefix":" { flag=1; sub("^"prefix":", ""); print; next }
      flag && /^[A-Za-z][A-Za-z0-9-]*:/ { flag=0 }
      flag { print }
    ' "$file" \
    | tr ',' '\n' \
    | sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//' \
    | grep -E '^zimbra-' || true)"
  [ -z "$deps_with_versions" ] && { echo "verify-build-deps: no internal zimbra- build-time deps declared, skipping"; return 0; }

  # deb/rpm version compare, preferring the platform-native comparator for
  # correct epoch/tilde semantics.
  version_ge() {
    local have="$1" want="$2"
    if command -v dpkg >/dev/null 2>&1; then
      dpkg --compare-versions "$have" ge "$want"
    elif command -v rpmdev-vercmp >/dev/null 2>&1; then
      rpmdev-vercmp "$have" "$want" >/dev/null 2>&1
      local rc=$?
      [ "$rc" = "0" ] || [ "$rc" = "11" ]
    else
      [ "$(printf '%s\n%s\n' "$want" "$have" | sort -V | tail -1)" = "$have" ]
    fi
  }
  installed_version() {
    local name="$1" s
    if command -v dpkg-query >/dev/null 2>&1; then
      s="$(dpkg-query -W -f='${Status} ${Version}' "$name" 2>/dev/null || true)"
      case "$s" in *"ok installed"*) echo "${s##* }" ;; esac
    elif command -v rpm >/dev/null 2>&1; then
      rpm -q "$name" >/dev/null 2>&1 && rpm -q --qf '%{VERSION}-%{RELEASE}' "$name" 2>/dev/null
    fi
  }
  published_version() {
    local name="$1"
    if command -v apt-cache >/dev/null 2>&1; then
      apt-cache madison "$name" 2>/dev/null | awk -F'|' 'NR==1{gsub(/ /,"",$2); print $2}'
    elif command -v yum >/dev/null 2>&1; then
      { yum --showduplicates list available "$name" 2>/dev/null || true; } \
        | awk -v n="$name" '$1==n || index($1, n".")==1 {v=$2} END{print v}'
    fi
  }

  local missing=0
  while IFS= read -r line; do
    [ -n "$line" ] || continue
    local name
    name=$(sed -E 's/[[:space:]]*\(.*//' <<<"$line" | sed -E 's/[[:space:]]*[<>=!].*//')

    if is_self_produced "$name"; then
      echo "verify-build-deps: SKIP  $name (sibling binary package produced by this same build)"
      continue
    fi

    local ver_raw=""
    case "$line" in
      *'('*) ver_raw=$(sed -E 's/.*\(>=?[[:space:]]*([^)]+)\).*/\1/' <<<"$line") ;;
      *)
        ver_raw=$(sed -E 's/^[^><=!]*[><=!]+[[:space:]]*//' <<<"$line")
        [ "$ver_raw" = "$line" ] && ver_raw=""
        ;;
    esac

    if [ -z "$ver_raw" ]; then
      local found_local=0
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

    local ver_want="${ver_raw%%ZAPPEND*}"
    local found_local=0
    if [ -d "$LOCAL_REPO" ]; then
      for f in "$LOCAL_REPO/${name}_"*.deb "$LOCAL_REPO/${name}-"*.rpm; do
        [ -e "$f" ] || continue
        local base ver_have
        base="$(basename "$f")"
        ver_have="${base#${name}[-_]}"
        case "$base" in
          *.deb) ver_have="${ver_have%.deb}"; ver_have="${ver_have%_*}" ;;
          *.rpm) ver_have="${ver_have%.rpm}"; ver_have="${ver_have%.*}" ;;
        esac
        if version_ge "$ver_have" "$ver_want"; then
          found_local=1
          echo "verify-build-deps: OK   $name >= ${ver_want} (built earlier in this job, found ${ver_have})"
          break
        fi
      done
    fi
    [ "$found_local" = "1" ] && continue

    local ver_have
    ver_have="$(installed_version "$name")"
    if [ -n "$ver_have" ] && version_ge "$ver_have" "$ver_want"; then
      echo "verify-build-deps: OK   $name >= ${ver_want} (already installed in image, found ${ver_have})"
      continue
    fi

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
    echo "Must be satisfiable one of 3 ways: built earlier in THIS job, already"
    echo "installed in the image, or published in the zimbra repo. None applied."
    exit 1
  fi
}

########################################################################
# 2e) register a package's just-built .deb/.rpm into the job-local repo,
#     pinned ABOVE the published zimbra repo (was ci/register-local-repo.sh)
#     - arg: <package build dir, e.g. thirdparty/foo/build>
########################################################################
register_local_repo() {
  local pkg_build_dir="$1"
  mkdir -p "$LOCAL_REPO"

  local deb_files rpm_files
  deb_files=$(find "$pkg_build_dir" -name '*.deb' 2>/dev/null || true)
  rpm_files=$(find "$pkg_build_dir" -name '*.rpm' ! -name '*.src.rpm' 2>/dev/null || true)

  if [ -n "$deb_files" ] && command -v dpkg-scanpackages >/dev/null 2>&1; then
    cp $deb_files "$LOCAL_REPO/"
    ( cd "$LOCAL_REPO" && dpkg-scanpackages . /dev/null 2>/dev/null | gzip -9c > Packages.gz )
    if [ ! -f /etc/apt/sources.list.d/local-build.list ]; then
      echo "deb [trusted=yes] file:$LOCAL_REPO ./" | sudo tee /etc/apt/sources.list.d/local-build.list >/dev/null
      printf 'Package: *\nPin: origin ""\nPin-Priority: 1001\n' | sudo tee /etc/apt/preferences.d/local-build >/dev/null
    fi
    # Scoped refresh only (file://, instant) - never touch zimbra.list's index.
    sudo apt-get update -qq \
      -o Dir::Etc::sourcelist="sources.list.d/local-build.list" \
      -o Dir::Etc::sourceparts="-" \
      -o APT::Get::List-Cleanup="0"
    echo "register-local-repo: added $(wc -w <<<"$deb_files") deb(s) to $LOCAL_REPO"
  fi

  if [ -n "$rpm_files" ]; then
    local createrepo_bin=""
    if command -v createrepo_c >/dev/null 2>&1; then createrepo_bin="createrepo_c"
    elif command -v createrepo >/dev/null 2>&1; then createrepo_bin="createrepo"; fi
    if [ -n "$createrepo_bin" ]; then
      cp $rpm_files "$LOCAL_REPO/"
      "$createrepo_bin" --update "$LOCAL_REPO" >/dev/null
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
      sudo yum makecache -y --disablerepo="*" --enablerepo="local-build" >/dev/null 2>&1 || true
      echo "register-local-repo: added $(wc -w <<<"$rpm_files") rpm(s) to $LOCAL_REPO"
    else
      echo "register-local-repo: WARNING - neither createrepo_c nor createrepo found, skipping RPM registration" >&2
    fi
  fi
}

########################################################################
# 2c) install a package's declared build-time deps (name only, no version -
#     verify_build_deps above already confirmed the version is satisfied)
########################################################################
install_declared_build_deps() {
  local file="$1" label="$2" prefix="$3"; shift 3
  local deps
  deps=$(awk -v prefix="$prefix" '
      $0 ~ "^"prefix":" { flag=1; sub("^"prefix":", ""); print; next }
      flag && /^[A-Za-z][A-Za-z0-9-]*:/ { flag=0 }
      flag { print }
    ' "$file" \
    | tr ',' '\n' \
    | sed -E 's/\(.*\)//; s/[<>=!].*//; s/^[[:space:]]+//; s/[[:space:]]+$//' \
    | grep -v '^$' \
    | sort -u || true)
  if [ -n "$deps" ]; then
    echo "Installing ${label} build-deps: ${deps}"
    "$@" $deps
  else
    echo "No ${label} build-deps declared for ${file}, skipping install"
  fi
}

########################################################################
# main
########################################################################
echo "=== Installing build tooling + baseline dev libraries ==="
install_build_tooling

export PKG_CONFIG_PATH="/opt/zimbra/common/lib/pkgconfig:${PKG_CONFIG_PATH:-}"
mkdir -p "build/dist_workspace/${PLATFORM_TAG}"

total="$(grep -c . "$INPUT" || true)"
n=0

while IFS= read -r PKGPATH; do
  [ -n "$PKGPATH" ] || continue
  n=$((n + 1))

  echo ""
  echo "############################################################"
  echo "###  [${n}/${total}] Building ${PKGPATH}   (platform: ${PLATFORM_TAG})"
  echo "############################################################"

  if [ ! -d "$PKGPATH" ]; then
    echo "ERROR: $PKGPATH does not exist"
    exit 1
  fi

  PRE_HOOK="${PKGPATH}/ci/pre_build.sh"
  if [ -x "$PRE_HOOK" ]; then
    echo "--- [${n}/${total}] ${PKGPATH}: running pre-build hook ---"
    "$PRE_HOOK" "${PLATFORM_TAG}"
  fi

  CONTROL_FILE=$(find "$PKGPATH" -path "*/debian/control" 2>/dev/null | head -1)
  if [ -n "$CONTROL_FILE" ] && command -v apt-get >/dev/null 2>&1; then
    verify_build_deps "$CONTROL_FILE" "Build-Depends"
    install_declared_build_deps "$CONTROL_FILE" "Debian" "Build-Depends" \
      sudo apt-get install -y --no-install-recommends
  fi

  SPEC_FILE=$(find "$PKGPATH" -path "*/SPECS/*.spec" 2>/dev/null | head -1)
  if [ -n "$SPEC_FILE" ] && command -v yum >/dev/null 2>&1; then
    verify_build_deps "$SPEC_FILE" "BuildRequires"
    install_declared_build_deps "$SPEC_FILE" "RPM" "BuildRequires" \
      sudo yum install -y
  fi

  echo "--- [${n}/${total}] ${PKGPATH}: make ---"
  ( cd "$PKGPATH" && make )

  register_local_repo "${PKGPATH}/build"

  find "${PKGPATH}/build" -type f \
    \( -name "*.deb" -o -name "*.rpm" \) ! -name "*.src.rpm" \
    -exec cp {} "build/dist_workspace/${PLATFORM_TAG}/" \;

  echo "--- [${n}/${total}] ${PKGPATH}: done ---"
done < "$INPUT"

echo ""
echo "=== build/dist_workspace/${PLATFORM_TAG} contents ==="
ls -la "build/dist_workspace/${PLATFORM_TAG}/"
