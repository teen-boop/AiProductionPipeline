#!/usr/bin/env python3
"""Edit library from reference videos (ads, spec spots, films): shots, sub-shots, transitions, edit rhythm, tags, HTML page.

All data lives in one SQLite file; every path stored in it is relative to the project root.
Needs ffmpeg/ffprobe on PATH. `transitions`, `rhythm`, `sheets`, `strips` need numpy and Pillow
(run with a venv python, e.g. ~/.venvs/edit-library/bin/python).

Usage (every command takes --root <project> [--db <file>] [--video-dir <dir>] [--out <dir>]):
  init                       create the tables
  ingest [--urls urls.txt] [--rename]   register every video in the video folder; with --urls, match files to links by YouTube title
  link REF URL               attach a link (and its YouTube title) to a reference by hand
  cuts [--th 0.30]           hard-cut detection, one row per shot, one thumbnail per shot
  refine [--min 4]           second pass inside long shots (dark scenes hide soft cuts): adds sub-shots <id>a, b, c
  sheets                     one labelled contact sheet per reference
  transitions                transition candidates (WHIP, MATCH, FLASH, DIP); keeps verdicts from earlier runs
  strips                     8-frame strip per candidate + review sheets of 12
  verdict ID TOP|GOOD|NO KIND "note"     record the human review of one candidate
  tag CLIP TAG "note"        tag a shot (product, sneakers, hands, logo ...)
  group REF GROUP            set a reference's style group
  grammar REF "structure" "devices" "what we take"
  rhythm                     shot-length stats, pace by quarter, cuts on audio hits, barcode image per reference
  library                    LIBRARY.html (transitions by kind with AI recipes, rhythm, tagged shots)
  clips transitions|tag:NAME --pool pool.json [--pad 1.0]   Resolve clip_infos JSON for a library timeline
  report                     one-screen summary
"""
import argparse, json, math, pathlib, re, sqlite3, subprocess, sys, tempfile, urllib.request, urllib.parse, difflib, html

SCHEMA = """
CREATE TABLE IF NOT EXISTS reference_videos(ref_id TEXT PRIMARY KEY, source_url TEXT, kind TEXT, title TEXT, channel TEXT,
  duration_s REAL, width INT, height INT, fps REAL, file TEXT, status TEXT, style_group TEXT, notes TEXT);
CREATE TABLE IF NOT EXISTS ref_clips(clip_id TEXT PRIMARY KEY, ref_id TEXT, parent_id TEXT, tc_in TEXT, tc_out TEXT,
  start_s REAL, end_s REAL, dur_s REAL, thumb TEXT, description TEXT, motion TEXT, style_group TEXT);
CREATE TABLE IF NOT EXISTS transitions(trans_id TEXT PRIMARY KEY, ref_id TEXT, type TEXT, frame INT, t_s REAL, tc TEXT,
  clip_out TEXT, clip_in TEXT, score REAL, strip TEXT, verdict TEXT, kind TEXT, notes TEXT);
CREATE TABLE IF NOT EXISTS shot_tags(clip_id TEXT, tag TEXT, note TEXT, PRIMARY KEY(clip_id, tag));
CREATE TABLE IF NOT EXISTS edit_stats(ref_id TEXT PRIMARY KEY, shots INT, duration_s REAL, cuts_per_min REAL, asl_mean REAL,
  asl_median REAL, shortest REAL, longest REAL, pct_under_05 REAL, pct_over_3 REAL, q1_asl REAL, q2_asl REAL, q3_asl REAL,
  q4_asl REAL, pace_shape TEXT, cuts_on_onset_pct REAL, onset_bpm REAL, barcode TEXT);
CREATE TABLE IF NOT EXISTS edit_grammar(ref_id TEXT PRIMARY KEY, structure TEXT, devices TEXT, steal TEXT);
"""
KINDS = [
 ("PORTAL", "Portal", "Camera or subject falls into another world (painting, screen, print).",
  "Clip A ends with the camera flying at a flat surface; clip B starts inside that world on the same motion vector and speed."),
 ("SPIN", "Spin / roll", "Camera rolls 90-180 degrees (or the product flips) and lands in the next space.",
  "End A mid-roll with motion blur, start B mid-roll in the same direction; cut on the fastest frame."),
 ("WHIP_PAN", "Whip pan", "A fast pan smears the frame and lands on the next subject.",
  "Last 4-6 frames of A and first 4-6 of B are a horizontal smear in ONE direction; cut inside the blur."),
 ("WHIP", "Smear cut", "The cut hides inside an action blur (swing, head turn, run).",
  "Cut on the fastest frame of the action; B starts already blurred and settles within 6 frames."),
 ("PUSH_IN", "Push-in / dive", "Macro push into an object until its texture becomes the next scene.",
  "A: slow push-in to macro on a texture. B: start on the same texture and pull back to reveal the new place."),
 ("OBJECT_WIPE", "Object wipe", "An object crosses the lens (page, note, card) and wipes to the next shot.",
  "A ends with the object passing close to the lens; B starts as it clears frame. Same object colour in both."),
 ("BODY_WIPE", "Body / fabric wipe", "A body or fabric passes the lens, the frame goes dark or blurred, new shot.",
  "A ends with fabric filling the frame, B starts with fabric leaving the frame in the same direction."),
 ("CAMERA_BLOCK", "Lens block", "Something hits or covers the lens (thrown object, jump over camera), black, new scene.",
  "End A on a full black or full blur frame, start B from black; ultra-wide low angle sells it."),
 ("FLASH", "Flash / flare", "A light burst or flare covers the cut.",
  "2-4 frames of white or coloured flare between shots; in generation ask for a flare peak at the end of A."),
 ("ECHO", "Echo trails", "Multi-exposure ghost trails of a moving body.",
  "Generate a clean move on a dark set, then stack 4-6 delayed copies with lighten blend in the edit."),
 ("MATCH_CUT", "Match cut", "Same shape, position or object across two different worlds.",
  "Lock the object's position and size in both first frames; change only the world."),
 ("GRAPHIC_MATCH", "Graphic match", "A graphic element (clock digits, countdown, UI) carries over the cut.",
  "Repeat a readout with the same framing as a chapter marker."),
 ("PRODUCT_PUSH", "Product push", "The product physically enters the next space (slot, door, hand).",
  "A: the product pushed toward a gap; B: it arrives inside at the same speed."),
 ("PUNCH_IN", "Punch-in", "Same axis, tighter framing.", "Generate one master and crop, or re-generate tighter on the same axis."),
 ("GRAPHIC_SLIDE", "Graphic slide", "A colour block slides across.", "Edit-only (HyperFrames or the NLE), not in generation."),
 ("DISSOLVE", "Dissolve", "Soft blend between two shots.", "Edit-only."),
]

def args():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd"); ap.add_argument("rest", nargs="*")
    ap.add_argument("--root", required=True); ap.add_argument("--db"); ap.add_argument("--video-dir"); ap.add_argument("--out")
    ap.add_argument("--urls"); ap.add_argument("--th", type=float, default=0.30); ap.add_argument("--min", type=float, default=4.0)
    ap.add_argument("--pool"); ap.add_argument("--pad", type=float, default=1.0); ap.add_argument("--fps", type=float, default=24.0)
    ap.add_argument("--rename", action="store_true")
    return ap.parse_args()

A = args()
ROOT = pathlib.Path(A.root).expanduser().resolve()
DB = pathlib.Path(A.db).expanduser() if A.db else ROOT / "DATABASE" / "edit_library.db"
VID = pathlib.Path(A.video_dir).expanduser() if A.video_dir else ROOT / "01_REFERENCES" / "EXTERNAL" / "VIDEO"
OUT = pathlib.Path(A.out).expanduser() if A.out else ROOT / "01_REFERENCES" / "EXTERNAL" / "ANALYSIS"
DB.parent.mkdir(parents=True, exist_ok=True); OUT.mkdir(parents=True, exist_ok=True)
db = sqlite3.connect(DB); db.executescript(SCHEMA)
for t, c in (("ref_clips", "parent_id TEXT"), ("ref_clips", "thumb TEXT"), ("transitions", "kind TEXT"), ("transitions", "frame INT"),
             ("reference_videos", "style_group TEXT"), ("ref_clips", "style_group TEXT")):
    try: db.execute(f"ALTER TABLE {t} ADD COLUMN {c}")
    except sqlite3.OperationalError: pass
rel = lambda p: str(pathlib.Path(p).resolve().relative_to(ROOT))
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".mkv", ".webm"}

def tc(t, fps):
    f = round(t * fps); r = round(fps)
    return f"{f//(r*3600):02d}:{f//(r*60)%60:02d}:{f//r%60:02d}:{f%r:02d}"

def probe(p):
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
        "stream=width,height,r_frame_rate:format=duration", "-of", "json", str(p)], capture_output=True, text=True).stdout)
    s = j["streams"][0]; n, d = s["r_frame_rate"].split("/")
    return s["width"], s["height"], round(int(n) / int(d), 3), round(float(j["format"]["duration"]), 2)

def thumb(src, t, dst):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(src), "-frames:v", "1", "-vf", "scale=-2:180", str(dst)])

def font(size=15):
    from PIL import ImageFont
    for f in ("/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        if pathlib.Path(f).exists(): return ImageFont.truetype(f, size)
    return ImageFont.load_default()

def refs():
    return db.execute("select ref_id, file, fps, duration_s, title from reference_videos where file is not null order by ref_id").fetchall()

def cmd_init():
    print("tables ready in", DB)

def cmd_ingest():
    known = {r[0] for r in db.execute("select file from reference_videos where file is not null")}
    n = db.execute("select count(*) from reference_videos").fetchone()[0]
    new = [p for p in sorted(VID.iterdir()) if p.suffix.lower() in VIDEO_EXT and not p.name.startswith("._") and rel(p) not in known]
    titles = {}
    if A.urls:  # match files to links by title (YouTube oEmbed, no login, no download)
        for u in [l.strip() for l in open(A.urls) if l.strip().startswith("http")]:
            try:
                q = "https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(u, safe="")
                d = json.load(urllib.request.urlopen(q, timeout=15)); titles[u] = (d["title"], d.get("author_name"))
            except Exception as e:
                print("no title for", u, e)
    for p in new:
        n += 1; ref = f"REF{n:02d}"; w, h, fps, dur = probe(p)
        url = title = ch = None
        if titles:
            stem = re.sub(r"[^a-z0-9 ]", " ", p.stem.lower())
            best = max(titles.items(), key=lambda kv: difflib.SequenceMatcher(None, stem, re.sub(r"[^a-z0-9 ]", " ", kv[1][0].lower())).ratio())
            if difflib.SequenceMatcher(None, stem, re.sub(r"[^a-z0-9 ]", " ", best[1][0].lower())).ratio() > 0.6:
                url, (title, ch) = best[0], best[1]
        if A.rename:
            slug = re.sub(r"[^A-Za-z0-9]+", "_", title or p.stem).strip("_")[:40]
            dst = p.with_name(f"{ref}_{slug}{p.suffix.lower()}")
            p.rename(dst); p = dst
        db.execute("insert into reference_videos(ref_id,source_url,kind,title,channel,duration_s,width,height,fps,file,status) values(?,?,?,?,?,?,?,?,?,?,?)",
                   (ref, url, "vertical" if h > w else "horizontal", title or p.stem, ch, dur, w, h, fps, rel(p), "ingested"))
        print(ref, f"{w}x{h}", fps, dur, p.name, "<-", url or "no link match")
    db.commit()
    if titles:
        used = {r[0] for r in db.execute("select source_url from reference_videos where source_url is not null")}
        for u, (t, _) in titles.items():
            if u not in used: print("NOT FOUND ON DISK:", t, u)

def cmd_link():
    ref, url = A.rest
    title = ch = None
    try:
        d = json.load(urllib.request.urlopen("https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(url, safe=""), timeout=15))
        title, ch = d["title"], d.get("author_name")
    except Exception as e:
        print("no title from oEmbed:", e)
    db.execute("update reference_videos set source_url=?, title=coalesce(?,title), channel=coalesce(?,channel) where ref_id=?", (url, title, ch, ref))
    db.commit(); print(ref, url, title or "")

def detect(src, th, start=None, dur=None):
    cmd = ["ffmpeg", "-hide_banner"] + (["-ss", f"{start:.3f}", "-t", f"{dur:.3f}"] if start is not None else []) + \
          ["-i", str(src), "-an", "-vf", f"select='gt(scene,{th})',showinfo", "-f", "null", "-"]
    return [float(x) for x in re.findall(r"pts_time:([0-9.]+)", subprocess.run(cmd, capture_output=True, text=True).stderr)]

def cmd_cuts():
    import concurrent.futures as cf
    (OUT / "thumbs").mkdir(exist_ok=True)
    rows = refs()
    with cf.ThreadPoolExecutor(6) as ex:
        found = dict(zip([r[0] for r in rows], ex.map(lambda r: detect(ROOT / r[1], A.th), rows)))
    for ref, f, fps, dur, _ in rows:
        pts = [0.0]
        for c in found[ref]:
            if c - pts[-1] >= 0.25 and dur - c >= 0.25: pts.append(c)
        pts.append(dur)
        db.execute("delete from ref_clips where ref_id=?", (ref,))
        for i in range(len(pts) - 1):
            s, e = pts[i], pts[i + 1]; cid = f"{ref}_S{i+1:03d}"; th = OUT / "thumbs" / f"{cid}.jpg"
            thumb(ROOT / f, s + (e - s) / 2, th)
            db.execute("insert into ref_clips(clip_id,ref_id,tc_in,tc_out,start_s,end_s,dur_s,thumb,style_group) select ?,?,?,?,?,?,?,?,style_group from reference_videos where ref_id=?",
                       (cid, ref, tc(s, fps), tc(e, fps), round(s, 3), round(e, 3), round(e - s, 3), rel(th), ref))
        print(ref, len(pts) - 1, "shots")
    db.commit()

def cmd_refine():
    db.execute("delete from ref_clips where parent_id is not null"); total = 0
    for cid, ref, s, e, fps, f in db.execute("""select c.clip_id,c.ref_id,c.start_s,c.end_s,r.fps,r.file from ref_clips c join reference_videos r using(ref_id)
            where c.dur_s>=? and c.parent_id is null order by c.clip_id""", (A.min,)).fetchall():
        pts = [s]
        for c in [s + x for x in detect(ROOT / f, 0.12, s, e - s)]:
            if c - pts[-1] >= 0.4 and e - c >= 0.4: pts.append(c)
        if len(pts) < 2: continue
        pts.append(e)
        for i in range(len(pts) - 1):
            sub = f"{cid}{chr(97+i)}"; a, b = pts[i], pts[i + 1]; th = OUT / "thumbs" / f"{sub}.jpg"
            thumb(ROOT / f, a + (b - a) / 2, th)
            db.execute("insert into ref_clips(clip_id,ref_id,parent_id,tc_in,tc_out,start_s,end_s,dur_s,thumb,style_group) select ?,ref_id,?,?,?,?,?,?,?,style_group from ref_clips where clip_id=?",
                       (sub, cid, tc(a, fps), tc(b, fps), round(a, 3), round(b, 3), round(b - a, 3), rel(th), cid))
        total += len(pts) - 1; print(cid, "->", len(pts) - 1, "sub-shots")
    db.commit(); print("sub-shots:", total)

def cmd_sheets():
    from PIL import Image, ImageDraw
    F = font(); (OUT / "sheets").mkdir(exist_ok=True); TW, TH, COLS, HEAD = 320, 180, 8, 34
    for ref, _, _, _, title in refs():
        rows = db.execute("select clip_id,tc_in,dur_s,thumb from ref_clips where ref_id=? and parent_id is null order by start_s", (ref,)).fetchall()
        if not rows: continue
        r = (len(rows) + COLS - 1) // COLS
        sheet = Image.new("RGB", (COLS * TW, HEAD + r * TH), "black"); d = ImageDraw.Draw(sheet)
        d.text((8, 8), f"{ref}  {title}  ({len(rows)} shots)", fill="white", font=F)
        for k, (cid, tcin, dur, th) in enumerate(rows):
            im = Image.open(ROOT / th).convert("RGB"); im.thumbnail((TW, TH))
            x, y = (k % COLS) * TW, HEAD + (k // COLS) * TH
            sheet.paste(im, (x + (TW - im.width) // 2, y + (TH - im.height) // 2))
            lab = f"{cid.split('_')[-1]}  {tcin}  {dur:.1f}s"
            d.rectangle((x, y, x + d.textlength(lab, font=F) + 10, y + 22), fill=(0, 0, 0)); d.text((x + 5, y + 3), lab, fill="white", font=F)
        sheet.save(OUT / "sheets" / f"{ref}.jpg", quality=82); print("sheet", ref, len(rows))

def gray_frames(path, W=96, H=54):
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"scale={W}:{H},format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)

def cmd_transitions():
    import numpy as np
    old = {(r[0], r[1], r[2]): r[3:] for r in db.execute("select ref_id,type,frame,verdict,kind,notes,strip from transitions")}
    db.execute("delete from transitions")
    def sharp(f):
        lap = f[1:-1, 1:-1] * 4 - f[:-2, 1:-1] - f[2:, 1:-1] - f[1:-1, :-2] - f[1:-1, 2:]; return lap.var()
    def corr(a, b):
        a = a - a.mean(); b = b - b.mean(); d = np.sqrt((a * a).sum() * (b * b).sum()); return float((a * b).sum() / d) if d > 0 else 0.0
    for ref, f, fps, dur, _ in refs():
        F = gray_frames(ROOT / f); n = len(F)
        if n < 10: continue
        S = np.array([sharp(x) for x in F]); B = F.mean(axis=(1, 2)); D = np.r_[0, np.abs(np.diff(F, axis=0)).mean(axis=(1, 2))]
        med = np.median(S) + 1e-6
        shots = db.execute("select clip_id,start_s from ref_clips where ref_id=? and parent_id is null order by start_s", (ref,)).fetchall()
        cuts = [(shots[i][0], shots[i + 1][0], round(shots[i + 1][1] * fps)) for i in range(len(shots) - 1)]
        cf_ = {c[2] for c in cuts}; cand = []
        for o, i_, k in cuts:
            if k < 4 or k > n - 4: continue
            blur = 1 - min(1, np.mean(np.r_[S[k-3:k], S[k:k+3]]) / med)
            sim = max(corr(F[k-1], F[k]), corr(F[k-1], F[min(n-1, k+2)]))
            if blur > 0.55: cand.append(("WHIP", k, round(float(blur), 3), o, i_))
            if sim > 0.55: cand.append(("MATCH", k, round(sim, 3), o, i_))
        for i in range(3, n - 3):
            if any(abs(i - c) < 6 for c in cf_): continue
            if S[i] < 0.2 * med and D[i] > 2 * np.median(D) + 1 and S[i-3] > 0.5 * med: cand.append(("WHIP", i, round(float(1 - S[i] / med), 3), None, None))
            if B[i] - np.median(B[max(0, i-12):i]) > 60: cand.append(("FLASH", i, round(float(B[i]), 1), None, None))
            if (B[i] < 8 or B[i] > 245) and abs(B[i-3] - B[i]) > 40: cand.append(("DIP", i, round(float(B[i]), 1), None, None))
        cand.sort(key=lambda c: (c[0], c[1])); kept = []
        for c in cand:
            if kept and kept[-1][0] == c[0] and c[1] - kept[-1][1] < fps / 2:
                if c[2] > kept[-1][2]: kept[-1] = c
                continue
            kept.append(c)
        for j, (typ, k, sc, o, i_) in enumerate(kept):
            t = k / fps
            if o is None:
                row = db.execute("select clip_id from ref_clips where ref_id=? and parent_id is null and start_s<=? and end_s>?", (ref, t, t)).fetchone()
                o = i_ = row[0] if row else None
            v = old.get((ref, typ, k), (None, None, None, None))
            db.execute("insert into transitions(trans_id,ref_id,type,frame,t_s,tc,clip_out,clip_in,score,verdict,kind,notes,strip) values(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                       (f"{ref}_T{j+1:03d}", ref, typ, k, round(t, 3), tc(t, fps), o, i_, sc, *v))
        print(ref, {t: sum(1 for c in kept if c[0] == t) for t in ("WHIP", "MATCH", "FLASH", "DIP")})
    db.commit()

def cmd_strips():
    from PIL import Image, ImageDraw
    F = font(); O = OUT / "transitions"; O.mkdir(exist_ok=True); TW, TH, N = 200, 112, 8
    rows = db.execute("select t.trans_id,t.type,t.t_s,t.tc,t.score,r.file,r.title from transitions t join reference_videos r using(ref_id) order by t.type,t.trans_id").fetchall()
    tmp = pathlib.Path(tempfile.mkdtemp())
    for tid, typ, t, tcode, sc, f, title in rows:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0, t-0.5):.3f}", "-i", str(ROOT / f), "-vf",
                        f"fps={N},scale={TW}:{TH}:force_original_aspect_ratio=decrease,pad={TW}:{TH}:(ow-iw)/2:(oh-ih)/2", "-frames:v", str(N), str(tmp / f"{tid}_%02d.png")])
        strip = Image.new("RGB", (TW * N, TH + 22), "black"); d = ImageDraw.Draw(strip)
        for k in range(N):
            p = tmp / f"{tid}_{k+1:02d}.png"
            if p.exists(): strip.paste(Image.open(p), (k * TW, 22))
        d.text((4, 3), f"{tid}  {typ}  {tcode}  score {sc}  | {title[:60]}", fill="white", font=F)
        strip.save(O / f"{tid}.jpg", quality=80); db.execute("update transitions set strip=? where trans_id=?", (rel(O / f"{tid}.jpg"), tid))
    db.commit()
    for s in range(0, len(rows), 12):
        part = [O / f"{r[0]}.jpg" for r in rows[s:s+12]]; sheet = Image.new("RGB", (TW * N, (TH + 22) * len(part)), "black")
        for k, p in enumerate(part): sheet.paste(Image.open(p), (0, k * (TH + 22)))
        sheet.save(O / f"_review_{s//12+1:02d}.jpg", quality=80)
    print(len(rows), "strips,", (len(rows) + 11) // 12, "review sheets in", O)

def cmd_verdict():
    tid, v, kind, *note = A.rest
    db.execute("update transitions set verdict=?, kind=?, notes=? where trans_id=?", (v.upper(), kind.upper(), " ".join(note), tid)); db.commit(); print(tid, v, kind)

def cmd_tag():
    cid, tag, *note = A.rest
    db.execute("insert or replace into shot_tags values(?,?,?)", (cid, tag, " ".join(note))); db.commit(); print(cid, tag)

def cmd_group():
    ref, grp = A.rest
    db.execute("update reference_videos set style_group=? where ref_id=?", (grp, ref))
    db.execute("update ref_clips set style_group=? where ref_id=?", (grp, ref)); db.commit(); print(ref, grp)

def cmd_grammar():
    ref, st, dev, steal = A.rest
    db.execute("insert or replace into edit_grammar values(?,?,?,?)", (ref, st, dev, steal)); db.commit(); print(ref, "grammar saved")

def onsets(path, SR=11025, HOP=256):
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, np.float32)
    if len(x) < SR: return np.array([]), 0
    n = (len(x) - 1024) // HOP
    fr = np.lib.stride_tricks.as_strided(x, (n, 1024), (x.strides[0] * HOP, x.strides[0])) * np.hanning(1024)
    flux = np.maximum(0, np.diff(np.log1p(np.abs(np.fft.rfft(fr, axis=1))), axis=0)).sum(axis=1)
    flux = flux - np.convolve(flux, np.ones(43) / 43, "same"); flux[flux < 0] = 0; th = flux.mean() + 1.5 * flux.std()
    pk = [i for i in range(1, len(flux) - 1) if flux[i] > th and flux[i] >= flux[i-1] and flux[i] >= flux[i+1]]
    env = np.zeros(len(flux) + 2); env[np.array(pk, int)] = 1
    ac = np.correlate(env, env, "full")[len(env) - 1:]; lags = np.arange(len(ac)) * HOP / SR; ok = (lags > 60 / 180) & (lags < 60 / 70)
    bpm = 60 / lags[ok][np.argmax(ac[ok])] if ok.any() and ac[ok].max() > 0 else 0
    return np.array(pk) * HOP / SR, bpm

def cmd_rhythm():
    import numpy as np
    from PIL import Image, ImageDraw
    F = font(14); O = OUT / "rhythm"; O.mkdir(exist_ok=True)
    for ref, f, fps, dur, _ in refs():
        sh = db.execute("select start_s,dur_s from ref_clips where ref_id=? and parent_id is null order by start_s", (ref,)).fetchall()
        if not sh: continue
        L = np.array([d for _, d in sh]); st = np.array([s for s, _ in sh])
        qa = [round(float(L[(st >= dur*k/4) & (st < dur*(k+1)/4)].mean()), 2) if ((st >= dur*k/4) & (st < dur*(k+1)/4)).any() else None for k in range(4)]
        v = [x for x in qa if x]; shape = "flat"
        if len(v) >= 3:
            mid = [x for x in qa[1:3] if x]
            if qa[0] and mid and qa[0] > 1.4 * min(mid): shape = "accelerates"
            if mid and min(mid) < 0.6 * float(np.median(v)): shape = "fast middle peak"
            if qa[3] and qa[3] > 1.6 * float(np.median(v)): shape += " + long final hold"
        on, bpm = onsets(ROOT / f); cuts = st[1:]
        hit = round(100 * float(np.mean([np.min(np.abs(on - c)) < 0.07 for c in cuts]))) if len(on) and len(cuts) else None
        Wd, Hd = 1400, 90; img = Image.new("RGB", (Wd, Hd + 24), "white"); d = ImageDraw.Draw(img)
        for s, l in sh:
            x0 = int(s / dur * Wd); x1 = max(x0 + 1, int((s + l) / dur * Wd) - 1); h = int(min(1, 0.4 / max(l, 0.1)) * Hd)
            d.rectangle((x0, 24 + Hd - h, x1, 24 + Hd), fill=(30, 30, 30) if l >= 1 else (220, 60, 40))
        for c in on: d.line((int(c / dur * Wd), 20, int(c / dur * Wd), 24), fill=(40, 120, 220))
        d.text((4, 2), f"{ref}  {len(L)} shots  {60*len(L)/dur:.0f} cuts/min  median {np.median(L):.2f}s  on-hit {hit}%  ~{bpm:.0f} bpm  [{shape}]", fill="black", font=F)
        img.save(O / f"{ref}.png")
        db.execute("insert or replace into edit_stats values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (ref, len(L), dur, round(60 * len(L) / dur, 1), round(float(L.mean()), 2), round(float(np.median(L)), 2), round(float(L.min()), 2),
             round(float(L.max()), 2), round(100 * float((L < 0.5).mean())), round(100 * float((L > 3).mean())), *qa, shape, hit, round(float(bpm)), rel(O / f"{ref}.png")))
        print(ref, f"{60*len(L)/dur:.1f} cuts/min", shape, f"on-hit {hit}%")
    db.commit()

def cmd_library():
    e = html.escape; up = "../" * len(OUT.relative_to(ROOT).parts); r = lambda p: up + p if p else ""
    tr = db.execute("""select t.trans_id,t.kind,t.verdict,t.tc,t.notes,t.strip,v.title from transitions t join reference_videos v using(ref_id)
                       where t.verdict in ('TOP','GOOD') order by t.verdict desc,t.trans_id""").fetchall()
    st = db.execute("""select v.ref_id,v.title,v.style_group,s.shots,s.cuts_per_min,s.asl_median,s.pct_under_05,s.pace_shape,s.cuts_on_onset_pct,s.onset_bpm,s.barcode,
                       g.structure,g.devices,g.steal from reference_videos v left join edit_stats s using(ref_id) left join edit_grammar g using(ref_id) order by v.ref_id""").fetchall()
    tags = db.execute("select t.tag,t.clip_id,t.note,c.thumb,c.tc_in,c.dur_s from shot_tags t join ref_clips c using(clip_id) order by t.tag,t.clip_id").fetchall()
    nshots = db.execute("select count(*) from ref_clips where parent_id is null").fetchone()[0]
    o = ["""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Edit library</title><style>
:root{--bg:#111;--fg:#eee;--mute:#999;--card:#1b1b1b;--acc:#e8553d}body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.45 -apple-system,Helvetica,sans-serif}
header,main{max-width:1500px;margin:auto;padding:16px}h1{margin:0 0 4px;font-size:26px}h2{margin:36px 0 10px;font-size:20px;border-bottom:1px solid #333;padding-bottom:6px}
h3{margin:22px 0 4px;font-size:16px;color:var(--acc)}nav a{color:var(--mute);margin-right:14px}.recipe{color:var(--mute);margin:0 0 10px;max-width:900px}
.strip{background:var(--card);margin:0 0 10px;padding:6px;border-radius:6px}.strip img{width:100%;display:block}.strip p{margin:4px 2px 0;color:var(--mute);font-size:13px}
table{border-collapse:collapse;width:100%;font-size:13px}td,th{border-bottom:1px solid #2a2a2a;padding:6px;vertical-align:top;text-align:left}th{color:var(--mute);font-weight:500}
.bar img{width:100%;max-width:700px;background:#fff}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:8px}
.grid div{background:var(--card);border-radius:6px;overflow:hidden}.grid img{width:100%;display:block}.grid p{margin:4px 6px 6px;font-size:12px;color:var(--mute)}
</style></head><body><header><h1>Edit library</h1>""",
         f"<p style='color:var(--mute)'>{len(st)} references, {nshots} shots, {len(tr)} selected transitions. Source: {e(rel(DB))}</p>",
         "<nav><a href='#trans'>Transitions</a><a href='#rhythm'>Edit rhythm</a>" + "".join(f"<a href='#tag-{e(t)}'>{e(t)}</a>" for t in sorted({x[0] for x in tags})) + "</nav></header><main><h2 id='trans'>Transitions</h2>"]
    for k, name, what, recipe in KINDS + [(k, k, "", "") for k in sorted({x[1] for x in tr if x[1]} - {k[0] for k in KINDS})]:
        rows = [x for x in tr if x[1] == k]
        if not rows: continue
        o.append(f"<h3>{e(name)} ({len(rows)})</h3><p class='recipe'>{e(what)}<br><b>AI recipe:</b> {e(recipe)}</p>")
        for tid, _, v, tcode, notes, strip, title in rows:
            o.append(f"<div class='strip'><img loading='lazy' src='{e(r(strip))}'><p><b>{tid}</b> {v} · {tcode} · {e(title)} · {e(notes or '')}</p></div>")
    o.append("<h2 id='rhythm'>Edit rhythm</h2><p class='recipe'>One bar per shot: width = length, height = speed, red = under 1 s; blue ticks = audio hits. On-hit = cuts within 70 ms of an audio hit.</p>"
             "<table><tr><th>Ref</th><th>Cuts/min</th><th>Median</th><th>&lt;0.5 s</th><th>Pace</th><th>On hit</th><th>Rhythm</th><th>Structure / devices / take</th></tr>")
    for ref, title, grp, n, cpm, med, u05, shape, onb, bpm, bar, s1, dev, steal in st:
        o.append(f"<tr><td><b>{ref}</b><br>{e(title or '')}<br><span style='color:var(--mute)'>{e(grp or '')} · {n} shots</span></td><td>{cpm}</td><td>{med} s</td><td>{u05}%</td>"
                 f"<td>{e(shape or '')}</td><td>{onb}% · ~{bpm} bpm</td><td class='bar'>{f'<img loading=lazy src={chr(39)}{e(r(bar))}{chr(39)}>' if bar else ''}</td>"
                 f"<td>{e(s1 or '')}<br><span style='color:var(--mute)'>Devices: {e(dev or '')}</span><br><b>Take:</b> {e(steal or '')}</td></tr>")
    o.append("</table>")
    for tg in sorted({x[0] for x in tags}):
        rows = [x for x in tags if x[0] == tg]
        o.append(f"<h2 id='tag-{e(tg)}'>{e(tg)} ({len(rows)})</h2><div class='grid'>")
        for _, cid, note, th, tcin, d in rows:
            o.append(f"<div><img loading='lazy' src='{e(r(th))}'><p><b>{cid}</b> · {tcin} · {d:.1f}s<br>{e(note or '')}</p></div>")
        o.append("</div>")
    o.append("</main></body></html>")
    (OUT / "LIBRARY.html").write_text("\n".join(o)); print(OUT / "LIBRARY.html")
    miss = [s for s in re.findall(r"src='([^']+)'", "\n".join(o)) if not (OUT / html.unescape(s)).exists()]
    print("missing images:", miss[:5] if miss else 0)

def cmd_clips():
    what = A.rest[0]; pool = json.load(open(A.pool)); TL = A.fps
    if what == "transitions":
        rows = db.execute("select trans_id,ref_id,t_s-?,t_s+?,kind from transitions where verdict in ('TOP','GOOD') order by kind,verdict desc,trans_id", (A.pad, A.pad)).fetchall()
    else:
        rows = db.execute("""select c.clip_id,c.ref_id,c.start_s,min(c.end_s,c.start_s+3.0),t.note from shot_tags t join ref_clips c using(clip_id)
                             where t.tag=? order by c.ref_id,c.start_s""", (what.split(":", 1)[1],)).fetchall()
    infos, idx, rec = [], [], 0
    for name, ref, s, e, label in rows:
        fps = db.execute("select fps from reference_videos where ref_id=?", (ref,)).fetchone()[0]
        s = max(0, s); n = round((e - s) * TL); sf = round(s * fps)
        ef = sf + (n if abs(fps - TL) < 0.1 else math.ceil(n * fps / TL) + 1)  # end is exclusive; spare frame for rate conform
        infos.append({"clip_id": pool[ref], "start_frame": sf, "end_frame": ef, "record_frame": rec})
        idx.append(f"{rec}\t{rec/TL:.2f}\t{name}\t{label or ''}"); rec += n
    (OUT / f"clips_{what.replace(':', '_')}_index.tsv").write_text("record_frame\tsec\tid\tlabel\n" + "\n".join(idx) + "\n")
    print(json.dumps(infos)); print(len(infos), "items", round(rec / TL, 1), "s; index:", OUT / f"clips_{what.replace(':', '_')}_index.tsv", file=sys.stderr)

def cmd_report():
    q = lambda s: db.execute(s).fetchone()[0]
    print("references:", q("select count(*) from reference_videos"), "| shots:", q("select count(*) from ref_clips where parent_id is null"),
          "| sub-shots:", q("select count(*) from ref_clips where parent_id is not null"))
    print("transitions:", dict(db.execute("select coalesce(verdict,'unreviewed'),count(*) from transitions group by 1").fetchall()))
    print("tags:", dict(db.execute("select tag,count(*) from shot_tags group by 1").fetchall()))
    print("rhythm rows:", q("select count(*) from edit_stats"), "| grammar rows:", q("select count(*) from edit_grammar"))

{"init": cmd_init, "ingest": cmd_ingest, "link": cmd_link, "cuts": cmd_cuts, "refine": cmd_refine, "sheets": cmd_sheets, "transitions": cmd_transitions,
 "strips": cmd_strips, "verdict": cmd_verdict, "tag": cmd_tag, "group": cmd_group, "grammar": cmd_grammar, "rhythm": cmd_rhythm,
 "library": cmd_library, "clips": cmd_clips, "report": cmd_report}[A.cmd]()
