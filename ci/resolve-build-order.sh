#!/usr/bin/env bash
# Path in repo: ci/resolve-build-order.sh
#
# Called as: bash ci/resolve-build-order.sh packages_to_build.txt
#
# NO per-package ci/build-deps.txt file is used anywhere in this script.
# Every internal zimbra-* dependency a package has is ALREADY declared in
# that package's own debian/control (Depends:/Build-Depends:) or .spec
# (Requires:/BuildRequires:) file - that's the single, authoritative
# source of truth the package's real build already relies on. Keeping a
# second, hand-maintained per-package text file duplicating the same
# information is unnecessary and drifts out of sync over time. This
# script reads directly from those real files instead.
#
# This script does exactly TWO things:
#
#   1) EXPAND: figure out which OTHER packages depend on a package that
#      just changed (reverse-dependents), so they get rebuilt too.
#        a. For each changed package, find every binary package NAME it
#           actually produces (e.g. thirdparty/clamav produces
#           zimbra-clamav, zimbra-clamav-lib, zimbra-clamav-dev, ...) -
#           read straight from its own debian/control "Package:" lines
#           and/or .spec "Name:"/"%package" lines.
#        b. Scan every OTHER package's debian/control and .spec files
#           for a Depends:/Build-Depends:/Requires:/BuildRequires: entry
#           that exactly matches one of those produced names (e.g.
#           zimbra/mta-components' control file lists "zimbra-clamav" in
#           its Depends: field) - if found, that package is a reverse
#           dependent and gets pulled into this run too.
#        c. Repeat until no new package gets pulled in, so transitive
#           chains work (A's rebuild pulls in B, B's rebuild pulls in C).
#
#   2) ORDER: sort the expanded list to match ci/build-order.txt's
#      sequence (the same proven order used on genesis), so dependencies
#      always build before whatever needs them.
set -euo pipefail
INPUT="${1:-packages_to_build.txt}"
BUILD_ORDER="${BUILD_ORDER_FILE:-build-order}"

[ -s "$INPUT" ] || { echo "resolve-build-order: $INPUT is empty, nothing to do"; exit 0; }
[ -f "$BUILD_ORDER" ] || {
  echo "resolve-build-order: ERROR - $BUILD_ORDER not found. This is the master build-order list and is required."
  exit 1
}

# --- every real package path, taken straight from the master order list -
master_pkgs="$(grep -vE '^[[:space:]]*(#|$)' "$BUILD_ORDER" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"

# --- find a package's control/spec files (mirrors config.yml's own find)
find_control_file() { find "$1" -path "*/debian/control" 2>/dev/null | head -1; }
find_spec_file()    { find "$1" -path "*/SPECS/*.spec"    2>/dev/null | head -1; }

# --- every binary package NAME this package produces --------------------
produced_names() {
  local pkgpath="$1" cf sf names=""
  cf="$(find_control_file "$pkgpath")"
  if [ -n "$cf" ]; then
    names="$(grep -E '^Package:' "$cf" | awk '{print $2}')"
  fi
  sf="$(find_spec_file "$pkgpath")"
  if [ -n "$sf" ]; then
    base_name="$(grep -E '^Name:' "$sf" | head -1 | awk '{print $2}')"
    sub_names="$base_name"
    while IFS= read -r line; do
      case "$line" in
        *'-n '*) n="$(sed -E 's/.*-n[[:space:]]+([^[:space:]]+).*/\1/' <<<"$line")" ;;
        *)       n="${base_name}-$(awk '{print $2}' <<<"$line")" ;;
      esac
      [ -n "$n" ] && sub_names="$(printf '%s\n%s' "$sub_names" "$n")"
    done < <(grep -E '^%package' "$sf" || true)
    names="$(printf '%s\n%s' "$names" "$sub_names")"
  fi
  printf '%s\n' "$names" | sed '/^$/d' | sort -u
}

# --- every zimbra-* dependency NAME this package declares (any field,
#     any stanza - build-time and runtime both count as a relationship) -
declared_dep_names() {
  local pkgpath="$1" cf sf
  cf="$(find_control_file "$pkgpath")"
  sf="$(find_spec_file "$pkgpath")"
  {
    # NOTE: each check is "|| true" - a package legitimately missing a
    # control or spec file makes "[ -n "$cf" ] &&/-n "$sf" ] &&" itself
    # exit non-zero (since && short-circuits to false), and under
    # `set -e` + pipefail that would silently kill this whole script the
    # moment it hit a package with only ONE of the two file types (this
    # is the exact same class of bug noted in verify-build-deps.sh).
    [ -n "$cf" ] && awk '
        /^(Build-)?Depends:/ { flag=1; sub(/^[A-Za-z-]+:/, ""); print; next }
        flag && /^[A-Za-z][A-Za-z0-9-]*:/ { flag=0 }
        flag { print }
      ' "$cf"
    [ -n "$sf" ] && awk '
        /^(Build)?Requires:/ { flag=1; sub(/^[A-Za-z]+:/, ""); print; next }
        flag && /^[A-Za-z][A-Za-z0-9-]*:/ { flag=0 }
        flag { print }
      ' "$sf"
    true
  } 2>/dev/null \
    | tr ',' '\n' \
    | sed -E 's/\(.*\)//; s/[<>=!].*//; s/^[[:space:]]+//; s/[[:space:]]+$//' \
    | grep -E '^zimbra-' \
    | sort -u
}

declare -A seen=()
queue=()
while IFS= read -r p; do
  [ -n "$p" ] || continue
  queue+=("$p"); seen["$p"]=1
done < "$INPUT"

# --- expand: repeat until no new reverse-dependent gets pulled in -------
i=0
while [ "$i" -lt "${#queue[@]}" ]; do
  pkg="${queue[$i]}"; i=$((i+1))
  [ -d "$pkg" ] || continue

  this_names="$(produced_names "$pkg")"
  [ -n "$this_names" ] || continue

  while IFS= read -r cand_pkg; do
    [ -n "$cand_pkg" ] || continue
    [ -n "${seen[$cand_pkg]:-}" ] && continue
    [ "$cand_pkg" = "$pkg" ] && continue
    [ -d "$cand_pkg" ] || continue

    cand_deps="$(declared_dep_names "$cand_pkg")"
    [ -n "$cand_deps" ] || continue

    while IFS= read -r name; do
      [ -n "$name" ] || continue
      if grep -qxF "$name" <<<"$this_names"; then
        seen["$cand_pkg"]=1
        queue+=("$cand_pkg")
        echo "resolve-build-order: auto-adding '$cand_pkg' (depends on '$name', produced by changed package '$pkg')"
        break
      fi
    done <<< "$cand_deps"
  done <<< "$master_pkgs"
done

# --- order the queue by position in the master build-order list --------
bad=0
ordered_file="$(mktemp)"
for pkg in "${queue[@]}"; do
  idx="$(grep -nxF "$pkg" <<<"$master_pkgs" | head -1 | cut -d: -f1)"
  if [ -z "$idx" ]; then
    echo "resolve-build-order: ERROR '$pkg' is not listed in $BUILD_ORDER - add it there before it can be built."
    bad=1; continue
  fi
  if [ ! -d "$pkg" ] || [ ! -f "$pkg/Makefile" ]; then
    echo "resolve-build-order: ERROR '$pkg' is not a valid package directory (missing dir or Makefile)."
    bad=1; continue
  fi
  echo "$idx $pkg" >> "$ordered_file"
done

if [ "$bad" -eq 1 ]; then
  echo ""
  echo "ERROR: resolve-build-order found one or more unresolvable packages - aborting before build."
  rm -f "$ordered_file"
  exit 1
fi

sort -n "$ordered_file" | awk '{print $2}' > "$INPUT"
rm -f "$ordered_file"

echo "=== Build order after dependency resolution ==="
cat "$INPUT"
