// g4hv.cc -- Geant4 vertex generator for the Geant4 -> Fatras hand-over (quirks v2, Phase 2 channel (iii), Tatiana,
// 2026-11-16; extends phase1_strategy/src/generators/g4sv/g4sv.cc of the feasibility phase).
//
// Geometry: text file written by make_geom_g4.py from the SAME source as the ACTS geometry (sim/stage3/code/
// surfaces_s3.json + the passive cylinders of acts/stage4/code/s4geo.py).  Lines:
//   B <field_T>
//   C <name> <r_mm> <zmin_mm> <zmax_mm> <x_over_X0> <material> <sensitive 0|1>     cylinder at radius r
//   D <name> <z_mm> <rmin_mm> <rmax_mm> <x_over_X0> <material> <sensitive 0|1>     disc at z
// The thickness of a slab is x/X0 times the radiation length of its Geant4 material, centred on the surface.  A
// sensitive slab is built as two halves "<name>#a" and "<name>#b", so that a step boundary lies exactly on the
// surface: a crossing of the primary is recorded there.  Slabs with x/X0 = 0 (BTL) are 2 x 5 um of vacuum.
//
// Modes:
//   prim <primaries.txt> : one Geant4 event per input line "id pdg x y z t px py pz" (mm, ns, GeV).  The primary is
//        tracked in the field; secondaries are recorded at their vertex and killed (Fatras propagates them).
//        Output text records, written only for primaries that end in a vertex (a process other than transportation
//        kills the primary) inside r < RMAX, |z| < ZMAX:
//          V <id> <process> <volume> <parent_pdg> <x> <y> <z> <t> <px> <py> <pz> <nprod> <ncross>
//          P <pdg> <px> <py> <pz> <E> <x> <y> <z> <t>              (nprod lines; GeV, mm, ns)
//        Product hand-over point: with the option 'exit', the products of a vertex inside a material slab are
//        tracked by Geant4 until they leave that slab and are recorded there (those that stop inside the slab are
//        not handed over; N_STOP counts them); without it, and for vertices in vacuum, at the vertex itself.
//          X <surface> <x> <y> <z> <t> <px> <py> <pz>              (ncross lines: the primary's crossings before the vertex)
//        and one summary line "G4HV ..." on stdout.
//   scan <n_per_eta> : geantinos from the origin at eta = -3.0 ... 3.0 in steps of 0.1 (uniform phi); output
//          S <eta> <volume> <path_mm> <x_over_X0> <x_over_lambdaI> <r_mid_mm> <z_mid_mm>
//        Option 'allx' (added 2026-11-16 by Xavier for the half-turn study; default behaviour unchanged): a record is
//        written for EVERY primary, also for one that ends without a vertex: its V line then carries the pseudo-process
//        "LeftWorld" (r > RMAX or |z| > ZMAX) or "TimeLimit" (t > 25 ns) and the point where it was dropped, with all its
//        crossings of sensitive surfaces as X lines.  Products are recorded at the vertex and killed, as without 'exit'.
// Usage: g4hv <geom.txt> <physlist> <seed> <out.txt> prim <primaries.txt> [rmax_mm] [exit|allx] | scan <n_per_eta> [overlap]
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
#include "G4Geantino.hh"
#include "G4ProcessTable.hh"
#include "Randomize.hh"
#include <cstdio>
#include <fstream>
#include <sstream>
#include <vector>
#include <map>
#include <string>
#include <cmath>
#include <ctime>

struct Slab { char type; std::string name; double a, b, c, xx0; std::string mat; int sens; };
struct Prim { long id; int pdg; double x, y, z, t, px, py, pz; };
static std::vector<Slab> gSlab;
static std::vector<Prim> gPrim;
static double gB = 3.8112;
static bool gScan = false;
static int gScanN = 5;
static FILE* gOut = nullptr;
static double RMAX = 1200.0;                                        // mm: the primary is dropped beyond (argument)
static const double ZMAX = 2700.0, TMAX = 25.0;                      // mm, ns
static std::map<std::string, long> gCount;                           // "process|volume" -> vertices
static long gNvtx = 0, gNcut = 0, gNprim = 0;
static bool gOverlap = false;
static bool gExit = false;
static bool gAllX = false;                                           // option 'allx' (Xavier, 2026-11-16): see usage
static long gNstop = 0, gNexit = 0;
struct Prod { int pdg; double px, py, pz, e, x, y, z, t; };
static std::vector<Prod> gProd;
static bool gHaveVtx = false;
static std::string gVtxVol, gVtxHead;

static std::string base(const G4String& n) {
  auto k = n.find('#');
  return k == std::string::npos ? std::string(n) : std::string(n.substr(0, k));
}

class Det : public G4VUserDetectorConstruction {
 public:
  G4VPhysicalVolume* Construct() override {
    auto nist = G4NistManager::Instance();
    auto vac = nist->FindOrBuildMaterial("G4_Galactic");
    auto wbox = new G4Box("World", 1.3 * m, 1.3 * m, 3.0 * m);
    auto wlv = new G4LogicalVolume(wbox, vac, "World");
    auto wpv = new G4PVPlacement(nullptr, {}, wlv, "World", nullptr, false, 0);
    for (auto& s : gSlab) {
      auto mat = s.xx0 > 0 ? nist->FindOrBuildMaterial(s.mat) : vac;
      double t = s.xx0 > 0 ? s.xx0 * mat->GetRadlen() : 0.010 * mm;
      int nh = s.sens ? 2 : 1;
      for (int h = 0; h < nh; ++h) {
        std::string nm = s.sens ? s.name + (h == 0 ? "#a" : "#b") : s.name;
        double lo = (nh == 2 ? (h == 0 ? -0.5 * t : 0.0) : -0.5 * t), hi = (nh == 2 ? (h == 0 ? 0.0 : 0.5 * t) : 0.5 * t);
        G4VSolid* sol; G4ThreeVector pos;
        if (s.type == 'C') {
          sol = new G4Tubs(nm, s.a * mm + lo, s.a * mm + hi, 0.5 * (s.c - s.b) * mm, 0, 360 * deg);
          pos = G4ThreeVector(0, 0, 0.5 * (s.b + s.c) * mm);
        } else {
          sol = new G4Tubs(nm, s.b * mm, s.c * mm, 0.5 * (hi - lo), 0, 360 * deg);
          pos = G4ThreeVector(0, 0, s.a * mm + 0.5 * (lo + hi));
        }
        auto lv = new G4LogicalVolume(sol, mat, nm);
        new G4PVPlacement(nullptr, pos, lv, nm, wlv, false, 0, gOverlap);
      }
    }
    return wpv;
  }
  void ConstructSDandField() override {
    auto field = new G4UniformMagField(G4ThreeVector(0, 0, gB * tesla));
    auto fm = G4TransportationManager::GetTransportationManager()->GetFieldManager();
    fm->SetDetectorField(field);
    fm->CreateChordFinder(field);
  }
};

static double gEta = 0;
class Gun : public G4VUserPrimaryGeneratorAction {
  G4ParticleGun gun{1};
 public:
  void GeneratePrimaries(G4Event* ev) override {
    if (gScan) {
      gEta = -3.0 + 0.1 * (ev->GetEventID() / gScanN);
      double phi = 2 * M_PI * G4UniformRand();
      gun.SetParticleDefinition(G4Geantino::Definition());
      gun.SetParticleMomentumDirection(G4ThreeVector(std::cos(phi), std::sin(phi), std::sinh(gEta)).unit());
      gun.SetParticleEnergy(1 * GeV);
      gun.SetParticlePosition({0, 0, 0});
      gun.GeneratePrimaryVertex(ev);
      return;
    }
    const Prim& p = gPrim[ev->GetEventID()];
    auto def = G4ParticleTable::GetParticleTable()->FindParticle(p.pdg);
    if (!def) { G4cerr << "unknown pdg " << p.pdg << G4endl; def = G4Geantino::Definition(); }
    gun.SetParticleDefinition(def);
    G4ThreeVector mom(p.px * GeV, p.py * GeV, p.pz * GeV);
    double mass = def->GetPDGMass();
    gun.SetParticleMomentumDirection(mom.unit());
    gun.SetParticleEnergy(std::sqrt(mom.mag2() + mass * mass) - mass);
    gun.SetParticlePosition({p.x * mm, p.y * mm, p.z * mm});
    gun.SetParticleTime(p.t * ns);
    gun.GeneratePrimaryVertex(ev);
  }
};

struct Cross { std::string surf; double x, y, z, t, px, py, pz; };
static std::vector<Cross> gCross;
struct ScanAcc { double path = 0, xx0 = 0, xl = 0, r = 0, z = 0; };
static std::map<std::string, ScanAcc> gAcc;

class EvAct : public G4UserEventAction {
 public:
  void BeginOfEventAction(const G4Event*) override { gCross.clear(); gAcc.clear(); gProd.clear(); gHaveVtx = false; }
  void EndOfEventAction(const G4Event*) override {
    if (!gScan) {
      if (!gHaveVtx) return;
      std::fprintf(gOut, "%s %zu %zu\n", gVtxHead.c_str(), gProd.size(), gCross.size());
      for (auto& q : gProd)
        std::fprintf(gOut, "P %d %.9g %.9g %.9g %.9g %.6f %.6f %.6f %.6f\n", q.pdg, q.px, q.py, q.pz, q.e, q.x, q.y, q.z, q.t);
      for (auto& c : gCross)
        std::fprintf(gOut, "X %s %.6f %.6f %.6f %.6f %.9g %.9g %.9g\n", c.surf.c_str(), c.x, c.y, c.z, c.t, c.px, c.py,
                     c.pz);
      return;
    }
    for (auto& kv : gAcc)
      std::fprintf(gOut, "S %.2f %s %.6f %.8f %.8f %.3f %.3f\n", gEta, kv.first.c_str(), kv.second.path, kv.second.xx0,
                   kv.second.xl, kv.second.r, kv.second.z);
  }
};

class Step : public G4UserSteppingAction {
 public:
  void UserSteppingAction(const G4Step* s) override {
    auto tr = s->GetTrack();
    auto pre = s->GetPreStepPoint(); auto post = s->GetPostStepPoint();
    if (gScan) {
      auto pv = pre->GetPhysicalVolume();
      if (pv && pv->GetName() != "World") {
        auto mat = pre->GetMaterial();
        auto& a = gAcc[base(pv->GetName())];
        double L = s->GetStepLength();
        auto mid = 0.5 * (pre->GetPosition() + post->GetPosition());
        a.path += L / mm; a.xx0 += L / mat->GetRadlen(); a.xl += L / mat->GetNuclearInterLength();
        a.r = mid.perp() / mm; a.z = mid.z() / mm;
      }
      return;
    }
    if (tr->GetParentID() != 0) {
      // product of the vertex, tracked inside the vertex slab (option 'exit'): handed over where it leaves the slab
      auto pv2 = post->GetPhysicalVolume();
      std::string vnow = pv2 ? base(pv2->GetName()) : "none";
      if (!gHaveVtx || vnow != gVtxVol) {
        if (gHaveVtx) {
          auto x = post->GetPosition(); auto p = post->GetMomentum();
          gProd.push_back({tr->GetDefinition()->GetPDGEncoding(), p.x() / GeV, p.y() / GeV, p.z() / GeV,
                           post->GetTotalEnergy() / GeV, x.x() / mm, x.y() / mm, x.z() / mm, post->GetGlobalTime() / ns});
          ++gNexit;
        }
        tr->SetTrackStatus(fStopAndKill);
      } else if (tr->GetTrackStatus() == fStopAndKill || tr->GetTrackStatus() == fStopButAlive
                 || post->GetGlobalTime() > TMAX * ns) {
        if (tr->GetTrackStatus() != fStopAndKill) tr->SetTrackStatus(fStopAndKill);
        ++gNstop;
      }
      return;
    }
    // crossing of a sensitive surface: boundary between the two halves of one slab
    if (post->GetStepStatus() == fGeomBoundary) {
      auto v1 = pre->GetPhysicalVolume(); auto v2 = post->GetPhysicalVolume();
      if (v1 && v2 && v1 != v2) {
        const G4String& n1 = v1->GetName(); const G4String& n2 = v2->GetName();
        if (n1.find('#') != std::string::npos && n2.find('#') != std::string::npos && base(n1) == base(n2)) {
          auto x = post->GetPosition(); auto p = post->GetMomentum();
          gCross.push_back({base(n1), x.x() / mm, x.y() / mm, x.z() / mm, post->GetGlobalTime() / ns, p.x() / GeV,
                            p.y() / GeV, p.z() / GeV});
        }
      }
    }
    auto proc = post->GetProcessDefinedStep();
    auto st = tr->GetTrackStatus();
    if (proc && st == fStopAndKill && proc->GetProcessName() != "Transportation") {
      auto x = post->GetPosition();
      auto sec = s->GetSecondaryInCurrentStep();
      auto pv = pre->GetPhysicalVolume();
      std::string vol = pv ? base(pv->GetName()) : "none";
      // parent momentum at the vertex: direction after transport (post-step), magnitude from the pre-step kinetic
      // energy minus the energy lost along the step (the interaction itself sets the post-step energy to zero)
      double mass = tr->GetDefinition()->GetPDGMass();
      double ek = pre->GetKineticEnergy() - s->GetTotalEnergyDeposit();
      if (ek < 0) ek = 0;
      double pm = std::sqrt(ek * (ek + 2 * mass));
      auto d = post->GetMomentumDirection();
      if (proc->GetProcessName() == "Decay" && post->GetMomentum().mag() > 0) { pm = post->GetMomentum().mag(); }
      if (x.perp() < RMAX * mm && std::fabs(x.z()) < ZMAX * mm) {
        long id = gPrim[G4RunManager::GetRunManager()->GetCurrentEvent()->GetEventID()].id;
        char buf[512];
        std::snprintf(buf, sizeof buf, "V %ld %s %s %d %.6f %.6f %.6f %.6f %.9g %.9g %.9g", id,
                      proc->GetProcessName().c_str(), vol.c_str(), tr->GetDefinition()->GetPDGEncoding(), x.x() / mm,
                      x.y() / mm, x.z() / mm, post->GetGlobalTime() / ns, pm * d.x() / GeV, pm * d.y() / GeV,
                      pm * d.z() / GeV);
        gVtxHead = buf; gVtxVol = vol; gHaveVtx = true;
        if (!(gExit && vol != "World")) {          // hand-over at the vertex: record now, the stack kills them
          for (auto q : *sec) {
            auto p = q->GetMomentum();
            gProd.push_back({q->GetDefinition()->GetPDGEncoding(), p.x() / GeV, p.y() / GeV, p.z() / GeV,
                             q->GetTotalEnergy() / GeV, x.x() / mm, x.y() / mm, x.z() / mm, post->GetGlobalTime() / ns});
          }
        }
        ++gNvtx; ++gCount[proc->GetProcessName() + "|" + vol];
      }
      return;
    }
    auto x = post->GetPosition();
    if (x.perp() > RMAX * mm || std::fabs(x.z()) > ZMAX * mm || post->GetGlobalTime() > TMAX * ns) {
      tr->SetTrackStatus(fStopAndKill); ++gNcut;
      if (gAllX && !gHaveVtx) {
        long id = gPrim[G4RunManager::GetRunManager()->GetCurrentEvent()->GetEventID()].id;
        auto p = post->GetMomentum();
        char buf[512];
        std::snprintf(buf, sizeof buf, "V %ld %s %s %d %.6f %.6f %.6f %.6f %.9g %.9g %.9g", id,
                      post->GetGlobalTime() > TMAX * ns ? "TimeLimit" : "LeftWorld", "none",
                      tr->GetDefinition()->GetPDGEncoding(), x.x() / mm, x.y() / mm, x.z() / mm, post->GetGlobalTime() / ns,
                      p.x() / GeV, p.y() / GeV, p.z() / GeV);
        gVtxHead = buf; gVtxVol = "none"; gHaveVtx = true;
      }
    }
  }
};

class Stack : public G4UserStackingAction {
 public:
  G4ClassificationOfNewTrack ClassifyNewTrack(const G4Track* t) override {
    if (t->GetParentID() == 0) return fUrgent;
    return (gExit && gHaveVtx && gVtxVol != "World") ? fUrgent : fKill;      // products tracked only inside a slab
  }
};

class Act : public G4VUserActionInitialization {
 public:
  void Build() const override {
    SetUserAction(new Gun);
    SetUserAction(new EvAct);
    SetUserAction(new Step);
    SetUserAction(new Stack);
  }
};

int main(int argc, char** argv) {
  if (argc < 7) { G4cerr << "usage: g4hv geom.txt physlist seed out.txt prim primaries.txt | scan n_per_eta [overlap]\n"; return 2; }
  std::ifstream g(argv[1]);
  std::string line;
  while (std::getline(g, line)) {
    if (line.empty() || line[0] == '#') continue;
    std::istringstream is(line); char ty; is >> ty;
    if (ty == 'B') { is >> gB; continue; }
    Slab s; s.type = ty; is >> s.name >> s.a >> s.b >> s.c >> s.xx0 >> s.mat >> s.sens; gSlab.push_back(s);
  }
  std::string plist = argv[2]; long seed = std::atol(argv[3]);
  gOut = std::fopen(argv[4], "w");
  if (!gOut) { G4cerr << "cannot open " << argv[4] << G4endl; return 2; }
  std::string mode = argv[5];
  int nev = 0;
  if (mode == "scan") { gScan = true; gScanN = std::atoi(argv[6]); nev = 61 * gScanN; gOverlap = argc > 7; }
  else {
    std::ifstream pf(argv[6]);
    while (std::getline(pf, line)) {
      if (line.empty() || line[0] == '#') continue;
      std::istringstream is(line); Prim p; is >> p.id >> p.pdg >> p.x >> p.y >> p.z >> p.t >> p.px >> p.py >> p.pz;
      gPrim.push_back(p);
    }
    nev = (int)gPrim.size(); gNprim = nev;
    if (argc > 7) RMAX = std::atof(argv[7]);
    gExit = argc > 8 && std::string(argv[8]) == "exit";
    gAllX = argc > 8 && std::string(argv[8]) == "allx";
  }
  G4Random::setTheSeed(seed);
  auto rm = G4RunManagerFactory::CreateRunManager(G4RunManagerType::Serial);
  rm->SetUserInitialization(new Det);
  G4PhysListFactory f;
  auto pl = f.GetReferencePhysList(plist);
  if (!pl) { G4cerr << "unknown physics list " << plist << G4endl; return 2; }
  rm->SetUserInitialization(pl);
  rm->SetUserInitialization(new Act);
  auto ui = G4UImanager::GetUIpointer();
  ui->ApplyCommand("/control/verbose 0"); ui->ApplyCommand("/run/verbose 0"); ui->ApplyCommand("/tracking/verbose 0");
  ui->ApplyCommand("/process/verbose 0"); ui->ApplyCommand("/process/had/verbose 0"); ui->ApplyCommand("/process/em/verbose 0");
  std::clock_t c0 = std::clock();
  rm->Initialize();
  std::clock_t c1 = std::clock();
  rm->BeamOn(nev);
  std::clock_t c2 = std::clock();
  std::fclose(gOut);
  G4cout << "G4HV mode=" << mode << " physlist=" << plist << " field_T=" << gB << " nev=" << nev << " init_cpu_s="
         << double(c1 - c0) / CLOCKS_PER_SEC << " event_cpu_s=" << double(c2 - c1) / CLOCKS_PER_SEC << " cpu_ms_per_event="
         << 1e3 * double(c2 - c1) / CLOCKS_PER_SEC / std::max(nev, 1) << " nvtx=" << gNvtx << " ndropped=" << gNcut << " handover=" << (gExit ? "exit" : "vertex")
         << " nprod_exit=" << gNexit << " nprod_stopped_in_slab=" << gNstop;
  for (auto& kv : gCount) G4cout << " " << kv.first << "=" << kv.second;
  G4cout << G4endl;
  delete rm;
  return 0;
}
