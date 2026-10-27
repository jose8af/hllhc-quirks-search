"""R2: leaf-by-leaf diff of sandbox reruns against the delivered results; also count leaves present in R1's sandbox copy
(pre-fix) whose values changed (pre-existing central values)."""
import json, math, sys
from pathlib import Path
S3 = Path('/Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track/sim/stage3')
def leaves(o, p=''):
    if isinstance(o, dict):
        for k, v in o.items(): yield from leaves(v, f'{p}/{k}')
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from leaves(v, f'{p}[{i}]')
    else: yield p, o
def same(a, b):
    if isinstance(a, float) and isinstance(b, float):
        return (math.isnan(a) and math.isnan(b)) or a == b
    return a == b
for f in ('P1.json', 'P2.json', 'P2_points.json'):
    D = dict(leaves(json.load(open(S3/'results'/f)))); N = dict(leaves(json.load(open(S3/'review/r2_checks/repro/results'/f))))
    O = dict(leaves(json.load(open(S3/'review/r1_checks/repro/results'/f))))
    diff = [k for k in D if k in N and not same(D[k], N[k])]; miss = set(D) ^ set(N)
    pre = [k for k in O if k in D and not same(O[k], D[k])]; gone = [k for k in O if k not in D]
    print(f, 'delivered leaves', len(D), '| rerun diffs', len(diff), 'key mismatch', len(miss), '| R1-era leaves', len(O), 'changed since R1', len(pre), 'removed since R1', len(gone))
    for k in (pre + gone)[:8]: print('   ', k, O.get(k), '->', D.get(k))
