#!/bin/zsh
# prodstop_fri.sh -- plan §11 production stop (orchestrator 2026-10-14, C1_LAUNCH §4 option b): at Fri 2026-10-16 12:00
# -05 create run_stage4's graceful-stop file (no new job starts, running jobs finish, completed jobs kept).
#   prod/C2/STOP always (C2B); prod/C1/STOP only if C2B has not been launched yet (then C1b stops and chain_c1.sh does
#   not launch C2B).  Polls the clock every 120 s.  Detached: nohup zsh acts/stage4/validation/prodstop_fri.sh &
cd "${0:A:h}/../../.." || exit 2
LOG=data/acts_stage4/prod/C1/chain_log.txt
T=$(TZ=America/Guayaquil date -j -f "%Y-%m-%d %H:%M:%S" "2026-10-16 12:00:00" +%s)
echo "$(date '+%Y-%m-%d %H:%M:%S') prodstop helper started (pid $$), STOP at epoch $T (Fri 2026-10-16 12:00 -05)" >> $LOG
while (( $(date +%s) < T )); do sleep 120; done
mkdir -p data/acts_stage4/prod/C2
touch data/acts_stage4/prod/C2/STOP
W="prod/C2/STOP"
if ! grep -q "C2B launched" $LOG; then touch data/acts_stage4/prod/C1/STOP; W="$W + prod/C1/STOP"; fi
echo "$(date '+%Y-%m-%d %H:%M:%S') production stop: created $W (running jobs finish, completed jobs kept)" >> $LOG
