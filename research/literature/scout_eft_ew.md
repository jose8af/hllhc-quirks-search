# Scout note: EFT and electroweak precision cluster (eft_ew)

Companion to `scout_eft_ew.json` (18 seeds, 118 papers, 229 logged queries). All arXiv IDs came from INSPIRE records. Gap quotes were string-checked against the cached PDF text or INSPIRE abstract. Gap types are guesses only, not findings.

## Intellectual development

1. **Foundations.** Warsaw basis (1008.4884) gives the dim-6 language. Dim-8 bases (2005.00008, 2005.00059) opened a second front, and positivity bounds (1808.00010, 2005.03047, 2101.01191) turned the sign and cone of dim-8 coefficients into a UV-motivated target.
2. **Energy-growth programme.** High-energy Drell-Yan (1609.08157, 1811.12260, 2008.12978) and diboson interference resurrection (1708.07823) establish that the useful signal sits in the high-energy tails. Interference suppression and EFT validity are the recurring caveats (1604.06444, 2412.14162, 2607.02649).
3. **Convergence of strands (2020-2026).** Dim-8 DY angular dependence (2003.11615) leads to A_i at high mass (2512.05018) and T-odd A6/A7 (2511.19617, 2608.04437). Positivity moves from VBS (1808.00010) to DY moments (2204.13121), then to diphoton (2512.04336) and the full aQGC cone (2604.00107).
4. **Experimental side.** CMS and ATLAS have EFT combinations (2504.02958, 2604.21670), Z-peak angular coefficients (2604.25678, 1606.00689), nTGC and aQGC limits, and first polarised ssWW results (2009.09429, 2503.11317).
5. **New direction.** Quantum-information observables in diboson (2302.00683, 2505.12125, 2601.09540) are recent. In the WZ study (2601.09540) the entanglement witness is not established for realistic WZ kinematics.

## Seeds with the best-supported gap statements (medium confidence)

- High-mass A_i (Lam-Tung / A0-A2). Quotes: 2512.05018 and 2003.11615.
- T-odd A5-A7. Quote: 2511.19617 explicitly encourages experimentalists.
- Positivity tests (DY moments 2204.13121, aQGC cone 2604.00107).
- EFT validity and truncation nuisances (2607.02649, 2412.14162).
- High-mass A_FB and above-Z running of sin2theta (2302.10782, 2310.19638).
- Interference resurrection (2301.13663).
- Heavy-flavour DY tails (2003.12421; CMS b-tag search 2506.13565 already exists, so the open piece is c/tau).
- Triboson SMEFT (2303.18215, 2407.09600).

## Forward-citation checks performed

- Citations of 2003.11615, 2204.13121, 2511.19617, 2512.04336, 2301.13663, 2310.19638, 2412.14162, 1808.00010 and 2402.16365 were read in recent-first order. Only the 10-12 most recent citations of each were listed, so completeness is UNVERIFIED.
- Follow-ups found are all theory or phenomenology (e.g. 2512.05018, 2608.04437, 2604.00107, 2605.03254). No CMS/ATLAS high-mass A_i or dim-8 DY fit appeared by title search.
- HEPData and CONF notes were not searched.

## Dead ends and caveats

- **W mass and SMEFT.** Title and abstract searches found no paper on BSM-induced bias in the ATLAS or CMS W-mass analyses. The only hits were generic EWPO fits (2204.04805). No seed produced.
- **Flavour-nonuniversal e-vs-mu ratio at high mass.** Searches returned nothing specific. This is folded into the heavy-flavour/flavour seed.
- **Top-quark EFT (tt tails, tW).** Covered by global fits, with no explicit gap sentence. Retained as a low-confidence "well-covered" seed.
- **Universal SMEFT W,Y.** The gap quote is weak (a result, not a gap statement). Confidence is low.
- **INSPIRE query syntax.** Mixing `or` and `and` without parentheses often returned empty results or off-topic hits. `abstract "..."` returned nothing, while `ab "..."` worked intermittently. Many title-field combinations failed silently, so negative search results are not strong evidence of absence.
- **Experiment coverage not fully verified.** The CMS 2408.07622 mass range and CMS 2510.00118 aQGC parametrisation were taken from abstracts and titles only, not read in the PDFs.
- **Shared scratchpad.** Other scouts overwrote same-named helper files in the shared scratchpad. This run used its own `eft/` subdirectory.
- **Cache contention.** Parallel scouts share the INSPIRE cache and rate limit, which slowed query throughput.

## Novelty kinds

- Mostly new experimental analysis of existing theory (A_i at high mass, T-odd coefficients, cone-aware aQGC).
- Phenomenology-only seeds: universal SMEFT, HEFT multi-Higgs, tt tails.
