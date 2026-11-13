// node score.mjs <page.html> <out.f32>  : renders window.renderScore() of a score page to raw float stereo 48 kHz
import fs from 'node:fs'; import path from 'node:path'; import { createRequire } from 'node:module'; import { pathToFileURL } from 'node:url';
const puppeteer = createRequire(import.meta.url)(process.env.PUPPETEER_CORE || 'puppeteer-core');
const [pageFile, out] = process.argv.slice(2);
const b = await puppeteer.launch({ executablePath: process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args: ['--allow-file-access-from-files'] });
const p = await b.newPage(); p.on('pageerror', (e) => console.error(e.message));
await p.goto(pathToFileURL(path.resolve(pageFile)).href); await p.waitForFunction('window.READY === true');
fs.writeFileSync(out, Buffer.from(await p.evaluate('window.renderScore()'), 'base64')); await b.close(); console.log('score', out);
