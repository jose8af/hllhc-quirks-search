#!/usr/bin/env bash
# make_test_samples.sh -- task 2 test samples (quirks v2 Phase 1, executor Basil). Run on a worker (schrodinger):
#   bash make_test_samples.sh
# Work dir: node-local /home/scratch/jdochoa/basil_samples; final files -> cajuela data/feasibility/generators/<sample>/
# written as .part, sha256-checked after the copy, renamed; MANIFEST.txt per sample dir; one marker per file in
# analyses/quirks_v2/ledger/markers/feasibility_generators/ (format as Anselm's feasibility_chain markers).
# Samples:  E_LOPS_m200 : p p > xe+ xe- (v1 F_LOPS / E-LOPS cards), m_E = 200 GeV, 1000 LHE events, MG iseed 21902001
#                         (= v1 E-LOPS m200 chunk 0 seed), PY8 seed 219020011 (v1 rule (iseed*10+j) mod 9e8 + 1, j = 0)
#           ZNN_J       : p p > vl vl~ j, MET (misset) > 200 GeV, 1000 LHE events, iseed 7001, PY8 seed 70011
# Sigma-only runs (no shower, not copied): 20000 events each, seeds 21902101 / 7101.
set -euo pipefail
. /home/users/jdochoa/hllhc-quirks-search/tools/env.sh
G=$QV2/phase1_strategy/src/generators
W=/home/scratch/jdochoa/basil_samples
OUT=$QV2_DATA/feasibility/generators
MK=$QV2/ledger/markers/feasibility_generators
mkdir -p "$W/models" "$MK"
[ -d "$W/models/quirkE" ] || cp -r "$G/models/quirkE" "$W/models/"
export QV2_MODELS=$W/models
T="/usr/bin/time -v -a -o $W/times.txt"
cd "$W"
step() { echo "=== $* $(date -Is)" >> "$W/times.txt"; nice -n 10 $T python3 "$G/feas_mg.py" "$@" >> "$W/driver.log" 2>&1; }
[ -d E_LOPS ] || step output E_LOPS "$W/E_LOPS"
[ -d ZNN_J ] || step output ZNN_J "$W/ZNN_J"
[ -s E_LOPS/Events/E200/unweighted_events.lhe.gz ] || step launch "$W/E_LOPS" E200 1000 21902001 200
[ -s E_LOPS/Events/E200/py8/events.hepmc ] || step shower "$W/E_LOPS" E200 219020011
[ -s ZNN_J/Events/Z1/unweighted_events.lhe.gz ] || step launch "$W/ZNN_J" Z1 1000 7001
[ -s ZNN_J/Events/Z1/py8/events.hepmc ] || step shower "$W/ZNN_J" Z1 70011
[ -s E_LOPS/Events/E200_xs/unweighted_events.lhe.gz ] || step launch "$W/E_LOPS" E200_xs 20000 21902101 200
[ -s ZNN_J/Events/Z_xs/unweighted_events.lhe.gz ] || step launch "$W/ZNN_J" Z_xs 20000 7101

publish() {  # sample procdir run
  local s=$1 d=$W/$2/Events/$3 o=$OUT/$1
  mkdir -p "$o"
  [ -s "$d/py8/events.hepmc.gz" ] || nice -n 10 gzip -k -6 "$d/py8/events.hepmc"
  tar czf "$d/aux.tar.gz" -C "$W" "$2/Cards/run_card.dat" "$2/Cards/param_card.dat" "$2/Cards/proc_card_mg5.dat" \
      "$2/Events/$3/$(cd "$d" && ls *_banner.txt)" "$2/Events/$3/py8/PY8Card.dat" "$2/Events/$3/py8/PY8_log.txt" \
      "launch_$3.log" "output_$2.log"
  : > "$o/MANIFEST.txt.part"
  for f in unweighted_events.lhe.gz py8/events.hepmc.gz aux.tar.gz; do
    local src=$d/$f b; b=$(basename "$f")
    local sha; sha=$(sha256sum "$src" | cut -d' ' -f1)
    cp "$src" "$o/$b.part"; sync "$o/$b.part"
    [ "$(sha256sum "$o/$b.part" | cut -d' ' -f1)" = "$sha" ] || { echo "copy check failed $b"; exit 1; }
    mv "$o/$b.part" "$o/$b"; stat "$o/$b" > /dev/null
    local bytes; bytes=$(stat -c %s "$o/$b")
    printf '%s  %s  %s\n' "$sha" "$bytes" "$b" >> "$o/MANIFEST.txt.part"
    printf '{"bytes": %s, "host": "%s", "job": "basil_testsamples", "path": "%s", "sha256": "%s", "status": "done", "t": "%s", "writer": "basil/feasibility"}\n' \
      "$bytes" "$(hostname -s)" "$o/$b" "$sha" "$(date +%Y-%m-%dT%H:%M:%S%z)" > "$MK/feasibility__generators__${s}__${b}.marker"
  done
  mv "$o/MANIFEST.txt.part" "$o/MANIFEST.txt"
  cat "$o/MANIFEST.txt"
}
publish E_LOPS_m200 E_LOPS E200
publish ZNN_J ZNN_J Z1
grep -h "Cross-section\|Nb of events" launch_*.log
