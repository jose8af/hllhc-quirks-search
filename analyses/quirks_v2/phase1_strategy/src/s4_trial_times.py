"""s4_trial_times.py -- feasibility A (Anselm): per-trial finder timing from Stage-4 benchmark outputs (TT env, worker).

Usage: python s4_trial_times.py <bench_root> <label>
Reads every <bench_root>/s4pu_*/s4/prod/bench/*/*.npz, takes trials.times (columns trials.times_cols, seconds per
trial, recorded by finder/production.process_trial) and the chain per-event stage timing, and appends one JSON line
per file to phase1_strategy/outputs/feasibility/bench_logs/s4_trials.jsonl.
"""
import json
import socket
import sys
from pathlib import Path

import numpy as np

QV2 = Path(__file__).resolve().parents[2]
OUT = QV2 / 'phase1_strategy' / 'outputs' / 'feasibility' / 'bench_logs' / 's4_trials.jsonl'


def main():
    root, label = Path(sys.argv[1]), sys.argv[2]
    with open(OUT, 'a') as fo:
        for f in sorted(root.glob('s4pu_*/s4/prod/bench/*/*.npz')):
            with np.load(f) as z:
                t = z['trials.times']
                cols = [str(c) for c in z['trials.times_cols']]
                rec = dict(label=label, file=str(f.relative_to(root)), host=socket.gethostname(), n_trials=int(len(t)),
                           cols=cols, mean_per_trial=dict(zip(cols, t.mean(0).tolist())),
                           sum_per_trial=float(t.sum(1).mean()), p90_find=float(np.percentile(t[:, cols.index('find')], 90))
                           if 'find' in cols else None, bytes=f.stat().st_size)
            fo.write(json.dumps(rec) + '\n')
            print(rec['file'], rec['n_trials'], {k: round(v, 3) for k, v in rec['mean_per_trial'].items()})


if __name__ == '__main__':
    main()
