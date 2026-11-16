"""p2c_fatras_check.py -- B1-d: does the running Fatras instance of the chain decay or absorb hadrons?

  <acts python> p2c_fatras_check.py <out.json> <n_events>

K+-, pi+- and protons from run_chain.py's own gun mode (10 per event, 1 < pT < 2 GeV, |eta| < 0.3, no pile-up), the same
sequencer as every sample.  If Fatras decayed kaons, about 9 % of them (path 1.1 m, beta gamma c tau = 11 m at 1.5 GeV)
would not reach the outermost barrel layer, against none for protons.  Reported per species: fraction of gun particles
with a hit of the primary (generation 0) on TB2S_L3_out, on TBPX_L1, and hits of later generations per particle.
"""
import json
import sys

import numpy as np

import p2c_common as C

sys.path.insert(0, str(C.CODE))
import run_chain as rc  # noqa: E402

log = C.setup_logging('p2c_fatras_check')
SURF = json.loads((C.QV2 / 'sim' / 'stage3' / 'code' / 'surfaces_s3.json').read_text())['surfaces']
SID = {s['name']: i for i, s in enumerate(SURF)}


def main(out, n):
    res = {}
    for name, pdg, mass in (('K', 321, 0.493677), ('pi', 211, 0.13957039), ('p', 2212, 0.93827209)):
        f = f'gun_{name}.npz'
        rc.TIMES.clear()
        rc.main(['gun', f, str(n), '4242', '--mu', '0', '--gun-pdg', str(pdg), '--gun-mass', str(mass), '--gun-pt', '1', '2',
                 '--gun-eta', '-0.3', '0.3', '--gun-n', '10'])
        z = np.load(f)
        tot = out3 = in1 = 0; later = 0
        for i in range(n):
            ev = z[f'ev{i}']
            g0 = ev[ev[:, 9] == 0]
            tot += 10
            out3 += len(np.unique(g0[g0[:, 0] == SID['TB2S_L3_out'], 7]))
            in1 += len(np.unique(g0[g0[:, 0] == SID['TBPX_L1'], 7]))
            later += int((ev[:, 9] > 0).sum())
        res[name] = dict(particles=tot, frac_reaching_TB2S_L3_out=out3 / tot, frac_with_TBPX_L1_hit=in1 / tot,
                         later_generation_hits_per_particle=later / tot)
        log.info('%s %s', name, res[name])
    dk = res['p']['frac_reaching_TB2S_L3_out'] - res['K']['frac_reaching_TB2S_L3_out']
    res['proton_minus_kaon_reach'] = dk
    res['error'] = float(np.sqrt(2 * 0.01 * 0.99 / (10 * n)))
    res['expected_if_fatras_decayed_kaons'] = 0.09
    with open(out, 'w') as fh:
        json.dump(res, fh, indent=1)
    log.info('proton - kaon reach %.4f (0.09 expected if kaons decayed)', dk)


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]))
