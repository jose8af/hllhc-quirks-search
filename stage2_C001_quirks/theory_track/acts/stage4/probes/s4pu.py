"""s4pu.py -- Stage-4 PROBE helper (E9): Pythia8 CP5 14 TeV minimum-bias pool -> HepMC3 (Python conversion, as smoke_test.py).
Decays: Pythia decays K0S/Lambda/hyperons (tau0Max = 1000 mm; displaced vertices kept); pi+-, K+-, mu, K0L stable (Fatras
does no decays; their in-flight decays/kinks are not simulated -- plan §4)."""
import time
import pythia8
import pyhepmc

PY_LINES = ("Beams:eCM = 14000.", "SoftQCD:inelastic = on", "ParticleDecays:limitTau0 = on", "ParticleDecays:tau0Max = 1000.",
            "211:mayDecay = off", "321:mayDecay = off", "13:mayDecay = off", "130:mayDecay = off", "Print:quiet = on",
            "Random:setSeed = on", "Next:numberCount = 0")


def to_hepmc(ev, iev):
    ge = pyhepmc.GenEvent(pyhepmc.Units.GEV, pyhepmc.Units.MM)
    ge.event_number = iev
    parts = [None] * ev.size()
    for i in range(1, ev.size()):
        p = ev[i]
        gp = pyhepmc.GenParticle(pyhepmc.FourVector(p.px(), p.py(), p.pz(), p.e()), p.id(), 1 if p.isFinal() else (4 if i <= 2 else 2))
        gp.generated_mass = p.m(); parts[i] = gp; ge.add_particle(gp)
    endv = {}
    for i in range(3, ev.size()):
        p = ev[i]
        moms = tuple(sorted(set(m for m in p.motherList() if m > 0))) or (1, 2)
        v = endv.get(moms)
        if v is None:
            v = pyhepmc.GenVertex(pyhepmc.FourVector(p.xProd(), p.yProd(), p.zProd(), p.tProd()))
            for m in moms:
                if parts[m].end_vertex is None:
                    v.add_particle_in(parts[m])
            ge.add_vertex(v); endv[moms] = v
        v.add_particle_out(parts[i])
    return ge


def make_pool(path, n, seed, cp5):
    py = pythia8.Pythia("", False)
    py.readFile(str(cp5))
    for line in PY_LINES + (f"Random:seed = {seed}",):
        py.readString(line)
    assert py.init()
    t0 = time.time(); k = 0
    with pyhepmc.io.WriterAscii(str(path)) as w:
        while k < n:
            if not py.next():
                continue
            w.write(to_hepmc(py.event, k)); k += 1
    return time.time() - t0
