# Build, verify, render

The engines are local tools: the HyperFrames CLI (HTML + GSAP rendered by headless Chrome and ffmpeg), Remotion, and ffmpeg. Pin
the engine version the project tested; do not run vendor commands that install or update skills, sign in, render in a cloud or
publish.

## 1. Scaffold

```
motion/<shot-id>/
  shot-plan.json
  index.html        copied from a template or written from the category file
  fonts/            the glyph-tested font files (ASCII file names)
  plates/           frozen plates, scans, traced SVGs, coastline data (no remote URLs)
```

Copy `assets/templates/date-stamp.html` (from this skill) to `index.html` for stamps and clocks; for other categories write the
composition from the category file. Replace the generic font stacks with `@font-face` rules pointing into `fonts/`, and the palette
tokens with values from the look sources.

## 2. Composition contract (HyperFrames)

- One root element with `data-composition-id`, `data-width`, `data-height`, `data-duration`, `data-fps="24"`.
- Exactly one GSAP timeline created paused, registered as `window.__timelines["<composition-id>"]` after it is fully built.
- **Seekable, deterministic:** the renderer jumps to arbitrary times. Every visual state must be a function of timeline time:
  - counters, clocks, typewriters, grain seeds and markers are proxy tweens whose `onUpdate` writes the state;
  - no `Date`, no unseeded random, no network, no timers, no one-shot callbacks for state;
  - delayed elements use `fromTo` with an explicit hidden start (`autoAlpha: 0`), or a static initial state set at build time.
- Do not tween visibility on elements that carry `data-start` (the runtime owns them); animate a child.
- Do not combine a CSS `transform` and a tween on the same property; put the start state in the tween.
- Text lays out with flex and padding inside the safe area; absolute positions only for decoratives and map-anchored labels.
- Variables (`data-composition-variables` on `<html>`) make strings and switches overridable at render time
  (`--variables '{"date":"..."}'`); every string passed this way must still be an approved text in the spec.
- A full-frame plate or grain must not be present in an alpha render (see the template: `transparent` hides both).

## 3. Remotion (alternative engine)

Use `motion-remotion-build` with these cinema overrides in its setup prompt: 24 fps, ease-in-out interpolation instead of springs
for type (springs only with full damping, no overshoot), grain derived from the frame number, fonts loaded from local files.
Transparent export:

```bash
npx remotion render <CompId> out.mov --codec=prores --prores-profile=4444 --pixel-format=yuva444p10le --image-format=png
```

## 4. Verify

```bash
python3 <skill>/scripts/spec_lint.py shot-plan.json
cd motion/<shot-id>
npx hyperframes lint .
npx hyperframes check .                    # layout, motion, contrast; first_frame_empty is expected for overlays
npx hyperframes snapshot . --at 0.5,3.6,7.0,11.6 -o qc/snaps   # times from qc.snapshots_at
```

`snapshot` writes a contact sheet next to the stills; open it. Render one QC pass with the `guides` variable on to see the safe area.

**Legibility over the real plate** (overlays): composite a snapshot over the graded frame it will sit on, then look at it full size
and at phone size:

```bash
ffmpeg -i plate_frame.png -i qc/snaps/<still>.png -filter_complex "[0][1]overlay=0:0" qc/composite.png
ffmpeg -i qc/composite.png -vf scale=480:-1 qc/composite_phone.png
```

**Own contact sheet from a render** (one frame every second, 4 columns):

```bash
ffmpeg -i renders/<file> -vf "fps=1,scale=480:-1,tile=4x3" -frames:v 1 qc/sheet.jpg
```

## 5. Render

```bash
npx hyperframes render . --format mov -o renders/<shot-id>_<lang>_<aspect>.mov          # ProRes 4444 with alpha
npx hyperframes render . --format webm -o renders/<shot-id>_<lang>_<aspect>.webm        # VP9 with alpha
npx hyperframes render . --format mp4 -q delivery -o renders/<shot-id>_<lang>_<aspect>.mp4  # full-frame graphic
npx hyperframes render . --format png-sequence -o renders/<shot-id>_png                 # RGBA frames for Fusion / Nuke
```

Pass overrides with `--variables` (for example `'{"transparent":true}'`). Render each language and aspect separately.

**Probe every file:**

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,profile,pix_fmt,width,height,r_frame_rate,nb_frames -of default=nw=1 <file>
```

Expect `r_frame_rate=24/1`, `nb_frames = duration x 24`, the spec size, and for alpha a `yuva` pixel format (ProRes 4444:
`yuva444p12le`).

**Alpha veil check:** extract the alpha of a frame where nothing should be visible (before the first entrance) and of a hold frame.
The first must be 0 everywhere; the second must be 0 outside the graphic.

```bash
ffmpeg -ss 0.2 -i renders/<file>.mov -frames:v 1 -vf "alphaextract,format=gray" -f rawvideo qc/alpha.raw
python3 -c "d=open('qc/alpha.raw','rb').read(); print('nonzero share', 1-d.count(0)/len(d), 'max', max(d))"
```

**ProRes to WebM alpha** (when only one render was made):

```bash
ffmpeg -i in.mov -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 18 -auto-alt-ref 0 out.webm
```

**Neutral + LUT pipeline:** apply the project LUT once, after the render: `ffmpeg -i in.mov -vf lut3d=project.cube ...` (keep
ProRes 4444 for alpha), or apply it in the NLE on the graphic's track. Never on a graphic built from graded samples.

## 6. Hand-off

Give `nle-timeline-assembly` one entry per graphic: file, track (overlays on V2 and up), `record_in` on the cut, no retime. Add a
marker with the shot id. After the film export, `render-cut-verification` checks the cuts around each graphic on the encoded file.
