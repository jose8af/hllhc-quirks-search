#!/bin/bash
# chain_p1d.sh -- channel (ii), landau, 1 slot: run p2-b-p1-ev then p2-b-p1-run, one job at a time (s2c-inc complete).
set -u
R=/home/users/jdochoa/hllhc-quirks-search/tools/runner; C=/home/users/jdochoa/hllhc-quirks-search/tools/campaigns/p2-b
for c in p2-b-p1-ev p2-b-p1-run; do
  echo "$(date '+%F %T %z') launch $c"
  "$R/bin/qv2run" ssh launch "$C/$c.json" --nodes landau --max-per-node 1 --on landau; sleep 30
  "$R/bin/qv2-watch" "$C/$c.json" 60 300; echo "$(date '+%F %T %z') $c watcher exit $?"
done
echo "$(date '+%F %T %z') chain_p1d end"
