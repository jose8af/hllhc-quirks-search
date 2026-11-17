#!/bin/bash
# status of p2-c-pilot_mb from the markers (run on einstein; the runner itself runs on the worker)
NODE=${1:-schrodinger}
ssh -x -o BatchMode=yes $NODE 'for f in /home/users/jdochoa/hllhc-quirks-search/tools/runner/examples/p2x/pilot/p2-c-pilot-mb.json; do /home/users/jdochoa/hllhc-quirks-search/tools/runner/bin/qv2run status $f --json; done; tail -n 2 /home/scratch/jdochoa/drivers/p2-c-pilot_mb_*lane*.log 2>/dev/null; pgrep -u jdochoa -af "[q]v2run job" | wc -l'
