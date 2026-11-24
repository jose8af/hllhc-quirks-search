"""Seed disjointness of dev.pu1 against c1.pu1, c1.pu2, prod.pu1, prod.pu2, reserve.pu1 (STR §4.17).

  python3 -I phase3_selection/src/p3e/seed_check.py      (from AN; writes outputs/p3e/seed_disjoint.json)

Job seed = blake2b("qv2|<stream>|<chunk>", digest 8, little endian) & 0x7FFFFFFFFFFF, the formula of
acts/stage4/run_stage4.py hash_seed (copied here, checked against the import-free source text below) as called by
phase2_exploration/src/c1_pu_job.py.  Reports the seeds of the first and last chunk of each stream (chunk ranges from the
campaign files; reserve.pu1 has no campaign yet: 24,000 events at 20 per job -> chunks 0..1199, ESTIMATE) and checks
that the full sets over the actual ranges, and over chunks 0..99,999 of every stream, are pairwise disjoint.
"""
import hashlib
import json
import re
from itertools import combinations
from pathlib import Path

AN = Path(__file__).resolve().parents[3]
REPO = AN.parents[1]
SRC_RS = AN / 'acts' / 'stage4' / 'run_stage4.py'


def hash_seed(s):
    return int.from_bytes(hashlib.blake2b(s.encode(), digest_size=8).digest(), 'little') & 0x7FFFFFFFFFFF


def chunks_of(campaign):
    d = json.loads(Path(campaign).read_text())
    st = {re.search(r'--stream (\S+)', j['command']).group(1) for j in d['jobs']}
    ch = sorted(int(re.search(r'--chunk (\d+)', j['command']).group(1)) for j in d['jobs'])
    assert len(st) == 1 and len(set(ch)) == len(ch)
    return st.pop(), ch, str(Path(campaign).relative_to(REPO))


def main():
    src = SRC_RS.read_text()
    assert ("return int.from_bytes(hashlib.blake2b(s.encode(), digest_size=8).digest(), 'little') & 0x7FFFFFFFFFFF"
            in src), 'hash_seed in run_stage4.py differs from the copy here'
    assert 'RS.hash_seed(f"qv2|{a.stream}|{a.chunk}")' in (AN / 'phase2_exploration/src/c1_pu_job.py').read_text()
    camps = [REPO / 'tools/runner/campaigns/p2-a-c1-pu1.json', REPO / 'tools/runner/campaigns/p2-a-c1-pu2.json',
             AN / 'phase3_selection/src/p3b/campaigns/prod/p4a-b2-prod-pu1.json',
             AN / 'phase3_selection/src/p3b/campaigns/prod/p4a-b2-prod-pu2.json',
             AN / 'phase3_selection/src/p3e/campaigns/p3-e-devpu1.json']
    streams = {}
    for c in camps:
        s, ch, rel = chunks_of(c)
        streams[s] = dict(chunks=ch, source=rel)
    streams['reserve.pu1'] = dict(chunks=list(range(1200)), source='ESTIMATE: STR §4.17 row 16, 24,000 events, 20/job')
    res = dict(formula='blake2b("qv2|<stream>|<chunk>", digest_size=8) little-endian & 0x7FFFFFFFFFFF '
                       '(acts/stage4/run_stage4.py hash_seed)', streams={}, pairs={}, wide_range=None)
    sets = {}
    for s, v in streams.items():
        ch = v['chunks']
        seeds = [hash_seed(f'qv2|{s}|{k}') for k in ch]
        sets[s] = set(seeds)
        res['streams'][s] = dict(source=v['source'], n_chunks=len(ch), first_chunk=ch[0], last_chunk=ch[-1],
                                 seed_first=seeds[0], seed_last=seeds[-1], unique_within=len(set(seeds)) == len(seeds))
    for a, b in combinations(sorted(sets), 2):
        res['pairs'][f'{a} vs {b}'] = len(sets[a] & sets[b])
    wide = {s: {hash_seed(f'qv2|{s}|{k}') for k in range(100000)} for s in streams}
    wide_pairs = {f'{a} vs {b}': len(wide[a] & wide[b]) for a, b in combinations(sorted(wide), 2)}
    res['wide_range'] = dict(chunks='0..99999 for every stream', unique_within={s: len(w) == 100000 for s, w in wide.items()},
                             overlaps=wide_pairs)
    dev = 'dev.pu1'
    res['verdict_dev_pu1'] = ('DISJOINT' if all(v == 0 for k, v in res['pairs'].items() if dev in k)
                              and all(v == 0 for k, v in wide_pairs.items() if dev in k) else 'OVERLAP')
    res['verdict_all_pairs'] = ('DISJOINT' if all(v == 0 for v in res['pairs'].values())
                                and all(v == 0 for v in wide_pairs.values()) else 'OVERLAP')
    out = AN / 'phase3_selection/outputs/p3e/seed_disjoint.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1) + '\n')
    for s, v in res['streams'].items():
        print(f"{s:12s} chunks {v['first_chunk']}..{v['last_chunk']} ({v['n_chunks']}) seed_first {v['seed_first']} "
              f"seed_last {v['seed_last']} unique {v['unique_within']}")
    print('pairs (actual ranges):', res['pairs'])
    print('pairs (0..99999):', wide_pairs)
    print('dev.pu1:', res['verdict_dev_pu1'], ' all pairs:', res['verdict_all_pairs'])


if __name__ == '__main__':
    main()
