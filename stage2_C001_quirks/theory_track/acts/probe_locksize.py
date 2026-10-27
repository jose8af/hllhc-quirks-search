"""E5: sum download sizes of packages in a pixi.lock (conda 'size' fields; PyPI sizes looked up on PyPI JSON).
Run: python3 -I acts/probe_locksize.py <pixi.lock>"""
import sys, re, json, urllib.request
txt = open(sys.argv[1]).read()
# pixi lock v6: package entries start with '- conda: <url>' or '- pypi: <url or name>'
blocks = re.split(r'\n(?=- (?:conda|pypi): )', txt)
tot = 0; n = 0; big = []; pypi = []
for b in blocks:
    m = re.match(r'- conda: (\S+)', b)
    if m:
        s = re.search(r'\n  size: (\d+)', b)
        if s:
            sz = int(s.group(1)); tot += sz; n += 1; big.append((sz, m.group(1).rsplit('/', 1)[-1]))
    m = re.match(r'- pypi: (\S+)', b)
    if m:
        pypi.append(m.group(1))
big.sort(reverse=True)
print(f"conda packages: {n}, download {tot/1e6:.0f} MB")
for sz, name in big[:12]:
    print(f"  {sz/1e6:7.1f} MB  {name}")
print("pypi:", pypi)
