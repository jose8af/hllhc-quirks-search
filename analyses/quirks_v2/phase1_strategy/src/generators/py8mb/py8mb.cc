// py8mb.cc -- Pythia 8 minimum-bias (pile-up input) benchmark with the v1 settings (quirks v2 Phase 1, executor Basil).
// Settings = v1 TT/acts/stage4/code/s4pu.py PY_MB (l.31-33) on top of the CP5 card (TT/sim/cards/pythia8_tune_CP5.dat,
// identical to TT/acts/scripts/pythia8_tune_CP5.dat).  Like v1, the RNG is re-initialised per interaction
// (rndm.init(seed)), and the selection into Fatras (final-state charged + photons, pT > 50 MeV, |eta| < 4) is counted.
// Usage: py8mb <cp5_card> <nevents> <seed> [hepmc_out|-]
#include "Pythia8/Pythia.h"
#include <cmath>
#include <ctime>
#include <cstdio>
#include <string>
#ifdef WITH_HEPMC2
#include "Pythia8Plugins/HepMC2.h"
#endif
using namespace Pythia8;

int main(int argc, char** argv) {
  if (argc < 4) { std::fprintf(stderr, "usage: py8mb cp5.dat nev seed [hepmc|-]\n"); return 2; }
  int nev = std::atoi(argv[2]);
  int seed = std::atoi(argv[3]);
  std::string hep = argc > 4 ? argv[4] : "-";
  Pythia py("../share/Pythia8/xmldoc", false);
  py.readFile(argv[1]);
  const char* lines[] = {"Beams:eCM = 14000.", "SoftQCD:inelastic = on", "ParticleDecays:limitTau0 = on",
                         "ParticleDecays:tau0Max = 1000.", "211:mayDecay = off", "321:mayDecay = off",
                         "13:mayDecay = off", "130:mayDecay = off", "Print:quiet = on", "Next:numberCount = 0",
                         "Next:numberShowEvent = 0", "Next:numberShowInfo = 0", "Next:numberShowProcess = 0",
                         "Random:setSeed = on"};
  for (auto l : lines) py.readString(l);
  py.readString("Random:seed = " + std::to_string(seed));
  std::clock_t c0 = std::clock();
  if (!py.init()) return 1;
  std::clock_t c1 = std::clock();
#ifdef WITH_HEPMC2
  HepMC::Pythia8ToHepMC toHepMC;
  HepMC::IO_GenEvent* io = hep != "-" ? new HepMC::IO_GenEvent(hep, std::ios::out) : nullptr;
#endif
  long nsel = 0, nfin = 0;
  for (int i = 0; i < nev; ++i) {
    py.rndm.init(seed * 1000 + i + 1);
    if (!py.next()) continue;
    for (int k = 0; k < py.event.size(); ++k) {
      const Particle& p = py.event[k];
      if (!p.isFinal()) continue;
      ++nfin;
      if ((p.isCharged() || p.id() == 22) && p.pT() > 0.05 && std::abs(p.eta()) < 4.0) ++nsel;
    }
#ifdef WITH_HEPMC2
    if (io) { HepMC::GenEvent* ev = new HepMC::GenEvent(); toHepMC.fill_next_event(py, ev); *io << ev; delete ev; }
#endif
  }
  std::clock_t c2 = std::clock();
#ifdef WITH_HEPMC2
  delete io;
#endif
  std::printf("PY8MB nev=%d init_cpu_s=%.3f event_cpu_s=%.3f cpu_ms_per_event=%.3f final_per_ev=%.1f sel_per_ev=%.1f "
              "sigmaGen_mb=%.4g\n", nev, double(c1 - c0) / CLOCKS_PER_SEC, double(c2 - c1) / CLOCKS_PER_SEC,
              1e3 * double(c2 - c1) / CLOCKS_PER_SEC / nev, double(nfin) / nev, double(nsel) / nev,
              py.info.sigmaGen());
  return 0;
}
