#!/bin/bash
# chain_after.sh <campaign.json>... -- wait until chain_s2_first.sh has ended on this node, then run the given
# campaigns one job at a time on this node (channel (ii) keeps to 1 slot on landau).
set -u
R=/home/users/jdochoa/hllhc-quirks-search/tools/runner; NODE=$(hostname -s)
L=/home/scratch/jdochoa/drivers/chain_s2_first.log
echo "$(date '+%F %T %z') waiting for chain_s2_first"
until grep -q 'chain end' $L 2>/dev/null; do sleep 60; done
for c in "$@"; do
  echo "$(date '+%F %T %z') launch $c"
  "$R/bin/qv2run" ssh launch "$c" --nodes "$NODE" --max-per-node 1 --on "$NODE"; sleep 30
  "$R/bin/qv2-watch" "$c" 60 300; echo "$(date '+%F %T %z') $c watcher exit $?"
done
echo "$(date '+%F %T %z') chain_after end"
