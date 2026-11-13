#!/bin/bash
# TEST ONLY. Run ON landau:  ssh -x landau 'nohup …/scenario_mini_ssh.sh > LOG 2>&1 &'
# 24-job mini-campaign through the SSH backend (driver detached on landau, max 2 jobs) with fault injection:
#  1 kill -9 the driver midway; running jobs finish on their own; restart the driver -> it resumes;
#  2 SIGTERM one running wrapper (clean kill -> 'killed' -> retried);  3 kill -9 another wrapper (-> 'lost' -> retried);
#  4 idempotency;  5 corrupt one output -> verify -> rerun only it;  6 ownership/mode/.part/dir inodes.
set -u
REPO=/home/users/jdochoa/hllhc-quirks-search
R=$REPO/tools/runner/bin/qv2run
W=$REPO/tools/runner/bin/qv2-watch
F=$REPO/tools/runner/examples/feas/feas-mini-ssh.json
L=$REPO/analyses/quirks_v2/phase1_strategy/outputs/feasibility/runner_ledger/markers/feas-mini-ssh
D=/nfs/cajuela/jdochoa/quirks_v2/data/feasibility/runner/feas-mini-ssh
O=/nfs/cajuela/jdochoa/quirks_v2/data/feasibility/runner
ts() { date +%H:%M:%S; }
ndone() { grep -l '"status":"done"' $L/*/*.marker 2>/dev/null | wc -l; }
nrun() { for m in $L/*/*.marker; do tail -1 $m; done 2>/dev/null | grep -c '"status":"started"'; }
running_pid() { for m in $L/*/*.marker; do tail -1 $m; done 2>/dev/null | grep '"status":"started"' | tail -1 |
  python3 -c 'import json,sys; r=json.loads(sys.stdin.read()); print(r["job_id"], r["pid"])'; }
dpid() { python3 -c "import json;print(json.load(open('$L/_driver/driver.json'))['pid'])"; }
echo "$(ts) T0"; T0=$(date +%s.%N)
$R ssh launch $F --nodes landau --max-per-node 2 --poll 5 --on landau
until [ "$(ndone)" -ge 6 ]; do sleep 5; done
P=$(dpid); echo "$(ts) step1: done=$(ndone); driver RSS $(ps -o rss= -p $P) kB; kill -9 driver $P"; kill -9 $P
sleep 30
echo "$(ts) step1: no driver for 30 s: done=$(ndone) running=$(nrun) (only jobs already running continue)"
stat -c '%n inode=%i' $D/000 $D/001 > $O/mini-ssh-dir-inodes-before.txt 2>/dev/null
$R ssh launch $F --nodes landau --max-per-node 2 --poll 5 --on landau
until [ "$(nrun)" -ge 1 ]; do sleep 2; done; sleep 4
read J P < <(running_pid); echo "$(ts) step2: SIGTERM wrapper of $J (pid $P)"; kill -TERM $P
sleep 12
read J2 P2 < <(running_pid); echo "$(ts) step3: kill -9 wrapper of $J2 (pid $P2); payload orphaned"; kill -KILL $P2
$W $F 10 300; echo "$(ts) watcher exit $?"
T1=$(date +%s.%N); echo "makespan_s $(python3 -c "print(round($T1-$T0,1))")"
echo "$(ts) marker histories of $J and $J2:"; for j in $J $J2; do echo "  $j: $(python3 -c "import json;print([json.loads(l)['status'] for l in open('$(ls $L/*/$j.marker)')])")"; done
echo "scratch left: $(ls /home/scratch/jdochoa | grep -c mini-ssh)  scopes left: $(systemctl --user list-units --plain --no-legend 'qv2-mini-*' | wc -l)"
echo "$(ts) step4: relaunch on a complete campaign (foreground):"; $R ssh launch $F --nodes landau --max-per-node 2 2>&1 | grep -E 'dispatch|finished'
echo "$(ts) step4: direct run of a done job:"; $REPO/tools/runner/bin/qv2-job --campaign $F --job mini-ssh-005 --mechanism ssh 2>&1 | tail -1
echo "$(ts) step5: corrupt mini-ssh-007"; printf 'X' >> $D/000/mini-ssh-007.dat
$R verify $F | tail -2
$R ssh launch $F --nodes landau --max-per-node 2 2>&1 | grep -E 'dispatched|finished'
$R verify $F | tail -1
echo "$(ts) step6: files (uid:gid mode count):"; find $D -type f -printf '%U:%G %m\n' | sort | uniq -c
echo "dirs:"; find $D -type d -printf '%U:%G %m %p\n'
echo "part files left: $(find $D -name '*.part' | wc -l)"
stat -c '%n inode=%i' $D/000 $D/001 > $O/mini-ssh-dir-inodes-after.txt
diff $O/mini-ssh-dir-inodes-{before,after}.txt && echo "dir inodes unchanged"
$R status $F
echo "$(ts) END"
