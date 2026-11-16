#!/bin/bash
# chain_wait.sh <campaign.json>... -- (env WAIT_LOG, WAIT_PAT) wait until WAIT_PAT appears in WAIT_LOG on this node, then run the given
# campaigns one job at a time on this node (channel (ii) keeps to 1 slot on landau).
set -u
R=/home/users/jdochoa/hllhc-quirks-search/tools/runner; NODE=$(hostname -s)
L=${WAIT_LOG:-/home/scratch/jdochoa/drivers/chain_s2_first.log}; PAT=${WAIT_PAT:-chain end}
echo "$(date '+%F %T %z') waiting for chain_s2_first"
until grep -q "$PAT" $L 2>/dev/null; do sleep 60; done
for c in "$@"; do
  echo "$(date '+%F %T %z') launch $c"
  "$R/bin/qv2run" ssh launch "$c" --nodes "$NODE" --max-per-node 1 --on "$NODE"; sleep 30
  "$R/bin/qv2-watch" "$c" 60 300; echo "$(date '+%F %T %z') $c watcher exit $?"
done
echo "$(date '+%F %T %z') chain_after end"
