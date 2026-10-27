"""Re-run the PRODUCTION A1 (or A5 = with PU) path for chosen rows into the investigation scratch dir and dump per-event
diagnostics.  Reuses run_g1b helpers / frozen finder unchanged; writes only under data/acts_stage4/investigation/.
usage: rerun_a1.py SPIN M LAM rows(comma) [--pu] [--tag X]"""
import sys, json, os
from pathlib import Path
import numpy as np
from acts.stage4 import run_stage4 as RS, run_g1b as RG
from acts.stage4.finder import g1b_tt as GT
from acts.stage4.code import s4sig as S

spin, m, lam = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
rows = [int(x) for x in sys.argv[4].split(',')]
pu = '--pu' in sys.argv
tag = sys.argv[sys.argv.index('--tag') + 1] if '--tag' in sys.argv else ''
VARIANTS = sys.argv[sys.argv.index('--variants') + 1].split(',') if '--variants' in sys.argv else []
OUT = RS.TT / 'data/acts_stage4/investigation'; OUT.mkdir(parents=True, exist_ok=True)
key = S.point_key(spin, m, lam)
P = S.Point(key)
fz = RS.frozen_inputs()
cfg, wcfg = RS.finder_configs(fz, dict(campaign='C1'), False)
jid = f"A1_{key.replace('/', '_')}"
job = {j['id']: j for j in json.loads((RS.JOBS / 'C1.json').read_text())['jobs']}[jid]
name = f"inv_{'A5like' if pu else 'A1'}_{spin}{m}_L{lam:g}{tag}"
tmpc = OUT / f'{name}.chain.npz'; rowsf = OUT / f'{name}.rows.json'
rowsf.write_text(json.dumps(rows))
args = ['sig', tmpc, len(rows), job['seed'], '--point', key, '--rows', rowsf, '--mat-scale', 1.0]
if not pu:
    args.append('--no-pu')
if not tmpc.exists():
    RG.chain(job, tmpc, args)
z = np.load(tmpc)
res_all = []
for ie, row in enumerate(rows):
    h, ev, met_true, pv, phimet, tseed = RG.sig_event_inputs(S, P, row, spin, P.m)
    e = z[f'ev{ie}']; tr = z[f'tru{ie}']
    variants = {}
    for vname in VARIANTS:
        ee = e.copy()
        if vname == 'noCKFq':      # A2 treatment: quirk measurements never on CKF tracks
            ee[ee[:, 7].astype(np.int64) == GT.SIG_VP, 6] = 0
        rs = np.random.default_rng(S.hseed('sig-topup', spin, P.m, row))
        Pv = GT.assemble(ee, tr, 0, rs, inserted_vp=(GT.SIG_VP,), do_topup=pu, merge_scale=(1e-9 if vname == 'nomerge' else 1.0))
        bq = Pv['H0'][:, 7].astype(np.int64) == GT.SIG_VP
        if len(Pv['H']) < 3:
            variants[vname] = dict(eff=False, eff_fckf=False, skipped=True); continue
        r_, Xv = GT.trial(Pv['H'], Pv['sid'], Pv['INT'], pv, phimet, tseed, cfg, wcfg, ckf=Pv['ckf'], btl=(Pv['btl'], Pv['btl_INT']))
        sv, _ = GT.signal_summary(Pv, Xv, int(bq.sum()), pv, phimet, cfg, Pv['ckf'], (Pv['btl'], Pv['btl_INT']))
        variants[vname] = dict(eff_R04=bool(sv['eff'][3]), eff_fckf_R04=bool(sv['eff_fckf'][3]), eff_R01=bool(sv['eff'][0]),
                               nc=int(Xv['nc']), best_frac=sv['best_frac'])
    rs = np.random.default_rng(S.hseed('sig-topup', spin, P.m, row))
    Pp = GT.assemble(e, tr, 0, rs, inserted_vp=(GT.SIG_VP,), do_topup=pu)
    H0 = Pp['H0']; barq = H0[:, 7].astype(np.int64) == GT.SIG_VP
    nqw = int(barq.sum())
    q = H0[barq]
    names = [S.NAME[int(s)] for s in q[:, 0]]
    per_surf = {}
    for nm_, part, ck in zip(names, q[:, 8].astype(int), (Pp['H0_ckf'][barq])):
        per_surf.setdefault(nm_, []).append((int(part), int(ck)))
    out = dict(row=row, eta=ev['eta'], nqw=nqw, n_ckf_q=int((barq & Pp['H0_ckf']).sum()), stats=Pp['stats'],
               per_surf={k: v for k, v in sorted(per_surf.items())}, phimet=phimet, pv=pv.tolist(), variants=variants)
    if len(Pp['H']) >= 3:
        r, X = GT.trial(Pp['H'], Pp['sid'], Pp['INT'], pv, phimet, tseed, cfg, wcfg, ckf=Pp['ckf'], btl=(Pp['btl'], Pp['btl_INT']))
        summ, rec = GT.signal_summary(Pp, X, nqw, pv, phimet, cfg, Pp['ckf'], (Pp['btl'], Pp['btl_INT']))
        out['n_road'] = int(len(X['road_idx'])); out['nc'] = int(X['nc']); out['n_q_road'] = summ['n_q_road']
        if rec is not None:
            j = int(np.argmax(rec['frac'])); c = int(rec['idx'][j])
            hh = X['hits'][X['hoff'][c]:X['hoff'][c + 1]]
            A = X['A']
            # per local layer/side counts of the band hits, quirk or not
            pool = X['road_idx'][hh]
            isq = (Pp['INT'][pool] % 1_000_000) == GT.SIG_VP
            sidb = Pp['sid'][pool]
            band = {}
            for s_, qq in zip(sidb, isq):
                band.setdefault(S.NAME[int(s_)], [0, 0])[0 if qq else 1] += 1
            # quirk pool hits NOT in band, by surface, with their out-of-plane residual
            nrm = X['r']['normal'][c]; ax = X['r']['axis'][c]
            qpool = np.where((Pp['INT'] % 1_000_000) == GT.SIG_VP)[0]
            inb = set(pool.tolist())
            miss = []
            for pi in qpool:
                if pi in inb: continue
                u = Pp['H'][pi, 1:4] - pv
                miss.append((S.NAME[int(Pp['sid'][pi])], float(u @ nrm), float(u @ np.cross(nrm, ax)), bool(pi in set(X['road_idx'].tolist()))))
            V = X['r']['vars']
            out['best'] = dict(c=c, frac=float(rec['frac'][j]), nq=int(rec['nq'][j]), nip2=int(V['nip2'][c]), nit2=int(V['nit2'][c]),
                               n2s2=int(V['n2s2'][c]), w_core=float(V['dw_core'][c]), f_ckf=float(rec['f_ckf'][j]),
                               dphi=float(X['r']['dphi_met'][c]), eta=float(X['eta'][c]), F=[int(x) for x in X['F'][c][:14]],
                               band=dict(sorted(band.items())), q_not_in_band=miss)
        out['eff_fckf_R04'] = bool(summ['eff_fckf'][3])
    else:
        out['skipped'] = True
    res_all.append(out)
json.dump(res_all, open(OUT / f'{name}.json', 'w'), indent=1, default=float)
for o in res_all:
    b = o.get('best', {})
    print(o['row'], f"eta {o['eta']:+.2f} nqw {o['nqw']} ckfq {o['n_ckf_q']} nroad_q {o.get('n_q_road')} skipped {o.get('skipped', False)}",
          'R04pass', o.get('eff_fckf_R04'), 'nip2', b.get('nip2'), 'nq', b.get('nq'), 'fckf', b.get('f_ckf'),
          {k: v.get('eff_fckf_R04') for k, v in o['variants'].items()})
