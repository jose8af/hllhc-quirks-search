#!/usr/bin/env python3
"""Download an arXiv PDF, convert to text, optionally extract 'future work' style sentences.

Usage: arxiv_pdf.py <arxiv-id> [--gaps]
Saves research/cache/pdf/<id>.pdf and .txt (id with '/' replaced by '_'); prints the .txt path.
"""
import os, re, subprocess, sys, urllib.request

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cache", "pdf")
GAP = re.compile(
    r"(leave[s]? .{0,60}future|future work|it would be interesting|has not (yet )?been (studied|explored|investigated)"
    r"|deserves? (further|more)|dedicated search|poorly constrained|unconstrained|blind spot|overlooked|neglected"
    r"|not (yet )?(been )?(probed|searched)|worth (investigating|exploring)|beyond the scope)", re.I)


def get(aid):
    os.makedirs(CACHE, exist_ok=True)
    stem = aid.replace("/", "_")
    pdf, txt = os.path.join(CACHE, stem + ".pdf"), os.path.join(CACHE, stem + ".txt")
    if not os.path.exists(txt):
        if not os.path.exists(pdf):
            req = urllib.request.Request(f"https://arxiv.org/pdf/{aid}", headers={"User-Agent": "hllhc-search-research/0.1"})
            with urllib.request.urlopen(req, timeout=90) as r, open(pdf, "wb") as f:
                f.write(r.read())
        subprocess.run(["pdftotext", "-layout", pdf, txt], check=True)
    return txt


def gaps(txt):
    text = re.sub(r"\s+", " ", open(txt, errors="ignore").read())
    for s in re.split(r"(?<=[.!?]) ", text):
        if GAP.search(s) and len(s) < 600:
            print("-", s.strip())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    p = get(sys.argv[1])
    print(p)
    if "--gaps" in sys.argv:
        gaps(p)
