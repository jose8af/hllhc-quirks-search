"""stage5/acts_names.py -- Stage-4 ladder rung names (copy of acts.stage4.analysis.common.LADDER_NAMES, WP_RULE §3).

Kept as a literal so that make_figures runs without importing the frozen analysis package; check() compares it with
the frozen definition (read-only import, no bytecode written) and make_figures' --check-names calls it.
"""
import sys

LADDER_NAMES = ['R01_IP2>=4', 'R02_IP2>=5', 'R03_IP2>=6', 'R04_IP2>=7', 'R05_w<37.5', 'R06_w<18.75', 'R07_w<9.4',
                'R08_w<4.7', 'R09_p>1e-3', 'R10_p>0.01', 'R11_p>0.05', 'R12_2S2>=1', 'R13_2S2>=2', 'R14_2S2>=3',
                'R15_h>2', 'R16_h>3', 'R17_h>5', 'R18_o>2', 'R19_o>3', 'R20_o>5', 'R21_e>1.3', 'R22_e>1.6',
                'R23_e>2.0']


def check():
    sys.dont_write_bytecode = True
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from acts.stage4.analysis import common as C
    return list(C.LADDER_NAMES) == LADDER_NAMES


if __name__ == '__main__':
    ok = check()
    print('LADDER_NAMES match the frozen analysis package:', ok)
    raise SystemExit(0 if ok else 1)
