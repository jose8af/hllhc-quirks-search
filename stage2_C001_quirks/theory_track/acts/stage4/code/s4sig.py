"""code/s4sig.py -- Stage-3 quirk-hit access, numpy digitisation and energy deposit (G1, 2026-10-13; pure numpy, both envs:
acts env `import s4sig`, TT env `acts.stage4.code.s4sig`).  Plan §1.3, §1.5, §4.1 (row-major A2), review WP_RULE R1 B-2.

Signal-blind tooling: it prepares quirk measurements; it computes no efficiency.

* Input: campaign p2 (or mv), configuration BM (mv: BMx0.5/BMx2), status == 1, via data/sim_stage3/STAGE3_INDEX.json.
  Rows are matched across Lambda by the Stage-2 `row` (the same rows at every Lambda, HANDOVER §3).
* Hits: kinds T3V (virtual) and ETL (not in the ACTS geometry) are skipped and counted (V4-1).
* Digitisation (numpy, identical configuration to the ACTS smearing, plan §1.5): barrel (r phi, z) Gaussian with the
  s4geo.RES_PROD sigmas, discs (r, phi) with sigma_phi = sigma_rphi / r_mid, BTL (16 mm along phi, 0.9 mm z, 35 ps).
  Only the barrel counting surfaces and the BTL are WRITTEN (finder barrel-only, D4-12 re-decided barrel-only); the
  disc hits are counted for V4-1.  Unlike ACTS (bounded re-draws, G1 V4-9) the numpy smearing is unbounded.
* Energy deposit (B-2): dE ~ eloss.sample(Fatras slab of the surface x path factor, m, |p|) -- the same Landau model
  Fatras applies to PU and muons (closure 0.997 on the muon MIP unit, G1).  Stage-3 h_dE (mean Bethe loss in the active
  Si) is kept alongside; V4-1 checks eloss.bethe_mean(active Si x path) against h_dE in the median (consistency in mean).
* Seeds (deterministic, chunking-independent): smearing and hit efficiency from hash(spin, m, row) (identical at every
  Lambda: paired Lambda comparison, plan §4.1); dE from hash(spin, m, row, Lambda) (one uniform per hit in file order).
"""
import json
import math
from pathlib import Path

import numpy as np

try:
    from . import eloss as EL          # TT env: acts.stage4.code.s4sig
except ImportError:
    import eloss as EL                 # acts env: code/ on sys.path

TT = Path(__file__).resolve().parents[3]
S3 = TT / 'data' / 'sim_stage3'
SURF = json.loads((TT / 'sim' / 'stage3' / 'code' / 'surfaces_s3.json').read_text())['surfaces']
KIND = np.array([s['kind'] for s in SURF]); TYPE = np.array([s['type'] for s in SURF])
NAME = [s['name'] for s in SURF]
RES_PROD = {'IT': (7.2e-3, 28.9e-3), 'PS': (28.9e-3, 0.423), '2S': (26.0e-3, 14.5), 'BTL': (16.0, 0.9)}
SIG_T_BTL = 0.035
BARREL_COUNT = ['TBPX_L1', 'TBPX_L2', 'TBPX_L3', 'TBPX_L4'] + [f'{a}_L{k}_{s}' for a in ('TBPS', 'TB2S') for k in (1, 2, 3)
                                                                for s in ('in', 'out')]
WRITE = np.zeros(len(SURF), bool)
for _n in BARREL_COUNT + ['BTL']:
    WRITE[NAME.index(_n)] = True
RAD = np.array([s['p0'] * 10.0 for s in SURF])
SLAB = None
C_MM_PER_NS = 299.792458
T_ACC_NS = 25.0          # plan §1.5 hit-time window (variation 12.5)
EFF = 0.99               # plan §1.5 hit efficiency (variation 0.97)
ACTIVE_SI = {'IT': 0.15, 'PS': 0.20, '2S': 0.20}


def hseed(*parts, mod=2 ** 63):
    import hashlib
    s = '|'.join(str(p) for p in parts)
    return int.from_bytes(hashlib.blake2b(s.encode(), digest_size=8).digest(), 'little') % mod


def slab_table(mat_scale=1.0):
    return np.array([EL.slab_thickness(i, SURF, mat_scale=mat_scale) for i in range(len(SURF))])


def point_key(spin, m, lam, cfg='BM', campaign='p2'):
    return f'{campaign}/{spin}_m{int(m) if float(m).is_integer() else m}/L{lam:g}_{cfg}'


class Point:
    """All chunks of one Stage-3 point; row -> (chunk, event)."""

    def __init__(self, key, index=None):
        index = index or json.loads((S3 / 'STAGE3_INDEX.json').read_text())
        self.key = key
        self.meta = index['points'][key]
        self.files = [S3 / c['file'] for c in self.meta['chunks']]
        self.z = [np.load(f, allow_pickle=False) for f in self.files]
        self.m = float(self.z[0]['m']); self.lam = float(self.z[0]['lam_keV'])
        self.rowmap = {}
        for ci, z in enumerate(self.z):
            for ie, r in enumerate(z['row']):
                self.rowmap[int(r)] = (ci, ie)

    def rows(self, template=True, counting=True, status1=True):
        out = []
        for ci, z in enumerate(self.z):
            ok = np.ones(len(z['row']), bool)
            if template:
                ok &= z['tt_split'] == 0
            if counting:
                ok &= z['in_eta25'].astype(bool)
            if status1:
                ok &= z['status'] == 1
            out += [int(r) for r in z['row'][ok]]
        return sorted(out)

    def event(self, row):
        ci, ie = self.rowmap[row]
        z = self.z[ci]
        a, b = int(z['hit_offsets'][ie]), int(z['hit_offsets'][ie + 1])
        h = {k: z[k][a:b] for k in ('h_quirk', 'h_surf', 'h_t', 'h_x', 'h_y', 'h_z', 'h_px', 'h_py', 'h_pz', 'h_E', 'h_dE',
                                    'h_icross')}
        ev = dict(vtx=z['vtx'][ie].astype(float), recoil=z['recoil'][ie].astype(float), status=int(z['status'][ie]),
                  eta=float(z['eta'][ie]), in_eta25=bool(z['in_eta25'][ie]), tt_split=int(z['tt_split'][ie]),
                  p_qp=z['p_qp'][ie], p_qm=z['p_qm'][ie])
        return h, ev


def deposits(h, m, u01, slab):
    sid = h['h_surf'].astype(np.int64)
    p = np.sqrt(h['h_px'] ** 2 + h['h_py'] ** 2 + h['h_pz'] ** 2)
    pf = EL.path_factor(TYPE[sid], h['h_x'], h['h_y'], h['h_px'], h['h_py'], h['h_pz'])
    th = slab[sid] * pf
    ok = th > 0
    dE = np.zeros(len(sid))
    dE[ok] = EL.sample(th[ok], m, p[ok], u01[ok])
    # mean-consistency reference: Bethe mean in the ACTIVE Si (h_dE's definition, path capped as Stage 3 at 20x)
    act = np.array([ACTIVE_SI.get(k, 0.0) for k in KIND[sid]]) * np.minimum(pf, 20.0)
    bm = np.where(act > 0, EL.bethe_mean(np.maximum(act, 1e-9), m, p), 0.0)
    return dE, bm


def digitise(h, ev, m, spin, row, lam, slab, t_acc=T_ACC_NS, eff=EFF):
    """Quirk hits of one (row, Lambda) -> dict(meas (n_w, 13) G1 COLS for the written surfaces, tru (n_w, 3), hit index
    into the file, V4-1 counters).  Columns: sid, x, y, z, s0, s1, flag(0), vp(4000), particle(1 + quirk), gen(0),
    vsec(h_icross), dE (Fatras-model sample), t (ns; BTL smeared)."""
    n = len(h['h_surf'])
    sid = h['h_surf'].astype(np.int64)
    kind = KIND[sid]
    skip_t3v = kind == 'T3V'; skip_etl = kind == 'ETL'
    phys = ~(skip_t3v | skip_etl)
    rs = np.random.default_rng(hseed('sig-smear', spin, m, row))
    g = rs.normal(0.0, 1.0, (n, 3))                  # per hit in file order: (loc0, loc1, time)
    ue = rs.random(n)                                # hit efficiency
    ud = np.random.default_rng(hseed('sig-dE', spin, m, row, f'{lam:g}')).random(n)
    dE, bm = deposits(h, m, ud, slab)
    x, y, zz, t = h['h_x'], h['h_y'], h['h_z'], h['h_t']
    vt = ev['vtx']
    d = np.sqrt((x - vt[0]) ** 2 + (y - vt[1]) ** 2 + (zz - vt[2]) ** 2)
    delay = t - vt[3] - d / C_MM_PER_NS
    late = delay > t_acc
    lost_eff = ue >= eff
    keep = phys & WRITE[sid] & ~late & ~lost_eff
    idx = np.where(keep)[0]
    out = np.zeros((len(idx), 13))
    s = sid[idx]
    R = RAD[s]
    phi = np.arctan2(y[idx], x[idx])
    s0 = np.array([RES_PROD[k][0] for k in kind[idx]]) if len(idx) else np.zeros(0)
    s1 = np.array([RES_PROD[k][1] for k in kind[idx]]) if len(idx) else np.zeros(0)
    phim = phi + s0 * g[idx, 0] / R
    out[:, 0] = s; out[:, 1] = R * np.cos(phim); out[:, 2] = R * np.sin(phim); out[:, 3] = zz[idx] + s1 * g[idx, 1]
    out[:, 4] = s0; out[:, 5] = s1; out[:, 6] = 0; out[:, 7] = 4000; out[:, 8] = 1 + h['h_quirk'][idx]
    out[:, 9] = 0; out[:, 10] = h['h_icross'][idx]; out[:, 11] = dE[idx]
    btl = kind[idx] == 'BTL'
    out[:, 12] = t[idx] + np.where(btl, SIG_T_BTL * g[idx, 2], 0.0)
    tru = np.c_[x[idx], y[idx], zz[idx]]
    # V4-1 (numpy path)
    onsurf = np.abs(np.hypot(x, y) - RAD[sid])[phys & (TYPE[sid] == 0)]
    causal = t - vt[3] - d / C_MM_PER_NS
    act = (bm > 0) & (h['h_dE'] > 0)
    v41 = dict(n_hits=int(n), n_t3v=int(skip_t3v.sum()), n_etl=int(skip_etl.sum()), n_phys=int(phys.sum()),
               n_barrel_written_surfaces=int((phys & WRITE[sid]).sum()), n_late=int((phys & WRITE[sid] & late).sum()),
               n_ineff=int((phys & WRITE[sid] & ~late & lost_eff).sum()), n_meas=int(len(idx)),
               n_disc_or_other=int((phys & ~WRITE[sid]).sum()),
               max_onsurf_um=float(onsurf.max() * 1e3) if len(onsurf) else 0.0,
               min_causal_ns=float(causal[phys].min()) if phys.any() else 0.0,
               dE_mean_ratio_median=float(np.median(bm[act] / h['h_dE'][act])) if act.any() else float('nan'),
               n_dE=int(act.sum()))
    v41['pass'] = bool(v41['n_meas'] + v41['n_late'] + v41['n_ineff'] == v41['n_barrel_written_surfaces']
                       and v41['n_t3v'] + v41['n_etl'] + v41['n_phys'] == n and v41['max_onsurf_um'] < 1.0
                       and v41['min_causal_ns'] > -1e-6)
    return dict(meas=out, tru=tru, hit=idx, h_dE=h['h_dE'][idx].astype(np.float32), v41=v41,
                dE_all=dE, bethe_active=bm)
