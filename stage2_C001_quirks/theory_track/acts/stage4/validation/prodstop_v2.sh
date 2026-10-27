#!/bin/zsh
# prodstop_v2.sh -- replaces prodstop_fri.sh (orchestrator 2026-10-15: user moved the deadline to Sun 18 afternoon):
#   graceful STOP of C2B (prod/C2/STOP) at Fri 2026-10-16 20:00 -05; running jobs finish, completed jobs kept.
cd "${0:A:h}/../../.." || exit 2
LOG=data/acts_stage4/prod/C1/chain_log.txt
T=$(TZ=America/Guayaquil date -j -f "%Y-%m-%d %H:%M:%S" "2026-10-16 20:00:00" +%s)
echo "$(date '+%Y-%m-%d %H:%M:%S') prodstop_v2 started (pid $$), C2 STOP at Fri 2026-10-16 20:00 -05" >> $LOG
while (( $(date +%s) < T )); do sleep 120; done
mkdir -p data/acts_stage4/prod/C2; touch data/acts_stage4/prod/C2/STOP
echo "$(date '+%Y-%m-%d %H:%M:%S') production stop: created prod/C2/STOP" >> $LOG
