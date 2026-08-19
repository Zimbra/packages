#!/usr/bin/env bash
# Path in repo: ci/resolve-build-order.sh
#
# Called as: bash ci/resolve-build-order.sh packages_to_build.txt
#
# Entries in the input file are FULL relative paths (e.g. "thirdparty/
# nginx" or "zimbra/osl") - not bare names. This is what lets any
# top-level root (thirdparty/, zimbra/, or a future one) work without
# ever touching config.yml: the path itself is the package's identity.
#
# 1) Expands the list: if a package is a declared dependency of some
#    OTHER package (via that package's own ci/build-deps.txt, which
#    also lists full paths), pulls that other package in too.
# 2) Topologically sorts the final list so a dependency always builds
#    before whatever depends on it.
#
# Convention: <root>/<pkg>/ci/build-deps.txt is OPTIONAL. One full
# path (e.g. "thirdparty/openssl") per line. No file / empty file =
# no internal deps for that package.
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
  for cand_deps_file in */*/ci/build-deps.txt; do
    [ -f "$cand_deps_file" ] || continue
    # strip trailing "/ci/build-deps.txt" -> gives the full path pkg id
    cand_pkg="${cand_deps_file%/ci/build-deps.txt}"
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
  deps_file="${pkg}/ci/build-deps.txt"
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
    echo "ERROR: circular dependency among packages:"
    cat /tmp/tsort.err
    exit 1
  fi
else
  : > "$INPUT.sorted"
fi
rm -f "$edges_file"

{ cat "$INPUT.sorted"; printf '%s\n' "${queue[@]}"; } | awk '!seen[$0]++' > "$INPUT"
rm -f "$INPUT.sorted"

echo "=== Build order after dependency resolution ==="
cat "$INPUT"
