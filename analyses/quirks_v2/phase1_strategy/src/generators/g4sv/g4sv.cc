// g4sv.cc -- Geant4 feasibility app (quirks v2 Phase 1, executor Basil, 2026-11-13).
// Pion gun through barrel tracker cylinders in a uniform 3.8 T solenoid field; records the secondary vertices made by
// hadronic inelastic interactions and decays (in flight) of the primary, with their products, to a CSV.
//
// Geometry: read from a text file (one line per cylinder: name r_mm half_z_mm x_over_X0); each cylinder is a silicon
// tube whose thickness = x/X0 * X0(Si) (material-equivalent slab, as the v1 T3/ACTS slab model).  Generated from the v1
// geometry by make_geom.py, so the same numbers feed ACTS.
//
// Usage: g4sv <geom.txt> <nevents> <seed> <mode: full|primary> <out.csv> [pdg=211] [ptmin=1] [ptmax=10] [etamax=1]
//   mode full    : every secondary is tracked by Geant4 (cost upper bound)
//   mode primary : secondaries are recorded at their vertex and then killed (hand-over mode: Fatras propagates them)
#include "G4RunManagerFactory.hh"
#include "G4PhysListFactory.hh"
#include "G4VModularPhysicsList.hh"
#include "G4VUserDetectorConstruction.hh"
#include "G4VUserPrimaryGeneratorAction.hh"
#include "G4VUserActionInitialization.hh"
#include "G4UserSteppingAction.hh"
#include "G4UserStackingAction.hh"
#include "G4UserEventAction.hh"
#include "G4ParticleGun.hh"
#include "G4ParticleTable.hh"
#include "G4NistManager.hh"
#include "G4Box.hh"
#include "G4Tubs.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4UniformMagField.hh"
#include "G4FieldManager.hh"
#include "G4TransportationManager.hh"
#include "G4ChordFinder.hh"
#include "G4SystemOfUnits.hh"
#include "G4Step.hh"
#include "G4Track.hh"
#include "G4VProcess.hh"
#include "G4Event.hh"
#include "G4UImanager.hh"
#include "Randomize.hh"
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <cmath>
#include <ctime>

struct Cyl { std::string name; double r, hz, xx0; };
static std::vector<Cyl> gCyl;
static std::ofstream gOut;
static bool gPrimaryOnly = false;
static long gNvtx = 0, gNdecay = 0, gNinel = 0;

class Det : public G4VUserDetectorConstruction {
 public:
  G4VPhysicalVolume* Construct() override {
    auto nist = G4NistManager::Instance();
    auto vac = nist->FindOrBuildMaterial("G4_Galactic");
    auto si = nist->FindOrBuildMaterial("G4_Si");
    const double X0 = si->GetRadlen();
    auto wbox = new G4Box("World", 1.3 * m, 1.3 * m, 3.0 * m);
    auto wlv = new G4LogicalVolume(wbox, vac, "World");
    auto wpv = new G4PVPlacement(nullptr, {}, wlv, "World", nullptr, false, 0);
    for (auto& c : gCyl) {
      double t = c.xx0 * X0;
      auto tub = new G4Tubs(c.name, c.r * mm - 0.5 * t, c.r * mm + 0.5 * t, c.hz * mm, 0, 360 * deg);
      auto lv = new G4LogicalVolume(tub, si, c.name);
      new G4PVPlacement(nullptr, {}, lv, c.name, wlv, false, 0);
    }
    return wpv;
  }
  void ConstructSDandField() override {
    auto field = new G4UniformMagField(G4ThreeVector(0, 0, 3.8 * tesla));
    auto fm = G4TransportationManager::GetTransportationManager()->GetFieldManager();
    fm->SetDetectorField(field);
    fm->CreateChordFinder(field);
  }
};

static double gPtMin = 1, gPtMax = 10, gEtaMax = 1;
static int gPdg = 211;
class Gun : public G4VUserPrimaryGeneratorAction {
  G4ParticleGun gun{1};
 public:
  void GeneratePrimaries(G4Event* ev) override {
    double lpt = std::log(gPtMin) + G4UniformRand() * (std::log(gPtMax) - std::log(gPtMin));
    double pt = std::exp(lpt) * GeV;
    double eta = (2 * G4UniformRand() - 1) * gEtaMax, phi = 2 * M_PI * G4UniformRand();
    int sgn = G4UniformRand() < 0.5 ? 1 : -1;
    gun.SetParticleDefinition(G4ParticleTable::GetParticleTable()->FindParticle(sgn * gPdg));
    gun.SetParticleMomentum(G4ThreeVector(pt * std::cos(phi), pt * std::sin(phi), pt * std::sinh(eta)));
    gun.SetParticlePosition({0, 0, 0});
    gun.GeneratePrimaryVertex(ev);
  }
};

// Record vertices where the PRIMARY ends by an inelastic interaction or a decay (and, for completeness, any step of the
// primary that creates >=2 hadronic secondaries).  CSV: event,vtx,process,parent_pdg,x,y,z[mm],t[ns],ndau, then
// one line per product: event,vtx,"dau",pdg,px,py,pz[GeV],E[GeV]
class Step : public G4UserSteppingAction {
 public:
  void UserSteppingAction(const G4Step* s) override {
    auto tr = s->GetTrack();
    if (tr->GetParentID() != 0) return;
    auto pp = s->GetPostStepPoint();
    auto proc = pp->GetProcessDefinedStep();
    if (!proc) return;
    const G4String& pn = proc->GetProcessName();
    bool dec = (pn == "Decay");
    bool inel = (pn.find("Inelastic") != std::string::npos);
    if (!dec && !inel) return;
    auto sec = s->GetSecondaryInCurrentStep();
    int ev = G4RunManager::GetRunManager()->GetCurrentEvent()->GetEventID();
    auto x = pp->GetPosition();
    gOut << ev << ',' << gNvtx << ',' << pn << ',' << tr->GetDefinition()->GetPDGEncoding() << ',' << x.x() / mm << ','
         << x.y() / mm << ',' << x.z() / mm << ',' << pp->GetGlobalTime() / ns << ',' << sec->size() << '\n';
    for (auto d : *sec) {
      auto p = d->GetMomentum();
      gOut << ev << ',' << gNvtx << ",dau," << d->GetDefinition()->GetPDGEncoding() << ',' << p.x() / GeV << ','
           << p.y() / GeV << ',' << p.z() / GeV << ',' << d->GetTotalEnergy() / GeV << '\n';
    }
    ++gNvtx; dec ? ++gNdecay : ++gNinel;
  }
};

class Stack : public G4UserStackingAction {
 public:
  G4ClassificationOfNewTrack ClassifyNewTrack(const G4Track* t) override {
    return (gPrimaryOnly && t->GetParentID() > 0) ? fKill : fUrgent;
  }
};

class Act : public G4VUserActionInitialization {
 public:
  void Build() const override {
    SetUserAction(new Gun);
    SetUserAction(new Step);
    SetUserAction(new Stack);
  }
};

int main(int argc, char** argv) {
  if (argc < 6) { G4cerr << "usage: g4sv geom.txt nev seed full|primary out.csv [pdg ptmin ptmax etamax]\n"; return 2; }
  std::ifstream g(argv[1]);
  std::string line;
  while (std::getline(g, line)) {
    if (line.empty() || line[0] == '#') continue;
    std::istringstream is(line); Cyl c; is >> c.name >> c.r >> c.hz >> c.xx0; gCyl.push_back(c);
  }
  int nev = std::atoi(argv[2]); long seed = std::atol(argv[3]);
  gPrimaryOnly = std::string(argv[4]) == "primary";
  gOut.open(argv[5]);
  if (argc > 6) gPdg = std::atoi(argv[6]);
  if (argc > 7) gPtMin = std::atof(argv[7]);
  if (argc > 8) gPtMax = std::atof(argv[8]);
  if (argc > 9) gEtaMax = std::atof(argv[9]);
  G4Random::setTheSeed(seed);
  auto rm = G4RunManagerFactory::CreateRunManager(G4RunManagerType::Serial);
  rm->SetUserInitialization(new Det);
  G4PhysListFactory f;
  rm->SetUserInitialization(f.GetReferencePhysList("FTFP_BERT"));
  rm->SetUserInitialization(new Act);
  G4UImanager::GetUIpointer()->ApplyCommand("/control/verbose 0");
  G4UImanager::GetUIpointer()->ApplyCommand("/run/verbose 0");
  G4UImanager::GetUIpointer()->ApplyCommand("/tracking/verbose 0");
  std::clock_t c0 = std::clock();
  rm->Initialize();
  std::clock_t c1 = std::clock();
  rm->BeamOn(nev);
  std::clock_t c2 = std::clock();
  G4cout << "G4SV nev=" << nev << " mode=" << argv[4] << " init_cpu_s=" << double(c1 - c0) / CLOCKS_PER_SEC
         << " event_cpu_s=" << double(c2 - c1) / CLOCKS_PER_SEC << " cpu_ms_per_event="
         << 1e3 * double(c2 - c1) / CLOCKS_PER_SEC / nev << " nvtx=" << gNvtx << " ninel=" << gNinel
         << " ndecay=" << gNdecay << G4endl;
  gOut.close();
  delete rm;
  return 0;
}
