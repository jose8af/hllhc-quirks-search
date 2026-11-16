#!/usr/bin/env bash
# Notify the user by a NEW FILE committed and pushed on v2-jfc (user instruction of 2026-11-16, second form:
# "commit and push in the same fashion of the daily reports ... if I see a file that was not there then I know
# something happened"). The earlier empty-commit-on-main form is dropped.
# Usage: tools/notify/notify.sh <DECISION|RESULT|PROBLEM|INFO> "<subject>" <body-file(markdown)>
# Writes analyses/quirks_v2/notices/<YYYY-MM-DD_HHMM>_<KIND>_<slug>.md, commits ONLY that file, pushes v2-jfc.
# Never force; no other branch.
set -euo pipefail
kind="$1"; subject="$2"; body="$3"
case "$kind" in DECISION|RESULT|PROBLEM|INFO) ;; *) echo "bad kind" >&2; exit 2;; esac
cd "$(git rev-parse --show-toplevel)"
[ "$(git rev-parse --abbrev-ref HEAD)" = "v2-jfc" ] || { echo "not on v2-jfc" >&2; exit 3; }
slug="$(printf '%s' "$subject" | tr 'A-Z' 'a-z' | tr -c 'a-z0-9' '-' | sed 's/--*/-/g;s/^-//;s/-$//' | cut -c1-48)"
f="analyses/quirks_v2/notices/$(date '+%Y-%m-%d_%H%M')_${kind}_${slug}.md"
mkdir -p "$(dirname "$f")"
{
  echo "# [$kind] $subject"
  echo
  echo "Written $(date '+%Y-%m-%d %H:%M %z') by the orchestrator. Current status: \`analyses/quirks_v2/STATUS.md\`."
  echo
  cat "$body"
} > "$f"
git add "$f"
git commit -q -m "notice($kind): $subject

Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>" -- "$f"
for try in 1 2 3; do
  if timeout 120 git push -q origin v2-jfc; then echo "notice pushed: $f"; exit 0; fi
  timeout 60 git fetch -q origin && git merge -q --no-edit origin/v2-jfc || true
  sleep 5
done
echo "ERROR: push failed; notice committed locally at $f" >&2; exit 1
