"""make_p1_campaigns.py -- runner campaigns for P1 on new events (channel (ii), Sebastian).
  p2-b-p1-ev  : event sets from p2-b-s2c-inc (make_p1_events.py) for the five P1 points at 1 keV, E500/E1000 at 5 and 3 keV
  p2-b-p1-run : B*-off paired test at 5 keV (E500 + E1000, ~970 events), B*-off + population at 1 keV (300 x 5 points),
                floor test 2 + dd diagnostic at 3 keV, s = 1/9 (40 events x E500/E1000 x 3 kernels)
Usage: python3 -I make_p1_campaigns.py
"""
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('make_p1_campaigns')
CAMP = Path('/home/users/jdochoa/hllhc-quirks-search/tools/campaigns/p2-b')
QV2 = '/home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2'
PY = f'{QV2}/envs/tt/.pixi/envs/default/bin/python'
SRC = f'{QV2}/phase2_exploration/src/p1'
INC = '/nfs/cajuela/jdochoa/quirks_v2/data/p2-b-s2c-inc'
EV = '/nfs/cajuela/jdochoa/quirks_v2/data/p2-b-p1-ev/000'
PRE = ('export NUMBA_CACHE_DIR=$QV2_SCRATCH_DIR/numba PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 NUMBA_NUM_THREADS=1; ')
POINTS = {'e200': ('000', 'finc-m200', 200, 'F'), 'e500': ('001', 'finc-m500', 500, 'F'), 'e1000': ('002', 'finc-m1000', 1000, 'F'),
          'e1500': ('003', 'finc-m1500', 1500, 'F'), 's500': ('004', 'sinc-m500', 500, 'S')}


def job(i, cmd, outs, rss=800):
    return dict(id=i, shard=0, max_rss_mb=rss, timeout_s=1800, command=PRE + cmd, outputs=outs)


def main():
    ev = []
    sets = [(p, 1.0) for p in POINTS] + [('e500', 5.0), ('e1000', 5.0), ('e500', 3.0), ('e1000', 3.0)]
    for p, lam in sets:
        sh, pre, m, sp = POINTS[p]
        name = f'p1ev-{p}-l{lam:g}'
        ev.append(job(name, f'{PY} {SRC}/make_p1_events.py $QV2_OUT_DIR/{name}.npz {INC}/{sh}/{pre} {m} {sp} {lam}',
                      [f'{name}.npz']))
    runs = []
    for p in ('e500', 'e1000'):                                   # P1-b at 5 keV: 485 events each, 60 per job
        for k, i0 in enumerate(range(0, 485, 60)):
            n = min(60, 485 - i0)
            name = f'bstar5-{p}-{k:02d}'
            runs.append(job(name, f'{PY} {SRC}/p1_runs.py $QV2_OUT_DIR/{name}.json {EV}/p1ev-{p}-l5.npz bstar 5.0 {i0} {n}',
                            [f'{name}.json']))
    for p in POINTS:                                              # P1-b at 1 keV and P1-c: 300 events per point
        name = f'bstar1-{p}'
        runs.append(job(name, f'{PY} {SRC}/p1_runs.py $QV2_OUT_DIR/{name}.json {EV}/p1ev-{p}-l1.npz bstar 1.0 0 300',
                        [f'{name}.json']))
    for p in ('e500', 'e1000'):                                   # P1-a floor test 2 and the dd diagnostic
        for kern in ('nominal', 't44', 'dd'):
            name = f'floor-{p}-{kern}'
            runs.append(job(name, f'{PY} {SRC}/p1_runs.py $QV2_OUT_DIR/{name}.json {EV}/p1ev-{p}-l3.npz floor 3.0 0 40 '
                                  f'--kernel {kern} --s 0.1111111111 --fr 1,0.5,0.4,0.25,0.05', [f'{name}.json']))
    json.dump(dict(campaign='p2-b-p1-ev', tier='regenerable', expected_hours=0.5,
                   description='channel (ii) P1: new event sets (|eta_pair| < 1, pT(QQ) > 200, w > 0) from p2-b-s2c-inc, '
                               'with closed-form c_ev, k_B per Lambda', jobs=ev), open(CAMP / 'p2-b-p1-ev.json', 'w'), indent=1)
    json.dump(dict(campaign='p2-b-p1-run', tier='final', expected_hours=7.0,
                   description='channel (ii) P1-a/b/c on new events: paired B*-off at 5 and 1 keV, population estimator at '
                               '1 keV, floor test 2 (44-bit kernel) and double-double diagnostic', jobs=runs),
              open(CAMP / 'p2-b-p1-run.json', 'w'), indent=1)
    log.info('ev jobs %d, run jobs %d', len(ev), len(runs))


if __name__ == '__main__':
    main()
