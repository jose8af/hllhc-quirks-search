"""m2_compare.py -- P1-d Linux difference: compare v1's tracked Stage-1 M2 result (analytic/numerics/results/M2.json, copied
from v1 unchanged) with the Linux rerun (p2-b-p1-time job p1d-m2-linux, M2_linux.json).  Every numeric leaf is compared;
leaves whose relative difference exceeds 1e-6 are listed with both values.  Reading (STR §4.15): if a quoted P1 number
moves, it is corrected and listed in the errata.
Usage: python3 -I m2_compare.py <M2_v1.json> <M2_linux.json> <out.json>
"""
import json
import logging
import sys

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('m2_compare')


def leaves(x, path=''):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from leaves(v, f'{path}/{k}')
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from leaves(v, f'{path}[{i}]')
    elif isinstance(x, (int, float)) and not isinstance(x, bool):
        yield path, float(x)


def main():
    a = dict(leaves(json.load(open(sys.argv[1]))))
    b = dict(leaves(json.load(open(sys.argv[2]))))
    diff, missing = [], sorted(set(a) ^ set(b))
    for k in sorted(set(a) & set(b)):
        x, y = a[k], b[k]
        den = max(abs(x), abs(y), 1e-300)
        r = abs(x - y) / den
        if r > 1e-6:
            diff.append(dict(key=k, v1=x, linux=y, rel=r))
    diff.sort(key=lambda d: -d['rel'])
    json.dump(dict(n_common=len(set(a) & set(b)), n_diff=len(diff), only_in_one=missing, diffs=diff),
              open(sys.argv[3], 'w'), indent=1)
    log.info('common %d, differing %d, only in one %d', len(set(a) & set(b)), len(diff), len(missing))
    for d in diff[:40]:
        log.info('%s: v1 %.6g linux %.6g (rel %.2g)', d['key'], d['v1'], d['linux'], d['rel'])


if __name__ == '__main__':
    main()
