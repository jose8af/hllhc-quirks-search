#!/usr/bin/env bash
# Run one runner job command inside the qv2-c1 image.  Used as the `command` of a runner job:
#   tools/container/qv2-c1/ctr_exec.sh qv2-c1:<sha12> '<the unchanged C1 job command>'
# The runner's wrapper (SSH mechanism) has already made the scratch dir, set QV2_* and cwd; we pass those through.
# Container: no network, same uid/gid, memory capped at QV2_CTR_MEM_MB (default 2250 MB, no swap), 1 CPU, nice 10
# inside; only /home/scratch/jdochoa is mounted (read-write). The image holds the code and the environments.
# Note: the docker client is what the runner measures; the container's own CPU times and peak memory are printed
# at the end of the job log ("ctr_stats").
set -euo pipefail
IMAGE=$1; CMD=$2
NAME="jdochoa-qv2-ctr-${QV2_JOB_ID:-x}-${QV2_ATTEMPT:-0}-$$"
MEM=${QV2_CTR_MEM_MB:-2250}
envs=()
for v in QV2_JOB_ID QV2_CAMPAIGN QV2_SHARD QV2_OUT_DIR QV2_SCRATCH_DIR QV2_FINAL_DIR QV2_REPO QV2_NODE QV2_ATTEMPT; do
    [ -n "${!v:-}" ] && envs+=(-e "$v=${!v}")
done
cleanup() { docker kill "$NAME" >/dev/null 2>&1 || true; }
trap 'cleanup; exit 143' TERM INT HUP
docker image inspect "$IMAGE" --format 'ctr_image {{.Id}} revision {{index .Config.Labels "org.opencontainers.image.revision"}}'
INNER='nice -n 10 bash -c "$QV2_CTR_CMD"; rc=$?; echo "ctr_stats rc=$rc"; times;
       echo "ctr_stats memory.peak_bytes=$(cat /sys/fs/cgroup/memory.peak 2>/dev/null || echo NA)";
       grep -E "^(usage_usec|user_usec|system_usec)" /sys/fs/cgroup/cpu.stat 2>/dev/null | sed "s/^/ctr_stats /"; exit $rc'
docker run --rm --pull=never --network none --name "$NAME" \
    --label owner=jdochoa --label study=quirks-v2 \
    --user 10015:10000 --memory "${MEM}m" --memory-swap "${MEM}m" --cpus 1 \
    -v /home/scratch/jdochoa:/home/scratch/jdochoa -w "$PWD" \
    "${envs[@]}" -e HOME=/home/users/jdochoa -e "QV2_CTR_CMD=$CMD" \
    "$IMAGE" bash -c "$INNER" &
wait $!
