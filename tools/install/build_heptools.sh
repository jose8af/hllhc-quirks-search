#!/usr/bin/env bash
# build_heptools.sh -- build HepMC 2.06.09 (static, build-only), Pythia 8.313 and MG5aMC_PY8_interface V1.3 on a
# WORKER's local disk, with the FINAL install prefix baked in, and pack the install into ONE tarball
# (/var/tmp/jdochoa/heptools_stage/heptools_py8313.tar.gz).  Unpacking that tarball into $QV2_SW is a separate step
# (install_generators.sh, with nice -n 19 ionice -c3).  quirks v2, executor Basil, 2026-11-13.
# Versions: those of MG's HEPToolsInstaller V168 (hepmc 2.06.09, interface V1.3), Pythia pinned to 8.313 as v1.
# Pythia is built WITHOUT LHAPDF (v1 never used it in Pythia: CP5 uses the internal PDF:pSet = 20) and with system zlib
# (gzip input for events.lhe.gz).  Usage (on schrodinger):  bash build_heptools.sh
set -euo pipefail
if [ "$(hostname -s)" = "einstein" ]; then echo "refusing to build on einstein"; exit 1; fi
DL=/var/tmp/jdochoa/dl
B=/var/tmp/jdochoa/build_heptools
ST=/var/tmp/jdochoa/heptools_stage
FINAL=/home/users/jdochoa/sw/mg5/MG5_aMC_v2_9_22/HEPTools
J=${J:-3}
echo "d07e801501c4dcb76d948dc63285375f597453c1d6ec65e71287603dc776718c  $DL/pythia8313.tgz
e0f8fddd38472c5615210894444686ac5d72df3be682f7d151b562b236d9b422  $DL/hepmc2.06.09.tgz
1a7a62e96207701f9a8a44fec01426b7f474b580ba2c4fbb82ecd0d83fcea332  $DL/MG5aMC_PY8_interface_V1.3.tar.gz
f4759cf3deeeb8eb5a95ac6150eb4dd2b8510c106e7ad548844fa0210025365f  $DL/HEPToolsInstaller_V168.tar.gz" | sha256sum -c -
rm -rf "$B" "$ST"; mkdir -p "$B" "$ST"
cd "$B"
# ---- HepMC 2.06.09: static library only, local prefix (linked statically into the interface; never installed) ----
tar xzf "$DL/hepmc2.06.09.tgz"
HM=$B/hepmc2.06.09        # the MG-mirrored tarball unpacks to hepmc2.06.09/ (autotools configure present)
# MG's HEPToolsInstaller V168 (installHEPMC2.sh) replaces WeightContainer.{h,cc} so HepMC2 can write NAMED weights;
# with -DHEPMC2HACK the interface then writes ONE HepMC file with all weights (v1 behaviour), instead of one file per
# weight (20 x 190 MB per 1000 events, found 2026-11-13).
HI=/var/tmp/jdochoa/src/HEPToolsInstallers
mkdir -p /var/tmp/jdochoa/src && tar xzf "$DL/HEPToolsInstaller_V168.tar.gz" -C /var/tmp/jdochoa/src
cp "$HI/WeightContainer.cc" "$HM/src/WeightContainer.cc"; cp "$HI/WeightContainer.h" "$HM/HepMC/WeightContainer.h"
(cd "$HM" && ./configure --prefix="$B/hepmc" --with-momentum=GEV --with-length=MM --enable-static > ../hepmc_configure.log 2>&1 \
   && nice -n 10 make -j"$J" > ../hepmc_make.log 2>&1 && make install > ../hepmc_install.log 2>&1)
# ---- Pythia 8.313 with the final prefix ----
tar xzf "$DL/pythia8313.tgz"
cd "$B/pythia8313"
./configure --prefix="$FINAL/pythia8" --with-hepmc2="$B/hepmc" --with-gzip > ../py8_configure.log 2>&1
nice -n 10 make -j"$J" > ../py8_make.log 2>&1
make install PREFIX_BIN="$ST/pythia8/bin" PREFIX_INCLUDE="$ST/pythia8/include" PREFIX_LIB="$ST/pythia8/lib" \
     PREFIX_SHARE="$ST/pythia8/share/Pythia8" > ../py8_install.log 2>&1
# ---- MG5aMC_PY8_interface V1.3 (same recipe as its compile.py: static HepMC2, Pythia's Makefile.inc flags) ----
mkdir -p "$ST/MG5aMC_PY8_interface"
tar xzf "$DL/MG5aMC_PY8_interface_V1.3.tar.gz" -C "$ST/MG5aMC_PY8_interface"
cd "$ST/MG5aMC_PY8_interface"
# -DGZIP is REQUIRED: it changes the LHEF reader classes in Pythia's headers; without it the interface cannot read
# events.lhe.gz ("BeamSetup::initFrame: Les Houches initialization failed") and then loops forever (found 2026-11-13).
PYFLAGS="$(sed -n 's/^CXX_COMMON=//p' "$ST/pythia8/share/Pythia8/examples/Makefile.inc") -DHEPMC2HACK -DHEPMC2"
g++ "$HI/test-hepmc2hack.cc" -o "$B/test-hepmc2hack" -I"$B/hepmc/include" -L"$B/hepmc/lib" -lHepMC > "$B/hepmc2hack_test.log" 2>&1 \
  || { echo "HepMC named-weight patch not active"; exit 1; }
nice -n 10 g++ MG5aMC_PY8_interface.cc -o MG5aMC_PY8_interface $PYFLAGS \
   -I"$ST/pythia8/include" -I"$B/hepmc/include" -I. \
   -L"$ST/pythia8/lib" -Wl,-rpath,"$FINAL/pythia8/lib" -lpythia8 -ldl -lz "$B/hepmc/lib/libHepMC.a" > "$B/py8i_make.log" 2>&1
nice -n 10 g++ pythia8_version.cc -o get_pythia8_version_bin -I"$ST/pythia8/include" -L"$ST/pythia8/lib" \
   -Wl,-rpath,"$FINAL/pythia8/lib" -lpythia8 -ldl >> "$B/py8i_make.log" 2>&1 || true
# the two files MG reads (madevent_interface.py l.3967-3972), with the content compile.py l.204-205 writes
printf '2.9.22' > MG5AMC_VERSION_ON_INSTALL
printf '8.313' > PYTHIA8_VERSION_ON_INSTALL
echo "MG5aMC_PY8_interface V1.3 built $(date -Is) against Pythia 8.313 ($FINAL/pythia8), HepMC 2.06.09 (static, named-weight patch)" > BUILD_INFO_QV2
# ---- one tarball ----
cd "$ST"
tar czf heptools_py8313.tar.gz.part pythia8 MG5aMC_PY8_interface
mv heptools_py8313.tar.gz.part heptools_py8313.tar.gz
echo "files: $(tar tzf heptools_py8313.tar.gz | wc -l)  size: $(du -h heptools_py8313.tar.gz | cut -f1)"
sha256sum heptools_py8313.tar.gz
