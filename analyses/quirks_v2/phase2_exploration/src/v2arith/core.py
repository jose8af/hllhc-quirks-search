"""Core arithmetic of v2arith (see the package docstring for every convention and its v1 source)."""
from dataclasses import dataclass, field

import numpy as np

ZERO_COUNT = 1.14                  # 68 % upper value of a zero count (WP_RULE §4.2; v1 background.LN114)
SHARED = ('density', 'model_spread', 'normalisation', 'closure', 'trend', 'srt_pv', 'srt_sigt', 'T3')
LUMI_PB = 3.0e6


@dataclass
class Factor:
    N: float = None                 # counted numerator (may be a weighted count)
    M: float = None                 # denominator (population)
    value: float = None             # fixed factor instead of N/M
    s_ln: float = None              # given log width (bootstrap etc.); counted factors use max(s_ln, 1/sqrt(N))


def chain(factors):
    """-> (P, s_ln, zero_branch, used) with the v1 zero/low-count rule."""
    zeros = [i for i, f in enumerate(factors) if f.value is None and f.N == 0]
    bound = max(zeros, key=lambda i: (factors[i].M, -i)) if zeros else None
    P, s2, used = 1.0, 0.0, []
    for i, f in enumerate(factors):
        if f.value is not None:
            v, s = f.value, (f.s_ln or 0.0)
        elif f.N > 0:
            v, s = f.N / f.M, max(f.s_ln or 0.0, 1.0 / np.sqrt(f.N))
        elif i == bound:
            v, s = ZERO_COUNT / f.M, 1.0
        else:
            v, s = 1.0, 0.0
        P *= v; s2 += s * s; used.append((v, s))
    return P, float(np.sqrt(s2)), bound is not None, used


def sm_value(P, sigma_pb, K, lumi_pb=LUMI_PB):
    return P * sigma_pb * K * lumi_pb


def cprime_value(P, n_trig, rate, pv_line=1.0):
    return n_trig * rate * pv_line * P


def pu_value(n_trig, base, closure=1.0, trend=1.0, t3=1.0):
    return n_trig * base * closure * trend * t3


@dataclass
class Term:
    label: str
    value: float
    comps: dict = field(default_factory=dict)      # {component name: log width}


def sample_sum(terms, nmc, rng, zshared=None):
    zshared = {} if zshared is None else zshared
    tot = np.zeros(nmc)
    for t in terms:
        if t.value is None or t.value <= 0:
            continue
        lz = np.zeros(nmc)
        for name, s in t.comps.items():
            if not s:
                continue
            if name in SHARED:
                if name not in zshared:
                    zshared[name] = rng.standard_normal(nmc)
                z = zshared[name]
            else:
                z = rng.standard_normal(nmc)
            lz += s * z
        tot += t.value * np.exp(lz)
    return tot, zshared


def b84(terms, nmc=200_000, seed=1):
    s, _ = sample_sum(terms, nmc, np.random.default_rng(seed))
    return float(np.quantile(s, 0.84)), float(np.median(s)), float(np.mean(s))


def b84_analytic_single(value, s_ln):
    """One log-normal term: B84 = value exp(s_ln) (a closed form used by the unit tests)."""
    return value * float(np.exp(s_ln))


# ------------------------------------------------------------------ F1 (h, o) factors, SR-T time tag, trend (v1 wp.py)
def guarded(N, M, s_ln, holds_bound):
    """A zero count appended to a term that already holds its 1.14/M bound enters as 1 (WP_RULE §4.2: one bound per
    term; v1 wp.add_guarded)."""
    if N == 0 and holds_bound:
        return Factor(value=1.0, s_ln=0.0)
    return Factor(N=N, M=M, s_ln=s_ln)


def f1_conditional(fp, name):
    """F1 conditional p(name | population) of one parent column record, with the density-bin correlation factor c
    applied only if c - 2 sigma_c > 1 (sigma_c = c sqrt(1/N_bin + 1/N), bin of the largest p) (v1 wp.f1_factor)."""
    if not fp or fp.get("population") is None or name not in fp:
        return None
    x = fp[name]
    c = fp.get("c_density"); c_apply = 1.0
    if c is not None and c > 1:
        nb = [b for b in fp["density_bins"] if b["p"] is not None and b["M"]]
        if nb:
            b = max(nb, key=lambda q: q["p"])
            sc = c * np.sqrt(1 / max(b["N"], 1) + 1 / max(x["N"], 1)) if x["N"] else np.inf
            if c - 2 * sc > 1:
                c_apply = c
    return dict(N=x["N"], M=x["M"], s_ln=x.get("s_ln"), population=fp["population"], c=c_apply)


def times_f1(value, s_ln, zero_branch, f1x):
    """An SM or C' row x its F1 factor as one §4.2 term (v1 wp._f1_on_row): (value, s_ln, zero_branch)."""
    if f1x is None or f1x["M"] < 10:
        return value, s_ln, zero_branch
    P, s, zb, _ = chain([Factor(value=value, s_ln=0.0), guarded(f1x["N"], f1x["M"], f1x["s_ln"], zero_branch)])
    return P, float(np.hypot(s_ln, s)), zero_branch or zb


def pu_with_f1(p_per_trial, comps, zero_branch, f1x, n_trig):
    """SR-G PU term = column end state [x F1 factor (guarded) x c] (v1 wp.pu_term)."""
    fs = [Factor(value=p_per_trial, s_ln=0.0)]
    if f1x is not None:
        fs.append(guarded(f1x["N"], f1x["M"], f1x["s_ln"], zero_branch))
        if f1x["c"] > 1:
            fs.append(Factor(value=f1x["c"], s_ln=0.0))
    P, s, zb, _ = chain(fs)
    c = dict(comps); c["stat"] = float(np.hypot(c.get("stat", 0.0), s))
    return n_trig * P, c, zero_branch or zb


def srt_pu(esT, esA, f1x, srt, n_trig):
    """SR-T PU terms (PC-19): P(r & BTL) x P(late) and P(r & no BTL) x P_OOT (v1 wp.srt_pu_term).  -> [(name, value,
    comps)]; P(r & no BTL) = P(r) - P(r & BTL) only if both columns are reachable at rho = 2, else P(r)."""
    if esT.get("P_per_trial") is None or esA.get("P_per_trial") is None or srt is None:
        return []
    both = bool(esT.get("reachable_rho2")) and bool(esA.get("reachable_rho2"))
    p_t = esT["P_per_trial"]
    if both:
        p_nt, nt_src = esA["P_per_trial"] - p_t, esA
        if p_nt <= 0:
            p_nt, both = esA["P_per_trial"], False
    else:
        p_nt, nt_src = esA["P_per_trial"], esA
    out = []
    for nm, base, fac, src in (("present x P(late)", p_t, srt.get("P_late"), esT),
                               ("not present x P_OOT", p_nt, srt.get("P_oot"), nt_src)):
        zb = bool(src.get("zero_branch"))
        fs = [Factor(value=base, s_ln=0.0)]
        if f1x is not None:
            fs.append(guarded(f1x["N"], f1x["M"], f1x["s_ln"], zb))
        if fac is None or fac["M"] < 10:
            fs.append(Factor(value=1.0, s_ln=1.0))
        else:
            fs.append(guarded(fac["N"], fac["M"], None, zb))
            if nm.startswith("present") and srt.get("c_time", 1.0) > 1:
                fs.append(Factor(value=srt["c_time"], s_ln=0.0))
        P, s, _, _ = chain(fs)
        c = dict(src["sigma_ln_components"]); c["stat"] = float(np.hypot(c.get("stat", 0.0), s))
        c["srt_pv"] = srt.get("sigma_ln_PV", 1.0); c["srt_sigt"] = srt.get("sigma_ln_sigma_t", 1.0)
        out.append((nm, n_trig * P, c, src.get("trend_factor", 1.0)))
    return out


def trend_at(trend, x):
    """Trend term at ladder position x: |intercept + slope x| as width; an anti-conservative trend also scales the
    central value by exp(max(ln r, 0)) (v1 background.trend_sigma).  -> (sigma, factor)."""
    if not trend.get("significant"):
        return 0.0, 1.0
    lnr = trend["intercept_at_x0"] + trend["slope"] * x
    if trend["direction"] == "anti-conservative":
        return abs(lnr), float(np.exp(max(lnr, 0.0)))
    return abs(lnr), 1.0
