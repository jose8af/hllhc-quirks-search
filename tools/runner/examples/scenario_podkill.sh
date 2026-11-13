#!/bin/bash
# TEST ONLY. Run ON landau. Delete a running pod mid-job; expect wrapper 'killed' line, then Argo OnError retry
# (or driver resubmission) -> done. Saves and deletes the workflow.
export KUBECONFIG=/etc/kubernetes/student.conf
REPO=/home/users/jdochoa/hllhc-quirks-search; R=$REPO/tools/runner/bin/qv2run
F=$REPO/tools/runner/examples/feas/feas-podkill.json
L=$REPO/analyses/quirks_v2/phase1_strategy/outputs/feasibility/runner_ledger/markers/feas-podkill
S=/nfs/cajuela/jdochoa/quirks_v2/data/feasibility/runner/argo_status
SEL=owner=jdochoa,study=quirks-v2,qv2-campaign=feas-podkill
$R argo launch $F --nodes landau --max-parallel 2 --keep > /home/scratch/jdochoa/drivers/podkill.log 2>&1 &
until grep -qs '"status":"started"' $L/000/podkill-1.marker; do sleep 1; done; sleep 5
POD=$(python3 -c "import json;print(json.loads(open('$L/000/podkill-1.marker').readline())['pod'])")
echo "$(date +%T) delete pod $POD"; kubectl delete pod -n argo $POD --wait=false
wait
cat /home/scratch/jdochoa/drivers/podkill.log | grep -E 'submitted|marked|finished'
for m in $L/000/*.marker; do echo "$(basename $m): $(python3 -c "import json;print([json.loads(l)['status'] for l in open('$m')])")"; done
for w in $(kubectl get wf -n argo -l $SEL -o name | sed 's|.*/||'); do argo get -n argo $w -o json > $S/$w.json
  python3 -c "import json;w=json.load(open('$S/$w.json'));print('$w', w['status']['phase'], [(n['displayName'],n['phase'],n.get('message','')[:60]) for n in w['status']['nodes'].values() if n['type']=='Pod'])"
  argo delete -n argo $w; done
echo END
