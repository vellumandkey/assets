#!/usr/bin/env bash
# Run before every commit to this PUBLIC repo (bash tools/check_public.sh after git add).
# Fails if a staged change contains a Canva template link or a PDF.
# Template links are the paid product and must never be published here.
set -euo pipefail
files=$(git diff --cached --name-only --diff-filter=ACM)
[ -z "$files" ] && { echo "check_public: nothing staged"; exit 0; }
if echo "$files" | grep -qiE '\.pdf$'; then echo "BLOCKED: PDF staged (buyer PDFs must stay private)"; exit 1; fi
if git diff --cached -U0 -- . ':(exclude)tools/check_public.sh' | grep -E '^\+' | grep -qiE 'canva\.link/[a-z0-9]{6,}|utm_source=publishsharelink'; then
  echo "BLOCKED: staged changes contain a Canva template link"; exit 1; fi
echo "check_public: ok"
