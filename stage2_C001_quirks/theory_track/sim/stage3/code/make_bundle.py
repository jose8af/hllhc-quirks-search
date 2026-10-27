"""make_bundle.py -- Stage 3 (E7): assemble the self-contained Windows bundle and (optionally) write it to the USB stick.

  pixi run python sim/stage3/code/make_bundle.py stage            -> data/sim_stage3/bundle/quirks_sim/ (+ MANIFEST.json)
  pixi run python sim/stage3/code/make_bundle.py usb /Volumes/J8A/quirks_sim   -> copy the staged bundle to the USB
Contents: code/ (run_stage3.py, T3_causal_s3.py, s3_physics.py, surfaces_s3.json), inputs/ (all 22 event files + index),
jobs/ (pc.json, overlap.json, smoke.json, split_summary.json), RUN.md, PROMPT_FOR_CLAUDE.md, SETUP_WINDOWS.md (from
sim/stage3/bundle_src/), env/ (pixi.toml + pixi.lock taken unchanged from the USB).  FAT32-safe: plain files only,
no symlinks, short names, copies without extended attributes (shutil.copyfile); macOS '._*' files are removed after
the USB copy.  MANIFEST.json lists the md5 of every file.
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
S3 = HERE.parent
TT = S3.parents[1]
STAGE = TT / 'data' / 'sim_stage3' / 'bundle' / 'quirks_sim'
CODE_FILES = ['run_stage3.py', 'T3_causal_s3.py', 's3_physics.py', 'surfaces_s3.json']
JOB_FILES = ['pc.json', 'overlap.json', 'smoke.json', 'split_summary.json']
DOCS = ['RUN.md', 'PROMPT_FOR_CLAUDE.md', 'SETUP_WINDOWS.md']
USB_ENV = Path('/Volumes/J8A/quirks_sim/env')


def md5(p):
    return hashlib.md5(Path(p).read_bytes()).hexdigest()


def stage():
    if STAGE.exists():
        shutil.rmtree(STAGE)
    for d in ('code', 'inputs', 'jobs', 'env'):
        (STAGE / d).mkdir(parents=True)
    for f in CODE_FILES:
        shutil.copyfile(S3 / 'code' / f, STAGE / 'code' / f)
    for f in sorted((TT / 'data' / 'sim_stage3' / 'inputs').glob('*.npz')) + [TT / 'data' / 'sim_stage3' / 'inputs' / 'inputs_index.json']:
        shutil.copyfile(f, STAGE / 'inputs' / f.name)
    for f in JOB_FILES:
        shutil.copyfile(S3 / 'jobs' / f, STAGE / 'jobs' / f)
    for f in DOCS:
        shutil.copyfile(S3 / 'bundle_src' / f, STAGE / f)
    for f in ('pixi.toml', 'pixi.lock'):
        shutil.copyfile(USB_ENV / f, STAGE / 'env' / f)
    man = {str(p.relative_to(STAGE)).replace('\\', '/'): dict(md5=md5(p), bytes=p.stat().st_size)
           for p in sorted(STAGE.rglob('*')) if p.is_file()}
    json.dump(dict(created_by='make_bundle.py (E7)', files=man), open(STAGE / 'MANIFEST.json', 'w'), indent=1)
    big = max(v['bytes'] for v in man.values())
    print(f'staged {len(man)} files, {sum(v["bytes"] for v in man.values()) / 1e6:.1f} MB, largest {big / 1e6:.2f} MB -> {STAGE}')


def usb(dest):
    dest = Path(dest)
    man = json.load(open(STAGE / 'MANIFEST.json'))['files']
    for rel in list(man) + ['MANIFEST.json']:
        src = STAGE / rel; dst = dest / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if rel.startswith('env/') and dst.exists() and md5(dst) == md5(src):
            continue                       # leave the user's env files untouched when identical
        shutil.copyfile(src, dst)
    for p in list(dest.rglob('._*')) + list(dest.rglob('.DS_Store')):
        p.unlink()
    bad = [rel for rel in man if md5(dest / rel) != man[rel]['md5']]
    print(f'USB copy: {len(man)} files, {len(bad)} md5 mismatches', bad[:5])
    return not bad


if __name__ == '__main__':
    if sys.argv[1] == 'stage':
        stage()
    elif sys.argv[1] == 'usb':
        sys.exit(0 if usb(sys.argv[2]) else 1)
