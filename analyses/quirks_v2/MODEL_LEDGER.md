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
| 2026-11-16 | critical reviewer of strategy addendum 1 (session Ulrich) | fable | default | the addendum changes Gate-A-frozen readings of the binding day-15 rule and its first pool table was already wrong once; one reviewer only, so go up (brief §4) | ITERATE, 3 A / 10 B, all tables independently recomputed; found the excluded populations and the unvalidated hand-over |
| 2026-11-16 | executor for the toy-cost remedies (session Viktor) | opus | default | default model; bounded numerical timing task | delivered: jax backend + warm starts bring toys to 47–228 CPU-h at 60–100 parameters; correctness check passed |
| 2026-11-16 | critical re-reviewer of strategy addendum 1 v2 (session Wanda) | fable | default | same reason as the first addendum review; fresh session per the review protocol | ITERATE 2 A / 5 B / 12 C; independent code reproduced all tables; found the parent-truncation fault in the author's own validation file |
| 2026-11-16 | Phase-2 executor channel (iii) successor: pilot campaigns ready to submit (session Xavier) | fable | default | same reason as Tatiana: the pilot's content and classes are the only input of the binding day-15 rule | pending |
| 2026-11-16 | fixer of strategy addendum 1 v2 → v3 (session Yvonne) | fable | default | third version of a document that changes the binding day-15 readings; two iterations already (brief §4: go up after failures) | pending |
| 2026-11-16 | fixer of strategy addendum 1 v3 → v4 (session Zoe) | fable | default | same reason as v3; must integrate the half-turn finding and the looper result without softening | pending |
| 2026-11-16 | Phase-2 executor channel (iii), second successor: B1 pilot code and campaign files, looper rerun (session Albert) | fable | default | same reason as Tatiana and Xavier | pending |
| 2026-11-16 | critical reviewer of strategy addendum 1 v4, third and last 1-bot round (session Bruno) | fable | default | last review before the user's approval of changes to Gate-A-frozen numbers; two ITERATEs before (brief §4) | ITERATE 0 A / 4 B / 12 C with exact text; 42 numbers recomputed; read Stage 3 to close the signal gap |
| 2026-11-16 | fixer v4 → v5 of addendum 1 (session Clara) and mechanical check (session Dario) | opus | default | default: exact-text application and its verification | v5 delivered, all items applied; check PASS with 9 C edits |
| 2026-11-17 | Phase-2 executor channel (ii) successor (session Edgar) | opus | default | default model | pending |
| 2026-11-17 | T1-b likelihood check against v1 (session Flora) | fable | default | statistical procedure with unstable numerics and a frozen criterion that may fail as worded; error-prone (brief §4) | delivered: plan fixed in advance; FAIL as frozen on a thin margin; cause isolated (toy recipe at a jump, not the likelihood) |
| 2026-11-18 | Phase-2 executor channel (i) successor: c1-gen fix, E2(ii) restricted V4-5 scan, C2-b/c, stitch 100k, C1 comparisons (session Ignatius) | opus | default | default model (brief §4) | done 12:21: c1-gen fixed, rates PASS, C2-a(ii) FAIL, C2-b PASS, C2-c no power, stitch closes, SM FAIL |
| 2026-11-18 | Phase-2 executor: per-stream validation jobs of the B1 pilot (addendum P7) (session Hedda) | fable | default | output feeds the pilot classification behind the binding day-15 reading (state file §0 rule 1(c)) | done: 8/8 streams pass; pilot-wide 318 flagged events; val-s2 queued |
| 2026-11-18 | advisor call: D9 basis after the measured flagged-event count (session Isolde) | fable | default | advisor trigger: number behind an addendum-1 decision (state §0 rule 1(b)) | D9 stands; daily-report line; PREREG_v2 with/without rule |
| 2026-11-18 | regression investigator: SM family FAIL in C1 (session Jorund) | fable | default | brief §4: regression investigators go up; a frozen criterion failed | ticket: width in z-score (≈95 %), generator ruled out |
| 2026-11-18 | advisor call: SM-family ticket, E4 vs bug, notice content (session Kestrel) | fable | default | advisor trigger: frozen criterion re-read + decision to user | diagnosis accepted; E4 to the user; C′_PU fixed before reading |
| 2026-11-18 | fix agent: clustered widths in c1_compare.py (SM, C′_PU, joint replicas) (session Lisbet) | opus | default | default model | done: stage A 54610b6, SM PASS 3/3 pending E4 |
| 2026-11-19 10:07 -0500 | Nanna | fable | rule 1(c): hs-stream validation (val-s2) feeds the day-15 reading | running |
| 2026-11-19 10:07 -0500 | Mattias | opus | channel (i) successor: C1 comparisons | running |
| 2026-11-19 10:25 -0500 | — | — | Mattias finished: C1 open read 34/35 frozen, 35/35 amended | done |
| 2026-11-19 10:25 -0500 | — | — | Nanna finished: val-s2 3/3 PASS | done |
| 2026-11-19 10:29 -0500 | Oddny | fable | advisor (blinding trigger): sealed C1-d readiness | NO-GO until 3 items closed |
| 2026-11-19 10:29 -0500 | Petra | opus | fixer: sealed-mode coherence, global χ², guards (code + synthetic tests only) | running |
| 2026-11-19 10:29 -0500 | Ragnar | opus | closure-slope seed scan (diagnostic) | running |
| 2026-11-19 10:43 -0500 | Sigrid | opus | dedicated sealed C1-d session | done: all PASS |
| 2026-11-19 10:43 -0500 | Petra | opus | fixer (sealed mode) | done, 0fcba56 |
| 2026-11-19 10:45 -0500 | Ragnar | opus | closure seed scan (diagnostic) | done, no flip |
| 2026-11-19 11:10 -0500 | Sune | opus | channel (ii) successor: runner exception + FxFx | running |
| 2026-11-19 11:10 -0500 | Tove | fable | rule 1(c): pilot classification + preliminary B50 | running |
| 2026-11-19 11:12 -0500 | Ulrika | opus | D2 robustness test | running |
| 2026-11-19 11:12 -0500 | Vidar | opus | C1-c container rerun | running |
| 2026-11-19 11:15 -0500 | Wenche | fable | advisor: DP1 choices S2-e, P1 | done |
| 2026-11-19 11:19 -0500 | Vidar | opus | C1-c container | NOT TESTED (permission refused) |
| 2026-11-19 11:19 -0500 | Yrsa | fable | advisor: C1-c | done |
| 2026-11-19 15:22 -0500 | Tove | fable | preliminary rule-1 | done: 620 / 10,777 |
| 2026-11-19 15:24 -0500 | Åsa | fable | advisor: preliminary rule-1 | done |
| 2026-11-19 15:24 -0500 | Björn | fable | rule 1(c): independent review + ceiling cross-check | running |
| 2026-11-19 15:24 -0500 | Cecilie | fable | rule 1(c): positive control, subset-pass, shortcut power | running |
| 2026-11-19 15:35 -0500 | Björn | fable | independent review + ceiling | done |
