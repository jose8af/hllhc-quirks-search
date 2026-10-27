"""background.py -- B_PU per rung (WP_RULE §4, §6; plan §4.1) with the user-approved closure END STATE, the SM (C) and
C' terms (WP_RULE §7), and the zero/low-count rule (§4.2).

Closure (USER 2026-10-14): the pre-registered conservative end state -- B_PU = upper envelope of {thinning, power law,
factorisation} x N_obs/N_pred of the failed test, COMPOUNDED along the cumulative ladder (literal reading; the G3
report flags that it double-counts the R04 part of T1w -- conservative), a significant trend enters sigma_ln (and the
central value only if anti-conservative); T1/T1w RE-MEASURED at T_seed = 4 on the production B1/B2 union; no +50 %
statistics steps; no union-count rule change.  The branch per family is still DETERMINED by the re-measured tests
(analyse_g3.family_test, reused unchanged): nominal / conservative / anti-conservative / missing lever arm.

Estimators per in-job column r (governing per-hit-set convention, WP_RULE §2; union for NOGRP columns):
  P_thin(r)   = <S_ded(r)> per B2 trial (thinning, union bound), reachable at rho = 2 iff >= 10 groups at rho = 2;
  beyond the deepest reachable ladder rung r_d: P(r) = P_thin(r_d) x prod_j p_j (rung factorisation, conditionals at
              rho = 1 on B1 S2 records, each on the tightest population with M >= 10, zero-count rule, x c if flagged);
  P_fact(r)   = P_B1(r_b) x prod_j p_j from the deepest ladder rung r_b with >= 10 B1 groups (the factorisation model);
  P_pow(r)    = the power law A rho^alpha evaluated at rho = 1 = the B1 direct group rate (only where B1 has >= 10);
  anti-conservative branch: central = max(P_main, P_fact, P_pow) x compounded N_obs/N_pred, sigma_ln,model = ln(max/min).
F1 rungs (h, o): P(R15-R20) = P(R14) x p(h/o | R14); P(R21-23) = P(R14 & e_x) x p(h>5 & o>5 | R14 & e_x); fallback
r_fb = P(FB_k[e]) x p(h>5 & o>5 | FB_k[e]) (WP_RULE §6.2 composition), conditionals measured on B1 S4 records.
f_CKF: no credit for B_PU (factor 1, §1.2).
"""
import numpy as np

from acts.stage4.analysis import common as C
from acts.stage4.analysis import hitrec as HR
from acts.stage4.g3 import analyse_g3 as G3        # reused closure machinery (frozen G3 analysis, read-only import)

LN114 = 1.14


# ================================================================================================ loading
B1_CAND_KEYS = ['tag', 'group', 'trial', 'idx', 'nit2', 'nip2', 'n2s2', 'dw_core', 'p_chi2core', 'dedx', 'dphi_met',
                'eta_axis', 'rungs', 'cross', 'btl_n_band', 'f_ckf', 'n_core', 'n_hs_band']   # normal/axis/btl: lazy
TR_KEYS = ['ev', 'road', 'n_pass', 'n_grp', 'n_road', 'pv', 'trial_seed', 'n_pass_T', 'n_grp_T', 'S_ded', 'S_uni',
           'S_ded_T', 'S_uni_T', 'meanW_pull', 'meanW_pull_T', 'is_zero_draw_frac', 't_total']


def to_g3_job(rec, rho, keep_hits=False):
    """Reshape a collect() record into the dict layout analyse_g3 expects (tr, cand, job, n_trials)."""
    d = rec['d']
    tr = {k: d['trials.' + k] for k in TR_KEYS if 'trials.' + k in d}
    cand = {k: d['cand.' + k] for k in B1_CAND_KEYS if 'cand.' + k in d}
    j = dict(tr=tr, cand=cand, job=rec['job'], job_id=rec['job']['id'], n_trials=len(tr['ev']), meta=rec['d']['meta'],
             path=rec['path'])
    if keep_hits:
        j['hits'] = {k: d[k] for k in d if k.startswith('hit.')}
    if 'btl' in d:
        j['btl'] = d['btl']
    return j


def stack(jobs, rho):
    tr = {}
    ev_of = []; evn = 0; jev = []
    for ij, d in enumerate(jobs):
        for k, v in d['tr'].items():
            tr.setdefault(k, []).append(v)
        ue, inv = np.unique(d['tr']['ev'], return_inverse=True)
        ev_of.append(inv + evn); evn += len(ue)
        jev.append((d['job_id'], ue))
    tr = {k: np.concatenate(v) for k, v in tr.items()}
    return tr, (np.concatenate(ev_of) if ev_of else np.zeros(0, int)), evn


class PUSamples:
    """B1 (rho = 1) and B2 (rho = 2) union of the admitted campaigns, with event-level bootstrap indices."""

    def __init__(self, b1_jobs, b2_jobs, nboot, rng, t_cols=False):
        self.b1 = b1_jobs; self.b2 = b2_jobs
        tr1, ev1, E1 = stack(b1_jobs, 1)
        tr2, ev2, E2 = stack(b2_jobs, 2)
        sfx = '_T' if t_cols else ''
        self.tr1, self.ev1, self.E1, self.tr2, self.ev2, self.E2 = tr1, ev1, E1, tr2, ev2, E2
        self.ntr1_ev = C.ev_sums(ev1, np.ones(len(ev1)), E1)
        g1 = np.where(tr1['n_grp' + sfx] < 0, tr1['n_pass' + sfx], tr1['n_grp' + sfx]).astype(float)
        self.nobs_ev = C.ev_sums(ev1, g1, E1)
        self.npass1_ev = C.ev_sums(ev1, tr1['n_pass' + sfx].astype(float), E1)
        self.bi1 = C.boot_idx(E1, nboot, rng)
        self.have_b2 = E2 > 0
        if self.have_b2:
            self.ntr2_ev = C.ev_sums(ev2, np.ones(len(ev2)), E2)
            sd = np.where(np.isnan(tr2['S_ded' + sfx]), tr2['S_uni' + sfx], tr2['S_ded' + sfx])
            self.s2_ev = C.ev_sums(ev2, np.nan_to_num(sd), E2)
            self.suni_ev = C.ev_sums(ev2, np.nan_to_num(tr2['S_uni' + sfx]), E2)
            g2 = np.where(tr2['n_grp' + sfx] < 0, tr2['n_pass' + sfx], tr2['n_grp' + sfx]).astype(float)
            self.n2grp_ev = C.ev_sums(ev2, g2, E2)
            self.bi2 = C.boot_idx(E2, nboot, rng)

    def n1(self):
        return self.ntr1_ev.sum()

    def n2(self):
        return self.ntr2_ev.sum() if self.have_b2 else 0


# ================================================================================================ closure
def closure(S, rng, nboot):
    """T1, T1w, T1e, trend (WP_RULE §6.4) re-measured on the union; analyse_g3 functions unchanged."""
    if not S.have_b2:          # no B2 output yet (partial production): every closure test untestable, flagged
        u = dict(branch='untestable', ratio=None, r1=None, note='no B2 (rho = 2) outputs')
        return dict(T1=u, T1_readingB=u, T1w=u, T1e=dict(u, branch='-> T3'), trend=dict(significant=False, points=[]),
                    T1_governing_branch='untestable')
    a = (S.nobs_ev, S.ntr1_ev, S.s2_ev, S.ntr2_ev, S.n2grp_ev, S.bi1, S.bi2)
    out = dict(T1=G3.family_test('T1', [3], *a),
               T1_readingB=G3.family_test('T1 (any ladder rung R04-R14; reading B)', list(range(3, 14)), *a),
               T1w=G3.family_test('T1w', list(range(4, 11)), *a))
    if S.nobs_ev[:, 14].sum() >= 10:
        out['T1e'] = G3.family_test('T1e', [14], *a)
    else:
        out['T1e'] = dict(test='T1e', r1=None, N_obs_B1=float(S.nobs_ev[:, 14].sum()), branch='-> T3',
                          note='F0e>1.3 has < 10 B1 counts: the dE/dx family falls to T3 (WP_RULE §6.2)')
    out['trend'] = G3.trend_test(list(range(3, 14)), S.nobs_ev, S.ntr1_ev, S.s2_ev, S.ntr2_ev, S.bi1, S.bi2)
    # conservative reading of T1 (as G3): the more severe of reading A (r1 = R04) and reading B
    sev = G3.SEVERITY
    out['T1_governing_branch'] = max([out['T1'].get('branch'), out['T1_readingB'].get('branch')],
                                     key=lambda b: sev.get(b, 3))
    return out


def family_correction(test, branch):
    """-> (central factor, sigma_ln term) of one family's closure test (WP_RULE §6.4 failure paths; USER 2026-10-14)."""
    if test is None or test.get('ratio') is None:
        return 1.0, 0.0, 'untestable'
    r = float(test['ratio']); lnr = abs(np.log(r))
    if branch is None or branch == 'nominal':
        return 1.0, 0.0, 'nominal'
    if 'missing lever arm' in branch:      # REVIEW R1 B-2: failure of UNKNOWN direction never lowers B
        return max(r, 1.0), lnr, 'missing lever arm: central x max(N_obs/N_pred, 1), |ln(N_obs/N_pred)| in sigma_ln'
    if branch.startswith('anti-conservative'):
        return r, 0.0, 'anti-conservative: central x N_obs/N_pred (upper envelope applied separately)'
    if branch == 'conservative':
        return 1.0, lnr, 'conservative: thinning uncorrected, |ln(N_obs/N_pred)| in sigma_ln'
    return 1.0, 0.0, branch


def compounded(cl, rung_families):
    """Compound the per-family corrections over the families a rung contains (cumulative ladder; never cancelled).
    rung_families: set of families ('counting', 'wchi', 'dedx', 'f1')."""
    fac = 1.0; s2 = 0.0; parts = {}
    gov = {'counting': ('T1', cl['T1_governing_branch']), 'wchi': ('T1w', cl['T1w'].get('branch'))}
    if cl['T1e'].get('r1') is not None:
        gov['dedx'] = ('T1e', cl['T1e'].get('branch'))
    for fam in ('counting', 'wchi', 'dedx'):
        if fam in rung_families and fam in gov:
            t, br = gov[fam]
            if t == 'T1':                  # C-8: reading A or B with the governing branch; on a tie the larger ratio
                cands = [x for x in (cl['T1'], cl['T1_readingB']) if x.get('branch') == br]
                test = max(cands, key=lambda x: x.get('ratio') or 0.0) if cands else cl['T1']
            else:
                test = cl[t]
            f, s, why = family_correction(test, br)
            fac *= f; s2 += s * s
            parts[t] = dict(branch=br, factor=f, sigma_ln=s, why=why)
    return fac, np.sqrt(s2), parts


def families_of_column(col):
    """Families contained in in-job column col (cumulative)."""
    n = C.RUNGS[col]
    fam = {'counting'}
    if col >= 4 and col <= 13:
        fam.add('wchi')
    if col in (14, 15, 16):
        fam |= {'wchi', 'dedx'}
    if 17 <= col <= 36:
        fam.add('wchi')
        if 'e>' in n:
            fam.add('dedx')
    return fam


def trend_sigma(cl, x_rung):
    """Trend term at ladder position x (1..23): |fitted ln r| (G3 convention, trend.extrapolated_ln_r); anti-conservative
    trend also scales the central value by exp(fitted ln r) when positive."""
    tr = cl['trend']
    if not tr.get('significant'):
        return 0.0, 1.0
    lnr = tr['intercept_at_x0'] + tr['slope'] * x_rung
    if tr['direction'] == 'anti-conservative':
        return abs(lnr), float(np.exp(max(lnr, 0.0)))
    return abs(lnr), 1.0


# ================================================================================================ zero-count rule
class Term:
    """Product of measured factors with the WP_RULE §4.2 zero/low-count rule."""

    def __init__(self, name):
        self.name = name; self.f = []

    def add(self, label, N, M, s_ln=None, value=None):
        """A measured conditional N/M (M >= 10 required by the caller) or a fixed value (value=, s_ln)."""
        self.f.append(dict(label=label, N=float(N) if N is not None else None, M=float(M) if M is not None else None,
                           value=value, s_ln=s_ln))

    def evaluate(self):
        zeros = [i for i, x in enumerate(self.f) if x['value'] is None and x['N'] == 0]
        bound = max(zeros, key=lambda i: (self.f[i]['M'], -i)) if zeros else None
        val = 1.0; s2 = 0.0; used = []
        for i, x in enumerate(self.f):
            if x['value'] is not None:
                v, s = x['value'], (x['s_ln'] or 0.0)
            elif x['N'] > 0:
                v = x['N'] / x['M']
                s = max(x['s_ln'] or 0.0, 1.0 / np.sqrt(x['N']))
            elif i == bound:
                v, s = LN114 / x['M'], 1.0
            else:
                v, s = 1.0, 0.0
            val *= v; s2 += s * s
            used.append(dict(x, used=v, s_ln_used=s, zero_bound=(i == bound)))
        return dict(value=val, s_ln=float(np.sqrt(s2)), zero_branch=bound is not None, factors=used)


def boot_ratio_sigma(Ne, Me, bi):
    """sigma_ln of sum N / sum M from the event bootstrap (per-event arrays)."""
    if Ne.sum() <= 0:
        return None
    pb = Ne[bi].sum(1) / np.maximum(Me[bi].sum(1), 1e-300)
    pb = pb[pb > 0]
    return float(np.std(np.log(pb), ddof=1)) if len(pb) > 10 else None


# ================================================================================================ B1 records
REQ = {}


def req_flags(c):
    """Single added requirement of every ladder column + F1 helpers (WP_RULE §3) on S2 records."""
    a, aligned = G3.req_flags(c)
    return a, aligned


class B1Records:
    """B1 S2 records (R04 & aligned, tag bit0) as per-hit-set groups with per-event keys; F1 (h, o) computed on demand
    from the S4 hit records of the measuring population."""

    def __init__(self, jobs):
        self.jobs = jobs
        cols = []
        for jn, d in enumerate(jobs):
            c = d['cand']
            s2 = (c['tag'] & 1) > 0
            F = C.rung_flags(c['rungs'])
            evg = d['tr']['ev'][c['trial']].astype(np.int64) + 10_000_000 * jn
            rq, _al = G3.req_flags(c)
            dd = c['dedx'].astype(float)
            REQ = np.stack([rq[k] for k in range(14)] + [np.nan_to_num(dd, nan=-1.0) > e for e in C.E_MIN], 1)
            cols.append(dict(F=F[s2], REQ=REQ[s2], trial=c['trial'][s2].astype(np.int64) + 1_000_000 * jn,
                             group=c['group'][s2].astype(np.int64), ev=evg[s2], jn=np.full(s2.sum(), jn),
                             i=np.where(s2)[0], nroad=d['tr']['n_road'][c['trial'][s2]],
                             btl=(c['btl_n_band'][s2] > 0) if 'btl_n_band' in c else np.zeros(s2.sum(), bool),
                             full=(c['tag'][s2] & 4) > 0))
        self.R = {k: np.concatenate([x[k] for x in cols]) for k in cols[0]} if cols else {}
        self.gkey = self.R['trial'] * 100_000 + self.R['group'] if cols else np.zeros(0, int)
        ue, self.evi = np.unique(self.R['ev'], return_inverse=True) if cols else (np.zeros(0), np.zeros(0, int))
        self.E = len(ue)
        if cols:
            ug, self.gid = np.unique(self.gkey, return_inverse=True)
            self.ng = len(ug)
            self.gev = np.zeros(self.ng, np.int64)
            self.gev[self.gid] = self.evi
        else:
            self.gid = np.zeros(0, np.int64); self.ng = 0; self.gev = np.zeros(0, np.int64)
        self.h = np.full(len(self.gkey), np.nan); self.o = np.full(len(self.gkey), np.nan)
        self.f1_done = np.zeros(len(self.gkey), bool)

    def groups(self, mask):
        """Number of distinct groups with >= 1 member in mask, and per-event group counts."""
        f = np.zeros(self.ng, bool)
        f[self.gid[mask]] = True
        n = int(f.sum())
        if not n:
            return 0, np.zeros(self.E)
        return n, np.bincount(self.gev[f], minlength=self.E).astype(float)

    def compute_f1(self, mask, log=None, max_n=20000):
        """h, o for the records in mask that have a full hit record (S4).  Capped at max_n (first by order; flagged)."""
        cand = np.where(mask & self.R['full'])[0]
        capped = len(cand) > max_n
        if capped:      # a seeded RANDOM subsample of the measuring population (unbiased; ambiguity A27)
            cand = np.sort(np.random.default_rng([C.SEED, len(cand)]).choice(cand, max_n, replace=False))
        idx = cand[~self.f1_done[cand]]
        self.last_sample = np.zeros(len(self.gkey), bool)
        self.last_sample[cand] = True
        by_job = {}
        for k in idx:
            by_job.setdefault(int(self.R['jn'][k]), []).append(k)
        for jn, ks in by_job.items():
            d = self.jobs[jn]
            hits = {kk: v for kk, v in C.load_npz(d['path'], keys=('cand.normal', 'cand.axis'),
                                                  prefix=('hit.',)).items() if kk != 'meta'}
            hl = {(int(t), int(ci)): q for q, (t, ci) in enumerate(zip(hits['hit.trial'], hits['hit.cand']))}
            c = dict(d['cand'], normal=hits['cand.normal'], axis=hits['cand.axis'])
            for k in ks:
                i = int(self.R['i'][k])
                t = int(c['trial'][i]); ci = int(c['idx'][i])
                q = hl.get((t, ci))
                if q is None:
                    continue
                h = hits['hit.ref'][hits['hit.off'][q]:hits['hit.off'][q + 1]]
                pv = d['tr']['pv'][t]
                g = HR.geom(hits, h, pv, c['normal'][i], c['axis'][i])
                cm, cc, w = HR.core(g)
                self.h[k] = HR.h_var(g, cc, pv); self.o[k] = HR.o_var(g, cc)
                self.f1_done[k] = True
        if log:
            log(f'F1 computed on {len(idx)} B1 records (capped={capped})')
        return capped


def conditional(rec, parent_mask_fn, req_mask, chain_cols, nboot_idx):
    """Measure p(req | population) on the tightest population with M >= 10 along chain_cols (looser ancestors, tightest
    first).  parent_mask_fn(col) -> record mask of the population 'passes col'.  Per-hit-set groups."""
    for col in chain_cols:
        pm = parent_mask_fn(col)
        M, Me = rec.groups(pm)
        if M >= 10:
            N, Ne = rec.groups(pm & req_mask)
            s = boot_ratio_sigma(Ne, Me, nboot_idx) if N > 0 else None
            return dict(N=N, M=M, population=C.RUNGS[col] if isinstance(col, int) else str(col), s_ln=s)
    return dict(N=0, M=0, population=None, s_ln=None)


# ================================================================================================ B_PU per column
LADDER_REQ = C.LADDER_REQ
COL_REQ = C.COL_REQ
REQ_NAME = C.RUNGS[:14] + ['dE/dx>1.3', 'dE/dx>1.6', 'dE/dx>2.0']


VAR_OF_REQ = {0: 'cnt', 1: 'cnt', 2: 'cnt', 3: 'cnt', 4: 'w', 5: 'w', 6: 'w', 7: 'w', 8: 'p', 9: 'p', 10: 'p',
              11: '2s', 12: '2s', 13: '2s', 14: 'e', 15: 'e', 16: 'e'}


def chain_factors(rec, start_col, col, mask_extra, bi):
    """Single-requirement factorisation from ladder rung start_col to the requirement set of column col (WP_RULE §6.2
    step 3, §4.2).  Requirements not in the start prefix are added in ladder order.  Different variables are
    factorised (independence, covered by the c-test); the SAME variable is never factorised (its cuts are nested):
      * step q of variable v is measured as N(P & q) / N(P & q'), q' = the previous added cut of v, on the tightest
        population P (cumulative partial selection, else a looser ancestor) with N(P & q') >= 10;
      * if no such population exists, all factors of v are MERGED into one joint factor N(P & q) / N(P) on the tightest
        P with N(P) >= 10 among the populations WITHOUT an added cut of v (FIX R6) (reading A28: the literal per-step
        marginals would multiply nested tails of one variable, which is anti-conservative).
    -> list of factor dicts (label, N, M, s_ln, value)."""
    R = rec.R['REQ']
    base = rec.R['F'][:, start_col] & mask_extra
    todo = sorted(COL_REQ[col] - LADDER_REQ[start_col])
    pops = [(C.RUNGS[start_col], base)]
    out = []
    last = {}
    first = {}         # FIX R6 (INV_STATS_BKG item 2): index in pops of the first population with an ADDED cut of v
    for q in todo:
        v = VAR_OF_REQ[q]
        first.setdefault(v, len(pops))
        qp = last.get(v)
        sv = R[:, qp] if qp is not None else np.ones(len(base), bool)
        got = None
        for nm, m in reversed(pops):
            if rec.groups(m & sv)[0] >= 10:
                got = (nm, m); break
        if got is not None:
            nm, m = got
            M, Me = rec.groups(m & sv); N, Ne = rec.groups(m & sv & R[:, q])
            lab = f'p({REQ_NAME[q]} | {nm}' + (f' & {REQ_NAME[qp]})' if qp is not None else ')')
            out.append(dict(label=lab, N=N, M=M, s_ln=boot_ratio_sigma(Ne, Me, bi) if N > 0 else None, value=None,
                            var=v))
        else:
            # FIX R6: the joint tail N(P & q)/N(P) (A28) is taken only on populations WITHOUT an added cut of v
            # (pops[:first[v]]); the frozen search over all pops could return P & q_first, i.e. the conditional
            # p(q | ... & q_first) while the factor p(q_first | ...) is dropped below (SR-T FB2 C12, SM FB0/FB1 rows)
            got = next(((nm, m) for nm, m in reversed(pops[:first[v]]) if rec.groups(m)[0] >= 10), None)
            out = [f for f in out if f.get('var') != v]          # merge: drop the earlier factors of v
            if got is None:
                out.append(dict(label=f'p({REQ_NAME[q]}) no population with M >= 10', N=None, M=None, value=1.0,
                                s_ln=1.0, var=v))
            else:
                nm, m = got
                M, Me = rec.groups(m); N, Ne = rec.groups(m & R[:, q])
                out.append(dict(label=f'p({REQ_NAME[q]} | {nm}) [joint tail of {v}, merged]', N=N, M=M,
                                s_ln=boot_ratio_sigma(Ne, Me, bi) if N > 0 else None, value=None, var=v))
        last[v] = q
        pops.append((pops[-1][0] + ' & ' + REQ_NAME[q], pops[-1][1] & R[:, q]))
    return out


def bpu_columns(S, cl, rec, c_factor, rng, nboot, log=print, t_cols=False):
    """B_PU per trial (P, sigma_ln components) for the 43 in-job columns (N_L2 diagnostics: thinning only)."""
    N1 = S.n1(); N2 = S.n2() if S.have_b2 else 0
    out = []
    reach = [c for c in range(14) if S.have_b2 and S.n2grp_ev[:, c].sum() >= 10]
    r_d = max(reach) if reach else None
    b1ok = [c for c in range(14) if S.nobs_ev[:, c].sum() >= 10]
    r_b = max(b1ok) if b1ok else None
    bi_rec = C.boot_idx(rec.E, nboot, rng) if rec.E else None
    extra = rec.R['btl'] if (t_cols and rec.E) else (np.ones(len(rec.gkey), bool) if rec.E else np.zeros(0, bool))

    def term(label, start_col, start_val, start_s, col):
        T = Term(label)
        T.add(f'P({C.RUNGS[start_col]}) start', None, None, s_ln=start_s, value=start_val)
        fs = chain_factors(rec, start_col, col, extra, bi_rec)
        for f in fs:
            T.add(f['label'], f['N'], f['M'], s_ln=f['s_ln'], value=f['value'])
        if fs and c_factor > 1:
            T.add('c (factorisation/independence, flagged)', None, None, s_ln=0.0, value=c_factor)
        return T.evaluate()

    def start_of(col, cand):
        """Deepest ladder rung <= cand whose requirement prefix is contained in the column's requirement set."""
        for s in range(cand, -1, -1):
            if LADDER_REQ[s] <= COL_REQ[col]:
                return s
        return None

    for col in range(C.NR):
        n_b1 = float(S.nobs_ev[:, col].sum())
        row = dict(column=C.RUNGS[col], B1_groups=n_b1, B1_per_trial=n_b1 / N1 if N1 else None)
        reachable = False
        if S.have_b2:
            p_thin = float(S.s2_ev[:, col].sum() / N2)
            reachable = bool(S.n2grp_ev[:, col].sum() >= 10)
            row.update(P_thin=p_thin, s_ln_thin_boot=sthin(S, col) if p_thin > 0 else None,
                       B2_groups=float(S.n2grp_ev[:, col].sum()), reachable_rho2=reachable)
        if col in COL_REQ and not reachable and r_d is not None and col not in LADDER_REQ or \
                (col in LADDER_REQ and r_d is not None and col > r_d):
            s0 = start_of(col, r_d)
            ft = term(f'B_PU main {C.RUNGS[col]}', s0, row_pthin(S, s0), sthin(S, s0), col)
            row.update(P_main=ft['value'], s_ln_main=ft['s_ln'], main_method=f'factorisation from {C.RUNGS[s0]} '
                       f'(not reachable at rho = 2)', main_factors=ft['factors'], zero_branch=ft['zero_branch'])
        else:
            row.update(P_main=row.get('P_thin'), s_ln_main=row.get('s_ln_thin_boot'), main_method='thinning',
                       zero_branch=False)
        if col in COL_REQ and r_b is not None:
            if col in LADDER_REQ and col <= r_b:
                row['P_fact'] = n_b1 / N1
            else:
                s0 = start_of(col, r_b)
                nb = float(S.nobs_ev[:, s0].sum())
                ft = term(f'factorisation model {C.RUNGS[col]}', s0, nb / N1, 1.0 / np.sqrt(nb), col)
                row.update(P_fact=ft['value'], s_ln_fact=ft['s_ln'], fact_zero_branch=ft['zero_branch'],
                           fact_factors=ft['factors'])
        row['P_pow'] = n_b1 / N1 if n_b1 >= 10 else None
        out.append(row)
    return out, dict(deepest_reachable_rho2=C.RUNGS[r_d] if r_d is not None else None,
                     deepest_B1_ge10=C.RUNGS[r_b] if r_b is not None else None)


def row_pthin(S, col):
    return float(S.s2_ev[:, col].sum() / S.n2())


def sthin(S, col):
    pb = S.s2_ev[S.bi2, col].sum(1) / S.ntr2_ev[S.bi2].sum(1)
    pb = pb[pb > 0]
    return float(np.std(np.log(pb), ddof=1)) if len(pb) > 10 else 1.0


def t3_correction(t3):
    """REVIEW R1 B-1: the T3 branch on every factorised column (WP_RULE §6.4 T3 + failure paths).  Degenerate or
    untestable T3 -> factor 1, flagged 'T3 non-informative' (the frozen rule has no branch for it: user told)."""
    if not t3 or t3.get('z') is None or t3.get('informative') is False or t3.get('ln_r') is None:
        return 1.0, 0.0, 'T3 non-informative (degenerate or untestable): no correction, flagged'
    z = t3['z']; lnr = t3['ln_r']
    if z > 2:
        return float(np.exp(lnr)), 0.0, 'T3 anti-conservative: x N_obs/N_pred'
    if z < -2:
        return 1.0, abs(lnr), 'T3 conservative: |ln(N_obs/N_pred)| in sigma_ln'
    return 1.0, 0.0, 'T3 pass'


def end_state(rows, cl, sigma_dens, sigma_norm, x_of_col, t3=None):
    """Apply the closure end state per column: compounded family corrections, upper envelope (anti-conservative),
    trend, density and normalisation terms; the T3 branch on factorised columns (B-1)."""
    anti = any(str(b).startswith('anti') for b in (cl['T1_governing_branch'], cl['T1w'].get('branch'),
                                                   cl['T1e'].get('branch')))
    out = []
    for col, r in enumerate(rows):
        fams = families_of_column(col)
        fac, s_cl, parts = compounded(cl, fams)
        models = {k: r.get(k) for k in ('P_main', 'P_fact', 'P_pow') if r.get(k) is not None and r.get(k) > 0}
        if not models:
            out.append(dict(column=r['column'], P=None, note='no estimate')); continue
        if anti or r.get('P_main') is None:     # no thinning estimate (e.g. no B2 yet): the upper envelope, flagged
            base = max(models.values()); s_model = float(np.log(max(models.values()) / min(models.values())))
            how = 'upper envelope of ' + '/'.join(models) + ('' if anti else ' (no thinning estimate: no B2)')
        else:
            base = r['P_main']; s_model = float(np.log(max(models.values()) / min(models.values()))) if len(models) > 1 \
                else 0.0
            how = r['main_method']
        s_tr, f_tr = trend_sigma(cl, x_of_col(col))
        s_stat = r.get('s_ln_main') or 0.0
        sd = sigma_dens(col)
        factorised = 'factorisation' in str(r.get('main_method')) or (anti and base == r.get('P_fact')
                                                                       and r.get('P_fact') != r.get('P_pow'))
        f3, s3, why3 = t3_correction(t3) if factorised else (1.0, 0.0, 'not factorised')
        comps = dict(stat=s_stat, model_spread=s_model, closure=s_cl, trend=s_tr, density=sd, normalisation=sigma_norm,
                     T3=s3)
        s = float(np.sqrt(sum(v * v for v in comps.values())))
        out.append(dict(column=r['column'], P_per_trial=float(base * fac * f_tr * f3), base=base, base_method=how,
                        closure_factor=fac, trend_factor=f_tr, closure_parts=parts, T3=why3, T3_factor=f3,
                        sigma_ln=s, sigma_ln_components=comps, reachable_rho2=bool(r.get('reachable_rho2')),
                        zero_branch=bool(r.get('zero_branch')) or bool(r.get('fact_zero_branch'))))
    return out


def x_of_col(col):
    """Ladder position (rung number) used by the trend extrapolation for in-job columns."""
    if col < 14:
        return col + 1
    if col in (14, 15, 16):
        return 21 + (col - 14)
    if 17 <= col <= 21:
        return 20                      # FB_k & h>5 & o>5: deepest ladder position its requirements reach (R20)
    if 22 <= col <= 36:
        return 21 + (col - 22) % 3     # FB_k e>x & h>5 & o>5: the dE/dx rung of the same level (R21-R23)
    return 4


# ================================================================================================ F1 factors
def f1_factors(rec, parent_cols, rng, nboot, log=print, max_n=20000, btl_only=False):
    """p(h > h_min | parent), p(h>5 & o > o_min | parent) measured on B1 S4 records (tightest population with M >= 10
    along the parent's ancestors), and the density-bin independence test (3 bins of road-hit count).  h/o computed on
    demand (cost ~ms per record)."""
    if not rec.E:
        return {}
    F = rec.R['F']
    bi = C.boot_idx(rec.E, nboot, rng)
    res = {}
    for pc in parent_cols:
        chain = C.supersets(pc)
        pop_col = None
        for c in chain:
            m = F[:, c] & (rec.R['btl'] if btl_only else True)
            if rec.groups(m)[0] >= 10:
                pop_col = c; break
        if pop_col is None:
            res[C.RUNGS[pc]] = dict(population=None, note='no population with M >= 10'); continue
        pm = F[:, pop_col] & (rec.R['btl'] if btl_only else True)
        capped = rec.compute_f1(pm, log=log, max_n=max_n)
        ok = pm & rec.f1_done & rec.last_sample
        hv, ov = rec.h, rec.o
        out = dict(population=C.RUNGS[pop_col], capped=capped, n_records=int(ok.sum()))
        M, Me = rec.groups(ok)
        hp = {t: ~np.isfinite(hv) | (hv > t) for t in C.H_MIN}            # undefined passes (§1.4 [D6])
        op = {t: ~np.isfinite(ov) | (ov > t) for t in C.O_MIN}
        for name, req in [(f'h>{t:g}', hp[t]) for t in C.H_MIN] + [(f'h>5&o>{t:g}', hp[5.0] & op[t]) for t in C.O_MIN]:
            N, Ne = rec.groups(ok & req)
            out[name] = dict(N=N, M=M, s_ln=boot_ratio_sigma(Ne, Me, bi) if N > 0 else None)
        # independence in 3 bins of road-hit count (WP_RULE §6.2 h/o row)
        nr = rec.R['nroad']
        q = np.quantile(nr[ok], [1 / 3, 2 / 3]) if ok.sum() > 3 else [0, 0]
        b = np.digitize(nr, q)
        req = hp[5.0] & op[5.0]
        bins = []
        for k in range(3):
            mk = ok & (b == k)
            Mk = rec.groups(mk)[0]; Nk = rec.groups(mk & req)[0]
            bins.append(dict(bin=k, N=Nk, M=Mk, p=Nk / Mk if Mk else None))
        ptot = out['h>5&o>5']['N'] / M if M else None
        ratios = [x['p'] / ptot for x in bins if x['p'] is not None and ptot]
        out['density_bins'] = bins
        out['c_density'] = max(ratios) if ratios else None
        res[C.RUNGS[pc]] = out
    return res


# ================================================================================================ density term
def density_sigma(nom_jobs, low_jobs, high_jobs):
    """PC-11 / WP_RULE §4.1: sigma_ln,dens(r) = max(|ln(P_up/P_nom)|, |ln(P_low/P_nom)|) at r if r has >= 10 per-hit-set
    counts in all three runs (same 2 000 events at nominal); deeper rungs take the deepest qualifying value."""
    def rate(jobs):
        n = sum(len(d['tr']['ev']) for d in jobs)
        if not n:
            return None, None
        g = sum(np.where(d['tr']['n_grp'] < 0, d['tr']['n_pass'], d['tr']['n_grp']).sum(0) for d in jobs)
        return g / n, g
    pn, gn = rate(nom_jobs); pl, gl = rate(low_jobs); ph, gh = rate(high_jobs)
    if pn is None or pl is None or ph is None:
        return dict(available=False, note='DENS low/high or nominal B1 (first 2 000 events) missing'), (lambda col: 1.0)
    vals = {}
    last = None
    for col in list(range(14)):
        ok = min(gn[col], gl[col], gh[col]) >= 10
        if ok:
            last = max(abs(np.log(ph[col] / pn[col])), abs(np.log(pl[col] / pn[col])))
        vals[C.RUNGS[col]] = dict(qualifies=bool(ok), counts=[float(gn[col]), float(gl[col]), float(gh[col])],
                                  sigma_ln=float(last) if last is not None else None)
    deepest = last

    def f(col):
        if col < 14 and vals[C.RUNGS[col]]['sigma_ln'] is not None:
            return vals[C.RUNGS[col]]['sigma_ln']
        return float(deepest) if deepest is not None else 1.0
    return dict(available=True, per_rung=vals, n_trials=[sum(len(d['tr']['ev']) for d in x)
                                                          for x in (nom_jobs, low_jobs, high_jobs)]), f


def rho_dens(b1_dump_paths, max_events=2000):
    """WP_RULE §8 PU-density update statistic from the S6 dumps: rho_dens = sum_l mu_c,l (Nbar_l / N_l(plan)) /
    sum_l mu_c,l over TBPX L1-L4 (pre-top-up, pre-CKF-removal Fatras measurements); trigger rho_dens > 1.05."""
    mu = np.array([8.0, 3.0, 1.5, 1.0]); nplan = np.array([6686, 4901, 3564, 2811.0])
    cnt = np.zeros(4); nev = 0
    for p in b1_dump_paths:
        with np.load(p, allow_pickle=False) as z:
            keys = sorted({k.split('.')[1] for k in z.files if k.startswith('dump.') and k.endswith('.sid')})
            for ek in keys:
                if nev >= max_events:
                    break
                sid = z[f'dump.{ek}.sid'].astype(np.int64)
                lc = C.FF.LC_OF[np.clip(sid, 0, len(C.FF.LC_OF) - 1)]
                for l in range(4):
                    cnt[l] += np.sum(lc == l)
                nev += 1
        if nev >= max_events:
            break
    if not nev:
        return dict(available=False)
    nbar = cnt / nev
    r = float(np.sum(mu * nbar / nplan) / mu.sum())
    return dict(available=True, n_events=nev, nbar_per_layer=nbar.tolist(), n_plan=nplan.tolist(), rho_dens=r,
                trigger=bool(r > 1.05), note='trigger -> eadm_dilution re-run with mu_c x rho_dens BEFORE any fallback '
                                             'signal efficiency (WP_RULE §8); this pipeline then refuses the A.2b table')


class SimpleRecords:
    """Candidate-level records (SM C, C') with the B1Records interface used by chain_factors (groups = candidates)."""

    def __init__(self, F, REQ, ev):
        self.R = dict(F=F, REQ=REQ)
        ue, self.evi = np.unique(ev, return_inverse=True) if len(ev) else (np.zeros(0), np.zeros(0, int))
        self.E = len(ue)
        self.gkey = np.arange(len(F))

    def groups(self, mask):
        n = int(mask.sum())
        return n, (np.bincount(self.evi[mask], minlength=self.E).astype(float) if n else np.zeros(self.E))


def req_matrix(c):
    rq, _al = G3.req_flags(c)
    dd = np.asarray(c['dedx'], float)
    return np.stack([rq[k] for k in range(14)] + [np.nan_to_num(dd, nan=-1.0) > e for e in C.E_MIN], 1)


def depth_term(T, rec, cnt_col_direct, n_den, col, bi, fallback_rec=None, label='', c_factor=1.0):
    """P(col) = N(deep)/n_den x chain_factors(deep -> col), deep = the deepest LADDER rung whose requirement prefix is
    contained in COL_REQ[col] (REVIEW R1 A-3: also for the F0e / FB columns 14-36) with >= 10 entries; 'no population'
    factors taken from fallback_rec (C'0); the independence c multiplies a non-empty chain (B-3).  -> deep."""
    F = rec.R['F']
    okd = [c for c in range(14) if C.LADDER_REQ[c] <= C.COL_REQ[col] and rec.groups(F[:, c])[0] >= 10]
    if not okd:
        T.add(f'{label} P(R01) direct', int(F[:, 0].sum()), max(n_den, 1))
        deep = 0
    else:
        deep = max(okd)
        wt = rec.R.get('wt')               # D1 same footing: preselection-weighted base count (SM)
        T.add(f'{label} P({C.RUNGS[deep]}) direct' + (' (presel-weighted)' if wt is not None else ''),
              float(wt[F[:, deep]].sum()) if wt is not None else int(F[:, deep].sum()), max(n_den, 1))
    fs = chain_factors(rec, deep, col, np.ones(len(F), bool), bi) if (C.COL_REQ[col] - C.LADDER_REQ[deep]) else []
    for f in fs:
        if f['N'] is None and fallback_rec is not None and fallback_rec.E:
            q = [k for k, nm in enumerate(REQ_NAME) if f['label'].startswith(f'p({nm})')]
            if q:
                F0 = fallback_rec.R['F']; R0 = fallback_rec.R['REQ']
                pop = F0[:, max(q[0] - 1, 0)] if q[0] < 14 else F0[:, 13]
                if pop.sum() >= 10:
                    T.add(f"{f['label']} -> C'0 factor", int((pop & R0[:, q[0]]).sum()), int(pop.sum()))
                    continue
        T.add(f['label'], f['N'], f['M'], s_ln=f['s_ln'], value=f['value'])
    if fs and c_factor > 1:
        T.add('c (factorisation/independence, global max)', None, None, value=c_factor, s_ln=0.0)
    return deep


# ================================================================================================ SM (C) term
SM_PSEUDO = {   # D3 (orchestrator 2026-10-14): W(tau nu) per tau-decay class, no double counting (hit-level samples)
    'Znunu_j': [('C_Znunu_j', None)],
    'Wtau_l': [('C_Wtaunu_j', 'lep')],
    'Wtau_h': [('C_Wtaunu_j', 'had'), ('C_Wtauhnu_j', 'had')],
    'ttbar_1l': [('C_ttbar_1l', None)],
}


def sm_term(jobs, sm_proc, lumi_pb, regen, log=print, rng=None, nboot=200, c_factor=1.0):
    """B_SM,HS per pseudo-sample (WP_RULE §7; D1/D3 FIXER R2): candidates with >= 1 hard-scatter in-band hit
    (n_hs_band >= 1, S2 records), each weighted by its event's generator-level PRESELECTION weight (eps_trig x pass,
    regenerated from the stored seeds and verified by the stored hs_met; gen_d123.py smregen), so that B_SM and N_trig
    share one preselection.  Depth by chain_factors (A28) with the zero-count rule; f_CKF < 0.2 as a rung factor.
    B = sigma x K x L x [sum_cand w (deep)] / N_class x chain.  W(e nu)/W(mu nu): no hit-level sample (C2-C future
    work) -> a FLAGGED conservative proxy: sigma K L f_presel x max over the W(tau) pseudo-samples of P(r)/f_presel."""
    rng = rng or np.random.default_rng(C.SEED)
    out = {}
    if regen is None:
        return dict(_error='SM regeneration (gen_d123 smregen) missing: B_SM not computable')
    regen = {k: v for k, v in regen.items() if not k.startswith('_')}
    bad = {jid: r for jid, r in regen.items() if r['n_met_match'] != r['n']}
    if bad:
        return dict(_error=f'SM regeneration does not reproduce the stored hs_met for {list(bad)[:5]}: refused')
    by = {}
    for d in jobs:
        by.setdefault(d['job']['sample'], []).append(d)
    pres = {}
    for ps, srcs in SM_PSEUDO.items():
        Fl, Rl, Ev, fck, Wl = [], [], [], [], []
        n_class = 0; sw_class = 0.0
        for sample, cls in srcs:
            for jn, d in enumerate(by.get(sample, [])):
                rows = regen[d['job_id']]['rows']
                tau = np.array([r['tau'] for r in rows]); wev = np.array([r['w_presel'] for r in rows], float)
                inc = np.ones(len(rows), bool) if cls is None else (tau == cls)
                n_class += int(inc.sum()); sw_class += float(wev[inc].sum())
                c = d['cand']
                m = ((c['tag'] & 1) > 0) & (c['n_hs_band'] >= 1)
                ie = (d['tr']['ev'][c['trial']] - int(d['job'].get('ev0', 0))).astype(np.int64)
                m &= inc[np.clip(ie, 0, len(inc) - 1)]
                Fl.append(C.rung_flags(c['rungs'])[m]); Rl.append(req_matrix(c)[m]); fck.append(c['f_ckf'][m])
                Ev.append(ie[m] + 10_000_000 * (jn + 1000 * len(Ev))); Wl.append(wev[ie[m]])
        F = np.concatenate(Fl) if Fl else np.zeros((0, C.NR), bool)
        R = np.concatenate(Rl) if Rl else np.zeros((0, 17), bool)
        ev = np.concatenate(Ev) if Ev else np.zeros(0, np.int64)
        wt = np.concatenate(Wl) if Wl else np.zeros(0)
        okf = np.nan_to_num(np.concatenate(fck), nan=1.0) < 0.2 if fck else np.zeros(0, bool)
        rec = SimpleRecords(F, R, ev); rec.R['wt'] = wt
        bi = C.boot_idx(rec.E, nboot, rng) if rec.E else None
        pp = sm_proc.get(ps) or {}
        sig = pp.get('sigma_pb'); K = pp.get('K')     # B = sigma K L x preselection-weighted P
        rows_out = []
        for col in range(37):
            T = Term(f'SM {ps} {C.RUNGS[col]}')
            deep = depth_term(T, rec, None, max(n_class, 1), col, bi, label='HS cand', c_factor=c_factor)
            pop = F[:, deep]
            if pop.sum() >= 10:
                T.add('f_CKF<0.2 (rung factor)', int((pop & okf).sum()), int(pop.sum()))
            ev_ = T.evaluate()
            B = ev_['value'] * sig * K * lumi_pb if (sig and K) else None
            rows_out.append(dict(column=C.RUNGS[col], P_per_event=ev_['value'], s_ln=ev_['s_ln'],
                                 zero_branch=ev_['zero_branch'], B=B, factors=ev_['factors']))
        f_cls = sw_class / max(n_class, 1)
        out[ps] = dict(n_class_events=n_class, f_presel_class=f_cls, n_hs_cand_R04=int(F[:, 3].sum()), sigma_pb=sig,
                       K=K, rows=rows_out)
        pres[ps] = f_cls
    # N_trig-only processes without a hit-level sample -- W(e nu), W(mu nu) (D3), tt 2l, single top, tW allowance,
    # WW, WZ, ZZ (REVIEW R2 B-1): FLAGGED conservative proxy B = N_trig,p x max over the closest-topology existing
    # pseudo-samples of P(r | preselected) (normalisation.json sm_processes[p].proxy_of)
    proxies = [pn for pn, pp in sm_proc.items() if pp.get('proxy')]
    for ps in proxies:
        pp = sm_proc[ps]
        srcs = pp.get('proxy_of') or ['Wtau_l', 'Wtau_h']
        rows_out = []
        for col in range(37):
            cands = []
            for w in srcs:
                if w in out and pres.get(w, 0) > 0 and out[w]['rows'][col]['B'] is not None:
                    cands.append((out[w]['rows'][col]['P_per_event'] / pres[w], out[w]['rows'][col], w))
            if not cands or not pp.get('N_trig'):
                rows_out.append(dict(column=C.RUNGS[col], B=None, s_ln=None, zero_branch=False)); continue
            pmax, src, wn = max(cands, key=lambda x: x[0])
            rows_out.append(dict(column=C.RUNGS[col], P_per_presel_event=pmax, B=pp['N_trig'] * pmax, s_ln=src['s_ln'],
                                 zero_branch=src['zero_branch'], proxy_of=wn))
        out[ps] = dict(proxy=True, flag='CONSERVATIVE PROXY (no hit-level sample): N_trig,p x max over ' + '/'.join(srcs) +
                                        ' of P(r | preselected)' + (' [N_trig is itself an ALLOWANCE]' if pp.get('allowance')
                                                                    else ''),
                       rows=rows_out, N_trig=pp.get('N_trig'), proxy_of=srcs)
    tot = [sum((v['rows'][c]['B'] or 0.0) for v in out.values()) for c in range(37)]
    prx = [sum((out[p]['rows'][c]['B'] or 0.0) for p in proxies if p in out) for c in range(37)]
    out['_proxy_fraction_of_B_SM'] = {C.RUNGS[c]: (prx[c] / tot[c] if tot[c] > 0 else None) for c in range(37)}
    return out


def hseed(*parts, mod=900_000_000):
    """Exact copy of code/s4pu.hseed (blake2b, little endian) -- s4pu itself imports pythia8."""
    import hashlib
    s = '|'.join(str(p) for p in parts)
    return int.from_bytes(hashlib.blake2b(s.encode(), digest_size=8).digest(), 'little') % mod


GUN_RANGE = {'gamma': ('log', 0.5, 50.0), 'v0': ('log', 0.5, 50.0), 'looper': ('lin', 0.05, 0.7),
             'ni22': ('log', 0.5, 20.0), 'ni30': ('log', 0.5, 20.0), 'ni61': ('log', 0.5, 20.0), 'dif': ('log', 0.5, 10.0)}
SPEC_KEY = {'gamma': 'gamma', 'v0': 'v0', 'looper': 'looper', 'ni22': 'ni', 'ni30': 'ni', 'ni61': 'ni', 'dif': 'dif'}


def gun_pt(topo, ev_seed):
    """Regenerate the gun parent pT and phi_MET of one C' event from its seed, replaying code/s4cp.CPrime.event's RNG
    draws in order (numpy only).  -> (pT or None for pvpair, phi_MET)."""
    rng = np.random.default_rng(hseed('cp', topo, ev_seed, mod=2 ** 63))
    rng.normal(0, 1, 4); rng.normal(0, 1, 3)
    phimet = rng.uniform(-np.pi, np.pi)
    rng.uniform(-0.1, 0.1)
    lg = lambda a, b: float(np.exp(rng.uniform(np.log(a), np.log(b))))          # noqa: E731
    if topo == 'gamma':
        return lg(0.5, 50.0), phimet
    if topo == 'v0':
        rng.random(); return lg(0.5, 50.0), phimet
    if topo == 'looper':
        rng.random(); rng.choice([-1.0, 1.0]); rng.uniform(-0.5, 0.5); return float(rng.uniform(0.05, 0.7)), phimet
    if topo.startswith('ni'):
        rng.choice([-1.0, 1.0]); return lg(0.5, 20.0), phimet
    if topo == 'dif':
        rng.random(); rng.choice([-1.0, 1.0]); return lg(0.5, 10.0), phimet
    return None, phimet


def spectrum_weight(topo, spectra):
    """w(pT) = f_Pythia(pT) / f_gun(pT), both normalised over the gun range (D2: fold the gun spectrum to Pythia)."""
    if topo not in GUN_RANGE or spectra is None or SPEC_KEY[topo] not in spectra['hist']:
        return None
    kind, a, b = GUN_RANGE[topo]
    edges = np.asarray(spectra['bins']); h = np.asarray(spectra['hist'][SPEC_KEY[topo]], float)
    lo = np.maximum(edges[:-1], a); hi = np.minimum(edges[1:], b)
    frac = np.clip((np.log(hi / lo) if kind == 'log' else (hi - lo)) /
                   (np.log(edges[1:] / edges[:-1]) if kind == 'log' else (edges[1:] - edges[:-1])), 0, 1)
    hpy = h * frac
    if hpy.sum() <= 0:
        return None
    gun = np.clip((np.log(hi / lo) / np.log(b / a)) if kind == 'log' else ((hi - lo) / (b - a)), 0, None)
    dens = np.where(gun > 0, (hpy / hpy.sum()) / np.maximum(gun, 1e-300), 0.0)

    def w(pt):
        k = np.clip(np.searchsorted(edges, pt) - 1, 0, len(dens) - 1)
        return float(dens[k])
    return w


# FIX R6 / D11: the non-dE/dx column of every dE/dx column (F0e>x -> R14; FB_k e>x -> FB_k)
E_BASE_COL = {**{14 + _x: 13 for _x in range(3)}, **{22 + 3 * _k + _x: 17 + _k for _k in range(5) for _x in range(3)}}


def _has_hit_records(d):
    """True if a C'0 output stores S4 hit records (needed to evaluate h, o on C'0 candidates)."""
    p = d.get('path')
    if p is None:
        return False
    with np.load(p, allow_pickle=False) as z:
        return 'hit.trial' in z.files


def cprime_term(cp0_jobs, cppu_jobs, rates, log=print, rng=None, nboot=200, c_factor=1.0, spectra=None):
    """WP_RULE §7: P(pass at r | t) = f_pre,t x P(pass at r | preselected t, PU) (NI/DIF) or the gun P(pass | t, PU);
    depth by chain_factors on the ATTRIBUTED C'_PU candidates from the deepest rung with >= 10, with C'0 factors where
    C'_PU has no population; f_CKF < 0.2 as a rung factor; zero-count rule.  B_t = N_trig rate_t P (in wp.py)."""
    rng = rng or np.random.default_rng(C.SEED)
    out = {}
    by0 = {}; byp = {}
    for d in cp0_jobs:
        by0.setdefault(d['job']['topo'], []).append(d)
    for d in cppu_jobs:
        byp.setdefault(d['job']['topo'], []).append(d)

    def recs(js):
        Fl, Rl, Ev, fk = [], [], [], []
        is_pu = False; slot_src = []
        for jn, d in enumerate(js):
            dc = d['d_cp']
            if 'cp.ev' in dc and 'src' in str(dc.get('cp.ev_cols', '')):
                is_pu = True; slot_src += [int(x) for x in dc['cp.ev'][:, 1]]
            cc = {k[8:]: dc[k] for k in dc if isinstance(k, str) and k.startswith('cp.cand.')}
            if not cc or 'attributed' not in cc:
                continue
            a = cc['attributed'].astype(bool)
            Fl.append(C.rung_flags(cc['rungs'])[a]); Rl.append(req_matrix(cc)[a]); fk.append(cc['f_ckf'][a])
            if 'cp.ev' in dc and 'trials.ev' in dc and dc['cp.ev'].shape[1] >= 2 and 'src' in str(dc.get('cp.ev_cols', '')):
                # B-7: C'_PU clusters by SOURCE C'0 event (re-overlays of one source are correlated)
                ie = np.asarray(dc['trials.ev'])[cc['trial'][a]].astype(np.int64)
                Ev.append(dc['cp.ev'][ie, 1].astype(np.int64))
            else:
                Ev.append(cc['trial'][a].astype(np.int64) + 10_000_000 * jn)
        F = np.concatenate(Fl) if Fl else np.zeros((0, C.NR), bool)
        R = np.concatenate(Rl) if Rl else np.zeros((0, 17), bool)
        ev = np.concatenate(Ev) if Ev else np.zeros(0, np.int64)
        okf = np.nan_to_num(np.concatenate(fk), nan=1.0) < 0.2 if fk else np.zeros(0, bool)
        rr = SimpleRecords(F, R, ev)
        rr.src = ev if is_pu else None              # source C'0 event of every attributed C'_PU candidate
        rr.slot_src = slot_src                      # source C'0 event of every C'_PU slot (denominator)
        return rr, okf
    for t in sorted(set(by0) | set(byp)):
        js0 = by0.get(t, []); jsp = byp.get(t, [])
        n0 = 0; npre = 0; leak = 0; n_attr_pre = 0
        for d in js0:
            v = d['meta'].get('v410', {})
            n0 += int(v.get('n_events', 0)); npre += int(v.get('n_pre', 0)); leak += int(v.get('n_attr_nonpre_any_rung', 0))
            n_attr_pre += int(v.get('n_attr_pre_any_rung', 0))
        pre_topo = t not in ('gamma', 'v0', 'pvpair', 'looper')
        f_pre = (npre / n0) if (pre_topo and n0) else 1.0
        n_with = sum(len(d['tr']['ev']) for d in jsp)
        r0, okf0 = recs(js0)
        rp, okf = recs(jsp)
        rw = reweight_factor(t, js0, jsp, rp, spectra)          # D2: max(with, without) the Pythia-spectrum fold
        bi = C.boot_idx(rp.E, nboot, rng) if rp.E else None
        bi0 = C.boot_idx(r0.E, nboot, np.random.default_rng([C.SEED, 7])) if r0.E else None   # own stream (R6)
        # FIX R6 (INV_STATS_BKG §5 side finding (ii)): WP_RULE §7 'Low gun counts' -- a GUN topology with < 10 passes
        # in its C'_PU events at the loosest counting rung (R01) starts its depth from the C'0 factors under §4.2
        Fp = rp.R['F']
        n_r01_events = int(len(np.unique(rp.evi[Fp[:, 0]]))) if len(Fp) else 0
        gun_low = (not pre_topo) and n_with > 0 and n_r01_events < 10

        def row_term(col, e_from_c0):
            """One C' row as one §4.2 term.  e_from_c0 (D11 reading 'C'0'): depth on C'_PU for the column WITHOUT its
            dE/dx cut, times the C'0 dE/dx factor (tightest attributed-C'0 population with M >= 10, else 1)."""
            T = Term(f"C' {t} {C.RUNGS[col]}" + (" [dE/dx from C'0]" if e_from_c0 else ''))
            if pre_topo:
                T.add("f_pre (C'0)", npre, max(n0, 1))
                if leak > 0:                   # B-7: V4-10 failure path (WP_RULE §7)
                    corr = 1.0 + leak / max(n_attr_pre, 1)
                    T.add('V4-10 leak correction (1 + N_leak/N_attr,pre), FLAGGED', None, None, value=corr,
                          s_ln=float(abs(np.log(corr))))
            if gun_low:
                deep = depth_term(T, r0, None, n0, col, bi0, label="C'0 attributed (low gun count, WP_RULE §7)",
                                  c_factor=c_factor)
                F, ok_ = r0.R['F'], okf0
            else:
                dcol = E_BASE_COL[col] if e_from_c0 else col
                deep = depth_term(T, rp, None, n_with, dcol, bi, fallback_rec=r0, label="C'_PU attributed",
                                  c_factor=c_factor)
                F, ok_ = rp.R['F'], okf
                if e_from_c0:
                    x = sorted(C.COL_REQ[col] - C.COL_REQ[dcol])[0]
                    F0 = r0.R['F']; R0 = r0.R['REQ']
                    cd = conditional(r0, lambda c: F0[:, c], R0[:, x], C.supersets(dcol), bi0) if len(F0) else \
                        dict(N=0, M=0, population=None, s_ln=None)
                    if cd['M'] >= 10:
                        T.add(f"p({REQ_NAME[x]} | C'0 attributed {cd['population']}) [C'0 dE/dx factor, §7]",
                              cd['N'], cd['M'], s_ln=cd['s_ln'])
                    else:
                        T.add(f"p({REQ_NAME[x]}) C'0: no population with M >= 10", None, None, value=1.0, s_ln=1.0)
                    if c_factor > 1 and not (C.COL_REQ[dcol] - C.LADDER_REQ[deep]):   # chain was empty: c once
                        T.add('c (factorisation/independence, global max)', None, None, value=c_factor, s_ln=0.0)
            pop = F[:, deep]
            if pop.sum() >= 10:
                T.add('f_CKF<0.2', int((pop & ok_).sum()), int(pop.sum()))
            if rw.get('factor_used', 1.0) > 1.0:
                T.add('Pythia-spectrum fold: max(1, R_t) (D2)', None, None, value=rw['factor_used'], s_ln=0.0)
            return T.evaluate()
        rows = []
        for col in range(37):                                    # A-3: every COL_REQ column
            if pre_topo and npre == 0:         # B-7: N_pre = 0 -> f_pre under §4.2, conditional = 1, no C'_PU needed
                T = Term(f"C' {t} {C.RUNGS[col]}")
                T.add("f_pre (C'0), N_pre = 0", 0, max(n0, 1))
                ev_ = T.evaluate()
                rows.append(dict(column=C.RUNGS[col], P_given_t=ev_['value'], s_ln=ev_['s_ln'], zero_branch=True,
                                 factors=ev_['factors'], note='N_pre = 0 (WP_RULE §7 sampling)'))
                continue
            if n_with == 0:
                rows.append(dict(column=C.RUNGS[col], P_given_t=None, s_ln=None, zero_branch=False,
                                 missing="C'_PU outputs of this topology not available", factors=[]))
                continue
            ev_ = row_term(col, False)
            extra = {}
            if col in E_BASE_COL and not gun_low:
                # D11 (DECIDED, orchestrator 2026-10-16): the C' dE/dx factor is computed in BOTH readings -- measured
                # inside the C'_PU chain (implemented reading) and from C'0 (literal §7) -- and the LARGER P is used
                # (tie: the larger sigma_ln); both are recorded
                evB = row_term(col, True)
                useB = (evB['value'], evB['s_ln']) > (ev_['value'], ev_['s_ln'])
                extra['dedx_readings'] = {"C'_PU chain": dict(P=ev_['value'], s_ln=ev_['s_ln']),
                                          "C'0 factor": dict(P=evB['value'], s_ln=evB['s_ln']),
                                          'used': "C'0 factor" if useB else "C'_PU chain",
                                          'rule': 'D11: the larger P (conservative)'}
                if useB:
                    ev_ = evB
            rows.append(dict(column=C.RUNGS[col], P_given_t=ev_['value'], s_ln=ev_['s_ln'], zero_branch=ev_['zero_branch'],
                             factors=ev_['factors'], **extra))
        has_hits0 = any(_has_hit_records(d) for d in js0)
        out[t] = dict(n_c0=n0, n_pre=npre, f_pre=f_pre, v410_leak=leak, v410_pass=(leak == 0) if pre_topo else None,
                      spectrum_reweight=rw, low_gun_count=dict(applied=bool(gun_low), n_R01_events_cppu=n_r01_events,
                                                               rule='WP_RULE §7: gun topology with < 10 passes at R01 '
                                                                    "-> depth from the C'0 factors (FIX R6)"),
                      ho_c0=dict(measurable=False, cp0_hit_records=bool(has_hits0),
                                 note="D11: C'0 h/o factor = 1 (no rejection credited): " +
                                      ("C'0 outputs carry no S4 hit records" if not has_hits0 else
                                       "C'0 hit records present but h/o not evaluated -> 1 (>= any measured C'0 factor)")),
                      n_with_pu=n_with, n_attr_cppu=int(len(rp.R['F'])), n_attr_c0=int(len(r0.R['F'])), rows=rows,
                      rate=rates.get(t))
    return out


def reweight_factor(topo, js0, jsp, rp, spectra):
    """R_t = P(pass | t) with the gun parent pT reweighted to the Pythia spectrum / the unweighted one, from f_pre (C'0
    preselection) x P(attributed at the deepest rung with >= 10 | C'_PU).  The gun pT is regenerated from the stored
    event seeds and VERIFIED by reproducing the stored phi_MET of every C'0 event.  -> dict(R, factor_used = max(1, R))."""
    w = spectrum_weight(topo, spectra)
    if w is None:
        return dict(R=None, factor_used=1.0, note='no reweighting (pvpair: the gun already samples Pythia pairs) '
                                                  'or no spectrum')
    pt_of = {}; n_bad = 0; nw = 0.0; nw_pre = 0.0; n = 0; n_pre = 0
    for d in js0:
        cm = d['meta'].get('chain_meta', {})
        seeds = cm.get('event_seeds') or []
        E = d['d_cp'].get('cp.ev')
        if E is None or not len(seeds):
            continue
        ev0 = int(d['job'].get('ev0', 0))
        for row in E:
            g = int(row[0]); i = g - ev0
            pt, ph = gun_pt(topo, seeds[i])
            if abs(((ph - row[10]) + np.pi) % (2 * np.pi) - np.pi) > 1e-9:
                n_bad += 1
            pt_of[g] = pt
            ww = w(pt); n += 1; nw += ww
            pre = bool(row[1]) if topo in ('ni22', 'ni30', 'ni61', 'dif') else True
            n_pre += int(pre); nw_pre += ww * pre
    if n_bad:
        return dict(R=None, factor_used=1.0, n_phimet_mismatch=n_bad, note='gun RNG replay FAILED: no reweighting '
                                                                          '(flagged)')
    if not n:
        return dict(R=None, factor_used=1.0, note="no C'0 events")
    R_pre = (nw_pre / nw) / max(n_pre / n, 1e-300)
    R_deep = 1.0
    F = rp.R['F']
    if len(F):
        okd = [c for c in range(14) if F[:, c].sum() >= 10]
        if okd and rp.src is not None:
            dcol = max(okd)
            src_slots = rp.slot_src
            wsl = np.array([w(pt_of[s_]) if s_ in pt_of else 0.0 for s_ in src_slots])
            wc = np.array([w(pt_of[s_]) if s_ in pt_of else 0.0 for s_ in rp.src])
            pw = (wc * F[:, dcol]).sum() / max(wsl.sum(), 1e-300)
            pu = F[:, dcol].sum() / max(len(src_slots), 1)
            R_deep = pw / pu if pu > 0 else 1.0
    R = R_pre * R_deep
    return dict(R=float(R), R_fpre=float(R_pre), R_deep=float(R_deep), factor_used=float(max(1.0, R)),
                n_phimet_mismatch=0, n_c0_events=n)
