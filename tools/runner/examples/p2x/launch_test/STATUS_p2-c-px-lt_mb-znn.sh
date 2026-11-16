#!/bin/bash
# status of p2-c-px-lt_mb-znn from the markers (run on einstein; the runner itself runs on the worker)
NODE=${1:-schrodinger}
ssh -x -o BatchMode=yes $NODE 'for f in /home/users/jdochoa/hllhc-quirks-search/tools/runner/examples/p2x/launch_test/p2-c-px-lt-mb.json /home/users/jdochoa/hllhc-quirks-search/tools/runner/examples/p2x/launch_test/p2-c-px-lt-znn-00.json /home/users/jdochoa/hllhc-quirks-search/tools/runner/examples/p2x/launch_test/p2-c-px-lt-znn-01.json; do /home/users/jdochoa/hllhc-quirks-search/tools/runner/bin/qv2run status $f --json; done; tail -n 2 /home/scratch/jdochoa/drivers/p2-c-px-lt_mb-znn_*lane*.log 2>/dev/null; pgrep -u jdochoa -af "[q]v2run job" | wc -l'
