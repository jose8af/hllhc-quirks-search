#!/bin/bash
# queue_maxwell.sh <campaign.json>... -- channel (ii): wait until channel (i)'s rho = 2 jobs have left maxwell and it is
# 13:30 or later, then run the campaigns in order on maxwell with at most 2 concurrent jobs (Herwig install alongside).
set -u
R=/home/users/jdochoa/hllhc-quirks-search/tools/runner
echo "$(date '+%F %T %z') queued"
while [ "$(date +%H%M)" -lt 1330 ] || ls -d /home/scratch/jdochoa/d0pu2* >/dev/null 2>&1; do sleep 60; done
for c in "$@"; do
  echo "$(date '+%F %T %z') launch $c"
  "$R/bin/qv2run" ssh launch "$c" --nodes maxwell --max-per-node 2 --on maxwell; sleep 30
  "$R/bin/qv2-watch" "$c" 60 300; echo "$(date '+%F %T %z') $c watcher exit $?"
done
echo "$(date '+%F %T %z') queue_maxwell end"
