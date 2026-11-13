#!/bin/bash
# TEST ONLY, run ON A WORKER (landau): kill -9 the wrapper at each stage, then resume and check convergence.
# Stages: during_cmd (payload running, orphaned in its systemd scope), before_copy (command done, stash written),
# during_copy (.part present on cajuela), after_rename (final file present, no `done` marker yet).
set -u
R=/home/users/jdochoa/hllhc-quirks-search/tools/runner
F=$R/examples/feas/feas-kill.json
J=$R/bin/qv2-job
S=/home/scratch/jdochoa
D=/nfs/cajuela/jdochoa/quirks_v2/data/feasibility/runner/feas-kill/000
M=/home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2/phase1_strategy/outputs/feasibility/runner_ledger/markers/feas-kill/000
last() { tail -1 $M/$1.marker | python3 -c 'import json,sys; r=json.load(sys.stdin); print(r["status"], "stash" if r.get("resumed_from_stash") else "")'; }
for st in during_cmd before_copy during_copy after_rename; do
  id=kill-${st//_/-}
  echo "=== stage $st ($id)"
  if [ $st = during_cmd ]; then
    nice -n 10 $J --campaign $F --job $id --mechanism ssh 2>/dev/null & 
    until [ -f $M/$id.marker ]; do sleep 0.5; done; sleep 3
    pid=$(pgrep -f "qv2run job .*--job $id ")
  else
    QV2_TEST_PAUSE_AT=$st nice -n 10 $J --campaign $F --job $id --mechanism ssh 2>/dev/null &
    until [ -f $S/$id/.qv2_paused_$st ]; do sleep 0.5; done
    pid=$(cat $S/$id/.qv2_paused_$st)
  fi
  kill -9 $pid; sleep 1
  echo "after kill -9: marker=$(last $id) scratch=$(ls -A $S/$id 2>/dev/null | tr '\n' ' ') part=$(ls $D/kill-$st.dat.part 2>/dev/null | wc -l) final=$(ls $D/kill-$st.dat 2>/dev/null | wc -l) scopes=$(systemctl --user list-units --plain --no-legend "qv2-$id-*" | wc -l)"
  $R/bin/qv2run status --live $F | sed 's/^/  status: /'
  nice -n 10 $J --campaign $F --job $id --mechanism ssh 2>&1 | grep -E "orphan|stale|stash|result" | sed 's/^/  resume: /'
  echo "after resume: marker=$(last $id) scratch_exists=$([ -e $S/$id ] && echo yes || echo no) part=$(ls $D/*.part 2>/dev/null | wc -l) scopes=$(systemctl --user list-units --plain --no-legend "qv2-$id-*" | wc -l)"
  nice -n 10 $J --campaign $F --job $id --mechanism ssh 2>&1 | grep -E "result" | sed 's/^/  rerun: /'
done
$R/bin/qv2run verify $F
sha256sum $D/*.dat | cut -c1-16
echo END
