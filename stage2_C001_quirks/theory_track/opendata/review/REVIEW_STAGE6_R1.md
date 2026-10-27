# Review R1: STAGE6_FEASIBILITY.md (critical reviewer, fresh)

Method: read the note, plan.md §1.4/§4.2 (cross-references exist and match), LOG.md. Web check: 2016 UL MiniAOD/NanoAOD release is real
(CMS/CERN announcements); the search could not confirm RAW/ZeroBias record details, so those rest on the note's own API tags, which I did
not re-verify. I did not independently re-open the CMSSW event-content files.

Policy reminder: PRESENT (box at top, repeated at the end; says CMS member, internal rules document, terms of use, citation; makes no claim
about what is allowed). Good. Tagging: VERIFIED/UNVERIFIED/ESTIMATE used consistently. No Category A found.

## Findings

B-1 (omission vs. the brief). The note covers only tracker-background checks (NI/V0/conversion, cluster density, cosmics). It never discusses
the kinematic checks Open Data can actually do and that bear on the signal: Z(mumu)/V+jets pT (ISR hard-jet tail, which drives the Stage-2
signal normalisation and the quoted LO-MLM +12..+15/-11..-13 % tail uncertainty), MET scale/resolution/tails and MET recoil against the
leading jet in 2016 UL MiniAOD/NanoAOD, and MET-vs-plane direction behaviour for the Z(nunu)/W+jets SM background. These are cheap (NanoAOD,
no containers) and are the natural "what Open Data CAN check" items. Add a short subsection with limits (detector-level MET is not
truth-level quirk recoil; the quirk MET is the pair's recoil with no jet-like energy deposit, so only the ISR and SM-MET side is checkable;
Run-2 PU 25-35, not 200; comparison is data vs Pythia/MG, not a validation of the quirk model). Also state in one sentence that nothing in Open
Data can test the headline quirk-specific inputs (string dynamics, the P_fake ~1e-9 PU-combinatorics fake rate, signal efficiency).

B-2 (overclaim, check 3 and table). "Replaces the UNVERIFIED cosmic-rate citation in §4.2" and "cosmic and non-collision rate bound" is stronger
than the evidence: the note itself says there is no Cosmics PD and cosmic content of NoBPTX is UNVERIFIED, NoBPTX events are triggered in
empty bunches, so converting to an in-time rate x 25 ns x d0<1 mm acceptance needs trigger-efficiency and live-time bookkeeping the note does
not mention. Reword to "might provide a rough in-time cosmic/halo rate if NoBPTX contains them; otherwise cite the published CMS cosmic-muon rate".

B-3 (tag precision). "VERIFIED (collection kept)" for AOD contents (`nuclearInteractionMaker`, ClusterSummary, etc.) is verified from the CMSSW
event-content config, not from inspecting an Open Data file. Config-vs-file mismatches happen (Open Data files were produced with specific
releases and sometimes custom content). Tag as "VERIFIED from config; file content not inspected" and make the first step of any check a
`edmDumpEventContent` on one file. Same for the 10_6 `inclusiveSecondaryVertices` claim for AOD (relevance to released 2016 files unstated).

B-4 (missing overview). The note never states which years/tiers are released (Run 1: 2010-2012 AOD/RAW partly; 2015 AOD; 2016 UL MiniAOD,
NanoAOD; 2017 RAW/MC records found) and so the reader cannot see the baseline for "hit-level not in released tiers". The note shows hit-level
IS available only via RAW (2010-2012, 2017E) with a full re-reco in an SLC container; say explicitly that hits are absent from AOD/MiniAOD/
NanoAOD and that RAW re-reco is the only route, and that none of this is a quirk signal sample (no quirk-like anomalous tracks exist in released
data as a validation signal). Add a short year/tier table with tags (the 2016 UL MiniAOD/NanoAOD release is verified by CMS announcements).

B-5 (usefulness of check 1). Rates of NI/V0/conversion vertices per pp interaction vs r validate toy inputs (r_NI weights, B_NI rates), but
the Stage-4 NI background is a pattern-mimicry probability after PU overlay (plan §4.2, f_pre, 8-9 decades extrapolation). State that Open Data
constrains the input rates only (probably to ~tens of %, ESTIMATE) and cannot test the extrapolation or the final mimic rate. "Highest value per
effort" is fine; "Validates" should read "constrains".

B-6 (schedule). Deadline is Sat 2026-10-17 night. The note should say plainly that none of the checks fits that deadline and they are
follow-up work, so the user does not expect results in this project. Also the quoted effort (1-2 wk, 3-5 wk) has no tag beyond the "rough ESTIMATE"
header; fine, but link it to the deadline statement.

C-1 PU of runs (10-60 range) and 2017E runs are UNVERIFIED: ok as tagged; 2012 mean PU ~21, 2016 ~27 are well-known and could be tagged ESTIMATE.
C-2 "Phase-0 pixel in 2015-16, Phase-1 in 2017" correct (UNTAGGED); "beam-pipe radius also changed" is true (LS1) and could be tagged known/UNVERIFIED.
C-3 "Mac M3 emulation" (x86 containers): hardware label "M3" not in the sources I saw; verify or say "Apple silicon".
C-4 Looper row ("UNVERIFIED that low-pT loopers are reconstructible") fine; consider dropping it from the ranked list entirely as it is not used.
C-5 Mention the CC0 terms do not remove the CMS-member rules (implied; one clause would make it explicit). Also remind that Stage-5 labelling rules
(no CMS name/logo) must stay if any Open Data comparison is ever shown.

## Verdict: ITERATE (0 A / 6 B / 5 C)
No factual error found in the verified statements; blocking is on the omission of the kinematic checks named in the brief (B-1) and two
overclaims/tag issues (B-2, B-3). If the orchestrator regards B as advisory per 03-review.md §6.1, this is effectively PASS with notes.
