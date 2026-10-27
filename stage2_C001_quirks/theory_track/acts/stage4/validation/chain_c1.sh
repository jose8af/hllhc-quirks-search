#!/bin/zsh
# chain_c1.sh -- sequential Stage-4 sub-runs C1a -> C1b -> C2B (plan §11 row '7-12 s' + user-approved C2-B; C1_LAUNCH.md).
# Usage (detached): nohup zsh acts/stage4/validation/chain_c1.sh <C1a runner PID> > data/acts_stage4/prod/C1/chain_stdout.txt 2>&1 &
# Waits for the given runner PID to exit (kill -0 poll every 120 s; no pgrep patterns), then launches the next sub-run
# with the same flags, waits for it, and so on.  One timestamped line per transition in data/acts_stage4/prod/C1/chain_log.txt.
# Graceful abort of the chain: a STOP file in prod/C1/ (or prod/C2/ before C2B) prevents the next launch.
cd "${0:A:h}/../../.." || exit 2
LOG=data/acts_stage4/prod/C1/chain_log.txt
mkdir -p data/acts_stage4/prod/C1 data/acts_stage4/prod/C2
log() { echo "$(date '+%Y-%m-%d %H:%M:%S') $*" >> $LOG; }
waitpid() { while kill -0 $1 2>/dev/null; do sleep 120; done; }

PID=$1
[[ -n "$PID" ]] || { log "chain: no C1a PID given, abort"; exit 2; }
log "chain started (pid $$), waiting for C1a runner pid $PID"
waitpid $PID
log "C1a runner pid $PID exited; last line: $(tail -1 data/acts_stage4/prod/C1/run_stdout_C1a.txt 2>/dev/null)"

for CAMP OUTDIR in C1b C1 C2B C2; do
  if [[ -e data/acts_stage4/prod/C1/STOP || -e data/acts_stage4/prod/$OUTDIR/STOP ]]; then
    log "STOP file present: $CAMP NOT launched, chain ends"; exit 0
  fi
  nohup nice -n 10 caffeinate -i pixi run python -m acts.stage4.run_stage4 run --campaign $CAMP --workers 7 --mem-gb 19 \
      > data/acts_stage4/prod/$OUTDIR/run_stdout_$CAMP.txt 2>&1 &
  P=$!
  log "$CAMP launched, runner pid $P (stdout prod/$OUTDIR/run_stdout_$CAMP.txt)"
  waitpid $P
  log "$CAMP runner pid $P exited; last line: $(tail -1 data/acts_stage4/prod/$OUTDIR/run_stdout_$CAMP.txt 2>/dev/null)"
done
log "chain finished (C1a -> C1b -> C2B)"
