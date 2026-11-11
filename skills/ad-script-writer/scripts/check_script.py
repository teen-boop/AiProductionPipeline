#!/usr/bin/env python3
"""Mechanical check of an ad script beat sheet.

  check_script.py AD_SCRIPT_file.md [--wps 2.3] [--air 0.2]

Reads every beat table (a table whose header has the columns Time and Spoken) and reports:
  - beats that do not join up (gap or overlap) and the total length
  - words per second per beat (flag above 3.0) and for the whole script
    (budget = length x wps x (1 - air); default 2.3 words/s with 20% air)
  - long dashes anywhere in the Spoken or On-screen columns
Exits 1 if anything fails.
"""
import re, sys
args = sys.argv[1:]
if not args: sys.exit(__doc__)
path = args[0]
wps = float(args[args.index("--wps") + 1]) if "--wps" in args else 2.3
air = float(args[args.index("--air") + 1]) if "--air" in args else 0.2
lines = open(path, encoding="utf-8").read().split("\n")
fails = 0; title = ""; i = 0
def cells(l): return [c.strip() for c in l.strip().strip("|").split("|")]
while i < len(lines):
    l = lines[i]
    if l.startswith("#"): title = l.lstrip("# ").strip()
    if l.startswith("|") and "Time" in l and "Spoken" in l:
        head = cells(l); ti, si = head.index("Time"), head.index("Spoken")
        oi = next((k for k, h in enumerate(head) if h.lower().startswith("on-screen")), None)
        i += 2; rows = []
        while i < len(lines) and lines[i].startswith("|"): rows.append(cells(lines[i])); i += 1
        print(f"\n== {title}"); prev = 0.0; words = 0
        for r in rows:
            m = re.match(r"([\d.]+)\s*(?:to|-)\s*([\d.]+)", r[ti])
            if not m: print(f"  FAIL  cannot read time '{r[ti]}'"); fails += 1; continue
            a, b = float(m.group(1)), float(m.group(2))
            if abs(a - prev) > 0.01: print(f"  FAIL  beat at {a}s does not join the previous beat ending {prev}s"); fails += 1
            prev = b
            spoken = re.sub(r"\(.*?\)|\[.*?\]", "", r[si]); spoken = re.sub(r"\b[A-Z]{2,}:", "", spoken); n = len(re.findall(r"[A-Za-z0-9$%']+", spoken)); words += n
            rate = n / (b - a) if b > a else 0
            flag = "FAIL" if rate > 3.0 else "ok  "
            if rate > 3.0: fails += 1
            print(f"  {flag}  {a:>4.1f}-{b:<4.1f}s  {n:>2} words  {rate:.1f}/s")
            for col in (si, oi):
                if col is not None and col < len(r) and re.search("[—–]", r[col]): print(f"  FAIL  long dash in '{r[col][:40]}'"); fails += 1
        budget = prev * wps * (1 - air)
        ok = words <= budget + 0.5
        if not ok: fails += 1
        print(f"  {'ok  ' if ok else 'FAIL'}  total {prev:.0f}s, {words} spoken words, budget {budget:.0f}")
        continue
    i += 1
print("\nPASSED" if not fails else f"\nFAILED: {fails} problem(s)")
sys.exit(1 if fails else 0)
