#!/usr/bin/env python3
"""Build a MANUAL GENERATION PACK: one folder per frame the user will generate by hand.

Each frame folder gets:
  PROMPT.txt      the full prompt — copy-paste as is (PROMPT_1.txt, PROMPT_2.txt … when a job asks for several shots:
                  one single-image prompt per shot, because hand-used models merge them into a split screen)
  ref_1_*.png …   reference images, numbered in the order to attach them
  ref_N_*.txt     a placeholder when the reference is a frame that is not generated yet
                  (contains a machine-readable line  WAITING_FOR: <job_id>#<n>)
  INFO.txt        what the frame is, how many images, attach order, where to save
  job.json        machine-readable job record (used by intake.py)
The user saves results into the same folder as RESULT_1.png, RESULT_2.png …

Jobs file (JSON list), one object per frame job:
  id       unique id                          (required)
  base     output file prefix, e.g. "C3_v3_train_"   (required)
  folder   destination folder in the project  (required)
  prompt   full prompt text                   (required)
  refs     list of image paths, or "@<job_id>#<n>" = the n-th result of another job
  after    list of job ids this one depends on (optional)
  status   only "pending" jobs are packed (default "pending")
  outputs  existing output paths (for done jobs that others reference)
  section  optional section folder name, e.g. "02_CLIMAX"

Usage:
  build_pack.py --jobs jobs.json --out PACK_DIR [--root PROJECT_ROOT] [--sections sections.json]
                [--head "text prepended to every prompt"] [--lang en] [--style-file STYLE.md]
sections.json: [["01_RECREATE", "^rec_"], ["02_CLIMAX", "^f\\d"], …] — first regex matching the job id wins;
jobs without a match go to the job's own "section" or "99_OTHER".
"""
import argparse, json, os, re, shutil, unicodedata

T = {
 "en": dict(frame="FRAME", what="WHAT", count="IMAGES", diff=" (different shots — Image 1, Image 2 …)", var=" variations of one scene",
            refs="REFERENCES — attach in this order:", norefs="REFERENCES: none (prompt only).",
            how="HOW: 1) copy the whole PROMPT.txt  2) attach ref_1, ref_2 … in order  3) generate",
            multi="HOW: this folder has {n} SEPARATE prompts — PROMPT_1.txt → save as RESULT_1.png, PROMPT_2.txt → RESULT_2.png … One generation per prompt, same references (ref_1, ref_2 … in order). Never put two shots in one image.",
            save="4) save the finished image(s) INTO THIS SAME FOLDER as RESULT_1.png{more} (best one = RESULT_1).",
            later="   Failed ones need not be saved. Intake will move RESULT files into the project.",
            dest="Goes into the project as", ready="ready start frame", wait="RESULT_{n}.png from folder {f} (generate that one first)",
            missing="NOT FOUND", ph="First generate the frame in folder {f}. Then attach its RESULT_{n}.png (or the best variant) as reference #{i}.",
            readme_title="# Manual generation pack", readme_body=[
             "Folders are in priority order. In every folder:",
             "- **PROMPT.txt** — copy it whole (if there are PROMPT_1.txt, PROMPT_2.txt … — each is a separate generation → RESULT_1.png, RESULT_2.png …);",
             "- **ref_1…, ref_2…** — attach in this order (a `.txt` instead of an image = a frame from another folder; do that folder first);",
             "- **INFO.txt** — what the frame is and how many images;",
             "- save the result **into the same folder** as `RESULT_1.png`, `RESULT_2.png` (best = RESULT_1).",
             "", "When results pile up, run intake (or ask Claude to \"collect the frames\")."],
            cols="| # | folder | images | refs | waits for | what |")
}
DEFAULT_HEAD = ("Generate the image immediately — do not search the web, do not research, do not ask questions, do not write a plan. "
                "ONE single full-frame 16:9 photograph filling the entire frame edge to edge — NOT a split screen, NOT a diptych, NOT side-by-side panels, NOT a grid or collage; "
                "no black bars, no letterbox, no borders, no vignette, no captions, no watermark.")


ONE = ("Generate exactly ONE single photograph — one full frame, NOT a split screen, NOT a diptych, NOT side-by-side panels, not a grid, not a collage.")


def split_prompt(prompt):
    """Hand-used image models draw "Image 1 / Image 2" requests as ONE split-screen picture.
    Return one standalone single-image prompt per "Image N —" line (or the whole prompt, made single-image)."""
    lines = prompt.strip().split("\n")
    shots = [(i, m.group(1)) for i, l in enumerate(lines) for m in [re.match(r"\s*Image (\d+)\s*[—–-]\s*", l)] if m]
    def single(text):
        text = re.sub(r"Generate exactly (\d+|two|three) (separate images|variations)[^.]*?(—[^.]*?)?\.", ONE, text)
        text = re.sub(r"Generate exactly ONE single photograph(?! — one full frame)[^.]*?\.", ONE, text)
        for a, b in [("Both images belong to the SAME scene, same light and colour grade.", "This photograph is one shot of a scene — keep its light and colour grade."),
                     ("both images are closer shots of the SAME moment", "this image is a closer shot of the SAME moment"),
                     ("Both images are closer shots of the SAME moment", "This image is a closer shot of the SAME moment"),
                     ("all three images continue the SAME scene", "this image continues the SAME scene"),
                     ("Both images", "This image"), ("both images", "this image")]:
            text = text.replace(a, b)
        return re.sub(r"\s+for Image \d+", "", text)
    if not shots:
        return [single(prompt.strip())]
    out = []
    for _, k in shots:
        keep = []
        for i, l in enumerate(lines):
            m = re.match(r"\s*Image (\d+)\s*[—–-]\s*(.*)", l)
            if m and m.group(1) != k:
                continue
            keep.append(f"THIS SHOT — {m.group(2)}" if m else l)
        out.append(single("\n".join(keep)))
    return out


def n_images(prompt):
    m = re.search(r"exactly (ONE|one|\d)", prompt)
    return 1 if (not m or m.group(1).lower() == "one") else int(m.group(1))


def scene_line(prompt, limit=260):
    body = re.split(r"OPTICS:|LOOK:", prompt)[0]
    lines = [l.strip() for l in body.split("\n") if l.strip()]
    keep = [l for l in lines if not l.startswith("Generate exactly") and "attached image" not in l[:60]] or lines
    txt = re.sub(r"^Generate exactly [^.]*\.\s*", "", " ".join(keep))
    return txt[:limit] + ("…" if len(txt) > limit else "")


def safe(name):
    return re.sub(r"[^\w.-]+", "_", unicodedata.normalize("NFC", name))[:60]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--root", default=None); ap.add_argument("--sections", default=None)
    ap.add_argument("--head", default=DEFAULT_HEAD); ap.add_argument("--lang", default="en", choices=list(T), help="add more languages to the T table")
    ap.add_argument("--style-file", default=None)
    a = ap.parse_args(); L = T[a.lang]
    jobs = json.load(open(a.jobs, encoding="utf-8")); root = a.root or os.path.dirname(os.path.abspath(a.out))
    rules = [(n, re.compile(rx)) for n, rx in json.load(open(a.sections, encoding="utf-8"))] if a.sections else []
    sec = lambda j: next((n for n, rx in rules if rx.search(j["id"])), j.get("section") or "99_OTHER")
    order_names = [n for n, _ in rules]
    sec_rank = lambda j: order_names.index(sec(j)) if sec(j) in order_names else len(order_names)

    if os.path.exists(a.out):
        for r, _, files in os.walk(a.out):
            if any(f.startswith("RESULT") for f in files):
                raise SystemExit(f"{r} has RESULT files — run intake.py first, the pack was not rebuilt.")
        shutil.rmtree(a.out, ignore_errors=True)
    os.makedirs(a.out)

    byid = {j["id"]: j for j in jobs}
    pend = sorted([j for j in jobs if j.get("status", "pending") == "pending"], key=sec_rank)
    placed, seq = set(), []
    def place(j):
        if j["id"] in placed: return
        for dep in j.get("after", []):
            if dep in byid and byid[dep].get("status", "pending") == "pending": place(byid[dep])
        placed.add(j["id"]); seq.append(j)
    for j in pend: place(j)

    folder_of, index = {}, []
    for k, j in enumerate(seq, 1):
        d = f"{a.out}/{sec(j)}/{k:03d}_{safe(j['base'].rstrip('_'))}"; os.makedirs(d); folder_of[j["id"]] = d
        refs = []
        for i, ref in enumerate(j.get("refs", []), 1):
            if ref.startswith("@"):
                pid, n = ref[1:].split("#"); par = byid.get(pid, {}); outs = par.get("outputs") or []
                if par.get("status") == "done" and len(outs) >= int(n) and os.path.exists(outs[int(n) - 1]):
                    src = outs[int(n) - 1]; shutil.copy(src, f"{d}/ref_{i}_{safe(os.path.basename(src))}")
                    refs.append(f"ref_{i} — {L['ready']} {os.path.basename(src)}")
                else:
                    pf = os.path.basename(folder_of.get(pid, pid))
                    open(f"{d}/ref_{i}_WAIT_RESULT_{n}_{safe(pf)}.txt", "w", encoding="utf-8").write(
                        L["ph"].format(f=pf, n=n, i=i) + f"\nWAITING_FOR: {pid}#{n}\n")
                    refs.append(f"ref_{i} — " + L["wait"].format(n=n, f=pf))
            elif os.path.exists(ref):
                shutil.copy(ref, f"{d}/ref_{i}_{safe(os.path.basename(ref))}")
                refs.append(f"ref_{i} — {os.path.relpath(ref, root)}")
            else:
                refs.append(f"ref_{i} — {L['missing']}: {ref}")
        n = j.get("n") or n_images(j["prompt"])
        parts = split_prompt(j["prompt"])
        if len(parts) == 1:
            open(f"{d}/PROMPT.txt", "w", encoding="utf-8").write(f"{a.head}\n\n{parts[0]}\n")
        else:
            for pi, pt in enumerate(parts, 1):
                open(f"{d}/PROMPT_{pi}.txt", "w", encoding="utf-8").write(f"{a.head}\n\n{pt}\n")
        info = [f"{L['frame']}: {j['base'].rstrip('_')}  ({j['id']})", "", f"{L['what']}: {scene_line(j['prompt'])}", "",
                f"{L['count']}: {n}" + (L["diff"] if "Image 1" in j["prompt"] else (L["var"] if n > 1 else "")), "",
                *( [L["refs"], *[f"  {x}" for x in refs]] if refs else [L["norefs"]] ), "",
                *( [L["multi"].format(n=len(parts))] if len(parts) > 1 else [L["how"], L["save"].format(more=", RESULT_2.png" if n > 1 else "")] ), L["later"], "",
                f"{L['dest']}: {os.path.relpath(j['folder'], root)}/{j['base']}N.png"]
        open(f"{d}/INFO.txt", "w", encoding="utf-8").write("\n".join(info) + "\n")
        json.dump({"id": j["id"], "folder": j["folder"], "base": j["base"], "n": n}, open(f"{d}/job.json", "w"), ensure_ascii=False, indent=1)
        deps = [os.path.basename(folder_of[x]) for x in j.get("after", []) if x in folder_of]
        index.append((sec(j), f"{k:03d}", os.path.basename(d), n, len(j.get("refs", [])), deps, scene_line(j["prompt"], 140)))

    if a.style_file and os.path.exists(a.style_file):
        shutil.copy(a.style_file, f"{a.out}/{os.path.basename(a.style_file)}")
    md = [L["readme_title"], "", *L["readme_body"], ""]
    cur = None
    for s, num, name, n, nr, deps, desc in index:
        if s != cur:
            md += ["", f"## {s}", "", L["cols"], "|---|---|---|---|---|---|"]; cur = s
        md.append(f"| {num} | `{name}` | {n} | {nr} | {', '.join(deps) or '—'} | {desc.replace('|', '/')} |")
    open(f"{a.out}/README.md", "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(f"{len(index)} frame folders in {a.out}")


if __name__ == "__main__":
    main()
