#!/usr/bin/env bash
# Path in repo: ci/generate-dependency-graph.sh
#
# One-time-per-run scan: walks every package in build-order, extracts
# produced names, build-time deps, and all declared deps (reusing the
# exact same parsing rules as resolve-build-order.sh), and writes it
# all out as a single dependency-graph.json.
#
# This does NOT change what gets built - it only pre-computes what
# resolve-build-order.sh currently re-discovers by scanning files live
# on every run, so lookups become instant instead of grep-heavy.

set -euo pipefail

BUILD_ORDER="${BUILD_ORDER_FILE:-build-order}"
OUT="${1:-dependency-graph.json}"

find_control_file() { find "$1" -path "*/debian/control" 2>/dev/null | head -1; }
find_spec_file()    { find "$1" -path "*/SPECS/*.spec"    2>/dev/null | head -1; }

# --- identical logic to resolve-build-order.sh's produced_names() -------
produced_names() {
  local pkgpath="$1" cf sf names=""
  cf="$(find_control_file "$pkgpath")"
  [ -n "$cf" ] && names="$(grep -E '^Package:' "$cf" | awk '{print $2}' || true)"
  sf="$(find_spec_file "$pkgpath")"
  if [ -n "$sf" ]; then
    base_name="$(grep -E '^Name:' "$sf" | head -1 | awk '{print $2}' || true)"
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
  printf '%s\n' "$names" | sed '/^$/d' | sort -u || true
}

# --- identical logic to declared_dep_names() (unioned, reverse-match use) -
declared_dep_names() {
  local pkgpath="$1" cf sf
  cf="$(find_control_file "$pkgpath")"
  sf="$(find_spec_file "$pkgpath")"
  {
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
    | grep -E '^zimbra-' | sort -u || true
}

# --- deb build-time deps only (Build-Depends) ---------------------------
deb_build_deps() {
  local cf; cf="$(find_control_file "$1")"; [ -n "$cf" ] || return 0
  awk '
      /^Build-Depends:/ { flag=1; sub(/^Build-Depends:/, ""); print; next }
      flag && /^[A-Za-z][A-Za-z0-9-]*:/ { flag=0 }
      flag && /^[[:space:]]/ { print }
    ' "$cf" | tr ',' '\n' \
    | sed -E 's/\(.*\)//; s/\[.*\]//; s/[<>=!].*//; s/^[[:space:]]+//; s/[[:space:]]+$//' \
    | awk 'NF' | grep -E '^zimbra-' | sort -u || true
}

# --- rpm build-time deps only (BuildRequires) ----------------------------
rpm_build_deps() {
  local sf; sf="$(find_spec_file "$1")"; [ -n "$sf" ] || return 0
  awk '
      /^BuildRequires:/ { flag=1; sub(/^BuildRequires:/, ""); print; next }
      flag && /^[A-Za-z][A-Za-z0-9-]*:/ { flag=0 }
      flag && /^[[:space:]]/ { print }
    ' "$sf" | tr ',' '\n' \
    | sed -E 's/\(.*\)//; s/\[.*\]//; s/[<>=!].*//; s/^[[:space:]]+//; s/[[:space:]]+$//' \
    | awk 'NF' | grep -E '^zimbra-' | sort -u || true
}

json_array() {
  # turn newline-separated input into a JSON string array
  local first=1
  printf '['
  while IFS= read -r item; do
    [ -n "$item" ] || continue
    [ "$first" = 1 ] || printf ','
    printf '"%s"' "$item"
    first=0
  done
  printf ']'
}

master_pkgs="$(grep -vE '^[[:space:]]*(#|$)' "$BUILD_ORDER" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"

# Build reverse_index[name] = [package1, package2, ...] as we go
declare -A reverse_map=()

{
  echo "{"
  echo "  \"generated_from\": \"${BUILD_ORDER}\","
  echo "  \"packages\": {"

  idx=0
  count=$(wc -l <<< "$master_pkgs")
  while IFS= read -r pkg; do
    [ -n "$pkg" ] || continue
    [ -d "$pkg" ] || continue
    idx=$((idx+1))

    produces="$(produced_names "$pkg")"
    deb_deps="$(deb_build_deps "$pkg")"
    rpm_deps="$(rpm_build_deps "$pkg")"
    all_deps="$(declared_dep_names "$pkg")"

    # feed the reverse index: for every name this package declares
    # (deb+rpm, runtime+build), record "consumers of that name include $pkg"
    while IFS= read -r dep; do
      [ -n "$dep" ] || continue
      reverse_map["$dep"]="${reverse_map[$dep]:-}"$'\n'"$pkg"
    done <<< "$all_deps"

    printf '    "%s": {\n' "$pkg"
    printf '      "produces": %s,\n' "$(json_array <<< "$produces")"
    printf '      "build_time_deps_deb": %s,\n' "$(json_array <<< "$deb_deps")"
    printf '      "build_time_deps_rpm": %s,\n' "$(json_array <<< "$rpm_deps")"
    printf '      "declared_deps_all": %s,\n' "$(json_array <<< "$all_deps")"
    printf '      "build_order_index": %s\n' "$idx"
    if [ "$idx" -lt "$count" ]; then
      printf '    },\n'
    else
      printf '    }\n'
    fi
  done <<< "$master_pkgs"

  echo "  },"
  echo "  \"reverse_index\": {"

  keys=("${!reverse_map[@]}")
  klen=${#keys[@]}
  for i in "${!keys[@]}"; do
    name="${keys[$i]}"
    consumers="$(printf '%s\n' "${reverse_map[$name]}" | sed '/^$/d' | sort -u)"
    printf '    "%s": %s' "$name" "$(json_array <<< "$consumers")"
    if [ "$i" -lt $((klen-1)) ]; then printf ',\n'; else printf '\n'; fi
  done

  echo "  }"
  echo "}"
} > "$OUT"

echo "generate-dependency-graph: wrote $OUT ($(wc -l < "$OUT") lines)"
