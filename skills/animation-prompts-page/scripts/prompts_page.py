"""animation-prompts-page: builds ONE browsable HTML page from an animation hand-off folder and its prompt list — every frame in order with
its picture, duration and prompt, a copy button, the end frame of a first/last-frame pair, block filters, search and a per-frame "done"
tick (kept in the browser's localStorage).

  python3 prompts_page.py <hand-off folder> [--prompts 000_PROMPTS.txt] [--out <page.html>] [--title "…"]

The prompt list format: entries separated by a line of "=" characters, the header line "<file>.png   (<duration>)", then the prompt.
Default --out is <folder>_PROMPTS.html NEXT TO the folder (sync scripts often delete unknown files inside the hand-off folder).
Image links are relative to the page and use the exact on-disk names (exFAT/SMB keep Cyrillic names NFD)."""
import argparse, html, json, os, re, unicodedata
from urllib.parse import quote

nfc = lambda s: unicodedata.normalize("NFC", s)
UI_RU = json.loads('{"content:\\"  \\u2713 done\\"": "content:\\"  \\u2713 \\u0433\\u043e\\u0442\\u043e\\u0432\\u043e\\"", "frames in storyboard order \\u00b7 __PAIRS__ Kling start \\u2192 end pairs \\u00b7 load the frame as the start frame, copy its prompt, 16:9, sound off.": "\\u043a\\u0430\\u0434\\u0440\\u043e\\u0432 \\u0432 \\u043f\\u043e\\u0440\\u044f\\u0434\\u043a\\u0435 \\u0440\\u0430\\u0441\\u043a\\u0430\\u0434\\u0440\\u043e\\u0432\\u043a\\u0438 \\u00b7 __PAIRS__ \\u043f\\u0430\\u0440 Kling \\u00ab\\u0441\\u0442\\u0430\\u0440\\u0442 \\u2192 \\u0444\\u0438\\u043d\\u0430\\u043b\\u00bb \\u00b7 \\u0437\\u0430\\u0433\\u0440\\u0443\\u0437\\u0438\\u0442\\u044c \\u043a\\u0430\\u0434\\u0440 \\u043a\\u0430\\u043a \\u0441\\u0442\\u0430\\u0440\\u0442\\u043e\\u0432\\u044b\\u0439, \\u0441\\u043a\\u043e\\u043f\\u0438\\u0440\\u043e\\u0432\\u0430\\u0442\\u044c \\u043f\\u0440\\u043e\\u043c\\u043f\\u0442, 16:9, \\u0437\\u0432\\u0443\\u043a \\u0432\\u044b\\u043a\\u043b\\u044e\\u0447\\u0435\\u043d.", "Search name or text\\u2026": "\\u041f\\u043e\\u0438\\u0441\\u043a \\u043f\\u043e \\u0438\\u043c\\u0435\\u043d\\u0438 \\u0438\\u043b\\u0438 \\u0442\\u0435\\u043a\\u0441\\u0442\\u0443\\u2026", "hide done": "\\u0441\\u043a\\u0440\\u044b\\u0442\\u044c \\u0433\\u043e\\u0442\\u043e\\u0432\\u044b\\u0435", "pairs only": "\\u0442\\u043e\\u043b\\u044c\\u043a\\u043e \\u043f\\u0430\\u0440\\u044b", "\\"All\\"": "\\"\\u0412\\u0441\\u0435\\"", "pair end frame \\u2192": "\\u0444\\u0438\\u043d\\u0430\\u043b\\u044c\\u043d\\u044b\\u0439 \\u043a\\u0430\\u0434\\u0440 \\u043f\\u0430\\u0440\\u044b \\u2192", "Kling pair: start + end": "\\u043f\\u0430\\u0440\\u0430 Kling: \\u0441\\u0442\\u0430\\u0440\\u0442 + \\u0444\\u0438\\u043d\\u0430\\u043b", "picture missing from the folder": "\\u043a\\u0430\\u0440\\u0442\\u0438\\u043d\\u043a\\u0438 \\u043d\\u0435\\u0442 \\u0432 \\u043f\\u0430\\u043f\\u043a\\u0435", "Copy prompt": "\\u041a\\u043e\\u043f\\u0438\\u0440\\u043e\\u0432\\u0430\\u0442\\u044c \\u043f\\u0440\\u043e\\u043c\\u043f\\u0442", "Unmark": "\\u0421\\u043d\\u044f\\u0442\\u044c \\u043e\\u0442\\u043c\\u0435\\u0442\\u043a\\u0443", "Done \\u2713": "\\u0413\\u043e\\u0442\\u043e\\u0432\\u043e \\u2713", "Copied": "\\u0421\\u043a\\u043e\\u043f\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u043e", "` \\u00b7 done ${": "` \\u00b7 \\u0433\\u043e\\u0442\\u043e\\u0432\\u043e ${", " of ${F.length} \\u00b7 shown ${shown}": " \\u0438\\u0437 ${F.length} \\u00b7 \\u043f\\u043e\\u043a\\u0430\\u0437\\u0430\\u043d\\u043e ${shown}"}')   # --lang ru: English UI string -> Russian


def parse(path):
    txt = open(path, encoding="utf-8").read()
    parts = re.split(r"^={20,}\n(.+?\.png)\s+\(([^)]*)\)\n={20,}\n", txt, flags=re.M)
    frames = []
    for i in range(1, len(parts), 3):
        name, dur, body = parts[i].strip(), parts[i + 1].strip(), parts[i + 2].strip()
        frames.append(dict(name=nfc(name), dur=dur, prompt=body))
    return frames


def block(name):
    m = re.match(r"(?:H\d+_)?(?:\d+[a-z]*_)?([A-Z]+\d*)_", name)
    if name.startswith("H"):
        return "HERO"
    return m.group(1) if m else "—"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("folder"); ap.add_argument("--prompts"); ap.add_argument("--out"); ap.add_argument("--title"); ap.add_argument("--lang", default="en", choices=["en", "ru"])
    a = ap.parse_args()
    A = os.path.abspath(a.folder).rstrip("/")
    txts = [f for f in os.listdir(A) if f.lower().endswith(".txt") and not f.startswith("._")]
    pr = a.prompts or (sorted(txts)[0] if txts else None)
    assert pr, "no prompt list (.txt) in the folder — pass --prompts"
    OUT = a.out or f"{A}_PROMPTS.html"
    rel = os.path.relpath(A, os.path.dirname(os.path.abspath(OUT)))
    disk = {nfc(f): f for f in os.listdir(A) if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")) and not f.startswith("._")}
    SRC = lambda n: quote(rel) + "/" + quote(disk.get(n, n))
    frames = parse(pr if os.path.isabs(pr) else f"{A}/{pr}")
    for i, f in enumerate(frames):
        f["src"] = quote(rel) + "/" + quote(disk.get(f["name"], f["name"]))
        f["block"] = block(f["name"])
        f["pair"] = "End frame = " in f["prompt"] and "start frame only" not in f["prompt"].lower()
        # the end frame is NAMED in the prompt ("End frame = the picture <file>" or "End frame = <number>"); "the NEXT picture" is legacy
        m = re.search(r"End frame = (?:the picture )?(\S+?\.png)", f["prompt"]) or re.search(r"End frame = (\d{4}[a-z]*|[A-Z]+\d+)\b", f["prompt"])
        j = None
        if m:
            key = nfc(m.group(1))
            j = next((k for k, g in enumerate(frames) if g["name"] == key or g["name"].startswith(key + "_")), None)
        elif "the NEXT picture" in f["prompt"] and "not in this folder" not in f["prompt"] and i + 1 < len(frames):
            j = i + 1
        if f["pair"] and j is not None:
            f["end"] = frames[j]["name"]
            f["endsrc"] = SRC(frames[j]["name"])
        f["missing"] = f["name"] not in disk
    blocks = []
    for f in frames:
        if f["block"] not in blocks:
            blocks.append(f["block"])
    data = json.dumps(frames, ensure_ascii=False)
    page = TEMPLATE.replace("__DATA__", data.replace("</", "<\\/")).replace("__BLOCKS__", json.dumps(blocks, ensure_ascii=False))
    title = html.escape(a.title or os.path.basename(A))
    page = page.replace("__TITLE__", title).replace("__KEY__", json.dumps("anim_done_" + nfc(A)))
    page = page.replace("__COUNT__", str(len(frames))).replace("__PAIRS__", str(sum(f["pair"] for f in frames)))
    if a.lang == "ru":
        for en, r in sorted(UI_RU.items(), key=lambda kv: -len(kv[0])):
            page = page.replace(en, r)
    page = page.replace("__LANG__", a.lang)
    open(OUT, "w", encoding="utf-8").write(page)
    print("wrote", OUT, len(frames), "frames,", sum(f["missing"] for f in frames), "missing pictures")


TEMPLATE = r"""<!doctype html><html lang="__LANG__"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<style>
:root{--bg:#070d11;--card:#0e171d;--line:#1d2a32;--text:#e9e2d6;--mute:#8b98a0;--gold:#c9962f;--done:#2f6b45;--rose:#f14fa0}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:15px/1.5 -apple-system,BlinkMacSystemFont,"Inter",sans-serif}
header{position:sticky;top:0;z-index:5;background:rgba(7,13,17,.96);border-bottom:1px solid var(--line);padding:12px 20px}
h1{margin:0 0 6px;font-size:20px;letter-spacing:.02em}.sub{color:var(--mute);font-size:13px}
.bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:10px}
input[type=search]{background:var(--card);border:1px solid var(--line);color:var(--text);padding:7px 10px;border-radius:6px;min-width:220px}
.chip{background:var(--card);border:1px solid var(--line);color:var(--text);padding:4px 10px;border-radius:14px;cursor:pointer;font-size:13px}
.chip.on{border-color:var(--gold);color:var(--gold)}label.t{font-size:13px;color:var(--mute);cursor:pointer}
main{padding:16px 20px;display:grid;gap:14px}
.card{display:grid;grid-template-columns:minmax(260px,420px) 1fr;gap:16px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px}
.card.done{border-color:var(--done);opacity:.55}.card.done .name::after{content:"  ✓ done";color:#6fcf8f}
.imgs img{width:100%;border-radius:6px;display:block;cursor:zoom-in;background:#000}
.end{margin-top:8px;font-size:12px;color:var(--mute)}.end img{margin-top:4px}
.name{font-weight:600;word-break:break-all}.meta{color:var(--mute);font-size:13px;margin:2px 0 8px}
.pair{color:var(--rose);font-weight:600}
pre{white-space:pre-wrap;word-wrap:break-word;margin:0;background:#0a1116;border:1px solid var(--line);border-radius:6px;padding:10px;font:13px/1.5 ui-monospace,Menlo,monospace;max-height:340px;overflow:auto}
.btns{display:flex;gap:8px;margin-top:8px;flex-wrap:wrap}
button{background:var(--gold);color:#111;border:0;border-radius:6px;padding:7px 14px;font-weight:600;cursor:pointer}
button.sec{background:transparent;color:var(--text);border:1px solid var(--line)}
.miss{color:#ff8a8a}
@media (max-width:760px){.card{grid-template-columns:1fr}header{padding:10px 16px}main{padding:12px 16px}}
#zoom{position:fixed;inset:0;background:rgba(0,0,0,.92);display:none;align-items:center;justify-content:center;z-index:9;cursor:zoom-out}
#zoom img{max-width:96vw;max-height:94vh}
</style></head><body>
<header><h1>__TITLE__</h1>
<div class="sub">__COUNT__ frames in storyboard order · __PAIRS__ Kling start → end pairs · load the frame as the start frame, copy its prompt, 16:9, sound off.
<span id="stat"></span></div>
<div class="bar"><input type="search" id="q" placeholder="Search name or text…">
<label class="t"><input type="checkbox" id="hide"> hide done</label>
<label class="t"><input type="checkbox" id="onlypairs"> pairs only</label></div>
<div class="bar" id="chips"></div></header>
<main id="list"></main><div id="zoom"><img alt=""></div>
<script>
const F=__DATA__, BLOCKS=__BLOCKS__;
const KEY=__KEY__;
let done={};try{done=JSON.parse(localStorage.getItem(KEY)||"{}")}catch(e){}
const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(done))}catch(e){}};
let sel=new Set();
const chips=document.getElementById("chips");
["All",...BLOCKS].forEach(b=>{const c=document.createElement("span");c.className="chip"+(b==="All"?" on":"");c.textContent=b;
 c.onclick=()=>{if(b==="All"){sel.clear()}else{sel.has(b)?sel.delete(b):sel.add(b)}
 [...chips.children].forEach(x=>x.classList.toggle("on",x.textContent==="All"?sel.size===0:sel.has(x.textContent)));render()};chips.appendChild(c)});
const esc=s=>s.replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));
function render(){
 const q=document.getElementById("q").value.toLowerCase(),hide=document.getElementById("hide").checked,op=document.getElementById("onlypairs").checked;
 const L=document.getElementById("list");L.innerHTML="";let shown=0;
 F.forEach((f,i)=>{
  if(sel.size&&!sel.has(f.block))return;if(hide&&done[f.name])return;if(op&&!f.pair)return;
  if(q&&!(f.name.toLowerCase().includes(q)||f.prompt.toLowerCase().includes(q)))return;shown++;
  const d=document.createElement("div");d.className="card"+(done[f.name]?" done":"");
  d.innerHTML=`<div class="imgs"><img loading="lazy" src="${f.src}" alt="">${f.end?`<div class="end">pair end frame → ${esc(f.end)}<img loading="lazy" src="${f.endsrc}" alt=""></div>`:""}</div>
  <div><div class="name">${i+1}. ${esc(f.name)}</div><div class="meta">${esc(f.block)} · ${esc(f.dur)}${f.pair?' · <span class="pair">Kling pair: start + end</span>':''}${f.missing?' · <span class="miss">picture missing from the folder</span>':''}</div>
  <pre>${esc(f.prompt)}</pre><div class="btns"><button class="cp">Copy prompt</button><button class="sec dn">${done[f.name]?"Unmark":"Done ✓"}</button></div></div>`;
  d.querySelector(".cp").onclick=e=>{navigator.clipboard.writeText(f.prompt).then(()=>{e.target.textContent="Copied";setTimeout(()=>e.target.textContent="Copy prompt",1200)})};
  d.querySelector(".dn").onclick=()=>{done[f.name]?delete done[f.name]:done[f.name]=1;save();render()};
  d.querySelectorAll("img").forEach(im=>im.onclick=()=>{const z=document.getElementById("zoom");z.querySelector("img").src=im.src;z.style.display="flex"});
  L.appendChild(d)});
 document.getElementById("stat").textContent=` · done ${Object.keys(done).filter(k=>F.some(f=>f.name===k)).length} of ${F.length} · shown ${shown}`;
}
document.getElementById("zoom").onclick=e=>e.currentTarget.style.display="none";
["q","hide","onlypairs"].forEach(id=>document.getElementById(id).addEventListener("input",render));
render();
</script></body></html>"""

if __name__ == "__main__":
    main()
