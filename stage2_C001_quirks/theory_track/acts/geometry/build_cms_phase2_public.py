"""build_cms_phase2_public.py -- E5 (Stage 4, 2026-10-11): build acts/geometry/cms_phase2_public.json, the public
CMS Phase-2 tracker layout (IT barrel + discs, OT PS/2S barrel + TEDD discs) for the quirk hit-level layer.

Inputs (public; downloaded 2026-10-11, now in theory_track/data/tdr_geometry/, see data/README.md):
  * tkLayout layout OT806_IT742 (CMSSW scenario D111, CMSSW_14_1_X; page generated 2024-04-08),
    https://cms-tklayout.web.cern.ch/cmssw/OT806_IT742/ : DetId_modules_list.csv (one row per module: section, layer,
    ring, sensor-centre rho and z, tilt, phi, corner coordinates, width, length, sensor spacing, thickness),
    layout.html / layoutpixel.html (layer tables, module-type tables with pitch, strip length, weight).
  * CMS Phase-2 Tracker TDR, CERN-LHCC-2017-009 / CMS-TDR-014 (INSPIRE 1614103), text extracted with pdftotext.
    Numbers from its Tables 3.1, 3.3, 9.1, 10.1, 12.1, 12.2 are hard-coded below with page references (printed pages).
  * 2407.13721 (measured TBPX prototype module x/X0).
Run (any Python 3 with the stdlib):  python3 -I acts/geometry/build_cms_phase2_public.py [DetId_modules_list.csv]
  (default: data/tdr_geometry/tkLayout_OT806_IT742_D111/DetId_modules_list.csv)
User decisions 2026-10-11: baseline = D111 (TDR-2017 kept for reference); material = T3 slab values with a x0.5-x2
systematic, public information only.
Output: acts/geometry/cms_phase2_public.json (next to this script).  Units: mm, degrees, x/X0 as fractions.
"""
import csv, json, math, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
TDRG = HERE.parent.parent / "data" / "tdr_geometry"
csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else TDRG / "tkLayout_OT806_IT742_D111" / "DetId_modules_list.csv"
out = Path(__file__).with_name("cms_phase2_public.json")

TKL = "tkLayout OT806_IT742 (CMSSW D111), https://cms-tklayout.web.cern.ch/cmssw/OT806_IT742/"
SRC = {
    "TDR": "CMS Collaboration, The Phase-2 Upgrade of the CMS Tracker, CERN-LHCC-2017-009, CMS-TDR-014 (2017), "
           "INSPIRE 1614103, PDF https://inspirehep.net/files/338a99fa62dec25fcbc18d806bd7fb71 (page numbers = printed)",
    "TKL_layout": TKL + "layout.html (OT 'Layers and disks', tilted-ring tables, endcap ring radii, module-type table)",
    "TKL_pixel": TKL + "layoutpixel.html (IT 'Layers and disks', ring radii, module-type table)",
    "TKL_csv": TKL + "DetId_modules_list.csv (per-module positions; aggregated by this script)",
    "MOD_X0": "arXiv:2407.13721 (CMS Tracker Group), TBPX prototype module x/X0 = 0.825% average (Table 1 / Sec.2), "
              "measured regions 0.72% and 0.95% (abstract)",
    "T3": "theory_track/code/T3_propagator.py phase2_tracker() (slabs used for every truth-level number so far)",
    "MTD_TDR": "CMS, A MIP Timing Detector for the CMS Phase-2 Upgrade, CERN-LHCC-2019-003, CMS-TDR-020, INSPIRE 1819664 "
               "(data/tdr_geometry/beamspot_sources/CMS-TDR-020_MTD_TDR.pdf; printed pages)",
    "HLLHC_TDR": "HL-LHC Technical Design Report, CERN-2020-010, INSPIRE 1840718 "
                 "(data/tdr_geometry/beamspot_sources/CERN-2020-010_HL-LHC_TDR.pdf), Table 2-1 p.18",
}

rows = []
with open(csv_path) as fh:
    rd = csv.reader(fh)
    next(rd)
    for r in rd:
        if len(r) < 23:
            continue
        sec = r[2].strip()
        rows.append(dict(sec=sec, layer=int(r[3]), ring=int(r[4]), rho=float(r[5]), z=float(r[6]),
                         tilt=float(r[7]), corners=[float(x) for x in r[11:19]], width=float(r[19]),
                         length=float(r[20]), spacing=float(r[21]), thick=float(r[22])))


def mtype(row):
    w = row["width"]
    if row["sec"] in ("PXB", "FPIX_1", "FPIX_2"):
        return "IT_1x2" if w < 25 else "IT_2x2"
    return "PS" if abs(w - 96.0) < 1 else ("2S" if abs(w - 91.44) < 1 else f"?w{w}")


def rnd(x, n=1):
    return round(x, n)


# ------------------------------------------------------------------ barrel layers (aggregated from the module list)
barrel = []
for sec, name, sub in (("PXB", "TBPX", "IT"), ("TBPS", "TBPS", "OT"), ("TB2S", "TB2S", "OT")):
    for L in sorted({x["layer"] for x in rows if x["sec"] == sec}):
        m = [x for x in rows if x["sec"] == sec and x["layer"] == L]
        flat = [x for x in m if abs(x["tilt"]) < 1e-6]
        tilted = [x for x in m if abs(x["tilt"]) >= 1e-6]
        types = sorted({mtype(x) for x in m})
        zmax = max(abs(x["z"]) + 0.5 * x["length"] * math.cos(math.radians(x["tilt"])) for x in m)
        e = dict(name=f"{name}_L{L}", subdetector=sub, section_tkLayout=sec, layer=L, module_types=types,
                 n_modules=len(m), n_modules_flat=len(flat), n_modules_tilted=len(tilted),
                 sensor_rho_min_mm=rnd(min(x["rho"] for x in m)), sensor_rho_max_mm=rnd(max(x["rho"] for x in m)),
                 sensor_rho_mean_flat_mm=rnd(sum(x["rho"] for x in flat) / max(1, len(flat))),
                 z_half_extent_mm=rnd(zmax),
                 flat_z_half_extent_mm=rnd(max((abs(x["z"]) + 0.5 * x["length"] for x in flat), default=0.0)),
                 module_width_mm=sorted({x["width"] for x in m}), module_length_mm=sorted({x["length"] for x in m}),
                 sensor_spacing_mm=sorted({x["spacing"] for x in m}),
                 sensor_thickness_mm=sorted({x["thick"] for x in m}),
                 tilt_angles_deg=sorted({rnd(abs(x["tilt"]), 1) for x in tilted}),
                 source="TKL_csv")
        barrel.append(e)

# tkLayout nominal layer radii / z_max ("Layers and disks" tables) and TDR Tables 9.1 / 10.1
TKL_R = {"TBPX_L1": (30.0, 200.125), "TBPX_L2": (61.5, 201.425), "TBPX_L3": (104.5, 201.425), "TBPX_L4": (146.5, 201.425),
         "TBPS_L1": (249.438, 1202.910), "TBPS_L2": (371.678, 1203.526), "TBPS_L3": (522.700, 1201.877),
         "TB2S_L1": (687.0, 1174.214), "TB2S_L2": (860.0, 1174.214), "TB2S_L3": (1083.0, 1174.214)}
TKL_NRODS = {"TBPX_L1": 12, "TBPX_L2": 24, "TBPX_L3": 20, "TBPX_L4": 28, "TBPS_L1": 18, "TBPS_L2": 26, "TBPS_L3": 36,
             "TB2S_L1": 48, "TB2S_L2": 60, "TB2S_L3": 76}
TDR_R = {"TBPX_L1": (29.0, 199.7, 108, "TDR Table 10.1, p.236"), "TBPX_L2": (70.1, 199.7, 252, "TDR Table 10.1, p.236"),
         "TBPX_L3": (117.8, 199.7, 216, "TDR Table 10.1, p.236"), "TBPX_L4": (157.4, 199.7, 288, "TDR Table 10.1, p.236"),
         "TBPS_L1": (248.1, 1203.1, 558, "TDR Table 9.1, p.149"), "TBPS_L2": (371.7, 1203.5, 910, "TDR Table 9.1, p.149"),
         "TBPS_L3": (522.7, 1201.8, 1404, "TDR Table 9.1, p.149"), "TB2S_L1": (687.0, 1176.6, 1152, "TDR Table 9.1, p.149"),
         "TB2S_L2": (860.0, 1176.6, 1440, "TDR Table 9.1, p.149"), "TB2S_L3": (1108.0, 1176.6, 1872, "TDR Table 9.1, p.149")}
T3_R = {"TBPX_L1": 30.0, "TBPX_L2": 61.0, "TBPX_L3": 104.0, "TBPX_L4": 146.0, "TBPS_L1": 249.0, "TBPS_L2": 372.0,
        "TBPS_L3": 523.0, "TB2S_L1": 688.0, "TB2S_L2": 860.0, "TB2S_L3": 1083.0}
for e in barrel:
    n = e["name"]
    e["r_nominal_mm"] = TKL_R[n][0]; e["z_max_nominal_mm"] = TKL_R[n][1]; e["n_rods_or_ladders"] = TKL_NRODS[n]
    e["r_nominal_source"] = "TKL_layout" if n[:3] != "TBP" or n.startswith("TBPS") else "TKL_pixel"
    if n.startswith("TBPX"):
        e["r_nominal_source"] = "TKL_pixel"
    r, z, nm, ref = TDR_R[n]
    e["TDR_2017"] = dict(r_mm=r, z_coverage_mm=z, n_modules=nm, source=ref)
    e["T3_slab_r_mm"] = T3_R[n]

# ------------------------------------------------------------------ endcap discs (per disc: z, ring radii and types)
endcap = []
for sec, name, sub in (("FPIX_1", "TFPX", "IT"), ("FPIX_2", "TEPX", "IT"), ("TEDD_1", "TEDD", "OT"), ("TEDD_2", "TEDD", "OT")):
    for L in sorted({x["layer"] for x in rows if x["sec"] == sec}):
        m = [x for x in rows if x["sec"] == sec and x["layer"] == L and x["z"] > 0]
        zs = sorted(x["z"] for x in m)
        rings = []
        for R in sorted({x["ring"] for x in m}):
            mr = [x for x in m if x["ring"] == R]
            rc = [math.hypot(x["corners"][2 * i], x["corners"][2 * i + 1]) for x in mr for i in range(4)]
            rings.append(dict(ring=R, module_type=sorted({mtype(x) for x in mr}), n_modules=len(mr),
                              r_centre_mm=rnd(sum(x["rho"] for x in mr) / len(mr)),
                              r_min_mm=rnd(min(rc)), r_max_mm=rnd(max(rc)),
                              z_min_mm=rnd(min(x["z"] for x in mr)), z_max_mm=rnd(max(x["z"] for x in mr)),
                              sensor_spacing_mm=sorted({x["spacing"] for x in mr})))
        disc_no = L if sec != "TEDD_2" else L + 2
        endcap.append(dict(name=f"{name}_D{disc_no}", subdetector=sub, section_tkLayout=sec, layer_tkLayout=L,
                           z_mean_mm=rnd(sum(zs) / len(zs)), z_min_mm=rnd(zs[0]), z_max_mm=rnd(zs[-1]),
                           n_modules_per_side=len(m), n_rings=len(rings), rings=rings, mirrored_in_minus_z=True,
                           source="TKL_csv"))
TDR_Z = {"TFPX": ([250.0, 319.8, 409.0, 523.1, 669.1, 855.8, 1094.6, 1400.0], "TDR Table 10.1, p.236"),
         "TEPX": ([1750.0, 1985.4, 2250.8, 2550.0], "TDR Table 10.1, p.236"),
         "TEDD": ([1311.8, 1550.0, 1853.4, 2216.2, 2650.0], "TDR Table 9.1, p.149")}
TKL_Z = {"TFPX": [250.000, 319.760, 408.990, 523.110, 669.080, 840.780, 1109.570, 1400.000],
         "TEPX": [1750.000, 2009.590, 2307.690, 2650.000], "TEDD": [1311.800, 1550.000, 1853.400, 2216.190, 2650.000]}
for e in endcap:
    base = e["name"].split("_")[0]; k = int(e["name"].split("_D")[1]) - 1
    e["z_nominal_mm"] = TKL_Z[base][k]
    e["z_nominal_source"] = "TKL_pixel" if base in ("TFPX", "TEPX") else "TKL_layout"
    e["TDR_2017"] = dict(z_mm=TDR_Z[base][0][k], source=TDR_Z[base][1])

# ------------------------------------------------------------------ module types / segmentation / binary resolution
s12 = 1 / math.sqrt(12)
module_types = {
    "IT_1x2": dict(description="Inner Tracker 1x2 pixel module (2 ROCs), planar 25x100 um^2 pixels (TBPX L1: 3D sensors "
                   "in OT806_IT742, 'pixel_1x2_25x100_wide_2sens_3D')",
                   pitch_rphi_um=25.0, pitch_long_um=100.0, long_axis="z in barrel, r in discs",
                   sensor_thickness_mm=0.150, readout="pixel (analogue ToT, charge sharing)",
                   binary_resolution_um=[rnd(25 * s12, 1), rnd(100 * s12, 1)],
                   tkLayout_parametrised_resolution_um={"barrel_local_x_mean": 3.1, "barrel_local_y_mean": 10.8,
                                                        "disc_local_x_mean": 5.9, "disc_local_y_mean": 24.3},
                   module_mass_g={"TDR_TBPX_L1": 2.33, "TDR_TBPX_L2": 2.12, "TDR_TFPX_TEPX_R1-2": 1.74,
                                  "tkLayout_av": 3.2},
                   active_size_mm=[16.8, 43.65],
                   sources=["TKL_pixel module table (pitch 25.0, 'strip length' 99.9-100.1 um, resolutions, weight)",
                            "TDR p.74 (25x100 um^2 considered in the whole IT; 50x50 option), TDR Table 12.2 p.274 (masses), "
                            "TDR p.274 (150 um IT sensors in the material model)", "TKL_csv (width/length)"]),
    "IT_2x2": dict(description="Inner Tracker 2x2 pixel module (4 ROCs), 25x100 um^2", pitch_rphi_um=25.0,
                   pitch_long_um=100.0, sensor_thickness_mm=0.150, binary_resolution_um=[rnd(25 * s12, 1), rnd(100 * s12, 1)],
                   tkLayout_parametrised_resolution_um={"barrel_local_x_mean": 2.9, "barrel_local_y_mean": 13.1,
                                                        "disc_local_x_mean": 5.8, "disc_local_y_mean": 22.8},
                   module_mass_g={"TDR_TBPX_L3-4": 3.75, "TDR_TFPX_TEPX_R3-5": 3.49, "tkLayout_av_barrel": 5.0,
                                  "tkLayout_av_disc": 6.4},
                   active_size_mm=[33.85, 43.45], sources=["TKL_pixel", "TDR Table 12.2 p.274", "TKL_csv"]),
    "PS": dict(description="Outer Tracker PS module: strip sensor (PS-s) 2x960 strips 100 um x ~2.35 cm above a macro-pixel "
               "sensor (PS-p) 32x960 macro-pixels 100 um x 1.467 mm; binary readout; sensor spacing 1.6/2.6/4.0 mm",
               pitch_rphi_um=100.0, strip_length_um=23472.0, macro_pixel_length_um=1467.0,
               binary_resolution_um=[rnd(100 * s12, 1), rnd(1467 * s12, 0)],
               tkLayout_parametrised_resolution_um={"local_x": 20.4, "local_y": 423.5},
               measures="2D (r-phi from strips and macro-pixels; z (barrel) / r (disc) from macro-pixel 1.467 mm)",
               sensor_spacing_mm=[1.6, 2.6, 4.0], sensor_active_mm=[96.0, 46.944], sensor_thickness_mm_tkLayout=0.290,
               sensor_active_thickness_mm_TDR=0.200,
               module_mass_g={"TDR_PS_2.6mm": 32.4, "tkLayout_av_1.6": 49.9, "tkLayout_av_2.6": 56.0, "tkLayout_av_4.0": 59.4,
                              "tkLayout_av_TEDD": 38.2},
               sources=["TDR Table 3.1 p.29", "TDR Table 3.3 p.37 and Table 9.4 p.157 (pitch 100 um, strip 23 472 um, "
                        "macro-pixel 1 467 um, active 96.000 x 46.944 mm)", "TDR Table 12.1 p.274 (mass)",
                        "TKL_layout module table (pitch, strip length, resolution, weight)"]),
    "2S": dict(description="Outer Tracker 2S module: two strip sensors, 2x1016 strips 90 um x ~5 cm each, strips PARALLEL "
               "(no stereo); binary readout; sensor spacing 1.8/4.0 mm",
               pitch_rphi_um=90.0, strip_length_um=50274.0,
               binary_resolution_um=[rnd(90 * s12, 1), rnd(50274 * s12, -2)],
               tkLayout_parametrised_resolution_um={"local_x": 18.4, "local_y": 14505.9},
               measures="1D (r-phi only); z (barrel) / r (disc) known only to the 5 cm strip-row length",
               sensor_spacing_mm=[1.8, 4.0], sensor_active_mm=[91.44, 100.5], sensor_thickness_mm_tkLayout=0.290,
               sensor_active_thickness_mm_TDR=0.200,
               module_mass_g={"TDR_2S_1.8mm": 37.3, "tkLayout_av_barrel": 42.7, "tkLayout_av_TEDD_4.0": 45.1},
               sources=["TDR Table 3.1 p.29", "TDR Table 3.3 p.37 (2S pitch 90 um, strip 50 274 um, active 91.440 x "
                        "100.548 mm)", "TDR Table 12.1 p.274 (mass)", "TKL_layout module table"]),
}

# ------------------------------------------------------------------ material (x/X0 per layer at normal incidence)
# No public per-layer x/X0 table exists in the TDR (only Fig. 6.2, stacked vs |eta|) and the public tkLayout summary.root
# of OT806_IT742 holds no material histograms (checked 2026-10-11). Module-only areal densities are ESTIMATED as
# mass / (active area x module-coverage factor); X0_eff = 18 g/cm^2 (Si 21.8, Al 24.0, C-fibre ~42, Cu 12.9; hybrids are
# Cu/kapton-heavy) -- an assumption, +-40 %. Supports and services are NOT included.
X0EFF = 18.0
def est(mass_g, area_mm2):
    rho_x = mass_g / (area_mm2 / 100.0)
    return rnd(rho_x, 3), rnd(rho_x / X0EFF, 4)
mat = {}
for key, mass, area in (("TBPX_L1-2 (1x2, TDR mass 2.12-2.33 g)", 2.23, 16.8 * 43.65 * 1.1),
                        ("TBPX_L3-4 (2x2, TDR mass 3.75 g)", 3.75, 33.85 * 43.45 * 1.1),
                        ("PS module (TDR 32.4 g)", 32.4, 96.0 * 46.944 * 1.2),
                        ("PS module (tkLayout 56.0 g, incl. tilted-ring support share)", 56.0, 96.0 * 46.944 * 1.2),
                        ("2S module (TDR 37.3 g)", 37.3, 91.44 * 100.5 * 1.1),
                        ("2S module (tkLayout 42.7 g)", 42.7, 91.44 * 100.5 * 1.1)):
    rx, xx = est(mass, area)
    mat[key] = dict(areal_density_g_cm2=rx, x_over_X0_module_only=xx, status="ESTIMATE (X0_eff=18 g/cm2 assumed, "
                    "footprint = active area x 1.1-1.2; +-40 %)")
material = dict(
    note="No public per-layer x/X0 table. Values below: (a) one measured module, (b) module-only ESTIMATES from public "
         "masses, (c) the T3 slab values used so far (UNVERIFIED). Supports/services/cooling not included in (b). TDR Fig. 6.2 "
         "(p.98) gives the total inside the tracking volume vs |eta| only graphically (Phase-2 roughly 0.2-0.3 X0 at "
         "|eta|=0 as read by eye -- UNVERIFIED reading).",
    measured=dict(TBPX_prototype_module_x_over_X0=0.00825, regions=[0.0072, 0.0095], source="MOD_X0"),
    calibration_check="The mass-based method gives 1.3-1.5 % for TBPX modules vs 0.825 % measured (MOD_X0): it over-"
                      "estimates by x1.6-1.9 (X0_eff too low and/or footprint too small). Treat module_estimates as upper "
                      "bounds; scaled by 1/1.75 they give PS ~1.9-3.3 %, 2S ~1.2-1.3 % (module only).",
    module_estimates=mat,
    T3_slabs_used=dict(beam_pipe=0.0023, TBPX_each=0.012, IT_service_cylinder_r190=0.010, PS_layers_each=0.025,
                       two_S_layers_each=0.018, status="UNVERIFIED (T3 report Sec.2)", source="T3"),
    baseline="T3_slabs_used (user decision 2026-10-11), systematic variation x0.5 and x2 (all layers together)",
    recommendation="Keep T3 slab values as baseline (consistent with module-only estimates plus a support share) and vary "
                   "x0.5-x2 as a systematic; replace by a CMS-internal material map when available (needs CMS access).")

# ------------------------------------------------------------------ simplified ACTS / pure-Python geometry
simple = dict(note="Flat cylinders (barrel) and discs (endcaps) at the tkLayout nominal positions; TBPS tilted rings "
              "approximated by the flat-layer radius out to z_max (UNVERIFIED approximation: tilted sensors sit 4-15 mm "
              "farther out and are inclined 40-72 deg). Use for the hybrid ACTS geometry (Blueprint) and the fallback.",
              cylinders=[dict(name=e["name"], r_mm=e["r_nominal_mm"], half_z_mm=e["z_max_nominal_mm"],
                              module_type=e["module_types"][0] if len(e["module_types"]) == 1 else e["module_types"])
                         for e in barrel],
              discs=[dict(name=e["name"], z_mm=e["z_nominal_mm"], r_min_mm=min(r["r_min_mm"] for r in e["rings"]),
                          r_max_mm=max(r["r_max_mm"] for r in e["rings"]),
                          ps_2s_boundary_mm=(max([r["r_max_mm"] for r in e["rings"] if "PS" in r["module_type"]] or [0]) or None))
                     for e in endcap])

# ------------------------------------------------------------------ HL-LHC luminous region (for PU-200 vertex smearing)
gamma = 7000.0 / 0.938272
sig_beam_um = math.sqrt(2.5e-6 * 0.15 / gamma) * 1e6
beamspot = dict(
    sigma_z_mm=45.0, sigma_z_source="MTD_TDR p.2 (Sec.1.1): 'line spread along the beam axis of about 4.5 cm rms (averaged "
                                    "over the length of the fill)'",
    sigma_t_ps=190.0, sigma_t_source="MTD_TDR p.2 and p.3: collisions 'distributed over time with an rms of 180-200 ps' "
                                     "(mid value taken)",
    peak_line_density_per_mm_PU200=1.9, line_density_source="MTD_TDR p.2 text, Fig.1.1 p.3",
    sigma_xy_um=rnd(sig_beam_um / math.sqrt(2), 1),
    sigma_xy_source="ESTIMATE from HLLHC_TDR Table 2-1 p.18 (beta* = 0.15 m, eps_n = 2.50 um, E = 7 TeV): sigma*_beam = "
                    f"sqrt(eps_n beta*/gamma) = {sig_beam_um:.1f} um per beam, luminous = /sqrt(2); at minimum beta* (larger "
                    "while levelling). Negligible against tracker resolution.",
    pileup_mean=200, pileup_source="BRIEF (PU 200 target); HLLHC_TDR Table 2-1 gives 131-140 for the nominal levelled "
                                   "scenario, 200 is the CMS ultimate-scenario design value (UNVERIFIED citation in this file)",
)

doc = dict(
    title="CMS Phase-2 tracker, public layout (for the C001 quirk hit-level layer)",
    created="2026-10-11 by E5 (theory_track/acts), script acts/geometry/build_cms_phase2_public.py",
    units=dict(length="mm", angle="deg", material="x/X0 fraction at normal incidence"),
    primary_layout="tkLayout OT806_IT742 = geometry exported to CMSSW (scenario D111, CMSSW_14_1_X). It supersedes the "
                   "2017 TDR baseline: IT barrel radii changed (TDR 29.0/70.1/117.8/157.4 -> 30.0/61.5/104.5/146.5 mm), "
                   "TB2S L3 1108 -> 1083 mm (76 vs 78 ladders), TEPX z positions, TBPX L1 3D sensors. Both are given.",
    sources=SRC,
    status=dict(VERIFIED_against_source="positions, counts, pitches and strip lengths are read from the cited public pages "
                "(no CMS-internal input)",
                UNVERIFIED=["material x/X0 per layer (no public table)", "tilted-TBPS flat approximation in 'simplified'",
                            "sensor thickness: tkLayout lists 0.29 mm for OT, TDR quotes 200 um active (320 um physical "
                            "option) -- only matters for dE/dx", "final pixel choice: TDR studies assume 25x100 um^2 "
                            "everywhere; OT806_IT742 also uses 25x100 (L1 3D)"]),
    module_types=module_types,
    barrel_layers=barrel,
    endcap_discs=endcap,
    material=material,
    simplified=simple,
    beamspot=beamspot,
    totals=dict(modules_by_section={s: sum(1 for x in rows if x["sec"] == s) for s in sorted({x["sec"] for x in rows})},
                TDR_OT_modules=dict(TBPS=2872, TB2S=4464, TEDD=5960, total=13296, source="TDR Table 3.2 p.31"),
                TDR_IT_modules=dict(TBPX=864, TFPX=1728, TEPX=1760, source="TDR Table 4.1 p.75")),
)
out.write_text(json.dumps(doc, indent=1))
print("wrote", out, "| barrel layers", len(barrel), "| discs (+z)", len(endcap), "| modules", len(rows))
for e in barrel:
    print(f"  {e['name']:8s} r_nom {e['r_nominal_mm']:8.2f}  rho[{e['sensor_rho_min_mm']:7.1f},{e['sensor_rho_max_mm']:7.1f}]"
          f"  |z|<{e['z_half_extent_mm']:7.1f}  n={e['n_modules']} (tilted {e['n_modules_tilted']}) {e['module_types']}")
for e in endcap:
    print(f"  {e['name']:8s} z {e['z_mean_mm']:8.1f} r[{min(r['r_min_mm'] for r in e['rings']):6.1f},"
          f"{max(r['r_max_mm'] for r in e['rings']):7.1f}] rings {e['n_rings']} n/side {e['n_modules_per_side']} "
          f"types {sorted({t for r in e['rings'] for t in r['module_type']})}")
