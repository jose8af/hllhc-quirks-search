import numpy as np, json
from acts.stage4.analysis import common as C
d = C.load_npz(C.PROD/'C1'/'A1'/'A1_p2_F_m500_L5_BM.npz')
cols=[str(c) for c in d['sig.cols']]; ci={c:i for i,c in enumerate(cols)}
ex=json.load(open(C.TT/'data/acts_stage4/investigation/classify_F500.json'))['5.0']['examples']['no_qcand']
tab=d['sig.tab']
for r in ex:
    k=int(np.where(tab[:,ci['row']]==r)[0][0]); ti=int(d['sig.trial'][k])
    print(r, {c: tab[k,ci[c]] for c in ('n_q_written','n_q_ckf','n_q_pool','n_q_road','n_cand_q','best_frac')},
      {c: d['trials.'+c][ti] for c in ('n_road','n_trip','n_refit','n_kept_all','n_loose','phimet')}, 'phi_true', tab[k,ci['phimet_true']])
