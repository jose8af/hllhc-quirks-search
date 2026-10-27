"""normalise.py -- build the D1/D2/D3 normalisation inputs from the generator-level run (gen_d123.py nt) into
inputs/normalisation.json (FIXER R2; orchestrator/user decisions 2026-10-14).

    nice -n 15 pixi run python -m acts.stage4.analysis.normalise data/acts_stage4/analysis/d123/gen_d123.json

D1 (USER): N_trig = L x sum_p sigma_p K_p f_presel,p after the generator-level preselection (gen_d123.PROXIES).
  Processes: Z(nunu)+j, W(tau nu) as tau_l + tau_h (pooled), W(e nu), W(mu nu), tt 1l; N_trig-only: tt 2l, single
  top t-channel, WW, WZ, ZZ (generated), tW (flagged allowance), s-channel single top (negligible, not included).
D3 (REVIEW R2 A-1): sigma_p = sigma_gen x N_acc / (tries x (1 - failures/attempts)), attempts = tries reaching the
  hadronisation step; W(tau_l), W(tau_h) from the same run (sigma x measured tau-class fractions, no literals);
  K = 1.4 (V + jets; rule upper end), K_tt = 1.9 (CONSERVATIVE DEVIATION from the rule's 1.2-1.4, logged).
D2: rate_t per preselected event in the road (|dphi| < 0.15 rad, frozen delta95), gun phase space (code/s4cp.py);
  gamma/V0 (x charged BR)/PV pairs/loopers from the HS vertex; NI/DIF from the HS event + 200 x the minimum-bias
  per-interaction rate; NI per radius = sum cosh(eta) x (x/lambda_I) with 1.9e-3 (beam pipe, 22 mm) and 2.4e-3 per TBPX
  layer (30, 61.5 mm) (plan.md:1430-1432, ESTIMATE from s4geo.py); the P_PV-line 0.22 is applied in wp.cp_terms.
  Per topology the MAXIMUM over the SM processes of the per-preselected-event rate (conservative; the N_trig-weighted
  mean is reported).  The old NI 0.64-3.6 number is NOT used.
"""
import json
import math
import sys
from pathlib import Path

from acts.stage4.analysis import common as C

L_PB = 3.0e6
K_V = 1.4
K_TT = 1.9
TW_OVER_TT = 0.10     # FLAGGED allowance: Pythia 8 has no gb -> tW process; N_trig(tW) := 0.10 x N_trig(tt 1l + 2l)
                      # (UNVERIFIED ratio sigma(tW)/sigma(tt) ~ 0.085 at 14 TeV, rounded up); B_SM proxy = tt
EXTRA_K = dict(ttbar_2l=K_TT, top_t=K_V, WW=K_V, WZ=K_V, ZZ=K_V)
PROXY_OF = {'Wenu_j': ['Wtau_l', 'Wtau_h'], 'Wmunu_j': ['Wtau_l', 'Wtau_h'], 'ttbar_2l': ['ttbar_1l'],
            'top_t': ['ttbar_1l'], 'top_tW': ['ttbar_1l'], 'WW': ['Wtau_l', 'Wtau_h'],
            'WZ': ['Wtau_l', 'Wtau_h', 'Znunu_j'], 'ZZ': ['Znunu_j']}
X_LAMBDA = {'ni22': 1.9e-3, 'ni30': 2.4e-3, 'ni61': 2.4e-3}
NORM = C.HERE / 'inputs' / 'normalisation.json'


def build(gen):
    P = gen['processes']
    zt = P['Wtaunu_j']['tau_class']; zh = P['Wtauhnu_j']['tau_class']
    # REVIEW R2 A-1: W(tau) class cross sections from the corrected run (no literals): tau_l = sigma(W tau nu) x N_lep/N;
    # tau_h = the larger of sigma(W tau nu) x N_had/N and sigma(W tau_h nu sample, no BR in sigmaGen) x N_had/N
    n_inc = zt['lep']['n'] + zt['had']['n'] + zt['none']['n']
    fl = zt['lep']['n'] / n_inc; fh = zt['had']['n'] / n_inc
    SIG_TAU_L = P['Wtaunu_j']['sigma_MET200_pb'] * fl
    SIG_TAU_H = max(P['Wtaunu_j']['sigma_MET200_pb'] * fh, P['Wtauhnu_j']['sigma_MET200_pb'] * fh)
    f_tau_l = zt['lep']['sum_w'] / max(zt['lep']['n'], 1)
    f_tau_h = (zt['had']['sum_w'] + zh['had']['sum_w']) / max(zt['had']['n'] + zh['had']['n'], 1)
    proc = {
        'Znunu_j': dict(sigma_pb=P['Znunu_j']['sigma_MET200_pb'], K=K_V, f_presel=P['Znunu_j']['f_presel_weighted'],
                        rel_stat=P['Znunu_j']['rel_stat_total'], sigma_source='gen_d123 (hadfail-corrected)'),
        'Wtau_l': dict(sigma_pb=SIG_TAU_L, K=K_V, f_presel=f_tau_l, n=zt['lep']['n'],
                       rel_stat=math.sqrt(max(1 - f_tau_l, 0) / max(f_tau_l * zt['lep']['n'], 1e-9)),
                       sigma_source=f'sigma(W tau nu) x N_lep/N = {fl:.3f} (corrected run; tau_l events of the inclusive sample)'),
        'Wtau_h': dict(sigma_pb=SIG_TAU_H, K=K_V, f_presel=f_tau_h, n=zt['had']['n'] + zh['had']['n'],
                       rel_stat=math.sqrt(max(1 - f_tau_h, 0) / max(f_tau_h * (zt['had']['n'] + zh['had']['n']), 1e-9)),
                       sigma_source=f'max(sigma(W tau nu), sigma(W tau_h nu sample)) x N_had/N = {fh:.3f}; tau_h events pooled'),
        'Wenu_j': dict(sigma_pb=P['Wenu_j']['sigma_MET200_pb'], K=K_V, f_presel=P['Wenu_j']['f_presel_weighted'],
                       rel_stat=P['Wenu_j']['rel_stat_total'], sigma_source='gen_d123 (hadfail-corrected)'),
        'Wmunu_j': dict(sigma_pb=P['Wmunu_j']['sigma_MET200_pb'], K=K_V, f_presel=P['Wmunu_j']['f_presel_weighted'],
                        rel_stat=P['Wmunu_j']['rel_stat_total'], sigma_source='gen_d123 (hadfail-corrected)'),
        'ttbar_1l': dict(sigma_pb=P['ttbar_1l']['sigma_MET200_pb'], K=K_TT, f_presel=P['ttbar_1l']['f_presel_weighted'],
                         rel_stat=P['ttbar_1l']['rel_stat_total'], sigma_source='gen_d123 (hadfail-corrected)',
                         K_note='K_tt = 1.9: CONSERVATIVE DEVIATION from the rule 1.2-1.4 (orchestrator D3)'),
    }
    for pn, K in EXTRA_K.items():                     # REVIEW R2 B-1: N_trig-only processes (no hit-level sample)
        if pn in P:
            proc[pn] = dict(sigma_pb=P[pn]['sigma_MET200_pb'], K=K, f_presel=P[pn]['f_presel_weighted'],
                            rel_stat=P[pn]['rel_stat_total'], sigma_source='gen_d123 R3 (per-attempt hadfail)',
                            proxy=True, proxy_of=PROXY_OF[pn],
                            K_note=('K_tt = 1.9 (tt-like, conservative deviation)' if K == K_TT else 'K = 1.4 (rule top)'))
    for v in proc.values():
        v['N_trig'] = L_PB * v['sigma_pb'] * v['K'] * v['f_presel']
    tt = proc['ttbar_1l']['N_trig'] + proc.get('ttbar_2l', {}).get('N_trig', 0.0)
    proc['top_tW'] = dict(sigma_pb=None, K=None, f_presel=None, rel_stat=0.0, N_trig=TW_OVER_TT * tt, proxy=True,
                          proxy_of=PROXY_OF['top_tW'], allowance=True,
                          sigma_source='FLAGGED ALLOWANCE: no gb->tW in Pythia 8; 0.10 x N_trig(tt 1l + 2l) (UNVERIFIED)')
    for pn in ('Wenu_j', 'Wmunu_j'):
        proc[pn]['proxy'] = True; proc[pn]['proxy_of'] = PROXY_OF[pn]
    ntot = sum(v['N_trig'] for v in proc.values())
    rel = math.sqrt(sum((v['N_trig'] * v['rel_stat']) ** 2 for v in proc.values())) / ntot
    # D2 rates
    mb = gen['minbias']['per_PU200_event']
    rates = {}
    hs_map = dict(Znunu_j='Znunu_j', Wtaunu_j='Wtaunu_j', Wtauhnu_j='Wtauhnu_j', Wenu_j='Wenu_j', Wmunu_j='Wmunu_j',
                  ttbar_1l='ttbar_1l')
    wproc = {'Znunu_j': proc['Znunu_j']['N_trig'], 'Wtaunu_j': proc['Wtau_l']['N_trig'] + proc['Wtau_h']['N_trig'] / 2,
             'Wtauhnu_j': proc['Wtau_h']['N_trig'] / 2, 'Wenu_j': proc['Wenu_j']['N_trig'],
             'Wmunu_j': proc['Wmunu_j']['N_trig'], 'ttbar_1l': proc['ttbar_1l']['N_trig']}
    wproc.update({pn: proc[pn]['N_trig'] for pn in EXTRA_K if pn in proc})
    for t in ('gamma', 'v0', 'pvpair', 'looper', 'ni22', 'ni30', 'ni61', 'dif'):
        per = {}
        for pn in [x for x in P if P[x].get('rates_per_presel_event')]:
            r = P[pn]['rates_per_presel_event']
            if t.startswith('ni'):
                per[pn] = ((r.get('ni') or 0.0) + mb['ni']) * X_LAMBDA[t]
            elif t == 'dif':
                per[pn] = (r.get('dif') or 0.0) + mb['dif']
            else:
                per[pn] = r.get(t)
        vals = {k: v for k, v in per.items() if v is not None}
        mean = sum(vals[k] * wproc.get(k, 0.0) for k in vals) / sum(wproc.get(k, 0.0) for k in vals)
        rates[t] = dict(value=max(vals.values()), tag='ESTIMATE (generator-level Pythia, gen_d123)',
                        choice='max over SM processes (conservative); N_trig-weighted mean reported',
                        per_process=per, nt_weighted_mean=mean, sigma_ln=0.0,
                        pv_line_factor=(0.22 if t.startswith('ni') else 1.0),
                        note=('NIs per preselected event at r = (HS + 200 x min-bias) sum cosh(eta) x x/lambda_I; '
                              'x 0.22 applied in wp.cp_terms') if t.startswith('ni') else
                        ('HS + 200 x min-bias, all K decay modes (BR 1)' if t == 'dif' else 'HS vertex only'))
    spectra = dict(bins=gen['bins_pt'], hist={})
    for k in ('gamma', 'v0', 'looper', 'ni', 'dif'):
        h = [0.0] * (len(gen['bins_pt']) - 1)
        for pn in hs_map:
            sp = P[pn]['pt_spectra_presel'].get(k)
            if sp:
                h = [a + b * wproc[pn] for a, b in zip(h, sp)]
        if k in ('ni', 'dif'):
            sp = gen['minbias']['pt_spectra_per_interaction'][k]
            tw = sum(wproc.values())
            h = [a + 200 * b * tw for a, b in zip(h, sp)]
        spectra['hist'][k] = h
    return proc, ntot, rel, rates, spectra


def merge(a, b):
    """Merge two independent generator runs of one process (statistics top-up with distinct seeds)."""
    def sw2(x):
        N = x['n_acc']; f = x['f_presel_weighted']
        if 'sum_w2' in x:
            return x['sum_w2']
        sd = x['rel_stat_f'] * f * math.sqrt(N)
        return N * (sd ** 2 * (N - 1) / N + f ** 2)
    N = a['n_acc'] + b['n_acc']; T = a['tries'] + b['tries']; HF = a['hadfail'] + b['hadfail']
    swa = a['f_presel_weighted'] * a['n_acc']; swb = b['f_presel_weighted'] * b['n_acc']; sw = swa + swb
    sg = (a['sigma_gen_pb'] * a['n_acc'] + b['sigma_gen_pb'] * b['n_acc']) / N
    f = sw / N
    if 'attempts' not in a or 'attempts' not in b:
        raise SystemExit('REFUSED: merge needs the per-attempt hadronisation counts (REVIEW R2 A-1)')
    A = a['attempts'] + b['attempts']; f_att = HF / A
    var = (sw2(a) + sw2(b)) / N - f ** 2
    rel_f = math.sqrt(max(var, 0) * N / (N - 1)) / f / math.sqrt(N)
    rel_s = math.sqrt(max(1 - N / (T * (1 - f_att)), 0) / N)
    out = dict(a)
    out.update(n_acc=N, tries=T, hadfail=HF, attempts=A, f_hadfail_per_attempt=f_att, r_hadfail=HF / T, sigma_gen_pb=sg,
               sigma_MET200_pb=sg * N / (T * (1 - f_att)),
               rel_stat_sigma=rel_s, f_presel_weighted=f, rel_stat_f=rel_f, rel_stat_total=math.hypot(rel_s, rel_f),
               n_pass=a['n_pass'] + b['n_pass'], merged_from=[a.get('seed_tag', 'fixer-r2-d123'), b.get('seed_tag')],
               seconds=a['seconds'] + b['seconds'])
    out['rates_per_presel_event'] = {k: ((a['rates_per_presel_event'][k] or 0) * swa + (b['rates_per_presel_event'][k]
                                                                                        or 0) * swb) / sw
                                     for k in a['rates_per_presel_event']}
    out['pt_spectra_presel'] = {k: [(x * swa + y * swb) / sw for x, y in zip(a['pt_spectra_presel'][k],
                                                                             b['pt_spectra_presel'][k])]
                                for k in a['pt_spectra_presel']}
    return out


def main(argv=None):
    argv = argv or sys.argv[1:]
    gp = Path(argv[0]).resolve()
    gen = json.loads(gp.read_text())
    extra = []
    mbs = [a for a in argv[1:] if a.startswith('minbias=')]
    if 'minbias' not in gen and mbs:                     # minimum-bias block reused (independent of the preselection)
        mp = Path(mbs[0].split('=', 1)[1]).resolve(); extra.append(mp)
        gen['minbias'] = json.loads(mp.read_text())['minbias']
    for e in [a for a in argv[1:] if not a.startswith('minbias=')]:     # statistics top-ups (distinct seed tags)
        ep = Path(e).resolve(); extra.append(ep)
        x = json.loads(ep.read_text())
        for k, v in x['processes'].items():
            gen['processes'][k] = merge(gen['processes'][k], v)
    proc, ntot, rel, rates, spectra = build(gen)
    norm = json.loads(NORM.read_text())
    norm['n_trig'] = dict(value=ntot, rel_stat=rel, tag='ESTIMATE (generator-level Pythia + preselection proxies)',
                          status='USER DECISION D1 (2026-10-14): after the event-level preselection',
                          breakdown={k: dict(N_trig=v['N_trig'], sigma_pb=v['sigma_pb'], K=v['K'], f_presel=v['f_presel'])
                                     for k, v in proc.items()},
                          not_included='s-channel single top (negligible, 0.012 pb); Z(tau tau)+j, Z(ll)+j with lost '
                                       'leptons, QCD multijet fake MET (outside the rule list; UNVERIFIED <~1-2 % each)',
                          preselection_proxies=gen['proxies'], source=str(gp.relative_to(C.TT)),
                          source_sha256=C.sha256(gp),
                          additional_sources={str(e.relative_to(C.TT)): C.sha256(e) for e in extra},
                          additional_sources_note='minimum-bias block (minbias=) and/or statistics top-ups',
                          previous_default=1.2769e8)
    norm['sm_processes'] = proc
    norm['sm_xsec_pb'] = {k: dict(value=v['sigma_pb'], K=v['K'], tag='ESTIMATE', source=v['sigma_source'])
                          for k, v in proc.items()}
    norm['k_factor'] = K_V
    norm['k_factor_tt'] = dict(value=K_TT, note='conservative deviation from the rule range 1.2-1.4 (logged)')
    norm['cprime_rates'] = rates
    norm['cprime_spectra'] = spectra
    NORM.write_text(json.dumps(norm, indent=1))
    print(json.dumps(dict(N_trig=ntot, rel=rel, breakdown={k: round(v['N_trig'] / 1e6, 2) for k, v in proc.items()},
                          rates={k: v['value'] for k, v in rates.items()}), indent=1))


if __name__ == '__main__':
    main()
