"""make_s3_bench_jobs.py -- feasibility A (Anselm): Stage-3 job lists for the smoke test and the benchmarks (stdlib).

Jobs use the v1 p2 production settings (sim/stage3/jobs/all.json, F_m500 BM): cfg 'BM' (B = 3.8112 T + material),
luminous-region vertex, hmax 0.2, max_boost 1e-3 for Lambda <= 5 keV and 1e-2 for Lambda >= 7 keV.
Input: the toy file <spin>_m<m>_toy.npz (make_s3_toy_input.py).  Writes phase1_strategy/src/jobs/s3_{smoke,bench}.json.
Run: python3 -I phase1_strategy/src/make_s3_bench_jobs.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / 'jobs'
# Lambda [keV] -> events per benchmark job (sized for ~1-3 min per job on one M3 core, from the v1 per-event CPU of
# p2/F_m500 BM in STAGE3_INDEX.json: 0.33 / 8.2 / 32 / 16.5 s at 1 / 3 / 5 / 10 keV)
BENCH = {1.0: 30, 3.0: 8, 5.0: 4, 10.0: 6}
SMOKE = {1.0: 4, 3.0: 4, 10.0: 4}


def job(camp, m, lam, evs):
    mb = 1e-3 if lam <= 5.0 else 1e-2
    jid = f'{camp}/F_m{m}__L{lam:g}_BM_c00'
    return dict(id=jid, out=f'{camp}/F_m{m}/L{lam:g}_BM_c00.npz', campaign=camp, spin='F', m=m, lam=lam, cfg='BM',
                chunk=0, input=f'F_m{m}_toy.npz', ev=list(evs), max_boost=mb, hmax=0.2, vertex='lumi', est_s=0.0)


def main():
    OUT.mkdir(exist_ok=True)
    smoke = [job('s3smoke', 500, lam, range(n)) for lam, n in SMOKE.items()]
    json.dump(dict(name='s3smoke', jobs=smoke), open(OUT / 's3_smoke.json', 'w'), indent=1)
    for lam, n in BENCH.items():
        for m in (500, 1000):
            j = job('s3bench', m, lam, range(n))
            json.dump(dict(name=f's3bench_m{m}_L{lam:g}', jobs=[j]), open(OUT / f's3_bench_m{m}_L{lam:g}.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
