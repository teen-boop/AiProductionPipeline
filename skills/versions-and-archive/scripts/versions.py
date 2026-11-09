#!/usr/bin/env python3
"""Versions, archive and disk clean-up for a project. Dry run by default; --apply to act.

  supersede --target FILE --with NEWFILE [--apply]
        old FILE -> <dir>/_previous/<stem>_v01_<YYYYMMDD><ext>, NEWFILE copied to FILE's exact path and name
  report    --project P
        space used by _previous, _rejected, caches/proxies, temp files, duplicate content, rejected-but-not-moved takes
  archive   --project P --what previous|rejected|delivered|generated [--dest DIR] [--apply] [--trash-source]
        copy to DIR (default P/99_ARCHIVE) keeping relative paths, verify SHA-256, write ARCHIVE_MANIFEST.csv;
        sources go to the Finder Trash only with --trash-source, only after every copy verified
"""
import argparse, csv, hashlib, json, os, re, shutil, subprocess, sys, time
from collections import defaultdict

CACHE_RE = re.compile(r"^(CacheClip|Render ?Cache|Optimized ?Media|Proxy|Proxies|\.cache|__pycache__|node_modules|"
                      r"Media Cache|Media Cache Files|Peak Files|Auto-Save)$", re.I)
TEMP_RE = re.compile(r"(^_.*tmp|_tmp\.|\.tmp$|\.part$|\.crdownload$|^~\$)", re.I)
MEDIA = {".mp4", ".mov", ".m4v", ".webm", ".png", ".jpg", ".jpeg", ".webp", ".wav", ".mp3", ".exr", ".tif", ".tiff"}


def human(n):
    for u in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f} {u}"
        n /= 1024
    return f"{n:.1f} PB"


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def qhash(p):
    h, size = hashlib.sha1(), os.path.getsize(p)
    with open(p, "rb") as f:
        h.update(f.read(1 << 20))
        if size > 2 << 20:
            f.seek(-(1 << 20), 2); h.update(f.read(1 << 20))
    return f"{size}:{h.hexdigest()}"


def dir_size(d):
    t = 0
    for dp, _, fns in os.walk(d):
        for f in fns:
            try:
                t += os.path.getsize(os.path.join(dp, f))
            except OSError:
                pass
    return t


def trash(path):
    """Finder Trash: recoverable, unlike rm."""
    script = f'tell application "Finder" to delete POSIX file "{os.path.abspath(path)}"'
    return subprocess.run(["osascript", "-e", script], capture_output=True).returncode == 0


def cmd_supersede(a):
    tgt, new = os.path.abspath(a.target), os.path.abspath(a.with_)
    if not os.path.isfile(new):
        sys.exit(f"missing new file {new}")
    prev = os.path.join(os.path.dirname(tgt), "_previous")
    stem, ext = os.path.splitext(os.path.basename(tgt))
    n = 1
    while any(f.startswith(f"{stem}_v{n:02d}_") for f in (os.listdir(prev) if os.path.isdir(prev) else [])):
        n += 1
    old_dest = os.path.join(prev, f"{stem}_v{n:02d}_{time.strftime('%Y%m%d')}{ext}")
    if os.path.exists(tgt) and qhash(tgt) == qhash(new):
        print("same content already in place: nothing to do"); return
    print(("" if os.path.exists(tgt) else "(no current file) ") + f"old -> {old_dest}\nnew -> {tgt}")
    if not a.apply:
        print("dry run. Re-run with --apply after the user's yes."); return
    if os.path.exists(tgt):
        os.makedirs(prev, exist_ok=True); shutil.move(tgt, old_dest)
    shutil.copy2(new, tgt)
    print("done. Links and indexes that point at the final path still work.")


def walk(project):
    for dp, dns, fns in os.walk(project):
        yield dp, dns, fns


def cmd_report(a):
    P = os.path.abspath(a.project)
    buckets = defaultdict(lambda: [0, 0])
    caches, hashes = [], defaultdict(list)
    for dp, dns, fns in walk(P):
        for d in list(dns):
            full = os.path.join(dp, d)
            if CACHE_RE.match(d):
                s = dir_size(full); caches.append((s, full)); buckets["caches / proxies"][0] += s; buckets["caches / proxies"][1] += 1
                dns.remove(d)
            elif d == "_previous":
                s = dir_size(full); buckets["_previous versions"][0] += s; buckets["_previous versions"][1] += 1
            elif d == "_rejected":
                s = dir_size(full); buckets["_rejected takes"][0] += s; buckets["_rejected takes"][1] += 1
        if os.sep + "99_ARCHIVE" in dp:
            continue
        for f in fns:
            p = os.path.join(dp, f)
            try:
                size = os.path.getsize(p)
            except OSError:
                continue
            if TEMP_RE.search(f):
                buckets["temp / partial files"][0] += size; buckets["temp / partial files"][1] += 1
            if os.path.splitext(f)[1].lower() in MEDIA and size > 256 << 10:
                hashes[qhash(p)].append(p)
    dup_bytes, dup_groups, edit_copies = 0, [], 0
    for h, ps in hashes.items():
        if len(ps) > 1:
            in_edit = [p for p in ps if os.sep + "04_EDIT" + os.sep in p]
            extra = len(ps) - 1
            edit_copies += len(in_edit)
            dup_bytes += int(h.split(":")[0]) * extra
            dup_groups.append(ps)
    buckets["duplicate content (extra copies)"] = [dup_bytes, len(dup_groups)]
    log = os.path.join(P, "03_GENERATED", "GENERATION_LOG.jsonl")
    rej_out = []
    if os.path.exists(log):
        st = {}
        for line in open(log):
            if line.strip():
                r = json.loads(line); st.setdefault(r["id"], {}).update(r)
        rej_out = [r["file"] for r in st.values() if r.get("status") == "rejected" and r.get("file")
                   and os.path.exists(r["file"]) and "_rejected" not in r["file"]]
    print(f"project: {P}  total {human(dir_size(P))}")
    for k, (s, n) in sorted(buckets.items(), key=lambda x: -x[1][0]):
        print(f"  {k:34} {human(s):>10}  ({n})")
    if edit_copies:
        print(f"  note: {edit_copies} duplicates are edit-bin copies in 04_EDIT (intended while editing)")
    for s, d in sorted(caches, reverse=True)[:10]:
        print(f"  CACHE {human(s):>10}  {d}")
    for ps in sorted(dup_groups, key=lambda g: -os.path.getsize(g[0]))[:10]:
        print(f"  DUP x{len(ps)} {human(os.path.getsize(ps[0])):>10}  " + "  |  ".join(os.path.relpath(p, P) for p in ps[:3]))
    for f in rej_out[:10]:
        print("  REJECTED NOT MOVED:", f)
    print("nothing was changed. Caches can be rebuilt by the editor; deleting them is the user's call.")


def select(P, what):
    out = []
    for dp, dns, fns in walk(P):
        if os.sep + "99_ARCHIVE" in dp + os.sep:
            dns[:] = []; continue
        parts = set(os.path.relpath(dp, P).split(os.sep))
        hit = (what == "previous" and "_previous" in parts) or (what == "rejected" and "_rejected" in parts) or \
              (what == "delivered" and "06_DELIVERY" in parts) or (what == "generated" and "03_GENERATED" in parts)
        if hit:
            out += [os.path.join(dp, f) for f in fns if not f.startswith(".")]
    return out


def cmd_archive(a):
    P = os.path.abspath(a.project)
    dest = os.path.abspath(a.dest or os.path.join(P, "99_ARCHIVE"))
    files = select(P, a.what)
    total = sum(os.path.getsize(f) for f in files)
    print(f"{a.what}: {len(files)} files, {human(total)} -> {dest}")
    if not files:
        return
    free = shutil.disk_usage(os.path.dirname(dest) if not os.path.exists(dest) else dest).free
    if free < total * 1.05:
        sys.exit(f"not enough space at destination: {human(free)} free")
    if not a.apply:
        for f in files[:15]:
            print("  ", os.path.relpath(f, P))
        print("dry run. Re-run with --apply after the user's yes.")
        return
    man_path = os.path.join(dest, "ARCHIVE_MANIFEST.csv")
    new_man = not os.path.exists(man_path)
    os.makedirs(dest, exist_ok=True)
    ok = []
    with open(man_path, "a", newline="") as mf:
        w = csv.writer(mf)
        if new_man:
            w.writerow(["time", "what", "source", "archived", "size", "sha256", "verified"])
        for f in files:
            d = os.path.join(dest, os.path.relpath(f, P))
            os.makedirs(os.path.dirname(d), exist_ok=True)
            if not os.path.exists(d):
                shutil.copy2(f, d)
            hs, hd = sha256(f), sha256(d)
            good = hs == hd
            w.writerow([time.strftime("%Y-%m-%dT%H:%M:%S"), a.what, f, d, os.path.getsize(f), hs, good])
            if good:
                ok.append(f)
            else:
                print("VERIFY FAILED:", f)
    print(f"archived and verified {len(ok)}/{len(files)}. Manifest: {man_path}")
    if a.trash_source:
        if len(ok) != len(files):
            sys.exit("not every file verified: sources left in place")
        moved = sum(trash(f) for f in ok)
        print(f"sent {moved} source files to the Finder Trash (recoverable until the Trash is emptied)")
    else:
        print("sources left in place (use --trash-source after the user's yes to free the space)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("supersede"); s.add_argument("--target", required=True); s.add_argument("--with", dest="with_", required=True)
    s.add_argument("--apply", action="store_true")
    s = sp.add_parser("report"); s.add_argument("--project", required=True)
    s = sp.add_parser("archive"); s.add_argument("--project", required=True)
    s.add_argument("--what", required=True, choices=["previous", "rejected", "delivered", "generated"])
    s.add_argument("--dest"); s.add_argument("--apply", action="store_true"); s.add_argument("--trash-source", action="store_true")
    a = ap.parse_args()
    return {"supersede": cmd_supersede, "report": cmd_report, "archive": cmd_archive}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
