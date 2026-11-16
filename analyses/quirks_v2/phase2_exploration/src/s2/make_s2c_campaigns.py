"""make_s2c_campaigns.py -- write the runner campaigns of the S2-c inclusive samples (channel (ii), Sebastian).
  p2-b-s2c-inc : MLM 0-2j inclusive (v1 INC cards) chunks, nominal shower (CP5, qCut 45, QED-FSR) -> LHE + npz
  p2-b-s2c-rs  : re-showers of the same LHE: qc30+qc60 in one job, monash+nofsr in another (run after -inc is complete)
Usage: python3 -I make_s2c_campaigns.py <events_per_chunk> <chunks_per_point>
"""
import json
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('make_s2c')
CAMP = Path('/home/users/jdochoa/hllhc-quirks-search/tools/campaigns/p2-b')
S = 'python3 -I /home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2/phase2_exploration/src/s2/s2_job.py'
DATA = '/nfs/cajuela/jdochoa/quirks_v2/data/p2-b-s2c-inc'
POINTS = [('F_INC', 200, 0), ('F_INC', 500, 1), ('F_INC', 1000, 2), ('F_INC', 1500, 3), ('S_INC', 500, 4)]


def main():
    nev, nch = int(sys.argv[1]), int(sys.argv[2])
    inc, rs = [], []
    for proc, m, shard in POINTS:
        for c in range(nch):
            tag = f'{proc[0].lower()}inc-m{m}-c{c:02d}'
            inc.append(dict(id=tag, shard=shard, max_rss_mb=1500, timeout_s=1800,
                            command=f'{S} inc {tag} {proc} {m} {nev}',
                            outputs=[f'{tag}.lhe.gz', f'{tag}.nom.npz', f'{tag}.json', f'{tag}.aux.tar.gz']))
            src = f'{DATA}/{shard:03d}'
            for vv in ('qc30,qc60', 'monash,nofsr'):
                v1, v2 = vv.split(',')
                rs.append(dict(id=f'{tag}-rs-{v1}', shard=shard, max_rss_mb=1500, timeout_s=1800,
                               command=f'{S} reshower {tag} {src} {vv}',
                               outputs=[f'{tag}.{v1}.npz', f'{tag}.{v2}.npz', f'{tag}.rs.{v1}_{v2}.json']))
    json.dump(dict(campaign='p2-b-s2c-inc', tier='final', expected_hours=4.0,
                   description='channel (ii) S2-c: MLM 0-2j inclusive signal samples (E 200/500/1000/1500, Etilde 500) '
                               'for f200 and its uncertainty; nominal shower CP5 + QED-FSR (S2-d)', jobs=inc),
              open(CAMP / 'p2-b-s2c-inc.json', 'w'), indent=1)
    json.dump(dict(campaign='p2-b-s2c-rs', tier='final', expected_hours=6.0,
                   description='channel (ii) S2-c: re-showers of the p2-b-s2c-inc LHE (qCut 30, 60; Monash; FSR off)',
                   jobs=rs), open(CAMP / 'p2-b-s2c-rs.json', 'w'), indent=1)
    log.info('inc jobs %d, rs jobs %d', len(inc), len(rs))


if __name__ == '__main__':
    main()
