#!/usr/bin/env python3
"""Check that every media path a project refers to is really there, on the real drive.

Usage:
  python3 verify_media.py <paths or files...> [--json report.json] [--rewrite OLD_PREFIX NEW_PREFIX --from FILE --to NEWFILE]

Inputs can be: media paths; a .txt/.csv/.md list (one path per line or any absolute path inside the text);
a .json file (every string value that looks like an absolute path is collected, at any depth);
an .fcpxml / .xml / .edl / .html file (file:// URLs, src="..." and absolute paths are collected).

Status per path:
  ok       exists, and if it is under /Volumes/<name>, that volume is a real mount
  missing  not found (drive unplugged, renamed, or remounted as "<name> 1")
  phantom  the path resolves, but /Volumes/<name> is a plain folder on the boot disk, not the drive.
           Files there may be a stale or partial copy written while the drive was away.

For missing/phantom paths it suggests relinks to a mounted volume where the same relative path exists
(e.g. /Volumes/MyDrive -> /Volumes/MyDrive 1). It never relinks on its own. --rewrite writes a NEW copy
of one text/JSON file with the prefix replaced, only to a file that does not exist yet.
Python 3 stdlib only.
"""
import argparse
import json
import os
import re
import sys
from urllib.parse import unquote

VOL = "/Volumes"
PATH_RE = re.compile(r"(?:file://)?(/(?:Volumes|Users|private|tmp|mnt|media|home)/[^\"'<>\n\r\t|]+?\.[A-Za-z0-9]{2,5})(?=[\"'<>\s|,;)]|$)")
MEDIA_EXT = {".mp4", ".mov", ".m4v", ".mkv", ".webm", ".avi", ".mxf", ".wav", ".mp3", ".aif", ".aiff", ".m4a",
             ".flac", ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".exr", ".dpx", ".psd", ".webp", ".heic", ".srt", ".json"}


def collect(arg):
    if not os.path.isfile(arg) or os.path.splitext(arg)[1].lower() in MEDIA_EXT - {".json"}:
        return [arg]
    ext = os.path.splitext(arg)[1].lower()
    with open(arg, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    found = []
    if ext == ".json":
        try:
            def walk(x):
                if isinstance(x, dict):
                    for v in x.values():
                        walk(v)
                elif isinstance(x, list):
                    for v in x:
                        walk(v)
                elif isinstance(x, str) and x.startswith(("/", "file://")):
                    found.append(unquote(x[7:] if x.startswith("file://") else x))
            walk(json.loads(text))
            return found
        except ValueError:
            pass
    for m in PATH_RE.finditer(text):
        found.append(unquote(m.group(1)).strip())
    return found


def volume_of(path):
    parts = path.split("/")
    return "/".join(parts[:3]) if path.startswith(VOL + "/") and len(parts) > 2 else None


def status(path):
    vol = volume_of(path)
    if vol and os.path.isdir(vol) and not os.path.ismount(vol):
        return "phantom" if os.path.exists(path) else "missing"
    return "ok" if os.path.exists(path) else "missing"


def suggestions(path):
    vol = volume_of(path)
    if not vol or not os.path.isdir(VOL):
        return []
    rel = path[len(vol):]
    base = os.path.basename(vol)
    out = []
    for name in sorted(os.listdir(VOL)):
        cand = os.path.join(VOL, name)
        if cand == vol or not os.path.ismount(cand):
            continue
        if (name.startswith(base) or base.startswith(name)) and os.path.exists(cand + rel):
            out.append([vol, cand])
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--json")
    ap.add_argument("--rewrite", nargs=2, metavar=("OLD_PREFIX", "NEW_PREFIX"))
    ap.add_argument("--from", dest="src")
    ap.add_argument("--to", dest="dst")
    a = ap.parse_args()

    if a.rewrite:
        if not (a.src and a.dst):
            sys.exit("--rewrite needs --from FILE --to NEWFILE")
        if os.path.exists(a.dst):
            sys.exit("refusing to overwrite %s" % a.dst)
        with open(a.src, encoding="utf-8") as fh:
            text = fh.read()
        n = text.count(a.rewrite[0])
        with open(a.dst, "w", encoding="utf-8") as fh:
            fh.write(text.replace(a.rewrite[0], a.rewrite[1]))
        print("wrote %s (%d occurrences of %s -> %s). Re-run the check on it." % (a.dst, n, a.rewrite[0], a.rewrite[1]))
        return

    paths = []
    for inp in a.inputs:
        paths += collect(inp)
    seen, rows = set(), []
    for p in paths:
        p = os.path.normpath(p)
        if p in seen:
            continue
        seen.add(p)
        rows.append({"path": p, "status": status(p), "relink": suggestions(p) if status(p) != "ok" else []})
    phantoms = sorted({volume_of(r["path"]) for r in rows if r["status"] == "phantom"} |
                      {volume_of(r["path"]) for r in rows if volume_of(r["path"]) and os.path.isdir(volume_of(r["path"]))
                       and not os.path.ismount(volume_of(r["path"]))})
    relinks = sorted({tuple(s) for r in rows for s in r["relink"]})
    counts = {k: sum(1 for r in rows if r["status"] == k) for k in ("ok", "missing", "phantom")}
    for r in rows:
        if r["status"] != "ok":
            print("%-8s %s" % (r["status"].upper(), r["path"]))
    print("\n%d paths: %d ok, %d missing, %d phantom" % (len(rows), counts["ok"], counts["missing"], counts["phantom"]))
    for v in phantoms:
        try:
            n = len(os.listdir(v))
        except OSError:
            n = -1
        print("PHANTOM VOLUME FOLDER: %s is a folder on the boot disk, not a mounted drive (%d entries inside). "
              "Do not delete it if it holds files; ask the owner." % (v, n))
    for old, new in relinks:
        print("SUGGESTED RELINK (needs the user's yes): %s -> %s" % (old, new))
    if a.json:
        with open(a.json, "w") as fh:
            json.dump({"counts": counts, "rows": rows, "phantom_volumes": phantoms, "suggested_relinks": relinks}, fh, indent=2)
    sys.exit(0 if counts["missing"] == 0 and counts["phantom"] == 0 else 1)


if __name__ == "__main__":
    main()
