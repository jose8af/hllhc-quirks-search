#!/bin/bash
# queue_maxwell_fxfx.sh -- channel (ii) Edgar, 2026-11-17, maxwell, channel (ii)'s 1 slot: after queue_maxwell_edgar.sh
# (f200, nll) ends: FxFx compile jobs (p2-b-s2-fxfx-c, <= 30 min each), then the two first-launch jobs p2-b-s2-fxfx
# (user exception 2026-11-17: timeout 6000 s) -- only if the runner accepts the campaign (it validates timeout_s <= 1800
# unless the runner is changed); otherwise it logs that and stops.  One job at a time; node job count checked (<= 3).
set -u
R=/home/users/jdochoa/hllhc-quirks-search/tools/runner; C=/home/users/jdochoa/hllhc-quirks-search/tools/campaigns/p2-b
echo "$(date '+%F %T %z') waiting for queue_maxwell_edgar end"
until grep -q "queue_maxwell_edgar end" /home/scratch/jdochoa/drivers/queue_maxwell_edgar.log 2>/dev/null; do sleep 120; done
for c in p2-b-s2-fxfx-c p2-b-s2-fxfx; do
  if ! "$R/bin/qv2run" status "$C/$c.json" > /dev/null 2>&1; then
    echo "$(date '+%F %T %z') $c NOT launched: campaign rejected by the runner ($("$R/bin/qv2run" status "$C/$c.json" 2>&1 | tail -1))"; continue; fi
  until [ "$(pgrep -fc 'qv2run job')" -le 3 ]; do echo "$(date '+%F %T %z') node busy, waiting"; sleep 300; done
  echo "$(date '+%F %T %z') launch $c (node jobs before: $(pgrep -fc 'qv2run job'))"
  "$R/bin/qv2run" ssh launch "$C/$c.json" --nodes maxwell --max-per-node 1 --on maxwell; sleep 30
  "$R/bin/qv2-watch" "$C/$c.json" 60 300; echo "$(date '+%F %T %z') $c watcher exit $?"
done
echo "$(date '+%F %T %z') queue_maxwell_fxfx end"
