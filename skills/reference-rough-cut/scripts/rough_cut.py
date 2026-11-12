#!/usr/bin/env python3
"""Rough cuts built from reference shots (the edit library of ad-reference-edit-library), and generation slots from them.

Cut list format (TSV, one shot per line; '#' lines are comments; '# BLOCK <name>' starts a named block):
  <clip_id> <TAB> <seconds> <TAB> <position 0..1 inside the shot> <TAB> <note> [<TAB> <transition out, e.g. WHIP_PAN>]

Usage (every command takes --root <project> [--db <file>] [--fps 24]):
  check  CUT.tsv                       every clip exists, length fits the shot, warns about long parents with sub-shots
  build  REEL CUT.tsv --pool pool.json Resolve clip_infos JSON (stdout) + blocks TSV + rows in cut_shots
  preview CUT.tsv OUT.mp4 [--aspect 16x9|9x16] [--audio]   preview straight from the reference files, no NLE needed
  qc     OUT.mp4                       contact strip, 2 frames per second (<OUT>_qc.jpg)
  slots  REEL                          SLOTS.md + slots.json: one generation slot per shot for the video-prompt skills
"""
import argparse, json, math, pathlib, sqlite3, subprocess, sys, tempfile

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("cmd"); ap.add_argument("rest", nargs="*")
ap.add_argument("--root", required=True); ap.add_argument("--db"); ap.add_argument("--fps", type=float, default=24.0)
ap.add_argument("--pool"); ap.add_argument("--aspect", default="16x9"); ap.add_argument("--audio", action="store_true")
A = ap.parse_args()
ROOT = pathlib.Path(A.root).expanduser().resolve()
DB = pathlib.Path(A.db).expanduser() if A.db else ROOT / "DATABASE" / "edit_library.db"
db = sqlite3.connect(DB); TL = A.fps
db.executescript("""
CREATE TABLE IF NOT EXISTS reels(reel_id TEXT PRIMARY KEY, title TEXT, style TEXT, target_len_s REAL, status TEXT, notes TEXT);
CREATE TABLE IF NOT EXISTS cut_shots(reel_id TEXT, position INT, clip_id TEXT, block TEXT, length_s REAL, frames INT, record_frame INT,
  src_in_s REAL, note TEXT, transition_out TEXT, generated_file TEXT, status TEXT DEFAULT 'ref_only', PRIMARY KEY(reel_id, position));
""")

def parse(cut):
    rows, block = [], ""
    for line in pathlib.Path(cut).read_text().splitlines():
        s = line.strip()
        if not s: continue
        if s.startswith("#"):
            if s.upper().startswith("# BLOCK"): block = s[7:].strip()
            continue
        f = line.split("\t")
        if len(f) < 3: sys.exit(f"bad line (need clip_id, seconds, position separated by TABs): {line}")
        rows.append(dict(clip=f[0].strip(), length=float(f[1]), at=float(f[2]), note=f[3].strip() if len(f) > 3 else "",
                         tout=f[4].strip().upper() if len(f) > 4 else "", block=block))
    return rows

def shot(cid):
    r = db.execute("select c.start_s,c.end_s,c.ref_id,r.fps,r.file,c.thumb from ref_clips c join reference_videos r using(ref_id) where c.clip_id=?", (cid,)).fetchone()
    if not r: sys.exit(f"unknown clip_id {cid}")
    return r

def place(r):
    s, e, ref, fps, f, th = shot(r["clip"])
    length = min(r["length"], e - s); src = s + max(0.0, (e - s - length) * r["at"]); n = round(length * TL)
    sf = round(src * fps)
    ef = sf + (n if abs(fps - TL) < 0.1 else math.ceil(n * fps / TL) + 1)  # end is exclusive; one spare frame for rate conform
    return dict(ref=ref, fps=fps, file=f, thumb=th, src=src, n=n, sf=sf, ef=ef, length=length)

def cmd_check():
    bad = 0
    for r in parse(A.rest[0]):
        s, e, *_ = shot(r["clip"])
        subs = db.execute("select count(*) from ref_clips where parent_id=?", (r["clip"],)).fetchone()[0] if \
            db.execute("select 1 from pragma_table_info('ref_clips') where name='parent_id'").fetchone() else 0
        msg = []
        if r["length"] > e - s + 1e-3: msg.append(f"asks {r['length']}s, shot is {e-s:.2f}s (will be cut short)")
        if subs: msg.append(f"long take with {subs} sub-shots: use a sub-shot id or check the frame at position {r['at']}")
        if msg: bad += 1; print(r["clip"], "|", "; ".join(msg))
    print("ok" if not bad else f"{bad} lines to look at")

def cmd_build():
    reel, cut = A.rest; pool = json.load(open(A.pool)); rows = parse(cut)
    db.execute("delete from cut_shots where reel_id=?", (reel,))
    infos, blocks, rec, last = [], [], 0, None
    for i, r in enumerate(rows, 1):
        p = place(r)
        if r["block"] != last: blocks.append(f"{rec}\t{rec/TL:.2f}\t{r['block']}"); last = r["block"]
        infos.append({"clip_id": pool[p["ref"]], "start_frame": p["sf"], "end_frame": p["ef"], "record_frame": rec})
        db.execute("insert into cut_shots(reel_id,position,clip_id,block,length_s,frames,record_frame,src_in_s,note,transition_out) values(?,?,?,?,?,?,?,?,?,?)",
                   (reel, i, r["clip"], r["block"], round(p["n"] / TL, 3), p["n"], rec, round(p["src"], 3), r["note"], r["tout"]))
        rec += p["n"]
    db.execute("insert into reels(reel_id,target_len_s,status) values(?,?,'rough') on conflict(reel_id) do update set target_len_s=excluded.target_len_s", (reel, round(rec / TL, 2)))
    db.commit()
    bt = pathlib.Path(cut).with_suffix(".blocks.tsv"); bt.write_text("record_frame\tsec\tblock\n" + "\n".join(blocks) + "\n")
    print(json.dumps(infos)); print(f"{len(rows)} shots, {rec/TL:.1f} s, blocks: {bt}", file=sys.stderr)

def cmd_preview():
    cut, out = A.rest; out = pathlib.Path(out)
    W, H = (1280, 720) if A.aspect == "16x9" else (720, 1280)
    vf = (f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2" if A.aspect == "16x9"
          else f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}")
    tmp = pathlib.Path(tempfile.mkdtemp()); parts = []
    for k, r in enumerate(parse(cut)):
        p = place(r); seg = tmp / f"{k:03d}.mp4"
        cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{p['src']:.3f}", "-i", str(ROOT / p["file"]), "-frames:v", str(p["n"]),
               "-vf", f"fps={TL},{vf},setsar=1", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20"]
        cmd += (["-af", f"atrim=0:{p['n']/TL:.3f},apad", "-t", f"{p['n']/TL:.3f}", "-c:a", "aac", "-ar", "48000", "-ac", "2"] if A.audio else ["-an"])
        subprocess.run(cmd + [str(seg)], check=True); parts.append(seg)
    (tmp / "list.txt").write_text("".join(f"file '{x}'\n" for x in parts)); out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(tmp / "list.txt"), "-c", "copy", "-movflags", "+faststart", str(out)], check=True)
    print(out, len(parts), "shots")

def cmd_qc():
    src = pathlib.Path(A.rest[0]); dst = src.with_name(src.stem + "_qc.jpg")
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)], capture_output=True, text=True).stdout)
    cols = 16; rows = max(1, math.ceil(dur * 2 / cols))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf", f"fps=2,scale=200:-1,tile={cols}x{rows}", "-frames:v", "1", str(dst)], check=True)
    print(dst, f"{dur:.1f}s")

def cmd_slots():
    reel = A.rest[0]
    rows = db.execute("""select s.position,s.clip_id,s.block,s.length_s,s.frames,s.record_frame,s.src_in_s,s.note,s.transition_out,c.thumb,c.ref_id,r.title,r.width,r.height
                         from cut_shots s join ref_clips c using(clip_id) join reference_videos r on r.ref_id=c.ref_id where s.reel_id=? order by s.position""", (reel,)).fetchall()
    if not rows: sys.exit(f"no cut_shots for {reel}: run build first")
    out = ROOT / "02_PROMPTS" / reel; out.mkdir(parents=True, exist_ok=True); slots = []
    for i, (pos, cid, block, ln, fr, rec, src, note, tout, th, ref, title, w, h) in enumerate(rows):
        tin = rows[i - 1][8] if i else ""
        slots.append(dict(slot=f"{reel}_SL{pos:02d}", block=block, seconds=ln, frames=fr, record_s=round(rec / TL, 2),
                          reference_clip=cid, reference_film=f"{ref} {title}", reference_in_s=src, reference_thumb=th,
                          reference_aspect="vertical" if h > w else "horizontal", action=note, transition_in=tin or "CUT", transition_out=tout or "CUT",
                          generate_seconds=max(2.0, round(ln + 1.0, 1)) if ln < 1.5 else round(ln + 0.5, 1)))
    (out / "slots.json").write_text(json.dumps(slots, indent=1))
    md = [f"# {reel} generation slots", "", f"{len(slots)} slots, {sum(r[4] for r in rows)/TL:.1f} s. Each slot = one shot to generate.",
          "Copy the MOTION, CAMERA and TIMING of the reference clip, never its people, logos or text.", ""]
    for s in slots:
        md += [f"## {s['slot']}  ({s['seconds']} s / {s['frames']} f, at {s['record_s']} s)  {s['block']}",
               f"- Reference: {s['reference_clip']} from {s['reference_film']}, in at {s['reference_in_s']} s ({s['reference_aspect']})",
               f"- Thumb: {s['reference_thumb']}", f"- Action: {s['action']}",
               f"- Generate {s['generate_seconds']} s real-time, cut the {s['seconds']} s window where the action peaks (harvest window)",
               f"- Transition in: {s['transition_in']} | out: {s['transition_out']}", ""]
    (out / "SLOTS.md").write_text("\n".join(md)); print(out / "SLOTS.md", len(slots), "slots")

{"check": cmd_check, "build": cmd_build, "preview": cmd_preview, "qc": cmd_qc, "slots": cmd_slots}[A.cmd]()
