#!/bin/bash
# Cecilie 2026-11-19: campaigns of the rule-1 validation on schrodinger, one driver at a time, 2 jobs at most.
R=/home/users/jdochoa/hllhc-quirks-search/tools/runner
for c in p2-c-r1v-ctlp p2-c-r1v-zp p2-c-r1v-subb; do
  [ -e /home/scratch/jdochoa/drivers/STOP.r1v ] && exit 0
  $R/bin/qv2run ssh launch $R/examples/p2w/$c.json --nodes schrodinger --max-per-node 2
done
