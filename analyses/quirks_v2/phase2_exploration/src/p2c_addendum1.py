"""p2c_addendum1.py -- tables of strategy addendum 1 (rule-1 basis, day-15 table, Table 4.4a rows).  ESTIMATE.

  /usr/bin/python3 -I p2c_addendum1.py <out.json>

Everything from the Phase-1 budget script comes through p2c_rule1 (byte-identical copy, executed unchanged).  The
changed inputs are the named OVERRIDES below, each with its Phase-2 source.
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import p2c_rule1 as R  # noqa: E402

NS = R.NS
NTRIG, RATE, SM, MJ, NZ = R.NTRIG, R.RATE, R.SM, R.MJ, R.NZ
U68, H, alloc = NS['U68'], NS['H'], NS['allocate']
OVERRIDES = dict(
    PILOT_HS_GENERATED=2.3e6,        # pilot size (b): filter-level events generated
    F_EFF_Z=0.440,                   # N_eff / N of the v1 preselection weight, 10,000 events [V: p2-c-t-hs0 *znn*]
    F_EFF_Z_ERR=0.005,               # statistical (mean weight 0.4308 +- 0.0049)
    F_EFF={'Z': 0.440, 'W': 0.268, 'tt': 0.125},      # [V: p2-c-t-hs0, 10,000 events each]; other processes by proxy [E]
    F_PASS={'Z': 0.442, 'W': 0.315, 'tt': 0.2105},    # fraction with non-zero weight [V: same]
    DIF_G4_OVER_V1=0.04548 / (0.00780 / 0.2047),      # first-arc Geant4 decays per parent / v1 formula [V: p2-c-t-g4-y0] = 1.19
    DIF_ALL_OVER_FIRST=45635 / 22742.0,               # every decay at 30 < r < 1000 mm / first arc [V: same] = 2.01
    NI_PV_LINE=0.22,                                  # removed under O3 (a)
    NI_ELSEWHERE_OVER_3R_FIRST=21599 / 4154.0,        # inelastic vertices elsewhere / at the three radii, first arc [V] = 5.20
    NI_ELSEWHERE_OVER_3R_ALL=33947 / 5150.0,          # the same with curling parents [V] = 6.59
    PILOT_B1=1e6,
    COST=dict(Z=(0.042, 0.085), W=(0.086, 0.085), tt=(0.460, 0.111), tt_forced=(0.199, 0.111)),   # (generation, chain) s [V: p2-c-t-hs0, p2-c-prof]
    COST_B1={'DIF': 0.0037 + 0.000408 / 0.04548, 'NI 22 mm': 0.0112, 'NI 30 mm': 0.0133, 'NI 61.5 mm': 0.0133,
             'NI elsewhere': 0.0059 + 0.000408 / (21599 / 5e5)},
)
O = OVERRIDES
NI = R.NI


def kind(p):
    return 'Z' if p.startswith('Z') else ('tt' if p.startswith(('tt', 'tW', 't-')) else 'W')


def read(k_d, k_ni, k_sm, k_x=None):
    """rule-1 reading for transfer factors: DIF, three NI radii, all SM through the Z count, optional NI-elsewhere term."""
    out = {}
    for pl, pu in (('R09', R.PU9), ('R08', R.PU8)):
        def g(mz=0, md=0, mx=0):
            return [(k_d, md)] + [(k, 0) for k in k_ni] + [(k_sm, mz)] + ([(k_x, mx)] if k_x else [])

        def cross(w):
            for m in range(0, 60):
                if R.b50(g(**{w: m}), pu) > 300:
                    return m
            return None
        out[pl] = dict(b50_all_zero=round(R.b50(g(), pu), 1), cross_mZ=cross('mz'), cross_mD=cross('md'),
                       cross_mX=cross('mx') if k_x else None)
    return out


def main(out):
    res = dict(overrides=O, copy_sha256=R.hashlib.sha256(R.COPY.read_bytes()).hexdigest(), tag='ESTIMATE')
    sm_tot = sum(SM.values()) + MJ
    kd_v1 = NTRIG * RATE['DIF'] / O['PILOT_B1']
    kni_v1 = [NTRIG * RATE[t] / O['PILOT_B1'] for t in NI]
    kni = [k / O['NI_PV_LINE'] for k in kni_v1]
    kd = kd_v1 * O['DIF_G4_OVER_V1']
    meff = O['PILOT_HS_GENERATED'] * O['F_EFF_Z']
    ksm = sm_tot / meff
    kx_first = sum(kni) * O['NI_ELSEWHERE_OVER_3R_FIRST']
    kx_all = sum(kni) * O['NI_ELSEWHERE_OVER_3R_ALL']
    basis = dict(DIF_v1=kd_v1, DIF_proposed=kd, NI_v1=kni_v1, NI_proposed=kni, SM_STR=sm_tot / 2.3e6, SM_proposed=ksm,
                 Z_alone_proposed=NZ / meff, NI_elsewhere_first_arc=kx_first, NI_elsewhere_all=kx_all,
                 N_t=dict(DIF_v1=NTRIG * RATE['DIF'], DIF_proposed=NTRIG * RATE['DIF'] * O['DIF_G4_OVER_V1'],
                          NI_proposed=[k * O['PILOT_B1'] for k in kni], NI_elsewhere_first_arc=kx_first * O['PILOT_B1'],
                          NI_elsewhere_all=kx_all * O['PILOT_B1']),
                 SM_per_count_at_f_eff_pm_err=[sm_tot / (O['PILOT_HS_GENERATED'] * (O['F_EFF_Z'] + s * O['F_EFF_Z_ERR']))
                                               for s in (-1, 0, 1)])
    res['basis'] = basis
    res['readings'] = {
        'STR as frozen (65.1; 0.88/1.12/1.12; 18.1)': read(kd_v1, kni_v1, sm_tot / 2.3e6),
        'PROPOSED, lenient O4 (NI elsewhere recorded, not a term)': read(kd, kni, ksm),
        'PROPOSED, strict O4 (NI elsewhere a term, first arc)': read(kd, kni, ksm, kx_first),
        'proposed but DIF N_t kept at v1 (65.1)': read(kd_v1, kni, ksm),
        'rejected O12 (a): every Geant4 decay': read(kd * O['DIF_ALL_OVER_FIRST'], kni, ksm),
        'rejected O3 (b): 0.22 kept': read(kd, kni_v1, ksm),
        'rejected O1 (b), lower bound (no road cut: x 20.94)': read(kd * 20.94, [k * 20.94 for k in kni], ksm),
        'rejected pilot size (a) 0.83e6 generated': read(kd, kni, sm_tot / (0.83e6 * O['F_EFF_Z'])),
        'rejected pilot size (c) 2.3e6 effective': read(kd, kni, sm_tot / 2.3e6),
        'strict O4 with curling parents (all)': read(kd, kni, ksm, kx_all),
    }
    # ---- Table 4.4a at fixed CPU: SM share 457 CPU-h, B1 share 208 CPU-h, rule sqrt(N_t / c_t), G = 1, in EFFECTIVE events
    terms = NS['terms']; plan = alloc(NS['C_POOL'])
    sm_names = set(SM)
    cpu_sm = sum(plan[t] * c / H for t, n, c in terms if t in sm_names)
    cpu_b1 = sum(plan[t] * c / H for t, n, c in terms if t not in sm_names)
    tabs = {}
    for lab, forced, presel_first in (('chain on every generated event, tt unforced', False, False),
                                      ('chain on every generated event, tt forced', True, False),
                                      ('generator-level preselection before the chain, tt unforced', False, True),
                                      ('generator-level preselection before the chain, tt forced', True, True)):
        tt = []
        for p, n in SM.items():
            k = kind(p)
            cg, cc = O['COST']['tt_forced' if (k == 'tt' and forced) else k]
            c_gen_event = cg + (O['F_PASS'][k] if presel_first else 1.0) * cc
            tt.append((p, n, c_gen_event / O['F_EFF'][k], c_gen_event, k))
        al = alloc(cpu_sm, tt=[(t, n, c) for t, n, c, _, _ in tt])
        rows = [dict(term=t, N_t=n, cost_per_generated_ms=1e3 * cge, cost_per_effective_ms=1e3 * c, M_eff=al[t],
                     M_generated=al[t] / O['F_EFF'][k], floor68=U68 * n / al[t], cpu_h=al[t] * c / H) for t, n, c, cge, k in tt]
        tabs[lab] = dict(rows=rows, floor_SM=sum(r['floor68'] for r in rows), cpu_h_SM=cpu_sm)
    res['table_4_4a_SM_effective'] = tabs
    b1 = {}
    for lab, with_x in (('lenient', False), ('strict', True)):
        nt = {'DIF': NTRIG * RATE['DIF'] * O['DIF_G4_OVER_V1']}
        nt.update({t: NTRIG * RATE[t] / O['NI_PV_LINE'] for t in NI})
        if with_x:
            nt['NI elsewhere'] = kx_first * O['PILOT_B1']
        tt = [(t, n, O['COST_B1'][t]) for t, n in nt.items()]
        al = alloc(cpu_b1, tt=tt)
        rows = [dict(term=t, N_t=n, cost_ms=1e3 * c, M_t=al[t], floor68=U68 * n / al[t], cpu_h=al[t] * c / H) for t, n, c in tt]
        b1[lab] = dict(rows=rows, floor_B1=sum(r['floor68'] for r in rows), cpu_h_B1=cpu_b1)
    res['table_4_4a_B1'] = b1
    Path(out).write_text(json.dumps(res, indent=1))


if __name__ == '__main__':
    main(sys.argv[1])
