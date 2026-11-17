#!/bin/bash
# launch of p2-c-pilot_b1_offroad on 2 lane(s): one queue per lane, 1 job each.  Usage: LAUNCH NODE0 [NODE1 [NODE2]]
# (default schrodinger for every lane; lane i runs on NODEi, or on the last node given).
# Run on einstein AFTER: preflight ok, a line in phase2_exploration/SLOTS.md, the approval (orchestrator launches).
# Resume after any stop: run this script again with the same nodes (complete campaigns and done jobs are skipped).
NODES=("$@"); [ ${#NODES[@]} -eq 0 ] && NODES=(schrodinger)
NODE=${NODES[0]:-${NODES[-1]}}
echo "lane 0 on $NODE; qv2run jobs there now: $(ssh -x -o BatchMode=yes $NODE "pgrep -u jdochoa -af '[q]v2run job' | wc -l")"
ssh -x -o BatchMode=yes $NODE "mkdir -p /home/scratch/jdochoa/drivers; rm -f /home/scratch/jdochoa/drivers/STOP.p2-c-pilot-hpo; if [ -e /home/scratch/jdochoa/drivers/p2-c-pilot_b1_offroad_2slots_lane0.pid ] && kill -0 \$(cat /home/scratch/jdochoa/drivers/p2-c-pilot_b1_offroad_2slots_lane0.pid) 2>/dev/null; then echo lane 0 already runs; else setsid nohup bash -c 'echo \$\$ > /home/scratch/jdochoa/drivers/p2-c-pilot_b1_offroad_2slots_lane0.pid; exec /home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2/phase2_exploration/src/p2x_queue.sh $NODE 1 /home/users/jdochoa/hllhc-quirks-search/tools/runner/examples/p2x/b1_optional/p2-c-pilot-hpo.json /home/users/jdochoa/hllhc-quirks-search/tools/runner/examples/p2x/b1_optional/p2-c-pilot-g4o.json /home/users/jdochoa/hllhc-quirks-search/tools/runner/examples/p2x/b1_optional/p2-c-pilot-c0-offroad.json' > /home/scratch/jdochoa/drivers/p2-c-pilot_b1_offroad_2slots_lane0.log 2>&1 < /dev/null & echo lane 0 started; fi"
