# Review R3: STAGE6_FEASIBILITY.md (critical reviewer, fresh, round 3)

## R2 findings: resolution check
- B-1 (section 4 tagging/sourcing): RESOLVED. Section 4 now names records and tags them VERIFIED (API, 2026-10-16), tags NANOAODSIM DY/W+jets availability UNVERIFIED, the week figure ESTIMATE, and states the Z(mumu)-muons-removed recoil proxy for Z(nunu).
- C-1 (RAW size per event): fixed (1-10 GB for 1e4 events; record 62 about 0.11 MB/event). C-2 (release string): dropped/UNVERIFIED. C-3 (garbled tiers header, MiniAOD cluster claim): repaired, tagged UNVERIFIED. C-4 (tag-legend date): updated.

## Independent spot-checks (API, 2026-10-16), all reproduce
- 93950 `/ZeroBias/Run2017E-v1/RAW`, DOI 10.7483/OPENDATA.CMS.ZEN1.FJX6, formats root/raw, no container, no event count: matches "sparse metadata".
- 93952 SingleNeutrino ...PUForTRKv2...GEN-SIM-DIGI-RAW: exists, no container field: matches.
- 30530 SingleMuon 2016G NanoAODv9: containers root-vnc/python-vnc, "does not require CMSSW": matches. Also confirmed 30563 (SingleMuon H), 30526/30559 (MET G/H), 30525/30558 (JetHT G/H), 74908/74910 (ZJetsToNuNu NANOAODSIM, 2016G/H).
- 6018 NoBPTX 2012B AOD: 12.4 M ev, 342 GB (about 0.33 TB), cmssw_5_3_32: matches. 414 title matches the policy-box citation.
- Cost arithmetic sanity: 1e6 ev x 10-50 ms = 3-14 CPU-h (note says about 10); 1e4 ev x several s = 10-30 CPU-h: consistent. PU extrapolation 200/30 about 6.7 matches "x4-7".

## Whole-note assessment
- Feasibility/usefulness: honest and well ranked; leads with "nothing fits the deadline" and "cannot test quirk-specific inputs"; check 1 is correctly limited to input rates; check 3 flagged "may fail"; MET anomalous-track search correctly not recommended.
- Tagging: VERIFIED/ESTIMATE/UNVERIFIED applied consistently, including config-vs-file caveat. No overclaiming found.
- Policy: CMS-member Open Data policy reminder present at top and repeated at end, makes no claim about what is allowed, CC0 does not remove member rules, Stage-5 labelling carried.

## Findings
### Category A
None.
### Category B
None.
### Category C
- C-1. Section 4 data list covers 2016G/H only (as the API shows); the note could say this explicitly as the NanoAOD era, to avoid implying full 2016. Cosmetic.
- C-2. "about 10 CPU-h for 1e6 events" sits at the top of the 3-14 CPU-h range implied by 10-50 ms/event; harmless, tagged ESTIMATE.

## Verdict: PASS (0 A / 0 B / 2 C)
