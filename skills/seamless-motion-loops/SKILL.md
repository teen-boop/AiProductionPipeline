---
name: seamless-motion-loops
description: >-
  Builds seamless looping motion-graphic backgrounds in brand colors as code (Canvas 2D in one HTML file) and renders them
  to MP4: title and lower-third backgrounds, filler for the dead seconds between AI shots, bumpers, transitions and shape
  animations, optionally with a character or product still (from Lovart, Higgsfield or an approved frame) composited over
  the loop on the same clock. Verifies the seam (frame at LOOP equals frame at 0, the step across the loop point matches the
  motion around it) before and after encoding, and shows the same loop as a HyperFrames composition for our promos. Use when
  the user says "seamless loop", "looping background", "motion background", "animated background behind the title",
  "filler between shots", "bumper", "brand-color loop", "the loop jumps", "check the loop seam", or needs an endless
  background under otf-presentations or a promo. Includes scripts/render-loop.mjs and scripts/loop-template.html.
user-invocable: true
---

# Seamless Motion Loops

Adapted from scenario-labs/skills, MIT (see `LICENSE-scenario.txt`).

A loop is a pure function of time, drawn with Canvas 2D in one HTML file. Nothing is generated, so nothing warps or flickers,
one color change rebrands it, and it renders at any size and aspect. Never make the loop itself with a video model: a generated
clip's last frame rarely meets its first. Keep the loop in code; generators make only the subject.

- `draw(ctx, w, h, t, P)` paints the frame at `t` seconds. Every period divides `LOOP` (12 s by default), so the frame at
  `LOOP` is the frame at 0.
- `scripts/loop-template.html` holds the helpers (`M.*`), the palette (`P`), one example tile (Perspective Floor, a grid
  streaming toward the camera), an optional subject overlay, and the preview/render engine (supersampling, motion blur).
- `scripts/render-loop.mjs` checks the page (determinism and seam), renders stills or the MP4, and checks the encoded file.
- `references/loop-craft.md`: the patterns that close a loop, depth without a 3D engine, review habits. Read it before
  writing a new `draw()`.
- `references/hyperframes-loop.html`: the same tile as a HyperFrames composition.

Related skills: `motion-graphics-director` (which route a motion piece takes), `motion-style-core` (the look and palette),
`otf-presentations` (promos and explainers that put titles over these loops), `music-beat-grid` (when a loop length should be
a whole number of bars), `nle-timeline-assembly` (laying loops between shots), `render-cut-verification` and
`frame-qc-contact-sheet` (checking the finished edit), `generation-backend-setup` (the generators that make the subject).

## Setup

Needs Node 18 or newer, ffmpeg 5.1 or newer with ffprobe, and Playwright where the script runs. Install Playwright in a
project or scratch folder, never globally, and run the script from that folder:

```bash
mkdir -p loops && cd loops && npm init -y && npm install playwright
# either download Playwright's browser:
npx playwright install chromium
# or skip the download and add --channel chrome to every command (uses an installed Google Chrome)
```

The script finds Playwright in the current folder first. Tested with Node 24, ffmpeg 9, Playwright from npm and
`--channel chrome`.

## Quick reference

```bash
cp <skill>/scripts/loop-template.html loop.html      # one loop per file: settings, draw(), overlay
# open loop.html in a browser to preview; ?t=3 freezes it, ?tone=accent or ?tone=light switches tone
node <skill>/scripts/render-loop.mjs loop.html --check                          # determinism and seam, no video
node <skill>/scripts/render-loop.mjs loop.html --stills look --at 0,3,6,9       # stills to look at
node <skill>/scripts/render-loop.mjs loop.html --out loop.mp4                   # 12 s, 1920x1080, 24 fps
node <skill>/scripts/render-loop.mjs loop.html --params "overlay=subject.png" --out loop.mp4   # with a cut-out
node <skill>/scripts/render-loop.mjs loop.html --width 1080 --height 1920 --out loop-9x16.mp4  # vertical
node <skill>/scripts/render-loop.mjs --qa loop.mp4 composite.mp4               # seam and format check of any MP4
```

- Existing files are never overwritten without `--force`.
- The page check renders one moment twice (they must match), compares the frame at exactly `LOOP` with the frame at 0, and
  compares the step across the loop point with the motion around it and at every half-second cycle boundary.
- A render refuses to encode unless the check prints `PASS`. `--ignore-seam` is only for a cut designed to sit at the loop
  point; it waives the seam verdict of both checks.
- Defaults: 24 fps, 8 motion-blur sub-frames over a 180 degree shutter, 2x supersampling, H.264 High, CRF 16, 4:2:0, BT.709
  limited range, faststart. Pass `--fps 25` or `--fps 30` to match the edit.
- Render time is about 0.4 s per frame at 1080x1920 for the example tile (a 4 s loop: 40 s); a full 12 s 1080p loop takes a
  few minutes. Run long renders in the background.
- Loop length: change `LOOP` in the page. The template's example tile and overlay take their periods from `LOOP`
  (`LOOP / 8`, `LOOP / 4`, `LOOP / 2`), so they close at any length. Your own tiles must use periods that divide your `LOOP`.
  A `--seconds` shorter than `LOOP` renders a test clip and skips the file's seam QA.

## Rules every tile follows

- **Periods**: every period divides `LOOP` (at 12 s: 1, 1.5, 2, 3, 4, 6, 12). Use `M.phase(t, period, offset)`.
- **Scrolls**: move a whole number of pattern repeats per period; a fractional repeat jumps at the seam.
- **Randomness**: only from `M.rand(i, salt)`. Never `Math.random`, `Date` or state carried between frames: motion blur and the
  checks render frames out of order.
- **Units**: sizes from `u = h / 100`, counts from `w`, so a loop holds at 16:9, 9:16, 1:1 and thumbnail size.
- **Colors**: only from `P` (`bg`, `fg`, `fg2`, `mid`, `accent`, `paper`, `ink`). Rebrand by changing `BRAND` (take the
  accent from the project's style lock); fix contrast by changing tone (dark, accent, light), never by adding a color.
- **Multi-hue loops**: a rainbow or hue sweep is the one exception. Compute hues as `hsl(${360 * M.phase(t, LOOP)}, ...)` with
  a period dividing `LOOP`, and keep its settings in `BRAND` so it still rebrands from one place.
- **Easing**: from `M.ease`, with anticipation, overshoot and holds. Constant speed only for scrolls and streams.
- **Text**: the loop carries no words by default; titles go on top in the edit or the HyperFrames composition. If a tile draws
  text, await `document.fonts.load(...)` before the first frame.

## Verify the seam

A loop is not done until the seam is measured, not eyeballed:

1. `--check` must print `PASS` (determinism ok, frame at `LOOP` vs 0 below 0.5, seam step within 2x its neighbors).
2. The render's own file check must end in `ok` (it runs automatically when the render is one full loop; run `--qa` on any
   other MP4, including composites and HyperFrames renders).
3. Independent check with ffmpeg. The last frame of a seamless loop is one step BEFORE the first, so it should differ from
   frame 0 by exactly as much as any two neighboring frames differ, no more:

   ```bash
   N=$(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 loop.mp4)
   for n in 0 1 $((N-2)) $((N-1)); do ffmpeg -v error -y -i loop.mp4 -vf "select=eq(n\,$n)" -fps_mode passthrough -frames:v 1 f$n.png; done
   psnr(){ ffmpeg -i "$1" -i "$2" -lavfi psnr -f null - 2>&1 | grep -o 'average:[0-9.inf]*'; }
   psnr f$((N-1)).png f0.png; psnr f0.png f1.png; psnr f$((N-2)).png f$((N-1)).png
   ```

   The three PSNR values should be within about 1 dB of each other. A much lower seam value is a jump; a much higher one (or
   `inf`) is a duplicated frame that stutters when the clip is looped.
4. Stills at `t = 0` and `t = LOOP` (`--stills dir --at 0,<LOOP>`) must be identical (PSNR `inf`).
5. Play it looped a few times (`ffmpeg -stream_loop 2 -i loop.mp4 -c copy loop_x3.mp4`) and watch the joins.

## Worked example: a character or product floating over a brand loop

1. **Build the loop first (local, free).** Copy the template, set `BRAND.accent` to the brand color, keep the example tile or
   write your own `draw()`, then `--check` and `--stills look --at 0,3,6,9`. Look at the stills.
2. **Get the subject.** Any approved still works: a character frame already locked for the project, a product shot, or a new
   cut-out from Lovart or Higgsfield (a paid call: name the service and cost and wait for a yes). Ask for "full body,
   three-quarter view, a light floating pose, on a plain flat background, no shadow, no text" so the cut-out is clean. Remove
   the background with the generator's own background removal or any local remover, and save a PNG with alpha next to
   `loop.html` (for example `subject.png`).
3. **Inspect the cut-out** at 100% over the loop's background color. Halos at the outline show on dark tones: redo the removal
   with a stronger edge setting rather than hiding them. For a known character, check the face against the approved sheet
   before it goes into any video.
4. **Composite in the canvas and render.**

   ```bash
   node <skill>/scripts/render-loop.mjs loop.html --params "overlay=subject.png" --stills look --at 0,0.75,1.5,2.25 --force
   node <skill>/scripts/render-loop.mjs loop.html --params "overlay=subject.png" --out subject-loop.mp4 --psnr 4
   ```

   `drawOverlay()` in the page floats the subject on a `LOOP / 4` bob and a `LOOP / 2` sway with a contact shadow, so the
   composite shares the motion blur and still loops. Adjust size and placement there. `--psnr` compares one encoded frame with
   its lossless render.
5. **Optional: a shot where the subject moves.** Generate a short clip from the still on a plain background with a locked-off
   camera (any video generator), remove its background to WebM VP9 with alpha (ProRes 4444 for an NLE), render the loop
   without the overlay, and lay the shot over it:

   ```bash
   ffmpeg -stream_loop -1 -i loop-plain.mp4 -c:v libvpx-vp9 -i shot.webm \
     -filter_complex "[1:v]fps=24,scale=-2:720[s];[0:v][s]overlay=(W-w)/2:(H-h)/2:shortest=1,format=yuv420p,setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv" \
     -c:v libx264 -crf 16 -preset slow -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
     -color_range tv -movflags +faststart -an composite.mp4
   ```

   The composite is as long as the shot and is not a seamless loop unless the shot loops: run `--qa` on anything meant to loop.
6. **Hand over** the HTML (the loop stays editable), the MP4, the stills and any composite.

## The same loop as a HyperFrames composition

Our promos render with HyperFrames 0.8.229 (`npx -y hyperframes@0.8.229 render`). When the loop sits under titles in a
promo, build it inside the composition instead of importing an MP4, so it renders at the promo's size and frame rate.
`references/hyperframes-loop.html` is the template's tile wired to HyperFrames:

- The canvas is redrawn from `e.detail.time` in an `hf-seek` listener, wrapped into `[0, LOOP)` with `mod`. The tile itself is
  unchanged: same `draw(ctx, w, h, t, P)`, same rules. Do not animate the canvas with GSAP tweens or
  `requestAnimationFrame`; the seek must drive it.
- Size comes from the root's `data-width` and `data-height`. Set `data-duration` to `LOOP` or a whole multiple of it, so the
  composition ends on the seam.
- An empty paused GSAP timeline spanning `LOOP` is registered in `window.__timelines["main"]`, as our promo pages do.
- To render it alone: copy it as `index.html` into an empty folder, set `LOOP`, `data-duration`, `data-width`, `data-height`
  and the viewport meta together, then run `npx -y hyperframes@0.8.229 render -q delivery -o loop.mp4` in that folder. Check
  the result with `render-loop.mjs --qa` and the PSNR steps above.
- Inside a promo: move the canvas, style and script into a `<template>` sub-composition (all CSS and scripts must live inside
  the template) and give its host slot `data-track-kind="graphics"` and a `data-duration` that is a whole multiple of `LOOP`.
  Put titles on a higher track. Mark the canvas `data-layout-allow-overflow` (it is full-bleed art).
- HyperFrames renders frames without the template's motion-blur sub-frames. For fast tiles, either accept the crisper look or
  render the loop with `render-loop.mjs` and place the MP4 as a `<video>` clip (`muted playsinline`, looped by stacking
  whole-loop clips end to end).

## Common mistakes

- **A seam jump at `LOOP`.** A period that does not divide `LOOP` (a 5 s cycle in a 12 s loop), or a scroll that moves 2.5
  repeats. `--check` reports `SEAM JUMP`. Fix the period; never crossfade the ends.
- **Changing `LOOP` without the periods.** A tile written for 12 s with a hard-coded 1.5 s or 3 s period breaks at 4 s. Derive
  periods from `LOOP`, or re-check every period.
- **State, `Math.random` or `Date` in a tile.** The same `t` gives different frames and the loop cannot close. `--check`
  reports `NOT DETERMINISTIC`.
- **Color helpers that only read hex.** `P.mid` and `M.mixColor` return `rgb()` strings, and a hex-only parser silently turns
  them black. Use the template's `M.rgba` and `M.mixColor`.
- **Strobing on fast moves.** Eight sub-frames show stepped copies on a whole-frame push. Raise `--samples` for very fast loops.
- **Treating every flag as a bug.** A designed snap (a pop, a burst) or a hold at the loop point can trip the seam check. Look
  at the frames before changing the code.
- **A counter that wraps wrong.** Anything indexed by cycle wraps with `M.mod`, or it reads "06 / 05" at the loop point.
- **Opening the page from `file://` to render.** A local overlay image taints the canvas and the readback fails.
  `render-loop.mjs` serves the folder over a local address; the browser preview is unaffected.
- **Chasing bitrate.** Flat color compresses to a small file with almost no loss. The real loss is 4:2:0 chroma on thin
  saturated lines: check with `--psnr` and thicken those lines.
- **Color flags without `setparams`.** `-colorspace`, `-color_primaries` and `-color_trc` alone can leave primaries and
  transfer untagged. End the filter chain with `setparams`, as both commands here do. `--qa` reports `UNTAGGED COLOR` otherwise.
- **Losing the alpha of a VP9 shot.** ffmpeg's built-in VP9 decoder ignores alpha and the shot arrives in a black box. Put
  `-c:v libvpx-vp9` before `-i shot.webm`.
- **A loop length the edit cannot use.** Match `--fps` to the edit, and for a music cut make `LOOP` a whole number of bars
  (`music-beat-grid`), so repeats land on the grid.
