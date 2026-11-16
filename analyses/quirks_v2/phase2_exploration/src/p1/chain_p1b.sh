#!/bin/bash
# chain_p1.sh -- channel (ii), landau, 1 slot: after the landau S2 chains (chain_after3.log 'chain_after end') AND after
# all 25 p2-b-s2c-inc jobs are done (markers), run p2-b-p1-ev then p2-b-p1-run, one job at a time.
# v2 (16:2x): the FxFx diagnosis campaign p2-b-s2-fxfx-diag runs first, right after the landau S2 chains.
set -u
R=/home/users/jdochoa/hllhc-quirks-search/tools/runner; C=/home/users/jdochoa/hllhc-quirks-search/tools/campaigns/p2-b
M=/home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2/ledger/markers/p2-b-s2c-inc
echo "$(date '+%F %T %z') waiting"
until grep -q 'chain_after end' /home/scratch/jdochoa/drivers/chain_after3.log 2>/dev/null; do sleep 60; done
for c in p2-b-s2-fxfx-diag; do
  echo "$(date '+%F %T %z') launch $c"
  "$R/bin/qv2run" ssh launch "$C/$c.json" --nodes landau --max-per-node 1 --on landau; sleep 30
  "$R/bin/qv2-watch" "$C/$c.json" 60 300; echo "$(date '+%F %T %z') $c watcher exit $?"
done
until [ "$(grep -l '"status":"done"' $M/*/*.marker 2>/dev/null | wc -l)" -ge 25 ]; do sleep 120; done
for c in p2-b-p1-ev p2-b-p1-run; do
  echo "$(date '+%F %T %z') launch $c"
  "$R/bin/qv2run" ssh launch "$C/$c.json" --nodes landau --max-per-node 1 --on landau; sleep 30
  "$R/bin/qv2-watch" "$C/$c.json" 60 300; echo "$(date '+%F %T %z') $c watcher exit $?"
done
echo "$(date '+%F %T %z') chain_p1 end"
