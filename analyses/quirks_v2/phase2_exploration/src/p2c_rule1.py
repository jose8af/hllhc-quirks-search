"""p2c_rule1.py -- rule-1 readings (STR §11.7), pool and toy projections with the Phase-2 measured costs.  ESTIMATE.

  python3 p2c_rule1.py <out.json> [costs.json]

Uses `strategy_budget_copy.py`, a byte-identical COPY of phase1_strategy/src/strategy_budget.py (sha256 recorded),
executed in a private namespace with its printing discarded; its constants (NTRIG, RATE, SM_NTRIG, MJ_PLAN, NZ, PU9,
pu8, PU_CAP), its `allocate` and the generator of its `d15_q` are used unchanged.  The Phase-1 script and its stdout
are not touched.  costs.json (optional): {"process": seconds per event} overriding MEASURED below ("after step 1").
"""
import contextlib
import hashlib
import io
import json
import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
COPY = HERE / 'strategy_budget_copy.py'
NS = {'__name__': 'strategy_budget_copy'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(COPY.read_text(), str(COPY), 'exec'), NS)
NTRIG, RATE, SM, MJ, NZ, PU9, PU_CAP = NS['NTRIG'], NS['RATE'], NS['SM_NTRIG'], NS['MJ_PLAN'], NS['NZ'], NS['PU9'], NS['PU_CAP']
PU8 = (NS['pu8'], 0.43, PU_CAP)          # R08-like row of Table 4.4c: EST median, s_tot 0.43 (STR §4.0 pt 7)
NI = ("NI 22 mm", "NI 30 mm", "NI 61.5 mm")
ND = 20000


def b50(gam, pu, seed=7):
    """median of sum kappa Gamma(m+1) + censored pile-up term: the generator of d15_q, with the pile-up term as argument."""
    rnd = random.Random(seed); bs = []
    for _ in range(ND):
        b = sum(k * rnd.gammavariate(m + 1, 1.0) for k, m in gam)
        x = pu[0] * math.exp(pu[1] * rnd.gauss(0, 1))
        bs.append(b + min(x, -pu[2] * rnd.expovariate(1.0)))
    bs.sort()
    return bs[ND // 2]


def reading(k_d, k_ni, k_sm, pu):
    def g(mz=0, md=0):
        return [(k_d, md)] + [(k, 0) for k in k_ni] + [(k_sm, mz)]
    zero = b50(g(), pu)

    def cross(which):
        for m in range(0, 400):
            if b50(g(**{which: m}), pu) > 300:
                return m
        return None
    return dict(b50_all_zero=round(zero, 1), first_mZ_above_300=cross('mz'), first_mD_above_300=cross('md'))


def main(out, costs_file=None):
    res = dict(copy_sha256=hashlib.sha256(COPY.read_bytes()).hexdigest(), tag='ESTIMATE', pu9=PU9[0], pu8=PU8[0])
    sm_tot = sum(SM.values()) + MJ
    kd0 = NTRIG * RATE['DIF'] / 1e6
    kni0 = [NTRIG * RATE[t] / 1e6 for t in NI]
    F = 0.397                                   # mean v1 preselection weight of filter-level Z(nunu) events (200 events)
    zopts = {'STR (2.3e6 preselected events)': 2.3e6, '(a) 29 CPU-h: 0.83e6 filter-level': 0.83e6 * F,
             '(b) 2.3e6 filter-level': 2.3e6 * F, '(c) 2.3e6 preselected-equivalent': 2.3e6}
    res['Z_options'] = {}
    for lab, meff in zopts.items():
        r = dict(M_eff=meff, events_per_count_all_SM=sm_tot / meff, events_per_count_Z_alone=NZ / meff)
        for pl, pu in (('R09', PU9), ('R08', PU8)):
            r[pl] = reading(kd0, kni0, sm_tot / meff, pu)
        res['Z_options'][lab] = r
    kb = sm_tot / (2.3e6 * F)
    res['DIF_NI_options_with_Z_option_b'] = {}
    for lab, kd, kni in (('STR numbers (DIF 65.1; NI with 0.22)', kd0, kni0),
                         ('O12 (a) every Geant4 decay: N_t x 2.59 (yield ratio 0.0913 / 0.0353)', kd0 * 2.59, kni0),
                         ('O3 (a) NI without the 0.22 factor', kd0, [k / 0.22 for k in kni0]),
                         ('O1 (b) lower bound: no road cut only (x 2 pi / 0.30)', kd0 * 20.94, [k * 20.94 for k in kni0])):
        r = dict(events_per_DIF_count=kd, events_per_NI_count=kni)
        for pl, pu in (('R09', PU9), ('R08', PU8)):
            r[pl] = reading(kd, kni, kb, pu)
        res['DIF_NI_options_with_Z_option_b'][lab] = r
    # ---- pool projection (Table 4.4a) with measured costs
    meas = {"DIF": 0.0037 + 0.000408 / 0.0353, "NI 22 mm": 0.0038 + 0.0000469 / 0.0063, "NI 30 mm": 0.0059 + 0.0000469 / 0.0063,
            "NI 61.5 mm": 0.0059 + 0.0000469 / 0.0063}
    prov = {t: 'V (p2-c-t-b1x, p2-c-t-g4x)' for t in meas}
    for p in SM:
        if p.startswith('Z'):
            meas[p], prov[p] = 0.127, 'V (p2-c-t-hs0)' if 'nunu' in p else 'E (Z(nunu) cost)'
        elif p.startswith('tt 1l'):
            meas[p], prov[p] = 0.571, 'V (p2-c-t-hs0)'
        elif p.startswith(('tt', 'tW', 't-')) or p.startswith('t '):
            meas[p], prov[p] = 0.571, 'E (tt 1l cost)'
        else:
            meas[p], prov[p] = 0.171, 'E (W(tau nu) cost)'
    after = dict(meas)
    if costs_file:
        after.update(json.loads(Path(costs_file).read_text()))
    terms = NS['terms']; alloc = NS['allocate']; H = NS['H']; U68 = NS['U68']; cpool = NS['C_POOL']
    plan = alloc(cpool)
    rows = []
    for t, n, c in terms:
        rows.append(dict(term=t, N_t=n, M_planned=plan[t], cost_STR_s=c, cpu_h_STR=plan[t] * c / H, cost_measured_s=meas[t],
                         provenance=prov[t], cpu_h_measured=plan[t] * meas[t] / H, cost_after_step1_s=after[t],
                         cpu_h_after_step1=plan[t] * after[t] / H, floor_planned=U68 * n / plan[t]))
    res['pool_rows'] = rows
    sm_names = set(SM)
    tot = lambda key, sel: sum(r[key] for r in rows if sel(r['term']))  # noqa: E731
    res['pool_totals'] = {k: dict(all=tot(k, lambda t: True), SM=tot(k, lambda t: t in sm_names), B1=tot(k, lambda t: t not in sm_names))
                          for k in ('cpu_h_STR', 'cpu_h_measured', 'cpu_h_after_step1', 'floor_planned')}
    for lab, cost in (('measured', meas), ('after_step1', after)):
        tt = [(t, n, cost[t]) for t, n, c in terms]
        al = alloc(cpool, tt=tt)
        res[f'fixed_cpu_{lab}'] = dict(pool_cpu_h=cpool, summed_floor=sum(U68 * n / al[t] for t, n, c in tt),
                                        floor_SM=sum(U68 * n / al[t] for t, n, c in tt if t in sm_names),
                                        M={t: al[t] for t, n, c in tt})
        # same floors as planned, M re-optimised for the new costs: CPU needed scales as (sum sqrt(N c))^2
        s_new = sum(math.sqrt(n * cost[t]) for t, n, c in terms); s_old = sum(math.sqrt(n * c) for t, n, c in terms)
        res[f'same_floor_reoptimised_{lab}_cpu_h'] = cpool * (s_new / s_old) ** 2
    # ---- user decision 2026-11-16: approved CPU kept, hard-scatter pool shrunk.  SM share fixed at its planned CPU-h
    # (Table 4.4a: 457), B1 share at its planned CPU-h, each re-allocated by the strategy's rule sqrt(N_t / c_t), G = 1.
    cpu_sm = res['pool_totals']['cpu_h_STR']['SM']; cpu_b1 = res['pool_totals']['cpu_h_STR']['B1']
    res['replacement_rows_4_4a'] = {}
    for lab, cost in (('measured', meas), ('after_step1', after)):
        out_rows = []
        for share, cpu, sel in (('SM', cpu_sm, lambda t: t in sm_names), ('B1', cpu_b1, lambda t: t not in sm_names)):
            tt = [(t, n, cost[t]) for t, n, c in terms if sel(t)]
            al = alloc(cpu, tt=tt)
            out_rows += [dict(term=t, share=share, N_t=n, cost_ms=1e3 * c, M_t=al[t], transfer=n / al[t], floor68=U68 * n / al[t],
                              cpu_h=al[t] * c / H, provenance=prov[t]) for t, n, c in tt]
        res['replacement_rows_4_4a'][lab] = dict(rows=out_rows, cpu_h_SM=cpu_sm, cpu_h_B1=cpu_b1,
                                                  floor_SM=sum(r['floor68'] for r in out_rows if r['share'] == 'SM'),
                                                  floor_B1=sum(r['floor68'] for r in out_rows if r['share'] == 'B1'),
                                                  M_SM=sum(r['M_t'] for r in out_rows if r['share'] == 'SM'))
    # ---- toys (STR §4.11 pt 5 and cost line): budget items at 652 s per 1000 + 1000 toys, scaled by the measured ratios
    toy_items = {'pass 1 (5 x 11 x 8)': 80.0, 'pass-1 exact check': 22.0, 'pass 2 (3 x 11 x 8)': 48.0, 'pass-2 exact check': 13.0,
                 'T1-c (iii) stored distributions': 20.0}
    ratio = {'31': 638 / 652.0, '60': 11052 / 652.0, '80': 17799 / 652.0, '100': 48589 / 652.0}
    res['toys'] = dict(items_cpu_h_STR=toy_items, sum_STR=sum(toy_items.values()),
                       sum_at_n_par={k: sum(toy_items.values()) * v for k, v in ratio.items()}, ratio_to_652s=ratio)
    Path(out).write_text(json.dumps(res, indent=1))
    sys.stderr.write(json.dumps({k: res[k] for k in ('Z_options', 'DIF_NI_options_with_Z_option_b', 'pool_totals', 'toys')}, indent=1)[:200] + '\n')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
