#!/bin/bash
# queue_maxwell5.sh -- channel (ii), maxwell, 1 light slot: wait for the running p2-b-s2c-inc driver, then
# p2-b-hw-mb ([DP5], 1e6 + 1e6 MB events), p2-b-s2c-rs; one job at a time.
set -u
R=/home/users/jdochoa/hllhc-quirks-search/tools/runner; C=/home/users/jdochoa/hllhc-quirks-search/tools/campaigns/p2-b
echo "$(date '+%F %T %z') waiting for the running p2-b-s2c-inc driver (launched by queue_maxwell4)"
"$R/bin/qv2-watch" "$C/p2-b-s2c-inc.json" 60 300; echo "$(date '+%F %T %z') p2-b-s2c-inc watcher exit $?"
for c in p2-b-hw-mb p2-b-s2c-rs; do
  echo "$(date '+%F %T %z') launch $c"
  "$R/bin/qv2run" ssh launch "$C/$c.json" --nodes maxwell --max-per-node 1 --on maxwell; sleep 30
  "$R/bin/qv2-watch" "$C/$c.json" 60 300; echo "$(date '+%F %T %z') $c watcher exit $?"
done
echo "$(date '+%F %T %z') queue_maxwell5 end"
