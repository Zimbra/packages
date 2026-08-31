#!/usr/bin/env bash
# Path in repo: ci/generate-dependency-graph.sh
#
# One-time-per-run scan: walks every package in build-order, extracts
# produced names, build-time deps (WITH version constraints), and
# reverse-index consumers - reusing the same parsing rules as
# resolve-build-order.sh, but keeping the version string alongside
# each name instead of stripping it.
#
# This does NOT change what gets built - it only pre-computes what
# resolve-build-order.sh currently re-discovers by scanning files live
# on every run, so lookups become instant instead of grep-heavy.

set -euo pipefail

BUILD_ORDER="${BUILD_ORDER_FILE:-build-order}"
OUT="${1:-dependency-graph.json}"

find_control_file() { find "$1" -path "*/debian/control" 2>/dev/null | head -1; }
find_spec_file()    { find "$1" -path "*/SPECS/*.spec"    2>/dev/null | head -1; }

# --- identical to resolve-build-order.sh's produced_names() -------------
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

# --- raw (un-stripped) comma-split tokens from a field block ------------
# Emits one dependency TOKEN per line, still carrying its version
# constraint if it has one, e.g.:
#   "zimbra-openssl-devel >= 3.0.9-1zimbra8.8b1ZAPPEND"   (rpm form)
#   "zimbra-openssl-dev (>= 3.0.9-1zimbra8.8b1ZAPPEND)"   (deb form)
#   "zimbra-libxml2-dev"                                   (no constraint)
raw_field_tokens() {
  local file="$1" field="$2"
  [ -n "$file" ] || return 0
  awk -v f="$field" '
      $0 ~ "^"f":" { flag=1; sub("^"f":", ""); print; next }
      flag && /^[A-Za-z][A-Za-z0-9-]*:/ { flag=0 }
      flag { print }
    ' "$file" \
    | tr ',' '\n' \
    | sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//' \
    | awk 'NF' \
    || true
}

# --- split a raw token into "name<TAB>version" (version may be empty) ---
split_name_version() {
  while IFS= read -r tok; do
    [ -n "$tok" ] || continue
    local name="" ver=""
    case "$tok" in
      *'('*)
        name="$(sed -E 's/^([^[:space:](]+).*/\1/' <<<"$tok")"
        ver="$(sed -E 's/.*\(([^)]*)\).*/\1/' <<<"$tok")"
        ;;
      *[\<\>=]*)
        name="$(sed -E 's/^([^[:space:]<>=!]+).*/\1/' <<<"$tok")"
        ver="$(sed -E 's/^[^<>=!]*([<>=!].*)$/\1/' <<<"$tok")"
        ;;
      *)
        name="$tok"
        ;;
    esac
    ver="${ver%%ZAPPEND*}"
    ver="$(sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//' <<<"$ver")"
    case "$name" in
      zimbra-*) printf '%s\t%s\n' "$name" "$ver" ;;
    esac
  done
}

# Build-time deps (Build-Depends / BuildRequires), name+version, for
# BOTH flavours - each package's spec/control declares its own naming,
# so we capture both and let the consumer pick the flavour that matches
# the container it's building in (same reasoning as resolve-build-order.sh).
build_deps_versioned() {
  local pkgpath="$1" flavor="$2" file="" field=""
  case "$flavor" in
    deb) file="$(find_control_file "$pkgpath")"; field="Build-Depends" ;;
    rpm) file="$(find_spec_file "$pkgpath")";    field="BuildRequires" ;;
  esac
  raw_field_tokens "$file" "$field" | split_name_version
}

# ALL declared deps (Depends/Requires + Build-Depends/BuildRequires),
# name+version, unioned across deb+rpm - used ONLY to build the
# reverse_index (same reasoning as declared_dep_names() in
# resolve-build-order.sh: reverse matching must catch a consumer no
# matter which naming scheme it used).
all_declared_versioned() {
  local pkgpath="$1" cf sf
  cf="$(find_control_file "$pkgpath")"
  sf="$(find_spec_file "$pkgpath")"
  {
    raw_field_tokens "$cf" "Depends"
    raw_field_tokens "$cf" "Build-Depends"
    raw_field_tokens "$sf" "Requires"
    raw_field_tokens "$sf" "BuildRequires"
  } | split_name_version | sort -u
}

json_dep_map() {
  # stdin: "name<TAB>version" lines -> JSON object { "name": "version", ... }
  local first=1
  printf '{'
  while IFS=$'\t' read -r name ver; do
    [ -n "$name" ] || continue
    [ "$first" = 1 ] || printf ','
    printf '"%s":"%s"' "$name" "$ver"
    first=0
  done
  printf '}'
}

json_array() {
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
    deb_deps_vt="$(build_deps_versioned "$pkg" deb)"
    rpm_deps_vt="$(build_deps_versioned "$pkg" rpm)"
    all_vt="$(all_declared_versioned "$pkg")"

    # feed the reverse index using names only (version not needed for
    # "who consumes me" lookup)
    while IFS=$'\t' read -r name _ver; do
      [ -n "$name" ] || continue
      reverse_map["$name"]="${reverse_map[$name]:-}"$'\n'"$pkg"
    done <<< "$all_vt"

    printf '    "%s": {\n' "$pkg"
    printf '      "produces": %s,\n' "$(json_array <<< "$produces")"
    printf '      "build_requires_deb": %s,\n' "$(json_dep_map <<< "$deb_deps_vt")"
    printf '      "build_requires_rpm": %s,\n' "$(json_dep_map <<< "$rpm_deps_vt")"
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
