#!/bin/bash
# TEST ONLY. Run ON landau. Quiet-server re-measurement: 3x Argo then 3x SSH of the ~60 s CPU job, one at a time.
export KUBECONFIG=/etc/kubernetes/student.conf
REPO=/home/users/jdochoa/hllhc-quirks-search; R=$REPO/tools/runner/bin/qv2run; E=$REPO/tools/runner/examples/feas
S=/nfs/cajuela/jdochoa/quirks_v2/data/feasibility/runner/argo_status
echo "argo start $(date +%s.%N)"; $R argo launch $E/feas-cpu60q-argo.json --nodes landau --max-parallel 1 --keep | grep -E 'submitted|finished'; echo "argo end $(date +%s.%N)"
for w in $(kubectl get wf -n argo -l owner=jdochoa,study=quirks-v2,qv2-campaign=feas-cpu60q-argo -o name | sed 's|.*/||'); do argo get -n argo $w -o json > $S/$w.json; argo delete -n argo $w; done
sleep 20
echo "ssh start $(date +%s.%N)"; $R ssh launch $E/feas-cpu60q-ssh.json --nodes landau --max-per-node 1 --poll 5 | grep -E 'dispatched|finished'; echo "ssh end $(date +%s.%N)"
echo END
