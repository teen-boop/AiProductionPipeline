#!/usr/bin/env python3
"""One append-only log of every generation: what was made, with what, from what, for how much.

Log: <project>/03_GENERATED/GENERATION_LOG.jsonl (one JSON record per output file). Files are matched by content
(size + first/last MiB hash), so a take renamed or copied into EDIT bins still finds its record.

  add      --project P --file OUT [--file OUT2] --tool higgsfield --model seedance_2_0 --prompt "..." | --prompt-file F
           [--refs R020,R012,/path/ref.png] [--cost 12 --unit credits] [--params '{"duration":10}'] [--shot S03]
           [--job-id ID] [--parent G0004] [--note "..."]
  find     --project P FILE...           record(s) for these files, wherever they are now
  status   --project P --id G0007 approved|rejected|candidate [--note "..."]
  recipe   --project P (--id G0007 | --shot S03)   everything needed to regenerate
  report   --project P [--by model|tool|day|shot]  count, cost, approval rate
  missing  --project P --path DIR        media files in DIR that have no record (to backfill)
"""
import argparse, csv, hashlib, json, os, re, subprocess, sys, time
from collections import defaultdict

MEDIA = {".mp4", ".mov", ".m4v", ".webm", ".png", ".jpg", ".jpeg", ".webp", ".wav", ".mp3", ".m4a", ".glb"}


def qhash(p):
    h, size = hashlib.sha1(), os.path.getsize(p)
    with open(p, "rb") as f:
        h.update(f.read(1 << 20))
        if size > 2 << 20:
            f.seek(-(1 << 20), 2); h.update(f.read(1 << 20))
    return f"{size}:{h.hexdigest()}"


def probe(p):
    try:
        j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                       "stream=width,height:format=duration", "-of", "json", p],
                                      capture_output=True, text=True, timeout=30).stdout or "{}")
        st = (j.get("streams") or [{}])[0]
        d = float(j.get("format", {}).get("duration", 0) or 0)
        return st.get("width"), st.get("height"), round(d, 2) if d > 0.05 else None
    except Exception:
        return None, None, None


def log_path(project):
    return os.path.join(os.path.abspath(project), "03_GENERATED", "GENERATION_LOG.jsonl")


def load(project):
    p = log_path(project)
    recs = []
    if os.path.exists(p):
        for line in open(p):
            line = line.strip()
            if line:
                recs.append(json.loads(line))
    # later lines override earlier ones with the same id (status updates are appended, never rewritten)
    merged = {}
    for r in recs:
        merged.setdefault(r["id"], {}).update(r)
    return list(merged.values())


def append(project, rec):
    p = log_path(project)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def resolve_refs(project, refs):
    idx = os.path.join(os.path.abspath(project), "01_REFERENCES", "REFERENCES_INDEX.csv")
    by_hash = {}
    if os.path.exists(idx):
        with open(idx, newline="") as f:
            by_hash = {r["hash"]: r["id"] for r in csv.DictReader(f)}
    out = []
    for r in [x.strip() for x in refs.split(",") if x.strip()]:
        if os.path.isfile(r):
            out.append(by_hash.get(qhash(r)) or os.path.abspath(r))
        else:
            out.append(r)
    return out


def cmd_add(a):
    recs = load(a.project)
    n = max([int(r["id"][1:]) for r in recs] or [0])
    prompt = open(a.prompt_file).read().strip() if a.prompt_file else (a.prompt or "")
    if not prompt:
        sys.exit("a prompt is required (--prompt or --prompt-file): a take without its prompt cannot be repeated")
    refs = resolve_refs(a.project, a.refs or "")
    for f in a.file:
        if not os.path.isfile(f):
            sys.exit(f"missing file: {f}")
        n += 1
        w, h, d = probe(f)
        rec = dict(id=f"G{n:04d}", time=time.strftime("%Y-%m-%dT%H:%M:%S"), file=os.path.abspath(f), hash=qhash(f),
                   w=w, h=h, duration=d, tool=a.tool, model=a.model, prompt=prompt,
                   prompt_file=os.path.abspath(a.prompt_file) if a.prompt_file else None, refs=refs,
                   params=json.loads(a.params) if a.params else {}, cost=a.cost, unit=a.unit, shot=a.shot,
                   job_id=a.job_id, parent=a.parent, status="candidate", note=a.note)
        append(a.project, rec)
        print(rec["id"], os.path.basename(f), f"{a.model}", f"cost {a.cost} {a.unit}" if a.cost is not None else "")


def by_hash(recs):
    return {r["hash"]: r for r in recs}


def show(r):
    print(f"{r['id']}  {r.get('status')}  shot={r.get('shot') or '-'}  {r.get('tool')}/{r.get('model')}  "
          f"cost={r.get('cost')} {r.get('unit') or ''}  {r.get('time')}")
    print(f"  file:   {r.get('file')}")
    print(f"  refs:   {', '.join(r.get('refs') or []) or '-'}")
    print(f"  params: {json.dumps(r.get('params') or {})}")
    print(f"  prompt: {r.get('prompt')}")


def cmd_find(a):
    hb = by_hash(load(a.project)); rc = 0
    for f in a.files:
        r = hb.get(qhash(f)) if os.path.isfile(f) else None
        if r:
            show(r)
        else:
            print("NO RECORD:", f); rc = 1
    return rc


def cmd_status(a):
    recs = {r["id"]: r for r in load(a.project)}
    if a.id not in recs:
        sys.exit(f"no record {a.id}")
    append(a.project, dict(id=a.id, status=a.state, status_time=time.strftime("%Y-%m-%dT%H:%M:%S"),
                           **({"note": a.note} if a.note else {})))
    print(a.id, "->", a.state)
    if a.state == "rejected":
        print("  to keep it out of every organizer, move the file into 03_GENERATED/_rejected/ (only with the user's yes)")


def cmd_recipe(a):
    recs = load(a.project)
    sel = [r for r in recs if (a.id and r["id"] == a.id) or (a.shot and r.get("shot") == a.shot)]
    if a.shot:
        sel.sort(key=lambda r: (r.get("status") != "approved", r["time"]))
    for r in sel:
        show(r)
        if r.get("parent"):
            print(f"  built on: {r['parent']}")
        print()
    if not sel:
        print("nothing logged for that id/shot")


def cmd_report(a):
    recs = load(a.project)
    key = {"model": lambda r: r.get("model"), "tool": lambda r: r.get("tool"),
           "day": lambda r: (r.get("time") or "")[:10], "shot": lambda r: r.get("shot")}[a.by]
    g = defaultdict(lambda: dict(n=0, cost=defaultdict(float), approved=0, rejected=0))
    for r in recs:
        x = g[key(r) or "-"]; x["n"] += 1
        if r.get("cost") is not None:
            x["cost"][r.get("unit") or "?"] += float(r["cost"])
        x["approved"] += r.get("status") == "approved"; x["rejected"] += r.get("status") == "rejected"
    print(f"{'':24} {'takes':>6} {'approved':>9} {'rejected':>9}  cost")
    tot = defaultdict(float)
    for k in sorted(g, key=str):
        x = g[k]
        for u, v in x["cost"].items():
            tot[u] += v
        print(f"{str(k)[:24]:24} {x['n']:6d} {x['approved']:9d} {x['rejected']:9d}  "
              + ", ".join(f"{v:g} {u}" for u, v in x["cost"].items()))
    print("total:", len(recs), "takes;", ", ".join(f"{v:g} {u}" for u, v in tot.items()) or "no cost logged")


def cmd_missing(a):
    hb = by_hash(load(a.project)); miss = []
    for dp, dns, fns in os.walk(os.path.abspath(a.path)):
        dns[:] = [d for d in dns if not d.startswith(".")]
        for fn in sorted(fns):
            if os.path.splitext(fn)[1].lower() in MEDIA and not fn.startswith("."):
                p = os.path.join(dp, fn)
                if qhash(p) not in hb:
                    miss.append(p)
    for p in miss:
        print("NO RECORD:", p)
    print(f"{len(miss)} file(s) without a record")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("add")
    for k in ("--project", "--tool", "--model"):
        s.add_argument(k, required=True)
    s.add_argument("--file", action="append", required=True); s.add_argument("--prompt"); s.add_argument("--prompt-file")
    s.add_argument("--refs"); s.add_argument("--cost", type=float); s.add_argument("--unit", default="credits")
    s.add_argument("--params"); s.add_argument("--shot"); s.add_argument("--job-id"); s.add_argument("--parent")
    s.add_argument("--note")
    s = sp.add_parser("find"); s.add_argument("--project", required=True); s.add_argument("files", nargs="+")
    s = sp.add_parser("status"); s.add_argument("--project", required=True); s.add_argument("--id", required=True)
    s.add_argument("state", choices=["approved", "rejected", "candidate"]); s.add_argument("--note")
    s = sp.add_parser("recipe"); s.add_argument("--project", required=True); s.add_argument("--id"); s.add_argument("--shot")
    s = sp.add_parser("report"); s.add_argument("--project", required=True)
    s.add_argument("--by", default="model", choices=["model", "tool", "day", "shot"])
    s = sp.add_parser("missing"); s.add_argument("--project", required=True); s.add_argument("--path", required=True)
    a = ap.parse_args()
    return {"add": cmd_add, "find": cmd_find, "status": cmd_status, "recipe": cmd_recipe, "report": cmd_report,
            "missing": cmd_missing}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
