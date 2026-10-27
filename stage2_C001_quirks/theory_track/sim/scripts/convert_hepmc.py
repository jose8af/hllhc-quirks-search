"""convert_hepmc.py -- convert a MadGraph5_aMC + Pythia8 HepMC2 file of quirk pairs into the compact per-event
format read by sim/scripts/mg_events.py (and, through it, by code/T3_causal.run_causal).  Stage 2 of the
theory track (E4).  Run in the 'ana' pixi env of sim/:

  pixi run -e ana python scripts/convert_hepmc.py <events.hepmc.gz> <out.npz> --mq 500 --spin F \
      --sigma-lhe-pb 7.764e-4 --nlhe 1000 [--merging-nominal 45.000] [--banner run_banner.txt] [--tag ...]

Output npz (one row per event with non-zero weight for at least one merging scale; lengths in cm, momenta GeV):
  p_qp[N,4], p_qm[N,4]   (E, px, py, pz) of the positive (pid < 0, xe+/sxe+) and negative (xe-/sxe-) quirk after
                         the shower (status 1).  T3_causal convention: run_causal(p1=p_qp[1:], p2=p_qm[1:]) with the
                         default charges=(+1, -1).
  vtx[N,4]               production vertex (x, y, z, ct) [cm] (Pythia vertex spread is off: origin; beam spot is
                         applied downstream)
  p_qp_hard[N,4], p_qm_hard[N,4]  quirks before the shower (Pythia status 23 = LHE kinematics), for ISR-tail
                         studies; p_qq_hard = their sum
  recoil[N,4]            sum of final-state particles except quirks and neutrinos (all eta)
  recoil_eta5[N,4]       same, |eta| < 5
  nu[N,4]                sum of final-state neutrinos
  jets[N,4,4]            up to 4 leading anti-kt R=0.4 jets (pt, eta, phi, m), pt > 20 GeV, |eta| < 5, built from
                         recoil particles (zeros if absent); njet[N] = number of such jets (all, not only 4)
  n_me[N]                number of outgoing QCD partons in the hard process (status 23): 0, 1, 2 (MLM multiplicity)
  w[N]                   nominal weight [fb per event, N_IC = 1]: sum(w) = sigma_matched(nominal merging scale)
  wvar[N,K], wvar_names  all weight variations in the file (merging scales, mu_R/mu_F, dyn. scale, PDF members),
                         in the same units (fb per event, N_IC = 1)
  derived: gamma_star[N] (Lorentz factor of each quirk in the pair CM), cstar[N] (cos between quirk axis and pair
           velocity, T2 convention), bg_pair, eta_pair, y_pair, pt_pair, m_pair
  meta: mq, spin, sigma_lhe_fb, nlhe, n_in_file, merging_nominal, source, tag
Weights: MG writes the HepMC weights in pb with event_norm = average, so sigma = sum_i w_i / N_LHE.  We store
w_i(fb) = w_i(pb) * 1e3 / N_LHE so that plain sums give fb.  N_IC is NOT included (multiply by N_IC = 2).
"""
import argparse
import os
import time

import numpy as np
import pyhepmc

QPIDS = (9000011, 9000013)
NUPIDS = (12, 14, 16)


def derived(pp, pm):
    P = pp + pm
    M = np.sqrt(np.maximum(P[:, 0] ** 2 - np.sum(P[:, 1:] ** 2, 1), 0))
    b = P[:, 1:] / P[:, :1]
    b2 = np.sum(b * b, 1)
    g = 1 / np.sqrt(1 - b2)
    # boost the positive quirk to the pair rest frame
    bp = np.sum(b * pp[:, 1:], 1)
    coef = np.where(b2 > 0, (g - 1) * bp / np.where(b2 > 0, b2, 1), 0) - g * pp[:, 0]
    q = pp[:, 1:] + coef[:, None] * b
    e_star = g * (pp[:, 0] - bp)
    mq = np.sqrt(np.maximum(pp[:, 0] ** 2 - np.sum(pp[:, 1:] ** 2, 1), 0))
    gstar = e_star / mq
    bh = b / np.maximum(np.sqrt(b2), 1e-300)[:, None]
    cstar = np.sum(q * bh, 1) / np.maximum(np.linalg.norm(q, axis=1), 1e-300)
    pmag = np.linalg.norm(P[:, 1:], axis=1)
    pt = np.hypot(P[:, 1], P[:, 2])
    eta = np.arcsinh(P[:, 3] / np.maximum(pt, 1e-12))
    y = 0.5 * np.log((P[:, 0] + P[:, 3]) / (P[:, 0] - P[:, 3]))
    return dict(gamma_star=gstar, cstar=cstar, bg_pair=pmag / M, eta_pair=eta, y_pair=y, pt_pair=pt, m_pair=M)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('hepmc'); ap.add_argument('out')
    ap.add_argument('--mq', type=float, required=True); ap.add_argument('--spin', choices=('F', 'S'), required=True)
    ap.add_argument('--sigma-lhe-pb', type=float, required=True, help='MG cross section of the LHE file [pb]')
    ap.add_argument('--nlhe', type=int, required=True, help='number of LHE events showered')
    ap.add_argument('--merging-nominal', default=None, help="e.g. 45.000 (None: unmatched sample, use 'Weight')")
    ap.add_argument('--tag', default='')
    ap.add_argument('--max-events', type=int, default=-1)
    ap.add_argument('--no-jets', action='store_true')
    ap.add_argument('--norm', choices=('nlhe', 'auto'), default='nlhe',
                    help="nlhe: w_fb = w_pb*1e3/N_LHE (MG merged file); auto: w_fb = w * sigma_LHE / sum over ALL events read of "
                         "the unmerged central weight 'Weight' (scale-free; used for our own split shower jobs)")
    a = ap.parse_args()
    if not a.no_jets:
        import fastjet
        jdef = fastjet.JetDefinition(fastjet.antikt_algorithm, 0.4)
    t0 = time.time()
    names = None
    rows = dict(p_qp=[], p_qm=[], vtx=[], p_qp_hard=[], p_qm_hard=[], p_qq_hard=[], recoil=[], recoil_eta5=[], nu=[], jets=[], njet=[], n_me=[], wvar=[])
    nin = 0
    wsum_all = 0.0
    with pyhepmc.open(a.hepmc) as fh:
        for ev in fh:
            if 0 <= a.max_events <= nin:
                break
            nin += 1
            if names is None:
                names = list(ev.weight_names)
                if a.merging_nominal is None:
                    inom = names.index('Weight')
                    imerge = [inom]
                else:
                    inom = names.index(f'Weight_MERGING={a.merging_nominal}')
                    imerge = [i for i, n in enumerate(names) if n.startswith('Weight_MERGING=')]
                lscale = 0.1 if ev.length_unit == pyhepmc.Units.LengthUnit.MM else 1.0   # -> cm
                icen = names.index('Weight')
            w = np.asarray(ev.weights, float)
            wsum_all += w[icen]
            if not np.any(w[imerge] != 0):
                continue          # rejected by MLM at every merging scale
            qp = qm = None; hard = np.zeros(4); hp = hm = np.zeros(4); rec = np.zeros(4); rec5 = np.zeros(4); nu = np.zeros(4); nme = 0
            vis = []
            for p in ev.particles:
                apid = abs(p.pid); mo = p.momentum
                if p.status == 23 and (apid <= 6 or apid == 21):
                    nme += 1
                if apid in QPIDS:
                    if p.status == 23:
                        hard += (mo.e, mo.px, mo.py, mo.pz)
                        if p.pid < 0:
                            hp = np.array((mo.e, mo.px, mo.py, mo.pz))
                        else:
                            hm = np.array((mo.e, mo.px, mo.py, mo.pz))
                    if p.status == 1:
                        v = (mo.e, mo.px, mo.py, mo.pz)
                        if p.pid < 0:
                            qp = v; vx = p.production_vertex.position
                        else:
                            qm = v
                    continue
                if p.status != 1:
                    continue
                v4 = np.array((mo.e, mo.px, mo.py, mo.pz))
                if apid in NUPIDS:
                    nu += v4; continue
                rec += v4
                pt = np.hypot(mo.px, mo.py)
                if pt > 0 and abs(np.arcsinh(mo.pz / pt)) < 5:
                    rec5 += v4
                    vis.append(v4)
            assert qp is not None and qm is not None, 'event without two final-state quirks'
            jets = np.zeros((4, 4)); nj = 0
            if not a.no_jets and vis:
                cs = fastjet.ClusterSequence([fastjet.PseudoJet(v[1], v[2], v[3], v[0]) for v in vis], jdef)
                js = [j for j in fastjet.sorted_by_pt(cs.inclusive_jets(20.0)) if abs(j.eta()) < 5]
                nj = len(js)
                for k, j in enumerate(js[:4]):
                    jets[k] = (j.pt(), j.eta(), j.phi_std(), j.m())
            rows['p_qp'].append(qp); rows['p_qm'].append(qm)
            rows['vtx'].append((vx.x * lscale, vx.y * lscale, vx.z * lscale, vx.t * lscale))
            rows['p_qq_hard'].append(hard); rows['p_qp_hard'].append(hp); rows['p_qm_hard'].append(hm); rows['recoil'].append(rec); rows['recoil_eta5'].append(rec5); rows['nu'].append(nu)
            rows['jets'].append(jets); rows['njet'].append(nj); rows['n_me'].append(nme); rows['wvar'].append(w)
    out = {k: np.asarray(v) for k, v in rows.items()}
    # The MG5aMC_PY8_interface writes the merged (named, '..._MERGING=...') weights normalised to sigma/N_events of the
    # job, while 'Weight' and the AUX_* (LHE) weights are per-event sigma ('average').  MG's own merged file rescales
    # them; for our split jobs we detect the factor k = Weight / Weight_MERGING=nominal on accepted events (k = 1 for
    # MG-merged files, k = N_split for split jobs) and bring the named columns to the 'average' convention.
    raw = out['wvar']
    nz = raw[:, inom] != 0
    iref = inom
    if inom == icen:      # unmatched sample: reference = 'Weight_MERGING=0.000' (no veto, pure normalisation factor)
        cand = [i for i, n in enumerate(names) if n.startswith('Weight_MERGING=')]
        iref = cand[0] if cand else icen
        nz = raw[:, iref] != 0
    k = float(np.median(raw[nz, icen] / raw[nz, iref])) if nz.any() and iref != icen else 1.0
    named = np.array([('_MERGING=' in n) for n in names])
    raw[:, named] *= k
    out['merged_col_factor'] = k
    if a.norm == 'nlhe':
        out['wvar'] = out['wvar'] * 1e3 / a.nlhe      # pb (average norm) -> fb per event, sum = sigma
    else:
        out['wvar'] = out['wvar'] * (a.sigma_lhe_pb * 1e3 / wsum_all)
    out['w'] = out['wvar'][:, inom].copy()
    out.update(derived(out['p_qp'], out['p_qm']))
    out.update(wvar_names=np.array(names), mq=a.mq, spin=a.spin, sigma_lhe_fb=a.sigma_lhe_pb * 1e3, nlhe=a.nlhe,
               n_in_file=nin, merging_nominal=str(a.merging_nominal), source=os.path.abspath(a.hepmc), tag=a.tag,
               n_ic_included=0, norm_mode=a.norm, wsum_all_central=wsum_all)
    np.savez_compressed(a.out, **out)
    print(f'{a.hepmc}: {nin} events read, {len(out["w"])} kept (non-zero merging weight); sigma(nominal) = '
          f'{out["w"].sum():.5g} fb (N_IC=1); {time.time() - t0:.1f} s -> {a.out}')


if __name__ == '__main__':
    main()
