# Shared brief for theory-track agents (read fully before starting)

## 1. Context
- Project: search for colour-neutral, electroweak-charged **quirks** (heavy fermions or scalars charged under
  a new confining SU(N_IC) "infracolor" with no light infracoloured matter, so the flux tube never breaks)
  with mesoscopic confinement scale Λ ~ 0.1-100 keV. The pair QQ̄ oscillates on µm-cm scales and leaves
  non-helical, nearly coplanar hit patterns in the tracker.
- The user is a **CMS member**. The target is a CMS Phase-2 analysis (B = 3.8 T, Phase-2 Inner/Outer Tracker,
  MTD timing layer, PU 200, 3 ab⁻¹), with a possible Run-3 search first. ATLAS has an active quirk search
  (public code trail); FASER has published the first quirk search [2607.26195].
- Primary benchmark: E = vector-like Dirac fermion (1,1)_{-1}, N_IC = 2. Alternates: scalar Ẽ, doublet L (1,2)_{-1/2}.
- Convention: **Λ ≡ √σ_string** (collider literature). The cosmology paper [2512.20696] uses Λ = T_c = 0.6√σ.
- The user asked: "investigate possible theoretical improvements in the quirks theory. Improvements in
  constraints (ideas: Λ, quirk oscillation length, quirk propagation dynamics, quirk trajectory models). Any
  gap in the theory that can be exploited is of interest."

## 2. Read before you start (do not redo what is already done; build on it)
Paths relative to `stage2_C001_quirks/`:
- `research/theory_signal_model.md` — the existing theory/signal model. §3 (equations of motion, ionisation,
  radiation, how each study propagated quirks), §4 (signature map vs (m_Q, Λ) at CMS), §6 (cosmology,
  naturalness, LEP/EWPT). Read at least §0, §3, §4, §6.
- `literature/literature_map.md` — census, lineage, open problems; `literature/bibliography.json` (58 entries).
- `phase1_strategy/outputs/STRATEGY_DRAFT.md` — the experimental strategy (skim §4 and anything on Λ edges,
  timing, coplanarity). `phase1_strategy/outputs/OPEN_QUESTIONS.md`.
- PDF text cache: `../research/cache/pdf/<arxiv-id>.txt` (many quirk papers already there, e.g. 0805.4642,
  1708.02243, 1911.02223, 2002.07503, 1811.08903, 2108.06748, 2404.13814, 2410.00269, 2512.20696, 2607.26195).

## 3. Tools
- INSPIRE: `python3 ../research/tools/inspire.py search "<query>" --size 50 --sort mostrecent`, `get`, `refs`,
  `cites` (run from `stage2_C001_quirks/`). Quirks: use `abstracts.value:quirk` style, and recid (not
  `refersto:arxiv:`) for citation queries.
- arXiv PDF → text: `python3 ../research/tools/arxiv_pdf.py <id> [--gaps]` (caches to `../research/cache/pdf/`).
- WebSearch / WebFetch are allowed for things INSPIRE cannot give (lattice results, PDG, code repositories).
- Numerics: from `theory_track/`, run `pixi run python code/<your_file>.py` (numpy, scipy, sympy, matplotlib,
  mpmath, numba available). Save every script you rely on in `theory_track/code/` with a header comment
  (purpose, inputs, how to run) so results are reproducible. Figures go to `theory_track/figures/`.

## 4. Rules
- **Write only your own files**: `theory_track/investigations/<ID>_<topic>.md`, `theory_track/code/<ID>_*.py`,
  `theory_track/figures/<ID>_*`. Never edit anything else in the project (Phase-2 work is running in parallel).
  The only shared file you may touch is `theory_track/LOG.md` (append one line when you start and one when you
  finish, prefixed `- 2026-10-07 <ID>:`).
- **Save incrementally**: write the skeleton of your report early and append sections as you go, so a rate
  limit or interruption does not lose work. Do not spawn subagents.
- Tagging: every number or claim carries a reference with location, e.g. `[1911.02223 Eq.III.12]`.
  `ESTIMATE` = your own calculation (state inputs and the script). `UNVERIFIED` = recalled or secondary, not
  checked against the primary source. Do not invent references; if you cannot open a paper, say so.
- Physics honesty: if an idea turns out not to matter, say so with the number that kills it. Killed ideas are a
  useful result. Do not inflate significance.

## 5. Required output format (in your report)
1. **Executive summary** (≤ 15 lines): the 3-5 most important findings.
2. **Gap entries**, one per idea, each with:
   - `G-<ID>-n` title
   - Current treatment in the literature (who, what approximation, with refs)
   - Why it is a gap (what is missing, wrong, or uncontrolled)
   - Quantitative estimate of the effect for the CMS Phase-2 target (or for constraints), with method
   - How it could be exploited: (a) stronger/new constraint, (b) new or better signature or trigger,
     (c) better reconstruction / trajectory model, (d) parameter measurement after discovery,
     (e) reduced signal systematic, (f) publishable theory/pheno paper on its own
   - Effort (days / weeks / months) and confidence (high / medium / low)
   - Verdict: **EXPLOIT** / **WORTH A CHECK** / **NOT A GAP (killed)**
3. **Killed ideas** (short list with the killing number).
4. **Open questions for other workstreams** (T1-T6) and for the experimental Phase 2.
5. **References opened** (arXiv ids, with what you used from each).
