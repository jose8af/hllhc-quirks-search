# Scout note: SUSY beyond standard simplified models

Data: `scout_susy.json` (209 queries logged, 106 papers, 21 candidate seeds). All IDs came from inspire.py output; gap quotes were checked as substrings of the cached arXiv text (pdftotext, whitespace-normalised). No numbers (limits, reach) were taken from memory; any reach figure is UNVERIFIED unless a seed says otherwise.

## Intellectual development
- Split/mini-split (hep-ph/0406088, 1210.0555) and RPV reviews (hep-ph/9707435, hep-ph/0406039) set the long-lived-gluino/LLP and RPV language. After the 2011-12 null results, three "hide the SUSY" lines emerged: stealth (1105.5135, 1201.4875, 1512.05781), compressed/natural (1207.1613, 1111.6897, 1110.6926) and displaced/RPV (1204.6038, MFV SUSY 1111.1239).
- 2016-2020: LLP-oriented work (1601.01326 on displaced leptons from GMSB staus), Dirac-gaugino recasts (1308.3468 -> 1812.09293, 1910.12846), and HL-LHC projection papers (CMS Phase-2 stau/higgsino notes, recids 1704284/1704585).
- 2023-2026: systematic "coverage map" papers (ABC of RPV I-III: 2306.07317, 2503.03830, 2608.21033; ATLAS variable-coupling reinterpretation 2603.15007), compressed-higgsino experimental programmes (ATLAS 2401.14046, 2511.20042; CMS 2511.16394, 2604.25604) and the 2026 review 2601.06358 listing rare/challenging signatures.

## Forward-citation checks (gap followed up?)
- 1512.05781 (stealth stops unconstrained) -> CMS 2506.08825 (many light-jet stops) cites it: partly followed up; exact topology coverage not read.
- 2306.07317 ("LQD and UDD left for future work") -> 2503.03830 and 2608.21033 followed up, but both again defer the long-lived-LSP regime. Best open lead.
- 1804.00067 (no displaced dilepton search) -> ATLAS 2601.05664 now exists.
- 2311.17149 (1-5 GeV higgsino gap) -> ATLAS/CMS mildly-displaced-track and lepton-track searches 2024-26.
- 1601.01326 (solitary displaced stau leptons) -> CMS 2601.17576 (long-lived stau).
- 1308.3468 (no Dirac-gluino search): no CMS/ATLAS dedicated search found by title/abstract queries; only recasts.

## Dead ends / caveats
- INSPIRE collaboration filter works with `abstracts.value:` but not with `abstract`/`abs`; title-only collaboration queries missed many searches, so "no CMS/ATLAS search found" is weak evidence.
- Mini-split R-hadron/stopped searches look mature (well-covered); kept as weak seed.
- pdftotext two-column layout mangles review quotes (2601.06358, 2411.13837); only substring-verified quotes were kept.
- RPV 4-jet excess seed (2509.09062) and NMSSM light-singlet seed are weak/inferential.
- The scratchpad is shared with other agents; a first batch of ~15 queries was logged manually.
- Not done: reading the full text of CMS 2506.08825, ATLAS 2603.15007 and ATLAS 2609.37215 to see exactly which regions they leave open.
