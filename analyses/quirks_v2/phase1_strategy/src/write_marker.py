"""write_marker.py -- feasibility A (Anselm): ledger marker for a finished output file on cajuela (stdlib only).

Usage: python3 -I write_marker.py <output file under analyses/quirks_v2/data/> [--cpu-s X] [--max-rss-mb Y] [--job ID]
Appends one JSON line (status "done", path, sha256, bytes, cpu_s, max_rss_mb, host, time) to
  analyses/quirks_v2/ledger/markers/feasibility_chain/<relative path with '/' -> '__'>.marker
(the JSON-lines marker format of tools/runner/qv2run/markers.py). The marker is written as .part then renamed.
"""
import argparse
import hashlib
import json
import os
import socket
import time
from pathlib import Path

QV2 = Path(__file__).resolve().parents[2]
DATA_REAL = Path('/nfs/cajuela/jdochoa/quirks_v2/data')
MARK = QV2 / 'ledger' / 'markers' / 'feasibility_chain'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('path')
    ap.add_argument('--cpu-s', type=float, default=None)
    ap.add_argument('--max-rss-mb', type=float, default=None)
    ap.add_argument('--job', default=None)
    a = ap.parse_args()
    p = Path(a.path).absolute()
    real = Path(os.path.realpath(p))
    rel = real.relative_to(DATA_REAL)
    h = hashlib.sha256()
    with open(real, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    rec = dict(status='done', job=a.job or str(rel), path=str(DATA_REAL / rel), sha256=h.hexdigest(),
               bytes=real.stat().st_size, cpu_s=a.cpu_s, max_rss_mb=a.max_rss_mb, host=socket.gethostname(),
               writer='anselm/feasibility', t=time.strftime('%Y-%m-%dT%H:%M:%S%z'))
    MARK.mkdir(parents=True, exist_ok=True)
    m = MARK / (str(rel).replace('/', '__') + '.marker')
    old = m.read_text() if m.exists() else ''
    part = m.with_name(m.name + '.part')
    with open(part, 'w') as f:
        f.write(old + json.dumps(rec, sort_keys=True) + '\n')
        f.flush(); os.fsync(f.fileno())
    os.replace(part, m)
    print(f'{m.name}: {rec["sha256"][:12]} {rec["bytes"]} B')


if __name__ == '__main__':
    main()
