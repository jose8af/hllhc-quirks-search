# Scout note: orphaned / old ideas and cross-cutting gap statements

Cluster `orphaned_ideas`. Data: `scout_orphaned_ideas.json` (179 queries, 105 verified papers, 26 seeds). All paper IDs resolved through `inspire.py`; every gap quote was string-matched against the converted PDF text (`quote_verified_in_text` flag, all true). No numbers quoted from memory.

## Harvested 'gap' statements (verbatim, with locations)
- 1902.10229 (HL/HE-LHC addendum, CMS-FTR-18-018, PDF p.724): blind spot for lifetimes ~1 cm in H -> phi phi -> 4j; L1 track-trigger extension proposed. Echoed in 1902.00134 p.243.
- 2002.12220 (Les Houches 2019 BSM) p.70-71: blind spots across O(1 mm - 1 m) LLP decay lengths; displaced/delayed jet searches not targeted at small mass splittings. p.39/42: no search for mixed b nu t tau LQ final state or tau tau c.
- 1806.07396 (MATHUSLA physics case) p.163: no LHC search sensitive to dark Higgs-strahlung; p.39: no single displaced lepton-jet search.
- 2209.13128 (Snowmass BSM EF report) p.61: trigger is crucial for LLPs; p.30: some RPV scenarios significantly less constrained.
- 2203.09503 (Snowmass dark showers) p.12: dark-pion masses above a few GeV largely unconstrained.
- 1607.05641: CMS reports only combined OS+SS dilepton results (LNV/LNC split lost); 1308.3226/1302.4750 for tau-flavoured heavy leptons and UED MET searches designed for SUSY.
- LHC Reinterpretation Forum report 2003.07868 and HL-LHC WG3 report 1812.07831 were scanned (`--gaps`); WG3 repeats stau/low-mass-scalar 'unconstrained' statements (outside this cluster).

## Seeds (26)

| # | name | status guess | confidence |
|---|---|---|---|
| 1 | Quirk (infracolor string) signatures at ATLAS/CMS: timing, ionisation, stopped-quirk and out-of-time annihilation | proposed-not-searched | medium |
| 2 | Quirkonium annihilation to soft-unclustered pion showers: resonance plus low-pT track anomaly search | one-observable-not-another | medium |
| 3 | Dark Higgs-strahlung (h_D A') at the LHC | proposed-not-searched | medium |
| 4 | Lifetime ~1 cm blind spot for H -> phi phi -> 4j (L1 track trigger / displaced jets) | LHC-not-projected-to-HL | high |
| 5 | Freeze-out LLPs with small mass splitting: soft displaced visible decays | constrained-but-region-open | medium |
| 6 | Mixed leptoquark final state b nu t tau (S1 with DM mediator / balanced BRs) | one-observable-not-another | medium |
| 7 | Top-quark couplings to Z/H with right-handed tops: Z t_R t_R and h Z t_R t_R | indirectly-covered | low |
| 8 | Doubly-charged scalars decaying to tau, W W, or via H++ -> H+ W+ cascades | searched-limited-regime | medium |
| 9 | High-charge (/z/>7) and fractionally charged particles beyond Drell-Yan: HL-LHC acceptance and trigger limits | searched-limited-regime | medium |
| 10 | Lepton-flavour-violating Z decays with taus at HL-LHC (trigger-limited Z->e tau) | LHC-not-projected-to-HL | low |
| 11 | Heavy-neutrino LNV vs LNC charge-split and oscillation observables (pseudo-Dirac / quasi-Dirac N) in dilepton+jets | one-observable-not-another | medium |
| 12 | Tau-flavoured heavy leptons: type-III seesaw / heavy N coupled mainly to tau | constrained-but-region-open | low |
| 13 | Colour-octet scalars / sgluons: multi-top, same-sign and resonant-octet final states | indirectly-covered | low |
| 14 | Universal extra dimensions beyond MET: KK gluon / non-minimal UED / dilepton+MET at 13-14 TeV | indirectly-covered | medium |
| 15 | Stealth SUSY: complete natural model (left-handed stop/sbottom, higher-multiplicity) and HL reach | searched-limited-regime | medium |
| 16 | Neutral naturalness (Twin Higgs, Folded SUSY): top-partner pair production to glueball LLPs | constrained-but-region-open | medium |
| 17 | Pure-glue hidden valley glueball decays (v-glueballs) via heavy vector-like mediators | constrained-but-region-open | low |
| 18 | Dark showers with GeV-scale dark pions: unconstrained region for dark-pion masses above a few GeV | constrained-but-region-open | medium |
| 19 | Single displaced lepton-jet and lepton-jet+X topologies | one-observable-not-another | medium |
| 20 | Unparticle / mass-gapped conformal sector as hidden valley: continuum and broad-resonance signals | proposed-not-searched | low |
| 21 | Higgsless / fermiophobic heavy vectors: WZ/WW VBS resonances at HL-LHC | indirectly-covered | low |
| 22 | FCNC Higgs-top (t->cH, tcH) with extended scalar sectors beyond the SM Higgs: heavy-scalar t c phi final states | one-observable-not-another | low |
| 23 | Baryon-number-violating / Delta B=2 collider tests (n-nbar analogue) | constrained-but-region-open | low |
| 24 | R-hadrons: charge flipping, gluinonium and stopped R-hadrons at HL | searched-limited-regime | low |
| 25 | Vector-like confinement signals: onia and hidden-sector bound states with TeV vector-like quarks | proposed-not-searched | low |
| 26 | Hidden Higgs decaying to non-standard multi-particle final states (hidden Higgs; LEP-evasion reinterpreted at LHC) | searched-limited-regime | medium |

## Caveats
- 'No ATLAS/CMS search found' statements rest on INSPIRE title queries only and are marked UNVERIFIED in `notes`; check CDS/HEPData before promoting any seed.
- Several quotes are fragments from two-column PDF layout (flagged in notes). Unparticle, vector-like confinement, FCNC-with-heavy-scalar and BNV seeds lack a true gap sentence (low confidence, hypothesis only).
- Old orphan themes (fourth generation, Higgsless, leptophilic Higgs, pseudo-Dirac gauginos) largely returned either already-covered or no verifiable gap; INSPIRE boolean queries with `or`/parentheses silently returned nothing in many attempts.
- Shared scratch directory was concurrently written by other scouts; scratch helper files (not deliverables) may have been overwritten.
