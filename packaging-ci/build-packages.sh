#!/usr/bin/env bash
# Path in repo: packaging-ci/build-packages.sh
# This script builds the resolved package list for one platform. It installs only
# the base tools the pipeline itself needs. Package-specific build deps still come
# from each package manifest or Makefile.

set -euo pipefail

SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/$(basename "${BASH_SOURCE[0]}")"

install_package_deps() {
  [ "$#" -gt 0 ] || return 0

  local output rc
  local -a install_cmd
  if command -v apt-get >/dev/null 2>&1; then
    install_cmd=(
      sudo env DEBIAN_FRONTEND=noninteractive
      apt-get -qq --assume-yes --no-install-recommends
      -o Dpkg::Use-Pty=0 install
    )
  elif command -v yum >/dev/null 2>&1; then
    install_cmd=(sudo yum -q -y install)
  else
    echo "ERROR: neither apt-get nor yum is available to install dependencies" >&2
    return 1
  fi

  if output="$("${install_cmd[@]}" "$@" 2>&1)"; then
    echo "${DEP_CONTEXT:-Dependencies} ready: $*"
    return 0
  else
    rc=$?
  fi

  echo "ERROR: failed to install dependencies: $*" >&2
  printf '%s\n' "$output" >&2
  return "$rc"
}

if [ "${1:-}" = "--install-deps" ]; then
  shift
  install_package_deps "$@"
  exit
fi

: "${PLATFORM_TAG:?PLATFORM_TAG must be set}"
INPUT="${1:-packages_to_build.txt}"
LOCAL_REPO="${LOCAL_REPO:-/tmp/local-pkg-repo}"

[ -s "$INPUT" ] || { echo "build: $INPUT is empty, nothing to build"; exit 0; }

manifest_field() {
  local file="$1" prefix="$2"
  awk -v prefix="$prefix" '
      $0 ~ "^"prefix":" { flag=1; sub("^"prefix":", ""); print; next }
      flag && /^[A-Za-z][A-Za-z0-9-]*:/ { flag=0 }
      flag { print }
    ' "$file"
}

filter_apt_output() {
  tr -d '\000' \
    | grep -Ev "NO_PUBKEY 5234D2B73B6996C7|^$" \
    || true
}

apt_update() {
  local rc
  set +e
  sudo env DEBIAN_FRONTEND=noninteractive apt-get update -qq "$@" 2>&1 \
    | filter_apt_output
  rc="${PIPESTATUS[0]}"
  set -e
  return "$rc"
}

have_deb_build_tools() {
  command -v dpkg-buildpackage >/dev/null 2>&1 \
    && command -v dpkg-scanpackages >/dev/null 2>&1 \
    && command -v gcc >/dev/null 2>&1 \
    && command -v g++ >/dev/null 2>&1 \
    && command -v make >/dev/null 2>&1
}

have_rpm_build_tools() {
  command -v rpmbuild >/dev/null 2>&1 \
    && { command -v createrepo_c >/dev/null 2>&1 || command -v createrepo >/dev/null 2>&1; }
}

install_build_tooling() {
  if command -v apt-get >/dev/null 2>&1; then
    export DEBIAN_FRONTEND=noninteractive
    printf 'APT::Install-Recommends "false";\n' \
      | sudo tee /etc/apt/apt.conf.d/99-no-install-recommends >/dev/null
    apt_update

    if have_deb_build_tools; then
      echo "Build environment ready: Debian tools already installed"
      return 0
    fi

    local missing=()
    if ! command -v dpkg-buildpackage >/dev/null 2>&1 || ! command -v dpkg-scanpackages >/dev/null 2>&1; then
      missing+=("dpkg-dev")
    fi
    if ! command -v gcc >/dev/null 2>&1 || ! command -v g++ >/dev/null 2>&1 || ! command -v make >/dev/null 2>&1; then
      missing+=("build-essential")
    fi
    [ "${#missing[@]}" -eq 0 ] || install_package_deps "${missing[@]}"
  elif command -v yum >/dev/null 2>&1; then
    OS_VERSION=$(rpm -E %{rhel})
    if [ "$OS_VERSION" = "8" ]; then
      sudo sed -i \
        -e 's/^mirrorlist=/#mirrorlist=/' \
        -e 's/^metalink=/#metalink=/' \
        -e 's|^#baseurl=http://mirror.centos.org|baseurl=https://vault.centos.org|' \
        /etc/yum.repos.d/*.repo
    fi

    if have_rpm_build_tools; then
      echo "Build environment ready: RPM tools already installed"
      return 0
    fi

    local missing=()
    command -v rpmbuild >/dev/null 2>&1 || missing+=("rpm-build")
    if ! command -v createrepo_c >/dev/null 2>&1 && ! command -v createrepo >/dev/null 2>&1; then
      if ! sudo yum install -y --setopt=install_weak_deps=False "${missing[@]}" createrepo_c; then
        sudo yum install -y --setopt=install_weak_deps=False "${missing[@]}" createrepo
      fi
    elif [ "${#missing[@]}" -gt 0 ]; then
      sudo yum install -y --setopt=install_weak_deps=False "${missing[@]}"
    fi
  fi
}

# Verify that declared zimbra-* build dependencies can be resolved.
verify_build_deps() {
  local file="$1" prefix="$2"
  [ -f "$file" ] || { echo "verify-build-deps: $file not found, skipping"; return 0; }

  # Sibling packages from the same manifest are produced by the same build.
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
  is_self_produced() { [ -n "$self_pkgs" ] && grep -qxF "$1" <<<"$self_pkgs"; }

  local deps_with_versions
  deps_with_versions="$(manifest_field "$file" "$prefix" \
    | tr ',' '\n' \
    | sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//' \
    | grep -E '^zimbra-' || true)"
  [ -z "$deps_with_versions" ] && return 0

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
    ver_have="$(installed_version "$name")" || true
    if [ -n "$ver_have" ] && version_ge "$ver_have" "$ver_want"; then
      echo "verify-build-deps: OK   $name >= ${ver_want} (already installed in image, found ${ver_have})"
      continue
    fi

    ver_have="$(published_version "$name")" || true
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

# Add fresh packages to a local repo so later packages in the same job can use them.
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
    apt_update \
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

# Install only non-zimbra build deps from the manifest.
install_declared_build_deps() {
  local file="$1" label="$2" prefix="$3"
  local deps
  deps=$(manifest_field "$file" "$prefix" \
    | tr ',' '\n' \
    | sed -E 's/\(.*\)//; s/[<>=!].*//; s/^[[:space:]]+//; s/[[:space:]]+$//' \
    | grep -v '^$' \
    | grep -v '^zimbra-' \
    | sort -u || true)
  if [ -n "$deps" ]; then
    DEP_CONTEXT="${label} build dependencies" install_package_deps $deps
  fi
}

# If a package installs its own deps in pkgadd_deb/pkgadd_rpm, skip the generic install.
is_migrated_pkgadd() {
  local pkgpath="$1" target="$2" makefile="${pkgpath}/Makefile"
  [ -f "$makefile" ] && grep -qE "^${target}:" "$makefile"
}

handle_build_deps() {
  local pkgpath="$1" file field label
  if command -v apt-get >/dev/null 2>&1; then
    file=$(find "$pkgpath" -path "*/debian/control" 2>/dev/null | head -1)
    field="Build-Depends"; label="Debian"
    [ -n "$file" ] || return 0
    verify_build_deps "$file" "$field"
    if is_migrated_pkgadd "$pkgpath" "pkgadd_deb"; then
      echo "handle_build_deps: ${pkgpath}/Makefile defines pkgadd_deb - it installs its own build-time deps via pkgadd, skipping generic install to avoid a duplicate"
      return 0
    fi
    install_declared_build_deps "$file" "$label" "$field"
  elif command -v yum >/dev/null 2>&1; then
    file=$(find "$pkgpath" -path "*/SPECS/*.spec" 2>/dev/null | head -1)
    field="BuildRequires"; label="RPM"
    [ -n "$file" ] || return 0
    verify_build_deps "$file" "$field"
    if is_migrated_pkgadd "$pkgpath" "pkgadd_rpm"; then
      echo "handle_build_deps: ${pkgpath}/Makefile defines pkgadd_rpm - it installs its own build-time deps via pkgadd, skipping generic install to avoid a duplicate"
      return 0
    fi
    install_declared_build_deps "$file" "$label" "$field"
  fi
}

########################################################################
# main
########################################################################
install_build_tooling

export PKG_CONFIG_PATH="/opt/zimbra/common/lib/pkgconfig:${PKG_CONFIG_PATH:-}"

# Some packages do not build reliably with link-time optimization on newer Ubuntu.
if command -v apt-get >/dev/null 2>&1; then
  export DEB_BUILD_OPTIONS="${DEB_BUILD_OPTIONS:+$DEB_BUILD_OPTIONS }nolto"
  echo "Debian compatibility: link-time optimization disabled"
fi

mkdir -p "build/dist_workspace/${PLATFORM_TAG}"

make_args=()
make_args+=("PKG_EXTRACT=@bash ${SCRIPT_PATH} --install-deps")
if command -v yum >/dev/null 2>&1; then
  make_args+=('PKG_BUILD=rpmbuild --define "_topdir $$PWD" -ba')
fi

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

  handle_build_deps "$PKGPATH"

  echo "--- [${n}/${total}] ${PKGPATH}: make ---"
  ( cd "$PKGPATH" && make "${make_args[@]}" )

  register_local_repo "${PKGPATH}/build"

  find "${PKGPATH}/build" -type f \
    \( -name "*.deb" -o -name "*.rpm" \) ! -name "*.src.rpm" \
    -exec cp {} "build/dist_workspace/${PLATFORM_TAG}/" \;

  echo "--- [${n}/${total}] ${PKGPATH}: done ---"
done < "$INPUT"

echo ""
echo "=== build/dist_workspace/${PLATFORM_TAG} contents ==="
ls -la "build/dist_workspace/${PLATFORM_TAG}/"
