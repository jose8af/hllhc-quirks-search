#!/usr/bin/env python3
"""Stdlib-only INSPIRE helper with rate limiting and on-disk cache (research/cache/).

Usage:
  inspire.py search "<inspire query>" [--size 25] [--sort mostcited|mostrecent]
  inspire.py get <recid|arxiv:ID>
  inspire.py refs <recid|arxiv:ID> [--size 50]       # papers this one cites
  inspire.py cites <recid|arxiv:ID> [--size 25] [--sort mostcited|mostrecent]  # papers citing it
Output: JSON lines, one compact record per paper.
"""
import argparse, hashlib, json, os, sys, time, urllib.parse, urllib.request

BASE = "https://inspirehep.net/api/literature"
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cache")
FIELDS = "control_number,titles,authors.full_name,arxiv_eprints,dois,citation_count,preprint_date,earliest_date,collaborations,inspire_categories,abstracts,publication_info"
_last = [0.0]


def fetch(url):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, hashlib.md5(url.encode()).hexdigest() + ".json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    for attempt in range(4):
        wait = 0.45 - (time.time() - _last[0])  # stay below 15 req / 5 s
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "hllhc-search-research/0.1"})
            with urllib.request.urlopen(req, timeout=40) as r:
                data = json.load(r)
            with open(path, "w") as f:
                json.dump(data, f)
            return data
        except Exception as e:  # 429 / transient
            time.sleep(2 * (attempt + 1))
            err = e
    raise SystemExit(f"fetch failed: {url}: {err}")


def compact(h, abstract=True):
    m = h["metadata"]
    auth = [a["full_name"] for a in m.get("authors", [])[:4]]
    n_auth = len(m.get("authors", []))
    rec = {
        "recid": m.get("control_number"),
        "title": (m.get("titles") or [{}])[0].get("title"),
        "authors": auth + (["et al. (%d)" % n_auth] if n_auth > 4 else []),
        "collab": [c.get("value") for c in m.get("collaborations", [])],
        "arxiv": (m.get("arxiv_eprints") or [{}])[0].get("value"),
        "doi": (m.get("dois") or [{}])[0].get("value"),
        "year": (m.get("preprint_date") or m.get("earliest_date") or "")[:4],
        "cites": m.get("citation_count"),
    }
    if abstract:
        rec["abstract"] = ((m.get("abstracts") or [{}])[0].get("value") or "")[:900]
    return rec


def resolve(ident):
    if ident.isdigit():
        return ident
    q = ident if ident.startswith("arxiv:") else "arxiv:" + ident
    d = fetch(f"{BASE}?q={urllib.parse.quote(q)}&size=1&fields=control_number")
    hits = d["hits"]["hits"]
    if not hits:
        raise SystemExit("not found: " + ident)
    return str(hits[0]["metadata"]["control_number"])


def search(q, size, sort, abstract=True):
    url = f"{BASE}?q={urllib.parse.quote(q)}&size={size}&sort={sort}&fields={FIELDS}"
    return [compact(h, abstract) for h in fetch(url)["hits"]["hits"]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["search", "get", "refs", "cites"])
    ap.add_argument("arg")
    ap.add_argument("--size", type=int, default=25)
    ap.add_argument("--sort", default="mostcited", choices=["mostcited", "mostrecent"])
    ap.add_argument("--no-abstract", action="store_true")
    a = ap.parse_args()
    ab = not a.no_abstract
    if a.cmd == "search":
        out = search(a.arg, a.size, a.sort, ab)
    elif a.cmd == "get":
        out = search("recid:" + resolve(a.arg), 1, "mostcited", ab)
    elif a.cmd == "cites":
        out = search("refersto:recid:" + resolve(a.arg), a.size, a.sort, ab)
    else:
        out = search("citedby:recid:" + resolve(a.arg), a.size, "mostcited", ab)
    for r in out:
        print(json.dumps(r, ensure_ascii=False))


if __name__ == "__main__":
    main()
