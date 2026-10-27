#!/bin/bash
# run_all.sh -- single driver for Stage 2 (review S2-R1 B7c; fixer 2026-10-11).  Run from anywhere:
#   bash sim/scripts/run_all.sh <stage> [<stage> ...]        or  pixi run -e ana <stage>  (tasks in sim/pixi.toml)
# Stages, in dependency order (each one is resumable / idempotent):
#   probes    MG LO probes used by VALIDATION §1 (t3, t4, t12, t15, t16; every EW input set explicitly in the scripts)
#   produce   production of all points (scripts/produce.py, resumable; ~18 CPU-h) and the top-ups (--topup)
#   vshower   V-SHOWER re-showers (scripts/run_vshower.sh)
#   post      row map (add_rowmap.py), stitching (stitch_trg.py), MG --alps weights (run_alps.py)
#   validate  val_xsec -> annotate_npz -> val_spectra, val_mlm, val_tune, val_shower, val_lmax, val_interp, val_qed,
#             val_reshower (B-5 test), val_loader (theory-track env)
#   docs      make_samples_md.py, val_trgs_stats.py (S2-R2 C-3/C-7), val_summary.py > results/summary_tables.md,
#             val_headlines.py (VALIDATION §0)
#   all       = probes produce vshower post validate docs
# MG is always called with PYTHONDONTWRITEBYTECODE=1 (nothing is written into the MG install) and LHAPDF_DATA_PATH set.
set -e
SIM="$(cd "$(dirname "$0")/.." && pwd)"
TT="$(dirname "$SIM")"
MG="${MG5_DIR:?set MG5_DIR to the MadGraph5_aMC v2.9.22 install (see REPRODUCE.md)}"
export LHAPDF_DATA_PATH="$TT/data/sim/lhapdf" PYTHONDONTWRITEBYTECODE=1
cd "$SIM"
ana() { pixi run -e ana python "$@"; }
mg5() { pixi run -e mg python "$MG/bin/mg5_aMC" "$1" > "${1%.mg}.log" 2>&1; }

stage() {
  case "$1" in
    probes)
      # fresh tree: create the probe outputs, configure them, run the probes whose logs VALIDATION §1 parses.
      # existing tree: rerun t3/t4/t16 under new run names (*_rerun.log) and compare (results/probe_rerun.json).
      if [ ! -d mg_out/probe_E_incl ]; then
        mg5 probes/t2_out.mg; mg5 probes/t11_fr_out.mg
        for d in probe_E_incl probe_S_incl xcheck_FR_E xcheck_FR_S xcheck_HW_E xcheck_HW_S; do
          python3 scripts/mg_configure.py mg_out/$d ebeam1=7000.0 ebeam2=7000.0 pdlabel=lhapdf lhaid=14400 nevents=2000; done
        for t in t3_E_incl t4_xsec t12_xcheck t15_ewscheme t16_lo_grid; do echo "probe $t"; mg5 probes/$t.mg; done
      else
        pixi run -e mg python "$MG/bin/mg5_aMC" probes/t3_E_incl.mg > probes/t3_E_incl_rerun.log 2>&1
        mg5 probes/t4_xsec_rerun.mg; mg5 probes/t16_lo_grid_rerun.mg
        ana scripts/val_probe_rerun.py
      fi ;;
    produce)
      python3 scripts/produce.py
      python3 scripts/produce.py --topup ;;
    vshower)
      bash scripts/run_vshower.sh ;;
    post)
      ana scripts/add_rowmap.py
      ana scripts/stitch_trg.py
      ana scripts/run_alps.py ;;
    validate)
      ana scripts/val_xsec.py
      ana scripts/annotate_npz.py
      ana scripts/val_spectra.py; ana scripts/val_mlm.py; ana scripts/val_tune.py
      ana scripts/val_shower.py; ana scripts/val_lmax.py; ana scripts/val_interp.py; ana scripts/val_qed.py
      # B-5 regeneration test: one Pythia job re-showered and compared bit-for-bit
      python3 scripts/reshower.py --id E-INC --m 1500 --chunk 0 --splits 3 --out "$TT/data/sim/aux/fixer/repro" --convert "$TT/data/sim/aux/fixer/repro/r"
      ana scripts/val_reshower.py "$TT/data/sim/npz/E-INC_m1500.npz" 0 3 "$TT/data/sim/aux/fixer/repro/r_s3.npz" E-INC_m1500_c0_job3
      rm -rf "$TT/data/sim/aux/fixer/repro"
      (cd "$TT" && pixi run python sim/scripts/val_loader.py) ;;
    docs)
      ana scripts/make_samples_md.py
      ana scripts/val_trgs_stats.py
      ana scripts/val_summary.py > results/summary_tables.md
      ana scripts/val_headlines.py ;;
    all)
      for s in probes produce vshower post validate docs; do stage $s; done ;;
    *) echo "unknown stage $1"; exit 1 ;;
  esac
}
for s in "$@"; do stage "$s"; done
