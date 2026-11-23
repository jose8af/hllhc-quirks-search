# [PROBLEM] Power loss Thu 19 Nov 17:54 to Mon 13:00: no work ran, now resumed

Written 2026-11-23 13:29 -0500 by the orchestrator. Current status: `analyses/quirks_v2/STATUS.md`.

Written 2026-11-23 by the orchestrator (new session).

**What happened.** einstein and the workers lost power at about **17:54 on Thursday 19 Nov**. There was no clean shutdown. einstein and landau stayed off until today, 12:57. maxwell and schrodinger restarted at about 17:55 on Thursday but could not mount the home directory while einstein was off. The orchestrator session, its timers and its four agents (Sune, Cecilie, Eskil, Ulrika) died with einstein. **No work ran from Thursday 17:55 until today 13:25**, and nothing could send a notice or a daily report. There are no reports for 20–22 Nov.

**Damage check (all verified).**
- Repository intact (`git fsck` clean). 21 commits from Thursday afternoon had not been pushed; they are pushed with this notice.
- No truncated or partial files on the storage pool.
- **9 jobs were killed mid-run**: FxFx E1500 grids3 (at 35 min, no result), D2 find 2, rule-1 validation 4, NI C′_PU 2. None left an output.
- Recovery snapshot of the working tree: commit `087d653`.

**Resumed at 13:25 today.** All six interrupted campaigns are running again. The runner marked the 9 killed jobs "lost" and retried them.
- FxFx E1500 now runs as job `grids4`: the retry of `grids3` stopped on a stale MadGraph run name. This is still the one 7,200 s job you approved on 19 Nov; no attempt had produced a result.
- Report and heartbeat timers are re-created.

**Cluster issue for the admin (not repaired by me).** None of the workers can resolve another worker's hostname (`ssh landau` from maxwell: "Could not resolve hostname"). Only einstein knows the names. Work continues: drivers that span nodes now run on einstein. I don't know whether this predates the outage.

**Schedule.** About 4 working days were lost. Day 5 (decision point 1, compute checkpoint 1) is overdue. Whether to shift the calendar, including the day-15 binding reading on 1 Dec, comes to you in a separate DECISION notice after an advisor check.

**If this happens again:** the timers live inside the session on einstein. If no daily-report commit appears by about 19:30, assume einstein or the session is down.
