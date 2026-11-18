#!/usr/bin/env python3
"""Preproduction setup check.
  setup_check.py init <project_root> --scenes "S1:title,S2:title"   write a SETUP.json template
  setup_check.py check <SETUP.json>                                  report gaps; exit 1 if anything blocks
"""
import json, sys, pathlib
def init(root, scenes):
    root = pathlib.Path(root); out = root / "SETUP.json"
    if out.exists(): sys.exit(f"{out} exists; edit it instead")
    sc = [dict(id=s.split(":")[0], title=s.split(":", 1)[-1], location="", time_of_day="", state={"weather": "", "light": None}, key_light="",
               characters=[], wardrobe={}, props=[], look_ref={"path": "", "role": ""}, camera_refs=[], shots=[], master="", details=[]) for s in scenes.split(",") if s]
    json.dump(dict(project=root.name, style_card="", lessons="LESSONS.md", look_approved=False, characters={}, props={}, locations={}, scenes=sc), open(out, "w"), indent=1)
    print("wrote", out)
def check(path):
    path = pathlib.Path(path); root = path.parent; S = json.load(open(path)); bad = 0; rows = []
    def ex(p): return bool(p) and (root / p).exists()
    def line(scope, item, status, note=""):
        nonlocal bad
        if status != "OK": bad += 1
        rows.append((scope, item, status, note))
    line("project", "style card", "OK" if ex(S.get("style_card")) else "MISSING", S.get("style_card", ""))
    line("project", "LESSONS.md", "OK" if ex(S.get("lessons")) else "MISSING")
    line("project", "look approved", "OK" if S.get("look_approved") else "UNAPPROVED")
    for n, c in S.get("characters", {}).items():
        line(f"char {n}", "hero card", "OK" if ex(c.get("hero_card")) else "MISSING", c.get("hero_card", ""))
        if ex(c.get("hero_card")) and not c.get("approved"): line(f"char {n}", "hero card", "UNAPPROVED")
        for d in c.get("details", []): line(f"char {n}", "detail", "OK" if ex(d) else "MISSING", d)
    for n, p in S.get("props", {}).items():
        line(f"prop {n}", "detail card", "OK" if ex(p.get("card")) else "MISSING", p.get("card", ""))
        if ex(p.get("card")) and not p.get("approved"): line(f"prop {n}", "detail card", "UNAPPROVED")
    for n, l in S.get("locations", {}).items():
        line(f"loc {n}", "location card", "OK" if ex(l.get("card")) else "MISSING", l.get("card", ""))
        if ex(l.get("card")) and not l.get("approved"): line(f"loc {n}", "location card", "UNAPPROVED")
    for s in S.get("scenes", []):
        sid = f"scene {s['id']}"
        for k in ("location", "time_of_day", "key_light", "master"): line(sid, k, "OK" if s.get(k) else "MISSING", str(s.get(k, "")))
        if s.get("location") and s["location"] not in S.get("locations", {}): line(sid, "location card", "MISSING", f"{s['location']} not in locations")
        st = s.get("state", {}); line(sid, "state dials", "OK" if st.get("weather") and st.get("light") is not None else "MISSING", json.dumps(st))
        for c in s.get("characters", []):
            if c not in S.get("characters", {}): line(sid, f"hero card {c}", "MISSING", "character not in characters")
            if c not in s.get("wardrobe", {}): line(sid, f"wardrobe {c}", "MISSING")
        for p in s.get("props", []):
            if p not in S.get("props", {}): line(sid, f"prop card {p}", "MISSING")
        lr = s.get("look_ref", {}); line(sid, "look ref", "OK" if ex(lr.get("path")) and lr.get("role") else "MISSING", lr.get("path", ""))
        cr = s.get("camera_refs", []); line(sid, "camera refs", "OK" if cr and all(ex(c.get("path")) and c.get("role") for c in cr) else "MISSING", f"{len(cr)} refs")
        line(sid, "shot list", "OK" if s.get("shots") else "MISSING", f"{len(s.get('shots', []))} shots")
        line(sid, "detail shots", "OK" if s.get("details") else "MISSING", f"{len(s.get('details', []))} details")
        for k, v in s.items():
            if isinstance(v, dict) and v.get("proposed"): line(sid, k, "PROPOSED", "confirm with the user")
    w = max(len(r[0]) for r in rows) if rows else 10
    for r in rows: print(f"{r[0]:<{w}}  {r[1]:<16} {r[2]:<10} {r[3]}")
    print(f"\n{bad} item(s) block generation" if bad else "\nREADY: every scene passes"); sys.exit(1 if bad else 0)
if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    if a[0] == "init": init(a[1], a[a.index("--scenes") + 1] if "--scenes" in a else "")
    elif a[0] == "check": check(a[1])
    else: sys.exit(__doc__)
