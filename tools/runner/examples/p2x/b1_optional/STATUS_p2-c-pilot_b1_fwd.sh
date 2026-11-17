#!/bin/bash
# status of p2-c-pilot_b1_fwd from the markers.  Usage: STATUS [NODE ...] (the nodes given to LAUNCH; default schrodinger)
NODES=("$@"); [ ${#NODES[@]} -eq 0 ] && NODES=(schrodinger)
ssh -x -o BatchMode=yes ${NODES[0]} 'for f in /home/users/jdochoa/hllhc-quirks-search/tools/runner/examples/p2x/b1_optional/p2-c-pilot-g4f.json /home/users/jdochoa/hllhc-quirks-search/tools/runner/examples/p2x/b1_optional/p2-c-pilot-c0-fwd.json; do /home/users/jdochoa/hllhc-quirks-search/tools/runner/bin/qv2run status $f --json; done'
for N in $(printf "%s\n" "${NODES[@]}" | sort -u); do echo "== $N"; ssh -x -o BatchMode=yes $N 'tail -n 2 /home/scratch/jdochoa/drivers/p2-c-pilot_b1_fwd_*lane*.log 2>/dev/null; pgrep -u jdochoa -af "[q]v2run job" | wc -l'; done
