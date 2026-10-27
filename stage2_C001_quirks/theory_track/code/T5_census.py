#!/usr/bin/env python3
"""T5: INSPIRE census sweep for the quirk theory/pheno literature.
Purpose: run theory-side queries + citation queries, log hit counts, list records not in bibliography.json.
Run (from stage2_C001_quirks/):  python3 theory_track/code/T5_census.py
Outputs: theory_track/outputs/T5_census.json (all records + which queries hit), T5_queries.txt (log).
Uses research/tools/inspire.py (cached, rate-limited).
"""
import sys, json, os
sys.path.insert(0, '../research/tools')
import inspire
bib = json.load(open('literature/bibliography.json'))
known = {str(e['inspire_recid']) for e in bib}
Q = [
 't quirk*', 'abstracts.value:quirk*', 'abstracts.value:squirk*', 'abstracts.value:quirkonium', 'abstracts.value:infracolor*',
 'abstracts.value:"infracolour"', 'abstracts.value:"hidden valley" and abstracts.value:string',
 'abstracts.value:"hidden valley" and abstracts.value:confin*', 'abstracts.value:"folded supersymmetry" and abstracts.value:quirk*',
 'abstracts.value:"quirky little Higgs"', 'abstracts.value:"long string" and abstracts.value:collider',
 'abstracts.value:"macroscopic string" and abstracts.value:collider', 'abstracts.value:"flux tube" and abstracts.value:collider',
 'abstracts.value:"flux tube" and abstracts.value:"new physics"', 'abstracts.value:"hidden confining" and abstracts.value:electroweak',
 'abstracts.value:"dark glueball" and abstracts.value:quirk*', 'abstracts.value:glueball and abstracts.value:"heavy fermion" and abstracts.value:stable',
 'abstracts.value:"stable" and abstracts.value:"confining" and abstracts.value:"hidden sector" and abstracts.value:"LHC"',
 'abstracts.value:"vector-like confinement"', 'abstracts.value:"string tension" and abstracts.value:"heavy quark" and abstracts.value:"dark"',
 'abstracts.value:"dark QCD" and abstracts.value:"heavy quark"', 'abstracts.value:"dark pion" and abstracts.value:quirk*',
 'abstracts.value:"neutral naturalness" and abstracts.value:string', 'abstracts.value:"twin Higgs" and abstracts.value:"quirk*"',
 'abstracts.value:"heavy dark quark" and abstracts.value:confin*', 'abstracts.value:"Nambu-Goto" and abstracts.value:collider',
 'abstracts.value:"effective string" and abstracts.value:"LHC"', 'abstracts.value:"strongly interacting massive particles" and abstracts.value:string',
 'abstracts.value:"Lorentz" and abstracts.value:string and abstracts.value:"heavy particles" and abstracts.value:detector',
 'abstracts.value:monopole and abstracts.value:"Geant4" and abstracts.value:"magnetic field"',
 'abstracts.value:"exotic" and abstracts.value:"non-helical"', 'abstracts.value:"quirk*" and abstracts.value:"Sommerfeld"',
 'abstracts.value:"dark glueball" and abstracts.value:"Higgs"', 'abstracts.value:"mesoscopic" and abstracts.value:string and abstracts.value:LHC',
 'abstracts.value:"oscillating" and abstracts.value:"heavy" and abstracts.value:"infracolor"',
 'abstracts.value:"hypercolor" and abstracts.value:"string" and abstracts.value:LHC',
 'abstracts.value:"hidden sector" and abstracts.value:"confining" and abstracts.value:"track*" and abstracts.value:"anomalous"',
 'abstracts.value:"stable charged" and abstracts.value:"string" and abstracts.value:LHC',
 'abstracts.value:"dark photon" and abstracts.value:"quirk*"', 'abstracts.value:"electroweak" and abstracts.value:"quirk*" and abstracts.value:"W mass"',
]
cites = {'0805.4642':787371,'1708.02243':1614773,'1911.02223':1763305,'2002.07503':1781289,'1811.08903':1704655,
 '2108.06748':1905711,'2404.13814':2779435,'2512.20696':3095565,'2607.26195':3184325,'1106.2569':913637,
 '1703.00912':1516007,'2410.00269':2836006,'2509.08878':2968943,'1512.05782':1410596,'0805.4667':787381,
 '2504.02940':2908013,'2506.11192':3103830,'2311.15486':2726646,'1008.3547':865796,'0712.2681':770656,'0909.2034':830917,'0907.4932':827099}
recs = {}; log = []
def run(q, tag):
    try:
        out = inspire.search(q, 100, 'mostrecent')
    except SystemExit as e:
        log.append((tag, q, 'FAIL')); return
    log.append((tag, q, len(out)))
    for r in out:
        d = recs.setdefault(str(r['recid']), dict(r, hits=[]))
        d['hits'].append(tag)
for q in Q: run(q, 'Q')
for k, rid in cites.items(): run('refersto:recid:%d' % rid, 'cites:' + k)
os.makedirs('theory_track/outputs', exist_ok=True)
json.dump(recs, open('theory_track/outputs/T5_census.json', 'w'), indent=0)
with open('theory_track/outputs/T5_queries.txt', 'w') as f:
    for t, q, n in log: f.write('%s\t%s\t%s\n' % (t, q, n))
print(len(recs), 'records;', sum(1 for r in recs if r not in known), 'not in bibliography')
