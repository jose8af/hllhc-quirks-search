"""p2h_ephcount.py -- count of the flagged "early product hit" events over finished B1 pilot chain files.

  <acts python> p2h_ephcount.py <out.json> <manifest.json>

manifest.json: list of {path, campaign, job_id, node, bytes} (done markers of the chain campaigns).  Per file only the
zip members `meta` and `n_early_prod` are read (and `evt` of a file that has flagged events, to record the flagged
rows); no hit array is opened, nothing is recomputed, no pilot file is written.  Read-only diagnostic for
B1_STREAM_VALIDATION (Hedda, 2026-11-18); not part of the frozen pilot code and imports none of it.
"""
import json
import logging
import sys
import time
from pathlib import Path

import numpy as np

logging.basicConfig(level=logging.INFO, format='%(asctime)s p2h_ephcount %(message)s', handlers=[logging.StreamHandler(sys.stderr)])
log = logging.getLogger('p2h_ephcount')


def one(e):
    z = np.load(e['path'])
    m = json.loads(str(z['meta']))
    ne = z['n_early_prod']
    idx = np.nonzero(ne > 0)[0]
    vm = m.get('vertex_file_meta', {})
    r = dict(path=e['path'], campaign=e['campaign'], job_id=e['job_id'], node=e.get('node'), sample=m['sample'],
             stream=m['stream'], chunk=m['chunk'], first_vertex=m.get('first_vertex'), n_events=int(m['n_events']),
             n_array=int(len(ne)), trunc_mode=m.get('trunc_mode'), beta_min=m.get('beta_min'),
             vertex_file=Path(str(m.get('vertex_file', ''))).name, vertex_chunk=vm.get('chunk'),
             n_per_class=m.get('n_per_class'), n_per_ev_mode=m.get('n_per_ev_mode'),
             early_hits=int(ne.sum()), early_events=int(len(idx)),
             meta_early_hits=m.get('n_product_hits_before_own_production'),
             meta_early_events=m.get('n_events_with_product_hits_before_own_production'), flagged=[])
    if len(idx):
        ev = z['evt']; cols = m['evt_cols']
        for i in idx:
            r['flagged'].append(dict(event=int(i), n_early=int(ne[i]), evt={c: float(v) for c, v in zip(cols, ev[i])}))
    z.close()
    return r


def main(out, manifest):
    ents = json.loads(Path(manifest).read_text())
    t0 = time.time(); res = []; errors = []
    for k, e in enumerate(ents):
        try:
            res.append(one(e))
        except Exception as x:          # a file that cannot be read is reported, not skipped silently
            errors.append(dict(path=e['path'], error=repr(x)))
            log.error('%s: %r', e['path'], x)
        if (k + 1) % 50 == 0:
            log.info('%d of %d files, %.0f s', k + 1, len(ents), time.time() - t0)
    summ = dict(n_files_listed=len(ents), n_files_read=len(res), n_errors=len(errors), errors=errors,
                n_events=sum(r['n_events'] for r in res), early_hits=sum(r['early_hits'] for r in res),
                early_events=sum(r['early_events'] for r in res),
                meta_consistent=all(r['early_hits'] == r['meta_early_hits'] and r['early_events'] == r['meta_early_events']
                                    and r['n_array'] == r['n_events'] for r in res),
                manifest=str(manifest), wall_s=time.time() - t0, files=res)
    Path(out + '.tmp').write_text(json.dumps(summ, indent=1))
    Path(out + '.tmp').replace(out)
    log.info('%d files, %d events, %d early hits in %d events, %d errors', len(res), summ['n_events'], summ['early_hits'],
             summ['early_events'], len(errors))
    return 0          # unreadable files are listed under 'errors' in the output (the job itself must keep its output)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
