#!/bin/bash
# TEST ONLY. 24-job mini-campaign through the Argo backend on landau (parallelism 2), with fault injection:
#  1 kill the launcher (SIGKILL) midway; the workflow keeps running; a new launcher waits for it;
#  2 delete one running pod (OnError retry; wrapper gets SIGTERM -> 'killed' line, retry attempt 2);
#  3 idempotency (relaunch submits nothing);  4 corrupt one output -> verify -> relaunch reruns only it;
#  5 ownership / mode / no .part / directory inodes unchanged.  All test workflows deleted at the end.
set -u
. /home/users/jdochoa/hllhc-quirks-search/tools/env.sh
R=$REPO/tools/runner/bin/qv2run
F=$REPO/tools/runner/examples/feas/feas-mini-argo.json
L=$QV2/phase1_strategy/outputs/feasibility/runner_ledger/markers/feas-mini-argo
D=$QV2_DATA/feasibility/runner/feas-mini-argo
S=$QV2_DATA/feasibility/runner/argo_status
SEL=owner=jdochoa,study=quirks-v2,qv2-campaign=feas-mini-argo
ts() { date +%H:%M:%S; }
cnt() { $R status --json $F | python3 -c 'import json,sys; c=json.load(sys.stdin)["counts"]; print(c.get(sys.argv[1],0))' "$1"; }
wait_done() { while [ "$(cnt done)" -lt "$1" ]; do sleep 3; done; }
save_wfs() { for w in $(kubectl get wf -n argo -l $SEL -o name | sed 's|.*/||'); do argo get -n argo $w -o json > $S/$w.json; done; }
echo "$(ts) T0 start"; T0=$(date +%s.%N)
$R argo launch $F --nodes landau --max-parallel 2 --keep --detach
wait_done 6
DPID=$(python3 -c "import json;print(json.load(open('$L/_driver/driver.json'))['pid'])")
echo "$(ts) step1: $(cnt done) done; SIGKILL launcher pid $DPID"; kill -9 $DPID
pkill -KILL -f "argo wait -n argo jdochoa-qv2-feas-mini-argo" || true
sleep 20
echo "$(ts) step1: no launcher: done $(cnt done) running $(cnt running); workflow phase: $(kubectl get wf -n argo -l $SEL -o jsonpath='{.items[*].status.phase}')"
ls -d $D/000 $D/001 | while read d; do stat -c '%n inode=%i' $d; done > $QV2_DATA/feasibility/runner/mini-argo-dir-inodes-before.txt
$R argo launch $F --nodes landau --max-parallel 2 --keep --detach
sleep 10
POD=$(kubectl get pods -n argo -l $SEL --field-selector=status.phase=Running -o jsonpath='{.items[0].metadata.name}')
echo "$(ts) step2: delete running pod $POD"; kubectl delete pod -n argo $POD --wait=false
$R watch $F --interval 10 --grace 90; echo "$(ts) watch exit $?"
T1=$(date +%s.%N); echo "makespan $(python3 -c "print(round($T1-$T0,1))") s"
while pgrep -f "qv2run argo launch $F" > /dev/null; do sleep 3; done
save_wfs
echo "$(ts) step3: relaunch on a complete campaign:"; $R argo launch $F --nodes landau --max-parallel 2 --keep 2>&1 | tail -2
echo "$(ts) step4: corrupt mini-argo-013 output"; printf 'X' >> $D/001/mini-argo-013.dat
$R verify $F; echo "verify exit $?"
$R argo launch $F --nodes landau --max-parallel 2 --keep 2>&1 | grep -E 'submitted|finished'
$R verify $F; echo "verify exit after rerun $?"
save_wfs
echo "$(ts) step5: ownership/mode"; find $D -type f -printf '%U:%G %m\n' | sort | uniq -c
find $D -name '*.part' | wc -l | sed 's/^/part files left: /'
find $D -type d -printf '%U:%G %m %p\n'
ls -d $D/000 $D/001 | while read d; do stat -c '%n inode=%i' $d; done > $QV2_DATA/feasibility/runner/mini-argo-dir-inodes-after.txt
diff $QV2_DATA/feasibility/runner/mini-argo-dir-inodes-{before,after}.txt && echo "dir inodes unchanged"
$R status -vv $F | awk '{print $3}' | sort | uniq -c
for w in $(kubectl get wf -n argo -l $SEL -o name | sed 's|.*/||'); do argo delete -n argo $w; done
echo "$(ts) END"
