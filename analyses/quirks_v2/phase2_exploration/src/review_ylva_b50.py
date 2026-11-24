"""review_ylva_b50.py -- independent re-derivation of the rule-1 B50 from the subset-pass counts m, and of M of the Z term.

  nice -n 19 python3 -I review_ylva_b50.py <out.json>          (einstein; standard library only; about 1 CPU-minute)

Ylva (reviewer, rule 1(c)), 2026-11-23.  Imports no study script.  Every constant is transcribed below WITH the file
and the text that must stand on the cited line; `cite()` stops the script if the text is not there, and the line
numbers found are written to the output.  Reads: text sources, three small json files, and the member `meta` of the
61 classified-pilot outputs (file lists with the pilot writer's own sum of weights).  No signal file, no pilot event file.

Rule (frozen): B = sum_t (N_t / M_t) Gamma(m_t + 1) + min(med exp(s g), cap Exp(1));  B50 = median of >= 1e5 draws;
a reading >= 300 (1 - 0.003) pauses.   STR l.2730-2757, l.2949 (Df-11); ADD l.597-609.
Parts:
  A  empty pilot with the addendum's own random streams (re-implemented here): must equal addendum1_v4_stdout.txt l.66
  B  readings with counts, nd = 1e5: floors on the addendum streams, Gamma(m) from Python's generator (not numpy's)
  C  readings with counts, 1e6 fully independent draws (other seed, Gamma(m + 1) drawn directly), three values of M
  D  closed form: mean - skewness term of the Z term (no random numbers)
  M  M of the Z term from the writer's per-file sums of w_v1, with a rigorous bound on the low-weight class
"""
import glob
import json
import logging
import math
import random
import struct
import sys
import zipfile
from array import array
from pathlib import Path

log = logging.getLogger('review_ylva_b50')
QV2 = Path(__file__).resolve().parents[2]
P2 = QV2 / 'phase2_exploration'
F_BUD = QV2 / 'phase1_strategy/src/strategy_budget.py'
F_ADD = P2 / 'src/p2z_addendum1.py'
F_PART = P2 / 'outputs/partition_p2-c-part-0.json'
F_C = P2 / 'outputs/rule1_valid_c_ingvild_2026-11-23.json'
F_B = P2 / 'outputs/rule1_valid_b50_ingvild_2026-11-23.json'
F_TOVE = P2 / 'outputs/rule1_prelim_counts_tove_2026-11-19.json'
F_BJORN = P2 / 'review/review_bjorn_zdenominator_2026-11-19.json'
F_STDOUT = QV2 / 'phase1_strategy/outputs/addendum1_v4_stdout.txt'
CLS = '/nfs/cajuela/jdochoa/quirks_v2/data/p2c/pilot_class/p2-c-pilot-cls*/000/*.npz'
CITED = []
_TXT = {}


def cite(path, text, what, first=False):
    """line number (1-based) of the single line of `path` that contains `text`; stops if absent or not unique.
    first=True: the same statement stands twice in the file with the same value; the first one is cited."""
    if path not in _TXT:
        _TXT[path] = Path(path).read_text().split('\n')
    hits = [i + 1 for i, s in enumerate(_TXT[path]) if text in s]
    if len(hits) > 1:                                        # the same text inside a longer line elsewhere: keep the line that starts with it
        hits = [i for i in hits if _TXT[path][i - 1].startswith(text)]
    if first and hits:
        hits = hits[:1]
    if len(hits) != 1:
        raise SystemExit(f'cite: {text!r} found on lines {hits} of {path}')
    CITED.append(dict(what=what, file=str(Path(path).relative_to(QV2)), line=hits[0], text=text))
    return hits[0]


# ---- constants, each tied to its source line --------------------------------------------------------------------------------
NTRIG = 4.0848e7
cite(F_BUD, 'NTRIG = 4.0848e7', 'N_trig')
SM_V1 = {"Z(nunu)+j": 25078824.8, "W(tau_h)": 5407122.7, "W(e nu)": 2536644.1, "tt 1l": 2379799.0,
         "W(tau_l)": 2257327.6, "W(mu nu)": 2238036.6, "tW": 259273.4, "tt 2l": 212934.8, "WZ": 137419.5,
         "WW": 126435.9, "t-channel": 110124.9, "ZZ": 104504.5}
cite(F_BUD, 'SM_NTRIG_V1 = {"Z(nunu)+j": 25078824.8, "W(tau_h)": 5407122.7, "W(e nu)": 2536644.1, "tt 1l": 2379799.0,', 'SM N_trig (1/3)')
cite(F_BUD, '"W(tau_l)": 2257327.6, "W(mu nu)": 2238036.6, "tW": 259273.4, "tt 2l": 212934.8, "WZ": 137419.5,', 'SM N_trig (2/3)')
cite(F_BUD, '"WW": 126435.9, "t-channel": 110124.9, "ZZ": 104504.5}', 'SM N_trig (3/3)')
NZ = SM_V1["Z(nunu)+j"]
ADD_PLAN = {"Z(tautau)": 0.17 * 0.1 * NZ, "Z(ll) lost": 0.34 * 3.5e-3 * NZ}
cite(F_BUD, 'ADD_PLAN = {"Z(tautau)": 0.17 * 0.1 * NZ, "Z(ll) lost": 0.34 * 3.5e-3 * NZ}', 'planned additions Z(tautau), Z(ll)')
cite(F_BUD, 'SM_NTRIG = dict(SM_NTRIG_V1, **ADD_PLAN)', 'SM_NTRIG')
MJ_PLAN = 4e5
cite(F_BUD, 'MJ_PLAN, MJ_LO, MJ_HI = 4e5, 4e4, 4e6', 'multijets')
SMTOT = sum(SM_V1.values()) + sum(ADD_PLAN.values()) + MJ_PLAN          # N_t of the Z term
cite(F_ADD, 'SMTOT = sum(SM.values()) + MJ', 'N_t(Z) = all SM + multijets')
# pile-up term
R07 = 35 / 48000.0
cite(F_BUD, 'r07 = 35 / 48000.0', 'v1 direct R07 rate', first=True)          # repeated identically at l.1475
PU_R07 = NTRIG * R07
cite(F_BUD, 'PU_R07 = NTRIG * r07 ', 'pile-up at R07')
PU_R08 = (PU_R07 / (0.2470 / R07), PU_R07 / (49.72 / 0.2470))
cite(F_BUD, 'PU_R08 = (PU_R07 / (0.2470 / r07), PU_R07 / (49.72 / 0.2470))', 'pile-up at R08, two falls')
CHI0 = 2 / 35.0
cite(F_BUD, 'CHI = (2 / 35.0, 32 / 126.0, 12 / 32.0)', 'v1 fit-probability fraction R09')
cite(F_BUD, 'PU_R09 = tuple(x * CHI[0] for x in PU_R08)', 'pile-up at R09')
cite(F_BUD, 'pu9 = 0.5 * (PU_R09[0] + PU_R09[1])', 'R09 median = mean of the two')
PU9_MED = 0.5 * (PU_R08[0] + PU_R08[1]) * CHI0
CAP = NTRIG / 96000.0
cite(F_BUD, 'PU_CAP = -NTRIG / 96000 ', 'cap of the pile-up term (mean of the Exp)')
cite(F_BUD, 'PU9 = (pu9, 0.59, PU_CAP)', 'R09 pile-up row: width 0.59')
cite(F_BUD, 'bs.append(b + min(x, -PU9[2] * rnd.expovariate(1.0)))', 'the pile-up draw of d15_q')
R08_PILEUP = (87.9, 117.9, 148.0)
cite(F_ADD, 'R08_PILEUP=(87.9, 117.9, 148.0),', 'R08 pile-up medians')
cite(F_ADD, "PUS = [('R09', R.PU9)] + [(f'R08@{x:.0f}', (x, 0.43, R.PU_CAP)) for x in O['R08_PILEUP']]", 'four pile-up rows, R08 width 0.43')
PUS = [('R09', PU9_MED, 0.59)] + [(f'R08@{x:.0f}', x, 0.43) for x in R08_PILEUP]
TIE = 0.003
cite(F_ADD, 'TIE=0.003,', 'tie rule')
LIMIT = 300.0 * (1.0 - TIE)
cite(F_ADD, "LIMIT = 300.0 * (1.0 - O['TIE'])", 'limit')
# B1 terms and the hard-scatter term
F_HS = 1.5945 / 1.560
cite(F_ADD, 'F_HS=1.5945 / 1.560,', 'F_HS')
PART = json.loads(F_PART.read_text())
NF, ROAD = PART['n_fire'], PART['pool_in_road_per_interaction']
cite(F_PART, '"n_fire": 1500000,', 'partition firings')
cite(F_PART, '"pool_in_road_per_interaction": 0.3405126373648824,', 'pool in road')
CNT = {k: v['all'] for k, v in PART['counts'].items()}
CLASSES = dict(DIF=CNT['dif'] + CNT['k0l'], DIFC=CNT['difc'], NI22=CNT['ni22'], NI30=CNT['ni30'], NI61=CNT['ni61'],
               NIX=CNT['nix'], NIC=CNT['nic'])
cite(F_ADD, "CLASSES = dict(DIF=CNT['dif'] + CNT['k0l'], DIFC=CNT['difc'], NI22=CNT['ni22'], NI30=CNT['ni30'], NI61=CNT['ni61'],", 'B1 classes')
cite(F_ADD, "RATE = {k: 200.0 * ROAD * c / NF * O['F_HS'] for k, c in CLASSES.items()}", 'B1 rate per triggered event')
cite(F_ADD, "NT_MB = {k: v / O['F_HS'] for k, v in NT.items()}", 'minimum-bias share')
cite(F_ADD, 'NT_HS = sum(NT.values()) - sum(NT_MB.values())', 'hard-scatter share')
B1 = list(CLASSES)
NT = {t: NTRIG * 200.0 * ROAD * CLASSES[t] / NF for t in B1}             # minimum-bias share alone
NT['HS'] = sum(NT[t] for t in B1) * (F_HS - 1.0)
NT['Z'] = SMTOT
M_B1 = dict(DIF=4e6, DIFC=4e6, NI22=1e6, NI30=1e6, NI61=1e6, NIX=4e6, NIC=2e6, HS=2.0e6)
cite(F_ADD, 'S2 = dict(DIF=4e6, DIFC=4e6, NI22=1e6, NI30=1e6, NI61=1e6, NIX=4e6, NIC=2e6)', 'B1 sample sizes')
cite(F_ADD, "HS_SIZES={'H1': 2.0e6, 'H2': 2.0e5},", 'hs sample size H1')
M_PLAN = 2.3e6 * 0.4396
cite(F_ADD, 'PILOT_HS_GENERATED=2.3e6,', 'Z pilot generated')
cite(F_ADD, "M_FULL={'Z': 0.4396, 'W': 0.2657, 'tt': 0.1205}, LOW_CLASS={'Z': (0.0025, 0.05), 'W': (0.0516, 0.05), 'tt': (0.0946, 0.05)},", 'planned M fraction; low class weight 0.05')
cite(F_ADD, "return k_full, k_full * O['LOW_CLASS']['Z'][1] / 0.98, m_full", 'low-class events per count = k_full x 0.05 / 0.98')
LOWF = 0.05 / 0.98
ORDER = B1 + ['HS', 'Z', 'Zlow']
cite(F_ADD, "rnd = random.Random(f'{seed}|{tag}')", 'exponential stream seed')
cite(F_ADD, "rnd = random.Random(f'{seed}|pu')", 'pile-up stream seed')
cite(F_ADD, 'return s[int(f * len(s))]', 'quantile convention')
cite(F_STDOUT, 'empty pilot B50: R09 160.8 [16-84 %: 109-232]; R08 at pile-up 88 / 118 / 148: 238.3 / 262.3 / 283.8', 'approved empty-pilot row')


def kappa(m_z):
    """events in 3 ab^-1 per pilot count, by term, for a Z denominator m_z"""
    k = {t: NT[t] / M_B1[t] for t in B1 + ['HS']}
    k['Z'] = SMTOT / m_z
    k['Zlow'] = SMTOT * LOWF / m_z
    return k


def quant(v, f):
    s = sorted(v)
    return s[int(f * len(s))]


def pu_draw(rnd, med, s):
    x = med * math.exp(s * rnd.gauss(0, 1))
    return min(x, CAP * rnd.expovariate(1.0))


# ---- part M -----------------------------------------------------------------------------------------------------------------
def npz_meta(f):
    with zipfile.ZipFile(f) as z:
        b = z.read('meta.npy')
    if b[:6] != b'\x93NUMPY':
        raise SystemExit(f'{f}: not an npy member')
    off = 10 + struct.unpack('<H', b[8:10])[0] if b[6] == 1 else 12 + struct.unpack('<I', b[8:12])[0]
    return json.loads(b[off:].decode('utf-32-le').rstrip('\x00'))


def part_m():
    seen = {}
    for f in sorted(glob.glob(CLS)):
        for fm in npz_meta(f)['files']:
            if fm['stream'] != 'pilot.hs0.znn':
                continue
            if fm['path'] in seen or fm['n_classified_range'] != fm['n_events']:
                raise SystemExit(f"{fm['path']}: twice or partial")
            seen[fm['path']] = fm
    r = dict(n_files=len(seen), n_events=0, sum_w_writer=0.0, w_max=0.0, n_full=0, n_low=0, n_zero=0, sum_full_r4=0.0, sum_low_r4=0.0,
             low_max_r4=0.0, full_min_r4=9.0)
    for fm in seen.values():
        r['n_events'] += fm['n_events']
        r['sum_w_writer'] += fm['sum_w_v1']                  # the pilot writer's float(w.sum()), all events, unrounded (p2x_hs0.py)
        if abs(fm['w_sum'] - fm['sum_w_v1']) > 1e-6:         # the classifier's own unrounded sum of the same column
            raise SystemExit(f"{fm['path']}: classifier sum {fm['w_sum']} against writer {fm['sum_w_v1']}")
        r['w_max'] = max(r['w_max'], fm['w_max'])
        for k, n in fm['w_hist'].items():                    # weights rounded to 4 decimals (the source of Tove's M)
            w = float(k)
            if w >= 0.5:
                r['n_full'] += n; r['sum_full_r4'] += w * n; r['full_min_r4'] = min(r['full_min_r4'], w)
            elif w > 0:
                r['n_low'] += n; r['sum_low_r4'] += w * n; r['low_max_r4'] = max(r['low_max_r4'], w)
            else:
                r['n_zero'] += n
    if r['n_files'] != 460:
        raise SystemExit(f"{r['n_files']} Z files, expected 460")
    wm = r['w_max']
    half = 0.5e-4                                            # largest rounding error of one weight at 4 decimals
    r['M_rounded_hist'] = r['sum_full_r4'] / wm              # must reproduce Tove's number
    lo = r['sum_w_writer'] - (r['sum_low_r4'] + half * r['n_low'])
    hi = r['sum_w_writer'] - (r['sum_low_r4'] - half * r['n_low'])
    r['sum_w_full_bounds'] = [lo, hi]
    r['M_bounds'] = [lo / wm, hi / wm]                       # rigorous: exact total minus the low class within its rounding
    r['rounding_excess_total'] = r['sum_full_r4'] + r['sum_low_r4'] - r['sum_w_writer']
    return r


# ---- part A, B --------------------------------------------------------------------------------------------------------------
def streams(nd=100000, seed=7):
    es = []
    for i in range(len(ORDER)):
        rnd = random.Random(f'{seed}|t{i}')
        es.append(array('d', (rnd.expovariate(1.0) for _ in range(nd))))
    pus = {}
    for pl, med, s in PUS:
        rnd = random.Random(f'{seed}|pu')
        pus[pl] = array('d', (pu_draw(rnd, med, s) for _ in range(nd)))
    return es, pus


def part_ab(counts_by_reading, m_z, es, pus, gseeds=(1, 2, 3)):
    nd = len(es[0])
    out = {}
    k_plan = kappa(M_PLAN)
    base = [sum(k_plan[t] * es[i][j] for i, t in enumerate(ORDER)) for j in range(nd)]
    out['A_empty'] = {pl: quant([a + b for a, b in zip(base, pus[pl])], 0.5) for pl, _, _ in PUS}
    k = kappa(m_z)
    for name, cnt in counts_by_reading.items():
        res = {pl: [] for pl, _, _ in PUS}
        for gs in gseeds:
            rnd = random.Random(f'ylva|B|{name}|{gs}')
            tot = [0.0] * nd
            for i, t in enumerate(ORDER):
                m = cnt[t]
                e = es[i]
                if m > 0:
                    tot = [a + k[t] * (b + rnd.gammavariate(m, 1.0)) for a, b in zip(tot, e)]
                else:
                    tot = [a + k[t] * b for a, b in zip(tot, e)]
            for pl, _, _ in PUS:
                res[pl].append(quant([a + b for a, b in zip(tot, pus[pl])], 0.5))
        out['B_' + name] = res
    return out


# ---- part C -----------------------------------------------------------------------------------------------------------------
def part_c(counts_by_reading, m_values, nd=1000000):
    rnd = random.Random('ylva|C|2026-11-23')
    k0 = kappa(1.0)
    rest = array('d', bytes(8 * nd))
    for t in B1 + ['HS']:
        if any(c[t] for c in counts_by_reading.values()):
            raise SystemExit(f'{t}: a count; this part assumes zero counts in the B1 and hs terms')
        kt = k0[t]
        for j in range(nd):
            rest[j] += kt * rnd.expovariate(1.0)
    pus = {pl: array('d', (pu_draw(rnd, med, s) for _ in range(nd))) for pl, med, s in PUS}
    out = {}
    d = int(round(0.5 * math.sqrt(nd)))
    for name, cnt in counts_by_reading.items():
        gz = array('d', (rnd.gammavariate(cnt['Z'] + 1, 1.0) for _ in range(nd)))
        gl = array('d', (rnd.gammavariate(cnt['Zlow'] + 1, 1.0) for _ in range(nd)))
        out[name] = {}
        for ml, mz in m_values.items():
            kz, kl = SMTOT / mz, SMTOT * LOWF / mz
            core = [kz * a + kl * b + c for a, b, c in zip(gz, gl, rest)]
            r = {}
            for pl, _, _ in PUS:
                s = sorted(a + b for a, b in zip(core, pus[pl]))
                r[pl] = dict(B50=s[nd // 2], q16=s[int(0.16 * nd)], q84=s[int(0.84 * nd)], q0=s[0],
                             mc_err=0.5 * (s[nd // 2 + d] - s[nd // 2 - d]), n_below_limit=sum(1 for x in s[:1000] if x < LIMIT))
            out[name][ml] = r
            log.info('C %s %s: %s', name, ml, {pl: round(v['B50'], 1) for pl, v in r.items()})
    return out


# ---- part D -----------------------------------------------------------------------------------------------------------------
def part_d(cnt, m_z):
    """median ~ mean - kappa3 / (6 var) of the total (first Cornish-Fisher term); the pile-up mean by quadrature."""
    k = kappa(m_z)
    mean = sum(k[t] * (cnt[t] + 1) for t in ORDER)
    var = sum(k[t] ** 2 * (cnt[t] + 1) for t in ORDER)
    k3 = sum(2 * k[t] ** 3 * (cnt[t] + 1) for t in ORDER)
    out = dict(mean_without_pileup=mean, sd_without_pileup=math.sqrt(var), skew_term=k3 / (6 * var), z_term_median_wilson_hilferty=k['Z'] * (cnt['Z'] + 1) * (1 - 1 / (9 * (cnt['Z'] + 1))) ** 3)
    for pl, med, s in PUS:
        # E[min(X, Y)], X lognormal(med, s), Y = CAP Exp(1): integral over the normal g of med e^{s g} ... use E[min] = int_0^inf P(X > x) e^{-x/CAP} dx
        n, top = 20000, 40.0 * med
        h = top / n
        acc = 0.0
        for i in range(n):
            x = (i + 0.5) * h
            px = 0.5 * math.erfc(math.log(x / med) / (s * math.sqrt(2)))
            acc += px * math.exp(-x / CAP) * h
        out[pl] = dict(pileup_mean=acc, B50_closed_form=mean + acc - k3 / (6 * var))
    return out


def main(fout):
    logging.basicConfig(level=logging.INFO, format='%(message)s', stream=sys.stderr)
    C = json.loads(F_C.read_text()); Bj = json.loads(F_B.read_text())
    tove = json.loads(F_TOVE.read_text()); bjorn = json.loads(F_BJORN.read_text())
    lS = cite(F_C, ' "subS_R08_s0_with": {', 'table (S), R08, s = 0'); lF = cite(F_C, ' "subF_R08_s0_with": {', 'table (F), R08, s = 0')
    counts = {'S': {t: C['tables']['subS_R08_s0_with'][t] for t in ORDER}, 'F': {t: C['tables']['subF_R08_s0_with'][t] for t in ORDER}}
    for rd in 'SF':
        if C['tables'][f'sub{rd}_R08_s0_with']['LOWPT'] != 0:
            raise SystemExit('a low-pT count: the extra term is not implemented here')
    log.info('counts: S %s (C l.%d ff.), F %s (C l.%d ff.)', counts['S'], lS, counts['F'], lF)
    res = dict(script='review_ylva_b50.py', limit=LIMIT, N_t=NT, SMTOT=SMTOT, M_planned_Z=M_PLAN, pileup_rows=PUS, cap_mean=CAP, counts=counts)
    # N_t against the result file (comparison only)
    res['N_t_max_rel_diff_to_result_file'] = max(abs(NT[t] / Bj['N_t'][t] - 1) for t in B1 + ['HS', 'Z'])
    mm = part_m(); res['M'] = mm
    cite(F_TOVE, '"M_full_sum_w_over_wmax": 993887.3401020421', 'M (Tove, rounded weights)')
    cite(F_BJORN, '"M_full": 993885.9240774056,', 'M (Bjorn, unrounded weights of the 460 pilot files)')
    m_t, m_b = tove['z']['M_full_sum_w_over_wmax'], bjorn['M_full']
    mm.update(M_tove=m_t, M_bjorn=m_b, tove_reproduced_from_hist=abs(mm['M_rounded_hist'] - m_t) < 1e-6,
              bjorn_inside_bounds=mm['M_bounds'][0] <= m_b <= mm['M_bounds'][1], tove_inside_bounds=mm['M_bounds'][0] <= m_t <= mm['M_bounds'][1],
              bjorn_total_minus_writer_total=bjorn['sum_w_full'] + bjorn['sum_w_low'] - mm['sum_w_writer'],
              n_full_n_low_match_bjorn=(mm['n_full'], mm['n_low'], mm['n_zero']) == (bjorn['n_full'], bjorn['n_low'], bjorn['n_zero']))
    log.info('M: %s', json.dumps(mm))
    es, pus = streams()
    ab = part_ab(counts, m_t, es, pus); res.update(ab)
    res['A_empty_diff_to_result_file'] = {pl: ab['A_empty'][pl] - Bj['empty_check'][pl] for pl in ab['A_empty']}
    log.info('A empty %s diff %s', ab['A_empty'], res['A_empty_diff_to_result_file'])
    for rd in 'SF':
        log.info('B %s %s', rd, {pl: [round(x, 1) for x in v] for pl, v in ab['B_' + rd].items()})
    res['C'] = part_c(counts, dict(tove=m_t, bjorn=m_b, planned=M_PLAN))
    res['D'] = {rd: {ml: part_d(counts[rd], mz) for ml, mz in (('tove', m_t), ('bjorn', m_b))} for rd in 'SF'}
    cmp_ = {}
    for rd in 'SF':
        for pl, _, _ in PUS:
            ing = Bj['readings'][f'sub{rd}_with']['by_pileup'][pl]
            c = res['C'][rd]['tove'][pl]
            cmp_[f'{rd} {pl}'] = dict(ingvild=ing['B50'], ingvild_q16=ing['q16'], ingvild_q84=ing['q84'], ingvild_mc_err=ing['mc_err'],
                                      ylva_C=c['B50'], ylva_C_q16=c['q16'], ylva_C_q84=c['q84'], ylva_C_mc_err=c['mc_err'],
                                      ylva_B_three_gamma_seeds=res['B_' + rd][pl], ylva_D_closed_form=res['D'][rd]['tove'][pl]['B50_closed_form'],
                                      diff_C=c['B50'] - ing['B50'], diff_C_in_sigma=(c['B50'] - ing['B50']) / math.hypot(c['mc_err'], ing['mc_err']),
                                      shift_bjorn_M=res['C'][rd]['bjorn'][pl]['B50'] - c['B50'], ylva_C_bjorn_M=res['C'][rd]['bjorn'][pl]['B50'],
                                      ylva_C_planned_M=res['C'][rd]['planned'][pl]['B50'], lowest_of_1e6_draws=c['q0'])
    res['comparison'] = cmp_
    res['cited'] = CITED
    Path(fout).write_text(json.dumps(res, indent=1))
    for k_, v in cmp_.items():
        log.info('%s: %s', k_, {a: (round(b, 2) if isinstance(b, float) else b) for a, b in v.items()})


if __name__ == '__main__':
    main(sys.argv[1])
