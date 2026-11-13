"""INV_A2FC_E500 step 12: full-sample tallies of the replica runs (inv_a2fc_e500_replica_*.json): per smear draw k the
number of rows passing R08/R10/R11/R14 with numpy quirk smearing on the A2FC PU event, over the rows that pass R08 in A2
or A2FC (others assumed to fail; R14 needs R08).  -> data/acts_stage4/investigation/inv_a2fc_e500_repsum.json"""
import glob
import json
from pathlib import Path

TT = Path(__file__).resolve().parents[3]
D = TT / 'data/acts_stage4/investigation'
R = {}
for f in sorted(glob.glob(str(D / 'inv_a2fc_e500_replica_A2_F500_*_L3.json'))):
    R.update(json.loads(Path(f).read_text()))
ev = json.loads((D / 'inv_a2fc_e500_events_F500_L3.json').read_text())['rows']
out = dict(n_rows=len(R), rungs=['R04', 'R08', 'R10', 'R11', 'R14'], tallies={})
for k in ('-1', '0', '1'):
    t = [0] * 5
    for r, x in R.items():
        v = x['FCPU'].get(k)
        if v:
            t = [a + b for a, b in zip(t, v)]
    out['tallies'][f'FCPU_numpy_k{k}'] = t
# A2PU (chunk 1 only)
out['note'] = ('k=-1 = the production numpy smear (selection-biased: the rows were chosen partly by its A2 outcome); '
               'k=0,1 = fresh draws (unbiased).  Row 268 has 46 quirk hits stolen by the CKF in A2FC (absent here).')
out['row268'] = {k: R['268']['FCPU'][k] for k in ('-1', '0', '1')}
print(json.dumps(out, indent=1))
(D / 'inv_a2fc_e500_repsum.json').write_text(json.dumps(out, indent=1))
