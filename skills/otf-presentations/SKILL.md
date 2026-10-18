---
name: otf-presentations
description: >-
  OTF Presentations (One Two Film) — turns a project into a short cinematic presentation, announcement or explainer video (HyperFrames:
  HTML + GSAP → MP4), and UNDERSTANDS THE CONTEXT first: from the chat (purpose, audience, claims in the user's own words, must-show,
  banned) and from the project's material (the director's reference frames and the source prompts embedded in them, the style lock, the
  best project frames ranked by closeness to the look, videos, text docs). It also chooses FONTS that actually render the language
  (Cyrillic coverage is tested, not guessed) and an ANIMATION vocabulary matched to the look. Use when the user asks for a presentation, announcement, teaser, launch or explainer video, "announcement", "presentation", "teaser",
  "how does X work", or a video about the pipeline itself.
user-invocable: true
---

# OTF Presentations

A film project's truth lives in the **chat** and in the **references**. OTF Presentations reads both, writes down what it takes
from where, and only then plans and renders the video in the project's own look.

```
chat + references + project frames + fonts
        │  Step 1  otf_context.py  → otf-context.json / .md, palette.png, hero_sheet.jpg
        ▼
  CONTEXT MANIFEST  (what, from where, why) ── confirmed with the user
        │  Step 2  plan + storyboard (beats, text, timing, motion vocabulary, audio)
        ▼
  HyperFrames composition  (Step 3)  →  check · snapshot · look at every frame
        ▼
  render MP4 + poster + share copy (Step 4)
```

## Step 1 — Understand the context (never skip)

### 1a. From the chat

Before any tool runs, write these down in the user's own words:
- **purpose:** announcement, teaser, explainer or presentation;
- **audience** and **language** of the on-screen text;
- **length** and **format** (16:9 / 9:16 / 1:1);
- **must-show:** the frames, people and moments the user named;
- **claims:** quote the user, do not invent marketing language;
- **banned:** what the user rejected earlier, e.g. flat grey look, emoji, SaaS colours, unsafe actions, a wrong face;
- **tone:** one preset (`cinematic`, `polished`, `trailer`, `documentary`, `playful`, `fireworks`) plus a free direction.

When something important is missing (purpose or language), ask once. Otherwise infer it and mark it as an assumption.

### 1b. From the material

```
python3 scripts/otf_context.py <project>/otf-presentations/context --brief "<one line from the chat>" \
  --refs <director reference folder> --assets <final frames folder> [--assets <videos/docs folder>] \
  --style-lock <project>/STYLE_LOCK.json [--fonts <extra font dir>] [--cyrillic]
```

The script writes:
- **references:** the metrics and the source prompt embedded in each one (Midjourney `Description`, `parameters`, `prompt`);
- **palette:** 8 colours taken from the references, with `palette.png`;
- **hero stills:** the project frames ranked by closeness to the look, with `hero_sheet.jpg`;
- **videos** (durations) and **text docs** (headings, to pull titles and claims from);
- **fonts:** every family classified (serif display / condensed / grotesk / script / mono). Each one is **tested for the language**:
  the script renders the glyphs, so "Cinzel (no Cyrillic)" is a fact, not a guess; capital letters are tested so caps-only fonts such as Bebas Neue are judged correctly. A display / accent / body pairing that covers the
  language is proposed.

Look at `hero_sheet.jpg` and `palette.png` yourself, then fill in `to_fill_by_model` in `otf-context.json`: purpose, audience, length,
format, must-show, claims, banned, tone, animation vocabulary and open questions.

### 1c. Confirm

Show the user the manifest in 6–10 lines:
- what the video is for;
- which frames, from which folders;
- the fonts, and why;
- the palette;
- the motion vocabulary;
- the length.

Proceed when they agree or say "go". If they asked to just do it, proceed and list your assumptions in the final report.

## Step 2 — Plan and storyboard

Write `<out>/plan.md`:
- the **angle** in one line;
- the **beats** with timestamps:
  - hook: 2–3 s;
  - reveal;
  - 3–6 "how it works" beats;
  - payoff, which shows the real output frames;
  - end card;
- the text per beat and how long it holds. A label holds at least 0.8 s once settled; a sentence about 0.3 s per word;
- **motion vocabulary**, chosen from the look and listed explicitly. Examples:
  - light sweeps and crepuscular-ray wipes;
  - slow push-ins on stills (Ken Burns with parallax);
  - cards flying in from depth;
  - scanning lines;
  - palette swatches dropping out of an image;
  - typographic slams on music hits;
  - anamorphic streaks on highlights;
  - deterministic particle sparks.

  If an animation catalog exists (`animation-effects-catalog`, `motion-style-core`), take matching entries from it.
- **audio:**
  - reuse the project's own score if it has one;
  - otherwise use a bundled or licensed track;
  - SFX only on real hits;
  - align cuts to beats with `npx hyperframes beats`.

Length: a teaser or announcement is 15–30 s. An explainer or "fireworks" piece may run 35–45 s if every beat earns its place.

## Step 3 — Compose with HyperFrames

- Read the docs: `npx hyperframes docs compositions | data-attributes | gsap | rendering | examples | troubleshooting`.
- Build the composition:
  - root `data-composition-id="root"` at 1920×1080 (or the format chosen);
  - timed `class="clip"` elements with `data-start` / `data-duration`;
  - one paused GSAP timeline on `window.__timelines["root"]`;
  - `<audio data-start>` for the music and SFX.
- **Assets:** copy every image, video and font into the composition with ASCII file names. Paths with spaces or Cyrillic break
  loading. Load fonts with `@font-face` from the copied files.
- **The look comes from the manifest:** the palette, the director's references and the light. A video about a dark, cinematic film is
  never a white SaaS card deck.
- Particles and noise must be deterministic: use a seeded generator driven by the timeline, so renders are repeatable.

**Gate:**
1. `npx hyperframes check` passes with zero errors.
2. `npx hyperframes snapshot` at 8–10 timestamps, and **look at every snapshot**. Fix:
   - overlaps;
   - unreadable or too-short text;
   - empty frames;
   - fallback fonts (Cyrillic shown in the wrong typeface);
   - anything that contradicts the "banned" list.

## Step 4 — Render and deliver

- `npx hyperframes render -q high -f 30 -o <out>/<name>.mp4`.
- Pick the best frame as `<name>.jpg`, a real story moment, not frame 0.
- Verify with `ffprobe`: duration, resolution, audio. Then extract 6–8 frames and look at them.
- Write `share-copy.txt`: one line plus 2–3 sentences in the user's language, with their claims and their words.
- Report:
  - the paths;
  - the scene list with timestamps;
  - what was taken from where (from the manifest);
  - assumptions;
  - anything not fixed.

## Series of parts

When one clip cannot tell everything, split the presentation into a SERIES of equal-length parts (e.g. 28 s each). Each part has:
- an opening card «Part N/M · topic»;
- the same end card.

Cover every step and rule of the subject across the parts, with real visuals in every beat, never text slides. Audio: the music score
only. Use SFX only if the user asks for them, because random clicks and whooshes read as noise. Then assemble the parts on a DaVinci
timeline with `davinci-series-assembly`.

## Image quality (hard rules)

- **No grain or noise overlays** in presentation videos: no film-grain layer, no dust, no noise textures. Grain in a UI-style presentation
  reads as "static noise" and is amplified by compression. The film look comes from the frames themselves.
- **Never upscale.**
  - Every displayed image must satisfy `natural size ≥ displayed size ÷ 1.4`.
  - Never blow up thumbnails (contact sheets, timecode sheets, hero sheets). Rebuild them from full-resolution sources, or show them
    small.
  - For video stills, extract frames at native size with ffmpeg.
- No CSS blur on content images, except deliberate depth-of-field on background plates.
- **Masters** use `-q high`. **Share copies** use CRF 18 with `-preset slow`. Do not use CRF 27 or `-tune grain`: dark gradients band and
  fine detail smears.
- After rendering, pull frames from the MP4 and inspect images at 100% for sharpness before delivering.

## Languages and frame rate
## Languages and frame rate

- **Bilingual by default when the video will be used for promotion.** Make the Russian (or source-language) cut first. When it
  passes, make an English copy:
  - translate every on-screen line;
  - keep file and skill names as they are;
  - re-check that the longer lines still fit and hold.
  - Name the files `…_ru` / `…_en`.
- **Render at the frame rate of the edit it goes into.** Ask, or read it from the target DaVinci timeline (`timeline get_setting
  timelineFrameRate`). A 30 fps clip on a 24 fps timeline drops frames and stutters. Render with `npx hyperframes render -f 24`
  (or the timeline's rate).

## Rules

- **Context before design.** No storyboard until the manifest exists and you have looked at its sheets.
- **Real material only.** The payoff shows the project's real frames, chosen by the look, plus any frames the user named.
- **Fonts must render the language.** Check the `cyrillic` flag in the manifest; never set Russian text in a font marked "no Cyrillic".
- **Respect the banned list** from the chat: a rejected look, a rejected face, unsafe imagery.
- Never upload or publish without an explicit request. Hyperframes `publish` is opt-in only.
- Related:
  - `style-lock-guard`: the look;
  - `frame-qc-contact-sheet`: checking frames;
  - `animation-effects-catalog` and the `motion-*` skills: motion vocabulary;
