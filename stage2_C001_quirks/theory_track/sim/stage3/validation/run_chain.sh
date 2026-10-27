#!/bin/bash
# Stage-3 validation chain (E7): waits for the V2b production subset, then V2a, V1 (re-run on s3.2), V4, V6, V3.
cd "$(dirname "$0")/../../.."
while pgrep -f "jobs/v2b.json" > /dev/null; do sleep 20; done
for v in v2a v1 v4 v6 v3; do
  echo "=== $v start $(date)"
  nice pixi run python sim/stage3/validation/val_$v.py > data/sim_stage3/validation/$(echo $v | tr a-z A-Z)_stdout.txt 2>&1
  echo "=== $v exit $? $(date)"
done
