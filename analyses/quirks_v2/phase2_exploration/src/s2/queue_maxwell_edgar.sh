#!/bin/bash
# queue_maxwell_edgar.sh -- channel (ii) Edgar, 2026-11-17, maxwell, 1 slot: wait until Sebastian's queue_maxwell5.sh has
# finished p2-b-s2c-rs (its log says "queue_maxwell5 end"), then p2-b-s2c-f200 (f200 evaluation, minutes) and
# p2-b-s2-nll (Resummino NLO+NLL scan, 6 jobs); one job at a time.
set -u
R=/home/users/jdochoa/hllhc-quirks-search/tools/runner; C=/home/users/jdochoa/hllhc-quirks-search/tools/campaigns/p2-b
echo "$(date '+%F %T %z') waiting for queue_maxwell5 end"
until grep -q "queue_maxwell5 end" /home/scratch/jdochoa/drivers/queue_maxwell5.log 2>/dev/null; do sleep 120; done
for c in p2-b-s2c-f200 p2-b-s2-nll; do
  echo "$(date '+%F %T %z') launch $c"
  "$R/bin/qv2run" ssh launch "$C/$c.json" --nodes maxwell --max-per-node 1 --on maxwell; sleep 30
  "$R/bin/qv2-watch" "$C/$c.json" 60 300; echo "$(date '+%F %T %z') $c watcher exit $?"
done
echo "$(date '+%F %T %z') queue_maxwell_edgar end"
