# Literature review: how the HL-LHC idea search developed, and what it found

Date: 2026-10-06. Author: Gate 5 arbiter. Sources: `LOG.md`, `literature/scout_*.md`, `candidates/*.json`, and `reviews/{triage,adversarial,experimental,feasibility,theory}/`. All reference IDs are resolved in `citation_audit.json`.

## 1. Shape of the search

Ten scouts searched ten topic clusters:
- leptoquarks/flavour;
- dark sectors;
- SUSY;
- long-lived particles (LLPs);
- Higgs/scalars;
- EW/EFT;
- composite/heavy states;
- ALPs/light states;
- QCD/substructure;
- "orphaned" older ideas.

The scouts produced 199 seeds and 986 unique papers. These merged into 74 directions. By cluster label (some directions carry more than one) the counts were: orphaned ideas 23, LLP 16, dark sectors 14, Higgs/scalars 12, QCD/substructure 12, composite 11, SUSY 11, ALP 9, LQ/flavour 9, EW/EFT 6.

The candidates then passed through four gates:

| Gate | Reviewer | Input | Outcome |
|---|---|---|---|
| Gate 2 triage | sonnet | 74 directions | 27 PASS, 37 HOLD, 10 REJECT |
| Gate 3 adversarial | opus, one pass | the 27 PASS | 26 NARROWED, 1 DIES, 0 intact |
| Gate 4 | separate experimental, feasibility and theory reviewers (opus) | 10 survivors | full reviews |
| Gate 5 | arbiter | the 10 Gate 4 candidates | this report |

## 2. Intellectual development by cluster

**Dark showers and confining hidden sectors (C005, C003, C008, C001).**

The hidden-valley programme (hep-ph/0604261) has split into experimental sub-programmes, each with active CMS/ATLAS searches:
- emerging jets (1502.05409; CMS 2403.01556, ATLAS 2505.02429/2510.12347);
- semi-visible jets (1503.00009; CMS 2112.11125, 2608.05323);
- SUEP (1612.00850; CMS 2403.05311, 2604.05996, 2607.09621, ATLAS 2605.20015);
- Higgs-portal dark showers (CMS 2402.01898, 2511.11888).

The lesson is that the "dark QCD is unexplored" framing of 2021-22 is out of date. What remains are lifetime and kinematic corners:
- tracker-length lifetimes for Higgs-portal showers (C005);
- displaced isotropic SUEP (C003);
- photon-rich SVJs (C008).

Lifetime naturalness bounds (2103.01238) and hadronisation uncertainty (2203.09503, 2505.03058) shape which corners are physically motivated.

Quirks (0805.4642) are the exception. The only LHC-experiment search is FASER's (2607.26195). The ATLAS/CMS central-detector programme proposed in 1708.02243 has never been carried out.

**Extended scalars and neutrino-mass models (C019).**

Prompt H++ searches are mature (ATLAS 2211.07505, 2101.11961). The phenomenology has moved to non-prompt regimes:
- displaced H++ (1808.00943, 2608.27251);
- GM long-lived H5++ (2410.19561);
- compressed spectra (2305.06889, 2603.15882).

Experiments have not followed into these regimes. The surviving question is whether existing displaced-lepton searches without a charge requirement (CMS 2110.04809) already cover them.

**Composite Higgs and top partners (C044).**

The roadmap (2203.13753) and charge-5/3 papers (1907.05894) called for exotic-decay searches. Both ATLAS (2607.28381) and CMS (2610.03489) then searched the diphoton route in 2026. The recasting atlas (2609.00127) shows that the six-top route is bounded by recasts to 1.65 TeV. The field has moved from "unsearched exotic decays" to "optimising residual channels".

**Flavourful ALPs (C015).**

The idea of using top decays to produce long-lived ALPs came from 2202.09371. ATLAS took it up quickly (2403.15332), but only for m_a = 40-55 GeV in the inner detector. What remains is an interpretation exercise: adding the top-decay signal to existing lepton-triggered LLP searches.

**Leptoquarks (C066).**

The lepton-PDF idea (2005.06475, 2005.06477) became ATLAS (2507.03650) and CMS (2608.28377) searches within about five years. The third-generation and B-anomaly sub-ideas were all overtaken:
- ATLAS 2503.19836 excluded the CMS b-tau excess benchmark.
- beta_R benchmarks were covered in CMS 2208.02717.

**EW precision / EFT (C051).**

Drell-Yan angular coefficients are mature at the Z peak (ATLAS 1606.00689, CMS 2604.25678). High-mass A_FB is already measured (CMS 2202.12327). The remaining dimension-8 and l=3 null tests (2511.19617, 2003.11615) are measurement opportunities with modest BSM leverage.

**SUSY (C040).**

Compressed stau searches restarted in 2026 (ATLAS 2609.37215). The g-2 motivation disappeared after the 2025 Theory Initiative update (2505.21476). What remains is a dark-matter-motivated window and a missing HL-LHC projection.

## 3. Headline gaps that were overturned, and what overturned them

| Scout/triage headline | Overturned by | Stage |
|---|---|---|
| ~1 cm lifetime blind spot in H -> phi phi -> 4j (C028) | CMS 2409.10806 covers c*tau ~1.3-380 mm | Gate 2 |
| RPV LSP at intermediate lifetimes unsearched (C035) | ATLAS 2603.15007 variable-coupling reinterpretation; CMS 2402.15804 | Gate 2 |
| Mixed b nu t tau LQ unsearched (C067) | CMS 2012.04178 names this exact signature | Gate 2 |
| Charm/strange LQ (C070) | ATLAS 2006.05872 (c-tag pair), 2410.17824 | Gate 2 |
| MTD/HGTD 4D vertexing unexploited for LLPs (C026, a scout favourite) | The CMS MTD TDR (INSPIRE:1819664) already contains delayed-photon, H -> XX timing and HSCP-velocity studies; ATLAS 2502.06694 uses ToF | Gate 3 (DIES) |
| Dark pions "largely unconstrained" above a few GeV (C005) | CMS 2402.01898 Higgs-portal dark-shower limits; the Snowmass quote was about flavour bounds | Gate 3 / Gate 4 theory |
| No top-tagged long-lived ALP search (C015) | ATLAS 2403.15332 | Gate 3 |
| DY angular coefficients only at the Z peak (C051) | CMS 2202.12327 (A_FB and A0 above 170 GeV) | Gate 3 |
| VLQ -> t S unsearched (C044) | ATLAS 2607.28381; CMS 2610.03489; CMS-PAS-B2G-24-005 | Gate 3 |
| CMS 2.8 sigma b-tau LQ excess worth an HL follow-up (C066) | ATLAS 2503.19836 excludes the benchmark | Gate 3 |
| Lepton/tau-enriched SVJ unsearched (C008) | CMS 2608.05323; INSPIRE:3136606 | Gate 3 |
| Prompt SUEP and W/Z-associated SUEP gaps (C003) | CMS 2604.05996, 2607.09621; ATLAS 2605.20015 | Gate 3 |
| g-2-motivated light sleptons (C040) | Physics premise removed (2505.21476); CMS 2402.01888, 2508.13900 | Gate 3 |
| Photon-ISR SVJ benchmark (C008) | Excluded through visible Z' -> qq by ATLAS 2403.08547 | Gate 4 theory |
| "HL reach 5.7 (4.2) TeV" for lepton-quark LQ (C066) | Misreading of 2005.06475: it is a crossover with the Q_W bound | Gate 4 (all three reviewers) |

**Pattern.** The scouts' gap claims came mostly from "future work" sentences in theory papers that were 2-6 years old. In most cases a CMS or ATLAS result had appeared in the meantime, often in 2024-2026, sometimes under different terminology. Gap statements written in reviews and Snowmass reports went stale fastest.

## 4. Main negative results

- **Well covered after extensive search:**
  - prompt SUEP;
  - lepton/tau-enriched and t-channel SVJs;
  - prompt H++;
  - diphoton exotic VLQ decays;
  - third-generation and b-tau leptoquarks;
  - Higgs -> long-lived ALPs;
  - inelastic DM / compressed soft displaced tracks;
  - R-hadrons;
  - unparticles;
  - timing-detector LLP benchmarks.
- **No candidate is a novel-theory or novel-phenomenology opportunity.** Every surviving item already has a published phenomenology proposal. Several also have published HL-LHC pheno projections: 2512.24814, 1708.02243, 2608.27251, 2202.09371, 2302.10782, 2403.18991, 2005.06475.
- **Three of the ten Gate 4 survivors reduce to a recast, reinterpretation or projection:** C015, C040 and C066. A fourth, C044, reduces to optimising a strategy that recasts already bound.

## 5. Limitations and caveats of this process

1. **Coverage searches were INSPIRE title/abstract-level.** Full text was read only selectively (e.g. 2202.12327, 2403.15332, 2609.00127, 2607.26195).
   - CMS/ATLAS internal analyses, CDS-only notes and public-results pages were checked sparsely. WebFetch was lossy, and HEPData was blocked for at least one reviewer (Cloudflare).
   - "Not found" is never "absent". Two specific pre-emption risks were seen but not verifiable: an ATLAS "Quirks" Confluence page title (C001) and the ATLAS Higgs-portal dark-jet prospect (C005).
2. **Gate 2 triage used sonnet with abstract-level evidence.** 24 HOLD items were parked without strong-model review, so good ideas may hide among them (e.g. C042 Dirac gauginos/sgluons, C074 vector-like confinement onia, C036 baryon-number violation).
3. **Lean budget.**
   - Gate 3 ran a single adversarial pass on the 27 PASS items only.
   - Gate 4 ran one reviewer per role and no second adversarial round.
   - No lineage agent was run: `literature/lineage/` is empty. The lineage graphs in TOP_CANDIDATES.md were assembled by the arbiter from the review files.
   - Alternates C017, C061, C009, C047 and C048 were never reviewed at Gate 4.
4. **Numbers.** Many yields and reaches in the reviews are reviewer ESTIMATEs, made from published cross sections with assumed efficiencies. Pheno projections being leaned on (2512.24814, 2608.27251, 2202.09371, 2511.19617, 1812.11286) often have no pileup, a statistics-only treatment or idealised backgrounds. The reviews say so, and the ranking discounts them.
5. **Reviewer derivations.** Some theory caveats are the reviewers' own derivations. These are flagged in the dossiers and are not treated as evidence:
   - the C015 coupling-structure bound;
   - the C005 lifetime-bound evaluation;
   - the C008 coupling rescaling;
   - the C019 fermiophobic-naturalness argument.
6. **Date sensitivity.** Several decisive results are from mid-to-late 2026 (e.g. 2609.37215 of 29 Sep 2026, 2610.03489, 2608.05323, 2608.28377). The landscape is moving fast, so any choice should be re-checked against the latest CMS/ATLAS results before work starts.
