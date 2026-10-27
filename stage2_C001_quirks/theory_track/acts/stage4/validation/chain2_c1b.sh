#!/bin/zsh
# chain2_c1b.sh -- replaces chain_c1.sh after C1a (orchestrator 2026-10-15 00:40, token-outage plan):
#   wait for the C1b runner PID -> run the frozen Stage-4 analysis on C1 (non-DEV; if it refuses, a --dev run to a
#   separate dir) on the otherwise idle Mac -> launch C2B (same flags as before) and wait for it.
cd "${0:A:h}/../../.." || exit 2
LOG=data/acts_stage4/prod/C1/chain_log.txt
log() { echo "$(date '+%Y-%m-%d %H:%M:%S') $*" >> $LOG; }
waitpid() { while kill -0 $1 2>/dev/null; do sleep 120; done; }
PID=$1
log "chain2 started (pid $$), waiting for C1b runner pid $PID"
waitpid $PID
log "C1b runner pid $PID exited; last line: $(tail -1 data/acts_stage4/prod/C1/run_stdout_C1b.txt 2>/dev/null)"
A=data/acts_stage4/analysis
mkdir -p $A
log "analysis C1 (frozen, non-DEV) started -> $A/C1_v1"
caffeinate -i pixi run python -m acts.stage4.analysis.run_all --campaigns C1a,C1b --out $A/C1_v1 > $A/C1_v1.log 2>&1
RC=$?
log "analysis C1 non-DEV exit $RC"
if [[ $RC -ne 0 ]]; then
  log "analysis C1 --dev started -> $A/C1_v1_dev"
  caffeinate -i pixi run python -m acts.stage4.analysis.run_all --campaigns C1a,C1b --out $A/C1_v1_dev --dev > $A/C1_v1_dev.log 2>&1
  log "analysis C1 --dev exit $?"
fi
if [[ -e data/acts_stage4/prod/C1/STOP || -e data/acts_stage4/prod/C2/STOP ]]; then log "STOP present: C2B NOT launched"; exit 0; fi
nohup nice -n 10 caffeinate -i pixi run python -m acts.stage4.run_stage4 run --campaign C2B --workers 7 --mem-gb 19 \
    > data/acts_stage4/prod/C2/run_stdout_C2B.txt 2>&1 &
P=$!
log "C2B launched, runner pid $P (stdout prod/C2/run_stdout_C2B.txt)"
waitpid $P
log "C2B runner pid $P exited; last line: $(tail -1 data/acts_stage4/prod/C2/run_stdout_C2B.txt 2>/dev/null)"
log "chain2 finished"
