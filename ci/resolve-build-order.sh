#!/usr/bin/env bash
# Path in repo: ci/resolve-build-order.sh
#
# Called as: bash ci/resolve-build-order.sh packages_to_build.txt
#
# Entries in the input file are FULL relative paths (e.g. "thirdparty/
# nginx" or "zimbra/osl") - not bare names.
#
# 1) Expands the list: if a package is a declared dependency of some
#    OTHER package (via that package's own ci/build-deps.txt, which
#    lists full paths), pulls that other package in too - e.g. a
#    change to thirdparty/clamav also rebuilds zimbra/mta-components.
# 2) Orders the final list by looking each entry up in MASTER_ORDER -
#    an already-correct, full build sequence - instead of tsort'ing
#    edges built from per-package build-deps.txt files. A stale/typo'd
#    build-deps.txt line can no longer smuggle a phantom node or a
#    fake circular dependency into the run; it just fails validation.
# 3) Validates every entry is an actual, buildable package directory.
#
# Convention: <root>/<pkg>/ci/build-deps.txt is OPTIONAL and is used
# ONLY for the expand step (finding reverse-dependents) - it has no
# say in ordering anymore. One full path per line.
set -euo pipefail

INPUT="${1:-packages_to_build.txt}"
MASTER_ORDER="${MASTER_ORDER:-build-order}"

[ -s "$INPUT" ] || { echo "resolve-build-order: $INPUT is empty, nothing to do"; exit 0; }
[ -f "$MASTER_ORDER" ] || { echo "resolve-build-order: ERROR master order file '$MASTER_ORDER' not found"; exit 1; }

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
    cand_pkg="${cand_deps_file%/ci/build-deps.txt}"
    if grep -qxF "$pkg" "$cand_deps_file" 2>/dev/null && [ -z "${seen[$cand_pkg]:-}" ]; then
      seen["$cand_pkg"]=1
      queue+=("$cand_pkg")
      echo "resolve-build-order: auto-adding '$cand_pkg' (depends on changed package '$pkg')"
    fi
  done
done

# --- order by position in the master build-order file -------------------
ordered=()
while IFS= read -r line; do
  pkg="$(sed -e 's/#.*$//' -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' <<<"$line")"
  [ -n "$pkg" ] || continue
  case "$pkg" in thirdparty/*|zimbra/*) ;; *) continue ;; esac
  [ -n "${seen[$pkg]:-}" ] || continue
  ordered+=("$pkg")
  unset "seen[$pkg]"
done < "$MASTER_ORDER"

# anything still left in $seen was queued/pulled-in but never appeared
# in the master order file - surface it instead of silently dropping it
missing=0
for pkg in "${!seen[@]}"; do
  echo "resolve-build-order: ERROR '$pkg' is not listed in '$MASTER_ORDER'"
  missing=1
done
if [ "$missing" -eq 1 ]; then
  echo ""
  echo "ERROR: package(s) missing from master order file - add them there first."
  exit 1
fi

# --- validate every entry is a real, buildable package directory -------
bad=0
for pkg in "${ordered[@]}"; do
  if [ ! -d "$pkg" ] || [ ! -f "$pkg/Makefile" ]; then
    offenders=$(grep -lxF "$pkg" */*/ci/build-deps.txt 2>/dev/null || true)
    echo "resolve-build-order: ERROR '$pkg' is not a valid package directory (missing dir or Makefile)."
    if [ -n "$offenders" ]; then
      echo "resolve-build-order:   referenced from:"
      while IFS= read -r f; do echo "resolve-build-order:     $f"; done <<< "$offenders"
    fi
    bad=1
  fi
done
if [ "$bad" -eq 1 ]; then
  echo ""
  echo "ERROR: resolve-build-order produced one or more invalid package paths - aborting before build."
  exit 1
fi

printf '%s\n' "${ordered[@]}" > "$INPUT"

echo "=== Build order after dependency resolution ==="
cat "$INPUT"
