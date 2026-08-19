#!/usr/bin/env bash
# Path in repo: ci/resolve-build-order.sh
#
# Called as: bash ci/resolve-build-order.sh packages_to_build.txt
#
# 1) Expands the list: if a package in the list is a declared dependency
#    of some OTHER thirdparty package (via that package's
#    ci/build-deps.txt), pulls that other package into the list too.
#    -> e.g. only openssl changed => nginx gets auto-added, since
#       thirdparty/nginx/ci/build-deps.txt says it needs openssl.
# 2) Topologically sorts the final list so a dependency always builds
#    before whatever depends on it.
#
# Convention: thirdparty/<pkg>/ci/build-deps.txt is OPTIONAL. One
# thirdparty/<folder-name> per line. No file / empty file = no internal
# deps for that package. This file never touches config.yml.
set -euo pipefail

INPUT="${1:-packages_to_build.txt}"
[ -s "$INPUT" ] || { echo "resolve-build-order: $INPUT is empty, nothing to do"; exit 0; }

declare -A seen=()
queue=()
while IFS= read -r p; do
  [ -n "$p" ] || continue
  queue+=("$p"); seen["$p"]=1
done < "$INPUT"

# --- expand: pull in reverse-dependents that reference already-queued pkgs
i=0
while [ "$i" -lt "${#queue[@]}" ]; do
  pkg="${queue[$i]}"; i=$((i+1))
  for cand_deps_file in thirdparty/*/ci/build-deps.txt; do
    [ -f "$cand_deps_file" ] || continue
    cand_pkg="$(basename "$(dirname "$(dirname "$cand_deps_file")")")"
    if grep -qxF "$pkg" "$cand_deps_file" 2>/dev/null && [ -z "${seen[$cand_pkg]:-}" ]; then
      seen["$cand_pkg"]=1
      queue+=("$cand_pkg")
      echo "resolve-build-order: auto-adding '$cand_pkg' (depends on changed package '$pkg')"
    fi
  done
done

# --- build edge list "dep pkg" for tsort (dep must come before pkg) -----
edges_file="$(mktemp)"
has_edges=0
for pkg in "${queue[@]}"; do
  deps_file="thirdparty/${pkg}/ci/build-deps.txt"
  [ -f "$deps_file" ] || continue
  while IFS= read -r dep; do
    dep="$(sed -e 's/#.*$//' -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' <<<"$dep")"
    [ -n "$dep" ] || continue
    echo "$dep $pkg" >> "$edges_file"
    has_edges=1
  done < "$deps_file"
done

if [ "$has_edges" = "1" ]; then
  if ! tsort "$edges_file" > "$INPUT.sorted" 2>/tmp/tsort.err; then
    echo "ERROR: circular dependency among thirdparty packages:"
    cat /tmp/tsort.err
    exit 1
  fi
else
  : > "$INPUT.sorted"
fi
rm -f "$edges_file"

# tsort output first (correct order), then any isolated packages appended
{ cat "$INPUT.sorted"; printf '%s\n' "${queue[@]}"; } | awk '!seen[$0]++' > "$INPUT"
rm -f "$INPUT.sorted"

echo "=== Build order after dependency resolution ==="
cat "$INPUT"
