# FIX_PAPER_A_R1: response to REVIEW_PAPER_A_R1 (1 A, 15 B, 11 C)

Executor, 2026-10-16. Text, bib and style changes only (no rerun). Recompiled (31 pp, no errors/overfull/undefined);
changed pages rendered and inspected (pp. 1, 3, 6–24, references).

| finding | change (file) |
|---|---|
| **A-1** failed V2b gate | Abstract: c law "derived analytically and confirmed by blind numerics at 1 keV (0.105 ± 0.002)"; on the 2.2e5-event simulation the law holds per event (≤ 1 %), the population median is +2–3 % above prediction, above the pre-set 1.5 % gate, "which therefore failed", read as an estimator effect (estimate). §3.7 new paragraph "Population-level status of c (used throughout this note)": numerics within 1.5 %; Stage 3 +2.0/+2.1/+3.2 % (E500/E1500/Ẽ500), +0.7/+1.1 % (E200/E1000), pooled +1.71 ± 0.29 % at 1–2 keV, zero-median scatter +2.04 % → estimator effect (EST); population uncertainty quoted as +2–3 % at 1–2 keV; 3–5 keV excess attributed to B* (EST). "population c to 1–2 %" replaced by "blind numerics within 1.5 %; full simulation +2–3 %". §4.2 c-law bullet: gate V2b stated as not passed, numbers + σ, R(1/2) 2.4σ, estimator-effect reading (EST), not a step effect, user decision to proceed (LOG 2026-10-11). §4.4 summary uses the same statement. (03_string_dynamics, 04_truth_p1, 00_abstract) |
| B-1 oscillation scale | Abstract "between metres and micrometres"; intro gives ℓ_max ≈ 5 cm (keV/Λ)² at 500 GeV, ≈5 m/50 cm/0.5 mm/5 µm at 0.1/0.3/10/100 keV. |
| B-2 dimensional slip | §3.5: "accumulated tilt ∼ qBR G[…]/p* …; the displacement is this tilt times the lever arm ∼ ℓ₀ ∝ m_Q/σ, i.e. ∝ ε_B R". |
| B-3 exponent tests | §4.2: added 1→2 keV 4.1/4.5σ (E1500/Ẽ500) and 1→3 keV 3.0/3.4/3.9σ (E1000/E1500/Ẽ500), tied to ℓ_max/R_IT ≈ 0.5–0.6; "the edge of the validity window is therefore soft". |
| B-4 pyhf | §6.5: in-house CLs, toys primary; post-R6 asymptotic/toys 0.32–1.07 (1.02–1.07 single-category signal, 0.32–0.72 two categories with large σ_ln, genuine method difference; STAGE4_RESULTS §5); asymptotic bands not used; pyhf comparison only for the pre-R6 dry run, not claimed for the final code. |
| B-5 post-freeze changes | §6.6 lists HASH_ADDENDUM §1–§6 (runner hook, navigation recovery, T_seed, PC-19), the analysis-review fixes R1–R6 (B estimates only) and A2FC. |
| B-6 CKF fraction | §5.5: 13.9 % of all measurements, 19.5 % of barrel hits, ≈ 1540 tracks/event (G1_REPORT). |
| B-7 edge systematics | §9.1: 2.3–5.2 %. |
| B-8 symbol collisions | category → κ ∈ {T, G}; K-factor → K_QCD (Eq. 2, Tab. 1, text); R(f) → 𝓡(f); log cutoff L removed (ln(ℓ_max/b)); Θ = N_odd ϑ with N_odd defined; Λ baryon → Λ⁰; App. A: c-vs-speed-of-light sentence, new rows κ, K_QCD, L, R, 𝓡(f), N_odd. |
| B-9 figure quality | Fig. 5 (7-panel, illegible) replaced by a 1×2 composite: one cropped panel (IT pair separation, unchanged pixels) + T4 edges; the merging-fraction panel could not be cropped cleanly (overlapping neighbour label), its content is in T4. Fig. 2 kept (legible at 0.44 lw); "(see D9)" inside T4 cannot be edited here → ISSUES.md (Stage-5 restyle). |
| B-10 degeneracy claim | §9.1: "below Λ_cross(m_Q) (1.2–1.9 keV)", tagged (truth level, ESTIMATE); MS-dominated above. |
| B-11 bibliography | New `unsrtnat_hep.bst` (unsrtnat + collaboration, reportNumber, eprint). TDRs re-fetched from INSPIRE: report numbers printed, Tracker TDR DOI, MTD/L1 TDR no DOI on INSPIRE/DataCite (CDS blocks scripts) → CDS record URLs from INSPIRE's CDS ids; duplicate report numbers de-duplicated; BKNC prints JINR-E2-10626; FASER journal Phys. Rev. Lett. from INSPIRE publication_info; arXiv ids printed. Logged in BIB_PROVENANCE.md. |
| B-12 author set | "Li et al." |
| B-13 FASER wording | "up to ≈180 GeV near Λ ≈ 10 keV, falling to 57 and 66 GeV at the ends of 0.3–105 keV"; "Neither ATLAS nor CMS has published a dedicated search for coplanar, non-helical quirk tracks". |
| B-14 step convergence | §4.1: 10⁻³ field-only (10⁻² bias +0.1…+1.6 %), 10⁻² material; hit shifts 0.2–4 µm at 0.3–1 keV; V3 covered field-only cells (30/32); material runs at 0.45–1.5 keV untested, ≤ +1.6 % field-part bias, toward quadrature, conservative for the dip (EST). |
| B-15 MIP unit | "pooled truncated mean of all muon-gun TBPX hits (3.558e-4 GeV)". |
| C-1 credits | 1911.02223 Fig. 4 added (§3.5); FASER App. A and the Athena software path cited (§3.6); Gubser cited for segmented strings. |
| C-2 | "K changes c by at most 6 %". |
| C-3 | "above Λ_cross ≈ 1.2–1.9 keV" in §3.7 and §6.2. |
| C-4 | literal-form sentence moved to a footnote (no project history in the text). |
| C-5 | decision labels in the body replaced by "(user decision, Appendix C)"; "species-masses" → "(species, mass) points". |
| C-6 | \eqref throughout. |
| C-7 | §9.1 intro sentence added. |
| C-8 | 38.2 = √(R_IT/100 µm) = √1465 explained. |
| C-9 | "all 83 … except the endcap timing layer (ETL)". |
| C-10 | not changed (user-approved label; captions carry the disclaimer). |
| C-11 | CMS:2008xjf, CMS:2024nhn, Gubser:2016wno now cited (47 printed); CMSTrackerGroup:2024fgx and FASER:HEPData181308v1 left uncited (harmless). |
