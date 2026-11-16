"""p2z_addendum1.py -- every table and number of strategy addendum 1, VERSION 4 (new measurements integrated).  ESTIMATE.

  nice -n 19 /usr/bin/python3 -I p2z_addendum1.py > addendum1_v4_stdout.txt

Copy of p2y_addendum1.py (version 3, session Yvonne; not edited) with the changes of version 4 as the named
OVERRIDES_V4 below and the new sections [14]-[18].  Sections [1]-[7], [9], [10], [12] are those of version 3 and print
the same numbers (regression); [2], [8], [11], [13] change where a measured input changed (marked "v4").
What is different from version 3:
  [a]  A-1 settled: campaigns p2-c-px-tr / -val2 (radius, time, both) and p2-c-px-hy / -val3 (option (a)) read from
       their validation JSON -> section [14]
  [b]  the half-turn limit: campaigns p2-c-px-htg, -a1e read from their JSON -> section [15]
  [c]  the looper gun: p2-c-px-lps (first run, provisional) or p2-c-px-lpds (rerun) if it exists -> section [16]
  [d]  the proposed eighth B6 row (pile-up with the later arcs restored): size, cost, readings -> section [17]
  [e]  pilot part 1 as launched (measured CPU and bytes per job), B1 part with the production-code unit costs,
       calendar from the launch time; toy projection with the jax configuration -> sections [8], [11]
The text below is the docstring of version 3, kept.

Copy of p2c_addendum1.py (version 2, session Tatiana; not edited) with the changes of version 3 as the named
OVERRIDES_V3 below.  The Phase-1 budget script is used through p2c_rule1 (byte-identical copy, executed unchanged, its
printing discarded).  The Geant4 vertex partition is read from outputs/partition_p2-c-part-0.json and the hand-over
validation from data/p2c/p2-c-b1yv/000/p2-c-b1yv-val.json.  Pure Python, no numpy; prints text (the stdout is the record).

What is different from version 2 (each is a named entry of OVERRIDES_V3 or a new section):
  [A-2]  the hard-scatter parent sample is in the script and in every rule-1 row (three options H1, H2, H3)
  [B-1]  21 road orientations: exposure check 21 x 0.30 / 2 pi
  [B-2]  the low-pT check sample: N_t, events per count, size needed
  [B-3]  families K and T_c for 7 / 4 / 3 / 1 B1 terms; Q2 (c) table and the (alpha1), (gamma) rows on the new basis
  [B-5]  B1 pool floor with Geant4 charged once per pass
  [C-3]  ties pause (crossing = first count with B50 >= 300 x (1 - TIE)); frozen row printed by this script
  [C-7]  3 % more firings in the 'all' pass; [C-9] jobs of at most 2e6 firings; [C-10] low-weight-class pool floors;
  [C-11] readings with fewer terms; [C-12] toy projection at 80 and 100 parameters and with the jax readings
The sampler: B = sum_t kappa_t Gamma(m_t + 1) + min(med exp(s g), cap Exp(1)), the generator of d15_q
(strategy_budget.py l.878-888).  Here Gamma(m + 1) for integer m is drawn as a sum of m + 1 unit exponentials with common
random numbers across rows (same law; checked below against d15_q on the frozen case).
"""
import json
import math
import random
import sys
from array import array
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import p2c_rule1 as R  # noqa: E402

NS = R.NS
NTRIG, SM, MJ, NZ = R.NTRIG, R.SM, R.MJ, R.NZ
U68, H, alloc = NS['U68'], NS['H'], NS['allocate']
QV2 = HERE.parent.parent
PART = json.loads((HERE.parent / 'outputs' / 'partition_p2-c-part-0.json').read_text())
VAL = json.loads((QV2 / 'data' / 'p2c' / 'p2-c-b1yv' / '000' / 'p2-c-b1yv-val.json').read_text())

# ---- overrides of version 2 (unchanged; sources in p2c_addendum1.py l.25-35) --------------------------------------------
OVERRIDES = dict(
    PILOT_HS_GENERATED=2.3e6,
    M_FULL={'Z': 0.4396, 'W': 0.2657, 'tt': 0.1205}, LOW_CLASS={'Z': (0.0025, 0.05), 'W': (0.0516, 0.05), 'tt': (0.0946, 0.05)},
    F_PASS={'Z': 0.442, 'W': 0.315, 'tt': 0.2105},
    F_HS=1.5945 / 1.560,
    R08_PILEUP=(87.9, 117.9, 148.0),
    COST=dict(Z=(0.042, 0.085), W=(0.086, 0.085), tt=(0.460, 0.111), tt_forced=(0.216, 0.111)),
    CHAIN_B1=dict(DIF=0.0037, DIFC=0.0037, NI22=0.0038, NI30=0.0059, NI61=0.0059, NIX=0.0059, NIC=0.0059),
    G4_ALL_MS=PART['g4_ms_per_firing'], G4_NI_MS=0.0469,
)
# ---- overrides of version 3 (each with its finding and its source) -------------------------------------------------------
OVERRIDES_V3 = dict(
    TIE=0.003,                       # C-3: STR l.2757, a reading within the precision of 300 (0.3 %) counts as larger
    ND=100000, ND_CROSS=100000, ND_GRID=20000,  # binding median >= 1e5 draws (STR l.2757); the (c) grid at 2e4 draws as in the strategy
    # A-2: hard-scatter parents.  [V, validation slice p2-c-px-hsg-r0, 2,000 generated Z(nunu) events, session Xavier;
    #       read by /var/tmp/jdochoa/yvonne/slices.py]: pool-phase-space parents per triggered (weighted) event
    HS_IN_ROAD_PER_TRIG=0.8718, HS_ANY_PHI_PER_TRIG=35.50, HS_SLICE_PARENTS_W=723, HS_SLICE_EVENTS=2000, HS_SLICE_EVENTS_W=834,
    HS_SIZES={'H1': 2.0e6, 'H2': 2.0e5},
    HS_OFFROAD_SIZE=7.3e6,           # option: second stratum (hard-scatter hadrons outside the road), sized for about 25 events per count
    # B-2: parents outside the pool phase space.  [V, validation slice p2-c-px-mbb-big, 125,000 interactions, session Xavier; meta of the
    #      file, re-counted from its xpool arrays by /var/tmp/jdochoa/yvonne/slices2.py]: per interaction
    LOWPT_PER_INT=5.201752,          # 0.3 < pT <= 0.5 GeV, |eta| < 1
    FWD_PER_INT=3.643512,            # pT > 0.5 GeV, 1 <= |eta| < 1.5
    POOL_PER_INT_SLICE=7.09628, V1_DIF_RATE_PX_MBB=0.007967949,   # the pool and v1's DIF formula on the same slice
    LOWPT_YIELD_FACTOR=(1.0, 2.0),   # B1 vertices per firing relative to the pool's: NOT MEASURED [E planning range; review B-2 "more vertices each"]
    LOWPT_SIZE=2.0e5, LOWPT_CHAIN_S=0.0048,   # chain cost per low-pT event: mean of the B1 classes [E]
    ALL_PASS_MARGIN=1.03,            # C-7
    G4_JOB_FIRINGS=2.0e6,            # C-9 (partition job: 2,161 MB for 1.5e6 firings; guard 3,750 MB)
    V1_DIF_RATE_T_G4=0.007802,       # C-6: v1 formula on the 40,000 interactions of p2-c-t-g4 [U: typed from review Wanda section b]
    KB_PER_B1_EVENT=4.3, KB_PER_Z_EVENT=30.2, KB_Z_EXTRA=1.0,   # C-8: extra summary columns and hadron list, about 1 kB per event [E]
    HS_CHAIN_S=0.0050, HSPOOL_GEN_S=0.0383,   # hs sample: chain cost as the NI classes [E]; generator-level pool 76.4 CPU-s per 2,000 events [V: p2-c-px-hsg]
    TOY_S={'31 numpy': 638.0, '60 numpy': 11052.0, '80 numpy': 17799.0, '100 numpy': 48589.0,       # [V: p2-c-t-pyhf]
           '31 jax': 84.0, '60 jax': 432.0, '80 jax': 857.0, '100 jax': 1898.0},                     # [U: executor Viktor log 14:11, p2-c-toy-jax; correctness run not reviewed]
    NEW_4A_CPU_H=41.0,               # three new closure designs: 3 x 7 + 10 + 10 (version 2, section 4)
)
# ---- overrides of version 4 (each with its fact and its source) ----------------------------------------------------------
PXV = QV2 / 'data' / 'p2c' / 'px_validation'
OVERRIDES_V4 = dict(
    # [e] pilot part 1 as launched 2026-11-16 16:39 on 2 lanes of schrodinger (LOG.md 16:40).  [V: done markers read by Zoe:
    #     ledger/markers/p2-c-pilot-znn-00/000/p2-c-pilot-znn-0000{0,1,2}.marker, ledger/markers/p2-c-pilot-mb/000/*.marker]
    PILOT_ZNN_JOB_CPU_S=(677.731, 662.727, 665.947), PILOT_ZNN_JOB_BYTES=(169313573, 169187713, 169065349), PILOT_ZNN_JOB_EVENTS=5000,
    PILOT_MB_JOB_CPU_S=(879.824, 889.121), PILOT_MB_JOBS=40, PILOT_MB_GB=2.2,     # 40 jobs of 2.5e5 interactions; 2.2 GB [E: PILOT_READY section 4]
    PILOT_LAUNCH='2026-11-16 16:39', PILOT_LANES=2, DAY5='2026-11-21 00:00',
    # [e] B1 part: unit costs of the production code [V: p2-c-px-g4, PILOT_READY section 7: 'all' pass 675.6 CPU-s per 2e6 firings all-in,
    #     'ni' pass 538 CPU-s per 1e7 firings, 226 MB of vertex files per 2e6-firing 'all' job]; used for the PILOT cost only
    G4_ALL_MS_PILOT=675.6 / 2.0e6 * 1e3, G4_NI_MS_PILOT=538.0 / 1.0e7 * 1e3, G4_ALL_JOB_GB=0.226, G4_NI_GB=2.0,   # 'ni' vertex files: [E]
    # [a] chain cost of the two after-a-turn streams with option (a) [V: stage sums of p2-c-px-hy-difc-r0 / -nic-r0 in p2-c-px-val3-0.json]
    CHAIN_B1_HYBRID=dict(DIFC=0.00483, NIC=0.00622),
    # [e] bytes per event of the B1 slice files [V: p2-c-px-val2-0.json (radius) and p2-c-px-val3-0.json (hybrid, autoh)]
    B_PER_EVENT=dict(DIF=2587, DIFC=4452, NI22=3298, NI30=3557, NI61=3420, NIX=3493, NIC=5377, HS=3704, LOWPT=3522),
    # [e] toys [V units: TOY_COST_viktor_2026-11-16_16-33.md section 4 row e3, section 6; campaigns p2-c-toy-{jax,base,ref,tune,fix}; synthetic workspace]
    TOY_UNITS=1006.4, TOY_ALL_EXACT_UNITS=1303.0, TOY_FACTOR=1.6,
    TOY_S_JAX={31: 30.5, 60: 168.0, 80: 385.0, 100: 817.0},
    TOY_S_NUMPY_SCHRODINGER={31: 487.0, 60: 8814.0, 100: 67780.0},
    TOY_S_NUMPY_LANDAU={31: 638.0, 60: 11052.0, 80: 17799.0, 100: 48589.0},     # the "old backend" case of version 3 [V: p2-c-t-pyhf]
    # [d] unit costs for the proposed robustness test
    G4_MS_PER_FIRING_PIK=0.41,       # [V: p2-c-t-g4, EXPLORATION_iii_tatiana_2026-11-16_14-18.md l.38: pi/K through the tracker]
    PU_CHAIN_S=12.3, PU_FINDER_S=11.3, PU_TRIALS=4,      # [V: p2-a-day0-pu1, EXPLORATION_i_rosalie_2026-11-16_14-43.md section 1]
    PU_EVENT_S_MEASURED=58.0,        # rho = 1 event, chain + 4 trials: 57-59 CPU-s [V: p2-a-c1-pu1, same table]
    ROB_HITS=(1.0, 1.3), ROB_EVENTS=(600, 1000),          # hits relative to nominal: 1.0 = total density kept (top-up reduced), 1.3 = arcs on top [E]
    PU_RATE_PER_TRIAL=dict(R04=171.55, R05=49.7, R06=1482.0 / 6000.0, R07=7.29e-4),   # v1 direct rates [U: STR l.249, l.747, l.1185, l.1181]
    ROB_SLICE_CPU_H=2.0,             # slice and validation of the injection in a pile-up event [E, judgement]
    SIG_ROW_S=25.2,                  # signal row through the full chain [U: STR l.1511]
)
O = dict(OVERRIDES, **OVERRIDES_V3, **OVERRIDES_V4)
Z_MS = 1e3 * sum(O['PILOT_ZNN_JOB_CPU_S']) / (len(O['PILOT_ZNN_JOB_CPU_S']) * O['PILOT_ZNN_JOB_EVENTS'])     # ms per generated Z(nunu) event, all-in
Z_KB = 1e-3 * sum(O['PILOT_ZNN_JOB_BYTES']) / (len(O['PILOT_ZNN_JOB_BYTES']) * O['PILOT_ZNN_JOB_EVENTS'])    # kB per event
MB_CPU_H = O['PILOT_MB_JOBS'] * sum(O['PILOT_MB_JOB_CPU_S']) / len(O['PILOT_MB_JOB_CPU_S']) / 3600.0


def jload(*parts):
    p = PXV.joinpath(*parts)
    return json.loads(p.read_text()) if p.exists() else None


NF = PART['n_fire']
CNT = {k: v['all'] for k, v in PART['counts'].items()}
CLASSES = dict(DIF=CNT['dif'] + CNT['k0l'], DIFC=CNT['difc'], NI22=CNT['ni22'], NI30=CNT['ni30'], NI61=CNT['ni61'],
               NIX=CNT['nix'], NIC=CNT['nic'])
ROAD = PART['pool_in_road_per_interaction']
RATE = {k: 200.0 * ROAD * c / NF * O['F_HS'] for k, c in CLASSES.items()}   # per triggered event, hard-scatter share included (x F_HS)
NT = {k: NTRIG * r for k, r in RATE.items()}
NT_MB = {k: v / O['F_HS'] for k, v in NT.items()}                           # minimum-bias share alone
NT_HS = sum(NT.values()) - sum(NT_MB.values())                              # hard-scatter share of all seven classes at F_HS (upper-side planning value)
S1 = dict(DIF=1e6, DIFC=1e6, NI22=1e6, NI30=1e6, NI61=1e6, NIX=1e6, NIC=1e6)
S2 = dict(DIF=4e6, DIFC=4e6, NI22=1e6, NI30=1e6, NI61=1e6, NIX=4e6, NIC=2e6)
LARGE = ('DIF', 'DIFC', 'NIX', 'NIC')
SMTOT = sum(SM.values()) + MJ
P = print


def kind(p):
    return 'Z' if p.startswith('Z') else ('tt' if p.startswith(('tt', 'tW', 't-')) else 'W')


def sm_terms(n_generated):
    m_full = n_generated * O['M_FULL']['Z']
    k_full = SMTOT / m_full
    return k_full, k_full * O['LOW_CLASS']['Z'][1] / 0.98, m_full


# ---- sampler with common random numbers ---------------------------------------------------------------------------------------
_E = {}


def estream(tag, seed=7):
    """1e5 unit exponentials, one fixed stream per (tag, seed)."""
    key = (tag, seed)
    if key not in _E:
        rnd = random.Random(f'{seed}|{tag}')
        n = O['ND_CROSS'] if tag.startswith('x') else O['ND']
        _E[key] = array('d', (rnd.expovariate(1.0) for _ in range(n)))
    return _E[key]


_PU = {}


def pustream(pu, seed=7):
    key = (pu[0], pu[1], seed)
    if key not in _PU:
        rnd = random.Random(f'{seed}|pu')
        out = []
        for _ in range(O['ND']):
            x = pu[0] * math.exp(pu[1] * rnd.gauss(0, 1))
            out.append(min(x, -pu[2] * rnd.expovariate(1.0)))
        _PU[key] = array('d', out)
    return _PU[key]


def quant(v, f):
    s = sorted(v)
    return s[int(f * len(s))]


PUS = [('R09', R.PU9)] + [(f'R08@{x:.0f}', (x, 0.43, R.PU_CAP)) for x in O['R08_PILEUP']]
LIMIT = 300.0 * (1.0 - O['TIE'])


def zero_sum(terms, seed=7):
    z = [0.0] * O['ND']
    for i, (lab, k) in enumerate(terms):
        e = estream(f't{i}', seed)
        z = [a + k * b for a, b in zip(z, e)]
    return z


def crossing(base, k):
    """first count m at which B50 >= 300 (1 - TIE) when one term of transfer factor k counts m and the others zero; ND_CROSS draws."""
    n = O['ND_CROSS']
    b = base[:n]
    prev = quant(b, 0.5)
    if prev >= LIMIT:
        return 0, prev, None
    for m in range(1, 80):
        e = estream(f'x{m}')
        b = [a + k * c for a, c in zip(b, e[:n])]
        v = quant(b, 0.5)
        if v >= LIMIT:
            return m, v, prev
        prev = v
    return None, prev, None


def case(lab, terms, cross=(), show=True, seed=7):
    """terms: list of (label, events per count), all at zero counts.  Returns dict by pile-up label."""
    z = zero_sum(terms, seed)
    out = {}
    for pl, pu in PUS:
        b = [a + c for a, c in zip(z, pustream(pu, seed))]
        r = dict(empty=quant(b, 0.5), q16=quant(b, 0.16), q84=quant(b, 0.84), cross={})
        for name in cross:
            ks = [k for lab_, k in terms if lab_ in (name if isinstance(name, tuple) else (name,))]
            r['cross'][name] = [crossing(b, k) for k in ks]
        out[pl] = r
    if show:
        e = [out[pl]['empty'] for pl, _ in PUS]
        P(f'  {lab}')
        P('      events per count: ' + ', '.join(f'{a} {k:.2f}' for a, k in terms))
        P(f"      empty pilot B50: R09 {e[0]:.1f} [16-84 %: {out['R09']['q16']:.0f}-{out['R09']['q84']:.0f}]; R08 at pile-up 88 / 118 / 148: {e[1]:.1f} / {e[2]:.1f} / {e[3]:.1f}"
          + '   ' + ' / '.join('PAUSES WHEN EMPTY' if x >= LIMIT else 'below' for x in e))
        for name in cross:
            cells = []
            for pl, _ in PUS:
                cs = out[pl]['cross'][name]
                ms = sorted({c[0] for c in cs})
                cells.append(f"{pl}: " + ('-'.join(str(m) for m in ms))
                             + ' (' + '; '.join(f'B50 {c[1]:.1f} at {c[0]}' + (f', {c[2]:.1f} at {c[0] - 1}' if c[2] is not None else '') for c in cs) + ')')
            nm = name if isinstance(name, str) else 'one large B1 sample (' + ', '.join(name) + ')'
            P(f'      pause at how many counts in {nm}, the others zero: ' + ' | '.join(cells))
    return out


def b1_terms(sizes, use, nt):
    return [(t, nt[t] / sizes[t]) for t in use]


def smz(n_gen=2.3e6):
    kf, kl, _ = sm_terms(n_gen)
    return [('Z', kf), ('Zlow', kl)]


def reach(floors, pu=None):
    gam = [(x, 0) for x in floors] + [NS['MJK']]
    pmf, (b16, b50_, b84) = NS['pmf_pred'](gam, (R.PU9 if pu is None else pu,))
    lim = [NS['s95_pmf'](pmf, NS['quant_pmf'](pmf, f)) for f in (0.16, 0.5, 0.84)]
    return dict(B16=b16, B50=b50_, B84=b84, reach_median=NS['reach_of'](lim[1]), reach_84_edge=NS['reach_of'](lim[2]))


def main():
    allt = list(CLASSES); len_t = ['DIF', 'NI22', 'NI30', 'NI61']
    kf, kl, mf = sm_terms(O['PILOT_HS_GENERATED'])
    P('p2z_addendum1.py -- strategy addendum 1, version 4.  ESTIMATE unless marked [V].  Sections [1]-[7], [9], [10], [12]: as version 3.')
    P(f"budget copy sha256 {R.hashlib.sha256(R.COPY.read_bytes()).hexdigest()}")
    P('OVERRIDES (version 2): ' + json.dumps(OVERRIDES))
    P('OVERRIDES_V3: ' + json.dumps(OVERRIDES_V3))
    P('OVERRIDES_V4: ' + json.dumps(OVERRIDES_V4))
    P(f'derived from OVERRIDES_V4: Z(nunu) pilot job {Z_MS:.1f} ms and {Z_KB:.2f} kB per generated event (three done jobs); pilot.mb {MB_CPU_H:.2f} CPU-h for 40 jobs (two done jobs)')

    # ================================================================================================================ [1]
    P('\n[1] PARTITION AND N_t  [V counts: p2-c-part-0; N_t: E]')
    b1sum = sum(CLASSES.values())
    P(f"  firings {NF}; vertices {PART['n_vertices']}; classes: " + ', '.join(f'{k} {v}' for k, v in CNT.items()))
    P(f"  B1 classes: " + ', '.join(f'{k} {v}' for k, v in CLASSES.items()) + f"; sum of the B1 classes {b1sum}; + conversions {CNT['conversion']} + other {CNT['other']}"
      f" = {b1sum + CNT['conversion'] + CNT['other']} (all vertices: {PART['counts_sum']})")
    assert b1sum + CNT['conversion'] + CNT['other'] == PART['n_vertices'] == PART['counts_sum']
    P(f"  species of DIFC {PART['counts']['difc']['211']} pi, {PART['counts']['difc']['321']} K; DIF {PART['counts']['dif']['211']} pi, {PART['counts']['dif']['321']} K, K0L {CNT['k0l']}")
    P(f"  N_t = N_trig {NTRIG:.5g} x 200 x pool in road {ROAD:.5f} (= {PART['pool_per_interaction']:.5f} x 0.30 / 2 pi) x class vertices per firing x F_HS {O['F_HS']:.4f}")
    for k in allt:
        P(f"    {k:5s} count {CLASSES[k]:6d}  per firing {CLASSES[k] / NF:.5f}  N_t {NT[k]:.4g}  (minimum-bias share alone {NT_MB[k]:.4g}; statistical error {100 / math.sqrt(CLASSES[k]):.1f} %)")
    P(f"    sum N_t {sum(NT.values()):.4g}  (minimum-bias share {sum(NT_MB.values()):.4g}; hard-scatter share at F_HS {NT_HS:.3g})")
    fro = dict(DIF=NTRIG * 1.5945, NI22=NTRIG * .09823 * .22, NI30=NTRIG * .12408 * .22, NI61=NTRIG * .12408 * .22)
    P(f"    frozen (Table 4.4a): DIF {fro['DIF']:.3g}, NI {fro['NI22']:.3g} / {fro['NI30']:.3g} / {fro['NI61']:.3g}, sum {sum(fro.values()):.3g}; ratio new / frozen {sum(NT.values()) / sum(fro.values()):.2f}")
    kk = lambda c: NTRIG * 200 * ROAD * c / NF * O['F_HS']   # noqa: E731
    v1r = PART['dif_first_arc_in_v1_range']
    P(f"    DIF pieces: first arc at 30-1000 mm (v1's own definition) {v1r} -> {kk(v1r):.3g} (x{kk(v1r) / fro['DIF']:.3f} of the frozen 6.51e7); first arc at r < 30 or > 1000 mm"
      f" {CNT['dif'] - v1r} -> {kk(CNT['dif'] - v1r):.3g}; K0L {CNT['k0l']} -> {kk(CNT['k0l']):.3g}")
    P(f"    conversions of minimum-bias photons (B2 by the route table, not B1): {CNT['conversion']} -> {200 * ROAD * CNT['conversion'] / NF:.2f} per triggered event in the road,"
      f" {NTRIG * 200 * ROAD * CNT['conversion'] / NF:.3g} in 3 ab^-1 (minimum-bias share)")
    P(f"    later decays (DIFC) from parents above 0.57 GeV: 31,238 of {CNT['difc']} = {31238 / CNT['difc']:.0%} [V: review Wanda, part.py; the 53 % of version 2 was the first review's number for 30-1000 mm]")
    a, b = 200 * O['V1_DIF_RATE_T_G4'], 200 * PART['v1_rates']['dif']
    c3 = 200 * O['V1_DIF_RATE_PX_MBB']
    P(f"  C-6 hard-scatter share from v1's rates: v1 total 1.5687-1.5945 (STR l.255); v1 formula, minimum bias x 200: {a:.3f} on 40,000 interactions (p2-c-t-g4), {b:.3f} on the 25,000"
      f" of the partition campaign and {c3:.3f} on 125,000 (p2-c-px-mbb-big) -> share {1.5945 / b - 1:+.1%} / {1.5945 / c3 - 1:+.1%} / {1.5945 / a - 1:+.1%}, i.e. 0-3 %; F_HS = {O['F_HS']:.4f} kept as an upper-side value")
    hs_share = O['HS_IN_ROAD_PER_TRIG'] / (200 * ROAD)
    P(f"  A-2 measured on the hard-scatter slice [V: p2-c-px-hsg-r0, {O['HS_SLICE_EVENTS']} generated Z(nunu) events]: pool parents inside the road per triggered event"
      f" {O['HS_IN_ROAD_PER_TRIG']:.3f} +- {100 / math.sqrt(O['HS_SLICE_PARENTS_W']):.1f} % ({O['HS_SLICE_PARENTS_W']} parents in {O['HS_SLICE_EVENTS_W']} events of non-zero weight),"
      f" against 200 x {ROAD:.4f} = {200 * ROAD:.1f} from minimum bias: {hs_share:.2%} by parent count; at any azimuth {O['HS_ANY_PHI_PER_TRIG']:.1f} per triggered event"
      f" ({O['HS_ANY_PHI_PER_TRIG'] / O['HS_IN_ROAD_PER_TRIG']:.0f} off-road hadrons per in-road one; a uniform azimuth would put {O['HS_ANY_PHI_PER_TRIG'] * 0.30 / (2 * math.pi):.2f} in the road)")

    # ================================================================================================================ [2]
    P('\n[2] EVENTS IN 3 ab^-1 PER PILOT COUNT')
    for sl, sz in (('10^6 per sample', S1), ('proposed sizes 4, 4, 1, 1, 1, 4, 2 x 10^6', S2)):
        P(f"  {sl}: " + ', '.join(f'{t} {NT[t] / sz[t]:.1f}' for t in allt) + '   (with the hard-scatter share read on its own sample: '
          + ', '.join(f'{t} {NT_MB[t] / sz[t]:.1f}' for t in allt) + ')')
    P(f"  frozen: DIF {NS['D15_KD']:.1f}, NI " + ' / '.join(f'{x:.2f}' for x in NS['D15_KNI']) + f", all SM through one Z(nunu) count {NS['D15_KSM']:.1f}")
    P(f"  Z(nunu) pilot 2.3e6 generated: M (full-weight class) {mf:.4g}; one full-weight count = {kf:.2f} events for all SM processes and the multijets ({NZ / mf:.1f} for Z(nunu) alone);"
      f" one low-weight (0.05) count = {kl:.2f}")
    P(f'  v4: other Z(nunu) pilot sizes (generated events: CPU-h at the measured {Z_MS:.1f} ms of the pilot jobs [127 in version 3], events per full-weight count): '
      + '; '.join(f'{n:.3g}: {n * Z_MS / 3.6e6:.0f} CPU-h, {sm_terms(n)[0]:.1f}' for n in (0.83e6, 1.5e6, 2.3e6, 3.5e6, 5.23e6)))

    # ================================================================================================================ [3]
    P('\n[3] A-2  THE HARD-SCATTER PARENT SAMPLE pilot.c0.hs')
    y_b1 = b1sum / NF
    nt_hs_meas = NTRIG * O['HS_IN_ROAD_PER_TRIG'] * y_b1
    P(f"  N_t of the hard-scatter share, all seven classes: {NT_HS:.3g} at F_HS = {O['F_HS']:.4f} (used below; upper side);"
      f" from the measured parent count and the minimum-bias yield {y_b1:.4f} B1 vertices per firing: {nt_hs_meas:.3g} [E: the yield of the stiffer parents is not measured]")
    hs_k = {}
    par_w = O['HS_SLICE_PARENTS_W'] / O['HS_SLICE_EVENTS']          # in-road parents in events of non-zero weight, per generated event
    for hl, m in O['HS_SIZES'].items():
        fir = m / y_b1
        hs_k[hl] = NT_HS / m
        hs7 = {t: (NT[t] - NT_MB[t]) / (m * CLASSES[t] / b1sum) for t in allt}
        g4h, chh = fir * O['G4_ALL_MS'] / 3.6e6, m * O['HS_CHAIN_S'] / 3600
        P(f"  {hl}: {m:.2g} vertices in the natural class mixture = {fir:.3g} firings; one count = {hs_k[hl]:.1f} events as ONE term ({nt_hs_meas / m:.1f} at the measured parent count);"
          f" as seven weight classes (STR l.1564 read literally): {hs7['DIF']:.1f} per count in each class, seven zeros;"
          f" Geant4 {g4h:.2f} + chain {chh:.2f} = {g4h + chh:.1f} CPU-h")
        for src, nev in (('2e4 generator-level events (version 2)', 2e4), ('2e5 generator-level events', 2e5), ('the 2.3e6 Z(nunu) pilot events (stored hadron list, C-8)', 2.3e6)):
            npar = nev * par_w
            P(f"      parents from {src}: {npar:.3g} distinct in-road parents of non-zero weight, {fir / npar:.1f} firings each, {m / npar:.2f} vertices per parent"
              + (f"; pool generation {nev * O['HSPOOL_GEN_S'] / 3600:.1f} CPU-h" if nev < 1e6 else '; no generation cost'))
    nt_off = NTRIG * (O['HS_ANY_PHI_PER_TRIG'] - O['HS_IN_ROAD_PER_TRIG']) * y_b1
    mo = O['HS_OFFROAD_SIZE']
    P(f"  off-road hard-scatter hadrons (not in N_t as frozen: N_t counts parents inside the road): {nt_off:.3g} B1 vertices in 3 ab^-1 at the minimum-bias yield [E];"
      f" a second stratum of {mo:.2g} vertices would read {nt_off / mo:.1f} events per count and cost"
      f" {mo / y_b1 * O['G4_ALL_MS'] / 3.6e6:.1f} + {mo * O['HS_CHAIN_S'] / 3600:.1f} = {mo / y_b1 * O['G4_ALL_MS'] / 3.6e6 + mo * O['HS_CHAIN_S'] / 3600:.0f} CPU-h;"
      f" all central hadrons in one unweighted sample of 2e6 would read {(nt_off + nt_hs_meas) / 2e6:.0f} events per count")
    hs_off_k = nt_off / mo

    # ================================================================================================================ [4]
    P('\n[4] RULE 1: EMPTY-PILOT READING AND CROSSINGS  (B50 and crossings: medians of 1e5 draws, common random numbers; a reading >= 300 x (1 - 0.003) = 299.1 pauses: ties pause, STR l.2757)')
    frz = [('DIF', NS['D15_KD'])] + list(zip(('NI22', 'NI30', 'NI61'), NS['D15_KNI'])) + [('Z', NS['D15_KSM'])]
    chk = NS['d15_q'](NS['d15_gam'](), nd=100000)
    res = {}
    res['frozen'] = case('FROZEN (STR: 4 B1 terms, v1 N_t, 10^6 per sample, 18.1 per Z count)', frz, cross=('Z', 'DIF'))
    P(f"      regression check: d15_q of the unchanged budget script, 1e5 draws: {chk[1]:.1f} [{chk[0]:.0f}-{chk[2]:.0f}] (STR prints 76 [37-152]);"
      f" frozen m_Z = 11 / 12 / 13: " + ' / '.join(f"{NS['d15_q'](NS['d15_gam'](m), nd=100000)[1]:.1f}" for m in (11, 12, 13)))
    res['7_S1'] = case('SEVEN TERMS, 10^6 per sample, hard-scatter parents not read (H3)', b1_terms(S1, allt, NT) + smz(), cross=('Z', LARGE))
    res['7_S2_H3'] = case('SEVEN TERMS, proposed sizes, hard-scatter parents NOT READ (H3; the reading of version 2)', b1_terms(S2, allt, NT) + smz(), cross=('Z', LARGE))
    hs1 = [('HS', hs_k['H1'])]
    draft = b1_terms(S2, allt, NT_MB) + hs1 + smz()
    res['draft'] = case('** DRAFT **  SEVEN TERMS, proposed sizes, + pilot.c0.hs H1 (2e6 vertices) as one term', draft, cross=('Z', LARGE, 'HS'))
    seeds = [case('', draft, show=False, seed=s) for s in (11, 12, 13)]
    P('      three other seeds, empty pilot: ' + '; '.join(f"{pl} " + ' / '.join(f"{s[pl]['empty']:.1f}" for s in seeds) for pl, _ in PUS))
    for dct in (_E, _PU):
        for key in [k_ for k_ in dct if k_[-1] != 7]:
            del dct[key]
    hs7 = lambda m: [(f'HS-{t}', (NT[t] - NT_MB[t]) / (m * CLASSES[t] / b1sum)) for t in allt]   # noqa: E731
    res['H1_7'] = case('SEVEN TERMS, proposed sizes, + H1 (2e6) as seven weight classes (STR l.1564 literally)', b1_terms(S2, allt, NT_MB) + hs7(2e6) + smz(), cross=('Z', LARGE))
    res['H2_1'] = case('SEVEN TERMS, proposed sizes, + H2 (2e5 vertices, as drafted in version 2) as one term', b1_terms(S2, allt, NT_MB) + [('HS', hs_k['H2'])] + smz(), cross=('Z', LARGE, 'HS'))
    res['H2_7'] = case('SEVEN TERMS, proposed sizes, + H2 (2e5) as seven weight classes', b1_terms(S2, allt, NT_MB) + hs7(2e5) + smz(), cross=('Z', LARGE))
    res['draft_off'] = case('DRAFT + the off-road hard-scatter stratum (7.3e6 vertices) as one more term', draft + [('HSoff', hs_off_k)], cross=('Z', LARGE))
    for n in (3.5e6, 5.23e6):
        res[f'draft_Z{n:g}'] = case(f'DRAFT with the Z(nunu) pilot at {n:.3g} generated events', b1_terms(S2, allt, NT_MB) + hs1 + smz(n), cross=('Z', LARGE))
    s2x2 = {t: 2 * v for t, v in S2.items()}
    res['draft_x2'] = case('DRAFT with every B1 sample doubled (3.4e7 events) and H1 doubled', b1_terms(s2x2, allt, NT_MB) + [('HS', hs_k['H1'] / 2)] + smz(), cross=('Z', LARGE))
    P('  -- the number of terms (same 1.7e7 B1 events; hard-scatter parents not read in these four rows, so that they compare with 159) --')
    res['4_S2'] = case('FOUR TERMS (lenient: only DIF and the three radii read; 2.4e8 vertices not read), proposed sizes', b1_terms(S2, len_t, NT) + smz(), cross=('Z', 'DIF'))
    res['4_S1'] = case('FOUR TERMS (lenient), 10^6 per sample', b1_terms(S1, len_t, NT) + smz(), cross=('Z', 'DIF'))
    n3 = dict(DEC=NT['DIF'] + NT['DIFC'], NI3=NT['NI22'] + NT['NI30'] + NT['NI61'], NIO=NT['NIX'] + NT['NIC'])
    m3 = dict(DEC=8e6, NI3=3e6, NIO=6e6)
    res['3'] = case('THREE TERMS (all decays; the three radii; all other interactions), each sample a natural mixture, 8 + 3 + 6 x 10^6',
                    [(t, n3[t] / m3[t]) for t in n3] + smz(), cross=('Z', ('DEC', 'NIO')))
    res['1'] = case('ONE TERM (all B1 vertices in one natural mixture of 1.7e7 events)', [('B1', sum(NT.values()) / 1.7e7)] + smz(), cross=('Z', 'B1'))
    for lab_, add in (('with H1 as one term', hs1),):
        res['4_H1'] = case(f'FOUR TERMS (lenient), proposed sizes, {lab_}', b1_terms(S2, len_t, NT_MB) + add + smz(), cross=('Z',))
        res['3_H1'] = case(f'THREE TERMS, {lab_}', [(t, n3[t] / O["F_HS"] / m3[t]) for t in n3] + add + smz(), cross=('Z',))
        res['1_H1'] = case(f'ONE TERM, {lab_}', [('B1', sum(NT_MB.values()) / 1.7e7)] + add + smz(), cross=('Z',))

    # ================================================================================================================ [5]
    P('\n[5] B-3  WHAT THE NUMBER OF B1 TERMS DOES TO THE TWO TEST FAMILIES  (functions one_rung of the unchanged budget script)')
    L = math.log(2)
    one_rung = NS['one_rung']
    p2_ = None
    for nb in (4, 7, 3, 1):
        K = 6 + nb; n2 = 4 + nb; tc = 15 + nb
        ac = 0.05 / tc; pterm = ac + 4 * ac * ac; pfam = 1 - (1 - pterm) ** tc
        cells = []
        for fs in (0.0, 1.0):
            p = one_rung(L, fs * L / 3, L / 3, K)[3]
            anyf = 1 - (1 - p) ** K
            elig = 1 - (1 - p / 2) ** n2 * (1 - p * p)
            cells.append(f's_model = {fs:.0f} x cap: per test {p:.4f}, at least one FAIL {anyf:.3f}, one that removes a selection {elig:.3f}, either family {1 - (1 - elig) * (1 - pfam):.3f}')
        P(f"  {nb} B1 terms: K = {K} (B1-a x {nb}, B4-c x 4, B2-a, B2-b), re-test threshold 0.05/K = {0.05 / K:.5f}; T_c = {tc}, alpha_c = {ac:.5f}, ceiling family false FAIL at the boundary {pfam:.4f}")
        for c in cells:
            P('      ' + c)
    P('  (frozen: K = 10, T_c = 19: budget_stdout_v9.txt l.453-477: closure family 2.1-4.2 %, ceiling family 4.9 %, either 6.9-8.9 %)')

    # ================================================================================================================ [6]
    P('\n[6] B-1  ROAD ORIENTATIONS;  B-2  LOW pT AND |eta| > 1')
    P(f"  21 non-overlapping orientations of full width 0.30: 21 x 0.30 = {21 * 0.30:.3f} against 2 pi = {2 * math.pi:.4f}: the grid of step 2 pi / 21 = {2 * math.pi / 21:.4f} over-covers by"
      f" {21 * 0.30 / (2 * math.pi) - 1:+.2%}; N_t (parents inside one road: pool x 0.30 / 2 pi) x m / M with m summed over the 21 orientations is the rate in the road, over-read by that amount")
    lo_road = O['LOWPT_PER_INT'] * 0.30 / (2 * math.pi)
    P(f"  low-pT parents (0.3 < pT <= 0.5 GeV, |eta| < 1) [V: p2-c-px-mbb-big, 125,000 interactions]: {O['LOWPT_PER_INT']:.3f} per interaction, {lo_road:.4f} in a road"
      f" ({O['LOWPT_PER_INT'] / O['POOL_PER_INT_SLICE']:.0%} of the pool's {O['POOL_PER_INT_SLICE']:.3f})")
    lowk = []
    for f in O['LOWPT_YIELD_FACTOR']:
        nt = NTRIG * 200 * lo_road * y_b1 * f
        lowk.append(nt / O['LOWPT_SIZE'])
        m25 = nt / 25.0
        fir = m25 / (y_b1 * f)
        P(f"    B1 vertices per firing = {f:.0f} x the pool's {y_b1:.4f} (NOT MEASURED): N_t {nt:.3g} ({nt / sum(NT.values()):.2f} of the seven classes); one count in {O['LOWPT_SIZE']:.1g}"
          f" events = {nt / O['LOWPT_SIZE']:.0f} events; a zero count allows {U68 * nt / O['LOWPT_SIZE']:.0f} (limit 300);"
          f" 25 events per count needs {m25:.3g} events: Geant4 {fir * O['G4_ALL_MS'] / 3.6e6:.1f} + chain {m25 * O['LOWPT_CHAIN_S'] / 3600:.1f} = {fir * O['G4_ALL_MS'] / 3.6e6 + m25 * O['LOWPT_CHAIN_S'] / 3600:.0f} CPU-h")
    res['draft_low'] = case('DRAFT + the low-pT population as a term sized for 25 events per count (for the decision; NOT in the draft)', draft + [('LOWPT', 25.0)], cross=('Z',))
    res['draft_low2e5'] = case(f'DRAFT + the 2e5 low-pT check sample read as a term at its zero floor ({lowk[0]:.0f} per count; shown to make the point)', draft + [('LOWPT', lowk[0])])
    ff = O['FWD_PER_INT'] / O['POOL_PER_INT_SLICE']
    P(f"  parents with pT > 0.5 GeV at 1 <= |eta| < 1.5 [V: p2-c-px-mbb-big]: {O['FWD_PER_INT']:.3f} per interaction, {ff:.0%} of the pool; N_t {ff * sum(NT.values()):.3g} at the pool's vertex yield"
      f" (yield NOT MEASURED) [E]; a 2e5 check sample would read {ff * sum(NT.values()) / 2e5:.0f} events per count")
    P(f"  B1-g (Phase 3, 1,000 pile-up events): one count = N_trig / 1,000 = {NTRIG / 1000:.3g} events")

    # ================================================================================================================ [7]
    P('\n[7] A-1  HAND-OVER VALIDATION OF VERSION 2, AS MEASURED  [V: p2-c-b1yv-val.json; 1,000 events per stream, parent comparison on the first 100]')
    for f in VAL['files']:
        tot = f['ab_surfaces_both'] + f['ab_only_geant4'] + f['ab_only_fatras']
        P(f"    {f['term']:5s} parent hits {f['parent_hits']:6d}; later than the vertex time {f['parent_hits_later_than_vertex_time']:3d}; beyond the vertex radius {f['parent_hits_beyond_vertex_radius']};"
          f" Geant4 pre-vertex crossings of a counting surface {tot:5d}, of which without a Fatras parent hit {f['ab_only_geant4']:4d}"
          + (f" = {f['ab_only_geant4'] / tot:.1%}" if tot else '') + f"; product hits before the vertex time {f['product_hits_earlier_than_vertex']}")
    P(f"    all_hard_checks_pass (checks of version 2, which did not include the missing-crossing check): {VAL['all_hard_checks_pass']}")
    P(f"    events of the two after-a-turn streams at the proposed sizes: {S2['DIFC'] + S2['NIC']:.2g} of {sum(S2.values()):.2g}")

    # ================================================================================================================ [8]
    P('\n[8] v4  PILOT: SIZES, COST, STORAGE, CALENDAR  [E from V unit costs; part 1 from the first done jobs]')
    import datetime as _dt
    cost = {}
    chain_pil = dict(O['CHAIN_B1'], **O['CHAIN_B1_HYBRID'])
    for sl, sz, hsm in (('10^6 per sample', S1, 0.0), ('proposed sizes', S2, O['HS_SIZES']['H1'])):
        n_all0 = max(sz[t] / (CLASSES[t] / NF) for t in LARGE)
        n_all = n_all0 * O['ALL_PASS_MARGIN']
        n_ni = max(sz['NI22'] - n_all * CLASSES['NI22'] / NF, 0.0) / (CLASSES['NI22'] / NF)
        g4 = (n_all * O['G4_ALL_MS_PILOT'] + n_ni * O['G4_NI_MS_PILOT']) / 3.6e6
        g4_v3 = (n_all * O['G4_ALL_MS'] + n_ni * O['G4_NI_MS']) / 3.6e6
        chain = sum(sz[t] * chain_pil[t] for t in sz) / 3600.0
        chain_v3 = sum(sz[t] * O['CHAIN_B1'][t] for t in sz) / 3600.0
        zc = O['PILOT_HS_GENERATED'] * Z_MS / 3.6e6
        hs_g4 = hsm / y_b1 * O['G4_ALL_MS_PILOT'] / 3.6e6
        hs_c = (hs_g4 + hsm * O['HS_CHAIN_S'] / 3600) if hsm else 0.0
        low_c = 0.5
        nev = sum(sz.values()) + hsm + O['LOWPT_SIZE']
        njob = math.ceil(n_all / O['G4_JOB_FIRINGS'])
        gb_b1 = (sum(sz[t] * O['B_PER_EVENT'][t] for t in sz) + hsm * O['B_PER_EVENT']['HS'] + O['LOWPT_SIZE'] * O['B_PER_EVENT']['LOWPT']) * 1e-9
        gb_z = O['PILOT_HS_GENERATED'] * Z_KB * 1e-6
        gb_g4 = njob * O['G4_ALL_JOB_GB'] + O['G4_NI_GB']
        gb = gb_b1 + gb_z + O['PILOT_MB_GB'] + gb_g4
        part1 = zc + MB_CPU_H
        b1p = g4 + chain + hs_c + low_c
        cost[sl] = dict(n_all=n_all, n_ni=n_ni, g4=g4, chain=chain, z=zc, hs=hs_c, low=low_c, total=part1 + b1p, b1_part=b1p, part1=part1, nev=nev, gb=gb,
                        gb_b1=gb_b1, gb_z=gb_z, gb_g4=gb_g4)
        c = cost[sl]
        P(f"  {sl}: 'all' pass {n_all:.4g} firings (+ 3 % margin; available vertices: "
          + ', '.join(f'{t} {n_all * CLASSES[t] / NF:.3g}' for t in LARGE) + f"), {njob} jobs of <= 2e6 firings ({O['G4_JOB_FIRINGS'] * O['G4_ALL_MS_PILOT'] / 6e4:.0f} min each);"
          f" 'ni' pass {n_ni:.4g} firings")
        P(f"      CPU-h: minimum bias {MB_CPU_H:.1f} [10.0 planned]; Geant4 {g4:.1f} at the production-code cost {O['G4_ALL_MS_PILOT']:.3f} / {O['G4_NI_MS_PILOT']:.4f} ms per firing [{g4_v3:.1f} in version 3 at 0.305 / 0.0469];"
          f" chain {chain:.1f} [{chain_v3:.1f} in version 3; DIF-C and NI-C now at the option-(a) cost]; Z(nunu) {zc:.1f} [81.1 in version 3 at 127 ms; 85.0 planned by the executor at 133.2];"
          f" hard-scatter sample {hs_c:.1f}; low-pT check {low_c:.1f}")
        P(f"      TOTAL {c['total']:.1f} CPU-h (budgeted 54.5; overrun {c['total'] - 54.5:.0f}; version 3: 134.5).  PART 1, launched (Z(nunu) + minimum bias): {part1:.1f};  B1 PART, not launched: {b1p:.1f}")
        P(f"      storage {gb:.0f} GB = B1 events {gb_b1:.1f} ({nev:.3g} events at the measured slice sizes per stream, 2.6-5.4 kB) + Z(nunu) {gb_z:.1f} (2.3e6 x {Z_KB:.2f} kB) + minimum bias {O['PILOT_MB_GB']}"
          f" + Geant4 vertex files {gb_g4:.1f} ({njob} x {O['G4_ALL_JOB_GB']} GB measured per 'all' job + {O['G4_NI_GB']} for the 'ni' pass [E]; NOT in the 156 GB of version 3, which carried 1.5 GB for both);"
          f" part 1 alone {gb_z + O['PILOT_MB_GB']:.1f} GB")
    cp = cost['proposed sizes']
    pil = cp['total']
    t0 = _dt.datetime.strptime(O['PILOT_LAUNCH'], '%Y-%m-%d %H:%M')
    d5 = _dt.datetime.strptime(O['DAY5'], '%Y-%m-%d %H:%M')
    fmt = lambda t: t.strftime('%d Nov %H:%M')   # noqa: E731
    t_mb = t0 + _dt.timedelta(hours=MB_CPU_H)                         # pilot.mb is the first campaign of lane 0 (PLAN_p2-c-pilot_mb-znn.json, lanes for 2 slots)
    t1 = t0 + _dt.timedelta(hours=cp['part1'] / O['PILOT_LANES'])
    P(f"  calendar [E: wall = CPU, lanes never idle]: part 1 launched {fmt(t0)} on {O['PILOT_LANES']} lanes: pilot.mb complete about {fmt(t_mb)} (first campaign of lane 0);"
      f" Z(nunu) complete about {fmt(t1)} ({cp['part1']:.1f} CPU-h / {O['PILOT_LANES']})")
    for nl in (2, 3, 1):
        t2 = t1 + _dt.timedelta(hours=cp['b1_part'] / nl)
        P(f"      B1 part ({cp['b1_part']:.1f} CPU-h) started when Z(nunu) ends, on {nl} lane(s): complete about {fmt(t2)}; margin to day 5 ({fmt(d5)}): {(d5 - t2).total_seconds() / 3600:.0f} h")
    g4_only = cp['g4']
    t3 = t1 + _dt.timedelta(hours=(cp['b1_part'] - g4_only) / 2)
    P(f"      if the two Geant4 passes ({g4_only:.1f} CPU-h; they need only pilot.mb) run on a third slot before Z(nunu) ends: B1 part complete about {fmt(t3)} on 2 lanes")
    P(f"      order forced by the inputs: pilot.mb -> pilot.g4 ('all', 'ni'); Z(nunu) files (stored hadron list) -> parents of pilot.c0.hs -> its Geant4 firing and chain: pilot.c0.hs cannot start before about {fmt(t1)}")
    P(f"  B1 samples doubled: + {cp['g4'] + cp['chain'] + cp['hs']:.0f} CPU-h; Z(nunu) at 3.5e6 / 5.23e6: + {1.2e6 * Z_MS / 3.6e6:.0f} / + {2.93e6 * Z_MS / 3.6e6:.0f} CPU-h (appended parts, nothing regenerated)")
    P(f"  another jet radius or clustering input for the Z(nunu) summary: regeneration at generator level from the stored seeds, 2.3e6 x 46.1 ms = {2.3e6 * 0.0461 / 3600:.0f} CPU-h [E from V: generation stage of p2-c-px-znnb]")

    # ================================================================================================================ [9]
    P('\n[9] TABLE 4.4a AT THE APPROVED CPU  (457 + 208 CPU-h; M_t ~ sqrt(N_t / c_t); G = 1)')
    terms = NS['terms']; plan = alloc(NS['C_POOL'])
    smn = set(SM)
    cpu_sm = sum(plan[t] * c / H for t, n, c in terms if t in smn); cpu_b1 = sum(plan[t] * c / H for t, n, c in terms if t not in smn)
    P(f"  planned split SM {cpu_sm:.1f} / B1 {cpu_b1:.1f} CPU-h; planned floors SM {sum(U68 * n / plan[t] for t, n, c in terms if t in smn):.2f}, B1 {sum(U68 * n / plan[t] for t, n, c in terms if t not in smn):.2f},"
      f" all {sum(U68 * n / plan[t] for t, n, c in terms):.2f}")
    tabs = {}
    w_low = O['LOW_CLASS']['Z'][1] / 0.98
    for lab, forced, pf in (('as timed', False, False), ('forced tt', True, False), ('preselection before the chain', False, True), ('both', True, True)):
        tt = []
        for p, n in SM.items():
            k = kind(p)
            cg, cc = O['COST']['tt_forced' if (k == 'tt' and forced) else k]
            cge = cg + (O['F_PASS'][k] if pf else 1.0) * cc
            tt.append((p, n, cge / O['M_FULL'][k], cge, k))
        al = alloc(cpu_sm, tt=[(t, n, c) for t, n, c, _, _ in tt])
        rows = [dict(term=t, floor=U68 * n / al[t], M=al[t]) for t, n, c, cge, k in tt]
        fs = sum(r['floor'] for r in rows)
        tabs[lab] = dict(rows=rows, floor_SM=fs, low=fs * w_low, tt_share=sum(r['floor'] for r in rows if kind(r['term']) == 'tt') / fs)
        g = {r['term']: r['floor'] for r in rows}
        P(f"  SM, {lab:30s}: Z(nunu) {g['Z(nunu)+j']:.1f}, W(tau_h) {g['W(tau_h)']:.1f}, W(e nu) {g['W(e nu)']:.1f}, tt 1l {g['tt 1l']:.1f}; sum of 14 {fs:.1f}; tt-type share {tabs[lab]['tt_share']:.0%};"
          f" C-10 low-weight (0.05) classes, one zero each: + {fs * w_low:.1f} (= {w_low:.3f} x each row)")
    # B1, version 2 costing (each large class charged its own Geant4 pass) -- kept for the comparison
    g4_per = {t: O['G4_ALL_MS'] * 1e-3 / (CLASSES[t] / NF) for t in LARGE}
    y_ni = (CLASSES['NI22'] + CLASSES['NI30'] + CLASSES['NI61']) / NF
    g4_per.update({t: O['G4_NI_MS'] * 1e-3 / y_ni for t in ('NI22', 'NI30', 'NI61')})
    b1v2 = {}
    for lab, use in (('seven', allt), ('four', len_t)):
        tt = [(t, NT[t], O['CHAIN_B1'][t] + g4_per[t]) for t in use]
        al = alloc(cpu_b1, tt=tt)
        b1v2[lab] = {t: U68 * n / al[t] for t, n, c in tt}
        P(f"  B1, version-2 costing (one Geant4 pass charged per class), {lab}: " + ', '.join(f'{t} {v:.1f}' for t, v in b1v2[lab].items()) + f"; sum {sum(b1v2[lab].values()):.1f}")
    # B-5: one shared 'all' pass gives the vertices of every class; the rest of the CPU on the 'ni' pass (three radii only)
    yv = {t: CLASSES[t] / NF for t in allt}
    c_all = O['G4_ALL_MS'] * 1e-3 + sum(yv[t] * O['CHAIN_B1'][t] for t in allt)
    c_ni = O['G4_NI_MS'] * 1e-3 + sum(yv[t] * O['CHAIN_B1'][t] for t in ('NI22', 'NI30', 'NI61'))
    best = None
    for i in range(0, 1001):
        fa = i / 1000.0
        na = fa * cpu_b1 * H / c_all; nn = (1 - fa) * cpu_b1 * H / c_ni
        if na <= 0:
            continue
        fl = {t: U68 * NT[t] / (na * yv[t]) for t in LARGE}
        fl.update({t: U68 * NT[t] / ((na + nn) * yv[t]) for t in ('NI22', 'NI30', 'NI61')})
        if best is None or sum(fl.values()) < best[0]:
            best = (sum(fl.values()), fa, na, nn, fl)
    b1v3 = {t: best[4][t] for t in allt}
    P(f"  B-5  B1, seven classes, ONE shared 'all' pass ({c_all * 1e3:.3f} ms per firing with the chain for every vertex) + 'ni' pass ({c_ni * 1e3:.4f} ms per firing): best split {best[1]:.0%} of {cpu_b1:.0f} CPU-h on the 'all' pass"
      f" = {best[2]:.3g} firings, 'ni' pass {best[3]:.3g}: " + ', '.join(f'{t} {b1v3[t]:.1f}' for t in allt) + f"; sum {best[0]:.1f}  (version 2: {sum(b1v2['seven'].values()):.1f})")
    P(f"       events through the chain: {sum(best[2] * yv[t] for t in allt) + best[3] * y_ni:.3e}; B1 sum with ten times fewer 'ni' firings: "
      f"{sum(U68 * NT[t] / (best[2] * yv[t]) for t in LARGE) + sum(U68 * NT[t] / ((best[2] + 0.1 * best[3]) * yv[t]) for t in ('NI22', 'NI30', 'NI61')):.1f}")
    b1v3_four = {t: b1v2['four'][t] for t in len_t}
    sums = {}
    for a_ in tabs:
        s7 = tabs[a_]['floor_SM'] + sum(b1v3.values()); s7l = s7 + tabs[a_]['low']
        s4 = tabs[a_]['floor_SM'] + sum(b1v3_four.values())
        sums[a_] = (s7, s7l, s4)
        P(f"  ALL POOL TERMS, {a_:30s}: seven classes {s7:.0f} (with the low-weight classes {s7l:.0f}); four terms {s4:.0f}"
          f"   [version 2: {tabs[a_]['floor_SM'] + sum(b1v2['seven'].values()):.0f} / {tabs[a_]['floor_SM'] + sum(b1v2['four'].values()):.0f}]")
    P(f"  frozen: 12.6 (SM 8.6).  CPU-h for an SM floor of 39: {cpu_sm * tabs['both']['floor_SM'] / 39:.0f} (both) to {cpu_sm * tabs['as timed']['floor_SM'] / 39:.0f} (as timed);"
      f" of 8.6: {cpu_sm * tabs['both']['floor_SM'] / 8.6:.0f} to {cpu_sm * tabs['as timed']['floor_SM'] / 8.6:.0f}")
    P(f"  SM factor: costs x{39.0 / 8.64:.2f} (8.64 -> 39.0 with generated events counted as preselected, memo of 13:25), weights x{tabs['as timed']['floor_SM'] / 39.0:.2f}")
    # v4 sensitivity (NOT adopted in the table above, which is version 3's): the measured costs that became available after version 3
    c_all4 = O['G4_ALL_MS_PILOT'] * 1e-3 + sum(yv[t] * dict(O['CHAIN_B1'], **O['CHAIN_B1_HYBRID'])[t] for t in allt)
    c_ni4 = O['G4_NI_MS_PILOT'] * 1e-3 + sum(yv[t] * O['CHAIN_B1'][t] for t in ('NI22', 'NI30', 'NI61'))
    best4 = None
    for i in range(1, 1001):
        fa = i / 1000.0
        na = fa * cpu_b1 * H / c_all4; nn = (1 - fa) * cpu_b1 * H / c_ni4
        v = sum(U68 * NT[t] / (na * yv[t]) for t in LARGE) + sum(U68 * NT[t] / ((na + nn) * yv[t]) for t in ('NI22', 'NI30', 'NI61'))
        if best4 is None or v < best4:
            best4 = v
    zf = Z_MS / 127.0
    P(f"  v4 SENSITIVITY, not adopted (the table above stays as in version 3 until the day-12 re-allocation): with the production-code Geant4 cost and the option-(a) chain cost"
      f" ({c_all4 * 1e3:.3f} ms per 'all' firing against {c_all * 1e3:.3f}) the B1 sum is {best4:.1f} instead of {best[0]:.1f};"
      f" with the Z(nunu) cost {Z_MS:.1f} ms instead of 127 for the Z-type rows alone (x{zf:.3f} in cost, x{math.sqrt(zf):.3f} in the allowance of those rows): all pool terms as timed"
      f" about {sums['as timed'][1] + best4 - best[0] + (math.sqrt(zf) - 1) * sum(r['floor'] for r in tabs['as timed']['rows'] if kind(r['term']) == 'Z') * (1 + w_low):.0f} instead of {sums['as timed'][1]:.0f}"
      f" [E: the square-root rule applied to the Z rows only, no re-allocation]")

    # ================================================================================================================ [10]
    P('\n[10] REACH WITH EVERY CEILING EMPTY  (strategy functions pmf_pred, s95_pmf, reach_of; v1 placeholder efficiencies; ESTIMATE)')
    r0 = reach([n / plan[t] for t, n, c in terms])
    P(f"  frozen (regression check, STR Table 4.4c: 13 / 18 / 25, 790 [712]): B16/50/84 {r0['B16']:.0f} / {r0['B50']:.0f} / {r0['B84']:.0f}; reach {r0['reach_median']:.0f} [{r0['reach_84_edge']:.0f}]")
    rr = {}
    for a_ in ('as timed', 'both'):
        smf = [r['floor'] / U68 for r in tabs[a_]['rows']]
        low = [x * w_low for x in smf]
        for lab, b1f in (('seven classes, version-2 B1 costing (regression check)', [v / U68 for v in b1v2['seven'].values()]),
                         ('four terms (lenient)', [v / U68 for v in b1v2['four'].values()]),
                         ('seven classes, shared Geant4 pass (B-5)', [v / U68 for v in b1v3.values()]),
                         ('seven classes, shared pass, + low-weight classes (C-10)  ** version 3 **', [v / U68 for v in b1v3.values()] + low)):
            r = reach(smf + b1f)
            rr[(a_, lab)] = r
            P(f"  {a_:9s} + {lab}: B16/50/84 {r['B16']:.0f} / {r['B50']:.0f} / {r['B84']:.0f}; reach {r['reach_median']:.0f} [{r['reach_84_edge']:.0f}] GeV")
    pu8 = (NS['pu8'], 0.43, R.PU_CAP)
    r8f = reach([n / plan[t] for t, n, c in terms], pu8)
    P(f"  R08-like selection (pile-up median {NS['pu8']:.0f}), ceilings empty: frozen B50 {r8f['B50']:.0f}, reach {r8f['reach_median']:.0f} [{r8f['reach_84_edge']:.0f}] (STR: 113, 496 [435])")
    for a_ in ('as timed', 'both'):
        smf = [r['floor'] / U68 for r in tabs[a_]['rows']]
        r = reach(smf + [x * w_low for x in smf] + [v / U68 for v in b1v3.values()], pu8)
        r2 = reach(smf + [v / U68 for v in b1v2['seven'].values()], pu8)
        P(f"      {a_}: B50 {r['B50']:.0f}, reach {r['reach_median']:.0f} [{r['reach_84_edge']:.0f}] (version-2 floors: B50 {r2['B50']:.0f}); class limit 300")

    # ================================================================================================================ [11]
    P('\n[11] v4  PROJECTION AGAINST THE APPROVED FIGURES  (approved 4,609; stop-and-ask 5,992; toy line of the approved figure 183 CPU-h)')
    extra = dict(pilot_overrun=pil - 54.5, multijet_loose=1e6 * 0.100 / 3600 - 12.5, b6c=25.0 * (0.127 / 0.045) - 25.0, new_4a=O['NEW_4A_CPU_H'])
    ex = sum(extra.values())
    P('  extra lines: ' + ', '.join(f'{k} {v:+.1f}' for k, v in extra.items()) + f"; sum {ex:+.1f} CPU-h  (version 3: +181.9; the difference is the pilot)")
    U_ = O['TOY_UNITS']
    P(f"  toy programme: {U_} units of 1000 + 1000 toys (TOY_COST section 6; 182.3 CPU-h at the 652 s of STR)")
    proj = {}
    P('  PLANNING CASE: jax backend, scipy SLSQP with autodiff, merged layout, POI stitched, warm starts  [V per unit on a SYNTHETIC workspace, schrodinger; to be re-measured on the first real v2 workspace]')
    for n, sec in O['TOY_S_JAX'].items():
        th = U_ * sec / 3600.0
        lo, hi = th / O['TOY_FACTOR'], th * O['TOY_FACTOR']
        tot = 4609.0 - 183.0 + th + ex
        proj[n] = tot
        P(f"    {n:3d} parameters: {sec:6.1f} s per unit -> toys {th:5.1f} CPU-h (x/ {O['TOY_FACTOR']}: {lo:.0f}-{hi:.0f}) against 183; TOTAL {tot:.0f} ({4609.0 - 183.0 + lo + ex:.0f}-{4609.0 - 183.0 + hi + ex:.0f})"
          f" -> {'ABOVE' if 4609.0 - 183.0 + hi + ex > 5992 else 'below'} 5,992 over the whole band; conditional all-exact draw {O['TOY_ALL_EXACT_UNITS'] * sec / 3600:.0f} CPU-h (STR: 236 at 652 s)")
    P('  OLD BACKEND (numpy + scipy, finite-difference gradients), kept for the record:')
    for lab, tab in (("landau, version 3's inputs [V: p2-c-t-pyhf]", O['TOY_S_NUMPY_LANDAU']), ('schrodinger [V: p2-c-toy-base]', O['TOY_S_NUMPY_SCHRODINGER'])):
        P(f"    {lab}: " + '; '.join(f"{n} par: toys {U_ * sec / 3600:.0f} CPU-h, TOTAL {4609.0 - 183.0 + U_ * sec / 3600 + ex:.0f} ({'ABOVE' if 4609.0 - 183.0 + U_ * sec / 3600 + ex > 5992 else 'below'})" for n, sec in tab.items()))
    P("    as printed in version 3 (183 x s / 652, extras +181.9): 4,787 / 7,710 / 9,604 / 18,246 at 31 / 60 / 80 / 100 parameters")
    P(f"  break-even of the toy line with 183 CPU-h: about 93 parameters [E: TOY_COST section 1]; total projection at 60 / 80 / 100 parameters: {proj[60]:.0f} / {proj[80]:.0f} / {proj[100]:.0f},"
      f" i.e. {proj[60] - 4609:+.0f} / {proj[80] - 4609:+.0f} / {proj[100] - 4609:+.0f} against the approved 4,609 and {5992 - proj[100]:.0f} or more below 5,992")

    # ================================================================================================================ [12]
    P('\n[12] B-3  THE Q2 (c) TABLE AND THE (alpha1), (gamma) ROWS ON THE NEW BASIS  (R09 pile-up estimate; 2e4 draws per median as in the strategy; ESTIMATE, v1 placeholder inputs)')
    ALPHA = NS['ALPHA']; T1 = NS['D15_T1']; DG = NS['D15_G']
    sc = kk(v1r) / fro['DIF']
    P(f"  (alpha1) decays in flight after CKF from v1's counts: {ALPHA[(T1[0], False)][0]:.0f} / {ALPHA[(T1[1], False)][0]:.0f} events (fall x339 / x201) on the frozen N_t;"
      f" x{sc:.3f} for the first-arc N_t inside v1's own definition: {ALPHA[(T1[0], False)][0] * sc:.0f} / {ALPHA[(T1[1], False)][0] * sc:.0f}; the other classes have no v1 count")
    nd = O['ND_GRID']
    kap = dict(draft)
    zs = [0.0] * nd
    for i, (lab_, k) in enumerate(draft):
        if lab_ not in ('DIF', 'Z'):
            zs = [a + k * b for a, b in zip(zs, estream(f't{i}')[:nd])]
    pu = pustream(R.PU9)[:nd]
    base = [a + b for a, b in zip(zs, pu)]

    def b50c(md, mz, seed=5):
        rnd = random.Random(seed)
        v = [a + kap['DIF'] * rnd.gammavariate(md + 1, 1.0) + kap['Z'] * rnd.gammavariate(mz + 1, 1.0) for a in base]
        return quant(v, 0.5)

    def need(dsize, g):
        md = dsize / kap['DIF']
        if b50c(md, 0.0) > 300:
            return None
        lo, hi = 1.0, 1e5
        for _ in range(16):
            mid = math.sqrt(lo * hi)
            if b50c(md, g / mid / kap['Z']) > 300:
                lo = mid
            else:
                hi = mid
        return math.ceil(hi)
    e0 = b50c(0.0, 0.0)
    P(f"  basis: the DRAFT reading (seven terms, proposed sizes, H1): per count DIF {kap['DIF']:.1f}, Z {kap['Z']:.2f}; empty reading on these 2e4 draws {e0:.0f} (frozen basis: 76; room below 300: {300 - e0:.0f} against 224)")
    for scl, sl in ((1.0, "decays in flight at v1's size (frozen N_t)"), (sc, f"decays in flight x{sc:.2f} (first-arc Geant4 N_t)")):
        P(f"  -- {sl} --")
        for fd, fl in ((0.0, '0 (pilot count zero)'), (0.25, '1/4'), (math.exp(-1), 'e^-1'), (1.0, "1 (v1's central size)")):
            bb = [b50c(ALPHA[(t, False)][0] * fd * scl / kap['DIF'], 0.0) for t in T1]
            cells = []
            for gl, g in DG:
                nn = [need(ALPHA[(t, False)][0] * fd * scl, g) for t in T1]
                cells.append(f'{gl}: ' + ' / '.join('none suffices' if x is None else f'x{x:d} ({1 - 1 / x:.1%})' for x in nn))
            P(f"  |   f_D = {fl} | B50 with the conversions removed {bb[0]:.0f} / {bb[1]:.0f} | " + '; '.join(cells) + ' |')
    own = [need(0.0, NS['G_A1P'] / (1 - e)) for e in (0.8, 0.98)]
    P(f"  |   without an S_CKF estimate (own hits; eps_pair 0.8 / 0.98, assumed): f_D = 0: " + ' / '.join('none suffices' if x is None else f'x{x:d}' for x in own) + ' at 0.379 |')
    cr = [b50c(ALPHA[(t, True)][0] / kap['DIF'], ALPHA[(t, True)][1] / kap['Z']) for t in T1]
    P(f"  | (c) only: (alpha1) with fit-probability credit 2/35 on decays in flight and conversions, x339 / x201 | {cr[0]:.0f} / {cr[1]:.0f} | (frozen basis 109 / 130)")
    MZp = NS['MZ']
    P(f"  (gamma) row: m_H = 10 / 30 / 60 / 100 pool-equivalent counts of the frozen pool ({MZp:.3g} Z(nunu) events) = full-weight pilot counts "
      + ' / '.join(f'{mh * mf / MZp:.2f}' for mh in (10, 30, 60, 100)) + ' -> B50 ' + ' / '.join(f'{b50c(0.0, mh * mf / MZp):.0f}' for mh in (10, 30, 60, 100))
      + '  (frozen: m_Z 2.1 / 6.3 / 12.6 / 20.9 -> 117 / 195 / 309 / 462)')
    kd = kap['DIF']
    P(f"  expected pilot counts in the expected branch (alpha1') at eps_pair 0.8, frozen 'm_Z 1632, m_D 30-50': full-weight Z counts {NS['D15_ZCONV'] / 0.2 / (NZ / mf):.0f},"
      f" DIF-sample counts {ALPHA[(T1[0], False)][0] / 0.2 / kd:.0f}-{ALPHA[(T1[1], False)][0] / 0.2 / kd:.0f}: the pause stays the expected branch by a wide margin")

    # ================================================================================================================ [13]
    P('\n[13] SUMMARY NUMBERS FOR THE USER TABLE (version-3 lines; the rule-1, pool and reach numbers are UNCHANGED in version 4: none of their inputs changed)')
    d = res['draft']; h3 = res['7_S2_H3']; f0 = res['frozen']

    def cx(r, name):
        return ' / '.join('-'.join(str(m) for m in sorted({c[0] for c in r[pl]['cross'][name]})) for pl, _ in PUS)
    P(f"  B1 vertices behind the terms: frozen {sum(fro.values()):.3g} (4 terms); v3 {sum(NT.values()):.3g} (7 terms; of which hard-scatter share {NT_HS:.2g})")
    P(f"  per count: DIF frozen {NS['D15_KD']:.1f} -> {kap['DIF']:.1f}; DIFC {kap['DIFC']:.1f}; NI22/30/61 {kap['NI22']:.1f} / {kap['NI30']:.1f} / {kap['NI61']:.1f}; NIX {kap['NIX']:.1f}; NIC {kap['NIC']:.1f}; HS {kap['HS']:.1f}; Z {kap['Z']:.1f}; Zlow {kap['Zlow']:.1f}")
    P(f"  empty pilot R09: frozen {f0['R09']['empty']:.0f}; v2 (H3) {h3['R09']['empty']:.0f}; v3 draft {d['R09']['empty']:.0f}.  R08 88/118/148: frozen "
      + ' / '.join(f"{f0[pl]['empty']:.0f}" for pl, _ in PUS[1:]) + '; v2 ' + ' / '.join(f"{h3[pl]['empty']:.0f}" for pl, _ in PUS[1:]) + '; v3 draft ' + ' / '.join(f"{d[pl]['empty']:.0f}" for pl, _ in PUS[1:]))
    P(f"  pause at Z(nunu) counts (R09 / R08 88 / 118 / 148): frozen {cx(f0, 'Z')}; v2 {cx(h3, 'Z')}; v3 draft {cx(d, 'Z')}")
    P(f"  pause at counts in one large B1 sample: frozen DIF {cx(f0, 'DIF')}; v2 {cx(h3, LARGE)}; v3 draft {cx(d, LARGE)}; in the hard-scatter sample {cx(d, 'HS')}")
    P(f"  number of terms, empty pilot R09 (hard-scatter parents not read): seven {h3['R09']['empty']:.0f}; four {res['4_S2']['R09']['empty']:.0f}; three {res['3']['R09']['empty']:.0f}; one {res['1']['R09']['empty']:.0f};"
      f" with H1 as one more term: {d['R09']['empty']:.0f} / {res['4_H1']['R09']['empty']:.0f} / {res['3_H1']['R09']['empty']:.0f} / {res['1_H1']['R09']['empty']:.0f}")
    P(f"  v4: pilot {pil:.0f} CPU-h, {cost['proposed sizes']['gb']:.0f} GB (version 3: 135 CPU-h, 156 GB); pool floor sums as timed / both: seven {sums['as timed'][1]:.0f} / {sums['both'][1]:.0f}, four {sums['as timed'][2]:.0f} / {sums['both'][2]:.0f}")
    v3l = 'seven classes, shared pass, + low-weight classes (C-10)  ** version 3 **'
    P(f"  reach, every ceiling empty, R09-like: frozen {r0['reach_median']:.0f} [{r0['reach_84_edge']:.0f}]; v3 as timed {rr[('as timed', v3l)]['reach_median']:.0f} [{rr[('as timed', v3l)]['reach_84_edge']:.0f}],"
      f" both measures {rr[('both', v3l)]['reach_median']:.0f} [{rr[('both', v3l)]['reach_84_edge']:.0f}]; four terms {rr[('as timed', 'four terms (lenient)')]['reach_median']:.0f}"
      f" [{rr[('as timed', 'four terms (lenient)')]['reach_84_edge']:.0f}] / {rr[('both', 'four terms (lenient)')]['reach_median']:.0f} [{rr[('both', 'four terms (lenient)')]['reach_84_edge']:.0f}]")
    P('  day 5 of the calendar is 2026-11-21 (day 0 = 2026-11-16, COMMITMENTS l.49-50)')

    # ================================================================================================================ [14]
    P('\n[14] v4 [a]  A-1 SETTLED: PARENT TRUNCATION AND OPTION (a)  [V: p2-c-px-val2-0.json (campaign p2-c-px-tr, 2,000 events per file) and p2-c-px-val3-0.json (campaign p2-c-px-hy)]')
    P('  measure: Geant4 crossings of a barrel counting surface by the parent before its vertex, WITH MULTIPLICITY, all events with a charged parent (fields a1_*);')
    P("  'once per surface' is the measure of the second review on the first 100 events (fields ab_*); criterion: without a hit <= 2 % on the first measure")
    v2j, v3j = jload('p2-c-px-val2', '000', 'p2-c-px-val2-0.json'), jload('p2-c-px-val3', '000', 'p2-c-px-val3-0.json')
    for lab, js in (('p2-c-px-tr', v2j), ('p2-c-px-hy', v3j)):
        if js is None:
            P(f'  {lab}: validation JSON NOT FOUND'); continue
        for f in js['files']:
            nm = f['file'].split('/')[-1].replace('.npz', '')
            tot = f['a1_both'] + f['a1_g4_without_fatras']
            other = [k for k in ('v41_pass', 'offsets_ok', 'seeds_distinct', 'content_hash_recomputed_equal', 'class_recomputed_equal', 'parent_in_phase_space') if f.get(k) is False]
            P(f"    {nm:26s} mode {f.get('trunc_mode', '?'):7s} G4 crossings {tot:6d}: without a parent hit {f['a1_g4_without_fatras']:6d} = {100 * f['a1_g4_without_fatras'] / tot if tot else 0:6.2f} %;"
              f" parent hits without a G4 crossing {f['a1_fatras_without_g4']:5d} = {100 * f['a1_fatras_without_g4'] / max(f['a1_both'] + f['a1_fatras_without_g4'], 1):5.2f} %;"
              f" once per surface (100 events): only G4 {f['ab_only_geant4']:4d} of {f['ab_only_geant4'] + f['ab_surfaces_both']:5d};"
              f" later than the vertex time {f['parent_hits_later_than_vertex_time']:4d}; beyond the vertex radius {f['parent_hits_beyond_vertex_radius']:6d};"
              f" V4-1 {f['v41_pass']}; NaN {f['nan_hits']}; product hits before the vertex {f['product_hits_earlier_than_vertex']}; a1_ok {f.get('a1_ok')};"
              f" validator flag hard {f.get('hard')}" + (f"; OTHER CHECKS FALSE: {other}" if other else ''))
        P(f"    {lab}: all_hard_checks_pass = {js['all_hard_checks_pass']}; reruns identical = {js.get('all_reruns_identical')} ({js.get('reproducible_pairs')} pairs)")
    P("  NOTE: for files with turned parents the validator's flag 'hard' is False under option (a) because of its check 'no parent hit beyond the vertex radius' (see the counts above):")
    P("        that check does not apply to a parent that has turned; p2x_validate.py must make it class-aware before 'one validated job per stream' can read all-pass for DIF-C, NI-C, hs, lowpt")

    # ================================================================================================================ [15]
    P('\n[15] v4 [b]  THE HALF-TURN LIMIT  [V: p2-c-px-htg-{znn,mb}.json (2,000 Z(nunu) events, 20,000 minimum-bias interactions), p2-c-px-a1e-0.json]')
    HT = {}
    for k in ('znn', 'mb'):
        d = jload('p2-c-px-htg', '000', f'p2-c-px-htg-{k}.json')
        HT[k] = d
        if d is None:
            P(f'  {k}: JSON NOT FOUND'); continue
        bl = d['by_layer']
        el = d['end_of_central_loopers']
        P(f"  {k}: {d['n_events']} events; charged particles given to Fatras {d['charged_per_event']:.1f} per event, central {d['charged_central_per_event']:.1f}, central with pT < 0.63 GeV {d['charged_central_pt_below_0p63_per_event']:.1f}"
          f" ({d['frac_central_charged_that_can_loop_inside_barrel']:.0%});")
        P(f"      written hits on counting surfaces {d['written_hits_counting_per_event']:.0f} per event; Geant4 crossings of the same particles {d['g4_crossings_per_event']:.0f}, of which after half a turn"
          f" {d['g4_crossings_beyond_half_turn_per_event']:.1f} ({d['beyond_half_turn_fraction_of_g4_crossings']:.1%}); Geant4 crossings WITHOUT a simulated hit {d['g4_crossings_without_fatras_hit_per_event']:.1f}"
          f" = {d['missing_relative_to_written_hits']:.1%} of the written hits; hits without a Geant4 crossing {d['fatras_hits_without_g4_crossing_per_event']:.1f}")
        P('      by layer, crossings without a hit / hits of generation 0: ' + ', '.join(f"{n} {m / f:.0%}" for n, m, f in zip(d['layers'], bl['missing'], bl['fatras_gen0'])))
        P(f"      central particles with pT < 0.63 GeV in Geant4: {el['n']}; ended before half a turn {el['ended_before_half_turn'] / el['n']:.1%}, between half and one {el['ended_between_half_and_one_turn'] / el['n']:.1%},"
          f" alive after one turn {el['ended_after_one_turn'] / el['n']:.1%}; WITHOUT A GEANT4 RECORD {el['no_g4_record']} = {el['no_g4_record'] / el['n']:.2%}"
          f" (tracks ended by transportation only, multi-turn loopers: LOOPER_GUN addendum 17:20) -> the missing-crossing numbers above are LOW by up to that share of the particles")
    if HT['mb']:
        d = HT['mb']
        P(f"  x 200 interactions (one pile-up crossing) [E]: written {200 * d['written_hits_counting_per_event']:.3g}, Geant4 crossings {200 * d['g4_crossings_per_event']:.3g}, without a hit {200 * d['g4_crossings_without_fatras_hit_per_event']:.3g}")
    a1e = jload('p2-c-px-a1e', '000', 'p2-c-px-a1e-0.json')
    if a1e:
        a = a1e[0]
        ed, hb = a['turn_edges'], a['hits_by_turn']
        beyond = sum(h for e, h in zip(ed, hb) if e >= 0.5)
        P(f"  hits of generated charged particles by turn in {a['n_events']} Z(nunu) slice events [V: p2-c-px-a1e]: total {sum(hb):.4g}; beyond 0.5 turn {beyond:.0f} = {beyond / sum(hb):.4%}; the last bin below 0.5 (0.45-0.5) holds {hb[3]:.0f}")
    P('  v1 top-up [U: TT/acts/stage4/plan.md l.303-310]: (ratio - 1) x the event\'s own Fatras crossings per layer, z resampled from the layer, phi uniform, ratio 2.3-7.3 to the TDR occupancy:')
    P('      it restores the NUMBER of hits per layer; the added crossings are independent in phi, so the correlation of successive arcs of one particle is not restored (a looper-pair variant exists as a variation only)')

    # ================================================================================================================ [16]
    lp_new = jload('p2-c-px-lpds', '000', 'p2-c-px-lpds-0.json')
    lp = lp_new or jload('p2-c-px-lps', '000', 'p2-c-px-lps-0.json')
    lp_tag = ('RERUN p2-c-px-lpd (records of transportation-ended tracks included) [V: p2-c-px-lpds-0.json]' if lp_new else
              'FIRST RUN p2-c-px-lp: PROVISIONAL (0.9 % of events missing, rerun p2-c-px-lpd pending) [V: p2-c-px-lps-0.json]')
    P(f'\n[16] v4 [c]  THE LOOPER GUN  -- {lp_tag}')
    nl = {}
    for s_ in ('nat', 'flat'):
        if not lp or s_ not in lp:
            P(f'  {s_}: NOT FOUND'); continue
        fn, pa = lp[s_]['funnel'], lp[s_]['particles']
        norec = pa['end_process'].get('none', 0)
        nl[s_] = fn['events']
        P(f"  set {s_}: generated {fn['events']}; fewer than 3 pool hits {fn['fewer_than_3_pool_hits']}; finder run {fn['finder_run']}; with a seed triple {fn['with_seed_Tseed']}; with seed score >= T_seed {fn['with_refit']};"
          f" with a candidate after the refit {fn['with_kept_candidate_NL2ge4']}; events passing any rung {sum(lp[s_]['events_passing_rung'].values())};"
          f" finder {json.dumps(lp[s_]['finder_cfg'])}; without a Geant4 record {norec} ({norec / fn['events']:.2%}); crossings per event {lp[s_]['crossings']['counting_per_event']:.1f},"
          f" after half a turn {lp[s_]['crossings']['counting_after_half_turn_per_event']:.1f}")
    lpm = (lp or {}).get('nat', {}).get('chain_meta', {}).get('loopers_prompt_central_per_mb_interaction', 7.29955)
    fr = 0.2 / (2 * math.pi)
    nt_lp = NTRIG * 200 * lpm * fr
    M_lp = 1.0e5
    P(f"  what the zero bounds [E]: prompt charged particles with |eta| < 1, pT < 0.63 GeV: {lpm:.2f} per minimum-bias interaction [V: 145,991 in 20,000, p2-c-px-ht-mb]; started within +-0.1 of the road axis: {fr:.4f};"
      f" N_t = N_trig x 200 x {lpm:.2f} x {fr:.4f} = {nt_lp:.3g} in 3 ab^-1; one count in {M_lp:.0g} events = {nt_lp / M_lp:.3g} events; a zero allows {U68 * nt_lp / M_lp:.3g} at 68 %"
      f" (both sets as one sample of 2e5, different spectra: {U68 * nt_lp / 2e5:.3g}); for a zero to allow 25 events: M = {U68 * nt_lp / 25:.2g} gun events = {U68 * nt_lp / 25 * 0.011 / 3600:.0f} CPU-h at 11 ms")
    if HT['znn']:
        hsl = HT['znn']['charged_central_pt_below_0p63_per_event'] * fr
        nt_hl = NTRIG * hsl
        P(f"  the same gun read for the HARD-SCATTER event's own loopers [E; gun spectrum = minimum bias, hard-scatter rate of Z(nunu) used for all SM processes]: {HT['znn']['charged_central_pt_below_0p63_per_event']:.1f} per event x {fr:.4f}"
          f" = {hsl:.3f} per triggered event, N_t {nt_hl:.3g}; one count in 1e5 = {nt_hl / 1e5:.0f} events; a zero allows {U68 * nt_hl / 1e5:.0f} at 68 % (limit 300)")
    P('  NOT covered by the gun: loopers starting outside +-0.1 of the road axis (97 % of them), |eta| > 1, displaced loopers, products of the looper\'s decay or interaction, the dE/dx rungs, and')
    P('      a looper TOGETHER WITH OTHER PARTICLES (pile-up, or the rest of the hard-scatter event): none of these is bounded by the zero')

    # ================================================================================================================ [17]
    P('\n[17] v4 [d]  PROPOSED EIGHTH B6 ROW (for the user to accept or decline): pile-up with the later arcs restored against the same events on the present chain')
    rate = O['PU_RATE_PER_TRIAL']
    ch_mb = HT['mb']['charged_per_event'] if HT['mb'] else 52.6
    g4_meas = HT['mb']['g4_ms_per_particle'] if HT['mb'] else float('nan')
    g4_s = 200 * ch_mb * O['G4_MS_PER_FIRING_PIK'] * 1e-3
    nom_s = O['PU_CHAIN_S'] + O['PU_TRIALS'] * O['PU_FINDER_S']
    P(f"  unit costs: nominal rho = 1 event = chain {O['PU_CHAIN_S']} s + {O['PU_TRIALS']} trials x {O['PU_FINDER_S']} s = {nom_s:.1f} s (measured whole event 57-59 s);"
      f" Geant4 for the arcs: 200 x {ch_mb:.1f} charged particles x {O['G4_MS_PER_FIRING_PIK']} ms = {g4_s:.1f} s per crossing ({200 * ch_mb * g4_meas * 1e-3:.1f} s at the {g4_meas:.3f} ms per particle measured in p2-c-px-htg-mb)")
    P('  sample size: criterion B6-a = statistical error on ln(B_var / B_nom) < 0.1 at R06.  Poisson counts at the v1 direct rates per trial (LOWER bound on the error: candidates of one event are correlated; the bootstrap over events decides):')
    need = 2.0 / 0.1 ** 2
    for r_, x in rate.items():
        P(f"    {r_}: {x:.4g} per trial; unpaired error 0.1 needs {need:.0f} counts per sample = {need / x:.3g} trials = {need / x / O['PU_TRIALS']:.3g} events;"
          + ' '.join(f" at {n} events: {n * O['PU_TRIALS'] * x:.3g} counts, error {math.sqrt(2.0 / (n * O['PU_TRIALS'] * x)):.3f};" for n in O['ROB_EVENTS']))
    P('    -> R04-R06 evaluable at 600 events (the size of every other reduced B6 background row, STR l.1513), R07 not; the design is paired (same events and seeds), so 0.1 is an upper value')
    for n in O['ROB_EVENTS']:
        cells = []
        tot = {}
        for h in O['ROB_HITS']:
            for p_ in ((1,) if h == 1.0 else (1, 2)):
                ev = g4_s + O['PU_CHAIN_S'] * h + O['PU_TRIALS'] * O['PU_FINDER_S'] * h ** p_
                tot[(h, p_)] = n * ev / 3600
                cells.append(f"hits x{h}" + (f", finder ~ hits^{p_}" if h != 1.0 else '') + f": {ev:.0f} s per event, {n * ev / 3600:.1f} CPU-h")
        partner = n * nom_s / 3600
        lo, hi = min(tot.values()), max(tot.values())
        P(f"  {n} events: varied sample " + '; '.join(cells) + f"; nominal partner (same events, present chain) {partner:.1f} CPU-h; slice and validation {O['ROB_SLICE_CPU_H']:.0f} CPU-h [E]"
          f" -> TOTAL {lo + partner + O['ROB_SLICE_CPU_H']:.0f}-{hi + partner + O['ROB_SLICE_CPU_H']:.0f} CPU-h  ({lo + O['ROB_SLICE_CPU_H']:.0f}-{hi + O['ROB_SLICE_CPU_H']:.0f} if the nominal partner is an existing B6 / development sample of the same events)")
        if n == O['ROB_EVENTS'][0]:
            rob_lo, rob_hi = lo + partner + O['ROB_SLICE_CPU_H'], hi + partner + O['ROB_SLICE_CPU_H']
    sig = 4 * 300
    P(f"  optional signal arm (B6 signal column, read only after the closure verdicts): {sig} rows x ({O['SIG_ROW_S']} s x 1.0-1.3 + {g4_s:.1f} s) = {sig * (O['SIG_ROW_S'] + g4_s) / 3600:.0f}-{sig * (O['SIG_ROW_S'] * 1.3 + g4_s) / 3600:.0f} CPU-h [E; nominal partners are B6's]")
    P(f"  projection with the test accepted (600 events, own partner): 60 / 80 / 100 parameters {proj[60] + rob_hi:.0f} / {proj[80] + rob_hi:.0f} / {proj[100] + rob_hi:.0f} CPU-h at the upper cost: below 5,992")
    P('  what a shift of the pile-up term would do to rule 1 (DRAFT terms, empty pilot; pile-up median x f, same width and cap; the frozen rule reads the present chain, f = 1):')
    zd = zero_sum(draft)
    for f in (1.0, 1.1, 1.25, 1.5, 2.0):
        vals = []
        for pl, pu in PUS:
            b = [a + c for a, c in zip(zd, pustream((pu[0] * f, pu[1], pu[2])))]
            vals.append(quant(b, 0.5))
        P(f"    f = {f:4.2f} (ln f = {math.log(f):.2f}): R09 {vals[0]:.0f}; R08 at 88 / 118 / 148: {vals[1]:.0f} / {vals[2]:.0f} / {vals[3]:.0f}" + ('   <- the B6-b "robust" boundary, ln 2' if f == 2.0 else ''))

    # ================================================================================================================ [18]
    P('\n[18] v4  SUMMARY OF WHAT CHANGED AGAINST VERSION 3 (numbers for the user table)')
    P(f"  UNCHANGED: every rule-1 reading and crossing ([4]: draft {res['draft']['R09']['empty']:.0f}; R08 " + ' / '.join(f"{res['draft'][pl]['empty']:.0f}" for pl, _ in PUS[1:])
      + f"), N_t and events per count ([1]-[3]), families ([5]), pool table ([9]: {sums['as timed'][1]:.0f} as timed, {sums['both'][1]:.0f} both), reach ([10]), Q2 (c) grid ([12])")
    P(f"  pilot: {pil:.1f} CPU-h (v3 134.5), of which part 1 launched {cp['part1']:.1f} (v3 91.1) and B1 part {cp['b1_part']:.1f} (v3 43.4); storage {cp['gb']:.0f} GB (v3 156), part 1 {cp['gb_z'] + O['PILOT_MB_GB']:.0f} GB")
    P(f"  projection: {proj[60]:.0f} / {proj[80]:.0f} / {proj[100]:.0f} CPU-h at 60 / 80 / 100 parameters with the jax configuration (v3: 7,710 / 9,604 / 18,246 with the old backend)")
    P(f"  proposed robustness test: {rob_lo:.0f}-{rob_hi:.0f} CPU-h at 600 events with its own nominal partner")


if __name__ == '__main__':
    main()
