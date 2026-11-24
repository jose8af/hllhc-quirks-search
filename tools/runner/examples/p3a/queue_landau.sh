#!/bin/bash
# Aurora 2026-11-24 (p3-a): campaigns of the final pilot classification on landau, one driver at a time, 3 jobs at most.
# Stop between campaigns: touch /home/scratch/jdochoa/drivers/STOP.p3a
R=/home/users/jdochoa/hllhc-quirks-search/tools/runner
mkdir -p /home/scratch/jdochoa/drivers
for c in "$@"; do
  [ -e /home/scratch/jdochoa/drivers/STOP.p3a ] && exit 0
  echo "$(date '+%F %T') start $c"
  $R/bin/qv2run ssh launch $R/examples/p3a/$c.json --nodes landau --max-per-node 3
  echo "$(date '+%F %T') end $c rc=$?"
done
echo "$(date '+%F %T') QUEUE DONE"
