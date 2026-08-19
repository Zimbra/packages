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
# 3) Validates every entry that comes out the other end is an actual,
#    buildable package directory - a typo'd or stale line in any
#    ci/build-deps.txt (dependency or reverse-dependent) becomes a
#    graph node via tsort even though it was never a real package, and
#    would otherwise only surface as a build failure deep inside each
#    platform's build job. Failing here instead keeps that class of
#    error a ~seconds-long failure in checkout_and_resolve.
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
    rm -f "$edges_file"
    exit 1
  fi
else
  : > "$INPUT.sorted"
fi

# --- validate every edge participant is a real package BEFORE it gets
#     folded into the final list. tsort only knows the strings we fed
#     it - if a ci/build-deps.txt line is a typo'd / stale path that
#     doesn't correspond to an actual package directory, tsort still
#     happily emits it as a node, and it would otherwise ride straight
#     through into packages_to_build.txt.
bad=0
while IFS= read -r node; do
  [ -n "$node" ] || continue
  if [ ! -d "$node" ] || [ ! -f "$node/Makefile" ]; then
    # Find which build-deps.txt file(s) actually reference this bad path,
    # so the error points straight at the file to fix.
    offenders=$(grep -lxF "$node" */*/ci/build-deps.txt 2>/dev/null || true)
    echo "resolve-build-order: ERROR '$node' was pulled into the build set" \
         "but is not a valid package directory (missing dir or Makefile)."
    if [ -n "$offenders" ]; then
      echo "resolve-build-order:   referenced from:"
      while IFS= read -r f; do echo "resolve-build-order:     $f"; done <<< "$offenders"
    else
      echo "resolve-build-order:   (could not locate which build-deps.txt referenced it - check all ci/build-deps.txt files for '$node')"
    fi
    bad=1
  fi
done < "$INPUT.sorted"

if [ "$bad" -eq 1 ]; then
  echo ""
  echo "ERROR: resolve-build-order produced one or more invalid package paths - aborting before build."
  rm -f "$edges_file" "$INPUT.sorted"
  exit 1
fi

rm -f "$edges_file"

{ cat "$INPUT.sorted"; printf '%s\n' "${queue[@]}"; } | awk '!seen[$0]++' > "$INPUT"
rm -f "$INPUT.sorted"

echo "=== Build order after dependency resolution ==="
cat "$INPUT"
