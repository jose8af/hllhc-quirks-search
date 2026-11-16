#!/usr/bin/env bash
# Notify the user by an EMPTY commit on origin/main (user instruction of 2026-11-16).
# The commit message carries the information; the working tree and the current branch are not touched.
# Usage: tools/notify/notify.sh <DECISION|RESULT|PROBLEM|INFO> "<subject>" <body-file>
# Rules: fast-forward only, never force; no checkout (agents work in the tree); also pushes v2-jfc so that the
# files the message points to are readable from outside the network.
set -euo pipefail
kind="$1"; subject="$2"; body="$3"
case "$kind" in DECISION|RESULT|PROBLEM|INFO) ;; *) echo "bad kind" >&2; exit 2;; esac
cd "$(git rev-parse --show-toplevel)"
msg="$(mktemp -p /var/tmp/jdochoa notify.XXXXXX)"
{
  echo "[quirks-v2][$kind] $subject"
  echo
  cat "$body"
  echo
  echo "Sent: $(date '+%Y-%m-%d %H:%M %z'). Work branch: v2-jfc at $(git rev-parse --short v2-jfc)."
  echo "Status file: analyses/quirks_v2/STATUS.md (branch v2-jfc)."
  echo
  echo "Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>"
} > "$msg"
timeout 120 git push -q origin v2-jfc || echo "WARN: push of v2-jfc failed" >&2
for try in 1 2 3; do
  timeout 60 git fetch -q origin main
  parent="$(git rev-parse origin/main)"
  commit="$(git commit-tree "${parent}^{tree}" -p "$parent" -F "$msg")"
  if timeout 60 git push -q origin "$commit:refs/heads/main"; then
    echo "notified: $commit on main ($kind)"; rm -f "$msg"; exit 0
  fi
  sleep 5
done
echo "ERROR: notification push failed; message kept at $msg" >&2; exit 1
