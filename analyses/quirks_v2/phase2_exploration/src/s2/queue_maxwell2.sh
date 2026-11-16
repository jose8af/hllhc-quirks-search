#!/bin/bash
# queue_maxwell2.sh <after.json> <campaign.json>... -- channel (ii), maxwell, 1 light slot: wait until campaign <after>
# is complete (its own watcher), then run the others one job at a time.
set -u
R=/home/users/jdochoa/hllhc-quirks-search/tools/runner
after=$1; shift
echo "$(date '+%F %T %z') waiting for $after"
"$R/bin/qv2-watch" "$after" 60 300; echo "$(date '+%F %T %z') $after watcher exit $?"
for c in "$@"; do
  echo "$(date '+%F %T %z') launch $c"
  "$R/bin/qv2run" ssh launch "$c" --nodes maxwell --max-per-node 1 --on maxwell; sleep 30
  "$R/bin/qv2-watch" "$c" 60 300; echo "$(date '+%F %T %z') $c watcher exit $?"
done
echo "$(date '+%F %T %z') queue_maxwell2 end"
