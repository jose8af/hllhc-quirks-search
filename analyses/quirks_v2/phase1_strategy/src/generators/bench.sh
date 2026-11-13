#!/usr/bin/env bash
# bench.sh -- run a benchmark command 3 times sequentially (single) and once as 3 concurrent copies, under
# /usr/bin/time -v, each in its own work dir on node-local scratch.  quirks v2 Phase 1, executor Basil.
# Usage: bench.sh <tag> <workroot> <mode: single|conc|both> -- <command with {I} = replica index 1..3, {W} = work dir>
# Output: <workroot>/<tag>/results.tsv  with  tag mode rep user_s sys_s wall_s maxrss_kb exit
set -uo pipefail
export LC_ALL=C     # the nodes run an es_* locale: awk would read "03.95" as 3
tag=$1; root=$2; mode=$3; shift 4
cmd="$*"
out=$root/$tag; mkdir -p "$out"
res=$out/results.tsv
parse() {  # timefile mode rep
  local f=$1
  local u s w r x
  u=$(awk -F': ' '/User time/{print $2}' "$f"); s=$(awk -F': ' '/System time/{print $2}' "$f")
  w=$(awk -F': ' '/Elapsed/{print $2}' "$f" | awk -F: '{if(NF==3)print $1*3600+$2*60+$3; else print $1*60+$2}')
  r=$(awk -F': ' '/Maximum resident/{print $2}' "$f"); x=$(awk -F': ' '/Exit status/{print $2}' "$f")
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$tag" "$2" "$3" "$u" "$s" "$w" "$r" "$x" >> "$res"
}
run1() {  # mode rep
  local w=$out/$1_$2; rm -rf "$w"; mkdir -p "$w"
  local c=${cmd//\{I\}/$2}; c=${c//\{W\}/$w}
  (cd "$w" && nice -n 10 /usr/bin/time -v -o "$w/time.txt" bash -c "$c" > "$w/stdout.txt" 2>&1)
  parse "$w/time.txt" "$1" "$2"
}
if [ "$mode" = single ] || [ "$mode" = both ]; then for i in 1 2 3; do run1 single $i; done; fi
if [ "$mode" = conc ] || [ "$mode" = both ]; then
  for i in 1 2 3; do run1 conc $i & done; wait
fi
cat "$res"
