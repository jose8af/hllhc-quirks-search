"""Fix R4 (Stage-4 plan), review R4 C-2/C-3: frozen inputs of the fallback admissibility rule (plan §2.6), truth level.

(1) beta*gamma_IT(m) for all 17 p2 species-masses, recomputed from Stage-3 truth with the selection of the R1 constructive
    probe (data/acts_stage4/review_r1_constructive/r1c_signal_handles.py, which covered 5 species-masses only):
    template half (tt_split == 0), in_eta25 & status == 1, configuration BM; per event the median beta*gamma = |p|/m over
    the event's IT hits (both quirks, kind 'IT'); per (m, Lambda) point the median over events; beta*gamma_IT(m) = the
    median over ALL p2 Lambda points of that species-mass. Generator/truth kinematics only (no detector response, no PU,
    no efficiency). The probe rows of plan §2.5 item 10 are not removed (kinematics, not an efficiency; < 0.2 %).
(2) Lambda_R(m) (median l_max = R_IT): the per-mass value AND the smoothed value from sim/stage3/results/P2.json
    edge_fits_in_m (E: deg2 in ln m as HANDOVER §5.3 recommends; Etilde: deg1, the only fit stored for 3 masses).
    k_adm thresholds Lambda_R,s(m) * 2^((k+1)/2), k = 0..4.
(3) dE/dx admissibility EXPECTATION (ESTIMATE; Si constants recalled, UNVERIFIED, as review R4 r4_checks.py):
    (a) R_BB = Bethe mean loss / its minimum (review R4 convention);
    (b) the pre-declared R4 convention: restricted loss (T_cut) of the quirk / restricted loss of the calibration muon gun
        (pT 1-10 GeV, |eta| < 2.5; beta*gamma_mu ~ 10-100), i.e. directly in the muon-gun MIP-peak unit of e_min.
    e_adm = largest e in {1.3, 1.6, 2.0} with e <= ratio / 1.25.
Run (theory_track): pixi run python acts/stage4/probes/f4r_admissibility.py
Output: data/acts_stage4/fix_r4/f4r_admissibility.json
"""
import hashlib
import json
import math
from pathlib import Path

import numpy as np

TT = Path(__file__).resolve().parents[3]
S3 = TT / "data/sim_stage3"
P2 = TT / "sim/stage3/results/P2.json"
R1C = TT / "data/acts_stage4/review_r1_constructive/r1c_signal_handles.json"
OUT = TT / "data/acts_stage4/fix_r4"
OUT.mkdir(parents=True, exist_ok=True)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


IDX = json.loads((S3 / "STAGE3_INDEX.json").read_text())
p2 = json.loads(P2.read_text())

# ---------------------------------------------------------------- (1) beta*gamma_IT per species-mass
species = sorted(p2["edges"].keys(), key=lambda s: (s[0], int(s.split("_m")[1])))
bg_pts = {}
for key, pt in IDX["points"].items():
    if not key.startswith("p2/") or not key.endswith("_BM"):
        continue
    sp = key.split("/")[1]
    m = float(sp.split("_m")[1])
    lam = float(key.split("/")[2][1:].replace("_BM", ""))
    meds = []
    for ch in pt["chunks"]:
        d = np.load(S3 / ch["file"], allow_pickle=False)
        is_it = d["surf_kinds"] == "IT"
        off = d["hit_offsets"]
        sel = (d["in_eta25"] > 0) & (d["status"] == 1) & (d["tt_split"] == 0)
        for i in np.where(sel)[0]:
            a, b = off[i], off[i + 1]
            it = is_it[d["h_surf"][a:b]]
            if it.sum():
                E = d["h_E"][a:b][it]
                meds.append(float(np.median(np.sqrt(np.maximum(E * E - m * m, 0)) / m)))
    if meds:
        bg_pts.setdefault(sp, {})[lam] = (float(np.median(meds)), len(meds))

bg = {}
for sp in species:
    pts = bg_pts[sp]
    vals = np.array([v[0] for v in pts.values()])
    bg[sp] = {"betagamma_IT": round(float(np.median(vals)), 3),
              "min_over_Lambda": round(float(vals.min()), 3), "max_over_Lambda": round(float(vals.max()), 3),
              "rel_spread_half_range": round(float((vals.max() - vals.min()) / 2 / np.median(vals)), 3),
              "n_Lambda_points": len(vals), "n_events_total": int(sum(v[1] for v in pts.values())),
              "per_Lambda": {f"{k:g}": round(v[0], 3) for k, v in sorted(pts.items())}}

# cross-check against the R1 constructive probe (same selection, 18 points)
r1c = json.loads(R1C.read_text())
xchk = {}
for k, v in r1c.items():
    if isinstance(v, dict) and "median_IT_betagamma" in v:
        sp = k.split("/")[1]
        lam = float(k.split("/")[2][1:].replace("_BM", ""))
        mine = bg_pts.get(sp, {}).get(lam)
        xchk[k] = {"r1c": v["median_IT_betagamma"], "f4r": None if mine is None else round(mine[0], 3)}

# ---------------------------------------------------------------- (2) Lambda_R per mass and smoothed
fits = p2["edge_fits_in_m"]
lam_r = {}
for sp in species:
    m = float(sp.split("_m")[1])
    e = p2["edges"][sp]["lower_lmax_RIT_closed"]
    fam = sp[0]
    f = fits[f"{fam}/lower_lmax_RIT_closed"]
    form = "deg2" if (fam == "F" and "deg2" in f) else "deg1"
    x = math.log(m) - math.log(500.0)
    sm = math.exp(sum(p * x ** i for i, p in enumerate(f[form]["params"])))
    lam_r[sp] = {"per_mass_keV": round(e["value"], 4), "stat_err_keV": round(e["stat_err"], 4),
                 "smoothed_keV": round(sm, 4), "smoothing_form": f"{fam}/{form}",
                 "pull_per_mass_vs_smoothed": round((e["value"] - sm) / e["stat_err"], 2),
                 "k_thresholds_keV": {f"k>={k}": round(sm * 2 ** ((k + 1) / 2), 3) for k in range(0, 5)}}

# ---------------------------------------------------------------- (3) dE/dx expectation (ESTIMATE, constants UNVERIFIED)
ME = 0.51099895e-3   # GeV
I_SI = 173e-9        # GeV
MMU = 0.1056583755   # GeV


def delta(bgv):
    Cb, x0, x1, a, k, d0 = 4.4351, 0.2014, 2.8715, 0.14921, 3.2546, 0.14
    x = math.log10(bgv)
    if x >= x1:
        return 2 * math.log(10) * x - Cb
    if x >= x0:
        return 2 * math.log(10) * x - Cb + a * (x1 - x) ** k
    return d0 * 10 ** (2 * (x - x0))


def loss(bgv, M, tcut=None):
    """Bethe mean (tcut None) or restricted (T < tcut) loss, arbitrary units (K Z/A dropped)."""
    g = math.sqrt(1 + bgv * bgv)
    b2 = bgv * bgv / (g * g)
    tmax = 2 * ME * bgv * bgv / (1 + 2 * g * ME / M + (ME / M) ** 2)
    tup = tmax if tcut is None else min(tcut, tmax)
    return (0.5 * math.log(2 * ME * bgv * bgv * tup / I_SI ** 2) - b2 / 2 * (1 + tup / tmax) - delta(bgv) / 2) / b2


grid = np.logspace(-0.5, 2.5, 6000)
mean_min = min(loss(b, 1000.0) for b in grid)
bethe = {}
for sp in species:
    b = bg[sp]["betagamma_IT"]
    m = float(sp.split("_m")[1])
    r_mean = loss(b, m) / mean_min
    restricted = {}
    for tcut in (0.05e-3, 0.1e-3, 0.2e-3):
        for bmu in (10.0, 50.0, 100.0):
            restricted[f"Tcut{tcut*1e6:g}keV_bgmu{bmu:g}"] = round(loss(b, m, tcut) / loss(bmu, MMU, tcut), 3)
    def eadm(r):
        ok = [e for e in (1.3, 1.6, 2.0) if e <= r / 1.25]
        return max(ok) if ok else None
    rr = list(restricted.values())
    bethe[sp] = {"betagamma_IT": b, "R_BB_mean_over_min": round(r_mean, 3), "e_adm_R4_convention": eadm(r_mean),
                 "ratio_to_muon_gun_restricted": restricted,
                 "ratio_to_muon_gun_range": [min(rr), max(rr)],
                 "e_adm_muon_gun_unit_range": [eadm(min(rr)), eadm(max(rr))]}

res = {"inputs": {"P2.json_sha256": sha(P2), "STAGE3_INDEX.json_sha256": sha(S3 / "STAGE3_INDEX.json"),
                  "r1c_signal_handles.json_sha256": sha(R1C),
                  "selection": "p2, BM, template half tt_split==0, in_eta25 & status==1; per-event median IT |p|/m; "
                               "per-point median over events; per-mass median over all p2 Lambda points",
                  "tags": {"betagamma_IT": "VERIFIED (computed here from Stage-3 truth)",
                           "Lambda_R": "VERIFIED (read from P2.json; Stage-3 closed form ESTIMATE tag carried)",
                           "bethe": "ESTIMATE; Si constants recalled (I = 173 eV, Sternheimer Si), UNVERIFIED"}},
       "betagamma_IT": bg, "r1c_crosscheck": xchk, "Lambda_R": lam_r,
       "bethe_ESTIMATE": {"mean_min_betagamma": round(float(grid[np.argmin([loss(b, 1000.0) for b in grid])]), 2),
                          "per_species_mass": bethe}}
(OUT / "f4r_admissibility.json").write_text(json.dumps(res, indent=1))
for sp in species:
    print(sp, bg[sp]["betagamma_IT"], bg[sp]["min_over_Lambda"], bg[sp]["max_over_Lambda"],
          "| LR", lam_r[sp]["per_mass_keV"], lam_r[sp]["smoothed_keV"], lam_r[sp]["pull_per_mass_vs_smoothed"],
          "| RBB", bethe[sp]["R_BB_mean_over_min"], bethe[sp]["e_adm_R4_convention"],
          "| mu-unit", bethe[sp]["ratio_to_muon_gun_range"], bethe[sp]["e_adm_muon_gun_unit_range"])
bad = [k for k, v in xchk.items() if v["f4r"] is None or abs(v["f4r"] - v["r1c"]) > 1e-3]
print("r1c cross-check mismatches:", bad)
