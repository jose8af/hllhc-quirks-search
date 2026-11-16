#!/bin/bash
# launch of p2-c-px-lt_znn_add1 on 2 slot(s) of NODE (default schrodinger): one queue per slot, 1 job each.
# Run on einstein AFTER: preflight ok, a line in phase2_exploration/SLOTS.md, the go of the orchestrator.
# Resume after any stop: run this script again (complete campaigns and done jobs are skipped).
NODE=${1:-schrodinger}
echo "qv2run jobs on $NODE now: $(ssh -x -o BatchMode=yes $NODE "pgrep -u jdochoa -af '[q]v2run job' | wc -l")"
ssh -x -o BatchMode=yes $NODE "mkdir -p /home/scratch/jdochoa/drivers; rm -f /home/scratch/jdochoa/drivers/STOP.p2-c-px-lt-znn-02; if [ -e /home/scratch/jdochoa/drivers/p2-c-px-lt_znn_add1_2slots_lane0.pid ] && kill -0 \$(cat /home/scratch/jdochoa/drivers/p2-c-px-lt_znn_add1_2slots_lane0.pid) 2>/dev/null; then echo lane 0 already runs; else setsid nohup bash -c 'echo \$\$ > /home/scratch/jdochoa/drivers/p2-c-px-lt_znn_add1_2slots_lane0.pid; exec /home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2/phase2_exploration/src/p2x_queue.sh $NODE 1 /home/users/jdochoa/hllhc-quirks-search/tools/runner/examples/p2x/launch_test/p2-c-px-lt-znn-02.json' > /home/scratch/jdochoa/drivers/p2-c-px-lt_znn_add1_2slots_lane0.log 2>&1 < /dev/null & echo lane 0 started; fi"
