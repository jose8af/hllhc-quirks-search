#!/bin/bash
# run_vshower.sh -- V-SHOWER validation sample (plan §4 / V8; review S2-R1 B5, B-1; fixer 2026-10-11).
# Re-showers the kept LHE of E-TRG and E-INC m = 500 GeV chunk 0 (50k LHE each) with the Pythia shower renormalisation
# scale varied coherently for ISR and FSR: mu_R x 2 (renormMultFac = 4, "DN" in alpha_s) and mu_R x 1/2 (renormMultFac =
# 0.25, "UP" in alpha_s).  Same LHE, same card and seeds as the nominal jobs otherwise (scripts/reshower.py), so the
# nominal reference is the chunk-0 rows of the delivered files (column chunk).  Output: data/sim/npz/V-SHOWER-<VAR>-<S>_m500.npz
# (merged over the 6 Pythia jobs), analysed by scripts/val_shower.py.  Cost ~ 4 x 50k events x ~17 ms (PY8 + conversion).
# Run from sim/:  bash scripts/run_vshower.sh
set -e
cd "$(dirname "$0")/.."
DATA=../data/sim
TMP=$DATA/aux/fixer/vshower_tmp
for VAR in UP DN; do
  if [ $VAR = UP ]; then F=0.25; else F=4.0; fi
  for S in TRG INC; do
    OUT=$DATA/npz/V-SHOWER-$VAR-${S}_m500.npz
    [ -f $OUT ] && { echo "skip $OUT"; continue; }
    D=$TMP/$VAR-$S; mkdir -p $D
    python3 scripts/reshower.py --id E-$S --m 500 --chunk 0 --out $D --set "SpaceShower:renormMultFac = $F" \
        --set "TimeShower:renormMultFac = $F" --convert $D/job
    pixi run -e ana python scripts/merge_chunks.py $OUT $D/job_s*.npz
    mkdir -p $DATA/aux/fixer/V-SHOWER-$VAR-$S
    for j in 0 1 2 3 4 5; do cp $D/split_$j/PY8Card.dat $DATA/aux/fixer/V-SHOWER-$VAR-$S/PY8Card_job$j.dat; \
        cp $D/split_$j/PY8_log.txt $DATA/aux/fixer/V-SHOWER-$VAR-$S/PY8_log_job$j.txt; done
    rm -rf $D
  done
done
rmdir $TMP 2>/dev/null || true
