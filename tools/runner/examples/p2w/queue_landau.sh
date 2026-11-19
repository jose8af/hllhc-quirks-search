#!/bin/bash
# Cecilie 2026-11-19: campaigns of the rule-1 validation on landau, one driver at a time, 2 jobs at most.
R=/home/users/jdochoa/hllhc-quirks-search/tools/runner
for c in p2-c-r1v-s2a p2-c-r1v-zb1; do
  [ -e /home/scratch/jdochoa/drivers/STOP.r1v ] && exit 0
  $R/bin/qv2run ssh launch $R/examples/p2w/$c.json --nodes landau --max-per-node 2
done
