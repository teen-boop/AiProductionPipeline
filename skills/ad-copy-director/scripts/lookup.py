#!/usr/bin/env python3
"""Look up keywords in the ad research library.

  lookup.py --list                      brands in the library
  lookup.py -b BRAND KEYWORD ...        one brand only
  lookup.py -b BRAND --section 8        print one whole section (1-10)
  lookup.py -b BRAND -c A6 [KEYWORD]    rows tagged with one audience category

Library root: $AD_LIBRARY, else ~/ad-research-library. One folder per brand,
each holding AD_GLOSSARY.md (the file written by the ad-research-glossary skill).
"""
import argparse, os, re, sys

ROOT = os.path.expanduser(os.environ.get("AD_LIBRARY", "~/ad-research-library"))

def brands():
    if not os.path.isdir(ROOT): return []
    return sorted(d for d in os.listdir(ROOT) if os.path.isfile(os.path.join(ROOT, d, "AD_GLOSSARY.md")))

def sections(path):
    cur, out = "0. Header", []
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if line.startswith("## "): cur = line[3:].strip(); continue
        if line.strip() and not re.match(r"^\|[-| ]+\|$", line): out.append((cur, line))
    return out

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("keywords", nargs="*"); ap.add_argument("-b", "--brand"); ap.add_argument("--list", action="store_true")
    ap.add_argument("--section", type=int); ap.add_argument("-c", "--category")
    a = ap.parse_args()
    bs = brands()
    if a.list or (not a.keywords and a.section is None and not a.category):
        print(f"library: {ROOT}"); [print(" ", b) for b in bs]; print(f"{len(bs)} brand(s)"); return
    if a.brand:
        hit = [b for b in bs if a.brand.lower() in b.lower()]
        if not hit: sys.exit(f"no glossary for '{a.brand}' in {ROOT}. Run the ad-research-glossary skill first.")
        bs = hit
    else:
        sys.exit("Name the brand with -b. Texts for one brand never use another brand's research.")
    kws = [k.lower() for k in a.keywords]; total = 0
    for b in bs:
        last = None
        for sec, line in sections(os.path.join(ROOT, b, "AD_GLOSSARY.md")):
            if a.section is not None and not sec.startswith(f"{a.section}."): continue
            if a.category and not re.search(rf"\b{re.escape(a.category)}\b", line, re.I): continue
            if kws and not any(k in line.lower() for k in kws): continue
            if (b, sec) != last: print(f"\n[{b}] {sec}"); last = (b, sec)
            print("  " + line); total += 1
    print(f"\n{total} line(s) matched" + ("" if total else ". Nothing in the library uses these words: update the glossary before writing."))

main()
