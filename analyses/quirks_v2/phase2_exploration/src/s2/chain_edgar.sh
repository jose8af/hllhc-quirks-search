#!/bin/bash
# chain_edgar.sh <campaign.json>... -- channel (ii) Edgar, 2026-11-17: run the given campaigns one after another on THIS
# node, one job at a time (channel (ii)'s single slot), each launched with the runner's SSH backend and watched.
set -u
R=/home/users/jdochoa/hllhc-quirks-search/tools/runner; NODE=$(hostname -s)
for c in "$@"; do
  echo "$(date '+%F %T %z') launch $c"
  "$R/bin/qv2run" ssh launch "$c" --nodes "$NODE" --max-per-node 1 --on "$NODE"; sleep 30
  "$R/bin/qv2-watch" "$c" 60 300; echo "$(date '+%F %T %z') $c watcher exit $?"
done
echo "$(date '+%F %T %z') chain_edgar end"
