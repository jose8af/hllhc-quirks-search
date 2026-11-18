"""c1_smregen_job.py -- channel (i), Ignatius 2026-11-18: run v1's gen_d123.py 'smregen' (unchanged) on the C1 SM
hit-level outputs (p2-a-c1-sm) to get each event's generator-level preselection weight (C1 family (v), STR §4.1).

Why a wrapper (trap in Rosalie's log, successor section): mode_smregen refuses unless the MPI init file exists at
gen_d123.TT / data/acts_stage4/g1/pythia_init/mpi_cp5_14tev_hs_<sample>.dat (v1 layout).  In v2 that file is a
node-local cache (s4pu.mpi_init_lines reads QV2_PYTHIA_INIT_DIR, default /home/scratch/jdochoa/cache/pythia_init) on the
node that ran c1-sm (landau).  The wrapper points gen_d123.TT at a scratch root holding two symlinks:
  <root>/data/acts_stage4/g1/pythia_init -> $QV2_PYTHIA_INIT_DIR   and   <root>/acts -> $QV2/acts
(the module constants CP5 and sys.path were set from the real tree at import time; the provenance hashes resolve
through the 'acts' link to the same files).  Nothing else changes; the event regeneration and its hs_met check are v1's.
Usage (runner job on landau, ACTS env python):  python c1_smregen_job.py <out.json> <sm npz> [...]
"""
import os
import sys
from pathlib import Path

QV2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(QV2 / "acts" / "stage4" / "analysis"))
import gen_d123 as G  # noqa: E402

init_dir = Path(os.environ.get("QV2_PYTHIA_INIT_DIR", "/home/scratch/jdochoa/cache/pythia_init"))
root = Path(os.environ.get("QV2_OUT_DIR", ".")).resolve() / "ttroot"
(root / "data" / "acts_stage4" / "g1").mkdir(parents=True, exist_ok=True)
for link, target in ((root / "data" / "acts_stage4" / "g1" / "pythia_init", init_dir), (root / "acts", QV2 / "acts")):
    if not link.is_symlink():
        link.symlink_to(target, target_is_directory=True)
G.TT = root
G.mode_smregen(sys.argv[1], sys.argv[2:])
