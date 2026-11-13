#!/bin/bash
# TEST ONLY. Run ON landau:  ssh -x landau 'nohup …/scenario_mini_argo.sh > LOG 2>&1 &'
# 24-job mini-campaign through the Argo backend (driver detached on landau, parallelism 2, pods pinned to landau):
#  1 kill -9 the driver midway; the workflow keeps running; a restarted driver waits for it;
#  2 delete one running pod (wrapper gets SIGTERM -> 'killed'; Argo OnError retry or driver resubmission);
#  3 idempotency (relaunch submits nothing);  4 corrupt one output -> verify -> relaunch reruns only it;
#  5 ownership / mode / no .part / dir inodes.  Every workflow is saved to argo_status/ and deleted.
set -u
export KUBECONFIG=/etc/kubernetes/student.conf
REPO=/home/users/jdochoa/hllhc-quirks-search
R=$REPO/tools/runner/bin/qv2run
W=$REPO/tools/runner/bin/qv2-watch
F=$REPO/tools/runner/examples/feas/feas-mini-argo.json
L=$REPO/analyses/quirks_v2/phase1_strategy/outputs/feasibility/runner_ledger/markers/feas-mini-argo
D=/nfs/cajuela/jdochoa/quirks_v2/data/feasibility/runner/feas-mini-argo
O=/nfs/cajuela/jdochoa/quirks_v2/data/feasibility/runner
S=$O/argo_status
SEL=owner=jdochoa,study=quirks-v2,qv2-campaign=feas-mini-argo
ts() { date +%H:%M:%S; }
ndone() { grep -l '"status":"done"' $L/*/*.marker 2>/dev/null | wc -l; }
dpid() { python3 -c "import json;print(json.load(open('$L/_driver/driver.json'))['pid'])"; }
save_wfs() { for w in $(kubectl get wf -n argo -l $SEL -o name | sed 's|.*/||'); do argo get -n argo $w -o json > $S/$w.json; done; }
echo "$(ts) T0"; T0=$(date +%s.%N)
$R argo launch $F --nodes landau --max-parallel 2 --keep --on landau
until [ "$(ndone)" -ge 6 ]; do sleep 5; done
P=$(dpid); echo "$(ts) step1: done=$(ndone); driver RSS $(ps -o rss= -p $P) kB; kill -9 driver $P"; kill -9 $P
sleep 30
echo "$(ts) step1: no driver for 30 s: done=$(ndone); workflow phase $(kubectl get wf -n argo -l $SEL -o jsonpath='{.items[*].status.phase}')"
stat -c '%n inode=%i' $D/000 $D/001 > $O/mini-argo-dir-inodes-before.txt
$R argo launch $F --nodes landau --max-parallel 2 --keep --on landau
sleep 8
POD=$(kubectl get pods -n argo -l $SEL --field-selector=status.phase=Running -o jsonpath='{.items[0].metadata.name}')
echo "$(ts) step2: delete running pod $POD"; kubectl delete pod -n argo $POD --wait=false
$W $F 10 600; echo "$(ts) watcher exit $?"
T1=$(date +%s.%N); echo "makespan_s $(python3 -c "print(round($T1-$T0,1))")"
save_wfs
echo "non-trivial marker histories:"; for m in $L/*/*.marker; do h=$(python3 -c "import json;print(' '.join(json.loads(l)['status'] for l in open('$m')))"); [ "$h" != "started done" ] && echo "  $(basename $m .marker): $h"; done
echo "$(ts) step3: relaunch on a complete campaign:"; $R argo launch $F --nodes landau --max-parallel 2 --keep 2>&1 | grep -E 'submitted|finished'
echo "$(ts) step4: corrupt mini-argo-013"; printf 'X' >> $D/001/mini-argo-013.dat
$R verify $F | tail -2
$R argo launch $F --nodes landau --max-parallel 2 --keep 2>&1 | grep -E 'submitted|finished'
$R verify $F | tail -1
save_wfs
echo "$(ts) step5: files (uid:gid mode count):"; find $D -type f -printf '%U:%G %m\n' | sort | uniq -c
echo "dirs:"; find $D -type d -printf '%U:%G %m %p\n'
echo "part files left: $(find $D -name '*.part' | wc -l)"
stat -c '%n inode=%i' $D/000 $D/001 > $O/mini-argo-dir-inodes-after.txt
diff $O/mini-argo-dir-inodes-{before,after}.txt && echo "dir inodes unchanged"
$R status $F
for w in $(kubectl get wf -n argo -l $SEL -o name | sed 's|.*/||'); do argo delete -n argo $w; done
echo "workflows left: $(kubectl get wf -n argo -l $SEL -o name | wc -l)"
echo "$(ts) END"
