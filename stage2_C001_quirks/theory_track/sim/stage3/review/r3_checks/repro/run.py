import sys, os, pathlib, runpy
H = pathlib.Path(__file__).resolve().parent
os.environ['NUMBA_CACHE_DIR'] = str(H / 'numba')
S3 = H.parents[2]
sys.path.insert(0, str(S3 / 'scripts'))
import s3common as C
C.RES = H / 'results'; C.FIG = H / 'figures'
sys.argv = [sys.argv[1]]
runpy.run_path(str(S3 / 'scripts' / sys.argv[0]), run_name='__main__')
