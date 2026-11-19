// fxfx_shower.cc -- FxFx (MC@NLO 0-1j) shower of quirk-pair LHE events with Pythia 8.313, written for the quirks v2
// study (channel (ii), S2-c FxFx piece).  Modelled on Pythia's examples/main164.cc (jet matching branch:
// CombineMatchingInput + JetMatchingMadgraph with JetMatching:doFxFx = on), without HepMC/Rivet.  Replaces
// MG5aMC_PY8_interface for FxFx, whose DJR histograms are booked for njet <= JetMatching:nJetMax but filled at
// nMEpartons, which overflows for MC@NLO events (segfault, FXFX_sune_2026-11-19.md section 6.2).
//
// Usage: fxfx_shower <card.cmnd> <out.txt>
//   The card holds all Pythia settings (built by s2_job.py fxfx_own_card from fxfx_py8_card: main164fxfx.cmnd
//   settings with qCut 45 / qCutME 30, nJetMax 1, CP5 + quirk cards + QED FSR) and Beams:LHEF.
// Output: one line per event that survives matching (weight != 0):
//   w  pt_pair  eta_pair  m_pair  pt_pair_hard  n_me  njet30  npnlo
//   w            = pythia.info.weightValueByIndex() (nominal, signed; units of the LHE weights, only ratios are used)
//   pt_pair etc. = pair of the final-state quirks (|id| 9000011/9000013, isFinal), as convert_hepmc.py (status 1)
//   pt_pair_hard = same for the hard-process quirks (process record, first copy with |status| 22 or 23)
//   n_me         = outgoing QCD partons in the hard process (process record, status 23)
//   njet30       = anti-kt R = 0.4 jets, pT > 30 GeV, |eta| < 5, from visible final-state particles except quirks
//   npnlo        = LHE event attribute npNLO (-1 if absent)
// A summary line starting with '#' is written at the end.
#include "Pythia8/Pythia.h"
#include "Pythia8Plugins/CombineMatchingInput.h"
#include <cstdio>

using namespace Pythia8;

static bool isQuirk(int id) { int a = abs(id); return a == 9000011 || a == 9000013; }

int main(int argc, char** argv) {
  if (argc != 3) { fprintf(stderr, "usage: %s card.cmnd out.txt\n", argv[0]); return 2; }
  Pythia pythia;
  if (!pythia.readFile(argv[1])) { fprintf(stderr, "card %s: unreadable or unknown setting\n", argv[1]); return 3; }
  if (!pythia.flag("JetMatching:merge") || !pythia.flag("JetMatching:doFxFx")) {
    fprintf(stderr, "card must set JetMatching:merge = on and JetMatching:doFxFx = on\n"); return 3;
  }
  CombineMatchingInput jetMatchingHook;
  jetMatchingHook.setHook(pythia);
  if (!pythia.init()) return 1;

  FILE* out = fopen(argv[2], "w");
  if (!out) { fprintf(stderr, "cannot open %s\n", argv[2]); return 4; }
  fprintf(out, "# w pt_pair eta_pair m_pair pt_pair_hard n_me njet30 npnlo\n");
  SlowJet slow(-1, 0.4, 30.0, 5.0, 2, 1);   // anti-kt R 0.4, pT > 30, |eta| < 5, visible final state, massive
  const long nEvent = pythia.mode("Main:numberOfEvents");
  const int nAbort = pythia.mode("Main:timesAllowErrors");
  int iAbort = 0;
  long nNext = 0, nOut = 0, nNeg = 0, nZero = 0;
  double sw = 0., sabs = 0.;
  while (nEvent <= 0 || pythia.info.nSelected() < nEvent) {
    ++nNext;
    if (!pythia.next()) {
      if (pythia.info.atEndOfFile()) break;
      if (++iAbort > nAbort) { fprintf(stderr, "too many aborts\n"); fclose(out); return 5; }
      continue;
    }
    const double w = pythia.info.weightValueByIndex();
    if (w == 0.) { ++nZero; continue; }
    const Event& ev = pythia.event;
    Vec4 pq, pqh;
    int nq = 0, nme = 0;
    for (int i = 0; i < ev.size(); ++i)
      if (ev[i].isFinal() && isQuirk(ev[i].id())) { pq += ev[i].p(); ++nq; }
    const Event& pr = pythia.process;
    bool seenP = false, seenM = false;   // quirks are status 22 (isResonance on, QED-FSR card) or 23: first copy each
    for (int i = 0; i < pr.size(); ++i) {
      const int st = pr[i].statusAbs();
      if (isQuirk(pr[i].id()) && (st == 22 || st == 23)) {
        bool& seen = pr[i].id() < 0 ? seenP : seenM;
        if (!seen) { pqh += pr[i].p(); seen = true; }
      } else if (st == 23 && (pr[i].idAbs() <= 6 || pr[i].id() == 21)) ++nme;
    }
    if (nq != 2) { fprintf(stderr, "event %ld: %d final-state quirks\n", nNext, nq); fclose(out); return 6; }
    Event vis;
    vis.init("vis", &pythia.particleData);
    vis.clear();
    for (int i = 0; i < ev.size(); ++i)
      if (ev[i].isFinal() && ev[i].isVisible() && !isQuirk(ev[i].id())) vis.append(ev[i]);
    slow.analyze(vis);
    string a = pythia.info.getEventAttribute("npNLO", true);
    int npnlo = a.empty() ? -1 : atoi(a.c_str());
    fprintf(out, "%.10e %.6f %.6f %.6f %.6f %d %d %d\n", w, pq.pT(), pq.eta(), pq.mCalc(), pqh.pT(), nme,
            slow.sizeJet(), npnlo);
    ++nOut; if (w < 0) ++nNeg; sw += w; sabs += fabs(w);
  }
  pythia.stat();
  fprintf(out, "# summary n_next %ld n_out %ld n_neg %ld n_zero %ld sum_w %.10e sum_absw %.10e sigmaGen_mb %.6e\n",
          nNext, nOut, nNeg, nZero, sw, sabs, pythia.info.sigmaGen());
  fclose(out);
  printf("fxfx_shower: %ld events written (%ld negative, %ld zero-weight skipped)\n", nOut, nNeg, nZero);
  return 0;
}
