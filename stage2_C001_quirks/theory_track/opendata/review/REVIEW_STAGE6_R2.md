# Review R2: STAGE6_FEASIBILITY.md (critical reviewer, fresh, round 2)

Method: read the note, R1 review and fix record. Re-queried opendata.cern.ch API (records 93950, 93951, 93952, 30516, 62, 24116, 24106, 6018, 414, plus searches for 2016 NanoAOD and Cosmics) and the raw CMSSW event-content files on GitHub (RecoLocalTracker and RecoVertex, 5_3_X / 7_6_X / 10_6_X). Plan cross-refs were checked in R1 and not re-opened.

## R1 findings: resolution check
- B-1 (kinematic checks, headline-inputs statement): RESOLVED in substance (top box + section 4, limits stated). Residual tagging gap, see B-1 below.
- B-2 (cosmic overclaim): RESOLVED. Row and check 3 now say "rough, may fail", bookkeeping named, fallback given. Reproduced: no Cosmics PD in the portal (only HLT-path records 6601, 25325, 25331...); NoBPTX 2012 AOD records exist (6018, 12.4 M ev, 342 GB, matches "about 0.33 TB").
- B-3 (config vs file): RESOLVED. Tags changed, edmDumpEventContent first-step caveat present. Re-checked configs: AOD keeps only clusterSummaryProducer in 5_3/7_6/10_6; RECO keeps siPixel/siStripClusters; nuclearInteractionMaker and generalV0Candidates in AOD in 5_3 and 10_6; inclusiveSecondaryVertices only in 10_6. All match the note.
- B-4 (year/tier table): RESOLVED. Table present and correct (below).
- B-5 ("validates" -> "constrains"): RESOLVED.
- B-6 (schedule): RESOLVED. Deadline now correctly Sun 2026-10-18 afternoon; none of the checks fits.
- C-1, C-2, C-3, C-5 applied. C-4 not applied; accepted (row already tagged UNVERIFIED).

## Spot-check of load-bearing factual claims (all reproduced 2026-10-16)
- 93950 `/ZeroBias/Run2017E-v1/RAW`, DOI 10.7483/OPENDATA.CMS.ZEN1.FJX6, 2025, CC0, no container, formats root/raw: matches (event count and size not in metadata: matches "sparse").
- 93952 SingleNeutrino ...PUForTRKv2...GEN-SIM-DIGI-RAW and 93951 QCD MuEnriched partner: exist, 2017, simulated: match.
- 30516 ZeroBias 2016G UL MiniAODv2, 2024, cmssw_10_6_30, 123 files: matches. NanoAODv9 SingleMuon 2016G/H exist (30530, 30563) and a PF-NanoAOD (31313): supports the "PF-NanoAOD subset" and section 4 premise.
- 62 MinimumBias 2012B RAW: 2,745,751 ev, 307 GB, cmssw_5_3_32, description says reconstruction can be repeated: matches.
- 24116 ZeroBias 2015D AOD: 197.7 M ev, 13.1 TB, cmssw_7_6_7: matches. 24106 MET 2015D AOD 2.38 TB: matches.
- 414 title "2018 CMS data preservation, re-use and open access policy"; research guide contains "Rules for use of open access CMS data by individual members of CMS": matches. Policy reminder PRESENT at top and end; makes no claim about what is allowed; CC0-does-not-remove-member-rules clause present; Stage-5 labelling carried over. Good.
- No overclaiming found in the ranked checks; check 1 is correctly limited to input rates.

## Findings

### Category A
None.

### Category B
B-1 (section 4 untagged and un-sourced). Section 4 is the only section with no VERIFIED/ESTIMATE/UNVERIFIED tags and no record IDs, yet it carries the claims "2016 UL NanoAOD, no container, uproot/ROOT only" and "about 1 week". Reviewer verified SingleMuon NanoAODv9 2016G/H exist (30530, 30563), but the note never names a dataset. The Z(nunu)/W+jets and MET-tail items need a MET/JetHT-type primary dataset in NanoAOD (or a Z(mumu) with muons removed method), and availability of 2016 NanoAOD for MET and for MC (DY/W/Z(nunu) samples, if data-vs-MC were wanted rather than data-vs-user-Pythia) is not stated. Fix: add one line with the record IDs (30530/30563 tagged VERIFIED (API)), tag MET/JetHT NanoAOD and any NanoAODSIM availability UNVERIFIED, tag the one-week figure ESTIMATE, and say whether a recoil-with-muons-removed proxy is meant for Z(nunu).

### Category C
C-1. Cost line inconsistent with the quoted sample sizes: "10^4 events RAW about 50-100 GB" implies 5-10 MB/event, but record 62 gives about 0.11 MB/event (307 GB / 2.75 M); even high-PU 2017 RAW is of order 1 MB/event, so 10^4 events is of order 1-10 GB, and check 2's "about 0.2 TB" also looks large. Already tagged ESTIMATE, direction is conservative; consider a clause or fix the number.
C-2. "UL NanoAOD (CMSSW_10_6_26)" in the year/tier table: the NanoAOD records I queried carry no release field, so this string is not backed by the API check. Tag UNVERIFIED or drop.
C-3. The "Data tiers (VERIFIED from CMSSW config; no Open Data file content inspected, CMSSW ..." header sentence is garbled (missing parenthesis/semicolon structure); MiniAOD "clusters only on muon track extras" claim was not re-checked by this reviewer.
C-4. Tag legend says VERIFIED means "checked on 2026-10-13"; the revision is 2026-10-16. Harmless; this review independently re-reproduced the API facts on 2026-10-16.

## Verdict: ITERATE (0 A / 1 B / 4 C)
No factual error found; all spot-checked facts reproduce. The single B is a small tagging/sourcing fix to section 4 (about 5 lines). If the orchestrator treats B as advisory per 03-review.md, this is effectively PASS with notes after that one edit.
