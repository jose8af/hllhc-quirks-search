# EXPLORATION — Phase 2 of the quirks v2 study (consolidated)

**Status:** consolidated Phase-2 artifact, written 2026-11-23 from 15:38 -0500 (`date`) by Peder (Opus, executor).
Six items were running or undecided at writing (D8 decided since, 23 Nov 15:45); each has a marked `PENDING` block (list in §11). Phase 2 is **not closed**
by this document: it closes when the PENDING blocks are filled or ruled on.

**What this is.** A consolidation of the channel files of Phase 2 (16–23 Nov 2026). No new computation, no new
number: every number below is copied from a channel file, a result JSON, `LOG.md`, `COMMITMENTS.md` or a notice, with
its source. Where two documents disagree on a number, both are given and the disagreement is listed in §12, not
resolved.

**Tags.** `[V]` = VERIFIED by the agent that measured or re-derived it (as that agent's file states); `[E]` = ESTIMATE;
`[U]` = UNVERIFIED (transcribed by the source agent, not checked by it). Each tag carries the source as
`file:line`. `re-read` = I re-read the value from the result JSON on einstein (read-only, `python3 -I`, nice 19) and
it agrees. File abbreviations are in §0.2.

**Blinding.** No signal sample file was opened for this document. No v2 signal efficiency is stated. The C1 open
signal tier is quoted as verdicts and p-values only; the sealed C1-d tier is quoted as PASS/FAIL only
(COM l.171). Signal quantities given are those COM BL-1 allows (cross sections, K, f₂₀₀).

**Binding wording.** D2 is worded by the advisor ruling of LOG l.991 (Olav), not by the D2 result file. Rule 1 is
worded by the rulings (i)–(iii) of LOG l.975 (Åsa). Frozen criteria are quoted from `COMMITMENTS.md`, the strategy
(STR) or addendum 1 (ADD), not reworded. Amendments E1–E4 are made after the results and are cited as such
(COM l.286-309).

## 0. Summary

### 0.1 Verdicts against the frozen Phase-2 criteria

| item | frozen criterion (quoted, short) | verdict as frozen | verdict as amended / reading in force | source |
|---|---|---|---|---|
| C1-a, 41 comparisons | "each p > 0.05/41, global χ² below its 99th percentile, family coherence \|z\| < 3" (COM l.168) | 40/41: sm.R04 FAIL (z +3.64), SM coherence +4.60 | **41/41 PASS with E1–E4**: 31/31 background, 4/4 open signal, 6/6 sealed; both global χ²₄₁ forms PASS | MAT l.17-21; LOG l.963; COM l.307 |
| C1-b | "central values to 10⁻⁶, B₈₄ within 1 %" (COM l.169) | central PASS; B₈₄ FAIL on 29/86 (worst 3.4 %) | **PASS under E1** (largest difference 1.76σ of v1's own MC scatter) | ROS l.135-144; COM l.292 |
| C1-c | "one C1 job rerun in the container with identical output hash" (COM l.170) | **NOT TESTED** (docker build refused by the permission system) | E5 (content comparison) proposed by the advisor, not decided; user's docker decision open, no default; deadline Phase 5 review | VID l.6-8; LOG l.970-971 |
| C1-d | sealed tier, PASS/FAIL only (COM l.171) | **6/6 PASS**; signal-family coherence 3/3 PASS; global χ²₄₁ frozen-naive PASS, joint-block PASS | — | LOG l.963; PET l.6 |
| C1-e | "twin ratio full/fast reported against the declared expectation" (COM l.172) | reported (diagnostic, no criterion), open part only | fallback twin ratio sealed (encrypted file only) | MAT l.113-114; PET l.29 |
| C2-a (V4-5) | "\|Δn\| < 1 mrad against the brute-force optimum and against the independent fit in ≥ 48/50 and ≥ 48/50" (COM l.173) | **FAIL** both halves (optimum 0/50, 6/50; fit 50/50, 50/50) | **E2: (i) PASS** (50/50, 50/50); (ii) restricted scan FAIL 46/50, 46/50 → "(i) alone is the accuracy test and the scan is reported as failed" | V45 l.15-18; V45R l.32-37; COM l.293, l.297-298 |
| C2-b (V4-4) | "bit-identical reruns on the same node; different seeds differ; seeds recorded" (COM l.174) | **PASS** (20/20 same node, 20/20 cross-node) | — | C2V l.11-16 |
| C2-c (T_seed) | "\|z\| < 2.73 for the pass fraction of every rung family at ρ = 1 and 2" (COM l.175) | **PASS, no power** (every family pass fraction 1 or 0) | flag: proposed reporting form, not applied | C2V l.39-43, l.54-60 |
| S2-a | three validations (COM l.231) | val. 1 PASS; val. 2 PASS with the qualifier "reference = an independent public code run by us … not a published number"; val. 3 PASS (power caveat) | — | EDG l.17; LOG l.577-583 |
| S2-b | "table of σ_norm(m) with both PDF sets; every limit also quoted with σ_NLO × (NLO+NLL)/NLO" (COM l.232) | **met** (ratio from self-run Resummino, scalar applied to E: flagged) | — | EDG l.18, l.91-133 |
| S2-c | "scale, PDF, merging-scale, tune and FxFx (500 and 1,500 GeV) comparisons; nuisance in T1" (COM l.233) | comparisons complete (scale, PDF, merging, tune, FxFx at 500 and 1,500 GeV; both FxFx central values inside the band, band and κ unchanged); T1 propagation due at 4a (row open) | — | EDG l.19; SUN l.201-204; HAL (FXFX_E1500_halvard_2026-11-23.md) |
| S2-d | "nominal samples showered with the QED-FSR card" (COM l.234) | met for the S2-c samples; production must pass `--qedfsr` | — | EDG l.20, l.211-214 |
| S2-e | "cited figure and page; else … 'parametrised, not sourced' with the pre-declared wide nuisance" (COM l.235) | curve sourced, no uncertainty stated | **user decision 19 Nov:** option (b), threshold 250 GeV, −10.6 % absolute at 250 GeV, recorded as a clarification before A | COM l.366; LOG l.969 |
| S2-f | "number per mass with its source (R-12) or the label 'not sourced'" (COM l.236) | +5.7 % (E 200) … +7.9 % (E 1500) at 1 keV; **not sourced**; one-sided band | — | EDG l.22, l.264-275 |
| P1-a | "executed and read against the pre-declared table" (COM l.237) | test 2 "not the floor pattern"; test 1 **not done** ([DT3]) | user decision 19 Nov: rn47 diagnostic recorded beside the verdict, "diagnostic, not a pre-declared test" | EDG l.23; COM l.367 |
| P1-b | "pre-declared reading at 3σ (5 keV) and 2σ (1 keV)" (COM l.238) | 5 keV: "B\* attribution not supported at 3σ"; 1 keV: compatible with zero at all five points | — | EDG l.24 |
| P1-c | "\|median\|/median(c_ev) ≤ 1.5 % and ≤ 2σ at five points" (COM l.239) | **FAIL** (3 of 5 points) | — | EDG l.25 |
| P1-d | validity-window table (COM l.240) | table done (9 of 30 cells pass); Linux rerun moves no quoted number | — | EDG l.26 |
| T1-a | "schema-valid" (COM l.208) | PASS for the builder's v1-mode workspace | — | TAT l.54 |
| T1-b | "reproduces the v1 best-point hybrid-toy limit μ₉₅ = 789.7 … within 10 %" (COM l.209) | **FAIL** (902.0 ± 31.9, outside [710.77, 868.72]) | **PASS under E3** ((a) 2×10⁻⁴; (b) identical, sd 38) | FLO l.12-17; COM l.294 |
| B1-d (Phase-2 part) | "\|Δ(x/X₀)\| ≤ 1 % per layer, positions to 1 µm; hadronic interactions and decays … off in Fatras" (COM l.180) | **PASS** (geometry and Fatras physics) | added fact: no hit beyond half a turn ([L15]) | TAT l.50-51; COM l.347 |
| Pilot (ST-1, rule 1 preliminary) | rule 1 "computed preliminarily at day 7 … binding at day 15" (STR l.2742-2745) | preliminary reading done day 3: **above 300** | stand-in lower bound B₅₀(R09) = 10,777 (m_Z = 253); subset-pass count unreviewed (§6) | TOV l.16-17; LOG l.975 |
| D2 robustness row | ADD l.310-321 | **"effect, robust"** with r < 1: no correction, no credit | wording of the advisor ruling, §5.6 | D2R l.27-46; LOG l.991 |
| ST-1 checkpoint 1 | "re-projection with measured costs at day 5" (COM l.257) | done 23 Nov: ≈ 4,600 [4,070–5,050] CPU-h, no stop rule near | — | LEI l.8-12 |

### 0.2 Source abbreviations (all under `phase2_exploration/` unless stated)

ROS `outputs/EXPLORATION_i_rosalie_2026-11-16_14-43.md` · MAT `outputs/EXPLORATION_i_mattias_2026-11-19.md` ·
V45 `outputs/V45_RESULT_rosalie_2026-11-17_08-13.md` · V45R `outputs/V45_RESTRICTED_ignatius_2026-11-18.md` ·
C2V `outputs/C2_VERDICTS_ignatius_2026-11-18.md` · STI `outputs/STITCH_100k_ignatius_2026-11-18.md` ·
SMF `outputs/SM_FIX_lisbet_2026-11-18.md` · PET `outputs/SEALED_PREP_petra_2026-11-19.md` ·
VID `outputs/C1C_CONTAINER_vidar_2026-11-19.md` · RAG `outputs/CLOSURE_SEEDSCAN_ragnar_2026-11-19.md` ·
SEB `outputs/EXPLORATION_ii_sebastian_2026-11-16_11-53.md` · EDG `outputs/EXPLORATION_ii_edgar_2026-11-17_08-17.md` ·
SUN `outputs/FXFX_sune_2026-11-19.md` · TAT `outputs/EXPLORATION_iii_tatiana_2026-11-16_14-18.md` ·
PDM `outputs/PILOT_DECISIONS_tatiana_2026-11-16_13-22.md` · PRX `outputs/PILOT_READY_xavier_2026-11-16_15-09.md` ·
HT `outputs/HALF_TURN_xavier_2026-11-16_16-08.md` · LG `outputs/LOOPER_GUN_xavier_2026-11-16_16-38.md` ·
A1T `outputs/A1_TRUNCATION_xavier_2026-11-16_15-40.md` · A1A `outputs/A1_OPTION_A_xavier_2026-11-16_16-17.md` ·
B1R `outputs/B1_READY_albert_2026-11-16_20-24.md` · HED `outputs/B1_STREAM_VALIDATION_hedda_2026-11-18.md` ·
FLO `outputs/T1B_RESULT_flora_2026-11-17_09-35.md` · VIK `outputs/TOY_COST_viktor_2026-11-16_16-33.md` ·
TOV `outputs/RULE1_PRELIM_tove_2026-11-19.md` · ING `outputs/RULE1_VALID_ingvild_2026-11-23.md` ·
CEC `outputs/RULE1_VALID_PLAN_cecilie_2026-11-19.md` · BJO `review/RULE1_REVIEW_bjorn_2026-11-19.md` ·
ESK `outputs/CPU_ATTRIB_eskil_2026-11-19.md` · D2R `outputs/D2_RESULT_jonas_2026-11-23.md` ·
LEI `outputs/CHECKPOINT1_leif_2026-11-23.md` · LOG `LOG.md` · COM `COMMITMENTS.md` · STR
`phase1_strategy/outputs/STRATEGY_oscar_2026-11-16_10-41.md` · ADD `phase1_strategy/outputs/STRATEGY_ADDENDUM_1_v5_clara_2026-11-16_18-21.md` ·
STATE `ORCHESTRATOR_STATE.md` · notices in `notices/` (repo path `analyses/quirks_v2/notices/`).

## 1. Sample inventory

All Phase-2 samples are simulation (no collider data). Bulk files are under `/nfs/cajuela/jdochoa/quirks_v2/data/`
with one marker per file in `ledger/markers/<campaign>/`; a file without a marker does not exist.

| sample | campaign(s) | size | content / schema | source |
|---|---|---|---|---|
| C1 pile-up ρ = 1 | `p2-a-c1-pu1` | 4,000 events, 200 jobs | chain + 4 finder trials per event; hit dumps 2.64 MiB/event | MAT l.13; LEI l.240 [V] |
| C1 pile-up ρ = 2 | `p2-a-c1-pu2` | 1,000 events, 200 jobs | 2 trials per event, pre-merge store 33.8 MB/trial (63.1 GiB total) | ROS l.22-26; LEI l.232 [V] |
| C1 C′₀, C′_PU, SM, rates | `p2-a-c1-cp0` (16), `-cppua` (50), `-cppub` (75), `-sm` (50), `-smregen` (2), `-gen2` (12) | as listed (jobs) | v1 frozen configuration (T_seed 4, road 0.15) | MAT l.13-14 [V] |
| C1 signal (open/sealed) | `p2-a-c1-s2`, `-s3`, `-siga2`, `-siga5` | 400 rows per point | regenerated Stage 2 and Stage 3; sealed outputs not opened here | ROS l.58-67; PET l.32 |
| stitch check | `p2-a-c1-s2inc` | 6 × 20,000 LHE at m = 200 | INC chunks for the TRG/INC closure | STI l.12-14 [V] |
| C2 | `p2-a-c2-v45*`, `-v44a/b/c`, `-tseed1/2`, `-tstime` | 100 events (V4-5), 20+20+22 jobs (V4-4), 500 + 200 events (T_seed) | finder outputs, npz | C2V l.5-7; V45 l.3-7 [V] |
| S2-c inclusive MLM 0–2j | `p2-b-s2c-inc` | 5 × 20,000 LHE per species-mass (5 points) | npz schema per `sim/scripts/convert_hepmc.py`: quirk momenta (hard and showered), recoil, ν, jets, n_me, w, wvar [N, 211] (9 scale, 59 CT18NLO, merging, AUX), derived pair variables | EDG l.556 [V] |
| S2-c re-showers | `p2-b-s2c-rs` | same LHE × 4 variants (qCut 30, 60, Monash, FSR off) | same npz schema | EDG l.557 [V] |
| FxFx E 500 | `p2-b-s2-fxfx`, `-fxfx-gen` | 2,000 + 7 × 20,000 LHE (88,319 matched) | own main164-style driver output (signed weight, pair p_T/η/m, n_ME, jets) | SUN l.150-199 [V] |
| P1 event sets / runs | `p2-b-p1-ev`, `-run`, `-rn` | 842–1,513 events per point | per-event Δs per field/fraction and kernel (JSON) | EDG l.558-559 [V] |
| Herwig/Pythia minimum bias | `p2-b-hw-mb` | 10⁶ + 10⁶ events | per-job histograms (π, K, p, charged) | EDG l.560 [V] |
| Pilot part 1 | `p2-c-pilot-mb`, `p2-c-pilot-znn-00…15` | 40 minimum-bias jobs; 460 × 5,000 = 2.3×10⁶ Z(νν) generated, 994,446 in the full-weight class | one npz per job: hits (13 columns), truth, `evt` (truth MET, v1 preselection weight and inputs), jets, jets10, lep, tau, nu, gsum; content hash in `meta` | PRX l.41-70; BJO l.45-48 [V] |
| Pilot part 2 (B1) | 39 campaigns `p2-c-pilot-*`, 762 jobs | DIF 4×10⁶, DIF-C 4×10⁶, NI 22/30/61.5 10⁶ each, NI-X 4×10⁶, NI-C 2×10⁶, HS 2×10⁶, lowpt 2×10⁵ | `evt`, `gvtx`, `gprod`, `gcross`, `inj`, per-event `n_early_prod` | TOV l.48-50; TAT l.78-81; B1R l.17-24 [V] |
| pilot classification | `p2-c-pilot-cls{,2,3}`, `p2-c-r1v-*` | 61 + 139 job outputs | stored candidates (7,607 rows, both variants) | TOV l.104, l.127; ING l.42-45 [V] |
| D2 varied arm | `p2-c-d2-chain`, `-find`, `-ctl`, `-sum` | 600 events, 2,400 paired trials | nominal arm = `p2-a-c1-pu1` jobs 0000–0029 | D2R l.21-25, l.86-91 [V] |
| validation slices | `p2-c-px-*`, `p2-c-pa-*`, `p2-c-t-*` | slices, not pilot data | streams `px.*`, `pa.*` | HT l.4-7; B1R l.31-36 |

Storage on 23 Nov 13:36: study 266 GB (247.5 GiB) in 9,090 files, of which pilot 157.6 GiB and phase2 80.2 GiB; pool
3,705 GiB free [V: LEI l.231-235].

## 2. Data quality and pathologies (archaeology)

| finding | what was found | effect / handling | source |
|---|---|---|---|
| **Half-turn limit** (chain-wide, inherited from v1) | Fatras in this chain leaves no hit beyond half a turn of any particle (path-limit aborter compiled into pyacts 48.0.0; not configurable from Python). Against Geant4: crossings without a Fatras hit are 25.2 % of the written hits in a Z(νν) event and 37.5 % in a minimum-bias interaction (lower bounds); 21.2 % of the Z(νν) crossings occur after half a turn | limitation [L15]; chain kept by the user's option B; DIF-C/NI-C parents get option (a) | HT l.25-55, l.149-157 [V]; A1T l.11-21 [V]; COM l.341 |
| v1's looper zero | v1's 0 of 10⁵ loopers follows from the limit (a particle stopped at half a turn cannot cross a layer twice) | 25th C3 item ("v1's looper bound measured nothing") | HT l.101-117 [V]; COM l.343 |
| Fatras step limit | 0.0275 (Z(νν)), 0.0385 (W(τν)), 0.057 (tt̄ 1ℓ) particles per event dropped with all their hits ("maximum number of steps"), mostly conversion positrons; whether v1 had it is unverified | not quantified; open | TAT l.86-90 [V] |
| Slow-fragment residue | protons/deuterons with β 0.13–0.21 born in outer layers get Fatras hits 12–35 ns before production. Pilot-wide **318 flagged events (524 hits) in 1.72×10⁷ B1 events** (1.85×10⁻⁵/event), all in NI classes; plus 38 in the hs stream (2.00×10⁶ events): **356** in all | D9 stands (β cut 0.1, events flagged); with and without flagged events the rule-1 readings are identical | B1R l.72-77 [V]; HED l.100 [V]; LOG l.933-934, l.959; TOV l.22-25 |
| Strict hard check in NI files | the strict hard check fails in 177 of 314 NI chain files on the early-product item | `hard_except_early_product_hits` is the reading in force; P7 9/9 streams pass | LOG l.933, l.958 [V] |
| v1 generator cut | p̂T > 150 GeV not fully efficient for MET > 200 GeV: 1.7 % of kept Z(νν) events within 10 GeV of the cut | size not measured | TAT l.91-92 [V] |
| Non-trivial weights | Z(νν) v1 preselection weights: 994,446 events with w ≥ 0.5 (0.9739–0.98), 8,095 with 0 < w < 0.5, 1,297,459 with w = 0 (of 2.3×10⁶); mean preselection weight 0.4308 ± 0.0049 (Z(νν)), 0.2604 (W(τν)), 0.1180 (tt̄ 1ℓ) on 10⁴ each. MLM: w = 0 rows for other merging scales kept. FxFx: 17.4 % negative weights (N_eff 37,567 of 88,319) | pool counted in effective preselected events (COM l.352); signed weights in f₂₀₀^FxFx | BJO l.45-48 [V]; TAT l.42-43 [V]; EDG l.563 [V]; SUN l.191-193 [V], re-read |
| Silent job failure | all 12 `p2-a-c1-gen` jobs failed at Pythia init on 17 Nov (PYTHIA8DATA unset), queue logged exit 0 | rerun `p2-a-c1-gen2` 12/12; `queue_slot.sh` now reports failures | LOG l.910-917, l.937 [V] |
| CPU accounting artefact | in aMC@NLO event mode the MG integrators are not waited-for children; marker CPU misses them | FxFx charged at wall × 1 core | EDG l.35-39 [V] |
| numba cache index | `subset_road` cache index fails after 51 entries; 36 jobs failed at start | rerun with a fresh `NUMBA_CACHE_DIR`; to-do: per-job cache dir before production | ING l.91-97 [V]; LOG l.989 |
| Infrastructure | power loss 19 Nov 17:54 – 23 Nov 13:25 (3.8 calendar days); 9 attempts killed, none left an output; `git fsck` clean | runner retried them | LOG l.984-985 [V] |

## 3. Channel (i): reproduction of v1 (C1) and finder cross-checks (C2)

### 3.1 Measured unit costs (Table 4.0)

ρ = 1 event 55.7 s on 4,000 events (first jobs 57–59 s; Table 4.0: 60.4 s); ρ = 2 event 203.1 s on 1,000 (206 s);
finder trial at road 0.15: 11.27 ± 7.33 s (11.7 s; the assumed ×0.77 road saving is not seen); ρ = 2 max RSS
1.60–2.12 GB at 1–8 events per job → 2 ρ = 2 jobs per node [V: LEI l.72-75; ROS l.11-15].

Deviations recorded by channel (i): D-i-1 pre-merge store 33.8 MB per trial against 3.6–14 MB planned (≈ 270 GB with
the 4a sample, below the 400 GB cap; threshold N_IP2 ≥ 6 kept); D-i-2 V4-5 scan algorithm (band accumulation, checked
against the direct sum to 9.4×10⁻⁵); D-i-3 probe-row exclusion off (v1 excluded zero rows at the three C1 points);
D-i-4 T_seed test by regeneration; D-i-5 every C1 signal comparison is between independent samples [V: ROS l.22-66;
V45 l.9-11].

### 3.2 C1: the 41 comparisons

Frozen: "41 declared comparisons with `C12FC_v1`: each p > 0.05/41, global χ² below its 99th percentile, family
coherence |z| < 3; power stated; fail → investigated, not tuned" (COM l.168).

- **Background, 31 entries:** frozen text 30 PASS / 1 FAIL (sm.R04, z +3.64, frozen-script width); amended 31/31
  [V: MAT l.17-19, table l.63-76]. Code commit 29079b7 (joint-replica coherence, committed before the read)
  [V: MAT l.15-16].
- **SM family under amendment E4** (made after the result for SM, before it for C′_PU): z +0.35 / +0.57 / +0.50 at
  R04–R06 (v1 width 0: +0.50 / +0.82 / +0.75), coherent; 2σ detectable shift 16 / 17 / 94 % (R06 a gross check)
  [V: SMF l.27-31; COM l.307]. Root cause (regression ticket): the frozen z-width 1/√(weighted candidate count) treats
  ≈ 47 candidates per event as independent [V: LOG l.945].
- **C′_PU family (7 entries, rule of 54610b6 committed before the read):** 7/7 PASS, no N < 10 branch; all gross
  checks (2σ detectable shifts 77 % to 2,660 %) [V: MAT l.78-87]. Ignatius's partial C′_PU file (12:17, 18 Nov, 1/√N,
  incomplete inputs) predates the rule and is superseded, not a verdict [MAT l.85-87].
- **Families** (joint replicas): pu1 −0.30, pu2 −0.25, clos −1.10, cp0 +0.03, rates +1.68, cppu −0.31, sm +0.51
  [V: MAT l.91-99].
- **Open signal tier, 4 entries:** 4/4 PASS by Fisher exact against v1 k/200; smallest p 0.0082 (E500 3 keV R04),
  above 0.05/41 = 0.00122 [V: MAT l.106-111]. Counts and twin ratios are in MAT §3 and `outputs/c1_signal_open.json`;
  they are not repeated here.
- **Global χ², 35 open entries:** frozen naive 23.56; joint blocks 33.20 (v1 width 0: 51.36); reference 99th
  percentile of χ²₄₁ = 64.95 [V: MAT l.117-124; background sums 16.11 / 25.75 / 43.91 re-read].
- **Sealed tier C1-d:** pre-registered choices and code committed (0fcba56) before any read, selftest 11/11 on
  synthetic numbers [PET l.1-6, l.39]. Fresh agent (Sigrid), 19 Nov 10:36–10:42: **6/6 sealed entries PASS;
  signal-family coherence 3/3 PASS; global χ²₄₁ frozen-naive PASS and joint-block PASS; n-complete yes.** Nothing
  decrypted; encrypted file sha256 `ae4de9ec…f4147a8` recorded in `ledger/sealed/` [V: LOG l.963].
- **C1 complete: 41/41 PASS with E1–E4**; under the frozen text one FAIL stays on record (SM R04) [LOG l.963, l.986;
  notice `2026-11-23_1332_RESULT`].

Flags carried forward (no verdict change):
1. **Closure slope is weight-fragile:** partial read z +2.83, full read −0.46; the swing comes from the WLS weight of
   R06 (σ 0.0211 → 0.0190 with 148 → 200 pu1 jobs); linear fit χ² 685 on 1 dof [V: MAT l.127-146]. Seed scan
   (diagnostic, 10 seeds): slope z −1.04 … +0.32 (sd 0.37), none beyond |z| 3.23; the σ(R06) change is 12.6 seed sd,
   i.e. sample size, not seed scatter [V: RAG l.22-33, l.43-54]. → PREREG_v2 (§10).
2. C′_PU block χ² with v1 width 0: 22.9/7 (p 0.0018); not a criterion [V: MAT l.98, l.149-152].
3. rates.pvpair z +2.43 (p 0.015), width ESTIMATE, gross check [MAT l.75, l.153-154].
4. Cross-family correlation (T1/T1w ⊂ pu1/pu2) not removed from the global sum [MAT l.52-54, l.155].

### 3.3 C1-c (container)

Recipe committed (26f4abe, `tools/container/qv2-c1/`); the image build on maxwell was refused by the permission
system ("Unauthorized Access") and not worked around: **NOT TESTED** [V: VID l.6-8]. Two further facts: the pinned
base image `ubuntu@sha256:2198e4c6…` is not in any worker's docker store (the recipe uses local `e9569c25…`); the
frozen "identical output hash" cannot pass as written because the npz `meta_json` carries `created_utc`, `wall_s`,
`cpu_s`, hostname and zip member times [E: VID l.39-46]. Advisor (Yrsa): the criterion fails as worded → E5 (content
comparison) to be amended before any rerun; the docker permission is the user's; deadline Phase 5 review [LOG l.971].
Status: open (§10).

### 3.4 C2

- **C2-a (V4-5):** frozen FAIL in both halves: F0 against the brute-force optimum 0/50 (PU) and 6/50 (signal + PU);
  against the independent fit 50/50 (max 0.64 mrad) and 50/50 (max 0.85 mrad) [V: V45 l.15-18]. At pile-up 200 the
  ±75 mm window holds 18–24 thousand hits and the optimum is another plane (median 237 / 85 mrad away) [V: V45
  l.20, l.38-46]. Amendment E2 part (ii), restricted scan: 46/50 and 46/50 → FAIL; "(i) alone is the accuracy test
  and the scan is reported as failed" [V: V45R l.32-37; COM l.293, l.297-298].
- **C2-b (V4-4): PASS**: 20/20 bit-identical on the same node and 20/20 across nodes (both i5-7500; identity across
  CPU models not covered) [V: C2V l.9-19].
- **C2-c (T_seed 4 → 2): PASS as frozen, no power** (0 of 8 tests |z| ≥ 2.73; four tests empty, four saturated);
  diagnostic: T_seed 2 finds ≈ +0.3 % more passing hit sets at R04 (ρ = 1, paired z +28) [V: C2V l.39-52].

### 3.5 Stitch check for f₂₀₀

20k INC at E 200: TRG/INC = 1.118 (+2.32σ); with 120k INC: **1.0001 ± 0.0252** (1.000 ± 0.032 with the chunk-spread
scaling) → the 20k excess was a fluctuation of chunk c00; the 95 % upper limit on a TRG excess is ≈ 5 % (≈ 6.5 %
scaled); no change of the f₂₀₀ definition and no extra band piece [V: ROS l.74-77; STI l.18-22, l.37-43]. E 500
(1.055, 1.5σ on 20k) is not rechecked [STI l.44-45].

CPU of channel (i): C1 186.2 of 198 CPU-h, C2 22.4 of 81 [V: MAT l.160-168] (LEI l.31 gives 186.3: §12).

## 4. Channel (ii): theory inputs (S2), thickness law (P1), retrievals, generator spread

### 4.1 S2-a, S2-b

- S2-a validation 1 (FO-LO against tree level): −0.021 / 0.000 / +0.024 %, z −0.40 / 0.00 / +0.40 at 200 / 500 /
  1000 GeV → PASS [V: SEB l.165-169]. Validation 2: no published fixed-order NLO slepton number exists; Resummino
  3.1.2 run by us, ours/Resummino 1.0006 / 1.0001 / 1.0018 with squarks and gluino decoupled → PASS with the
  qualifier [V: SEB l.205-216; LOG l.578-583]. Validation 3 (K(M) against Drell–Yan): PASS, |ΔK| ≤ 0.014 where the
  test has power [V: SEB l.230-240].
- S2-b: σ_norm(m) for 14 E and 4 Ẽ masses with PDF4LHC21 (nominal, 68 % CL) and CT18NLO; e.g. σ_norm(PDF4LHC21) =
  216 fb (200 GeV) … 0.01402 fb (1500 GeV), PDF ± 2.1 … 20.8 % [V: EDG l.91-106]. Resummed cross-check ratio
  (NLO+NLL)/NLO = 0.971 (200) → 1.000 (1500) from self-run Resummino, scalar applied to E (flagged); ≤ 0.9 % on
  σ_norm at 1–1.5 TeV [V: EDG l.119-133].

### 4.2 S2-c f₂₀₀ (MLM nominal), S2-d

One definition (`src/s2/f200.py`): f₂₀₀ = σ(p_T(QQ̄) > 200 GeV after the shower) / σ(matched, inclusive), no η cut
[EDG l.137-140].

| point | f₂₀₀ ± stat | v1 | band +/− | κ_up / κ_dn | source |
|---|---|---|---|---|---|
| E 200 | 0.04836 ± 0.00091 | 0.04764 | +4.3 / −3.2 % | 1.043 / 0.968 | EDG l.164 [V] |
| E 500 | 0.10410 ± 0.00142 | 0.10418 | +2.9 / −2.5 % | 1.029 / 0.975 | EDG l.165 [V] |
| E 1000 | 0.14801 ± 0.00173 | 0.14585 | +6.0 / −5.2 % | 1.060 / 0.948 | EDG l.166 [V] |
| E 1500 | 0.16755 ± 0.00185 | 0.16876 | +6.0 / −5.9 % | 1.060 / 0.941 | EDG l.167 [V]; band re-read |
| Ẽ 500 | 0.11424 ± 0.00150 | 0.1135 | +3.8 / −3.6 % | 1.038 / 0.964 | EDG l.168 [V] |

Within 1.5 % of v1 at all five points; the tune (Monash) is the largest piece at 1–1.5 TeV (+4.8 %, +5.4 %); v1's
band was +12…+15 / −11…−13 % [V: EDG l.174-182]. QED FSR (S2-d): the FSR-off shift −0.6 % (E 200) to −3.2 % (E 1500) is
quoted outside the band; production (S1) must pass `--qedfsr` [V: EDG l.183-184, l.211-214].

### 4.3 FxFx (S2-c piece)

Runner change for the user's exception (per-job `timeout_exception`, SSH only, cap 7,200 s; 23/23 tests) committed
7c31c9e [V: SUN l.17-28]. **E 500 done:** f₂₀₀^FxFx = **0.10519 ± 0.00169** against MLM 0.10410 (+1.05 ± 2.13 %),
inside the band; band and κ unchanged [V: SUN l.194-198; re-read]. Shower via our own main164-style driver against the
installed Pythia 8.313 (nothing installed or patched; commit b8f42ed before production) after the MG5aMC_PY8_interface
segfault (DJR histograms booked for nJetMax = 1, filled at the FxFx parton count) [V: SUN l.110-119, l.150-170].
Frozen consequence: "If the FxFx value lies outside the band, the band is enlarged to contain it" (STR l.2021-2022).

> **FILLED 2026-11-23 (orchestrator, advisor Siri; LOG.md 23 Nov).** FxFx at E 1,500 GeV done: the approved single job
> `grids4` took 6,728 s of 7,200 s [VERIFIED, marker]; σ = 1.052e-5 ± 2.8e-8 pb (= Sune's step 0); 6 × 15,000 events.
> f₂₀₀^FxFx(E 1500) = 0.16353 ± 0.00242 (55,979 matched events, N_eff 24,986, 16.6 % negative weights) against MLM
> 0.16755: −2.40 ± 1.80 % (1.3σ), central value inside the +5.96 / −5.94 % band [VERIFIED, `s2/f200_fxfx_E1500.json`].
> With E 500 (+1.05 ± 2.13 % [VERIFIED, SUN]) the S2-c FxFx comparisons are complete; under STR l.2021-2022 (enlarge
> only if outside) band and κ (1.060 / 0.941) are unchanged. No difference is resolved at the ±1.8–2.1 % MC precision;
> a shift of up to ≈ 6 % at 1,500 GeV is not excluded at 2σ (−2.40 − 2 × 1.80 reaches the −5.94 % edge); the two masses
> have opposite signs and are not combined. CPU 2.74 CPU-h on 23 Nov [VERIFIED]; FxFx total for S2-c ≈ 7.3 CPU-h
> [ESTIMATE, includes Sune's 4.5 estimate].
> **Limitation (no new run, no rewording):** the frozen text calls 1,500 GeV "the mass that sets the reach"; if the
> reach sits near the Gate A ESTIMATE of ≈ 243 GeV, FxFx is untested there, below its lowest mass (500 GeV), where f₂₀₀ is
> smallest (≈ 0.048 at E 200 in v1). The criterion does not require a run there.
> **Stale field:** `s2/f200.json` (Edgar) `fxfx: "not run"` is superseded by `s2/f200_fxfx.json` (E 500, sha256
> 17b75798…5743) and `s2/f200_fxfx_E1500.json` (E 1500, sha256 e28fc947…ea16); the other species–masses have no FxFx
> test, none being required. f200.json is left untouched; T1 will read a scripted `s2/f200_T1_inputs.json` (successor item).

### 4.4 S2-e, S2-f

- S2-e: L1 TDR Table 4.1 p. 210 (50 % at 128 GeV, 90 % at 200 GeV) and Fig. 3.125 p. 188; curve at 0.975 at 250 GeV;
  no uncertainty stated; HLT not sourced [V: EDG l.218-246]. User decision (19 Nov): option (b), threshold 250 GeV
  kept, wide nuisance −10.6 % absolute at 250 GeV (−4.9 % at 275, −1.9 % at 300), recorded as a clarification of the
  frozen branches before A is computed [COM l.366; LOG l.967, l.969].
- S2-f: ⟨δ⟩ at 1 keV +5.68 % (E 200), +6.14 % (E 500), +7.03 % (E 1000), +7.94 % (E 1500); Ẽ 500 +3.60 % uses the
  S-wave form and is not a valid estimate for the P-wave scalar; R-12 **not sourced** → one-sided band (default)
  [V: EDG l.264-280].

### 4.5 P1

On new events (v1's P1 inputs are lost) [SEB l.295-318]. P1-b 5 keV (969 events): +0.00085 ± 0.00051 (1.7σ),
+0.0052 ± 0.0041 for k_B ≥ 6 (1.3σ) → "B\* attribution not supported at 3σ"; 1 keV: ≤ 2σ at all five points →
reading met [V: SEB l.362-377]. P1-c FAIL at 3 of 5 points (E 200 +1.58 %; E 1000 2.6σ; Ẽ 500 +1.96 %, 2.2σ)
[V: SEB l.379-390]. P1-a test 2 (44-bit truncation): KS p 1.6×10⁻⁷ / 2.8×10⁻⁶ → "not the floor pattern"; test 1 not
done ([DT3]) [V: SEB l.392-413]. Diagnostic (not pre-declared): the specification's "44 bits (u′ ≈ 64u)" is
inconsistent (44 bits = 512u); at 64u (rn47) the nominal Δc(20) pattern is not rejected at k = 2.5 (KS p 0.53 / 0.47,
40 events) [V: EDG l.364-401]; recorded beside the verdict by the user's decision, with the correction of the 17 Nov
daily report ("is not excluded at the precision v1 meant (diagnostic)") [COM l.367; LOG l.967].

### 4.6 Retrievals (REF-2) and the MET-model hand-over

R-1, R-2 (L1), R-3, R-7, R-8, R-9, R-12 (not sourced), R-14 (partial), R-15–R-18 closed or reported with their STR §6.4
consequence; open with later deadlines: R-4, R-5, R-6, R-10, R-11, R-13, R-19, R-20 [V: EDG l.433-454]. R-15–R-17:
values but no uncertainties → "no nuisance; μ₉₅ shift of the robustness test reported" [EDG l.28, l.500-503].
MET model (B4-b): sources and four construction options A–D tabulated; the 2013 European-Strategy formula is ×2–4
above both PU-200 full-simulation figures (option D would fail the validation); the non-Gaussian jet-response tail is
**not sourced** in any option; the choice is Phase-3 work [V: SEB l.95-129; EDG l.514-534; LOG l.367-376].

### 4.7 Generator spread ([DP5])

Herwig 7.3.0 against Pythia 8.312 CP5, 10⁶ + 10⁶ events: charged multiplicity ratio 0.946 (|η| < 1), 0.919
(1–1.5); K/π +24 … +34 % at 0.5–2 GeV; p/π +41 … +54 % at 0.7–3 GeV; a generator spread (tunes not equivalent), not
an uncertainty [V: SEB l.441-466; EDG l.405-429].

CPU of channel (ii): 39.5 CPU-h charged of 139 (to 17 Nov) [V: EDG l.41]; FxFx ≈ 4.5 CPU-h on 19 Nov [E: SUN l.231].

## 5. Channel (iii): pilot, T1, toys, half-turn limit, D2

### 5.1 Unit costs and pool

No-pile-up hard-scatter event 127 ms (Z(νν)), 171 ms (W(τν)), 571 ms (tt̄ 1ℓ; 327 ms with forced W decays) against
the 45 ms guess; 132 ms per Z(νν) pilot event over 2.3×10⁶ events (×2.9) [V: TAT l.32-34; LEI l.76]. User decision
16 Nov ("option 1"): the pool keeps 457 + 208 CPU-h and loses events (COM l.44-47); the first pool table given to the
user counted filter-level events as preselected (corrected, LOG l.440-445). Addendum 1 (D1–D9) approved 17 Nov
[COM l.314-324].

### 5.2 Geant4 vertex partition, B1-d, hand-over

1.5×10⁶ pool parents → 245,945 Geant4 vertices in disjoint classes; v1's rates reproduced on Pythia (DIF 1.56,
NI 0.098 per event) [V: TAT l.66-72]. B1-d PASS (83 surfaces, largest difference 4.5×10⁻¹⁰ µm; Fatras hadronic
interactions and π/K decays off) [V: TAT l.50-51]. Hand-over rule per stream (ADD; COM l.344): first-arc streams keep
v1's radius cut (0.00–0.11 % of Geant4 pre-vertex crossings without a hit); DIF-C and NI-C get option (a) (Fatras to
half a turn plus injected Geant4 crossings): 0.04 % / 0.05 % without a hit, 1.5 % duplicates at the seam
[V: A1T l.30-58, l.78-86; A1A l.17-29]. Per-stream validation P7: 9 of 9 streams pass under
`hard_except_early_product_hits` [V: HED l.3-5; LOG l.958].

### 5.3 Pilot

Part 1 (minimum bias + Z(νν)) 500/500 jobs, 94.05 CPU-h; part 2 (B1) 762/762, 46.80 CPU-h; no failed job [V: LOG
l.957; LEI l.39-40]. Z(νν) pilot: 133.2 ms and 33.56 kB per event in the slices [V: PRX l.31-33].

### 5.4 T1-a, T1-b, toys

- T1-b FAIL as frozen on a thin margin (pooled 902.0 ± 31.9 against [710.77, 868.72]; 0 failed fits in 160,000 toys);
  the likelihood agrees with v1 (asymptotic 828.7069 against 828.7067); cause: the b-only median sits on a jump of the
  statistic and the frozen grid with ln-CLs interpolation returns 704–963 from identical inputs [V: FLO l.12-24]. E3:
  PASS as measured; for PREREG_v2 the toy recipe gets "a bracket refinement (bisection to 2 %) and a stated empty-tail
  rule" [COM l.294-296].
- Toys: jax backend, merged auxiliary channels, POI stitched out, warm starts: 30 / 168 / 385 / 817 s per 1000 + 1000
  toys at 31 / 60 / 80 / 100 parameters; programme **47 / 108 / 228 CPU-h** against 183 (factor ≈ 1.6 either way);
  0 failed fits in 25,180 toys; synthetic workspace, to be re-measured on the first real v2 workspace [V: VIK
  l.10-20; E: projection].

### 5.5 Half-turn limit [L15] and the looper gun

Looper gun with full Geant4 trajectories injected as hits, frozen finder: **0 candidates at every rung in 2×10⁵
events** (rerun with the transportation-ended tracks: unchanged, seed-threshold events 33 / 34) [V: LG l.8-23,
l.126-140]. The zero bounds little: one count = 1.9×10⁴ events in 3 ab⁻¹, a zero allows 2.2×10⁴ at 68 %; not covered:
loopers outside ±0.1 of the road, |η| > 1, displaced, or with pile-up [E: LG l.71-83]. Later arcs arrive 2.7–7.1 ns
after the collision (10–90 %), so a one-crossing time window removes none [V: LG l.85-92]. Frozen [L15] text: COM l.341.

### 5.6 D2 robustness row "later arcs restored"

Frozen reading (ADD l.310-321, quoted): "**Effect, 'robust' by the frozen B6-b threshold** (|ln r| ≤ ln 2 at R04–R06,
STR l.1502): if r(R06) > 1 the pile-up estimate is multiplied by r(R06) … no credit is taken for r < 1" (ADD l.316).
Plan committed before any event (564fa1a), not changed [D2R l.3-5].

**Result, in the wording of the advisor ruling (LOG l.991, Olav; binding for this document, [L15] and the paper):**
- 600 development events, 2,400 paired trials: r = 0.766 / 0.759 / 0.720 at R04 / R05 / R06; ln r(R06) = −0.328 ±
  0.061 (paired bootstrap), evaluated at R06 [V: D2R l.27-33; re-read].
- Reading: not "no effect" (|ln r| > 0.1); not "not robust" (max |ln r| 0.328 < ln 2, trend negative). It is
  "**effect, robust**", where "robust" means "below the factor-2 threshold". **No significant trend** (−0.062 ± 0.061).
  r(R06) < 1 → **no correction, no credit**; the day-15 reading is unchanged. No user choice is triggered (the §1.5
  choice is void when nothing is corrected) [LOG l.991 (1)].
- The statement holds at R04–R06, at fixed raw hit density, on 600 development events, with the TDR density assumed;
  it is not a statement that v1 is conservative without these qualifiers. The pile-up term at R08 and beyond stays an
  extrapolation [LOG l.991 (4)]. The inverse 1/r(R06) = 1.39 ± 0.08 is never used as a factor [LOG l.991 (4)].
- Caveat: 55 of the 427 varied R06 groups (12.9 %) are a same-particle-double class that is absent in v1 (2 of
  14,507); a net r < 1 does not show that this class stays subdominant at R07 and beyond [LOG l.991 (4); D2R l.53-57].
- Cost: 15.83 CPU-h measured (plan 12.4–14.5, stop 28); the Geant4-injection chain unit cost is 2.0× the plan and goes
  into any future projection [V: D2R l.102-108; LOG l.991 (4)].
- **[L15] addition** (ruling (2), stated limitation, no measurement): "crossings Geant4 produces before half a turn
  after Fatras stopped (3,133 per event, 10 % of those restored) were not restored; effect not measured" [LOG l.991].

## 6. Rule 1: the PRELIMINARY reading from the pilot

Frozen text (STR l.2754-2757): "If B₅₀ is at most 300 events … production proceeds and the user is informed in
`STATUS.md`. If it is larger, or if both pile-up estimators are above their cap, the outcome class has changed: the
study pauses and the user is asked. The binding B₅₀ is the median of at least 10⁵ draws (precise to about 0.3 %), and
a reading within that precision of 300 counts as larger." The day-7 rider was not taken (COM l.37); the binding
reading is day 15. **The rule-1 B₅₀ is a ceiling, not a background estimate** (STATE l.69).

Reading of the frozen text recorded by the advisor (LOG l.975, Åsa; not an amendment): the frozen count is near-pass
inclusive (H = P_geo + Σ f_k, STR l.760, l.797-798, l.2745; Df-11); (i) the binding m is the subset-pass count of STR
l.755-761; (ii) if that classifier is not reviewed by day 15, the finder near-pass count stands in as a **lower
bound, valid only for an "above" verdict**; a lower-bound reading ≤ 300 is "not shown below" → pause; (iii) B₅₀ is
read at the lowest-G candidate; if G is unavailable, at every T2 candidate, and they must agree.

| count at R08 = R09 (4.7 mm) | m_Z | B₅₀(R09) [16–84 %] | B₅₀(R08), pile-up 88 / 118 / 148 | status | source |
|---|---|---|---|---|---|
| **finder near-pass (k ≤ 3): the stand-in lower bound (ruling (ii))** | **253** | **10,777** [10,130–11,459] | 10,855 / 10,878 / 10,901 | reviewed (Björn: re-derived exactly) | TOV l.17 [V], re-read; BJO l.14-16 |
| finder pass (k = 0) = P_geo alone | 11 | 620 [482–784] | 697 / 721 / 743 | information only (ruling of LOG l.975) | TOV l.16 [V], re-read |
| subset pass (S), primary of the plan | 1,501 | 63,170 [61,578–64,802] | 63,246 / 63,271 / 63,294 | **not yet reviewed** (ruling (ii)); exact or a lower bound | ING l.17 [V], re-read |
| subset pass (F), N_IT2 ≥ 3 required | 1,474 | 62,037 [60,460–63,654] | 62,113 / 62,138 / 62,161 | not yet reviewed | ING l.18 [V] |
| empty pilot (reproduction check) | 0 | 160.8 | 238.3 / 262.3 / 283.8 | — | TOV l.18 [V] |

- **Preliminary reading: above 300 at every T2 candidate with a pile-up estimate** (R09 and R08 at the three pile-up
  values agree to 0.2 % for the subset count, ruling (iii)); with and without the flagged events identical
  [V: ING l.27-33; TOV l.22-25]. The whole excess is the Z(νν) term (it stands for every SM hard-scatter process and the
  multijets); every B1 class, the hard-scatter-parent sample and the low-p_T alarm sample are empty at R08 [V: TOV
  l.10-12, l.46].
- B₅₀ is ESTIMATE as physics (v1 preselection, provisional classification, pile-up term = v1-based EST rows;
  M = 993,887 → 41.96 events per count) [TOV l.20-21, l.51-52].
- N_2S2 ≥ 3 candidates (R14 type, FB): no pile-up estimate in the script, no B₅₀ formed; counts 147 (finder),
  969 (S) / 846 (F) [V: TOV l.81-83; ING l.31-33; BJO l.70].
- After CKF (information only, not rule 1): 0 passes, 17 near-passes at R08 [V: TOV l.57-59].
- Validation before day 15 (rulings (a)–(e)): (a) positive control **no power** as planned; (a2) injection control
  **PASS** (D2 = 0, 350 events ≥ 100); (b) independent review: 253 / 11 re-derived exactly, no discrepancy lowers m_Z by
  more than 0.06 % (weighted m 252.85); (c) subset-pass count above; (d) shortcut power **PASS** (n_lost = 0 on 350);
  (e) ceiling paradox **explained** (v1's 0.0162 counts tagged pile-up, §7) [V: ING l.67-87; BJO l.12-24, l.67].
- Lower-bound items from the review: D1 (finder instead of subset pass) and D2 (N_IT2 ≥ 3 as a veto) raise the frozen
  count by an unmeasured amount; D3 hit merging before the finder is a provisional choice to be frozen; D9: 54 of the
  253 contain a secondary-product hit (without them 199, same verdict) [V: BJO l.62-72].
- CPU: classification 9.3 CPU-h (Tove), validation 4.93 CPU-h (plan 2.8–7.6, stop 10) [V: TOV l.100; ING l.111].

> **PENDING: Nils (Fable, reviewer), second-agent review of `p2w_subset.py` (ruling (ii)).** Until it is read, the
> binding stand-in is the finder near-pass count as a lower bound, m_Z = 253 → B₅₀(R09) = 10,777, valid only for an
> "above" verdict; the subset-pass count 1,501 → 63,170 is not the reading in force. To fill: review verdict, and
> whether the subset count replaces the stand-in.

## 7. Attribution: v1's tag, v1's C′_PU link rule and the frozen rule j ≥ n/2

Frozen attribution (STR l.747-753): "The candidate is **attributed** to that class if j ≥ n/2, **mixed** if 1 ≤ j <
n/2 for every class, and **pure pile-up** if j = 0 … v1 used attributed counts (D4 l.196 [U]); its coded rule is
transcribed in Phase 2 and printed in the pre-registration. C1 uses v1's rule, and the difference is measured on the
C′_PU samples."

- **SM term (Björn):** v1's 0.0162 per event at R06 counts candidates with ≥ 1 hard-scatter hit (`n_hs_band >= 1`,
  v1 `background.py` l.712), i.e. tagged pile-up; on v2's reproduction 92 tagged R06 candidates, **0** attributed by
  j ≥ 4; like-for-like gap ×13 [V: BJO l.100-146]. So "v1 used attributed counts" (STR l.753) is wrong for the SM
  term [BJO l.148-153].
- **C′_PU (Eskil):** frozen j ≥ 4 against v1's link rule: DIF 0/141 (R05), γ 10/174 (one source event), V⁰ 26/612
  (R05); γ 1/11, V⁰ 1/11 (R06); PV pair 0/4 (R04); no j ≥ 4 candidate outside v1's rule; DIF event-level 95 % UL
  < 0.064, γ ≈ 0.22 [V: ESK l.8-18, l.36-50]. 60 % (γ) / 28 % (V⁰) of v1's candidates become "mixed" (no term)
  [V: ESK l.69-75].
- **Advisor ruling (LOG l.978, Dagny):** rule-1 inputs and day-15 text unaffected; the Gate A range (0.7–1.0×10⁴
  attributed background below 243 GeV; B₅₀ 3×10⁴–3×10⁵) rests on the C′_PU conversion counts, not on 0.0162
  (correction of an earlier statement; §12). Eskil's ESTIMATE: attributed conversion term × 0.06–0.09 → ≈ 5–9×10²
  (UL ≈ 2×10³) instead of 0.7–1.0×10⁴; the Gate A range is an upper envelope only [E: ESK l.83-95; LOG l.979].

> **FILLED 2026-11-23 (Kari, 121f78e; `CPU_ATTRIB_NI_kari_2026-11-23.md`).** NI 22 run 25/25 + 25/25, 0 failures, 7.06 CPU-h
> (+ ≤ 0.16 killed by the power loss; stop 9) [VERIFIED]; cpu_attrib.py unchanged, Eskil's DIF/γ/V⁰/PV-pair counts reproduced
> identically, 415,996 hit records, 0 mismatches. Frozen rule vs v1 rule per 1,000 slots: R05 2 / 82, ρ = 0.024
> (16/50/84 % 0 / 0.022 / 0.047; 95 % UL 0.13, ESTIMATE), both passes from one source event; R04 2 / 309, bracket [2, 229]
> only (most R04 candidates lack a hit record); R06 0 / 0 [VERIFIED counts]. v1 rule reproduces v1 (6,918 / 309 / 82 vs
> 7,830 / 254 / 92 at R02 / R04 / R05, within statistics). v1's NI candidates at R05: 85 % pure pile-up, 12 % mixed,
> 2 % attributed. Attributed conversion-led total ≈ 4–9×10² events (UL ≈ 2.2×10³) vs Gate A 0.7–1.0×10⁴ [ESTIMATE];
> NI does not move it; γ (ratio 0.057–0.091, one source event) dominates; Gate A's range is an upper envelope.
> **Strategy-revision input:** the STR §4.4 NI R05 test (sized for 92 / 120 / 378) would hold ≈ 2 at 22 mm (measured),
> ≈ 3 / ≈ 9 at 30 / 61.5 mm (analogy) under the frozen rule: almost no power [ESTIMATE] → re-size in Phase 3 / pause
> package. v1 link rule: g1b_tt.py l.354-355 (v1 commit d724a1c; l.356-357 is a comment) [VERIFIED] (closes §12 item 6).
> Open: more γ source events (no run defined; new plan + approval needed); no NI 30 / 61.5 mm sample.

## 8. Compute, storage and calendar (stop-rule checkpoint 1)

- CPU used by Phase 2: **431.6 CPU-h** (all attempts, 3,135 jobs) plus ≈ 3–5 not in markers; waste 2.56 CPU-h (0.6 %)
  [V: LEI l.47, l.51-55]. Finished Phase-2 items ≈ 150 CPU-h under their lines (C1 −12, C2 −59, P1 −45, FxFx ≈ −32)
  [V: LEI l.61-63].
- **Projection ≈ 4,603 CPU-h, band 4,067–5,046** against 4,609 approved / 5,992 stop-and-ask: no stop rule near
  [E: LEI l.128-130]. Largest band terms: toys (−79 … +257), B4-c (−258 or 0, pending the user) [LEI l.132-139]. No
  single conditional draw crosses 5,992 from the high end; any two of the large ones would [E: LEI l.163-164].
- Storage 266 GB now, ≈ 0.68 TB projected against 1.5 TB budget and 2.0 TB stop [E: LEI l.244-252].
- Calendar: 3.8 days lost to the power loss; projection ≈ 64 days (68 at the measured development utilisation 0.58)
  against 60 approved; reported under D6, not a stop rule [E: LEI l.207, l.220; LOG l.985, l.988]. DECISION notice
  `2026-11-23_1341`: default option C (shift every later date by 4 days, day 15 → Sat 5 Dec; two riders) at Wed
  25 Nov 12:00.
- Utilisation before the outage 0.63 (slot) / 0.58 (CPU) against 0.50 assumed; one full-queue day at 0.82 CPU
  [V: LEI l.187-193].

> **DECIDED 2026-11-23 (orchestrator, advisor Runa; LOG.md 2026-11-23): Z(νν) top-up (addendum D8) NOT drawn.** The top-up
> exists only to keep an R08 candidate from pausing on 1–3 counts (ADD l.109). First counts at R08 = R09: 253 (finder,
> lower bound) to 1,501 (subset pass, under review) [VERIFIED, ING §1], i.e. B₅₀ 10,777–63,170 events against a
> pause level of 299.1 (≈ 7 counts at ≈ 42 events per count); a 1.5× or 2.3× larger sample changes the events per count,
> not the side of 300. 0 CPU-h spent (+45 / +109 if drawn). Reopens (as a user decision, a launch needs approval) only if a
> revised count at any T2 candidate falls to ≈ 10 counts or fewer; a FAIL of the subset review does not reopen it (the
> finder lower bound alone is above by a factor 36). R14-type candidates (969 / 147 counts vs a pause level of 4) do not
> reopen it. The user was told in the daily report of 23 Nov and may still ask for it.

## 9. Strategy-revision inputs

Form: Phase 1 assumed / Phase 2 found / Implications. Items 1–6 are the advisor's list of 19 Nov (Dagny; STATE l.65,
LOG l.977-979); items 7 onward are from the channel files.

1. **v1 SM counts are one-hit tags, not attributed.** Assumed: "v1 used attributed counts" (STR l.753). Found: v1's SM
   term counts candidates with ≥ 1 hard-scatter hit; 0 of 92 tagged R06 candidates are attributed by j ≥ 4 (BJO
   l.122-127). Implications: STR l.753 is wrong for the SM term; the C1 SM row label "hard-scatter" becomes "tagged"
   (criterion unaffected); SM ceiling tests (STR l.803-811) are already "attributed" and pass with ≈ no power (quote
   it) [LOG l.978].
2. **Void planning numbers.** STR l.791-797; Table 4.4c m_H rows (STR l.970-976); the B5 hard-scatter share 10/8/6 %
   (STR l.1420); and, from the C′_PU measurement, DIF 31 at R06 and H(R06) ≥ 0.004 (STR l.1048-1051), so the DIF R06
   ceiling test has ≈ no power [LOG l.978-979; ESK l.97-103].
3. **B4-c and B5 closures NOT EVALUABLE on SM samples.** B4-c (STR l.1374-1381, +258 CPU-h sized on tagged counts)
   and the B5 timing closure (STR l.1272-1273) cannot be evaluated on the SM samples under the frozen attribution →
   user question in the day-15 pause package (accept NOT TESTED, or amend; an amendment would come after a development
   result) [LOG l.978].
4. **Hold the row-20 extra events** (STR l.2116) until the user answers item 3 [LOG l.978].
5. **Attributed vs C′_PU-linked** (STR l.753-754): measured for DIF, γ, V⁰, PV pair (§7); NI PENDING (Kari). Gate A's
   range carries over only as an upper envelope [ESK l.88-95].
6. **Rule-1 reading clarifications (i)–(iii)** of the frozen text (LOG l.975, Åsa), §6.
7. **Half-turn limit [L15].** Assumed: the chain simulates curling particles (v1 plan l.1267). Found: no hit beyond half
   a turn; 21 % (Z(νν)) / 29 % (minimum bias) of the true crossings occur after half a turn. Implications: a named
   topology (repeated crossings by one looper) is absent from every v1 and v2 sample; the pile-up hit pattern lacks
   about a third of its correlated hits; v1's looper zero measured nothing; D2 measured its effect on the pile-up count
   at R04–R06 (§5.6) [HT l.9-23; LOG l.567-570].
8. **Unit costs and preselection.** Assumed 45 ms per no-pile-up hard-scatter event and preselected generated events.
   Found 127–571 ms and mean preselection weights 0.12–0.43. Implications: pool at fixed CPU with higher floors (user
   option 1); 41 events per Z(νν) pilot count instead of 18 [TAT l.97-102].
9. **Single-interaction vertices.** Assumed DIF and NI at three radii (6.8×10⁷ vertices). Found 3.66×10⁸ when every
   Geant4 class is counted, no factor 0.22 in the generation. Implications: seven B1 terms (addendum D4) [TAT l.103-105;
   PDM l.57-66; COM l.344].
10. **Hand-over.** Assumed Fatras takes every Geant4 product at the vertex. Found it cannot (slow fragments); the
    after-a-turn parents need injected Geant4 crossings. Implications: hand-over per stream; flagged-event rule (D9)
    [TAT l.106-107; A1A l.8-15].
11. **C2-a and C2-c tests without the power assumed.** V4-5 score optimum is another plane at pile-up 200; T_seed pass
    fractions saturate at 0 or 1 [V45 l.37-46; C2V l.54-60].
12. **T1 toy recipe.** Found: the frozen grid with ln-CLs interpolation is unstable at the b-only jump → bracket
    refinement and empty-tail rule (COM l.295-296) [FLO l.21-34].
13. **Toy cost.** Assumed "may double" at 60–100 parameters; found ×17 at 60 with numpy; remedy (jax) brings the
    programme to 47 / 108 / 228 CPU-h [TAT l.108-109; VIK l.10-16].
14. **MET model (B4-b).** Assumed a public soft-term parametrisation validated against an independent PU-200 figure.
    Found the 2013 formula ×2–4 above both PU-200 figures; options A–C exist with the CMS note; jet-response tail not
    sourced [EDG l.463-469].
15. **P1 on new events; floor-test specification** (44 bits ≠ 64u) [EDG l.470-480].
16. **S2-e** (no stated uncertainty; decided), **S2-b** (no NLO column in the public tables), **S2-f** (largest
    single theory band below ≈ 700 GeV), **published K-factors** (2404.13814: K = 1.33 / 1.45 at 13 TeV, settings not
    stated; ours 1.163 / 1.178), **B6-d** (no uncertainties for R-15–R-17), **unit costs** of S2 [EDG l.481-512].
17. **Closure slope weights** (C1 FLAG 1) [MAT l.127-146; RAG l.50-54].

> **FILLED 2026-11-23 (Tora 610c107; advisor Ulla, LOG 23 Nov; RESULT notice 16:38).** Gate A's strategy_budget.py re-run
> unchanged (reproduces Gate A exactly [VERIFIED]), backgrounds only; all ESTIMATE on v1 placeholder efficiencies (high by
> 1/0.87). Gate A envelope B₅₀ 6.8–10.2×10³ → reach < 243 GeV (stays the upper envelope). Attributed-only (optimistic
> edge, lower bound on background; mixed 60 % in no term; SM after-CKF 0): B₅₀ 418–916 → reach 351–444 GeV. SM after-CKF
> bracket 0 to ≥ 17; at 17: 277–296 GeV. Attributed UL (ρ_γ 0.22) + own-hit 11: < 243–266 GeV. ρ_γ rests on one source
> event (0–0.12 at 68 %, UL 0.22). If ≳ 10–20 % of the mixed candidates survive, the reach is back below ≈ 250 GeV.
> **Reach outlook vs Gate A: more promising, weakly; not established.** Sensitivity to the surviving mixed fraction:
> Tora's erratum (pending). The day-15 rule-1 ceiling (≈ 10,800 events) is a separate quantity; the pause stays expected.

> **PENDING: Phase-3 inputs, the MET model and the final pilot classification (day 12 = 28 Nov as scheduled; +4 days
> under the pending calendar option C).** The MET-model construction choice (options A–C of §4.6, tail width set
> without a source and labelled) and the final classification of the pilot (subset pass, hit merging, PV choice, flagged
> events variant, G / best candidate) feed the binding day-15 reading. "41 per count" is provisional until the MET model
> (TOV l.86). To fill: the chosen construction and its validation result; the final m per term.

## 10. Open items for PREREG_v2 and the day-15 pause package

**For the pause package (questions to the user):**
1. **B4-c and B5 closures NOT EVALUABLE on SM samples** (§9 item 3): accept NOT TESTED or amend. State with it that
   an amended, evaluable B4-c on **attributed** counts would need ≈ **4,800 CPU-h** [E, rough: 52,792 events × 13 ×
   25.2 s; LEI l.167-171], which crosses the 5,992 CPU-h stop-and-ask threshold on its own. Row-20 extra events held
   until then.
2. **C1-c NOT TESTED** pending the user's docker-build decision (notice `2026-11-19_1119_DECISION`, no default;
   deadline Phase 5 review); E5 (content comparison) to be amended before any rerun [LOG l.970-971].
3. The binding rule-1 reading and the expected pause (Gate A Q2 (a)); calendar per the pending DECISION (option C:
   day 15 at the latest Sat 5 Dec, the user says whether the pause is answered on 5–6 Dec or Mon 7 Dec).

**For PREREG_v2 (fixed before the freeze):**
4. **Ingvild's readings S1–S5** of text the strategy does not fix (subset-pass classifier `p2w_subset.py`; CEC
   l.38-54; ING l.119): S1 plane and membership = the finder's own refit kernel; S2 every pair of road hits on two IP
   layers seeds a plane; S3 "width of r" = the rung variable w_core maximised over subsets, no hard window; S4 subset
   search inside a plane (witness search, count exact or a lower bound); S5 N_IT2 ≥ 3 inside k_IP (S, primary) with
   (F) as cross-check.
5. **D2 / [L15] additions** (LOG l.991): the [L15] sentence of §5.6; the measured size r(R06) = 0.720, ln r = −0.328 ±
   0.061 with the qualifiers (R04–R06, fixed raw density, 600 development events, TDR density assumed); the
   same-particle-double caveat (12.9 % of varied R06 groups); the 2.0× unit cost of the Geant4-injection chain for any
   projection.
6. Flagged-event definition (n_early_prod > 0 at β_min 0.1), the binding variant per B1 term and for day 15
   (recommended WITH, WITHOUT as cross-check), what a with/without difference triggers (size is the user's), per-stream
   rates and the hs count (38 flagged in 2.00×10⁶) [LOG l.934, l.959].
7. Error model of C1-type comparisons (E4, remediation 1 of 3) [COM l.308-309].
8. Closure-slope fit: fixed trend weights, or an unweighted or covariance fit, with the width including its weight
   dependence [MAT l.145-146; RAG l.53-54].
9. T1 toy recipe: bracket refinement (bisection to 2 %) and empty-tail rule; ties compared within 10⁻⁵ [COM l.295-296,
   l.356].
10. Provisional pilot choices to be frozen: hit merging before the finder, PV for Z(νν), M of the Z term (measured
    993,887 vs planned 1.011×10⁶), the best-candidate (G) rule and a pile-up estimate for the N_2S2 ≥ 3 candidates
    [TOV l.75-88; BJO l.66].
11. S2-e (b) −10.6 % and the P1 diagnostic line (user decisions of 19 Nov) [COM l.366-367].
12. C2-c reporting form (mean passing sets with its paired error) and the C2-a failed-scan statement [C2V l.58-60;
    V45R l.59-62].
13. Runner pre-flight: per-job `NUMBA_CACHE_DIR` (or no cache) for numba campaigns [LOG l.989].
14. Phase-3 sizing uses attributed rates only (§7, §9 items 1–5); NI after Kari's result.

## 11. PENDING blocks (summary)

| # | who | what | section |
|---|---|---|---|
| 1 | Halvard | FxFx E 1500 first launch and f₂₀₀^FxFx at E 1500 — FILLED 23 Nov | §4.3 |
| 2 | Kari | NI C′_PU attributed vs C′_PU-linked — FILLED 23 Nov | §7 |
| 3 | Nils | review of `p2w_subset.py` (ruling (ii)) | §6 |
| 4 | Tora (Opus) | reach re-estimate — FILLED 23 Nov (erratum + mixed-fraction table pending) | §9 |
| 5 | orchestrator | D8 Z(νν) top-up decision — DECIDED 23 Nov: not drawn | §8 |
| 6 | Phase 3 | MET model and final pilot classification | §9 |

## 12. Disagreements between documents on a number (listed, not resolved)

1. **D2 mismatch events:** Ulrika's log 8 events, Jonas 9 events with a ±1-hit nominal mismatch (D2R l.80-81).
2. **D2 wording/number:** D2R l.16 ("conservative"), l.113-114 ("1.39×") and DAILY_NOTES l.71 ("nominal/varied
   1.39") against the binding ruling LOG l.991 (4) ("1/r(R06) = 1.39 ± 0.08 is never a factor"; no "conservative"
   without qualifiers). This document follows the ruling.
3. **D2 same-particle-double share:** 55 of 427 varied R06 groups (12.9 %, LOG l.991) and 62 of 446 hit-recorded R06
   candidates (13.9 %, D2R l.55): two denominators for one finding.
4. **Basis of the Gate A range:** BJO l.155-157 (planning estimates and the Gate A range built on 0.0162) against
   LOG l.978 (Gate A range rests on the C′_PU conversion counts; recorded there as a correction of BJO §4.3).
5. **M of the Z term:** 993,887.3 (TOV l.51, weights rounded to 4 decimals) against 993,885.9 (BJO l.47); 1.4×10⁻⁶.
6. **Line of v1's C′_PU link rule:** STR cites `g1b_tt.py` l.356-357; ESK l.117 and LOG l.979 find l.354-355.
7. **C1 CPU:** 186.2 CPU-h (MAT l.162) against 186.3 (LEI l.31); counting conventions differ (last line vs all
   attempts).
8. **Pilot classification CPU:** 9.3 CPU-h (TOV l.100, incl. ≈ 0.07 outside the ledger) against 9.14 (LEI l.42).
9. **Flagged slow-fragment events:** "of order 10²" (B1R l.77) and "about 170" (16 Nov 20:28 notice, LOG l.934)
   against 318 measured (HED l.100); B1R said none in ni22/30/61, nic, lowpt, measured in all NI classes (LOG l.934).
   Ruled by the advisor (Isolde): D9 stands.
10. **SM bootstrap width at R04:** 0.0522 (SMF l.29) against 0.0505 (regression ticket), explained in SMF l.56-57 as
    seed and script spread.
11. **Outage facts:** "about 4 working days" (notice `2026-11-23_1329_PROBLEM` l.21; LOG l.984) corrected to 3.8
    calendar days (LOG l.985); hostname resolution "unknown whether this predates the outage" (notice l.19; LEI l.195-196
    "multi-node drivers therefore run from einstein") against LOG l.987 (never configured; fixed; driver back on
    maxwell).
12. Superseded within one channel, kept for the record: C1-b PASS on the partial ladder (ROS l.86-99) vs FAIL as
    frozen on the full ladder (ROS l.130-144); T1-b "no verdict" (TAT l.55, l.58-64) vs FAIL as frozen (FLO l.12);
    the f₂₀₀ stitch excess 1.118 on 20k (ROS l.76; EDG l.187-207) vs 1.0001 on 120k (STI l.22); Tatiana's pool table
    (COSTS_POOL, floor 41.7 / 36.0) superseded by the addendum (LOG l.440-445).

## 13. Self-review (JFC Phase-2 tier: self-review + plot validator)

Rules applied: `methodology/03-phases.md` l.268-354, `methodology/06-review.md` l.164-169, `phase2_exploration/CLAUDE.md`,
`tools/jfc/src/agents/plot_validator.md`, with the study overrides of `CLAUDE.md` (simulation only, no RAG corpus,
blinding by BL-1) taking precedence.

| JFC check | status here |
|---|---|
| Sample inventory complete, with schema and event counts | §1 (schemas by pointer to the channel files and the producing scripts' docstrings) |
| Data quality: pathologies, outliers, unphysical values | §2; the open ones: Fatras step limit (unquantified), half-turn limit ([L15]) |
| Data archaeology: weights and flags | §2 (preselection weights, MLM w = 0 rows, FxFx negative weights, `n_early_prod` flag) |
| Data archaeology: processing applied / pre-selection | §2 (generator-level filter MET > 200 GeV; v1 preselection weights; generator cut 150 GeV not fully efficient) |
| Data archaeology: MC generation parameters | §1, §4 (generator, tune CP5, PDF, √s = 14 TeV, cards); Herwig spread §4.7 |
| Data archaeology: truth level | pilot files store truth MET, ν, τ, hadron list, Geant4 vertices and crossings (§1) |
| Strategy-revision gate | §9, 17 items in the required form |
| Object definitions from the corpus | not applicable: no corpus (study override); public sources via `retrieval_log.md` (#11–#31) |
| Data/MC agreement; variable survey and ranking; baseline yields after preselection | not applicable: no collider data; signal-dependent selection quantities are not formed before the closure verdicts (blinding, COM BL-1). Generator-vs-generator and code-vs-code comparisons stand in (§4) |
| Plots and plot validator | **no figure is referenced** and none exists for Phase 2 (`outputs/figures/` empty). `conventions/lint_plots.py phase2_exploration` run on einstein: "No plotting scripts found". No new figure added |
| PDF build test (`pixi run build-pdf` stub) | **not run**: this session is einstein-only and pixi may solve there (AGENT_RULES); open item for the orchestrator on a worker |
| Experiment log | channel entries exist in `experiment_log.md`; my judgment call (tag convention) is in my session log and appended to `experiment_log.md` |
| Numbers tagged, sources cited, nothing from memory | every number carries a tag and a file:line; ten values re-read from the JSONs (session log) |
| Blinding | no signal file opened; no v2 signal efficiency stated; sealed tier PASS/FAIL only |
| Frozen criteria quoted, amendments cited | §0.1, §3–§6 quote COM/STR/ADD; E1–E4 cited as amendments made after the results |

Self-review findings (no Category A by my reading): (1) the inventory gives schemas by pointer, not in full; (2) the
PDF build test is outstanding; (3) six PENDING blocks keep Phase 2 open.
