"""cpu_tally.py -- channel (ii) CPU accounting per campaign from the ledger markers (the source of jobs.tsv), stdlib only.
Channel (ii), Edgar, 2026-11-17.  For every p2-b-* campaign: sum over every terminal marker line (each attempt:
done / failed / timeout / oom / killed / ...) of cpu_s (user + sys of the job's waited-for children) and wall_s, number
of jobs, attempts and statuses.  The aMC@NLO event-mode artefact (MG's integration processes are not waited-for children,
so cpu_s misses them) is handled by charging the listed campaigns at wall time x 1 core in the column 'charged_h'.
Usage: python3 -I cpu_tally.py <out.json>
"""
import glob
import json
import logging
import os
import sys

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('cpu_tally')
LEDGER = '/home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2/ledger/markers'
WALL_CHARGED = {'p2-b-s2-fxfx-time', 'p2-b-s2-fxfx-diag', 'p2-b-s2-fxfx-diag2'}   # EXPLORATION_ii_sebastian §2.6


def main():
    out = sys.argv[1]
    res, tot = {}, dict(cpu_h=0.0, wall_h=0.0, charged_h=0.0)
    for cd in sorted(glob.glob(os.path.join(LEDGER, 'p2-b-*'))):
        camp = os.path.basename(cd)
        r = dict(jobs=0, attempts=0, status={}, cpu_h=0.0, wall_h=0.0, nodes=set())
        for mk in glob.glob(os.path.join(cd, '[0-9][0-9][0-9]', '*.marker')):
            r['jobs'] += 1
            last = None
            for line in open(mk):
                if not line.strip():
                    continue
                d = json.loads(line)
                if d.get('status') == 'started':
                    continue
                r['attempts'] += 1
                r['cpu_h'] += (d.get('cpu_s') or 0.0) / 3600
                r['wall_h'] += (d.get('wall_s') or 0.0) / 3600
                r['nodes'].add(d.get('node'))
                last = d.get('status')
            r['status'][last or 'running'] = r['status'].get(last or 'running', 0) + 1
        r['nodes'] = sorted(x for x in r['nodes'] if x)
        r['charged_h'] = r['wall_h'] if camp in WALL_CHARGED else r['cpu_h']
        r['charging'] = 'wall x 1 core (MG event-mode artefact)' if camp in WALL_CHARGED else 'marker cpu_s'
        for k in ('cpu_h', 'wall_h', 'charged_h'):
            tot[k] += r[k]
        res[camp] = r
        log.info('%-22s jobs %3d att %3d %s cpu %.3f h wall %.3f h charged %.3f h', camp, r['jobs'], r['attempts'],
                 r['status'], r['cpu_h'], r['wall_h'], r['charged_h'])
    res['_total'] = tot
    log.info('TOTAL %s', tot)
    json.dump(res, open(out, 'w'), indent=1)


if __name__ == '__main__':
    main()
