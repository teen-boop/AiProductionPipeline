#!/usr/bin/env python3
"""Progress report for one project's full pipeline run.

  pipeline_status.py --project <dir>                         write PIPELINE_STATUS.md and print it
  pipeline_status.py --project <dir> --approve research      record the user's approval of a gate
  pipeline_status.py --project <dir> --note "text"           add a line to the run log

State lives in <project>/PIPELINE_RUN.json (gates the user approved, notes). Everything else is read from the
project's own folders: the research glossary, scripts, generated files, GENERATION_LOG.jsonl, edit, finals,
delivery and post-launch results. It never looks outside the project folder. Standard library only.
"""
import argparse, glob, json, os, time

STAGES = [  # id, title, files that show the stage produced something, gate the user must approve after it
    ("brief",      "Brief and delivery target",   ["**/00_BRIEF/BRIEF.md", "BRIEF.md"],                                        "brief"),
    ("backend",    "Generation backend",          ["**/pipeline.config.json"],                                                   None),
    ("research",   "Research (Ad Glossary)",      ["**/AD_GLOSSARY.md"],                                                      "research"),
    ("texts",      "Ad texts",                    ["**/AD_TEXTS_*.md"],                                                       None),
    ("script",     "Script",                      ["**/AD_SCRIPT_*.md"],                                                      "script"),
    ("refs",       "References (cast, look)",     ["**/01_REFERENCES/INTERNAL/**/LOCKED/*", "**/LOOK.md", "**/STYLE_LOCK.json"], "refs"),
    ("frames",     "Images and keyframes",        ["**/03_GENERATED/IMAGES/*", "**/frames/**/*.png"],                           "frames"),
    ("video",      "Video clips",                 ["**/03_GENERATED/VIDEO/*"],                                                   "video"),
    ("titles",     "Titles and motion graphics",  ["**/motion/**/index.html", "**/renders/*.mp4"],                           None),
    ("sound",      "Sound",                       ["**/audio/mix.wav", "**/04_EDIT/**/03_AUDIO/**/*.wav"],                      None),
    ("edit",       "Edit and timeline",           ["**/04_EDIT/**/EDIT_MANIFEST.csv", "**/04_EDIT/**/cutplan.json"],               "cut"),
    ("verify",     "Encoded-file check",          ["**/qc/**/report.md", "**/VERIFY.md"],                                    None),
    ("finals",     "Finals tree",                 ["**/05_FINAL_OUTPUTS/INDEX.md", "**/FINAL_OUTPUTS/INDEX.md"],                   None),
    ("delivery",   "Delivery package",            ["**/06_DELIVERY/*/DELIVERY_NOTE.md"],                                        "delivery"),
    ("results",    "Results after launch",        ["**/07_POSTING/RESULTS*.md", "**/AD_RESULTS*.md"],                           None),
]

def found(root, pats):
    hits = []
    for p in pats:
        hits += [h for h in glob.glob(os.path.join(root, p), recursive=True)
                 if not os.path.basename(h).startswith(".") and "/_previous/" not in h and "/99_ARCHIVE/" not in h]
    return sorted(set(hits))

def genlog(root):
    logs = found(root, ["**/GENERATION_LOG.jsonl"])
    rows = []
    for lp in logs:
        for line in open(lp, encoding="utf-8", errors="ignore"):
            try: rows.append(json.loads(line))
            except Exception: pass
    last = {}
    for r in rows:
        if r.get("id"): last.setdefault(r["id"], {}).update({k: v for k, v in r.items() if v not in (None, "")})
    cost = {}
    for r in last.values():
        if r.get("cost") is not None: cost[r.get("unit", "?")] = cost.get(r.get("unit", "?"), 0) + float(r["cost"])
    by = {}
    for r in last.values():
        k = ("video" if str(r.get("file", "")).lower().endswith((".mp4", ".mov", ".webm")) else "image")
        by[k] = by.get(k, 0) + 1
    st = {}
    for r in last.values(): st[r.get("status", "?")] = st.get(r.get("status", "?"), 0) + 1
    return len(last), by, st, cost

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", required=True); ap.add_argument("--approve"); ap.add_argument("--note")
    a = ap.parse_args(); root = os.path.abspath(a.project)
    sp = os.path.join(root, "PIPELINE_RUN.json")
    state = json.load(open(sp)) if os.path.exists(sp) else {"approved": {}, "log": []}
    now = time.strftime("%Y-%m-%d %H:%M")
    gates = {g for *_, g in STAGES if g}
    if a.approve:
        if a.approve not in gates: raise SystemExit(f"unknown gate '{a.approve}'. Gates: {', '.join(sorted(gates))}")
        state["approved"][a.approve] = now; state["log"].append(f"{now} approved: {a.approve}")
    if a.note: state["log"].append(f"{now} {a.note}")
    if a.approve or a.note: json.dump(state, open(sp, "w"), indent=1)
    out = [f"# Pipeline status: {os.path.basename(root)}", "", f"Updated {now}. Read from this project's folder only.", "",
           "| # | Stage | Output found | Gate |", "|---|---|---|---|"]
    nxt = None
    for i, (sid, title, pats, gate) in enumerate(STAGES, 1):
        hits = found(root, pats)
        g = "" if not gate else (f"approved {state['approved'][gate]}" if gate in state["approved"] else ("WAITING for approval" if hits else "not reached"))
        if nxt is None and (not hits or (gate and gate not in state["approved"])): nxt = (title, bool(hits), gate)
        out.append(f"| {i} | {title} | {len(hits)} file(s)" + (f": `{os.path.relpath(hits[0], root)}`" if hits else "") + f" | {g} |")
    n, by, st, cost = genlog(root)
    out += ["", "## Generations", ""]
    if n:
        out += [f"- {n} logged: " + ", ".join(f"{v} {k}" for k, v in by.items()),
                "- status: " + ", ".join(f"{k} {v}" for k, v in st.items()),
                "- cost so far: " + (", ".join(f"{v:g} {k}" for k, v in cost.items()) if cost else "none recorded")]
    else:
        out.append("- No GENERATION_LOG.jsonl in this project: generations are not being logged (run generation-log).")
    out += ["", "## Next", ""]
    if nxt:
        t, has, g = nxt
        out.append(f"- {t}: " + ("output exists, waiting for the user's approval" if has and g else "not done yet"))
    else:
        out.append("- All stages have output and every gate is approved.")
    if state["log"]: out += ["", "## Run log", ""] + [f"- {l}" for l in state["log"][-15:]]
    text = "\n".join(out) + "\n"
    open(os.path.join(root, "PIPELINE_STATUS.md"), "w").write(text); print(text)

main()
