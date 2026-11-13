// Renders the product3d styles in headless Chrome (GPU on).
//   node render.mjs stills <style> <out_dir> t1,t2,...   -> JPEG stills at 16 samples (storyboard)
//   node render.mjs video  <style> <out.mp4>              -> every frame at the style's full sample count + sound, -15 LUFS
import fs from 'node:fs';
import path from 'node:path';
import { spawn, execFileSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';
const HERE = path.dirname(fileURLToPath(import.meta.url));
const PUP = process.env.PUPPETEER_CORE || 'puppeteer-core';   // npm i puppeteer-core, or point PUPPETEER_CORE at an installed copy
const puppeteer = createRequire(import.meta.url)(PUP);
const CHROME = process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const [mode, style, out, times] = process.argv.slice(2);

const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist', '--enable-unsafe-swiftshader', '--allow-file-access-from-files', '--autoplay-policy=no-user-gesture-required'] });
const page = await browser.newPage();
await page.setViewport({ width: 1920, height: 1124 });
page.on('pageerror', (e) => console.error('PAGE ERROR', e.message));
page.on('console', (m) => { if (m.type() === 'error') console.error('CONSOLE', m.text()); });
await page.goto(pathToFileURL(path.join(HERE, 'player.html')).href + `?style=${style}&render${process.env.NO_TEXT ? '&notext' : ''}`, { waitUntil: 'networkidle0', timeout: 120000 });
await page.waitForFunction('window.READY === true', { timeout: 120000 });
const grab = (t, n) => page.evaluate((t, n) => { window.seek(t, n); return document.getElementById('c').toDataURL('image/jpeg', 0.92); }, t, n);

if (mode === 'stills') {
  fs.mkdirSync(out, { recursive: true });
  for (const t of times.split(',').map(Number)) {
    const d = await grab(t, 16);
    fs.writeFileSync(path.join(out, `${style}_${t.toFixed(2)}.jpg`), Buffer.from(d.split(',')[1], 'base64'));
    console.log('still', style, t);
  }
} else {
  const dur = await page.evaluate('window.DURATION'), N = Math.round(dur * 30), tmp = out + '.silent.mp4', wav = out + '.f32';
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', '30', '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', tmp]);
  for (let i = 0; i < N; i++) {
    const d = await grab(i / 30, 0);
    if (!ff.stdin.write(Buffer.from(d.split(',')[1], 'base64'))) await new Promise((r) => ff.stdin.once('drain', r));
    if (i % 30 === 0) console.log('frame', i, '/', N);
  }
  ff.stdin.end(); await new Promise((r) => ff.on('close', r));
  fs.writeFileSync(wav, Buffer.from(await page.evaluate('window.renderSound()'), 'base64'));
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', tmp, '-f', 'f32le', '-ar', '48000', '-ac', '2', '-i', wav, '-filter_complex', '[1:a]loudnorm=I=-15:TP=-1.5:LRA=11,aresample=48000[a]', '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-shortest', out]);
  fs.unlinkSync(tmp); fs.unlinkSync(wav);
  console.log('video', out);
}
await browser.close();
