"""G2b criterion (plan §6.2 / §11): t2 <= t2,max, the largest t2 at which every campaign the user chose fits <= 1 Mac
day AND the chosen set fits the production window.  Arithmetic only: blocks() of probes/f4r_deadline.py (= f3r blocks
+ C' in C1), executed read-only up to its result section; t1 = G2a mean, t2 = G2b mean (both measured).
User's set (D4-16, LOG 2026-10-13 16:12): C1 -> C2, then C4' (C4 without A3/A4) only if C2 ends by Thu 22:00.
Run (theory_track): pixi run python -m acts.stage4.finder.g2b_criterion -> data/acts_stage4/g2b/g2b_criterion.json
"""
import json

from .trials import TT

SRC = (TT / 'acts' / 'stage4' / 'probes' / 'f4r_deadline.py').read_text()
NS = {'__file__': str(TT / 'acts' / 'stage4' / 'probes' / 'f4r_deadline.py')}
exec(SRC[:SRC.index('res = {')], NS)
cpu, root, CAP, MAC_W = NS['cpu'], NS['root'], NS['CAP'], NS['MAC_W']
G2 = TT / 'data' / 'acts_stage4' / 'g2'
G2B = TT / 'data' / 'acts_stage4' / 'g2b'


def t2max(t1, cs, window_h):
    def worst(t2):
        per = max(cpu(c, t1, t2, d) - CAP for c, d in cs)
        win = sum(cpu(c, t1, t2, d) for c, d in cs) - window_h * MAC_W
        return max(per, win)
    return root(worst, 0.1, 5000)


def main():
    t1 = json.loads((G2 / 'timing_rho1.json').read_text())['summary_wall']['mean']
    g = json.loads((G2B / 'timing_g2b_final.json').read_text())   # final production config (incl. the delta95 cut)
    t2 = g['summary_wall']['mean']
    t2_find = float(sum(r['times_s']['find'] for r in g['trials']) / len(g['trials']))
    C4p = ('C4', ('A3', 'A4'))
    sets = {'C1': [('C1', ())], 'C1+C2': [('C1', ()), ('C2', ())], 'C1+C2+C4p': [('C1', ()), ('C2', ()), C4p]}
    res = dict(t1_mean_s=t1, t2_mean_s=t2, t2_median_s=g['summary_wall']['median'], t2_p90_s=g['summary_wall']['p90'],
               t2_finder_only_mean_s=t2_find, mac_cpu_h_per_day=CAP, window_h_plan=47, sets={})
    for name, cs in sets.items():
        row = {}
        for win in (47, 53):
            row[f't2max_s_window{win}h'] = t2max(t1, cs, win)
        row['cpu_h_at_measured'] = {c + ('p' if d else ''): round(cpu(c, t1, t2, d), 1) for c, d in cs}
        row['wall_h_at_measured_7w'] = round(sum(cpu(c, t1, t2, d) for c, d in cs) / MAC_W, 1)
        row['wall_h_at_measured_5p5w'] = round(sum(cpu(c, t1, t2, d) for c, d in cs) / 5.5, 1)
        row['each_fits_1day'] = all(cpu(c, t1, t2, d) <= CAP for c, d in cs)
        row['pass_47h'] = t2 <= row['t2max_s_window47h']
        res['sets'][name] = row
    res['G2b_PASS_chosen_C1_C2'] = res['sets']['C1+C2']['pass_47h']
    res['note'] = ('t2max = largest t2 with every campaign <= 168 CPU-h (1 Mac day at 7 workers) and the set inside the '
                   'window (47 h plan; 53 h = 47 h + the ~6 h lead the orchestrator reports). C4p is optional under the '
                   "user's rule (only if C2 ends by Thu 22:00). PU event without finder 4.7 s is the plan ESTIMATE (G1).")
    (G2B / 'g2b_criterion.json').write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == '__main__':
    main()
