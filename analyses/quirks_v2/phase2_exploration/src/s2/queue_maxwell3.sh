#!/bin/bash
# queue_maxwell3.sh -- channel (ii), maxwell, 1 light slot (re-ordered 2026-11-16 13:35 so that the validation-2 and DP5
# smoke jobs run before the remaining S2-c chunks): wait until no p2-b-s2c-inc job runs on this node, then run
# p2-b-hw-smoke, then resume p2-b-s2c-inc (the runner skips done jobs), then p2-b-s2c-rs; one job at a time.
set -u
R=/home/users/jdochoa/hllhc-quirks-search/tools/runner; C=/home/users/jdochoa/hllhc-quirks-search/tools/campaigns/p2-b
echo "$(date '+%F %T %z') waiting for the running s2c-inc job to end"
while pgrep -f "qv2run job --campaign $C/p2-b-s2c-inc.json" >/dev/null; do sleep 30; done
for c in p2-b-hw-smoke p2-b-s2c-inc p2-b-s2c-rs; do
  echo "$(date '+%F %T %z') launch $c"
  "$R/bin/qv2run" ssh launch "$C/$c.json" --nodes maxwell --max-per-node 1 --on maxwell; sleep 30
  "$R/bin/qv2-watch" "$C/$c.json" 60 300; echo "$(date '+%F %T %z') $c watcher exit $?"
done
echo "$(date '+%F %T %z') queue_maxwell3 end"
