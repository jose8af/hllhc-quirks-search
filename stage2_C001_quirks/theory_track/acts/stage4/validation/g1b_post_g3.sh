#!/bin/zsh
# G1b post-G3 procedure (HASH_ADDENDUM.md): apply the two additive patches ONLY after the G3 runner has exited, verify
# the resulting sha256 equal the tested candidates, confirm the PU/SM/dens regression on the applied files, regenerate
# the C1 manifest.  Does NOT launch C1 and does NOT rerun the 2 failed G3 jobs (orchestrator decisions).
set -e
cd "${0:A:h}/../../.."
if pgrep -f "run_stage4 run" > /dev/null; then echo "REFUSED: a run_stage4 run is still alive"; exit 2; fi
pixi run python acts/stage4/validation/g1b_apply_hook.py
pixi run python acts/stage4/validation/g1b_apply_chainfix.py
A=$(shasum -a 256 acts/stage4/run_stage4.py | cut -d' ' -f1)
B=$(shasum -a 256 acts/stage4/code/run_chain.py | cut -d' ' -f1)
[[ "$A" == "1258e82a6ba0fd34d14c9aa6293075ef6e23bd6b90c0ff96298ef0b7dc07571c" ]] || { echo "run_stage4.py sha $A != tested candidate"; exit 3; }
[[ "$B" == "bdea0e276e30473908f93b7b23e75d3876e4d6b43893b78077accf21f24aec8d" ]] || { echo "run_chain.py sha $B != tested candidate"; exit 3; }
rm -f acts/stage4/_rs4_candidate.py acts/stage4/code/_run_chain_candidate.py
nice -n 15 pixi run python -m acts.stage4.validation.g1b_regress run after_applied
pixi run python -m acts.stage4.validation.g1b_regress compare before after_applied
pixi run python -c "from acts.stage4 import run_stage4 as R; d = R.make_manifest('C1'); print('C1 manifest:', len(d['jobs']), 'jobs')"
pixi run python -m acts.stage4.run_stage4 status --campaign C1
echo "G1b post-G3 procedure done: patches applied, regression above, C1 manifest regenerated (not launched)."
