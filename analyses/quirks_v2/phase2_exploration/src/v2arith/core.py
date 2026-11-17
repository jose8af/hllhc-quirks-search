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
