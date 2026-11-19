# C1-c container test: permission for one docker build, amendment E5, base-image exception (not urgent; due by the Phase 5 review)

**What happened.** C1-c (Linux reproducibility) asks for one C1 job to be rerun in a container with an "identical
output hash". The executor wrote the container recipe (commit 26f4abe, `tools/container/qv2-c1/`). The permission
system refused the docker image build on maxwell. No agent may work around a refusal, so nothing has been built or
run. C1-c stands as NOT TESTED. It does not block decision point 1 or the freeze: its deadline is the Phase 5 review.
An independent advisor checked everything below.

## Questions (defaults are my recommendation)
1. **Amendment E5: compare file content, not the file hash.** Every output file records its creation time, CPU and
   wall time, and hostname. No rerun can therefore reproduce the file hash, inside a container or outside it. This
   follows from reading the code, before any run.
   - Proposed wording: every array is byte-identical, except the timing entries, which are already skipped by the
     C2-b "bit-identical" test.
   - In the metadata, every field is equal except the creation time, the timings, the hostname and the platform.
     The code, input and library-version hashes must be equal.
   - The file sha256 is still reported, and is expected to differ.
   - *Default: approve, labelled "amended before any rerun".*
2. **Base image.** The pinned image (Ubuntu 24.04) is not available to docker on the workers. The recipe instead
   uses the local Ubuntu 22.04 image already there, with no pull: digest `e9569c25505f…af999`, present on maxwell
   and schrodinger. The pin is an operations rule, not frozen text, and the test of reproducibility is unchanged.
   *Default: accept, as a recorded exception.*
3. **The docker build and one rerun on maxwell.** This needs your permission. Before you give it:
   - Docker group membership is root-equivalent on shared workers, and the image lands in the shared docker store.
   - The build downloads packages from conda-forge/PyPI. It does not use Docker Hub.
   - The rerun is confined: no network, your uid, 2.25 GB, 1 CPU, only `/home/scratch/jdochoa` mounted.
   - The image can be removed afterwards (`docker rmi`).

   Choose one of:
   - (a) Run the build yourself (about 10–20 min):
     `! ssh -x maxwell 'nice -n 19 ionice -c3 /home/users/jdochoa/hllhc-quirks-search/tools/container/qv2-c1/build.sh 26f4abe'`
     An agent then runs the one rerun job, which may need the same permission.
   - (b) Add a permission rule for exactly that build and the one `ctr_exec.sh` runner job.
   - (c) Do not allow docker builds on the workers. C1-c then stays NOT TESTED and is disclosed as such.

   *Default: none. I will not act on item 3 without your answer.*

**Without an answer:** C1-c is reported as "NOT TESTED, recipe committed" at decision point 1 and onwards. E5 and
the base-image exception are applied only if you approve them.
