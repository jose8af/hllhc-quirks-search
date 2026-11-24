import sys; sys.path.insert(0,'/home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2/phase3_selection/src/p3d')
import p3d_specs, p3d_model as pm, numpy as np
import logging; logging.basicConfig(level=logging.INFO, format="%(message)s"); log=lambda *a: logging.info(" ".join(str(x) for x in a))
s=p3d_specs.get(sys.argv[1])
log('npar', pm.n_parameters(s), 'counted', len(s['counted']), 'samples', len(s['samples']))
for r in pm.term_table(s):
  log(r['term'], {c:'%.4g'%v for c,v in r['yield_coeff'].items()}, [(f.split('|')[-1], m, M) for f,m,M in r['counted']], {k:round(v,3) if not isinstance(v,list) else v for k,v in r['nuis'].items()})
for n in s["meta"].get("notes",[]): log('NOTE', n)
log({k:round(v['bound'],3) for k,v in s['nuis'].items() if v['bound'] is not None})
p=pm.predictive(s, nmc=100000)
log(p['cats'], 'f0', p['f0'])
for t,d in sorted(p['terms'].items(), key=lambda x:-x[1]['B84'])[:8]: log(t,d)
log('lead', pm.leading_zero_term(s,p))
