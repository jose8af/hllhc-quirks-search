"""admissibility.py -- D4-17 option (i) (WP_RULE §8, plan §2.6): per-hypothesis admissible width and dE/dx levels,
the fallback selection r_fb(m, Lambda, c), and the admissibility of a working-point rung r*_c.

Inputs (frozen, hash-checked against WP_RULE A.3):
  data/acts_stage4/fix_r4/f4r_admissibility.json (45847697...) -> Lambda_R smoothed (k_adm thresholds)
  data/acts_stage4/frozen/eadm_dilution.json     (7661bd63...) -> e_adm(m, Lambda) (dilution-aware, A.2b)
k_adm(m, Lambda) = the largest k in {0..4} with Lambda >= Lambda_R(m) 2^((k+1)/2)  (computed, and cross-checked with
the A.2b table where the point is tabulated).  The PU-density update of A.2b (rho_dens > 1.05 -> re-run) is checked
by background.rho_dens from the S6 dumps (background.json rho_dens); if triggered, run_all.limits_stage REFUSES to
produce any fallback result with this table (REVIEW R1 B-5); signal_eff.json records the check as pending.
"""
import json

import numpy as np

from acts.stage4.analysis import common as C

F4R = C.DATA / 'fix_r4' / 'f4r_admissibility.json'
EADM = C.DATA / 'frozen' / 'eadm_dilution.json'
F4R_SHA = '45847697b76fadaa7d2269c385258b0d67a2248cb1848fff78acedbc13bda97a'
EADM_SHA = '7661bd634053da542ef8f114bd6ccad27a36e2a75d0dd7aaea5bee325b9babcd'


class Admissibility:
    def __init__(self):
        self.sha = {str(F4R.relative_to(C.TT)): C.sha256(F4R), str(EADM.relative_to(C.TT)): C.sha256(EADM)}
        self.ok = self.sha[str(F4R.relative_to(C.TT))] == F4R_SHA and self.sha[str(EADM.relative_to(C.TT))] == EADM_SHA
        if not self.ok:
            raise RuntimeError(f'admissibility inputs do not match WP_RULE A.3: {self.sha}')
        f4 = json.loads(F4R.read_text())
        self.lam_r = {k: v['smoothed_keV'] for k, v in f4['Lambda_R'].items()}
        self.eadm = json.loads(EADM.read_text())['e_adm']

    @staticmethod
    def key(spin, m):
        return f'{spin}_m{int(m)}'

    def k_adm(self, spin, m, lam):
        lr = self.lam_r[self.key(spin, m)]
        k = 0
        for kk in range(1, 5):
            if lam >= lr * 2 ** ((kk + 1) / 2) - 1e-12:
                k = kk
        return k

    def e_adm(self, spin, m, lam):
        t = self.eadm.get(self.key(spin, m), {})
        cell = t.get(f'{lam:g}')
        if cell is None:
            return None, 'not tabulated'
        return cell.get('e_adm'), cell.get('k_adm')

    def point(self, spin, m, lam):
        k = self.k_adm(spin, m, lam)
        e, k_tab = self.e_adm(spin, m, lam)
        if e is not None and k != 4:
            raise RuntimeError('e_adm without k_adm = 4 contradicts WP_RULE §8')
        fb = f'FB{k}' + (f'e>{e:g}' if e is not None else '')
        return dict(k_adm=k, k_adm_table=k_tab if k_tab != 'not tabulated' else None, k_consistent=(k_tab in (None, 'not tabulated') or k_tab == k),
                    e_adm=e, fb_column=fb, r_fb=fb + '&h>5&o>5', width_cut_mm=C.W_K[k - 1] if k >= 1 else None)


def rung_levels(rung):
    """(width level k, dE/dx level) of ladder rung number 1..23 (cumulative ladder, WP_RULE §3)."""
    k = 0 if rung <= 4 else min(4, rung - 4)
    e = {21: 1.3, 22: 1.6, 23: 2.0}.get(rung)
    return k, e


def rstar_admissible(rung, k_adm, e_adm):
    """WP_RULE §8: r*_c admissible at (m, Lambda) iff its width level <= k_adm and its dE/dx level <= e_adm."""
    if rung is None:
        return False
    k, e = rung_levels(rung)
    if k > k_adm:
        return False
    if e is not None and (e_adm is None or e > e_adm + 1e-9):
        return False
    return True


def primary(spin, m, lam, rstar, adm):
    """Primary selection per category (WP_RULE §8 'Primary result per (m, Lambda, c)'); rstar = {'T': rung|None,
    'G': rung|None}.  Mixed admissibility -> the 'exactly one category' branch of §5.2 at that point."""
    p = adm.point(spin, m, lam)
    out = {}
    for c in ('T', 'G'):
        r = rstar.get(c)
        if r is not None and rstar_admissible(r, p['k_adm'], p['e_adm']):
            out[c] = dict(kind='r*', rung=r, name=C.LADDER_NAMES[r - 1], background_free_claim=True)
        else:
            out[c] = dict(kind='r_fb', rung=None, name=p['r_fb'] + ('&SR-T' if c == 'T' else ''),
                          background_free_claim=False,
                          why='no WP' if r is None else 'r* not admissible at this point')
    n_rstar = sum(v['kind'] == 'r*' for v in out.values())
    out['branch'] = {2: 'both r* (combined guard applies)', 1: 'mixed: exactly-one-category branch (§5.2)',
                     0: 'fallback both'}[n_rstar]
    out['admissibility'] = p
    return out
