#!/usr/bin/env python3
"""Round log for the independent-frame-critic skill (Python 3 stdlib only).

  critic_log.py check  CRITIQUE.json
  critic_log.py add    LOG.json CRITIQUE.json [--label TEXT]
  critic_log.py status LOG.json [--floor 6] [--bar 7] [--max-rounds 5] [--stall 3]

A critique is the reviewer's JSON: {"scores": {category: 1-10}, "fixes": [...], "frames": {...}, "summary": "..."}.
status decides PASS / CONTINUE / STALLED / CAPPED from the logged rounds.
"""
import argparse
import json
import os
import sys
import time

CATEGORIES = ["world_fit", "identity", "look", "light", "composition", "plausibility", "text_signage", "story_beat"]
VERDICTS = {"keep", "fix", "reject"}


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def problems_in(c):
    out = []
    scores = c.get("scores")
    if not isinstance(scores, dict):
        return ["no 'scores' object"]
    for k in CATEGORIES:
        v = scores.get(k)
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            out.append(f"score '{k}' missing or not a number")
        elif not 1 <= v <= 10:
            out.append(f"score '{k}' = {v} is outside 1-10")
    extra = set(scores) - set(CATEGORIES)
    if extra:
        out.append("unknown categories: " + ", ".join(sorted(extra)))
    fixes = c.get("fixes", [])
    if not isinstance(fixes, list):
        out.append("'fixes' is not a list")
    elif len(fixes) > 5:
        out.append(f"{len(fixes)} fixes (the brief allows at most 5)")
    for i, fx in enumerate(fixes if isinstance(fixes, list) else []):
        if not isinstance(fx, dict) or not fx.get("problem") or not fx.get("frame"):
            out.append(f"fix {i + 1} lacks 'frame' or 'problem'")
    for fid, fv in (c.get("frames") or {}).items():
        if not isinstance(fv, dict) or fv.get("verdict") not in VERDICTS:
            out.append(f"frame {fid}: verdict must be keep, fix or reject")
    return out


def stats(c):
    v = [c["scores"][k] for k in CATEGORIES]
    return sum(v), sum(v) / len(v), min(v), min(CATEGORIES, key=lambda k: c["scores"][k])


def cmd_check(a):
    p = problems_in(load(a.critique))
    if p:
        print("\n".join("PROBLEM: " + x for x in p))
        return 1
    print("OK")
    return 0


def cmd_add(a):
    c = load(a.critique)
    p = problems_in(c)
    if p:
        print("\n".join("PROBLEM: " + x for x in p))
        print("Not logged. Ask the reviewer to answer in the brief's JSON format.")
        return 1
    log = load(a.log) if os.path.exists(a.log) else {"rounds": []}
    log["rounds"].append({"n": len(log["rounds"]) + 1, "label": a.label or "", "logged": time.strftime("%Y-%m-%d %H:%M"),
                          "source": os.path.abspath(a.critique), "critique": c})
    tmp = a.log + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)
    os.replace(tmp, a.log)
    total, mean, low, _ = stats(c)
    print(f"logged round {len(log['rounds'])}: total {total}, mean {mean:.2f}, lowest {low}")
    return 0


def decide(rounds, floor, bar, max_rounds, stall):
    last = rounds[-1]["critique"]
    _, mean, low, _ = stats(last)
    if low >= floor and mean >= bar:
        return "PASS"
    totals = [stats(r["critique"])[0] for r in rounds]
    if len(totals) > stall and max(totals[-stall:]) <= max(totals[:-stall]):
        return "STALLED"
    if len(rounds) >= max_rounds:
        return "CAPPED"
    return "CONTINUE"


def cmd_status(a):
    if not os.path.exists(a.log):
        print("no rounds logged yet")
        return 1
    rounds = load(a.log)["rounds"]
    if not rounds:
        print("no rounds logged yet")
        return 1
    print(f"{'round':<6}{'total':>6}{'mean':>7}{'low':>5}  lowest category   label")
    best = None
    for r in rounds:
        total, mean, low, cat = stats(r["critique"])
        if best is None or total > best[1]:
            best = (r["n"], total)
        print(f"{r['n']:<6}{total:>6}{mean:>7.2f}{low:>5}  {cat:<17} {r.get('label', '')}")
    last = rounds[-1]["critique"]
    verdicts = {}
    for fid, fv in (last.get("frames") or {}).items():
        verdicts.setdefault(fv["verdict"], []).append(fid)
    print(f"best round: {best[0]} (total {best[1]})")
    for v in ("keep", "fix", "reject"):
        if verdicts.get(v):
            print(f"{v}: {', '.join(sorted(verdicts[v]))}")
    for i, fx in enumerate(last.get("fixes", []), 1):
        print(f"fix {i}: [{fx.get('frame')}] {fx.get('problem')} -> {fx.get('fix', '')}")
    d = decide(rounds, a.floor, a.bar, a.max_rounds, a.stall)
    print(f"DECISION: {d}" + (f" (deliver round {best[0]}'s keep frames and report)" if d in ("STALLED", "CAPPED") else ""))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("critique")
    ad = sub.add_parser("add")
    ad.add_argument("log")
    ad.add_argument("critique")
    ad.add_argument("--label")
    st = sub.add_parser("status")
    st.add_argument("log")
    st.add_argument("--floor", type=float, default=6)
    st.add_argument("--bar", type=float, default=7)
    st.add_argument("--max-rounds", type=int, default=5)
    st.add_argument("--stall", type=int, default=3)
    a = ap.parse_args()
    return {"check": cmd_check, "add": cmd_add, "status": cmd_status}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
