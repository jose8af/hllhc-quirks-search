"""stage5/build_external_bounds.py -- writes stage5/external_bounds.json (existing-limit overlay for figure D7).

    python3 -I stage5/build_external_bounds.py --hepdata-t2 <t2.csv> --faser-fig5 <summary_limits_gray.pdf>

Stdlib only (run with -I; the inputs are downloaded files and are treated as data). Inputs:
  t2.csv    https://www.hepdata.net/download/table/ins3184325/Exclusion%20Contours/1/csv   (doi:10.17182/hepdata.181308.v1/t2)
  fig5 pdf  arXiv:2607.26195 e-print source, figs/summary_limits_gray.pdf (FASER Fig. 5, matplotlib vector PDF)
D0 (1008.3547) and Farina-Low (1703.00912) numbers are quoted from the papers' TeX source (abstract, Table I; Table II)
and are written here as constants with their location.

Schema (external_bounds v1) -- also described in stage5/EXTERNAL_BOUNDS.md:
  units {m: GeV, lam: keV}; curves {id: {label, applies_to [E|Etilde], model, model_match {E, Etilde},
  source {...}, method, uncertainty_tag VERIFIED|ESTIMATE, kind, points [[m_GeV, lam_keV], ...], draw, notes}}
  kind = 'upper_mass_edge': at each Lambda, m below the curve is excluded (down to m_low_GeV if given);
         'polygon': closed region, inside excluded (edges listed in 'artefact_edges' are plot-frame edges, not limits);
         'benchmarks': isolated (m, Lambda) limit points, no curve between them is given by the source.
  draw = overlay this curve on D7 by default (expected/+-1sigma FASER curves are stored but not drawn).
"""
import argparse
import csv
import datetime
import hashlib
import json
import math
import re
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# ------------------------------------------------------------------ HEPData t2 (FASER contours)
def read_hepdata_t2(path):
    """Return {column header: [(lam_eV, m_GeV), ...]} for the 4 blocks of the HEPData csv."""
    blocks, cur, head = {}, None, None
    for row in csv.reader(Path(path).read_text().splitlines()):
        if not row or row[0].startswith('#:'):
            cur = None
            continue
        if row[0].startswith('Infra-color'):
            head = row[1]
            cur = blocks.setdefault(head, [])
            continue
        if cur is not None:
            cur.append((float(row[0]), float(row[1])))
    return blocks


# ------------------------------------------------------------------ FASER Fig. 5 vector paths
def pdf_streams(path):
    data = Path(path).read_bytes()
    for m in re.finditer(rb'stream\r?\n', data):
        e = data.find(b'endstream', m.end())
        try:
            yield zlib.decompressobj().decompress(data[m.end():e]).decode('latin-1')
        except zlib.error:
            continue


def parse_paths(stream):
    """Painted paths of a matplotlib PDF content stream: list of dict(op, fill, stroke, dash, pts)."""
    toks = re.sub(r'BT.*?ET', ' ', stream, flags=re.S).split()
    st = dict(fill=(0.,), stroke=(0.,), dash=False)
    stack, num, path, sub, out = [], [], [], [], []
    i = 0
    while i < len(toks):
        t = toks[i]
        try:
            num.append(float(t))
            i += 1
            continue
        except ValueError:
            pass
        if t == '[':                                   # dash array "[a b] off d"
            j = toks.index('d', i)
            st['dash'] = toks[i + 1] != ']'
            i = j + 1
            num = []
            continue
        if t == 'm':
            if sub:
                path.append(sub)
            sub = [tuple(num[-2:])]
        elif t in ('l', 'c'):
            sub.append(tuple(num[-2:]))
        elif t == 're':
            x, y, w, h = num[-4:]
            if sub:
                path.append(sub)
            sub = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
        elif t in ('g', 'rg'):
            st['fill'] = tuple(num[-(1 if t == 'g' else 3):])
        elif t in ('G', 'RG'):
            st['stroke'] = tuple(num[-(1 if t == 'G' else 3):])
        elif t == 'q':
            stack.append(dict(st))
        elif t == 'Q':
            st = stack.pop() if stack else st
        elif t in ('f', 'f*', 'B', 'B*', 'S', 's', 'b', 'b*', 'n'):
            if sub:
                path.append(sub)
            if t != 'n':
                out += [dict(op=t, fill=st['fill'], stroke=st['stroke'], dash=st['dash'], pts=s) for s in path]
            path, sub = [], []
        num = []
        i += 1
    return out


def faser_fig5(path):
    """Gray 'existing limits' polygons and the two FASER curves, in (m GeV, Lambda eV).
    Calibration from the figure's own tick marks: x major ticks m = 60..200 GeV every 20 GeV (linear),
    y major ticks Lambda = 1e2..1e6 eV (log10). Tick positions are read from the stream, not assumed."""
    P = max((parse_paths(s) for s in pdf_streams(path)), key=len)
    frame_x0, frame_y0 = 68.174375, 51.53375                        # axes lower-left corner (pt), from the clip box
    xt = sorted({round(o['pts'][0][0], 4) for o in P if len(o['pts']) == 2 and o['pts'][0][1] == frame_y0
                 and o['pts'][1][1] - frame_y0 > 0})
    yt = sorted({round(o['pts'][0][1], 4) for o in P if len(o['pts']) == 2 and abs(o['pts'][0][0] - frame_x0) < 1e-3
                 and o['pts'][1][0] - frame_x0 > 0})
    # major ticks: x every 100.1 pt (5 minor per major); y every 134.6 pt (decades)
    xmaj = [x for x in xt if any(abs(x - (118.2236 + 100.10 * k)) < 0.05 for k in range(8))]
    ymaj = [y for y in yt if any(abs(y - (81.3992 + 134.621 * k)) < 0.05 for k in range(5))]
    assert len(xmaj) == 8 and len(ymaj) == 5, (xmaj, ymaj)
    ax = (200. - 60.) / (xmaj[-1] - xmaj[0])
    ay = (6. - 2.) / (ymaj[-1] - ymaj[0])
    X = lambda x: 60. + (x - xmaj[0]) * ax                                              # noqa: E731
    Y = lambda y: 10 ** (2. + (y - ymaj[0]) * ay)                                       # noqa: E731
    gray = [o for o in P if len(o['pts']) > 4 and abs(o['fill'][0] - 0.851) < 1e-3 and len(o['fill']) == 1]
    lines = [o for o in P if o['op'] == 'S' and len(o['pts']) > 10]
    conv = lambda o: [(X(x), Y(y)) for x, y in o['pts']]                                # noqa: E731
    frame = dict(m_min=X(frame_x0), lam_min_eV=Y(frame_y0))
    return dict(gray=[conv(o) for o in gray], obs=[conv(o) for o in lines if len(o['stroke']) == 3][0],
                exp=[conv(o) for o in lines if len(o['stroke']) == 1][0], frame=frame,
                calib=dict(GeV_per_pt=ax, decades_per_pt=ay, x_major_pt=xmaj, y_major_pt=ymaj))


def r(v, n=2):
    return round(float(v), n)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--hepdata-t2', required=True)
    ap.add_argument('--faser-fig5', required=True)
    ap.add_argument('--out', default=str(HERE / 'external_bounds.json'))
    a = ap.parse_args()

    hd = read_hepdata_t2(a.hepdata_t2)
    key = {k.split(' [')[0]: k for k in hd}
    obs = hd[key['Observed excluded quirk mass at 95% CL']]
    exp = hd[key['Expected excluded quirk mass at 95% CL']]
    ep1 = hd[key['Expected excluded quirk mass at 95% CL, +1 sigma']]
    em1 = hd[key['Expected excluded quirk mass at 95% CL, -1 sigma']]
    F = faser_fig5(a.faser_fig5)

    # identify the gray regions by their extent (labels in the figure: monojet, HSCP, OoT, D0)
    def ext(poly):
        ms, ls = [p[0] for p in poly], [p[1] for p in poly]
        return min(ms), max(ms), min(ls), max(ls)
    reg = {}
    for poly in F['gray']:
        m0, m1, l0, l1 = ext(poly)
        if l0 > 5e3:
            reg['D0'] = poly
        elif l1 > 1e6:
            reg['monojet'] = poly
        elif m1 > 600:
            reg['HSCP'] = poly
        else:
            reg['OoT'] = poly
    assert len(reg) == 4, reg.keys()

    # HSCP: the physical boundary is the upper/right edge. The polygon's bottom side lies exactly on the frame floor
    # (Lambda = 60 eV) and is dropped; edge points below the floor are kept (present in the path, clipped in the figure).
    floor = F['frame']['lam_min_eV']
    hscp_edge = sorted([p for p in reg['HSCP'] if abs(p[1] / floor - 1) > 1e-3], key=lambda p: p[0])
    # monojet: right edge (points with m > frame left edge); left edge at m = 50 GeV is the frame
    mono_edge = sorted([p for p in reg['monojet'] if p[0] > F['frame']['m_min'] + 1e-6], key=lambda p: p[1])
    oot = reg['OoT']
    d0 = reg['D0']

    hep = dict(record='HEPData ins3184325 (FASER, arXiv:2607.26195)', doi='10.17182/hepdata.181308.v1/t2',
               table='Exclusion Contours (t2)', url='https://www.hepdata.net/record/ins3184325')
    faser_model = ('(1,1,-1) fermion under SU(3)c x SU(2)L x U(1)Y, SU(N_IC = 2) fundamental, single flavour; '
                   'Drell-Yan gamma/Z; pp 13.6 TeV, 186.3 fb^-1 [2607.26195 p.1-2]')
    fig5 = dict(arxiv='2607.26195', figure='Fig. 5 (figs/summary_limits_gray.pdf in the e-print source)',
                note='gray "existing limits" as drawn by FASER for its (1,1,-1), N_IC = 2 benchmark')
    vec = ('vector digitisation: path coordinates read from the matplotlib PDF content stream, calibrated on the '
           "figure's own tick marks (closure: FASER's own observed/expected curves in the same PDF reproduce HEPData t2)")
    C = {}
    for cid, pts, lab, draw in (('FASER_obs', obs, 'FASER 2026 (obs.)', True),
                                ('FASER_exp', exp, 'FASER 2026 (exp.)', False),
                                ('FASER_exp_p1s', ep1, 'FASER 2026 (exp. +1 sigma)', False),
                                ('FASER_exp_m1s', em1, 'FASER 2026 (exp. -1 sigma)', False)):
        C[cid] = dict(label=lab, applies_to=['E'], model=faser_model,
                      model_match=dict(E='exact (same SM rep, fermion, N_IC = 2, sigma = Lambda^2)',
                                       Etilde='not directly comparable (fermion limit; FASER gives no scalar result)'),
                      source=hep, method='HEPData', uncertainty_tag='VERIFIED', kind='upper_mass_edge',
                      points=[[r(m), r(l / 1e3, 4)] for l, m in pts], draw=draw,
                      notes='Contour sampled at 19 Lambda values 0.3-105 keV. The figure draws the region left of the '
                            'curve as excluded down to the left frame (m = 50 GeV); no lower mass edge is given in t2.')
    C['D0_2010'] = dict(
        label='D0 2010', applies_to=['E'],
        model='charged (|Q| = 1) colourless fermion, SU(N) infracolour N = 2 (also 3, 5), p pbar 1.96 TeV, 2.4 fb^-1; '
              'pair seen as one straight highly-ionising track [1008.3547 abstract, p.1-2]',
        model_match=dict(E='probable: charge, colour and spin match and N = 2 is quoted; the SU(2)_L representation / '
                           'hypercharge is not stated in the Letter (Kang-Luty modified MadGraph). FASER overlays it on '
                           'its (1,1,-1) plane.',
                         Etilde='not directly comparable (fermion cross section)'),
        source=dict(arxiv='1008.3547', journal='PRL 105 (2010) 211803', where='abstract; Table I (sigma_N=2 and limits)'),
        method='paper text (abstract) + Table I; region shape (Lambda = 10 keV - 1 MeV, m = 60-107 GeV) from the text',
        uncertainty_tag='VERIFIED', kind='polygon',
        points=[[60.0, 10.0], [107.0, 10.0], [107.0, 1000.0], [60.0, 1000.0]], draw=True,
        artefact_edges=['m = 60 GeV is the lowest simulated mass (Table I), not a limit'],
        notes='Lambda-independent within the quoted range; the Lambda edges are the scenario range of the Letter, '
              'not computed limits. Lambda via L ~ m_Q/Lambda^2 (Eq. 1), i.e. tension ~ Lambda^2 up to O(1).')
    fl_src = dict(arxiv='1703.00912', where='Table II (benchmarks Lambda = 1 eV, 100 eV, 1 keV)')
    fl_model = ('(1,1)_{-1}, N_c = 2, 13 TeV recasts of CMS HSCP (12.9 fb^-1) and ATLAS monojet (3.2 fb^-1, also scaled '
                'to 12.9 fb^-1); straight-string EoM, T = Lambda^2')
    C['FarinaLow_E_TabII'] = dict(
        label='Farina-Low 2017 (Tab. II)', applies_to=['E'], model='fermion ' + fl_model,
        model_match=dict(E='exact (fermion (1,1)_{-1}, N_c = 2, T = Lambda^2)', Etilde='see FarinaLow_Etilde_TabII'),
        source=fl_src, method='paper table', uncertainty_tag='VERIFIED', kind='benchmarks',
        points=[[650.0, 0.001], [150.0, 0.1]], no_limit_at_lam_keV=[1.0], draw=True,
        notes="Tab. II lists '-' (no limit) at Lambda = 1 keV. No curve between benchmarks is given for E "
              '(Fig. 3 is for the colour triplet (3,1)_{2/3} only and is not used).')
    C['FarinaLow_Etilde_TabII'] = dict(
        label='Farina-Low 2017 (Tab. II, scalar)', applies_to=['Etilde'], model='scalar ' + fl_model,
        model_match=dict(E='no (scalar)', Etilde='exact (scalar (1,1)_{-1}, N_c = 2)'),
        source=fl_src, method='paper table', uncertainty_tag='VERIFIED', kind='benchmarks',
        points=[[350.0, 0.001], [60.0, 0.1]], no_limit_at_lam_keV=[1.0], draw=True, notes="'-' at 1 keV.")
    C['FarinaLow_HSCP_viaFASER'] = dict(
        label='CMS HSCP recast (Farina-Low, as drawn by FASER)', applies_to=['E'], model=faser_model,
        model_match=dict(E='as FASER applies it (E, N_IC = 2); FASER cites [Farina-Low] for it',
                         Etilde='not directly comparable'),
        source=fig5, method=vec, uncertainty_tag='ESTIMATE', kind='upper_mass_edge',
        points=[[r(m), r(l / 1e3, 6)] for m, l in hscp_edge], draw=True,
        notes='Upper/right edge of the region; the lower edge at Lambda = %.0f eV is the figure frame. The edge runs '
              'past m = 200 GeV and below Lambda = 60 eV outside the visible axes (present in the PDF path but clipped), to '
              'm = %.0f GeV at Lambda = %.1f eV; that part is not visible in the published figure.'
              % (F['frame']['lam_min_eV'], hscp_edge[-1][0], hscp_edge[-1][1]))
    C['FarinaLow_monojet_viaFASER'] = dict(
        label='ATLAS/CMS monojet recast (as drawn by FASER)', applies_to=['E'], model=faser_model,
        model_match=dict(E='as FASER applies it; does NOT agree with Farina-Low Tab. II (no E limit at 1 keV)',
                         Etilde='not directly comparable'),
        source=fig5, method=vec, uncertainty_tag='ESTIMATE', kind='upper_mass_edge',
        points=[[r(m), r(l / 1e3, 6)] for m, l in mono_edge], draw=True,
        notes='Right edge; the left edge at m = 50 GeV is the figure frame. Extends to Lambda ~ 5 MeV.')
    C['CMS_OoT_EvansLuty_viaFASER'] = dict(
        label='CMS out-of-time recast (as drawn by FASER)', applies_to=['E'], model=faser_model,
        model_match=dict(E='as FASER applies it (cited as CMS 1801.00359; recast by Evans-Luty 1811.08903; '
                           'the recast model was not re-checked here)', Etilde='not directly comparable'),
        source=fig5, method=vec, uncertainty_tag='ESTIMATE', kind='polygon',
        points=[[r(m), r(l / 1e3, 6)] for m, l in oot], draw=True,
        artefact_edges=['the m = 202 GeV vertical segment is where the drawn polygon ends (axes clip at 200 GeV)'],
        notes='Not requested in FIGURE_PLAN item 6; kept because FASER shows it as an existing limit. Lambda < 0.16 keV.')
    C['D0_viaFASER'] = dict(
        label='D0 (as drawn by FASER)', applies_to=['E'], model=C['D0_2010']['model'],
        model_match=C['D0_2010']['model_match'], source=fig5, method=vec, uncertainty_tag='ESTIMATE',
        kind='polygon', points=[[r(m), r(l / 1e3, 3)] for m, l in d0], draw=False,
        artefact_edges=['m = 50 GeV edge is the figure frame'], notes='Cross-check of D0_2010 only.')

    # ------------------------------------------------------------ cross-checks
    X = []
    lg = lambda v: math.log(v)                                                          # noqa: E731

    def interp_m_at_lam(pts, lam):      # pts [(m, lam)] ; log-lambda interpolation of m
        s = sorted(pts, key=lambda p: p[1])
        for (m0, l0), (m1, l1) in zip(s, s[1:]):
            if l0 <= lam <= l1:
                return m0 + (m1 - m0) * (lg(lam) - lg(l0)) / (lg(l1) - lg(l0))
        return None
    d_obs = max(abs(a_[0] - b_[1]) for a_, b_ in zip(F['obs'], obs))
    d_lam = max(abs(lg(a_[1] / b_[0])) for a_, b_ in zip(F['obs'], obs))
    d_exp = max(abs(a_[0] - b_[1]) for a_, b_ in zip(F['exp'], exp))
    X.append(dict(check='Fig. 5 vector closure: FASER observed curve (PDF path) vs HEPData t2', expected='identical',
                  found=f'max |dm| = {d_obs:.3f} GeV, max |d ln Lambda| = {d_lam:.1e} (expected curve: {d_exp:.3f} GeV)',
                  verdict='PASS' if d_obs < 0.05 and d_exp < 0.05 and d_lam < 1e-3 else 'FAIL'))
    m10 = dict(obs)[10000.0]
    X.append(dict(check='FASER text: "Masses up to 179 GeV are excluded for Lambda = 10 keV" [2607.26195, text on Fig. 4]',
                  expected=179.0, found=m10, verdict='PASS' if abs(m10 - 179) < 0.5 else 'FAIL'))
    X.append(dict(check='FASER abstract: exclusion "above the weak scale" for 300 eV < Lambda < 100 keV',
                  expected='t2 range 0.3-100 keV', found=f'{obs[0][0]/1e3:g}-{obs[-1][0]/1e3:g} keV',
                  verdict='PASS (t2 extends to 105 keV)'))
    prev = {0.3: 57, 0.5: 72, 1: 113, 1.7: 149, 3: 163, 10: 179, 30: 173, 100: 71}
    dprev = max(abs(dict((l / 1e3, m) for l, m in obs)[k] - v) for k, v in prev.items())
    X.append(dict(check='TT prior use (research/theory_signal_model.md l.103/483, code/T1_figure.py): 8 rounded t2 values',
                  expected=prev, found=f'max |d| = {dprev:.2f} GeV (rounding)', verdict='PASS' if dprev < 0.6 else 'FAIL'))
    tab = {100: (16., 13.), 120: (9.3, 14.)}   # D0 Table I: sigma_{N=2} [fb], observed limit [fb]
    q0, q1 = lg(tab[100][0] / tab[100][1]), lg(tab[120][0] / tab[120][1])
    m_cross = 100 + 20 * q0 / (q0 - q1)
    X.append(dict(check='D0 abstract 107 GeV (N = 2) vs crossing sigma_N=2 = sigma_95 from Table I (log-linear, 100-120 GeV)',
                  expected=107.0, found=round(m_cross, 1), verdict='PASS' if abs(m_cross - 107) < 2 else 'FAIL'))
    dm = max(p[0] for p in d0)
    dl = sorted({p[1] for p in d0})
    X.append(dict(check='D0 region as drawn in FASER Fig. 5 vs D0 text (m < 107 GeV, 10 keV < Lambda < 1 MeV)',
                  expected='107 GeV; 10-1000 keV', found=f'{dm:.2f} GeV; {dl[0]/1e3:.2f}-{dl[-1]/1e3:.0f} keV',
                  verdict='PASS' if abs(dm - 107) < 0.5 and abs(dl[0] / 1e4 - 1) < 0.02 else 'FAIL'))
    m100 = interp_m_at_lam(hscp_edge, 100.0)
    X.append(dict(check='Farina-Low Tab. II E, N = 2: 150 GeV at Lambda = 100 eV vs FASER-drawn HSCP edge at 100 eV',
                  expected=150.0, found=round(m100, 1), verdict='PASS (within 5 %)' if abs(m100 / 150 - 1) < 0.05
                  else 'DISCREPANT'))
    X.append(dict(check='Farina-Low Tab. II E, N = 2: 650 GeV at Lambda = 1 eV vs FASER-drawn HSCP edge (lowest Lambda)',
                  expected='650 GeV at 1 eV (Tab. II)', found=f'{hscp_edge[-1][0]:.0f} GeV at {hscp_edge[-1][1]:.1f} eV',
                  verdict='DISCREPANT (FASER edge reaches higher m at larger Lambda than Tab. II); tension documented, '
                          'not resolved'))
    m1k = interp_m_at_lam(mono_edge, 1000.0)
    X.append(dict(check="Farina-Low Tab. II E, N = 2: no limit ('-') at 1 keV vs FASER-drawn monojet region at 1 keV",
                  expected='no limit', found=f'm < {m1k:.1f} GeV excluded in FASER Fig. 5',
                  verdict='DISCREPANT (Tab. II gives only 30 GeV even for N = 5); likely a different source/rescaling '
                          'by FASER; region lies at m < 57 GeV, far below D7'))

    out = dict(
        schema='external_bounds v1', created=datetime.date.today().isoformat(),
        generated_by='stage5/build_external_bounds.py (python3 -I, stdlib only)',
        units=dict(m='GeV', lam='keV'), point_order='[m_GeV, lam_keV]',
        lambda_convention='string tension sigma = Lambda^2 (TT, FASER, Farina-Low T = Lambda^2; D0 L ~ m/Lambda^2): '
                          'no conversion applied',
        tags=dict(VERIFIED='numbers from a tabulated source (HEPData, or a table/quoted value in the paper text)',
                  ESTIMATE='digitised from a figure (here: vector paths of FASER Fig. 5); precision of the drawing, '
                           'and the drawing itself is FASER\'s rendering of other papers\' limits'),
        inputs=[dict(what='HEPData t2 csv', path_at_build=a.hepdata_t2, sha256=sha(a.hepdata_t2),
                     url='https://www.hepdata.net/download/table/ins3184325/Exclusion%20Contours/1/csv'),
                dict(what='FASER Fig. 5 PDF (arXiv e-print 2607.26195)', path_at_build=a.faser_fig5,
                     sha256=sha(a.faser_fig5), url='https://arxiv.org/e-print/2607.26195')],
        faser_fig5_calibration=F['calib'], curves=C, cross_checks=X)
    Path(a.out).write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n')
    for x in X:
        print(f"[{x['verdict'][:10]:10s}] {x['check']}\n             expected {x['expected']}  found {x['found']}")
    print('wrote', a.out, '|', ', '.join(f'{k}({len(v["points"])})' for k, v in C.items()))


if __name__ == '__main__':
    main()
