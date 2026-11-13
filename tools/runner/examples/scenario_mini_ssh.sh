#!/bin/bash
# TEST ONLY. 24-job mini-campaign through the SSH backend on landau (max 2 concurrent), with fault injection:
#  1 kill the launcher (SIGKILL) midway and resume it;  2 SIGTERM one running job (clean kill -> retry);
#  3 SIGKILL another job's wrapper and payload (hard death -> liveness 'lost' -> retry, debris cleaned);
#  4 idempotency (relaunch dispatches nothing; direct run skips);  5 corrupt one output -> verify -> rerun;
#  6 ownership 10015:10000, mode 644, no .part left, directory inodes unchanged.
set -u
. /home/users/jdochoa/hllhc-quirks-search/tools/env.sh
R=$REPO/tools/runner/bin/qv2run
F=$REPO/tools/runner/examples/feas/feas-mini-ssh.json
L=$QV2/phase1_strategy/outputs/feasibility/runner_ledger/markers/feas-mini-ssh
D=$QV2_DATA/feasibility/runner/feas-mini-ssh
ts() { date +%H:%M:%S; }
cnt() { $R status --json $F | python3 -c 'import json,sys; c=json.load(sys.stdin)["counts"]; print(c.get(sys.argv[1],0))' "$1"; }
wait_done() { while [ "$(cnt done)" -lt "$1" ]; do sleep 3; done; }
running_rec() { # newest 'started' record of a running job: job pid
  python3 - "$L" <<'EOF'
import json, sys, pathlib
best = None
for m in pathlib.Path(sys.argv[1]).glob("*/*.marker"):
    r = json.loads(m.read_text().splitlines()[-1])
    if r["status"] == "started" and (best is None or r["ts"] > best["ts"]):
        best = r
print(best["job_id"], best["pid"]) if best else print("none 0")
EOF
}
echo "$(ts) T0 start"; T0=$(date +%s.%N)
$R ssh launch $F --nodes landau --max-per-node 2 --detach
wait_done 6
DPID=$(python3 -c "import json;print(json.load(open('$L/_driver/driver.json'))['pid'])")
echo "$(ts) step1: $(cnt done) done; SIGKILL driver pid $DPID"; kill -9 $DPID
sleep 25
echo "$(ts) step1: with no driver: done $(cnt done) running $(cnt running) (running jobs must finish on their own)"
ls -d $D/000 $D/001 2>/dev/null | while read d; do stat -c '%n inode=%i' $d; done > /nfs/cajuela/jdochoa/quirks_v2/data/feasibility/runner/mini-ssh-dir-inodes-before.txt
$R ssh launch $F --nodes landau --max-per-node 2 --detach
sleep 15
read J P < <(running_rec)
echo "$(ts) step2: SIGTERM wrapper of $J (pid $P on landau)"; ssh -x landau "kill -TERM $P"
sleep 15
read J2 P2 < <(running_rec)
echo "$(ts) step3: SIGKILL the wrapper only of $J2 (pid $P2): worst case, payload orphaned"
ssh -x landau "kill -KILL $P2; sleep 1; ls -d /home/scratch/jdochoa/$J2 && echo scratch-left-behind; systemctl --user list-units --plain --no-legend 'qv2-$J2-*'"
$R watch $F --interval 10 --grace 60; echo "$(ts) watch exit $?"
T1=$(date +%s.%N); echo "makespan $(python3 -c "print(round($T1-$T0,1))") s"
echo "$(ts) step3: scratch of $J2 after retry:"; ssh -x landau "ls -d /home/scratch/jdochoa/$J2 2>&1 | tail -1; ls /home/scratch/jdochoa; echo scopes:; systemctl --user list-units --plain --no-legend 'qv2-*'"
echo "$(ts) step4: relaunch on a complete campaign:"; $R ssh launch $F --nodes landau --max-per-node 2 2>&1 | tail -2
echo "$(ts) step4: direct run of a done job:"; ssh -x landau "$REPO/tools/runner/bin/qv2-job --campaign $F --job mini-ssh-005 --mechanism ssh" 2>&1 | tail -2
echo "$(ts) step5: corrupt mini-ssh-007 output"; printf 'X' >> $D/000/mini-ssh-007.dat
$R verify $F; echo "verify exit $?"
$R ssh launch $F --nodes landau --max-per-node 2 2>&1 | grep -E 'dispatched|finished'
$R verify $F; echo "verify exit after rerun $?"
echo "$(ts) step6: ownership/mode"; find $D -type f -printf '%U:%G %m %p\n' | awk '{print $1, $2}' | sort | uniq -c
find $D -name '*.part' | wc -l | sed 's/^/part files left: /'
find $D -type d -printf '%U:%G %m %p\n'
ls -d $D/000 $D/001 | while read d; do stat -c '%n inode=%i' $d; done > /nfs/cajuela/jdochoa/quirks_v2/data/feasibility/runner/mini-ssh-dir-inodes-after.txt
diff /nfs/cajuela/jdochoa/quirks_v2/data/feasibility/runner/mini-ssh-dir-inodes-{before,after}.txt && echo "dir inodes unchanged"
$R status -vv $F | awk '{print $3}' | sort | uniq -c
echo "$(ts) END"
