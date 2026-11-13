"""bench_run.py -- feasibility A (Anselm): run one benchmark unit under /usr/bin/time -v and record it (stdlib only).

Usage (on a worker):
  python3 -I bench_run.py --label L --rep R --conc C --workdir DIR [--units N] [--unit-name event] -- CMD ARGS...
Runs `nice -n 10 /usr/bin/time -v -o <workdir>/time.txt CMD ARGS` in DIR (created, node-local scratch), keeps the
last 40 lines of stdout+stderr, parses user/sys/wall/max RSS, and appends one JSON line to
  phase1_strategy/outputs/feasibility/bench_logs/<label>.jsonl
(the full /usr/bin/time -v text and the output tail are stored in the record, so every number is citable).
`--units` is the number of work units (events, trials) the command processed, for the per-unit columns.
"""
import argparse
import json
import os
import platform
import re
import socket
import subprocess
import sys
import time
from pathlib import Path

QV2 = Path(__file__).resolve().parents[2]
LOGS = QV2 / 'phase1_strategy' / 'outputs' / 'feasibility' / 'bench_logs'


def parse_time(txt):
    def g(key, conv=float):
        m = re.search(rf'^\s*{re.escape(key)}:\s*(.+)$', txt, re.M)
        return conv(m.group(1).strip()) if m else None

    def wall(s):
        parts = [float(x) for x in s.split(':')]
        v = 0.0
        for p in parts:
            v = v * 60 + p
        return v
    return dict(user_s=g('User time (seconds)'), sys_s=g('System time (seconds)'),
                wall_s=g('Elapsed (wall clock) time (h:mm:ss or m:ss)', wall),
                max_rss_kb=g('Maximum resident set size (kbytes)', int), exit_status=g('Exit status', int),
                major_faults=g('Major (requiring I/O) page faults', int), cpu_pct=g('Percent of CPU this job got', str))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--label', required=True)
    ap.add_argument('--rep', type=int, required=True)
    ap.add_argument('--conc', type=int, required=True, help='number of benchmark jobs running at the same time')
    ap.add_argument('--workdir', required=True)
    ap.add_argument('--units', type=float, default=None)
    ap.add_argument('--unit-name', default='event')
    ap.add_argument('--note', default='')
    ap.add_argument('cmd', nargs=argparse.REMAINDER)
    a = ap.parse_args()
    cmd = a.cmd[1:] if a.cmd and a.cmd[0] == '--' else a.cmd
    wd = Path(a.workdir)
    wd.mkdir(parents=True, exist_ok=True)
    tf = wd / f'time_{a.rep}.txt'
    of = wd / f'out_{a.rep}.txt'
    t0 = time.time()
    with open(of, 'w') as fo:
        r = subprocess.run(['nice', '-n', '10', '/usr/bin/time', '-v', '-o', str(tf)] + cmd, cwd=wd, stdout=fo,
                           stderr=subprocess.STDOUT, env=os.environ)
    ttxt = tf.read_text() if tf.exists() else ''
    rec = dict(label=a.label, rep=a.rep, conc=a.conc, host=socket.gethostname(), cpu=platform.processor() or platform.machine(),
               start=time.strftime('%Y-%m-%dT%H:%M:%S%z', time.localtime(t0)), cmd=cmd, cwd=str(wd), returncode=r.returncode,
               units=a.units, unit_name=a.unit_name, note=a.note, loadavg_end=os.getloadavg(), **parse_time(ttxt))
    if rec['user_s'] is not None:
        rec['cpu_s'] = rec['user_s'] + rec['sys_s']
        if a.units:
            rec['cpu_s_per_unit'] = rec['cpu_s'] / a.units
            rec['wall_s_per_unit'] = rec['wall_s'] / a.units
    rec['time_v'] = ttxt
    rec['out_tail'] = of.read_text(errors='replace').splitlines()[-40:]
    LOGS.mkdir(parents=True, exist_ok=True)
    with open(LOGS / f'{a.label}.jsonl', 'a') as f:
        f.write(json.dumps(rec) + '\n')
    sys.stdout.write(f"{a.label} rep {a.rep} conc {a.conc}: rc {r.returncode} cpu {rec.get('cpu_s')} wall {rec['wall_s']} "
                     f"rss {rec['max_rss_kb']} kB\n")
    return r.returncode


if __name__ == '__main__':
    sys.exit(main())
