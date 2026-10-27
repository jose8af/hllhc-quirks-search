"""regen_report_figures.py -- report writer W: larger-font copies of theory-track figures for the PDF report.

Purpose: the report reviewers (review/REPORT_RENDERING_REVIEW.md B3-B4, C3-C5, C9) found several figures illegible
at page size. This script regenerates them with larger fonts (and a few layout fixes: legend position, panel labels,
tick labels, an overlapping annotation) WITHOUT touching theory_track/figures/ or theory_track/code/.
Physics content is unchanged: every curve comes from the original script or from the data file it saved.
  * exec'd copies of the original scripts (fontsize x SCALE, output redirected): T1_figure, T3_ms_figure, T4_met,
    T4_local (re-runs ~10 min serially, same fixed seeds as the original), T6_coverage, T2_approx_errors
  * re-plotted from saved data: T4_fisher_summary.npz, T4_comb.npy, T2_string_methods_B.npy
Outputs: report/figures/<name>_rep.png
Run (from theory_track/): pixi run python report/figures/regen_report_figures.py [names...]
"""
import os, re, sys, subprocess, tempfile
import numpy as np

TT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CODE = os.path.join(TT, 'code'); FIGIN = os.path.join(TT, 'figures')
OUT = os.path.join(TT, 'report', 'figures')
SCALE = 1.45


def scaled(src, scale=SCALE):
    src = re.sub(r'fontsize=([0-9.]+)', lambda m: f'fontsize={float(m.group(1)) * scale:.1f}', src)
    head = ("import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib as _mpl\n"
            "_mpl.rcParams.update({'font.size': 13, 'axes.titlesize': 13, 'axes.labelsize': 13, "
            "'xtick.labelsize': 12, 'ytick.labelsize': 12, 'legend.fontsize': 11})\n")
    return head + src


def run_copy(name, edits, scale=SCALE):
    src = open(os.path.join(CODE, name)).read()
    src = src.replace("sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))", f"sys.path.insert(0, {CODE!r})")
    src = re.sub(r"FIG = os\.path\.join\(os\.path\.dirname\(os\.path\.abspath\(__file__\)\), '\.\.', 'figures'\)",
                 f"FIG = {FIGIN!r}", src)
    for a, b in edits:
        assert a in src, (name, a)
        src = src.replace(a, b)
    src = scaled(src, scale)
    d = tempfile.mkdtemp()
    fn = os.path.join(d, name.replace('.py', '_rep.py'))
    open(fn, 'w').write(f"import sys\nsys.path.insert(0, {CODE!r})\n" + src)
    env = dict(os.environ, PYTHONPATH=CODE)
    subprocess.run([sys.executable, fn] + (['80'] if name == 'T4_local.py' else []), cwd=TT, check=True, env=env)


def o(n):
    return os.path.join(OUT, n)


JOBS = {
    'T1': lambda: run_copy('T1_figure.py', [('fig.savefig("figures/T1_lambda_plane.png", dpi=150)',
                                              f'fig.savefig({o("T1_lambda_plane_rep.png")!r}, dpi=150, bbox_inches="tight")'),
                                             ('figsize=(13, 6.2)', 'figsize=(13, 7.4)')]),
    'T3ms': lambda: run_copy('T3_ms_figure.py', [("axs[0].legend(fontsize=8, loc='lower left', frameon=False)",
                                                  "fig.legend(*axs[0].get_legend_handles_labels(), loc='lower center', ncol=4, fontsize=8, frameon=False)"),
                                                 ("ax.text(2.2, 120, 'Δs = 100 µm cut [1708.02243]', fontsize=8,",
                                                  "ax.text(3.0, 125, 'Δs = 100 µm cut', fontsize=7,"),
                                                 ("fig.tight_layout()", "fig.tight_layout(rect=(0, 0.08, 1, 1))"),
                                                 ("fig.savefig(os.path.join(FIG, 'T3_ms_thickness.png'), dpi=140)",
                                                  f"fig.savefig({o('T3_ms_thickness_rep.png')!r}, dpi=140, bbox_inches='tight')"),
                                                 ("figsize=(13, 4.3)", "figsize=(13, 5.0)")]),
    'T4met': lambda: run_copy('T4_met.py', [("fig.savefig(os.path.join(FIG, 'T4_met_alignment.png'), dpi=130)",
                                             f"fig.savefig({o('T4_met_alignment_rep.png')!r}, dpi=130)"),
                                            ("figsize=(11, 4.4)", "figsize=(10, 5.4)"),
                                            ("axs[0].legend(fontsize=6)", "axs[0].legend(fontsize=7.2)")]),
    'T4local': lambda: run_copy('T4_local.py', [("fig.savefig(os.path.join(FIG, 'T4_local.png'), dpi=130)",
                                                 f"fig.savefig({o('T4_local_rep.png')!r}, dpi=130)"),
                                                ("figsize=(11, 4.2)", "figsize=(10, 5.4)"),
                                                ("axs[1].legend(fontsize=6)", "axs[1].legend(fontsize=7.2)"),
                                                ("""            with Pool(2) as pool:
                res[(m, lam)] = pool.map(job, [(float(m), lam, th) for th in ths])""",
                                                 """            res[(m, lam)] = list(map(job, [(float(m), lam, th) for th in ths]))   # serial (Pool fails from a temp copy)""")]),
    'T6': lambda: run_copy('T6_coverage.py', [("plt.savefig('figures/T6_coverage.png')",
                                               f"plt.savefig({o('T6_coverage_rep.png')!r})"),
                                              ("figsize=(11, 7.2)", "figsize=(14, 9.6)"),
                                              ("ax.set_title('Schematic (m_Q, Lambda) coverage, E=(1,1)_{-1}, N_IC=2, 14 TeV, HL-LHC 3/ab  (edges +-factor 2; T6 report)', fontsize=10)",
                                               "ax.set_title('Schematic (m_Q, Lambda) coverage, E=(1,1)_{-1}, N_IC=2, 14 TeV, HL-LHC 3/ab (edges +-factor 2; T6)', fontsize=10)")],
                                             scale=1.2),
    'T2approx': lambda: run_copy('T2_approx_errors.py', [("ax.text(2.5, 0.675, 'NR virial 2/3', fontsize=8)",
                                                          "ax.text(2.3, 0.655, 'NR virial 2/3', fontsize=8)"),
                                                         ("fig.savefig(os.path.join(FIG, 'T2_approx_errors.png'), dpi=130)",
                                                          f"fig.savefig({o('T2_approx_errors_rep.png')!r}, dpi=130)"),
                                                         ("ax2.set_yticks([]); ax2.legend(loc='upper center', fontsize=7)",
                                                          "ax2.set_yticks([]); ax2.legend(loc='upper left', bbox_to_anchor=(0.0, -0.17), ncol=2, fontsize=7, frameon=False)"),
                                                         ("figsize=(11, 4.2)", "figsize=(12, 5.6)")]),
}


def setup_mpl():
    import matplotlib
    matplotlib.use('Agg')
    matplotlib.rcParams.update({'font.size': 13, 'axes.titlesize': 13, 'axes.labelsize': 13,
                                'xtick.labelsize': 12, 'ytick.labelsize': 12, 'legend.fontsize': 11})
    import matplotlib.pyplot as plt
    return plt


def fisher():
    plt = setup_mpl()
    z = np.load(os.path.join(FIGIN, 'T4_fisher_summary.npz'), allow_pickle=True)
    res = z['res'][0]
    MASSES, LAMS = (200, 500, 1000), (1.0, 3.0, 10.0)
    cfgs = ['P2 B, positions + MS', 'M1 P2 + MET + PV', 'M3 M2 + IT dE/dx', 'M4 M3 + eloss model']
    cols = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    fig, axs = plt.subplots(1, 3, figsize=(11, 5.6))
    for j, m in enumerate(MASSES):
        ax = axs[j]
        for c, cfg in zip(cols, cfgs):
            ym = [res.get((m, lam, cfg), {}).get('ens', {}).get(30, (np.nan, np.nan))[0] for lam in LAMS]
            yl = [res.get((m, lam, cfg), {}).get('ens', {}).get(30, (np.nan, np.nan))[1] for lam in LAMS]
            ax.loglog(LAMS, ym, 'o-', color=c, label=f'σ(m)/m   {cfg}')
            ax.loglog(LAMS, yl, 's--', color=c, label=f'σ(Λ)/Λ   {cfg}')
        ax.set_title(f'm_Q = {m} GeV, N = 30 events')
        ax.set_xlabel('Λ [keV]'); ax.grid(alpha=0.3, which='both')
        if j == 0:
            ax.set_ylabel('relative resolution (Cramér-Rao)')
    h, l = axs[0].get_legend_handles_labels()
    fig.legend(h, l, loc='lower center', ncol=2, fontsize=11, frameon=False, bbox_to_anchor=(0.5, -0.01))
    fig.tight_layout(rect=(0, 0.25, 1, 1))
    fig.savefig(o('T4_fisher_summary_rep.png'), dpi=130)


def comb():
    plt = setup_mpl()
    store = np.load(os.path.join(FIGIN, 'T4_comb.npy'), allow_pickle=True)[0]
    nosc = {1.0: 9, 3.0: 83, 10.0: 922}          # as printed in the original panel titles (T4_comb.py)
    fig, axs = plt.subplots(2, 3, figsize=(10.5, 8.0))
    for j, lam in enumerate((1.0, 3.0, 10.0)):
        for row in (0, 1):
            ds, c2, w, dev = store[(lam, row)]
            ax = axs[row, j]
            ax.semilogy(ds, np.maximum(c2, 1e-2), lw=1.4)
            ax.axhline(1, color='gray', lw=0.7, ls='--'); ax.axhline(25, color='gray', lw=0.7, ls=':')
            ax.set_title(f'({"ab"[row]}{j + 1}) Λ = {lam:g} keV\nN_osc≈{nosc[lam]}, σ_loc = {w:.2g}', fontsize=12)
            ax.set_xlabel('δ (shift of ln par.)' if row else 'δ = δ ln ℓ0')
            ax.tick_params(axis='x', labelsize=10, rotation=30)
        axs[0, 0].set_ylabel('(a) χ², ℓ0 direction')
        axs[1, 0].set_ylabel('(b) χ², vacuum-degenerate dir.')
    fig.tight_layout()
    fig.savefig(o('T4_comb_rep.png'), dpi=130)


def smb():
    plt = setup_mpl()
    from matplotlib.ticker import LogLocator, NullFormatter
    rows = np.load(os.path.join(FIGIN, 'T2_string_methods_B.npy'))
    fig, ax = plt.subplots(1, 2, figsize=(12, 5.0))
    for j, (lab, col) in enumerate((('causal (Athena port, unconverged setting)', 'k'),
                                    ('lab-simultaneous straight string (labSS)', 'C3'), ('CM straight string (cmSS)', 'C0'))):
        ax[0].scatter(rows[:, 0] * (1 + 0.03 * (j - 1)), rows[:, 3 + j], color=col, label=lab, s=22)
    lam = np.logspace(np.log10(0.5), np.log10(6), 50)
    ax[0].plot(lam, 1.16 * 5 * 3.8 / lam ** 4, 'k:', label='formula [1911.02223 Eq.III.12]')
    ax[0].set_ylabel('plane thickness d_min [µm]'); ax[0].legend(fontsize=9.5, loc='lower left')
    ax[1].scatter(rows[:, 0] * 0.97, rows[:, 6], color='C3', label='labSS', s=22)
    ax[1].scatter(rows[:, 0] * 1.03, rows[:, 7], color='C0', label='cmSS', s=22)
    ax[1].set_ylabel('max |hit(straight) − hit(causal)| [µm]'); ax[1].legend(fontsize=10)
    for a in ax:
        a.set_xscale('log'); a.set_yscale('log'); a.set_xlabel('Λ [keV]'); a.grid(alpha=0.3, which='both')
        a.set_xticks([0.6, 1, 2, 5]); a.set_xticklabels(['0.6', '1', '2', '5'])
        a.xaxis.set_minor_locator(LogLocator(subs='all')); a.xaxis.set_minor_formatter(NullFormatter())
    fig.suptitle('WITHDRAWN stand-in (T2): labSS / cmSS vs causal, m_Q = 500 GeV, 3.8 T, no material', color='#B3261E')
    fig.tight_layout(); fig.savefig(o('T2_string_methods_B_rep.png'), dpi=130)


JOBS.update({'fisher': fisher, 'comb': comb, 'smb': smb})

if __name__ == '__main__':
    names = sys.argv[1:] or list(JOBS)
    for n in names:
        print('==', n, flush=True)
        JOBS[n]()
