"""common.py -- paths, rung map, admission (WP_RULE §5.4 item 11 + HASH_ADDENDUM), loading, bootstrap helpers.

Read-only on data/acts_stage4/prod/.  Nothing here makes a physics choice; every constant is a transcription of
acts/stage4/WP_RULE.md (sha256 1b2ea9bd...), WP_RULE_PC19.md, HASH_ADDENDUM.md or the LOG decisions of 2026-10-13/14.
"""
import hashlib
import json
import re
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent            # acts/stage4/analysis
S4 = HERE.parent                                  # acts/stage4
TT = S4.parents[1]                                # theory_track
PROD = TT / 'data' / 'acts_stage4' / 'prod'
DATA = TT / 'data' / 'acts_stage4'

from acts.stage4.finder import production as PR   # noqa: E402  (frozen; read-only use of constants)
from acts.stage4.finder import finder as FF       # noqa: E402

RUNGS = list(PR.RUNGS)                            # 43 in-job columns
NR = len(RUNGS)
NOGRP = set(PR.NOGRP)                             # union-only columns (R01-R03, N_L2 diagnostics)
COL = {n: i for i, n in enumerate(RUNGS)}
# WP_RULE §3 ladder: R01-R14 are in-job columns 0..13; R15-R23 are factorised (F1, offline)
LADDER_NAMES = RUNGS[:14] + ['R15_h>2', 'R16_h>3', 'R17_h>5', 'R18_o>2', 'R19_o>3', 'R20_o>5',
                             'R21_e>1.3', 'R22_e>1.6', 'R23_e>2.0']
H_MIN = (2.0, 3.0, 5.0)                           # WP_RULE §3 R15-R17
O_MIN = (2.0, 3.0, 5.0)                           # R18-R20
E_MIN = (1.3, 1.6, 2.0)                           # R21-R23 (MIP)
FAMILY_OF_RUNG = {**{r: 'counting' for r in range(1, 5)}, **{r: 'width' for r in range(5, 9)},
                  **{r: 'chi2core' for r in range(9, 12)}, **{r: '2S' for r in range(12, 15)},
                  **{r: 'h' for r in range(15, 18)}, **{r: 'o' for r in range(18, 21)},
                  **{r: 'dedx' for r in range(21, 24)}}
# WP_RULE §8 reporting rungs (tables of eps and B only, no limit)
REPORT_RUNGS = {'R_A': 'R04_IP2>=7', 'R_B': 'R06_w<18.75 (R_A + w_core<18.75)', 'R_C': 'R_A + w_core<4.7',
                'R_D': 'R14_2S2>=3', 'R_E': 'R23_e>2.0'}
W_K = (37.5, 18.75, 9.4, 4.7)                     # mm (k = 1..4)
# requirement sets of the in-job columns: indices 0..13 = the single added requirement of ladder rung R01..R14,
# 14..16 = dE/dx > 1.3 / 1.6 / 2.0 (WP_RULE §3, §8; production.full_set_flags)
LADDER_REQ = {col: set(range(col + 1)) for col in range(14)}
COL_REQ = dict(LADDER_REQ)
for _x in range(3):
    COL_REQ[14 + _x] = set(range(14)) | {14 + _x}
for _k in range(5):
    _base = {0, 1, 2, 3, 8, 9, 10, 11, 12, 13} | set(range(4, 4 + _k))
    COL_REQ[17 + _k] = set(_base)
    for _x in range(3):
        COL_REQ[22 + 3 * _k + _x] = _base | {14 + _x}


def supersets(col):
    """In-job columns whose selection CONTAINS column col's (requirement subset), tightest first, col itself first."""
    if col not in COL_REQ:
        return [col]
    cs = [c for c in COL_REQ if COL_REQ[c] <= COL_REQ[col]]
    return sorted(cs, key=lambda c: (-len(COL_REQ[c]), c != col, c))
DT_BX = 25.0
SIG_VP = 4000                                     # g1b_tt.SIG_VP (quirk interaction id)
GUN_VP = 3500
HS_VP = 3000
SEED = 20261014

# ------------------------------------------------------------------------------------------------ admission
WP_RULE_SHA = '1b2ea9bdad69e3cc599422811b74010b83d255057e346b7cd7a23143ad0b1c2a'
PC19_SHA = 'd30bcc2fd271de9fcc2111d6379bbe8cb897a81c36506b4332091f4fc04d5c8e'
ADDENDUM_SHA = 'e273c07756e6ec85856da11c23fd0120f5e4d7097416c2833fbbbf42480ad293'
FROZEN_INPUTS_SHA_TSEED4 = '2adc8f9d9e71fc6fc6763a5a4e74d157ae06773df7133ffcddccc3de42368928'
# HASH_ADDENDUM §1, §2, §5: the admitted post-freeze versions of the two changed files (all other A.3 files: frozen)
ADDENDUM_ALLOWED = {
    'acts/stage4/run_stage4.py': {
        '85b978f5d85cee28d290d298bb96bb9895299f916bc4df632a9cf2bb66a4879e': 'frozen (G3)',
        '1258e82a6ba0fd34d14c9aa6293075ef6e23bd6b90c0ff96298ef0b7dc07571c': 'G1b hook (§1)',
        '0d122cfc3fbc0d3baac92651260b7870c086d7b74153709997769d855518f5f9': 'T_seed:=4 re-timing + sub-runs (§5; C1a)',
        'e371c2b2ef6f3792380b5d38ab3e9d763134f71ce7cbee1891550c2aa22dca46': 'C2B ordering (§5 update; C1b, C2B)'},
    'acts/stage4/code/run_chain.py': {
        'b1130b40f6c729a1145d23ad15b8a176060d0cf3b718e8794f2efe5a9819e8c0': 'frozen (G3)',
        'bdea0e276e30473908f93b7b23e75d3876e4d6b43893b78077accf21f24aec8d': 'nav-assertion recovery (§2)'},
}
G1B_ALLOWED = {'acts/stage4/run_g1b.py': '0f8989bf9828c0de1b55499a309daedd90d80e0993c5935ed3d3c1821fe188ed',
               'acts/stage4/finder/g1b_tt.py': 'a2e4ddffe751628eb18a297731d5fd4bfeecb3f9b36937d4664a09f6bdfaaead'}
EXCLUDED_JOBS = {'G3B1_00021': 'ACTS nav failure (orchestrator 2026-10-13)',
                 'G3B1_00059': 'ACTS nav failure (orchestrator 2026-10-13)',
                 'G3B1_00077': 'ACTS nav failure (orchestrator 2026-10-14)'}
G1B_KINDS = ('a1', 'a2', 'a5', 'cp0', 'cppu')


def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


_FZ4 = None


def frozen_inputs_tseed4():
    global _FZ4
    if _FZ4 is None:
        p = S4 / 'frozen_inputs.json'
        if sha256(p) != FROZEN_INPUTS_SHA_TSEED4:
            raise RuntimeError('acts/stage4/frozen_inputs.json changed (REVIEW R1 C-2): refusing')
        _FZ4 = json.loads(p.read_text())
    return _FZ4


FREEZE_FILE = HERE / 'inputs' / 'analysis_freeze.json'
IMPORTED_FROZEN = ('acts/stage4/g3/analyse_g3.py', 'acts/stage4/g3/srt_tmin_check.py',    # C-6
                   'acts/stage4/code/s4pu.py', 'acts/stage4/code/s4cp.py', 'acts/stage4/code/s4sig.py',
                   'acts/stage4/jobs/C1.json',                                                # REVIEW R2 C-5
                   'acts/stage4/finder/finder.py', 'acts/stage4/finder/weights.py',           # REVIEW R3 C-6
                   'acts/stage4/finder/production.py', 'data/sim_stage3/STAGE3_INDEX.json',
                   'sim/stage3/results/P2.json',
                   'acts/stage4/investigation/V46_REVERT_SET.json', 'acts/stage4/jobs/A2FC.json')   # FIX R6 (V4-6 revert)


def freeze_sha():
    return sha256(FREEZE_FILE) if FREEZE_FILE.exists() else None


def provenance(dev, freeze_match, t_seed=None, campaigns=None):
    """REVIEW R3 B-1: the stamp every producing stage embeds in its own outputs (+ T_seed, campaigns: R4 C-1)."""
    return dict(dev=bool(dev), freeze_match=bool(freeze_match), freeze_sha256=freeze_sha(), t_seed=t_seed,
                campaigns=campaigns, created=time.strftime('%Y-%m-%d %H:%M:%S'))


def provenance_issues(prov, name):
    """Why an input may not feed a non-DEV output: missing stamp, DEV, unfrozen, or produced under another freeze."""
    if not isinstance(prov, dict):
        return [f'{name}: no embedded provenance stamp']
    out = []
    if prov.get('dev'):
        out.append(f'{name}: DEV')
    if not prov.get('freeze_match'):
        out.append(f'{name}: not produced with the frozen code/inputs')
    if prov.get('freeze_sha256') != freeze_sha():
        out.append(f'{name}: produced under another freeze ({str(prov.get("freeze_sha256"))[:12]})')
    return out


def freeze_targets():
    """Every analysis code and input file covered by the freeze (B-8; orchestrator 2026-10-14)."""
    fs = sorted(HERE.glob('*.py')) + sorted(p for p in (HERE / 'inputs').glob('*.json') if p.name not in
                                            ('analysis_freeze.json', 'fix_r1.json'))
    return [str(p.relative_to(TT)) for p in fs] + list(IMPORTED_FROZEN)


def freeze_status():
    """-> dict(match, frozen, current, mismatched).  match = every file has the frozen sha256."""
    cur = {f: sha256(TT / f) for f in freeze_targets()}
    if not FREEZE_FILE.exists():
        return dict(match=False, frozen=None, current=cur, mismatched=sorted(cur), note='no freeze file')
    fr = json.loads(FREEZE_FILE.read_text())['sha256']
    bad = sorted(f for f in set(cur) | set(fr) if cur.get(f) != fr.get(f))
    return dict(match=not bad, frozen=fr, current=cur, mismatched=bad)


def a3_hashes():
    """WP_RULE.md Appendix A.3 (parsed exactly as analyse_g3.frozen_hashes)."""
    txt = (S4 / 'WP_RULE.md').read_text()
    return dict(re.findall(r'\| `([^`]+)` \| `([0-9a-f]{64})` \|', txt.split('### A.3')[1].split('### A.4')[0]))


def governing_docs():
    """sha256 of the governing documents; the run refuses if WP_RULE / PC19 / HASH_ADDENDUM changed."""
    out = {}
    for f, ref in (('WP_RULE.md', WP_RULE_SHA), ('WP_RULE_PC19.md', PC19_SHA), ('HASH_ADDENDUM.md', ADDENDUM_SHA)):
        h = sha256(S4 / f)
        out[f] = dict(sha256=h, expected=ref, ok=h == ref)
    out['frozen_inputs.json'] = dict(sha256=sha256(S4 / 'frozen_inputs.json'), expected=FROZEN_INPUTS_SHA_TSEED4)
    out['frozen_inputs.json']['ok'] = out['frozen_inputs.json']['sha256'] == FROZEN_INPUTS_SHA_TSEED4
    return out


def admission(meta, kind, expect_tseed, a3=None):
    """WP_RULE §5.4 item 11 as amended by HASH_ADDENDUM (§1-§6, accepted as part of A.3 by the orchestrator,
    2026-10-14 00:35/01:50).  A job is admitted iff:
      * every A.3 file it records has the A.3 sha256, except run_stage4.py / run_chain.py which may carry one of the
        HASH_ADDENDUM versions;
      * its recorded WP_RULE.md sha256 is 1b2ea9bd...;
      * its frozen_inputs are frozen and its finder T_seed equals expect_tseed (4: C1/C2 production; 6: G3 only);
      * G1b kinds: run_g1b.py / g1b_tt.py have the HASH_ADDENDUM 'new files' sha256.
    Returns dict(ok, reasons, tseed, ...)."""
    a3 = a3 or a3_hashes()
    cs = meta.get('code_sha256', {}) or {}
    reasons = []
    for f, h in a3.items():
        if f not in cs:
            continue
        if cs[f] == h:
            continue
        if f in ADDENDUM_ALLOWED and cs[f] in ADDENDUM_ALLOWED[f]:
            continue
        reasons.append(f'{f}: {cs[f][:12]} not A.3/addendum')
    if cs.get('acts/stage4/WP_RULE.md') != WP_RULE_SHA:
        reasons.append('WP_RULE sha mismatch')
    fz = meta.get('frozen_inputs') or {}
    if not fz.get('frozen'):
        reasons.append('frozen_inputs not frozen')
    if expect_tseed == 4 and fz != frozen_inputs_tseed4():      # REVIEW R1 C-2: the job's frozen inputs = the file
        reasons.append('meta.frozen_inputs differs from acts/stage4/frozen_inputs.json (2adc8f9d...)')
    for f in a3:                                                 # C-2: A.3 code files must be recorded by the job
        if f.startswith('acts/stage4/') and f.endswith('.py') and 'probes' not in f and 'eadm' not in f \
                and f not in cs:
            reasons.append(f'{f}: not recorded in code_sha256')
    tseed = (meta.get('finder_cfg') or {}).get('tseed')
    if tseed != expect_tseed:
        reasons.append(f'T_seed {tseed} != {expect_tseed}')
    if kind in G1B_KINDS:
        gs = meta.get('g1b_sha256', {}) or {}
        for f, h in G1B_ALLOWED.items():
            if gs.get(f) != h:
                reasons.append(f'{f}: g1b sha mismatch')
    rep = (meta.get('chain_meta') or {}).get('replaced_events') or []
    return dict(ok=not reasons, reasons=reasons, tseed=tseed, n_replaced_events=len(rep),
                other_code=dict((k, v) for k, v in cs.items() if k not in a3))


# ------------------------------------------------------------------------------------------------ manifests
def manifest(camp):
    return json.loads((S4 / 'jobs' / f'{camp}.json').read_text())['jobs']


def job_files(camps, kinds=None, samples=None, prod=PROD):
    """[(job, path or None)] for the manifests of the given campaigns (job dicts as in jobs/<C>.json)."""
    out = []
    for c in camps:
        for j in manifest(c):
            if kinds and j['kind'] not in kinds:
                continue
            if samples and j['sample'] not in samples:
                continue
            p = prod.joinpath(*j['out'].split('/'))
            out.append((j, p if p.is_file() else None))
    return out


def load_npz(p, keys=None, prefix=None):
    """Load selected arrays (all if keys is None and prefix is None) + parsed meta."""
    out = {}
    with np.load(p, allow_pickle=False) as z:
        fl = z.files
        for k in fl:
            if k == 'meta_json':
                continue
            if keys is not None and k not in keys and not (prefix and any(k.startswith(x) for x in prefix)):
                continue
            out[k] = z[k]
        out['meta'] = json.loads(str(z['meta_json'])) if 'meta_json' in fl else {}
    return out


def collect(camps, kinds, expect_tseed, samples=None, keys=None, prefix=None, max_jobs=0, prod=PROD, log=None):
    """Load admitted, complete job outputs.  Returns (list of dict(job, path, d), status dict)."""
    a3 = a3_hashes()
    st = dict(manifest=0, missing=[], excluded=[], invalid=[], not_admitted={}, used=0, replaced_events=0,
              input_sha256={})
    res = []
    for j, p in job_files(camps, kinds, samples, prod):
        st['manifest'] += 1
        if j['id'] in EXCLUDED_JOBS:
            st['excluded'].append(j['id']); continue
        if p is None:
            st['missing'].append(j['id']); continue
        if max_jobs and len(res) >= max_jobs:
            continue
        try:
            d = load_npz(p, keys=keys, prefix=prefix)
        except Exception as e:                                  # noqa: BLE001
            st['invalid'].append(f"{j['id']}: {e}"); continue
        jid = str(d.get('job_id', '')) if 'job_id' in d else None
        if jid is None:
            with np.load(p, allow_pickle=False) as z:
                jid = str(z['job_id']); comp = int(z['complete'])
        else:
            comp = int(d.get('complete', 1))
        if jid != j['id'] or comp != 1:
            st['invalid'].append(j['id']); continue
        ad = admission(d['meta'], j['kind'], expect_tseed, a3)
        if not ad['ok']:
            st['not_admitted'][j['id']] = ad['reasons']; continue
        st['replaced_events'] += ad['n_replaced_events']
        st['input_sha256'][str(p.relative_to(TT))] = sha256(p)
        res.append(dict(job=j, path=p, d=d))
        st['used'] += 1
    if log:
        log(f"collect {camps} {kinds}: used {st['used']}/{st['manifest']} (missing {len(st['missing'])}, "
            f"not admitted {len(st['not_admitted'])}, excluded {len(st['excluded'])})")
    return res, st


# ------------------------------------------------------------------------------------------------ statistics
def boot_idx(n, nboot, rng):
    return rng.integers(0, n, size=(nboot, n))


def ev_sums(ev_of_trial, x, n_ev):
    out = np.zeros((n_ev,) + np.shape(x)[1:])
    np.add.at(out, ev_of_trial, x)
    return out


def clopper_pearson(k, n, cl=0.6827):
    from scipy.stats import beta
    k = np.asarray(k, float); n = np.asarray(n, float)
    a = (1 - cl) / 2
    lo = np.where(k > 0, beta.ppf(a, k, n - k + 1), 0.0)
    hi = np.where(k < n, beta.ppf(1 - a, k + 1, n - k), 1.0)
    return lo, hi


def rung_flags(packed):
    return np.unpackbits(packed, axis=1)[:, :NR].astype(bool)


def jdump(obj, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)

    def dflt(o):
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return None if not np.isfinite(o) else float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, Path):
            return str(o)
        return str(o)
    txt = json.dumps(obj, indent=1, default=dflt, allow_nan=True)
    txt = txt.replace('NaN', 'null').replace('-Infinity', '"-inf"').replace('Infinity', '"inf"')
    Path(path).write_text(txt)


def logger(path=None):
    def log(msg):
        line = time.strftime('%H:%M:%S ') + str(msg)
        print(line, flush=True)
        if path:
            with open(path, 'a') as f:
                f.write(line + '\n')
    return log
