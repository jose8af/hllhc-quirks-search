#!/usr/bin/env bash
# reparse.sh -- rebuild every <root>/<tag>/results.tsv from the per-run time.txt files with LC_ALL=C (the first
# benchmarks were parsed under the es_* locale, which truncated wall seconds to integers). Usage: reparse.sh <root>
export LC_ALL=C
root=$1
for d in "$root"/*/; do
  tag=$(basename "$d"); res=$d/results.tsv; : > "$res.new"
  for w in "$d"/single_* "$d"/conc_*; do
    [ -f "$w/time.txt" ] || continue
    b=$(basename "$w"); mode=${b%_*}; rep=${b#*_}; f=$w/time.txt
    u=$(awk -F': ' '/User time/{print $2}' "$f"); s=$(awk -F': ' '/System time/{print $2}' "$f")
    wl=$(awk -F': ' '/Elapsed/{print $2}' "$f" | awk -F: '{if(NF==3)print $1*3600+$2*60+$3; else print $1*60+$2}')
    r=$(awk -F': ' '/Maximum resident/{print $2}' "$f"); x=$(awk -F': ' '/Exit status/{print $2}' "$f")
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$tag" "$mode" "$rep" "$u" "$s" "$wl" "$r" "$x" >> "$res.new"
  done
  mv "$res.new" "$res"
  # inner (timed sub-step) files, if any -> inner.tsv with the same columns
  : > "$d/inner.tsv.new"
  for w in "$d"/single_* "$d"/conc_*; do
    f=$w/inner_time.txt; [ -f "$f" ] || continue
    b=$(basename "$w"); mode=${b%_*}; rep=${b#*_}
    u=$(awk -F': ' '/User time/{print $2}' "$f"); s=$(awk -F': ' '/System time/{print $2}' "$f")
    wl=$(awk -F': ' '/Elapsed/{print $2}' "$f" | awk -F: '{if(NF==3)print $1*3600+$2*60+$3; else print $1*60+$2}')
    r=$(awk -F': ' '/Maximum resident/{print $2}' "$f"); x=$(awk -F': ' '/Exit status/{print $2}' "$f")
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$tag" "$mode" "$rep" "$u" "$s" "$wl" "$r" "$x" >> "$d/inner.tsv.new"
  done
  if [ -s "$d/inner.tsv.new" ]; then mv "$d/inner.tsv.new" "$d/inner.tsv"; else rm -f "$d/inner.tsv.new"; fi
done
