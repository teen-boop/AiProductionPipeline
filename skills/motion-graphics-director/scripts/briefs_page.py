#!/usr/bin/env python3
"""Build a browsable card page (search, filter, copy button) from references/HYPERFRAMES-BRIEFS.md.
Usage: python3 briefs_page.py [--out ../assets/hyperframes-briefs.html]
Every fenced code block becomes a card titled by the nearest heading above it."""
import html, re, sys, pathlib
here = pathlib.Path(__file__).resolve().parent
src = here.parent / 'references' / 'HYPERFRAMES-BRIEFS.md'
out = pathlib.Path(sys.argv[sys.argv.index('--out') + 1]) if '--out' in sys.argv else here.parent / 'assets' / 'hyperframes-briefs.html'
text = src.read_text()
cards, head, sect = [], '', ''
for m in re.finditer(r'^(#{2,3}) ([^\n]+)$|^```\n(.*?)^```', text, re.M | re.S):
    if m.group(1):
        head = m.group(2)
        if m.group(1) == '##': sect = m.group(2)
    elif m.group(3) is not None:
        group = 'Styles' if head.startswith('STY-') else 'Briefs'
        cards.append((group, head, m.group(3).strip()))
rows = []
for i, (g, h, body) in enumerate(cards):
    rows.append(f'<article class="card" data-g="{g}"><header><span class="tag">{g[:-1]}</span><h2>{html.escape(h)}</h2>'
                f'<button data-i="{i}">Copy</button></header><pre id="p{i}">{html.escape(body)}</pre></article>')
page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>HyperFrames Briefs</title><style>
:root{{--bg:#f2efe9;--ink:#15140f;--mut:#6d6a62;--card:#fff;--acc:#e5432d;--line:#e2ddd3}}
@media (prefers-color-scheme:dark){{:root{{--bg:#141413;--ink:#ecebe6;--mut:#9a978e;--card:#1d1d1b;--line:#2c2b28}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 -apple-system,Inter,sans-serif}}
.top{{position:sticky;top:0;background:var(--bg);padding:16px;border-bottom:1px solid var(--line);display:flex;gap:10px;flex-wrap:wrap;align-items:center;z-index:2}}
h1{{font-size:20px;margin:0 16px 0 0}}input{{flex:1;min-width:200px;padding:9px 12px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--ink)}}
.f button{{padding:8px 12px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--ink);cursor:pointer}}.f button.on{{background:var(--ink);color:var(--bg)}}
main{{max-width:1100px;margin:0 auto;padding:16px;display:grid;gap:14px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px}}
.card header{{display:flex;align-items:center;gap:10px}}.card h2{{font-size:16px;margin:0;flex:1}}
.tag{{font:11px ui-monospace,monospace;color:var(--acc);text-transform:uppercase;letter-spacing:.08em}}
.card header button{{padding:6px 12px;border:0;border-radius:6px;background:var(--acc);color:#fff;cursor:pointer}}
pre{{white-space:pre-wrap;font:13px/1.5 ui-monospace,Menlo,monospace;color:var(--mut);margin:10px 0 0;max-height:240px;overflow:auto}}
.card.open pre{{max-height:none}}
</style></head><body><div class="top"><h1>HyperFrames Briefs</h1><input id="q" placeholder="Search: logo, neon, vertical, 3D ...">
<span class="f"><button class="on" data-f="">All</button> <button data-f="Briefs">Briefs</button> <button data-f="Styles">Styles</button></span></div>
<main>{''.join(rows)}</main><script>
const q=document.getElementById('q');let f='';
function run(){{const v=q.value.toLowerCase();document.querySelectorAll('.card').forEach(c=>{{c.style.display=((!f||c.dataset.g===f)&&c.textContent.toLowerCase().includes(v))?'':'none'}})}}
q.oninput=run;document.querySelectorAll('.f button').forEach(b=>b.onclick=()=>{{document.querySelectorAll('.f button').forEach(x=>x.classList.remove('on'));b.classList.add('on');f=b.dataset.f;run()}});
document.querySelectorAll('.card header button').forEach(b=>b.onclick=async()=>{{const t=document.getElementById('p'+b.dataset.i).textContent;try{{await navigator.clipboard.writeText(t)}}catch(e){{const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();document.execCommand('copy');a.remove()}}b.textContent='Copied';setTimeout(()=>b.textContent='Copy',1200)}});
document.querySelectorAll('pre').forEach(p=>p.onclick=()=>p.parentElement.classList.toggle('open'));
</script></body></html>'''
out.parent.mkdir(parents=True, exist_ok=True); out.write_text(page)
print(f'{len(cards)} cards -> {out}')
