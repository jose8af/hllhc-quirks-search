#!/usr/bin/env bash
# install_generators.sh -- MG5_aMC 2.9.22 + Pythia 8.313 + MG5aMC_PY8_interface V1.3 + LHAPDF (v1 PDF sets), quirks v2.
# Written by executor Basil (Phase 1 feasibility, 2026-11-13). Idempotent: every step is skipped if its product exists.
# Run ON A WORKER (never on einstein), when no benchmark runs there:
#   ssh -x schrodinger 'bash /home/users/jdochoa/hllhc-quirks-search/tools/install/install_generators.sh'
# NFS rules (AGENT_RULES "einstein and NFS home rules"): builds in /var/tmp/jdochoa (local); every write to the NFS home
# is a tarball unpack under `nice -n 19 ionice -c3`; the `pixi install` of sw/envs/mg needs the study's install slot.
# Products (same absolute path on every node and pod):
#   $QV2_SW/mg5/MG5_aMC_v2_9_22           MG (4071 files) + HEPTools/{pythia8, MG5aMC_PY8_interface} (≈ 925 files)
#   $QV2_SW/envs/mg                       pixi: python 3.9, six, numpy 1.26, lhapdf 6.5 (conda-forge)
#   $QV2_SW/lhapdf_data                   CT18NLO (59 members) + NNPDF23_lo_as_0130_qed member 0, v1 patched .info files
set -euo pipefail
. /home/users/jdochoa/hllhc-quirks-search/tools/env.sh
if [ "$(hostname -s)" = "einstein" ]; then echo "refusing to run on einstein"; exit 1; fi
TT=$REPO/stage2_C001_quirks/theory_track
DL=/var/tmp/jdochoa/dl
mkdir -p "$DL" "$QV2_SW/mg5" "$QV2_SW/envs/mg" "$QV2_SW/lhapdf_data"
IO="nice -n 19 ionice -c3"

fetch() {  # url file sha256   (downloads only from the official sources; no personal data sent)
  local url=$1 f=$DL/$2 sha=$3
  if [ ! -s "$f" ] || ! echo "$sha  $f" | sha256sum -c --quiet - 2>/dev/null; then
    curl -sSL -A generic-client -o "$f" "$url"
  fi
  echo "$sha  $f" | sha256sum -c - || { echo "sha256 mismatch for $f (from $url)"; exit 1; }
}

# ---- 1. sources (sha256 measured 2026-11-13) ----
fetch https://launchpad.net/mg5amcnlo/lts/2.9.x/+download/MG5_aMC_v2.9.22.tar.gz MG5_aMC_v2.9.22.tar.gz \
      c15fac434458cc3c1d0637afc351889b7203f12a8b6e5b4b1545a93393198092      # md5 bb67626e… = launchpad +md5
fetch https://pythia.org/releases/pythia83/pythia8313.tgz pythia8313.tgz \
      d07e801501c4dcb76d948dc63285375f597453c1d6ec65e71287603dc776718c
fetch https://madgraph.mi.infn.it/Downloads/hepmc2.06.09.tgz hepmc2.06.09.tgz \
      e0f8fddd38472c5615210894444686ac5d72df3be682f7d151b562b236d9b422
fetch http://madgraph.mi.infn.it//Downloads/MG5aMC_PY8_interface/MG5aMC_PY8_interface_V1.3.tar.gz \
      MG5aMC_PY8_interface_V1.3.tar.gz 1a7a62e96207701f9a8a44fec01426b7f474b580ba2c4fbb82ecd0d83fcea332
fetch http://madgraph.mi.infn.it//Downloads/HEPToolsInstaller/HEPToolsInstaller_V168.tar.gz HEPToolsInstaller_V168.tar.gz \
      f4759cf3deeeb8eb5a95ac6150eb4dd2b8510c106e7ad548844fa0210025365f
fetch https://lhapdfsets.web.cern.ch/current/CT18NLO.tar.gz CT18NLO.tar.gz \
      c9127231e77e97cbec79cb5839203ab00f8db77237a061b61f9420f2b7b9c213
fetch https://lhapdfsets.web.cern.ch/current/NNPDF23_lo_as_0130_qed.tar.gz NNPDF23_lo_as_0130_qed.tar.gz \
      60d3c1df1c31e5840f91f4217163ae30a256b9291a5adc894882e86607ef5d63

# ---- 2. MG5_aMC (untouched release, except input/.autoupdate) ----
MG=$QV2_SW/mg5/MG5_aMC_v2_9_22
if [ ! -x "$MG/bin/mg5_aMC" ]; then
  $IO tar xzf "$DL/MG5_aMC_v2.9.22.tar.gz" -C "$QV2_SW/mg5"
fi
# No update check ever: last_check in the year 2100 (an `auto_update = 0` line in input/mg5_configuration.txt is read as
# a string and crashes MG's exit hook, abs(str); and an update check would rewrite this file from every job).
printf "version_nb   319\nlast_check   4102444800\n" > "$MG/input/.autoupdate"
# No MadLoop reduction tools from the web into the NFS install (ninja/collier/golem); CutTools + IREGI (shipped in
# vendor/) are enough for 2 -> 2 NLO QCD. These are the lines MG itself writes on "noinstall".
sed -i 's|^# golem = auto|golem = None|; s|^# ninja = ./HEPTools/lib|ninja = None|; s|^# collier = ./HEPTools/lib *$|collier = None|' "$MG/input/mg5_configuration.txt"

# ---- 3. pixi env for MG (Python 3.9: MG 2.9.22 calls python3.12 "experimental ... not for production") ----
# Needs the study's install slot (orchestrator). Manifest kept here verbatim.
if [ ! -x "$QV2_SW/envs/mg/.pixi/envs/default/bin/python3.9" ]; then
  cat > "$QV2_SW/envs/mg/pixi.toml" <<'EOF'
# MG5_aMC 2.9.22 runtime env (quirks v2, executor Basil, 2026-11-13). Same choice as v1 TT/sim/pixi.toml env `mg`:
# MG 2.9.x warns that python3.12 is experimental ("not for production"), so Python 3.9 + six + numpy 1.26 + LHAPDF.
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
  (cd "$QV2_SW/envs/mg" && $IO pixi install)
fi

# ---- 4. LHAPDF data (v1 tracked, patched .info + lhapdf.conf + pdfsets.index; members from the official tarballs) ----
L=$QV2_SW/lhapdf_data
if [ ! -s "$L/CT18NLO/CT18NLO_0058.dat" ]; then
  X=/var/tmp/jdochoa/pdf_unpack; rm -rf "$X"; mkdir -p "$X/CT18NLO" "$X/NNPDF23_lo_as_0130_qed"
  tar xzf "$DL/CT18NLO.tar.gz" -C "$X"
  tar xzf "$DL/NNPDF23_lo_as_0130_qed.tar.gz" -C "$X" NNPDF23_lo_as_0130_qed/NNPDF23_lo_as_0130_qed_0000.dat
  rm -f "$X"/CT18NLO/CT18NLO.info
  (cd "$X" && tar cf - CT18NLO NNPDF23_lo_as_0130_qed) | (cd "$L" && $IO tar xf -)
fi
cp "$TT/data/sim/lhapdf/CT18NLO/CT18NLO.info" "$L/CT18NLO/"
cp "$TT/data/sim/lhapdf/NNPDF23_lo_as_0130_qed/NNPDF23_lo_as_0130_qed.info" "$L/NNPDF23_lo_as_0130_qed/"
cp "$TT/data/sim/lhapdf/lhapdf.conf" "$TT/data/sim/lhapdf/pdfsets.index" "$L/"

# ---- 5. HEPTools: Pythia 8.313 + MG5aMC_PY8_interface V1.3, built locally, installed as ONE tarball ----
H=$MG/HEPTools
if [ ! -x "$H/MG5aMC_PY8_interface/MG5aMC_PY8_interface" ]; then
  bash "$REPO/tools/install/build_heptools.sh"
  mkdir -p "$H" && (cd "$H" && $IO tar xzf /var/tmp/jdochoa/heptools_stage/heptools_py8313.tar.gz)
fi
"$H/pythia8/bin/pythia8-config" --version
ldd "$H/MG5aMC_PY8_interface/MG5aMC_PY8_interface" | grep pythia8
echo "install_generators.sh: done"
