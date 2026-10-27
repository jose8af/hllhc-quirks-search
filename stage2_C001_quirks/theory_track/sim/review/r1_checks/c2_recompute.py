"""R1 check 2: independent recomputation of headline numbers from the npz files (no vlib import).
Run: pixi run -e ana python review/r1_checks/c2_recompute.py  (from sim/)"""
import os, numpy as np
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'data', 'sim', 'npz')
L = lambda n: dict(np.load(os.path.join(D, n + '.npz'), allow_pickle=False))
pt = lambda P: np.hypot(P[:, 1], P[:, 2])
def minv(P): return np.sqrt(np.maximum(P[:, 0]**2 - (P[:, 1:]**2).sum(1), 0))
def wmed(v, w):
    i = np.argsort(v); c = np.cumsum(w[i]); c /= c[-1]; return v[i][np.searchsorted(c, 0.5)]

print('=== A. sigma from event weights ===')
for n in ('E-INC_m500', 'E-TRG_m500', 'E-LOPS_m500', 'E-INC_m1000', 'S-INC_m500', 'E-INC_m1500', 'E-TRG_m1500'):
    c = L(n); w = c['w']; nz = w != 0
    names = [str(x) for x in c['wvar_names']]
    print(f"{n}: N_LHE={int(c['nlhe'])} kept={len(w)} w!=0={nz.sum()} sum(w)={w.sum():.5g} fb  sigma_LHE={float(c['sigma_lhe_fb']):.5g}"
          f"  accept(w-sum)={w.sum()/float(c['sigma_lhe_fb']):.4f} accept(count)={nz.sum()/int(c['nlhe']):.4f}"
          f"  chunks sigma_LHE={c.get('sigma_lhe_fb_chunks', 'n/a')}  w>0 all={bool((w[nz]>0).all())}"
          f"  distinct |w| (rel spread)={np.std(w[nz])/np.mean(w[nz]):.3g}")
    # quirk mass check
    mq = minv(c['p_qp']); mm = minv(c['p_qm'])
    print(f"   quirk masses after shower: p_qp {mq.min():.3f}-{mq.max():.3f}, p_qm {mm.min():.3f}-{mm.max():.3f} (mq={float(c['mq'])}); "
          f"m_pair min={c['m_pair'].min():.2f}; hard-vs-showered m_pair max|d|={np.abs(minv(c['p_qq_hard'])-c['m_pair']).max():.3g}")

print('\n=== B. ME-cut closure and TRGS stitching (E/S 200/500/1000) ===')
for pre in ('E', 'S'):
    for m in (200, 500, 1000):
        ci, ct, cs = L(f'{pre}-INC_m{m}'), L(f'{pre}-TRG_m{m}'), L(f'{pre}-TRGS_m{m}')
        pti, ptt = ci['pt_pair'], ct['pt_pair']
        hi, ht = pt(ci['p_qq_hard']), pt(ct['p_qq_hard'])
        wi, wt = ci['w'], ct['w']
        s_inc = wi[pti > 200].sum(); s_trg = wt[ptt > 200].sum()
        s_inc_hi = wi[(pti > 200) & (hi >= 100)].sum(); s_inc_lo = wi[(pti > 200) & (hi < 100)].sum()
        e_inc = np.sqrt((wi[pti > 200]**2).sum()); e_trg = np.sqrt((wt[ptt > 200]**2).sum())
        e_lo = np.sqrt((wi[(pti > 200) & (hi < 100)]**2).sum())
        ss = cs['w'][cs['pt_pair'] > 200].sum()
        frac_inc_in_trgs = cs['w'][(cs['pt_pair'] > 200) & (cs['origin'] == 1)].sum() / ss
        print(f"{pre}{m}: TRG/INC={s_trg/s_inc:.3f}±{np.hypot(e_trg/s_trg, e_inc/s_inc)*s_trg/s_inc:.3f}  gen-cut closure={s_trg/s_inc_hi:.3f}"
              f"  INC tail frac pT_ME<100={100*s_inc_lo/s_inc:.2f}±{100*e_lo/s_inc:.2f}%  TRGS/INC(pT>200)={ss/s_inc:.3f}"
              f"  TRG events with pT_ME<100: {(ht < 100).sum()} (min pT_ME {ht.min():.2f})  TRGS sigma frac from INC={100*frac_inc_in_trgs:.2f}%"
              f"  <w_INC>/<w_TRG>={wi[wi!=0].mean()/wt[wt!=0].mean():.2f}")

print('\n=== C. TRGS file order vs iter_events "first N" usage (tail, |eta|<2.5) ===')
for pre in ('E', 'S'):
    for m in (200, 500, 1000):
        cs = L(f'{pre}-TRGS_m{m}')
        sel = np.where((cs['w'] > 0) & (cs['pt_pair'] > 200) & (np.abs(cs['eta_pair']) < 2.5))[0]
        org = cs['origin'][sel]
        first_inc = np.argmax(org == 1) if (org == 1).any() else -1
        winc = cs['w'][sel][org == 1].sum() / cs['w'][sel].sum()
        print(f"{pre}{m}: selected={len(sel)}, INC-origin events={int((org==1).sum())} (weight share {100*winc:.1f}%), "
              f"position of first INC-origin event in iter_events order = {first_inc}  -> first {first_inc} events are TRG-only")

print('\n=== D. median l_max bias, recomputed (E 500, S 200) ===')
OLD = os.path.join(D, '..', '..', 'cache', 'T2_kinematics_cache.npz')
o = np.load(OLD)
for spin, pre, m in (('F', 'E', 500), ('F', 'E', 200), ('S', 'S', 200)):
    cs = L(f'{pre}-TRGS_m{m}')
    sel = (cs['w'] != 0) & (cs['pt_pair'] > 200) & (np.abs(cs['eta_pair']) < 2.5)
    xr = wmed(2 * (cs['gamma_star'][sel] - 1), cs['w'][sel])
    gi, wi_ = o[f'{spin}_{m}_incl_gamma_star'], o[f'{spin}_{m}_incl_w']
    x1 = wmed(2 * (gi[wi_ > 0] - 1), wi_[wi_ > 0])
    gx, wx, ex = o[f'{spin}_{m}_isr_gamma_star'], o[f'{spin}_{m}_isr_w'], o[f'{spin}_{m}_isr_eta_pair']
    bgx = o[f'{spin}_{m}_isr_bg_pair']; Mx = 2 * m * gx; ptx = Mx * bgx / np.cosh(ex)
    s2 = (wx > 0) & (ptx > 200) & (np.abs(ex) < 2.5)
    x2 = wmed(2 * (gx[s2] - 1), wx[s2])
    cl = L(f'{pre}-LOPS_m{m}'); s3 = (cl['pt_pair'] > 200) & (np.abs(cl['eta_pair']) < 2.5)
    x3 = wmed(2 * (cl['gamma_star'][s3] - 1), cl['w'][s3])
    ctr = L(f'{pre}-TRG_m{m}'); s4 = (ctr['w'] != 0) & (ctr['pt_pair'] > 200) & (np.abs(ctr['eta_pair']) < 2.5)
    x4 = wmed(2 * (ctr['gamma_star'][s4] - 1), ctr['w'][s4])
    # old 'isr' cache: min pT stored?
    print(f"{pre}{m}: ref median 2(g*-1) TRGS={xr:.4f}; (i) fixed-pT/old incl={x1:.4f} -> bias {100*(x1/xr-1):+.1f}%; "
          f"(ii) T2 V*+jet={x2:.4f} -> {100*(x2/xr-1):+.1f}%; (iii) LOPS={x3:.4f} -> {100*(x3/xr-1):+.1f}%; raw TRG={x4:.4f} -> {100*(x4/xr-1):+.1f}%;"
          f"  old isr cache min pT={ptx[wx>0].min():.1f}, max|y-gen| check: max|eta| among pT>200 = {np.abs(ex[s2]).max():.2f}")
