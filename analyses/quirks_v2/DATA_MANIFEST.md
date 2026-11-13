# Data manifest — `/nfs/cajuela/jdochoa/quirks_v2/`

Source of truth for what exists on cajuela. Sizes come from campaign manifests and markers, never from `du` over NFS.
Tiers: `final` (kept), `regenerable` (deleted after downstream verification, deletion logged in `LOG.md`), `scratch`.
Budget: soft 1.5 TB; stop and ask before 2.0 TB or if pool free space would fall below 1.0 TB.

| campaign | path under `data/` | size | files | manifest sha256 | tier | regenerate with |
|---|---|---|---|---|---|---|
| (none yet) | | | | | | |

Other areas: `logs/` (per-job logs; preflight probes only, < 1 kB), `backup/` (repo bundles, listed in `STATUS.md`).

Project total on cajuela: 0 GB of data (2026-11-13). Pool free space: 3.9 TB of 4.5 TB.
