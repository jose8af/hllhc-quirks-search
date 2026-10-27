# theory_track/data — moved to an external drive (2026-10-18)

The user moved `theory_track/data/` (46 GB, 20,385 files + 4,582 relative symlinks) from the Mac to an external drive
to free disk space. Nothing else in the project moved: code, `sim/`, `acts/`, `analytic/`, `stage5/`, `figures/`,
`report/` and `paper/` (incl. `quirks_p1p2_note.pdf`, v0.4) stay on the Mac.

External drive / path: ____________________ (fill in)

## What it held (sizes on 2026-10-18)
| subdir | size | content | regenerable? |
|---|---|---|---|
| `acts_stage4/` | 39 GB | Stage 4 ACTS production at PU 200 (2,295 jobs, ≈ 382 CPU-h) | only by rerunning Stage 4 (~1 day) |
| `sim/` | 5.4 GB | Stage 2 MadGraph+Pythia samples (2.41 M events) | yes, `../sim/scripts/produce.py`, ~35 CPU-h |
| `sim_stage3/` | 1.1 GB | Stage 3 truth propagation (218,571 events, Mac + PC) | only by rerunning Stage 3 (~583 CPU-h) |
| `stage1_numerics/` | 379 MB | Stage 1 blind numerics (c, G, K, b_odd) | yes, Stage 1 scripts (cost not recorded) |
| `tdr_geometry/` | 191 MB | public CMS Phase-2 TDR / tkLayout D111 geometry, beam-spot sources | re-download |
| `cache/` | 166 MB | `T2_kinematics_cache.npz` | yes, `code/T2_kinematics.py` |
| `pdf/`, `athena_quirks_snapshot/`, `README.md` | ~1 MB | CT18NLO grid, Athena quirk code snapshot, index | re-download |

Full index of the directory: `DATA_README_snapshot.md` (copy of `data/README.md`, which travels with the data).

## Consequences while the drive is unplugged
- About 200 scripts read `data/…` by relative path. Re-running any stage, regenerating figures from raw outputs, or
  re-checking a number from the production files fails until the data is back.
- Already-built outputs remain readable: the paper and its figures, stage reports, `results/*.json` summaries,
  `stage5/` figures, and the talk deck.

## Restoring
Either copy the directory back to `theory_track/data/`, or point a symlink at the drive (scripts use relative paths):

    ln -s "/Volumes/<DRIVE>/<path>/data" theory_track/data

## Notes for the move
- `sim_stage3/canon/` and others contain **relative symlinks**. exFAT/FAT32 drives cannot store symlinks, so use an
  APFS or Mac OS Extended drive, or move a tar archive (`tar -cf data.tar data`).
- Copy with `rsync -a` (preserves links and times). Before deleting the original, compare file counts (20,385 files +
  4,582 links) and sizes; `STAGE3_INDEX.json` lists md5 checksums for the Stage 3 chunks.

## How it was moved (plan, 2026-10-18)
Compression does not help: the bulk is NumPy `.npz` files that are already zip-compressed (zstd test on samples from
`acts_stage4/prod`, `p2`, `sim/npz`: 99–100 % of original size). Biggest folders: `acts_stage4/prod` 36 GB,
`sim` 5.4 GB. All 4,582 symlinks are in `sim_stage3/canon/` (a symlink view of `sim_stage3/out*`, rebuilt from
`STAGE3_INDEX.json` by `../sim/stage3/scripts/merge_index.py`).

The route is Mac → 32 GB USB stick → Windows PC → 1 TB NTFS drive, so the data goes as one uncompressed tar split into
3.9 GB parts. That size fits FAT32, and the tar keeps the symlinks. Run from `theory_track/` (the Mac had 73 GB free):

    mkdir -p ~/quirks_data_parts
    tar -cf - data | split -b 3900m - ~/quirks_data_parts/quirks_data.tar.part_
    cd ~/quirks_data_parts && shasum -a 256 quirks_data.tar.part_* > SHA256SUMS.txt
    cat quirks_data.tar.part_* | tar -tf - | wc -l     # entry count (files + links + dirs)

Move ~7 parts per USB trip. On Windows, check each part against SHA256SUMS.txt with
`Get-FileHash <part> -Algorithm SHA256`. Delete `data/` and the parts only after every part on the 1 TB drive matches.

Restore: copy the parts and SHA256SUMS.txt back into one folder on the Mac, then

    shasum -a 256 -c SHA256SUMS.txt
    cd <project>/stage2_C001_quirks/theory_track && cat <folder>/quirks_data.tar.part_* | tar -xf -
