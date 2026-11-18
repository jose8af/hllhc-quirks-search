#!/bin/bash
# queue_slot.sh NODE QUEUEFILE -- channel (i) (Rosalie, 2026-11-16): run runner campaigns one after another in ONE slot
# of NODE (SSH runner, --max-per-node 1, driver in the foreground). QUEUEFILE lists campaign names, one per line; it is
# re-read after every campaign, so campaigns can be appended or reordered while the queue runs (lines starting with
# '#' and campaigns already finished by this queue are skipped). A campaign whose driver already runs elsewhere is
# waited for with qv2-watch first. Empty queue: poll every 60 s; the line STOP ends the queue.
# Start detached:  ssh -x NODE "setsid nohup $0 NODE QUEUEFILE > /home/scratch/jdochoa/drivers/queue_NAME.log 2>&1 &"
R=/home/users/jdochoa/hllhc-quirks-search/tools/runner
node=$1; q=$2; declare -A seen
while true; do
  next=""
  while read -r c; do
    [[ -z "$c" || "$c" == \#* ]] && continue
    [[ "$c" == STOP ]] && { echo "[queue $(date '+%F %T')] STOP"; exit 0; }
    [[ -n "${seen[$c]}" ]] && continue
    next=$c; break
  done < "$q"
  if [[ -z "$next" ]]; then sleep 60; continue; fi
  seen[$next]=1
  f=$R/campaigns/$next.json
  echo "[queue $(date '+%F %T')] start $next"
  if pgrep -f "ssh launch .*campaigns/$next.json" >/dev/null; then
    $R/bin/qv2-watch $f 60 300; echo "[queue $(date '+%F %T')] watched $next exit $?"
  fi
  $R/bin/qv2run ssh launch $f --nodes $node --max-per-node 1
  rc=$?
  # Ignatius 2026-11-18: the driver exits 0 even when jobs failed (p2-a-c1-gen, 12/12 failed, logged "exit 0").
  # Report the campaign's job states and flag failed/timeout/oom jobs explicitly.
  st=$($R/bin/qv2run status $f 2>&1); nf=$(sed -n 's/.*| failed \([0-9]*\) |.*/\1/p' <<< "$st")
  echo "[queue $(date '+%F %T')] end $next exit $rc; $st"
  [[ "${nf:-?}" != 0 ]] && echo "[queue $(date '+%F %T')] WARNING $next: FAILED JOBS ${nf:-unknown} (never retried; rerun under new ids)"
done
