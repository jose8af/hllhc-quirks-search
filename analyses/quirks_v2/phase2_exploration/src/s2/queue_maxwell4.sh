#!/bin/bash
# queue_maxwell4.sh -- as queue_maxwell3.sh, plus: wait for the running p2-b-hw-smoke driver, relaunch it once (new smoke job ids after the PYTHIA8DATA and CT14nlo fixes), then
# smoke jobs run before the remaining S2-c chunks): wait until no p2-b-s2c-inc job runs on this node, then run
# p2-b-hw-smoke, then resume p2-b-s2c-inc (the runner skips done jobs), then p2-b-s2c-rs; one job at a time.
set -u
R=/home/users/jdochoa/hllhc-quirks-search/tools/runner; C=/home/users/jdochoa/hllhc-quirks-search/tools/campaigns/p2-b
echo "$(date '+%F %T %z') waiting for the running hw-smoke campaign"
"$R/bin/qv2-watch" "$C/p2-b-hw-smoke.json" 60 300

for c in p2-b-hw-smoke p2-b-s2c-inc p2-b-s2c-rs; do
  echo "$(date '+%F %T %z') launch $c"
  "$R/bin/qv2run" ssh launch "$C/$c.json" --nodes maxwell --max-per-node 1 --on maxwell; sleep 30
  "$R/bin/qv2-watch" "$C/$c.json" 60 300; echo "$(date '+%F %T %z') $c watcher exit $?"
done
echo "$(date '+%F %T %z') queue_maxwell4 end"
