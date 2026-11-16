# Model ledger

Default: subagents run on Opus 5.5 (`model: "opus"`) at default effort. Only non-default choices are listed
(brief §4). Gate-panel physics reviewers, critical reviewers and arbiters never run below Opus.

| date | task | model | effort | reason | outcome |
|---|---|---|---|---|---|
| 2026-11-13 | Phase-1 investigator D6 (grep digest of the v1 decision logs), session Andrzej | sonnet | default | mechanical log digest (brief §4 "go down") | delivered: all three logs read in full, numbers tagged with file:line; quality adequate |
| 2026-11-13 | Phase-1 strategy executor, session Brigitte | fable | default | acceptance criteria, schedule conversion and pre-registration structure are error-prone and set the whole study (brief §4 "go up") | delivered: STRATEGY (1,250 lines) + COMMITMENTS + budget script; under review |
| 2026-11-13 | Phase-1 fixer after ITERATE (35 merged findings; likelihood, closure and sample-size redesign), session Dmitri | fable | default | statistics/likelihood design and pre-registration criteria (brief §4 "go up") | delivered STRATEGY v2: 24 resolved, 3 partial, 8 deferred to Gate A; under re-review |
| 2026-11-13 | Phase-1 fixer cycle 2 (4 A + 14 B new, 7 partial), session Emeric | fable | default | same reason as cycle 1: closure/likelihood design; aim is a verification-only cycle 3 | delivered STRATEGY v3 (2,674 lines): 7 M closed, N1–N18 resolved; under cycle-3 review |
| 2026-11-14 | Phase-1 arbiter, cycle 8 (session Margaret) | fable | default | three reviewers agree on the defect (W1) but give different recomputed numbers; the last three arbiter-written fix texts were each incomplete; cycle 9 is the last before escalation to the user (brief §4: go up after failures and for contentious arbitration) | found the root cause (rule 1 itself ambiguous), reconciled all three reviewers' numbers, delivered complete replacement code with expected sha256, a self-test and a text checker |
| 2026-11-14 | Phase-1 arbiter, cycle 9 (session Odette) | fable | default | final cycle before the matter goes to the user; the verdict decides PASS or the open list (brief §4: arbitration, go up) | ITERATE (0 A, 1 B) with own mechanical confirmations, exact tested edit list and a corrected Gate-A package |
| 2026-11-16 | Phase-1 fixer, cycle 9→10 (session Oscar) | opus | default | default model; the fix is exact-text and mechanical (logged for completeness after two fable arbiters) | delivered v10; all hashes as predicted; one read-only git diff against instructions |
| 2026-11-16 | Phase-1 critical reviewer and arbiter, cycle 10 (sessions Pauline, Quentin) | opus | default | default; the cycle-9 arbiter defined a mechanical check with no new adjudication expected, so no reason to go up | reviewer: a–g pass; arbiter: PASS |
| 2026-11-16 | Phase-2 executor channel (iii): pilot, T1 workspace builder, Geant4 geometry and hand-over (session Tatiana) | fable | default | the pilot's counts are the only input of the binding day-15 rule and the Geant4→Fatras hand-over is a named top risk; error-prone and sets the study (brief §4 "go up") | pending |
| 2026-11-16 | critical reviewer of strategy addendum 1 (session Ulrich) | fable | default | the addendum changes Gate-A-frozen readings of the binding day-15 rule and its first pool table was already wrong once; one reviewer only, so go up (brief §4) | pending |
