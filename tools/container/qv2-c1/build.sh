#!/usr/bin/env bash
# Build the qv2-c1 image on a worker (never on einstein).  Usage:  build.sh [COMMIT]      (default: HEAD)
#   ssh -x maxwell 'nice -n 19 ionice -c3 /home/users/jdochoa/hllhc-quirks-search/tools/container/qv2-c1/build.sh'
# This is a `pixi install` (two environments, from the tracked lockfiles): it needs the study's install slot (SLOTS.md).
# Writes: the build tree /var/tmp/jdochoa/qv2-ctr/ctx-<sha> (local disk) and the image qv2-c1:<sha12> in the local
# docker store. Nothing on NFS home, nothing pushed to any registry.
set -euo pipefail
REPO=/home/users/jdochoa/hllhc-quirks-search
HERE=$REPO/tools/container/qv2-c1
COMMIT=$(git -C "$REPO" rev-parse "${1:-HEAD}")
SHA12=${COMMIT:0:12}
PIXI_BIN=/home/users/jdochoa/.pixi/bin/pixi
PIXI_VERSION=0.84.2
PIXI_SHA256=32523b4d1f43ca1583579252bbf7f977f83e4ce16f1333225379ece9f46bff0c
BASE=ubuntu@sha256:e9569c25505f33ff72e88b2990887c9dcf230f23259da296eb814fc2b41af999

[ "$(hostname -s)" != einstein ] || { echo "not on einstein" >&2; exit 2; }
docker image inspect "$BASE" >/dev/null || { echo "base image $BASE not in the local docker store (no pull)" >&2; exit 2; }
echo "$PIXI_SHA256  $PIXI_BIN" | sha256sum -c --quiet
[ "$("$PIXI_BIN" --version)" = "pixi $PIXI_VERSION" ]

CTX=/var/tmp/jdochoa/qv2-ctr/ctx-$SHA12
rm -rf "$CTX"; mkdir -p "$CTX/src" "$CTX/locks/envs/tt" "$CTX/locks/acts"
git -C "$REPO" archive --format=tar "$COMMIT" -- analyses/quirks_v2 tools/env.sh tools/container \
    ':(exclude)analyses/quirks_v2/ledger' | tar -x -C "$CTX/src"
for f in envs/tt/pixi.toml envs/tt/pixi.lock acts/pixi.toml acts/pixi.lock; do
    git -C "$REPO" show "$COMMIT:analyses/quirks_v2/$f" > "$CTX/locks/$f"
done
cp "$PIXI_BIN" "$CTX/pixi"
cp /etc/ssl/certs/ca-certificates.crt "$CTX/"
git -C "$REPO" show "$COMMIT:tools/container/qv2-c1/Dockerfile" > "$CTX/Dockerfile"

docker build --pull=false --build-arg BASE="$BASE" \
    --label org.opencontainers.image.revision="$COMMIT" --label owner=jdochoa --label study=quirks-v2 \
    -t "qv2-c1:$SHA12" "$CTX"
docker image inspect "qv2-c1:$SHA12" --format 'image {{.Id}} size {{.Size}} created {{.Created}}'
