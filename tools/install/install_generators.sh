#!/usr/bin/env bash
# install_generators.sh -- MG5_aMC 2.9.22 + Pythia 8.313 + MG5aMC_PY8_interface + LHAPDF (v1 PDF sets) for quirks v2.
# Written by executor Basil (Phase 1 feasibility, 2026-11-13). Idempotent: every step is skipped if its product exists.
# Run on a WORKER (builds are CPU-heavy), e.g.:  ssh -x schrodinger 'bash /home/users/jdochoa/hllhc-quirks-search/tools/install/install_generators.sh'
# Products (shared NFS, same path on every node and pod):
#   $QV2_SW/mg5/MG5_aMC_v2_9_22          MG install, HEPTools/{pythia8,MG5aMC_PY8_interface,hepmc,zlib,...}
#   $QV2_SW/envs/mg                       pixi workspace: python 3.9, six, numpy 1.26, lhapdf 6.5 (conda-forge)
#   $QV2_SW/lhapdf_data                   CT18NLO (59 members) + NNPDF23_lo_as_0130_qed member 0, v1 patched .info files
# Build tree: /var/tmp/jdochoa/build_generators (node-local).  Downloads only from the official sources below.
set -euo pipefail
. /home/users/jdochoa/hllhc-quirks-search/tools/env.sh
TT=$REPO/stage2_C001_quirks/theory_track
DL=/var/tmp/jdochoa/build_generators/dl
mkdir -p "$DL" "$QV2_SW/mg5" "$QV2_SW/envs/mg" "$QV2_SW/lhapdf_data"
UA="generic-client"

fetch() {  # url file sha256
  local url=$1 f=$DL/$2 sha=$3
  if [ ! -s "$f" ] || ! echo "$sha  $f" | sha256sum -c --quiet - 2>/dev/null; then
    curl -sSL -A "$UA" -o "$f" "$url"
  fi
  echo "$sha  $f" | sha256sum -c - || { echo "sha256 mismatch for $f (from $url)"; exit 1; }
}

# ---- 1. sources (sha256 measured 2026-11-13; MG md5 bb67626ef4e607b31c4544af8fa91e7b = launchpad +md5) ----
fetch https://launchpad.net/mg5amcnlo/lts/2.9.x/+download/MG5_aMC_v2.9.22.tar.gz MG5_aMC_v2.9.22.tar.gz \
      c15fac434458cc3c1d0637afc351889b7203f12a8b6e5b4b1545a93393198092
fetch https://pythia.org/releases/pythia83/pythia8313.tgz pythia8313.tgz \
      d07e801501c4dcb76d948dc63285375f597453c1d6ec65e71287603dc776718c
fetch https://lhapdfsets.web.cern.ch/current/CT18NLO.tar.gz CT18NLO.tar.gz \
      c9127231e77e97cbec79cb5839203ab00f8db77237a061b61f9420f2b7b9c213
fetch https://lhapdfsets.web.cern.ch/current/NNPDF23_lo_as_0130_qed.tar.gz NNPDF23_lo_as_0130_qed.tar.gz \
      60d3c1df1c31e5840f91f4217163ae30a256b9291a5adc894882e86607ef5d63

# ---- 2. MG5_aMC ----
MG=$QV2_SW/mg5/MG5_aMC_v2_9_22
if [ ! -x "$MG/bin/mg5_aMC" ]; then
  tar xzf "$DL/MG5_aMC_v2.9.22.tar.gz" -C "$QV2_SW/mg5"
  cp "$MG/input/mg5_configuration.txt" "$QV2_SW/mg5/mg5_configuration.release.txt"
  # the only change to the install: no interactive update check (it blocks non-interactive starts for 60 s)
  sed -i 's/^# auto_update = 7/auto_update = 0/' "$MG/input/mg5_configuration.txt"
fi

# ---- 3. pixi env for MG (Python 3.9: MG 2.9.22 calls python3.12 "experimental, not for production") ----
cat > "$QV2_SW/envs/mg/pixi.toml" <<'EOF'
# MG5_aMC 2.9.22 runtime env (quirks v2). Same choice as v1 TT/sim/pixi.toml env `mg`.
[workspace]
name = "qv2-mg"
channels = ["conda-forge"]
platforms = ["linux-64"]

[dependencies]
python = "3.9.*"
six = "*"
numpy = "1.26.*"
lhapdf = "6.5.*"
EOF
(cd "$QV2_SW/envs/mg" && pixi install)
PY=$QV2_SW/envs/mg/.pixi/envs/default/bin/python3

# ---- 4. LHAPDF data (v1 tracked, patched .info + lhapdf.conf + pdfsets.index; members from the official tarballs) ----
L=$QV2_SW/lhapdf_data
if [ ! -s "$L/CT18NLO/CT18NLO_0058.dat" ]; then
  X=$(mktemp -d /var/tmp/jdochoa/build_generators/pdfXXXX)
  tar xzf "$DL/CT18NLO.tar.gz" -C "$X"
  tar xzf "$DL/NNPDF23_lo_as_0130_qed.tar.gz" -C "$X" NNPDF23_lo_as_0130_qed/NNPDF23_lo_as_0130_qed_0000.dat
  mkdir -p "$L/CT18NLO" "$L/NNPDF23_lo_as_0130_qed"
  cp "$X"/CT18NLO/CT18NLO_00*.dat "$L/CT18NLO/"
  cp "$X"/NNPDF23_lo_as_0130_qed/NNPDF23_lo_as_0130_qed_0000.dat "$L/NNPDF23_lo_as_0130_qed/"
  rm -rf "$X"
fi
cp "$TT/data/sim/lhapdf/CT18NLO/CT18NLO.info" "$L/CT18NLO/"
cp "$TT/data/sim/lhapdf/NNPDF23_lo_as_0130_qed/NNPDF23_lo_as_0130_qed.info" "$L/NNPDF23_lo_as_0130_qed/"
cp "$TT/data/sim/lhapdf/lhapdf.conf" "$TT/data/sim/lhapdf/pdfsets.index" "$L/"

# ---- 5. HEPTools: Pythia 8.313 (pinned tarball) + MG5aMC_PY8_interface, through MG's own installer ----
export PYTHONDONTWRITEBYTECODE=1
if [ ! -x "$MG/HEPTools/MG5aMC_PY8_interface/MG5aMC_PY8_interface" ]; then
  B=/var/tmp/jdochoa/build_generators
  cat > "$B/heptools.mg" <<EOF
install pythia8 --pythia8_tarball=$DL/pythia8313.tgz
install mg5amc_py8_interface
exit
EOF
  (cd "$B" && PATH=$QV2_SW/envs/mg/.pixi/envs/default/bin:$PATH nice -n 10 "$PY" "$MG/bin/mg5_aMC" "$B/heptools.mg" < /dev/null \
     > "$QV2_SW/mg5/heptools_install.log" 2>&1)
fi
grep -h "^\s*pythia8_path\|^\s*mg5amc_py8_interface_path" "$MG/input/mg5_configuration.txt" || true
"$MG/HEPTools/pythia8/bin/pythia8-config" --version 2>/dev/null || true
echo "install_generators.sh: done"
