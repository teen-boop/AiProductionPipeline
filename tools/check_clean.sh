#!/usr/bin/env bash
# Scans the repository for things that must never be published:
# API keys / tokens, private keys, e-mail addresses, absolute personal paths,
# and non-English (Cyrillic) text. Exit code 1 if anything is found.
set -uo pipefail
cd "$(dirname "$0")/.."

found=0
check() {  # $1 = label, $2 = extended regex
  local hits
  hits=$(grep -rInE --exclude-dir=.git --exclude=check_clean.sh -e "$2" . || true)
  if [ -n "$hits" ]; then
    echo "== $1"; echo "$hits" | cut -c1-200; echo; found=1
  fi
}

check "API keys / tokens" '(sk-[A-Za-z0-9_-]{16,}|sk_[A-Za-z0-9]{16,}|ak_[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{30,}|xox[abpr]-[A-Za-z0-9-]{10,}|hf_[A-Za-z0-9]{20,}|r8_[A-Za-z0-9]{20,})'
check "Private key blocks" '-----BEGIN [A-Z ]*PRIVATE KEY-----'
check "Key assignments with a value" '(API_KEY|SECRET|TOKEN|ACCESS_KEY|PASSWORD)[A-Z_]*[[:space:]]*[=:][[:space:]]*["'"'"']?[A-Za-z0-9_/+-]{12,}'
check "E-mail addresses" '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(com|net|org|io|ru|de|co|me|ai)\b'
check "Absolute personal paths" '(/Users/[A-Za-z0-9._-]+|/home/[A-Za-z0-9._-]+|/Volumes/[A-Za-z0-9._ -]+|C:\\Users\\[A-Za-z0-9._-]+)'

cyr=$(python3 - <<'PY'
import os, re
pat = re.compile("[\u0400-\u04FF]")
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d != ".git"]
    for f in files:
        p = os.path.join(root, f)
        try:
            if pat.search(open(p, encoding="utf-8").read()): print(p)
        except (UnicodeDecodeError, OSError):
            pass
PY
)
if [ -n "$cyr" ]; then echo "== Non-English (Cyrillic) text in:"; echo "$cyr"; echo; found=1; fi

if [ "$found" -eq 0 ]; then echo "check_clean: OK — nothing found."; else echo "check_clean: FIX the findings above before committing."; fi
exit $found
