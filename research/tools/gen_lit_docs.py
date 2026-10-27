#!/usr/bin/env python3
"""Generate literature/seminal_papers.md and literature/citation_graph.md from papers.json + merged_candidates.json."""
import json, collections, re
P = json.load(open('literature/papers.json'))
M = json.load(open('candidates/merged_candidates.json'))
V = json.load(open('candidates/gate2_verdicts.json'))
A = json.load(open('candidates/gate3_adversarial.json'))
CL = {'alp_light':'ALPs & light states','composite_heavy':'Compositeness & heavy states','dark_sectors':'Dark sectors & portals',
      'eft_ew':'EFT & EW precision','higgs_scalars':'Exotic Higgs & scalars','leptoquark_flavour':'Leptoquarks & flavour',
      'llp':'Long-lived particles','orphaned_ideas':'Older / orphaned ideas','qcd_substructure':'QCD, substructure, quantum information','susy':'SUSY corners'}
def cl(p):
    c=p['clusters'][0]; c=c.replace('scout_','')
    for k in CL:
        if k in c or c.startswith(k[:6]): return CL[k]
    return c
def pid(p): return p.get('arxiv') or f"INSPIRE:{p.get('recid')}"
def fmt(p):
    a=', '.join(p.get('authors',[])[:2]) if p.get('authors') else ''
    return f"- **{pid(p)}** ({p.get('year')}, {p.get('cites')} cites) {p.get('title')} — {a}"
S=[p for p in P if p.get('role')=='seminal']
rev=[p for p in P if p.get('role')=='review']
L=["# Seminal papers found\n",
 f"Source: `papers.json` ({len(P)} unique papers; {len(S)} tagged *seminal* and {len(rev)} *review* by the scouts). Tags are scout judgements (sonnet), not a verified ranking; IDs and citation counts come from INSPIRE records at harvest time (Oct 2026). Papers cited by several scouts have been merged.\n",
 "How to read: *seminal* = introduced or crystallised an idea that later phenomenology/searches build on. Broad foundational reviews are listed separately in the last section because they are not 'overlooked idea' seeds.\n"]
bycl=collections.defaultdict(list)
for p in S: bycl[cl(p)].append(p)
for c in sorted(bycl):
    L.append(f"\n## {c} ({len(bycl[c])})\n")
    for p in sorted(bycl[c], key=lambda p:-(p.get('cites') or 0))[:25]: L.append(fmt(p))
L.append("\n## Foundational reviews (top 30 by citations)\n")
for p in sorted(rev,key=lambda p:-(p.get('cites') or 0))[:30]: L.append(fmt(p))
L.append("\n## Idea lineages anchored by these papers (the 'latent research program' pattern)\n")
L.append("""- **Hidden valleys** — Strassler & Zurek hep-ph/0604261 (2006) → emerging jets 1502.05409 → dark-shower benchmarks 2103.01238 → SUEP 1612.00850 → semi-visible jets; searches by CMS/ATLAS cover prompt and part of the displaced regimes (see C003, C005, C008).
- **Quirks** — Kang & Luty 0805.4642 (2008) → collider quirk phenomenology 1106.2569 → coplanar-track method 1708.02243 → no central ATLAS/CMS search found; FASER searched (2607.26195) (see C001).
- **Doubly charged Higgs / type-II seesaw** — INSPIRE:214561 (1985) → H++ production & decay hep-ph/0506176 → displaced H++ 1808.00943 → ATLAS prompt/WW/multi-charged searches; displaced same-sign regime not reinterpreted (see C019).
""")
open('literature/seminal_papers.md','w').write('\n'.join(L)+'\n')

# ---- citation graph (lineage by curation from scout seeds + reviews)
ids={}
for p in P:
    if p.get('arxiv'): ids[p['arxiv']]=p
def norm(i): return re.sub(r'^(arXiv:|arxiv:)','',str(i or '')).strip()
def label(i):
    p=ids.get(norm(i)); return f"{norm(i)} ({p.get('year')})" if p else norm(i)
G=["# Research-lineage graph\n",
"Edges are curated lineage (seminal → development → pheno prediction → experimental result), assembled from the scouts' `seminal_refs`, `followup_refs` and `exp_coverage_seen`, then corrected by the Gate 2/3/4 reviews. It is **not** an exhaustive citation network; full-network traversal was done per seed with INSPIRE `refersto`/`citedby:recid` queries (logged in each `scout_*.json`).\n",
"The status at the end of each chain is the gate result: Gate 2 verdict (P/H/R) and Gate 3 adversarial verdict where available.\n"]
mer=[]
for c in M:
    k=c['cand_id']; sem=[];fol=[];exp=[]
    for s in c['seeds']:
        sem+= [norm(r.get('id')) for r in s.get('seminal_refs',[]) if r.get('id')]
        fol+= [norm(r.get('id')) for r in s.get('followup_refs',[]) if r.get('id')]
        exp+= [norm(r.get('id')) for r in s.get('exp_coverage_seen',[]) if r.get('id')]
    uniq=lambda x:list(dict.fromkeys(x))
    sem,fol,exp=uniq(sem)[:6],uniq(fol)[:8],uniq(exp)[:6]
    v=V[k]['verdict']; a3=A.get(k,{}).get('verdict','—'); a3=a3.split(' ')[0]
    G.append(f"\n## {k} {c['name']}\n- Status: Gate2 **{v}**; Gate3 **{a3}**; found by {c['n_independent_scouts']} scout(s)\n- Foundational: {', '.join(label(i) for i in sem) or '—'}\n- Development/pheno: {', '.join(label(i) for i in fol) or '—'}\n- Experimental coverage seen: {', '.join(label(i) for i in exp) or '—'}")
    gap=V[k].get('specific_gap_statement') or V[k].get('reason') or ''
    G.append(f"- Gate-2 gap statement: {gap[:300]}")
    mer.append((k,sem,fol,exp,v))
# mermaid for the 10 reviewed
top=['C001','C005','C019','C044','C015','C051','C003','C008','C040','C066']
G.append("\n## Mermaid overview (reviewed candidates)\n\n```mermaid\nflowchart LR")
for k,sem,fol,exp,v in mer:
    if k not in top: continue
    nm=[c['name'] for c in M if c['cand_id']==k][0][:40].replace('"','')
    G.append(f'  {k}["{k} {nm}"]')
    for i,s in enumerate(sem[:2]): G.append(f'  s{k}{i}["{label(s)}"] --> {k}')
    for i,e in enumerate(exp[:2]): G.append(f'  {k} --> e{k}{i}["{label(e)}"]')
G.append("```\n")
open('literature/citation_graph.md','w').write('\n'.join(G)+'\n')
print(len(S),len(rev),len(G))
