import sys, pathlib
S3 = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(S3 / 'scripts'))
import s3common as C
C.RES_ORIG = C.RES
out = pathlib.Path(__file__).parent / 'res'
import json
_load = json.load
# read inputs from real RES, write to sandbox
import fix_r2_bstar_context as F
class R:
    def __truediv__(self, n): return C.RES_ORIG / n
F.C.RES = R()
def dump(name, obj):
    p = out / name; json.dump(obj, open(p, 'w'), indent=1, default=C._default); return p
F.C.dump = dump
F.main()
