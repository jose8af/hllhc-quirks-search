# quirks v2, commitment C1-c: container recipe for the C1 jobs (Linux, x86_64).
# Built by tools/container/qv2-c1/build.sh (never by hand): the build context is a `git archive` of one commit, so
# the code in the image is exactly that commit, and the two Python environments are installed with
# `pixi install --frozen` from the TRACKED lockfiles (envs/tt/pixi.lock, acts/pixi.lock). Nothing is solved.
#
# Base: ubuntu 22.04.3 by digest, already present in the docker store of maxwell and schrodinger (used with
# --pull=never: no Docker Hub traffic). The study's pinned pod image ubuntu@sha256:2198e4c6... lives only in the
# containerd k8s.io namespace of the workers and is not visible to docker (see C1C_CONTAINER_vidar_2026-11-19.md).
# Requirement from acts/pixi.toml: glibc >= 2.34 (pyacts 48.0.0 manylinux_2_34 wheel); 22.04 has 2.35.
#
# Paths inside the image are the host's absolute paths (brief 5.2), so the unchanged C1 job commands run as they are.
ARG BASE=ubuntu@sha256:e9569c25505f33ff72e88b2990887c9dcf230f23259da296eb814fc2b41af999
FROM ${BASE}

ENV REPO=/home/users/jdochoa/hllhc-quirks-search \
    QV2=/home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2 \
    PIXI_HOME=/home/users/jdochoa/.pixi \
    PIXI_CACHE_DIR=/var/tmp/pixi-cache \
    PIXI_NO_PATH_UPDATE=1 DO_NOT_TRACK=1 PIXI_NO_TELEMETRY=1 \
    SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \
    LANG=C.UTF-8

# Same uid/gid as on the hosts, so files written to the bind-mounted scratch belong to jdochoa.
RUN groupadd -g 10000 students \
 && useradd -u 10015 -g 10000 -d /home/users/jdochoa -M -s /bin/bash jdochoa \
 && mkdir -p /home/users/jdochoa/.pixi/bin /home/scratch/jdochoa /var/tmp/pixi-cache \
 && chown -R 10015:10000 /home/users/jdochoa /home/scratch/jdochoa /var/tmp/pixi-cache

# CA bundle copied from the build host (no apt in the recipe); pixi binary pinned by version and sha256 (build.sh).
COPY ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --chown=10015:10000 pixi /home/users/jdochoa/.pixi/bin/pixi
ENV PATH=/home/users/jdochoa/.pixi/bin:$PATH
USER 10015:10000

# 1) environments from the tracked lockfiles only (layer depends on the manifests + locks, not on the code)
COPY --chown=10015:10000 locks/envs/tt/ /home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2/envs/tt/
COPY --chown=10015:10000 locks/acts/ /home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2/acts/
RUN cd $QV2/envs/tt && pixi install --frozen \
 && cd $QV2/acts && pixi install --frozen \
 && rm -rf /var/tmp/pixi-cache/*

# 2) the code of one commit (git archive; ledger/ excluded)
COPY --chown=10015:10000 src/ /home/users/jdochoa/hllhc-quirks-search/

WORKDIR /home/scratch/jdochoa
