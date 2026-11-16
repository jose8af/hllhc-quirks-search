#!/bin/bash
# p2x_queue.sh NODE MAX CAMPAIGN.json [CAMPAIGN.json ...]   (channel (iii), Xavier, 2026-11-16; pattern of queue_slot.sh)
# Runs runner campaigns one after another on NODE with the SSH backend, MAX concurrent jobs, driver in the foreground.
# Run it ON the worker, detached (never on einstein):
#   ssh -x NODE "mkdir -p /home/scratch/jdochoa/drivers; setsid nohup $0 NODE MAX /abs/a.json /abs/b.json \
#                > /home/scratch/jdochoa/drivers/NAME.log 2>&1 < /dev/null &"
# Before each campaign it waits until (other 'qv2run job' processes of this user on the node) + MAX <= NODECAP
# (default 3: schrodinger shows a graphical session), so the node cap holds without a manual check per campaign.
# A campaign whose file lists other campaign files under "after" waits until those are complete.
# It stops at the first campaign that does not end complete (the next one may depend on it); if no job of it has
# failed (driver left for lack of capacity), the campaign is launched again every 5 minutes for up to 4 hours.  Resume: run the same
# line again; the runner skips done jobs.  A STOP file /home/scratch/jdochoa/drivers/STOP.<basename of first json>
# ends the queue before the next campaign.
R=/home/users/jdochoa/hllhc-quirks-search/tools/runner
node=$1; max=$2; shift 2
cap=${NODECAP:-3}
[ "$(hostname -s)" = "$node" ] || { echo "run this on $node" >&2; exit 1; }
stopf=/home/scratch/jdochoa/drivers/STOP.$(basename "$1" .json)
for f in "$@"; do
  [ -e "$stopf" ] && { echo "[queue $(date '+%F %T')] STOP file found"; exit 0; }
  c=$(basename "$f" .json)
  st=$($R/bin/qv2run status "$f" --json)
  if echo "$st" | python3 -I -c 'import json,sys; d=json.load(sys.stdin); sys.exit(0 if d["counts"].get("done",0)==d["jobs"] else 1)'; then
    echo "[queue $(date '+%F %T')] $c already complete"; continue
  fi
  # inputs: campaigns listed under "after" in the campaign file must be complete (waits; never starts on missing inputs)
  for dep in $(python3 -I -c 'import json,sys; print(" ".join(json.load(open(sys.argv[1])).get("after", [])))' "$f"); do
    until $R/bin/qv2run status "$dep" --json | python3 -I -c 'import json,sys; d=json.load(sys.stdin); sys.exit(0 if d["counts"].get("done",0)==d["jobs"] else 1)'; do
      [ -e "$stopf" ] && { echo "[queue $(date '+%F %T')] STOP file found"; exit 0; }
      echo "[queue $(date '+%F %T')] $c waits for $(basename "$dep" .json)"; sleep 120
    done
  done
  while true; do
    n=$(pgrep -u "$USER" -af '[q]v2run job' | grep -v -- "/$c.json" | wc -l)
    [ $((n + max)) -le "$cap" ] && break
    echo "[queue $(date '+%F %T')] $n other jobs on $node, waiting"; sleep 30
  done
  echo "[queue $(date '+%F %T')] start $c ($max slots)"
  tries=0
  while true; do
    $R/bin/qv2run ssh launch "$f" --nodes "$node" --max-per-node "$max"
    rc=$?
    st=$($R/bin/qv2run status "$f" --json)
    echo "[queue $(date '+%F %T')] end $c exit $rc $st"
    echo "$st" | python3 -I -c 'import json,sys; d=json.load(sys.stdin); sys.exit(0 if d["counts"].get("done",0)==d["jobs"] else 1)' && break
    # not complete.  If no job ended in a final failure, the driver left for a transient reason (no capacity because of
    # foreign load on the node, a probe that failed): wait 5 minutes and launch the same campaign again, up to 4 hours.
    if echo "$st" | python3 -I -c 'import json,sys; c=json.load(sys.stdin)["counts"]; sys.exit(0 if not any(c.get(k,0) for k in ("failed","timeout","oom","verify_failed")) else 1)' \
       && [ $tries -lt 48 ] && [ ! -e "$stopf" ]; then
      tries=$((tries + 1)); echo "[queue $(date '+%F %T')] $c not complete and no failed job: retry $tries in 300 s"; sleep 300; continue
    fi
    echo "[queue $(date '+%F %T')] $c not complete: queue stops"; exit 2
  done
done
echo "[queue $(date '+%F %T')] all complete"
