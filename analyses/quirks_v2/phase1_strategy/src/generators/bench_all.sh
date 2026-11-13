#!/usr/bin/env bash
# bench_all.sh -- task-3 benchmarks on one worker (schrodinger), node-local work dirs only (quirks v2 Phase 1, Basil).
# Each benchmark: 3 sequential single jobs + 3 concurrent jobs, /usr/bin/time -v (bench.sh). Run nothing else meanwhile.
# Usage: bash bench_all.sh [names...]   (default: all)
set -uo pipefail
. /home/users/jdochoa/hllhc-quirks-search/tools/env.sh
G=$QV2/phase1_strategy/src/generators
R=/home/scratch/jdochoa/basil_bench
S=/home/scratch/jdochoa/basil_samples          # compiled process dirs + LHE from make_test_samples.sh
CP5=$REPO/stage2_C001_quirks/theory_track/sim/cards/pythia8_tune_CP5.dat
H=$QV2_SW/mg5/MG5_aMC_v2_9_22/HEPTools/pythia8
mkdir -p "$R"
B="bash $G/bench.sh"
FM="QV2_MODELS={W}/models python3 $G/feas_mg.py"
MOD="cp -r $S/models {W}/"
names=${*:-"mg_output_E mg_output_Z mg_first_E mg_first_Z mg_gen1k_E mg_gen1k_Z mg_gen10k_E py8_E py8_Z py8_qed_E py8mb_1k"}
for n in $names; do
  rm -rf "$R/$n"
  case $n in
    mg_output_E) $B $n $R both -- "$MOD && $FM output E_LOPS {W}/p" ;;
    mg_output_Z) $B $n $R both -- "$MOD && $FM output ZNN_J {W}/p" ;;
    # output + first launch (compilation + survey/refine) with 1000 events
    mg_first_E) $B $n $R both -- "$MOD && $FM output E_LOPS {W}/p && $FM launch {W}/p r 1000 $((31000)){I} 200" ;;
    mg_first_Z) $B $n $R both -- "$MOD && $FM output ZNN_J {W}/p && $FM launch {W}/p r 1000 $((32000)){I}" ;;
    # generation only: a compiled MG process dir is NOT relocatable (MG writes lib/libLHAPDF.a as a RELATIVE symlink
    # ../../../../../users/...; a copied dir at another depth then links libLHAPDF.so and gensym fails), so each replica
    # makes its own output + warm-up launch (100 events) and only the second launch is timed (inner time file).
    mg_warm_gen1k_E) $B $n $R both -- "$MOD && $FM output E_LOPS {W}/p && $FM launch {W}/p w 100 3600{I} 200 && /usr/bin/time -v -o {W}/inner_time.txt env $FM launch {W}/p r 1000 3700{I} 200" ;;
    mg_warm_gen1k_Z) $B $n $R both -- "$MOD && $FM output ZNN_J {W}/p && $FM launch {W}/p w 100 3800{I} && /usr/bin/time -v -o {W}/inner_time.txt env $FM launch {W}/p r 1000 3900{I}" ;;
    mg_warm_gen10k_E) $B $n $R both -- "$MOD && $FM output E_LOPS {W}/p && $FM launch {W}/p w 100 4000{I} 200 && /usr/bin/time -v -o {W}/inner_time.txt env $FM launch {W}/p r 10000 4100{I} 200" ;;
    # (superseded, kept for the record: these failed for the reason above)
    mg_gen1k_E) $B $n $R both -- "$MOD && cp -r $S/E_LOPS {W}/p && rm -rf {W}/p/Events/* && $FM launch {W}/p r 1000 3300{I} 200" ;;
    mg_gen1k_Z) $B $n $R both -- "$MOD && cp -r $S/ZNN_J {W}/p && rm -rf {W}/p/Events/* && $FM launch {W}/p r 1000 3400{I}" ;;
    mg_gen10k_E) $B $n $R both -- "$MOD && cp -r $S/E_LOPS {W}/p && rm -rf {W}/p/Events/* && $FM launch {W}/p r 10000 3500{I} 200" ;;
    # Pythia 8.313 shower (MG5aMC_PY8_interface, v1 card: CP5 + quirk_common) of 1000 LHE events; HepMC written
    py8_E) $B $n $R both -- "mkdir -p {W}/p/Events/E200 && cp $S/E_LOPS/Events/E200/{unweighted_events.lhe.gz,*_banner.txt} {W}/p/Events/E200/ && python3 $G/feas_mg.py shower {W}/p E200 4100{I} && ls -l {W}/p/Events/E200/py8/events.hepmc && rm {W}/p/Events/E200/py8/events.hepmc" ;;
    py8_Z) $B $n $R both -- "mkdir -p {W}/p/Events/Z1 && cp $S/ZNN_J/Events/Z1/{unweighted_events.lhe.gz,*_banner.txt} {W}/p/Events/Z1/ && python3 $G/feas_mg.py shower {W}/p Z1 4200{I} && ls -l {W}/p/Events/Z1/py8/events.hepmc && rm {W}/p/Events/Z1/py8/events.hepmc" ;;
    py8_qed_E) $B $n $R both -- "mkdir -p {W}/p/Events/E200 && cp $S/E_LOPS/Events/E200/{unweighted_events.lhe.gz,*_banner.txt} {W}/p/Events/E200/ && python3 $G/feas_mg.py shower {W}/p E200 4300{I} qedfsr && ls -l {W}/p/Events/E200/py8_qed/events.hepmc && rm {W}/p/Events/E200/py8_qed/events.hepmc" ;;
    # Pythia minimum bias (v1 s4pu PY_MB + CP5), 1000 interactions, no file output (v1 kept PU in memory)
    py8mb_1k) $B $n $R both -- "PYTHIA8DATA=$H/share/Pythia8/xmldoc /var/tmp/jdochoa/py8mb/py8mb $CP5 1000 5{I}" ;;
    # Geant4 11.4.3 FTFP_BERT, pi+- gun (pT log-uniform 1-10 GeV, |eta| < 1) through the v1 barrel slabs in 3.8 T;
    # full = all secondaries tracked by Geant4; primary = secondaries recorded at the vertex then killed (hand-over mode)
    g4_full_20k) $B $n $R both -- "PIXI_CACHE_DIR=/home/scratch/jdochoa/cache/rattler pixi run --manifest-path /home/scratch/jdochoa/envs/g4/pixi.toml --frozen /var/tmp/jdochoa/g4sv_build/g4sv $G/g4sv/geom_barrel.txt 20000 6{I} full {W}/sv.csv && ls -l {W}/sv.csv" ;;
    g4_primary_20k) $B $n $R both -- "PIXI_CACHE_DIR=/home/scratch/jdochoa/cache/rattler pixi run --manifest-path /home/scratch/jdochoa/envs/g4/pixi.toml --frozen /var/tmp/jdochoa/g4sv_build/g4sv $G/g4sv/geom_barrel.txt 20000 7{I} primary {W}/sv.csv && ls -l {W}/sv.csv" ;;
  esac
done
