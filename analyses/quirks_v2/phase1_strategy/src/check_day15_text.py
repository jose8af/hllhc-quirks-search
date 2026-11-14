#!/usr/bin/env python3
"""Text check of the day-15 family (verdict cycle 8, §4.2). Standard library only.
usage: python3 -I check_day15_text.py STRATEGY.md budget_stdout.txt
Reads the day-15 table and the (c) grid printed by script [9b] (the "v9 (W1)" lines) and checks the strategy against them:
(A) the fenced blocks that quote the table are identical to the printed lines; (B) every required statement is present with the
printed value; (C) every statement of the family found by a regular expression carries a printed value; (D) no stale value is left.
Lines of §13 (history) and lines inside code fences are not scanned in (C) and (D). Prints one line per check and a summary."""
import re
import sys

strategy, stdout = sys.argv[1], sys.argv[2]
out = open(stdout, encoding="utf-8").read().split("\n")
src = open(strategy, encoding="utf-8").read().split("\n")
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
res = []


def rec(ok, what, info=""):
    res.append(ok)
    print(("OK       " if ok else "MISMATCH ") + what + (" :: " + info if info else ""))


def sci(v, nd=1):
    e = len(str(int(v))) - 1
    m = f"{v / 10 ** e:.{nd}f}"
    if float(m) >= 10:
        m, e = f"{float(m) / 10:.{nd}f}", e + 1
    return m, str(e).translate(SUP)


# ---- the printed table -----------------------------------------------------------------------------------------------------
i0 = next(i for i, l in enumerate(out) if l.startswith("  v9 (W1): day-15 reading"))
i1 = next(i for i, l in enumerate(out) if l.startswith("  |   without an S_CKF estimate"))
tab = out[i0:i1 + 1]
row = lambda key: next(l for l in tab if key in l)
cells = lambda l: [c.strip() for c in l.strip().strip("|").split("|")]
nums = lambda s: [float(x) for x in re.findall(r"\d+(?:\.\d+)?(?:e[+-]\d+)?", s)]
T = {}
c = cells(row("every pilot count zero"))
T["empty"] = [int(x) for x in re.findall(r"\d+", c[1].replace("16-84", ""))]
for key, name in (("Z(nunu) pilot count m_Z, DIF", "mz"), ("DIF pilot count m_D, Z(nunu)", "md")):
    c = cells(row(key))
    T[name] = list(zip([int(x) for x in c[0].split("=")[1].split("/")], [int(x) for x in c[1].split("/")], [x.strip() for x in c[2].split("/")]))
for key, name in (("(alpha1), no credit", "a1"), ("(alpha1'), no credit", "a1p")):
    T[name] = nums(cells(row(key))[1])                      # lo-hi at 0.8, lo-hi at 0.98
T["credit"] = [int(x) for x in cells(row("with fit-probability credit 2/35"))[1].split("/")]
T["grid"], T["base"] = {}, {}
for l in tab:
    m = re.match(r"\s*\|\s+f_D = (\S+)", l)
    if m:
        c = cells(l)
        T["base"][m.group(1)] = [int(x) for x in re.findall(r"\d+", c[1].replace("B50", ""))]
        for part in c[2].split(";"):
            rate, vals = part.rsplit(":", 1)
            T["grid"][(m.group(1), rate.strip()[:5])] = [None if "none" in v else (int(re.search(r"x(\d+)", v).group(1)), re.search(r"\((\d+\.\d)%\)", v).group(1)) for v in vals.split(" / ")]
T["own"] = [int(x) for x in re.findall(r"x(\d+)", row("without an S_CKF estimate"))]
zl = [m for m, b, k in T["mz"] if k == "at the limit"] or [max(m for m, b, k in T["mz"] if k == "below")]
zb, za = max(m for m, b, k in T["mz"] if k == "below"), min(m for m, b, k in T["mz"] if k == "above")
db, da = max(m for m, b, k in T["md"] if k == "below"), min(m for m, b, k in T["md"] if k == "above")
B = {m: b for m, b, k in T["mz"]}
BD = {m: b for m, b, k in T["md"]}
g = T["grid"]
st = next(l for l in out if l.strip().startswith("v9 self-test:"))
rec("ALL PASS" in st, "script self-test line", st.strip())

# ---- (A) verbatim blocks ---------------------------------------------------------------------------------------------------
fen, inside, body = [], False, [False] * len(src)
for i, l in enumerate(src):
    s = l[2:] if l.startswith("> ") else l
    if s.strip() == "```":
        inside = not inside
        body[i] = True
        continue
    body[i] = inside
    if inside:
        fen.append(s)
quoted = [l for l in fen if l in tab or l.startswith("  v") or l.startswith("  |") or l.startswith("  basis") or l.startswith("  (the v6")]
rec(quoted == tab, "(A) fenced blocks equal the printed table, line for line", f"{len(quoted)} quoted lines, {len(tab)} printed")

# ---- text to scan: outside the fences and outside §13 -----------------------------------------------------------------------
h0 = next((i for i, l in enumerate(src) if l.startswith("## 13.")), len(src))
h1 = next((i for i, l in enumerate(src) if i > h0 and l.startswith("## ")), len(src))
live = [(i, l) for i, l in enumerate(src) if not body[i] and not (h0 <= i < h1)]
text = "\n".join(l for _, l in live)
lineof = lambda pos: live[text.count("\n", 0, pos)][0] + 1
norm = re.sub(r"\s+", " ", text.replace("\n> ", "\n"))

# ---- (B) required statements, built from the printed values ----------------------------------------------------------------
a1p, a1 = T["a1p"], T["a1"]
h_lo, h_hi = sci(a1p[0], 0), sci(a1p[3], 0)
req = [
    ("§0 pause, §0 leading sentence, rider: expected reading", f"≈ {h_lo[0]}×10{h_lo[1]}–{h_hi[0]}×10{h_hi[1]}", 3),
    ("§0 pause: (alpha1) reading", f"≈ {sci(a1[0])[0]}×10{sci(a1[0])[1]}–{sci(a1[3])[0]}×10{sci(a1[3])[1]}", 2),
    ("§0 pause: empty reading", f"B₅₀ ≈ {T['empty'][0]} with every pilot count at zero", 1),
    ("§0, §4.4 (three places), §11.7: Z(nunu) limit", f"≈ {zl[0]} Z(νν) pilot counts", 5),
    ("§0, §11.7: DIF limit", f"between {db} and {da} decays-in-flight pilot counts", 2),
    ("Q2 digest: (alpha1') row", f"≈ {sci(a1p[0])[0]}–{sci(a1p[1])[0]}×10{sci(a1p[0])[1]} (ε_pair 0.8) to {sci(a1p[2])[0]}–{sci(a1p[3])[0]}×10{sci(a1p[2])[1]} (0.98)", 1),
    ("Q2 digest: Z(nunu) row", f"{B[zb]} at {zb}, {B[zl[0]]} at {zl[0]}, {B[za]} at {za} | below up to {zb}, at the limit at {zl[0]}, above from {za}", 1),
    ("Q2 digest: DIF row", f"{BD[db]} at {db}, {BD[da]} at {da} | below up to {db}, above from {da}", 1),
    ("Q2 digest: empty row", f"{T['empty'][0]} (16–84 %: {T['empty'][1]}–{T['empty'][2]}) | below", 1),
    ("Q2 digest: (c) credit row", f"| {T['credit'][0]}–{T['credit'][1]} | below", 1),
    ("Q2 (c): credit route", f"B₅₀ {T['credit'][0]}–{T['credit'][1]}) acts on both", 1),
    ("Q2 (c): conversions removed at the central size", f"B₅₀ is {T['base']['1'][0]}–{T['base']['1'][1]}", 1),
    ("Q2 (c): bar at f_D = 0", f"at least ×{g[('0', '0.379')][0][0]} ({g[('0', '0.379')][0][1]} %) [×{g[('0', '0.255')][0][0]}]", 1),
    ("Q2 (c): bar at f_D = 1/4", f"×{g[('1/4', '0.379')][0][0]}–{g[('1/4', '0.379')][1][0]} ({g[('1/4', '0.379')][0][1]}–{g[('1/4', '0.379')][1][1]} %) [×{g[('1/4', '0.255')][0][0]}–{g[('1/4', '0.255')][1][0]}]", 1),
    ("Q2 (c): bar at f_D = e^-1", (f"×{g[('e^-1', '0.379')][0][0]} ({g[('e^-1', '0.379')][0][1]} %) [×{g[('e^-1', '0.255')][0][0]}] at ×e⁻¹ with the pile-up fall ×339; at ×e⁻¹ with the fall ×201 none suffices"
                                   if g[("e^-1", "0.379")][1] is None and g[("e^-1", "0.379")][0] is not None else "<the e^-1 row changed its pattern: rewrite the sentence from the printed row>"), 1),
    ("Q2 (c): without S_CKF", f"×{T['own'][0]}–{T['own'][1]:,}", 1),
]
for what, frag, n in req:
    k = norm.count(frag)
    rec(k == n, f"(B) {what}", f"'{frag}' found {k}, expected {n}")

# ---- (C) scanners: every statement of the family must carry a printed value ----------------------------------------------
gridset = {v[0] for vs in g.values() for v in vs if v} | set(T["own"])
pct = {v[0]: v[1] for vs in g.values() for v in vs if v}
okc = {str(zl[0]), str(db), str(da)}
scan = [
    ("pilot-count limits", r"(?<![\w.,–-])(\d+(?:\.\d+)?)\s+(?:Z\(νν\)\s+|decays-in-flight\s+)?pilot\s+(?:ceiling\s+)?(?:counts|events)\b", lambda m: m.group(1) in okc),
    ("rejection factor with its percentage", r"×(\d[\d,]*)(?:–(\d[\d,]*))?\s+\((\d+\.\d)(?:–(\d+\.\d))?\s?%\)",
     lambda m: all(int(x.replace(",", "")) in gridset for x in m.group(1, 2) if x) and pct.get(int(m.group(1).replace(",", ""))) == m.group(3)
     and (m.group(4) is None or pct.get(int(m.group(2).replace(",", ""))) == m.group(4))),
    ("rejection factor in brackets", r"\[×(\d[\d,]*)(?:–(\d[\d,]*))?\]", lambda m: all(int(x.replace(",", "")) in gridset for x in m.group(1, 2) if x)),
    ("'at least xN' / 'xN-M' rejection statements in Q2 (c)", r"(?:at least|factor is)\s+×(\d[\d,]*)(?:–(\d[\d,]*))?", lambda m: all(int(x.replace(",", "")) in gridset for x in m.group(1, 2) if x)),
    ("day-15 reading in powers of ten", r"(?:reading is expected at|expected reading is B₅₀|projected B₅₀)\s+≈\s+(\S+)",
     lambda m: m.group(1).rstrip(".,;)") in {f"{h_lo[0]}×10{h_lo[1]}–{h_hi[0]}×10{h_hi[1]}"}),
]
for what, rx, good in scan:
    hits = list(re.finditer(rx, text))
    bad = [(lineof(m.start()), m.group(0).replace("\n", " ")) for m in hits if not good(m)]
    rec(not bad and len(hits) > 0, f"(C) {what}: {len(hits)} statements", "; ".join(f"l.{a}: '{b}'" for a, b in bad) if bad else "")
q0 = next(i for i, l in live if l.startswith("**Q2,"))
q1 = next(i for i, l in live if l.startswith("**Q3,"))
p0 = next(i for i, l in live if "**The pause.**" in l)
p1 = next(i for i, l in live if "**Leading sentence**" in l)
okr = {(T["credit"][0], T["credit"][1]), (T["base"]["1"][0], T["base"]["1"][1])}
hits = [(i + 1, m) for i, l in live if (q0 <= i < q1 or p0 <= i < p1) for m in re.finditer(r"B₅₀\s+(?:is\s+|≈\s+)?(\d[\d,]*)–(\d[\d,]*)(?![\d×]|\.\d)", l)]
bad = [(i, m.group(0)) for i, m in hits if (int(m.group(1).replace(",", "")), int(m.group(2).replace(",", ""))) not in okr]
rec(not bad and len(hits) > 0, f"(C) B₅₀ ranges in 'The pause' and in Q2: {len(hits)} statements", "; ".join(f"l.{a}: '{b}'" for a, b in bad))

# ---- (D) stale values of earlier versions ------------------------------------------------------------------------------
stale = [r"v8 table", r"budget_stdout_v8", r"≈ 20\s+(?:Z\(νν\)\s+)?(?:pilot|counts in the pilot|in the pilot|ceiling)", r"≈ 13\s+in the pilot", r"pool-equivalent", r"pilot ceiling",
         r"5(?:\.0)?×10⁴–5(?:\.1)?×10⁵", r"5\.0–5\.1×10[⁴⁵]", r"2\.8×10³–4\.8×10⁴", r"401–663", r"B₅₀ 51–74", r"×34\b", r"×23\]", r"×52–81", r"×69–235", r"×35–55", r"×47–159",
         r"U1 line", r"read as rule 1 reads them", r"would suffice", r"×31\b"]
for rx in stale:
    hits = [lineof(m.start()) for m in re.finditer(rx, text)]
    rec(not hits, f"(D) no '{rx}'", "lines " + ", ".join(map(str, hits)) if hits else "")
print(f"text check: {'ALL OK' if all(res) else 'MISMATCH'} ({sum(res)} of {len(res)})")
