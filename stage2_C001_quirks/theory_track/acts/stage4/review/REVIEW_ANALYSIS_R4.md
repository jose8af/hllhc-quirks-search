# REVIEW_ANALYSIS_R4: narrow verification of the R4 delta (FIX_ANALYSIS_R3.txt, "DELTA R4")

| Field | Value |
|---|---|
| Date | 2026-10-14 |
| Reviewer | fresh narrow verifier (critical_reviewer.md, 03-review.md) |
| Scope | Only R3 B-1 and B-2, the re-freeze, the selftest, and any breakage caused by the R4 changes |
| Not examined | Signal ε and acceptance values |
| Verdict | **FAIL: 0 A, 1 B (new, a regression from the R4 change), 2 C** |
| R3 findings | R3 B-1 and R3 B-2 are both RESOLVED |

## Checks run

All checks ran under `nice -n 15`, one process each, in about 1 minute or less. The probe scripts are in the
scratchpad under `r4v/`.

- **Freeze.** `analysis_freeze.json` has sha256 `b11cdf553dbe…4b89`, matching the stated `b11cdf55…`. All 30 listed files
  re-hash to their frozen sha256, with 0 mismatches.
- **Selftest.** `python -m acts.stage4.analysis.selftest` reports SELFTEST PASS, and `freeze` is true. These tests
  pass:
  - `R3B1_repro_refused`
  - `R3B1_repro_complete_refused`
  - `R3B1_repro_dev_stamped`
  - `R3B1_stamped_frozen_nondev`
  - `R3B1_products_refused`
- **The reviewer's exact reproduction** (`r3/b2_probe2.py`, run unchanged). Both cases are now refused:
  - **Incomplete B sum:** REFUSED (B-8), because the upstream `signal_eff.json` and `bsum_wp.json` have no embedded
    provenance stamp.
  - **`complete_inputs` forced to true:** REFUSED for the same reason, and no `limits.json` is written.
  - **Still true:** the manifest is rewritten to `dev: false`. It no longer matters, because the check reads the stamps
    embedded in the consumed files.
- **Independent variants** (`r4v/probe_r4.py`). Every case uses a frozen `--stages limits` or `products` without `--dev`
  on the same output directory:

| Case | Result |
|---|---|
| `signal_eff.json` stamped DEV | refused |
| `bsum_wp.json` stamped DEV | refused |
| `bsum_wp.json` produced under another freeze sha | refused ("another freeze") |
| stale unstamped `signal_srt.json` | refused |
| `background.json` stamped DEV | refused |
| DEV-stamped `signal_eff.json` with `--dev` | `limits.json` written with `dev: true`, a DEV label, and `provenance.dev: true` |
| products: `signal_eff.json` stamped DEV | refused |
| products: `signal_rows_a2.npz` stamped DEV | refused |
| products: `signal_rows_a2.npz` with no stamp | refused |

- **Stamping by the producing stages** (code read, `run_all.py`). Each output gets the same stamp,
  `C.provenance(a.dev, freeze.match)`:
  - `signal_eff.json` (l.353) and the `signal_rows/obs_*.npz` files (l.340, l.345);
  - `background.json` (l.426), `srt.json` (l.456) and `signal_srt.json` (l.102);
  - `bsum_wp.json` (l.468) and `limits.json` (l.186).
- **Consumers.**
  - `limits_stage` checks `signal_eff`, `bsum_wp`, `background` and `signal_srt`.
  - The products stage checks `signal_eff` and every `signal_rows/obs` npz for a1, a2 and a5.
  - Without `--dev`, either consumer refuses when an issue is found. With `--dev`, the output is marked DEV.

## Category A

None.

## Category B

### B-1 (NEW; a regression from the R4 B-1 fix): the products stage crashes on any stamped `signal_rows_*.npz`, so a default full run never reaches `limits`

**Cause.** R4 adds the key `provenance` to `signal_rows_{kind}.npz` (`run_all.py` l.340). `products.edges` (l.112)
builds its point keys from every key in `z.files`:
`keys = sorted({k.rsplit('|', 1)[0] for k in z.files})`. The key `provenance` therefore becomes a "point", and
`smp, spin, m, lam, cfg = key.split('|')` raises an error.

**Demonstrated** (`r4v/edges_probe.py`). An npz written the way l.340 writes it has the keys
`['provenance', 'A2|F|1000|1|BM|L', 'A2|F|1000|1|BM|rows']`:
- with the `provenance` key, `PD.edges` fails with `ValueError: not enough values to unpack (expected 5, got 1)`;
- with the same arrays minus `provenance`, it succeeds.

**Impact.**
- In the frozen production path, every `signal_rows` file is stamped, so `edges_det.json` is never produced.
- The default `--stages` is `signal,background,srt,wp,products,limits`, and products runs before limits (l.470 before
  l.497). A one-shot production run therefore stops with an exception before `limits.json` and the final manifest are
  written. That costs a second launch under the 2026-10-17 deadline.
- No wrong number is produced, so this is not category A.
- The selftest covers only the products refusal path. It never runs the positive path, which is why the error was not
  caught.

**Other npz consumers are not affected.** `sep_it_det`, `event_display` and `signal_srt_stage` read explicit keys.

**Fix (one line).**
- Filter the keys in `edges`: `{k.rsplit('|', 1)[0] for k in z.files if k.count('|') == 5}`, or skip
  `k == 'provenance'`.
- Add a selftest that runs `PD.edges` on a stamped npz, or runs the products positive path on a minimal stamped
  fixture.
- Then re-freeze, because `products.py` is a frozen file.

## Category C

- **C-1: the T_seed guard still trusts the rewritten manifest.**
  - `limits_stage` still reads `t_seed` from `sig_dir/manifest.json` and `bkg_dir/manifest.json`. With the default
    directories, that is the manifest the current run has just rewritten.
  - The embedded stamp records `dev`, the freeze and the time, but not `t_seed` or the campaigns.
  - **The case that slips through:** a stale `bsum_wp.json` from a non-`--dev` G3 dry run (T_seed 6) in the same
    directory would pass the T_seed check.
  - **Why it is only C:** dry-run B sums have `complete_inputs = false`, so a run without `--dev` refuses anyway, and
    with `--dev` the output is DEV.
  - **Suggestion:** add `t_seed` and the campaigns to `C.provenance` and compare those instead.
- **C-2: R3 B-2 is fixed as stated.** `products.acceptance` now loops over `('a2',)` only.
  - The `finder_note` now states the A2 denominator correctly: template half, `in_eta25`, status ≠ 1 counted as
    failures. That is the same set of events as A.
  - The note says explicitly that A1 and A5 are not paired.
  - Only the code and the note text were checked. No values were looked at.

## Disposition of the R3 findings

| R3 finding | Status | Evidence |
|---|---|---|
| B-1 (default same-directory provenance, for limits and products) | **RESOLVED** | The exact reproduction is refused, and 9 independent variants are refused or stamped DEV as expected. A frozen run without `--dev` can no longer launder DEV or unstamped upstream files. |
| B-2 (acceptance pairs A with mismatched-denominator A1/A5 ε) | **RESOLVED** | Only A2 is paired with A, and the note is corrected. |
| Freeze (30 files, `b11cdf55…`) and selftest | **PASS** | Independent re-hash: 0 mismatches. Selftest PASS. |

## Verdict

**FAIL** on one new B.

- The R4 fix of B-1 is correct, but stamping the npz files broke `products.edges`.
- The fix is a one-line key filter, a positive-path selftest and a re-freeze.
- A verifier round after that can be limited to that patch.
