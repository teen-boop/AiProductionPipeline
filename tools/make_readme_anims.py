#!/usr/bin/env python3
"""Writes docs/anim/NN_<stage>.svg: one small looping animation per pipeline stage for the README.
Pure SVG + CSS keyframes (GitHub renders them in <img>), no external fonts or files.
Run: python3 tools/make_readme_anims.py
"""
import os

W, H = 320, 180
BG, CARD, LINE = "#07050F", "#0F0D1A", "#1B1A26"
ACC, PRI, RED, BONE, ASH, AMB, GRN = "#22D3EE", "#0E7490", "#E23B2E", "#EEF3F6", "#8B93A3", "#F5B841", "#34D399"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "anim")
T = 4  # loop seconds


def svg(n, title, body, css):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{title}">
<style>
.f{{transform-box:fill-box;transform-origin:center}}
{css}
</style>
<rect width="{W}" height="{H}" rx="14" fill="{BG}"/>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{LINE}"/>
{body}
<text x="16" y="{H-14}" font-family="{MONO}" font-size="10" letter-spacing="1.5" fill="{ASH}">{n:02d}</text>
<text x="38" y="{H-14}" font-family="{MONO}" font-size="10" letter-spacing="1.5" fill="{BONE}">{title.upper()}</text>
</svg>
"""


def kf(name, steps):
    return f"@keyframes {name}{{{steps}}}"


def stage_setup():
    rows = ["00_BRIEF", "01_REFERENCES", "02_PROMPTS", "03_GENERATED", "04_EDIT", "05_FINAL_OUTPUTS", "06_DELIVERY"]
    b, css = [], [kf("in", "0%,4%{opacity:0;transform:translateX(-8px)}12%,88%{opacity:1;transform:none}100%{opacity:0}")]
    b.append(f'<path d="M28 22v{len(rows)*17}" stroke="{LINE}" stroke-width="1.5"/>')
    for i, r in enumerate(rows):
        y = 26 + i * 17
        d = i * 0.35
        b.append(f'<g class="r" style="animation:in {T}s {d:.2f}s infinite both"><path d="M28 {y+4}h10" stroke="{LINE}" stroke-width="1.5"/>'
                 f'<rect x="42" y="{y-2}" width="14" height="10" rx="2" fill="{PRI}"/><rect x="42" y="{y-4}" width="7" height="4" rx="1" fill="{PRI}"/>'
                 f'<text x="62" y="{y+7}" font-family="{MONO}" font-size="10" fill="{BONE if i else ACC}">{r}</text></g>')
    b.append(f'<g style="animation:in {T}s 2.6s infinite both"><rect x="200" y="40" width="96" height="58" rx="8" fill="{CARD}" stroke="{LINE}"/>'
             f'<text x="212" y="60" font-family="{MONO}" font-size="9" fill="{ASH}">PROJECT.json</text>'
             f'<rect x="212" y="68" width="60" height="4" rx="2" fill="{LINE}"/><rect x="212" y="78" width="44" height="4" rx="2" fill="{LINE}"/>'
             f'<circle cx="280" cy="84" r="7" fill="{GRN}"/><path d="M276.5 84l2.5 2.5 4.5-5" stroke="{BG}" stroke-width="2" fill="none"/></g>')
    return "".join(b), "\n".join(css)


def stage_research():
    b, css = [], [kf("scan", "0%{transform:translate(0,0)}25%{transform:translate(150px,0)}50%{transform:translate(150px,44px)}75%{transform:translate(0,44px)}100%{transform:translate(0,0)}"),
                  kf("hl", "0%,20%{fill:" + LINE + "}30%,90%{fill:" + AMB + "}100%{fill:" + LINE + "}")]
    for row in range(5):
        y = 30 + row * 20
        x = 24
        for j, w in enumerate([38, 22, 50, 30, 44][row:] + [26, 34][: row]):
            hot = (row, j) in {(0, 2), (1, 1), (2, 3), (3, 0), (4, 1)}
            st = f' style="animation:hl {T}s {0.5+row*0.6:.1f}s infinite"' if hot else ""
            b.append(f'<rect x="{x}" y="{y}" width="{w}" height="7" rx="3.5" fill="{LINE}"{st}/>')
            x += w + 8
            if x > 230:
                break
    b.append(f'<g style="animation:scan {T}s ease-in-out infinite"><circle cx="60" cy="52" r="20" fill="{ACC}" fill-opacity="0.08" stroke="{ACC}" stroke-width="2.5"/>'
             f'<path d="M74 66l14 14" stroke="{ACC}" stroke-width="4" stroke-linecap="round"/></g>')
    b.append(f'<text x="226" y="150" font-family="{MONO}" font-size="9" fill="{AMB}">"their words"</text>')
    return "".join(b), "\n".join(css)


def stage_story():
    b = [f'<rect x="22" y="18" width="128" height="134" rx="6" fill="{CARD}" stroke="{LINE}"/>',
         f'<text x="34" y="36" font-family="{MONO}" font-size="8" fill="{ACC}">INT. MARKET - NIGHT</text>']
    css = [kf("type", "0%,5%{transform:scaleX(0)}25%,90%{transform:scaleX(1)}100%{transform:scaleX(0)}"),
           kf("arc", "0%,10%{stroke-dashoffset:302}70%,90%{stroke-dashoffset:0}100%{stroke-dashoffset:302}"),
           kf("dot", "0%,10%{opacity:0}20%,90%{opacity:1}100%{opacity:0}"), "#t rect{transform-origin:left center;transform-box:fill-box}"]
    b.append('<g id="t">')
    for i, w in enumerate([96, 70, 104, 54, 88, 76, 60]):
        b.append(f'<rect x="34" y="{46+i*14}" width="{w}" height="5" rx="2.5" fill="{ASH if i%3 else BONE}" fill-opacity="{0.5 if i%3 else 0.85}" style="animation:type {T}s {i*0.25:.2f}s infinite both"/>')
    b.append("</g>")
    cx, cy, r = 232, 78, 48
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LINE}" stroke-width="2"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{ACC}" stroke-width="2.5" stroke-dasharray="302" transform="rotate(-90 {cx} {cy})" style="animation:arc {T}s ease-in-out infinite"/>')
    import math
    for k in range(8):
        a = -math.pi / 2 + k * math.pi / 4
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{RED if k==4 else ACC}" style="animation:dot {T}s {0.3+k*0.32:.2f}s infinite both"/>')
    b.append(f'<text x="{cx}" y="{cy+4}" text-anchor="middle" font-family="{MONO}" font-size="9" fill="{BONE}">BUT</text>')
    return "".join(b), "\n".join(css)


def stage_refs():
    cols = [("EXTERNAL", ASH, 46), ("INTERNAL", ACC, 160), ("PERSONAL", RED, 274)]
    b, css = [], []
    for name, c, x in cols:
        b.append(f'<rect x="{x-40}" y="104" width="80" height="44" rx="6" fill="{CARD}" stroke="{c}" stroke-opacity="0.6"/>'
                 f'<text x="{x}" y="141" text-anchor="middle" font-family="{MONO}" font-size="8.5" fill="{c}">{name}</text>')
    starts = [(150, 22), (150, 22), (150, 22)]
    targets = [(-114, 88), (0, 88), (114, 88)]
    for i, ((dx, dy), (name, c, _)) in enumerate(zip(targets, cols)):
        css.append(kf(f"m{i}", f"0%{{transform:translate(0,0) rotate({(i-1)*8}deg);opacity:0}}10%{{opacity:1}}30%{{transform:translate(0,0) rotate({(i-1)*8}deg)}}60%,88%{{transform:translate({dx}px,{dy-34}px) scale(.7);opacity:1}}100%{{transform:translate({dx}px,{dy-34}px) scale(.7);opacity:0}}"))
        b.append(f'<g class="f" style="animation:m{i} {T}s {i*0.25:.2f}s ease-in-out infinite both">'
                 f'<rect x="{starts[i][0]-6+i*4}" y="{starts[i][1]+i*3}" width="56" height="40" rx="4" fill="{c}" fill-opacity="0.38" stroke="{c}" stroke-width="1.5"/>'
                 f'<circle cx="{starts[i][0]+10+i*4}" cy="{starts[i][1]+14+i*3}" r="6" fill="{c}" fill-opacity="0.7"/>'
                 f'<path d="M{starts[i][0]-2+i*4} {starts[i][1]+36+i*3}l14-12 10 8 12-14 16 18z" fill="{c}" fill-opacity="0.55"/></g>')
    css.append(kf("lk", "0%,62%{opacity:0;transform:scale(.4)}70%,92%{opacity:1;transform:scale(1)}100%{opacity:0}"))
    b.append(f'<g class="f" style="animation:lk {T}s infinite"><rect x="185" y="90" width="14" height="11" rx="2" fill="{ACC}"/><path d="M188 90v-4a4 4 0 0 1 8 0v4" stroke="{ACC}" stroke-width="2" fill="none"/></g>')
    return "".join(b), "\n".join(css)


def stage_shots():
    b, css = [], [kf("pn", "0%,5%{opacity:0;transform:translateY(10px)}15%,88%{opacity:1;transform:none}100%{opacity:0}"),
                  kf("cam", "0%{transform:translateX(0)}100%{transform:translateX(30px)}")]
    sizes = ["WIDE", "MED", "CU", "ECU"]
    for i in range(4):
        x = 18 + i * 73
        s = 1 - i * 0.18
        b.append(f'<g style="animation:pn {T}s {i*0.45:.2f}s infinite both">'
                 f'<rect x="{x}" y="34" width="66" height="44" rx="4" fill="{CARD}" stroke="{ACC if i==2 else LINE}"/>'
                 f'<circle cx="{x+33}" cy="{56-(1-s)*6}" r="{5/s:.1f}" fill="{BONE}" fill-opacity="0.8"/>'
                 f'<rect x="{x+33-9/s:.1f}" y="{62-(1-s)*6:.1f}" width="{18/s:.1f}" height="{16}" rx="5" fill="{BONE}" fill-opacity="0.35"/>'
                 f'<text x="{x}" y="92" font-family="{MONO}" font-size="9" fill="{ACC}">S0{i+1}</text>'
                 f'<text x="{x+66}" y="92" text-anchor="end" font-family="{MONO}" font-size="8" fill="{ASH}">{sizes[i]}</text>'
                 f'<rect x="{x}" y="100" width="{40+i*6}" height="4" rx="2" fill="{LINE}"/><rect x="{x}" y="110" width="{30+i*8}" height="4" rx="2" fill="{LINE}"/></g>')
    b.append(f'<path d="M18 128h284" stroke="{LINE}" stroke-dasharray="3 4"/>')
    b.append(f'<g style="animation:cam {T}s ease-in-out infinite alternate"><path d="M40 122l10 6-10 6z" fill="{RED}"/></g>')
    b.append(f'<text x="302" y="140" text-anchor="end" font-family="{MONO}" font-size="8" fill="{ASH}">180° axis</text>')
    return "".join(b), "\n".join(css)


def stage_stills():
    b = [f'<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{PRI}"/><stop offset="1" stop-color="{RED}" stop-opacity="0.75"/></linearGradient>'
         f'<clipPath id="c"><rect x="60" y="20" width="200" height="112" rx="6"/></clipPath></defs>',
         f'<rect x="60" y="20" width="200" height="112" rx="6" fill="{CARD}" stroke="{LINE}"/>',
         '<g clip-path="url(#c)"><g style="animation:dev ' + str(T) + 's infinite">'
         f'<rect x="60" y="20" width="200" height="112" fill="url(#g)"/>'
         f'<rect x="60" y="96" width="200" height="36" fill="{BG}" fill-opacity="0.55"/>'
         f'<path d="M60 96 L140 60 L190 84 L230 64 L260 80 V96Z" fill="{BG}" fill-opacity="0.7"/>'
         f'<circle cx="214" cy="42" r="9" fill="{AMB}" fill-opacity="0.9"/>'
         f'<rect x="128" y="76" width="10" height="24" rx="4" fill="{BONE}"/><circle cx="133" cy="72" r="5" fill="{BONE}"/></g>'
         f'<rect x="60" y="0" width="200" height="8" fill="{ACC}" fill-opacity="0.8" style="animation:scanl {T}s infinite"/></g>',
         f'<text x="160" y="148" text-anchor="middle" font-family="{MONO}" font-size="9" fill="{ASH}">STYLE LOCK + hero card + plate</text>']
    css = [kf("dev", "0%,8%{opacity:0;filter:blur(6px)}45%,90%{opacity:1;filter:blur(0)}100%{opacity:0}"),
           kf("scanl", "0%{transform:translateY(12px);opacity:0}8%{opacity:1}45%{transform:translateY(132px);opacity:1}50%,100%{opacity:0;transform:translateY(132px)}")]
    return "".join(b), "\n".join(css)


def stage_qc():
    b, css = [], [kf("st", "0%,{a}%{{opacity:0;transform:scale(2.2)}}{b}%,90%{{opacity:1;transform:scale(1)}}100%{{opacity:0}}")]
    css = []
    verdict = [1, 1, 0, 1, 2, 1, 1, 0]
    for i in range(8):
        x, y = 24 + (i % 4) * 70, 22 + (i // 4) * 62
        a = 8 + i * 9
        css.append(kf(f"s{i}", f"0%,{a}%{{opacity:0;transform:scale(2.2)}}{a+6}%,90%{{opacity:1;transform:scale(1)}}100%{{opacity:0}}"))
        b.append(f'<rect x="{x}" y="{y}" width="62" height="52" rx="4" fill="{CARD}" stroke="{LINE}"/>'
                 f'<circle cx="{x+31}" cy="{y+22}" r="9" fill="{BONE}" fill-opacity="0.25"/><rect x="{x+18}" y="{y+33}" width="26" height="12" rx="5" fill="{BONE}" fill-opacity="0.15"/>')
        c = [GRN, GRN, RED, GRN, AMB, GRN, GRN, RED][i]
        icon = {1: f'<path d="M{x+44} {y+14}l4 4 8-9" stroke="{BG}" stroke-width="2.4" fill="none"/>',
                0: f'<path d="M{x+45} {y+9}l8 8M{x+53} {y+9}l-8 8" stroke="{BG}" stroke-width="2.4"/>',
                2: f'<path d="M{x+49} {y+8}v6M{x+49} {y+17}v1" stroke="{BG}" stroke-width="2.4" stroke-linecap="round"/>'}[verdict[i]]
        b.append(f'<g class="f" style="animation:s{i} {T}s infinite both"><circle cx="{x+49}" cy="{y+13}" r="9" fill="{c}"/>{icon}</g>')
    return "".join(b), "\n".join(css)


def stage_video():
    b = [f'<defs><clipPath id="v"><rect x="18" y="22" width="284" height="74" rx="6"/></clipPath></defs>',
         f'<rect x="18" y="22" width="284" height="74" rx="6" fill="{CARD}" stroke="{LINE}"/>',
         f'<g clip-path="url(#v)"><g style="animation:roll {T}s linear infinite">']
    for i in range(10):
        x = 18 + i * 64
        b.append(f'<rect x="{x+6}" y="32" width="54" height="54" rx="3" fill="{[PRI, RED, PRI, AMB][i%4]}" fill-opacity="0.45"/>'
                 f'<circle cx="{x+33}" cy="{52+(i%3)*4}" r="7" fill="{BONE}" fill-opacity="0.7"/>')
        for k in range(4):
            b.append(f'<rect x="{x+8+k*14}" y="25" width="8" height="4" rx="1" fill="{LINE}"/><rect x="{x+8+k*14}" y="89" width="8" height="4" rx="1" fill="{LINE}"/>')
    b.append("</g></g>")
    b.append(f'<text x="18" y="114" font-family="{MONO}" font-size="9" fill="{ACC}">START FRAME</text><text x="302" y="114" text-anchor="end" font-family="{MONO}" font-size="9" fill="{ACC}">END FRAME</text>')
    b.append(f'<rect x="18" y="124" width="284" height="4" rx="2" fill="{LINE}"/><rect x="18" y="124" width="284" height="4" rx="2" fill="{ACC}" style="transform-origin:18px 126px;animation:prog {T}s linear infinite"/>')
    b.append(f'<circle cx="160" cy="59" r="16" fill="{BG}" fill-opacity="0.6"/><path d="M155 51l13 8-13 8z" fill="{BONE}"/>')
    css = [kf("roll", "from{transform:translateX(0)}to{transform:translateX(-256px)}"), kf("prog", "from{transform:scaleX(0)}to{transform:scaleX(1)}")]
    return "".join(b), "\n".join(css)


def stage_edit():
    b, css = [], [kf("ph", "from{transform:translateX(0)}to{transform:translateX(252px)}"),
                  kf("cl", "0%,{a}%{{opacity:0;transform:translateX(-30px)}}{b}%,92%{{opacity:1;transform:none}}100%{{opacity:0}}")]
    css = [css[0]]
    tracks = [("V2", [(120, 40, AMB)]), ("V1", [(40, 60, PRI), (102, 50, RED), (154, 70, PRI), (226, 50, PRI)]), ("A1", [(40, 236, GRN)])]
    for ti, (name, clips) in enumerate(tracks):
        y = 26 + ti * 30
        b.append(f'<text x="18" y="{y+15}" font-family="{MONO}" font-size="9" fill="{ASH}">{name}</text><rect x="38" y="{y}" width="264" height="22" rx="3" fill="{CARD}"/>')
        for ci, (x, w, c) in enumerate(clips):
            k = ti * 4 + ci
            a = 4 + k * 8
            css.append(kf(f"c{k}", f"0%,{a}%{{opacity:0;transform:translateX(-24px)}}{a+8}%,92%{{opacity:1;transform:none}}100%{{opacity:0}}"))
            if name == "A1":
                wave = "".join(f'<rect x="{x+4+j*6}" y="{y+11-h}" width="3" height="{2*h}" rx="1" fill="{c}"/>' for j, h in enumerate([3, 6, 8, 5, 9, 4, 7, 3, 6, 8, 5, 3, 6, 9, 7, 4, 3, 5, 8, 6, 4, 7, 5, 3, 6, 8, 4, 6, 3, 5, 7, 4, 6, 3, 5, 8, 4, 6]) if j * 6 < w - 8)
                b.append(f'<g style="animation:c{k} {T}s infinite both">{wave}</g>')
            else:
                b.append(f'<rect x="{x}" y="{y+2}" width="{w-3}" height="18" rx="3" fill="{c}" fill-opacity="0.75" style="animation:c{k} {T}s infinite both"/>')
    b.append(f'<g style="animation:ph {T}s linear infinite"><path d="M44 18v84" stroke="{BONE}" stroke-width="1.5"/><path d="M39 16h10l-5 6z" fill="{BONE}"/></g>')
    b.append(f'<text x="302" y="130" text-anchor="end" font-family="{MONO}" font-size="9" fill="{ASH}">cut plan → Resolve / Premiere / EDL</text>')
    return "".join(b), "\n".join(css)


def stage_finals():
    boxes = [("16x9", 56, 32, 66), ("9x16", 20, 36, 160), ("1x1", 30, 30, 254)]
    b, css = [], []
    for i, (lab, w, h, cx) in enumerate(boxes):
        css.append(kf(f"d{i}", f"0%,{6+i*10}%{{transform:translateY(-60px);opacity:0}}{22+i*10}%,88%{{transform:none;opacity:1}}100%{{opacity:0}}"))
        b.append(f'<path d="M{cx-40} 72h22l5 6h53v50h-80z" fill="{CARD}" stroke="{LINE}"/>'
                 f'<text x="{cx}" y="144" text-anchor="middle" font-family="{MONO}" font-size="9" fill="{ASH}">{lab}/</text>')
        y0 = 86 + (36 - h) / 2
        b.append(f'<g style="animation:d{i} {T}s ease-out infinite both"><rect x="{cx-w/2}" y="{y0}" width="{w}" height="{h}" rx="3" fill="{PRI}" stroke="{ACC}"/>'
                 f'<path d="M{cx-3} {y0+h/2-5}l8 5-8 5z" fill="{BONE}"/></g>')
    b.append(f'<text x="18" y="30" font-family="{MONO}" font-size="10" fill="{BONE}">05_FINAL_OUTPUTS/Promos/</text>')
    b.append(f'<text x="18" y="48" font-family="{MONO}" font-size="10" fill="{ACC}">03-Rise/</text><text x="80" y="48" font-family="{MONO}" font-size="10" fill="{ASH}">aspect/ LANG/</text>')
    return "".join(b), "\n".join(css)


def stage_deliver():
    b = [f'<g style="animation:lid {T}s ease-in-out infinite;transform-origin:110px 70px"><path d="M60 70h100l-10-18H70z" fill="{PRI}"/></g>',
         f'<rect x="60" y="70" width="100" height="62" rx="4" fill="{CARD}" stroke="{PRI}" stroke-width="2"/>',
         f'<path d="M110 70v62" stroke="{PRI}" stroke-width="2"/>']
    css = [kf("lid", "0%,15%{transform:rotate(-28deg) translateY(-14px)}40%,90%{transform:none}100%{transform:rotate(-28deg) translateY(-14px)}"),
           kf("drop", "0%{transform:translateY(-40px);opacity:0}10%{opacity:1}30%{transform:translateY(20px);opacity:1}38%,100%{transform:translateY(20px);opacity:0}"),
           kf("ln", "0%,{a}%{{opacity:0}}{b}%,92%{{opacity:1}}100%{{opacity:0}}")]
    css = css[:2]
    for i, c in enumerate([ACC, AMB, BONE]):
        b.append(f'<rect x="{88+i*14}" y="44" width="10" height="16" rx="2" fill="{c}" style="animation:drop {T}s {i*0.25:.2f}s infinite both"/>')
    rows = ["specs  OK", "captions  OK", "leak check  OK", "sha256  OK"]
    for i, r in enumerate(rows):
        a = 40 + i * 9
        css.append(kf(f"r{i}", f"0%,{a}%{{opacity:0}}{a+5}%,92%{{opacity:1}}100%{{opacity:0}}"))
        b.append(f'<g style="animation:r{i} {T}s infinite both"><circle cx="190" cy="{58+i*20}" r="6" fill="{GRN}"/><path d="M187 {58+i*20}l2 2 4-4.5" stroke="{BG}" stroke-width="1.8" fill="none"/>'
                 f'<text x="202" y="{62+i*20}" font-family="{MONO}" font-size="9.5" fill="{BONE}">{r}</text></g>')
    return "".join(b), "\n".join(css)


def stage_promo():
    b = [f'<defs><linearGradient id="sw" x1="0" x2="1"><stop offset="0" stop-color="{BONE}" stop-opacity="0"/><stop offset=".5" stop-color="{BONE}" stop-opacity=".9"/><stop offset="1" stop-color="{BONE}" stop-opacity="0"/></linearGradient>'
         f'<clipPath id="tx"><text x="160" y="84" text-anchor="middle" font-family="Impact,Haettenschweiler,Arial Narrow,sans-serif" font-size="40" letter-spacing="4">THE KEEPER</text></clipPath></defs>',
         f'<clipPath id="cardc"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="13"/></clipPath>',
         f'<g clip-path="url(#cardc)"><rect x="0" y="0" width="{W}" height="22" fill="#000"/><rect x="0" y="{H-40}" width="{W}" height="16" fill="#000"/></g>',
         f'<text x="160" y="84" text-anchor="middle" font-family="Impact,Haettenschweiler,Arial Narrow,sans-serif" font-size="40" letter-spacing="4" fill="{ACC}" style="animation:ttl {T}s infinite">THE KEEPER</text>',
         f'<g clip-path="url(#tx)"><rect x="0" y="40" width="70" height="60" fill="url(#sw)" style="animation:sweep {T}s infinite"/></g>',
         f'<text x="160" y="110" text-anchor="middle" font-family="{MONO}" font-size="9" letter-spacing="3" fill="{ASH}" style="animation:ttl {T}s .4s infinite both">A FILM MADE WITH THE PIPELINE</text>']
    css = [kf("ttl", "0%,8%{opacity:0;letter-spacing:12px}30%,88%{opacity:1;letter-spacing:4px}100%{opacity:0}"),
           kf("sweep", "0%,35%{transform:translateX(-80px)}65%,100%{transform:translateX(340px)}")]
    return "".join(b), "\n".join(css)


STAGES = [
    ("setup", "Project setup", stage_setup), ("research", "Research", stage_research), ("story", "Story and script", stage_story),
    ("references", "References", stage_refs), ("shots", "Shot list", stage_shots), ("stills", "Still frames", stage_stills),
    ("qc", "Frame QC", stage_qc), ("video", "Video clips", stage_video), ("edit", "Edit and sound", stage_edit),
    ("finals", "Finals", stage_finals), ("delivery", "Delivery", stage_deliver), ("promo", "Promos and motion", stage_promo),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, (slug, title, fn) in enumerate(STAGES, 1):
        body, css = fn()
        with open(os.path.join(OUT, f"{i:02d}_{slug}.svg"), "w") as f:
            f.write(svg(i, title, body, css))
    print("wrote", len(STAGES), "animations to", os.path.normpath(OUT))
