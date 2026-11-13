"""lock_diff.py -- compare package versions between the osx-arm64 and linux-64 solves of a pixi.lock (feasibility A).

Usage (stdlib only):  python3 -I lock_diff.py <pixi.lock> [<v1 pixi.lock>]
Prints, per environment, every package whose version differs between osx-arm64 and linux-64 (or exists on one only).
With a second (v1, osx-arm64-only) lock, also checks that the osx-arm64 versions of the new lock equal the v1 ones.
Parsing: lock v6 lines '- conda: <url>' / '- pypi: <url>' under environments.<env>.packages.<platform>.
"""
import json
import re
import sys
from pathlib import Path

CONDA = re.compile(r'/([^/]+?)-([^-/]+)-([^-/]+)\.(?:conda|tar\.bz2)$')
WHEEL = re.compile(r'/([^/]+?)-([0-9][^-/]*)(?:-[^/]*)?\.(?:whl|tar\.gz|zip)$')


def parse(path):
    envs = {}
    env = plat = None
    in_envs = False
    for line in Path(path).read_text().splitlines():
        if line.startswith('environments:'):
            in_envs = True
            continue
        if in_envs and line and not line.startswith(' '):
            break
        m = re.match(r'^  (\S+):$', line)
        if in_envs and m:
            env = m.group(1)
            continue
        m = re.match(r'^      (\S+):$', line)
        if in_envs and m:
            plat = m.group(1)
            # lock v7 names platforms with their virtual packages, e.g. linux-64-glibc-2-34, osx-arm64-macos-26-0
            for base in ('osx-arm64', 'linux-64'):
                if plat.startswith(base):
                    plat = base
            continue
        m = re.match(r'^\s+- (conda|pypi): (\S+)$', line)
        if in_envs and m and env and plat:
            kind, url = m.groups()
            mm = (CONDA if kind == 'conda' else WHEEL).search(url)
            if mm:
                name = mm.group(1).lower().replace('_', '-')
                envs.setdefault(env, {}).setdefault(plat, {})[f'{kind}:{name}'] = mm.group(2)
    return envs


def main():
    new = parse(sys.argv[1])
    out = {}
    for env, plats in new.items():
        a, b = plats.get('osx-arm64', {}), plats.get('linux-64', {})
        diff = {k: [a.get(k), b.get(k)] for k in sorted(set(a) | set(b)) if a.get(k) != b.get(k)}
        out[env] = dict(n_osx=len(a), n_linux=len(b), differ=diff)
    if len(sys.argv) > 2:
        old = parse(sys.argv[2])
        for env, plats in old.items():
            o = plats.get('osx-arm64', {})
            n = new.get(env, {}).get('osx-arm64', {})
            out.setdefault(env, {})['osx_changed_vs_v1'] = {k: [o.get(k), n.get(k)] for k in sorted(set(o) | set(n))
                                                            if o.get(k) != n.get(k)}
    json.dump(out, sys.stdout, indent=1)
    sys.stdout.write('\n')


if __name__ == '__main__':
    main()
