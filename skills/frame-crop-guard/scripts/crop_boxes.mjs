#!/usr/bin/env node
// Lays out HTML compositions in headless Chrome and writes, for every <img> and <video>, the box it is drawn in and how
// the media is fitted (object-fit, object-position, natural size). Scripts do not run: the layout is the resting CSS
// layout, which is where crops are decided. Animated transforms (push-ins) are reported by crop_check as a margin.
//
// Usage: node crop_boxes.mjs --width 1920 --height 1080 --out boxes.json [--portrait-class "#root=is-portrait"] comp1.html ...
// Scripts are not run, so a class a runtime adds for the vertical layout must be named (default for H > W:
// "#root=is-portrait", the HyperFrames promo convention; pass "" to switch it off).
// Accepts HyperFrames sub-compositions (<template> wrappers) and plain HTML pages. Media paths resolve against the
// project root: the parent of a compositions/ folder, otherwise the file's own folder.
// Needs puppeteer-core (local install, global, or the npx cache HyperFrames uses) and a Chrome: CHROME_PATH, the
// HyperFrames headless shell in ~/.cache/hyperframes/chrome, or Google Chrome in /Applications.
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import http from "node:http";
import { createRequire } from "node:module";

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); if (i < 0) return d; const v = args[i + 1]; args.splice(i, 2); return v; };
const W = +opt("--width", 1920), H = +opt("--height", 1080), OUT = opt("--out", "boxes.json");
// layout classes a runtime would add (HyperFrames promo engines set #root.is-portrait for vertical formats)
const PCLASS = opt("--portrait-class", H > W ? "#root=is-portrait" : "");
if (!args.length) { console.error("give one or more composition HTML files"); process.exit(1); }

function loadPuppeteer() {
  for (const base of [process.cwd(), path.join(os.homedir(), ".npm", "_npx")]) {
    if (base.endsWith("_npx") && fs.existsSync(base)) {
      for (const d of fs.readdirSync(base)) {
        const p = path.join(base, d, "node_modules", "puppeteer-core");
        if (fs.existsSync(p)) return createRequire(path.join(p, "package.json"))(p);
      }
    } else {
      try { return createRequire(path.join(base, "x.js"))("puppeteer-core"); } catch {}
    }
  }
  console.error("puppeteer-core not found: run `npm i -g puppeteer-core` or render once with HyperFrames (npx caches it)");
  process.exit(1);
}
function findChrome() {
  if (process.env.CHROME_PATH && fs.existsSync(process.env.CHROME_PATH)) return process.env.CHROME_PATH;
  const hf = path.join(os.homedir(), ".cache", "hyperframes", "chrome");
  const walk = (d, depth) => { if (depth > 6 || !fs.existsSync(d)) return null; for (const n of fs.readdirSync(d)) { const p = path.join(d, n); if (n === "chrome-headless-shell" && fs.statSync(p).isFile()) return p; if (fs.statSync(p).isDirectory()) { const r = walk(p, depth + 1); if (r) return r; } } return null; };
  return walk(hf, 0) || ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/usr/bin/google-chrome", "/usr/bin/chromium"].find((p) => fs.existsSync(p));
}

const puppeteer = loadPuppeteer();
const browser = await puppeteer.launch({ executablePath: findChrome(), headless: true, args: ["--no-sandbox"] });
const out = [];
for (const file of args) {
  const abs = path.resolve(file);
  const root = path.basename(path.dirname(abs)) === "compositions" ? path.dirname(path.dirname(abs)) : path.dirname(abs);
  let html = fs.readFileSync(abs, "utf8");
  const t = html.match(/<template>([\s\S]*)<\/template>/);
  if (t) html = `<!doctype html><html><head><meta charset="utf-8"></head><body style="margin:0;width:${W}px;height:${H}px;overflow:hidden;background:#000">${t[1]}</body></html>`;
  html = html.replace(/<script[\s\S]*?<\/script>/g, "");
  // a tiny server so relative media paths resolve exactly as in the real project
  const server = http.createServer((q, s) => {
    const u = decodeURIComponent(q.url.split("?")[0]);
    if (u === "/__page.html") { s.writeHead(200, { "Content-Type": "text/html" }); return s.end(html); }
    const fp = path.join(root, u);
    if (!fp.startsWith(root) || !fs.existsSync(fp)) { s.writeHead(404); return s.end(); }
    s.writeHead(200); fs.createReadStream(fp).pipe(s);
  }).listen(0);
  const port = server.address().port;
  const page = await browser.newPage();
  await page.setViewport({ width: W, height: H });
  try {
    // media keeps streaming, so wait for the DOM, then for images and video metadata only
    await page.goto(`http://127.0.0.1:${port}/__page.html`, { waitUntil: "domcontentloaded", timeout: 60000 });
  } catch (e) { console.error(`skip ${file}: ${e.message}`); await page.close(); server.close(); continue; }
  await page.evaluate(() => Promise.all([...document.images].map((i) => (i.complete ? 0 : new Promise((r) => { i.onload = i.onerror = r; })))));
  await page.evaluate(() => Promise.all([...document.querySelectorAll("video")].map((v) => (v.readyState >= 1 ? 0 : new Promise((r) => { v.onloadedmetadata = v.onerror = r; setTimeout(r, 4000); })))));
  if (PCLASS) await page.evaluate((spec) => { const [sel, cls] = spec.split("="); document.querySelectorAll(sel).forEach((e) => e.classList.add(cls)); }, PCLASS);
  const items = await page.evaluate(() => [...document.querySelectorAll("img, video")].map((el) => {
    const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    // the first ancestor that clips, so a box larger than its frame is measured by what is really visible
    let clip = null; for (let p = el.parentElement; p; p = p.parentElement) { const s = getComputedStyle(p); if (s.overflow !== "visible") { const b = p.getBoundingClientRect(); clip = [b.left, b.top, b.right, b.bottom]; break; } }
    return { id: el.id || "", cls: el.className || "", src: el.getAttribute("src"), tag: el.tagName.toLowerCase(),
      box: [r.left, r.top, r.width, r.height], clip, fit: cs.objectFit, pos: cs.objectPosition, filter: cs.filter,
      natural: el.tagName === "IMG" ? [el.naturalWidth, el.naturalHeight] : [el.videoWidth, el.videoHeight],
      mediaStart: +(el.getAttribute("data-media-start") || 0), display: cs.display };
  }));
  for (const it of items) { it.file = path.relative(process.cwd(), abs); it.root = root; it.path = it.src ? path.join(root, it.src) : null; }
  out.push(...items.filter((i) => i.src && i.display !== "none" && i.box[2] > 4 && i.box[3] > 4));
  await page.close(); server.close();
}
await browser.close();
fs.writeFileSync(OUT, JSON.stringify({ width: W, height: H, items: out }, null, 1));
console.log(`${out.length} media boxes from ${args.length} file(s) -> ${OUT}`);
