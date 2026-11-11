---
name: cinematic-poster-designer
description: >-
  Designs striking, cinematic and unusual film posters for a project — one strong visual metaphor (an object replacing a head, a
  silhouette window, shard cut-outs, a lone figure in fog, a single colour field, the one sharp person in a blurred crowd) plus clean
  film typography. Learns the look ONLY from the user's favourite poster references (a curated LIKED list that grows over time),
  keeps a catalogue of poster devices and typography layouts, generates the key art without any text, then lays the title, tagline,
  credits and date in code (scripts/compose_poster.py) so the lettering is always perfect. Outputs 2:3 one-sheets plus 4:5 and 9:16
  versions. Use when the user asks for a poster, key art, a one-sheet, a cover or a thumbnail for a film, episode, promo or character;
  or when they add new poster references they like.
user-invocable: true
---

# Cinematic Poster Designer

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

## 1. The reference library (only what the user likes)

- Poster references live in the project's `references/poster/` folder (or wherever the user points).
- `LIKED.md` in that folder lists the references that define the look: one line per file with a 3–6 word note of what is liked
  ("the helmet-head metaphor", "wide-tracked thin title"). When the user adds or marks a favourite, append it there.
- When a reference is added, open it, decide which device (`references/POSTER_DEVICES.md`, D-ids) and typography layout (T-ids) it
  shows, and add a new device row only if it is genuinely new. Never learn from references that are not in `LIKED.md`; if the
  file does not exist yet, ask the user which of the folder's images they like most, or treat the whole folder as liked when they
  say so.

## 2. Concept before pixels

For each poster write a short card:

```
POSTER <project> · <variant>
Logline: <one sentence>
Metaphor: <the one image that says the logline without words>
Device: D<nn> (+ optional quiet second device)
Type layout: T<n> · title "<TITLE>" · tagline "<…>"
Palette: 60 <hex> / 30 <hex> / 10 <hex accent + its owner>
Characters: <names + their identity references, or "none / silhouette">
```

Offer 2–3 cards with different devices when the user has not chosen; recommend one. Good posters are surprising: prefer a metaphor
over a literal scene, a fragment over a full figure, a small subject in big negative space over a medium shot.

## 3. Generate the key art (no text)

- Prompt = the device's copy-ready art direction + the film's world + palette with owners + texture words (`film grain`, `paper
  grain`, `fog`) + `no text, no letters, no logos, no watermark, leave clean empty space at the <top|bottom|centre> for the title`.
- Attach identity references with role lines when a character must be recognisable (see `reference-style-builder`); for
  silhouettes and fragments, faces may stay anonymous.
- Generate at the poster's ratio (2:3 portrait) when the generator allows it; otherwise generate tall and crop.
- Make 2 variants of the chosen card; pick by the thumbnail test (shrink to 200 px wide: is the idea still there?).

## 4. Typography in code

```bash
python3 scripts/compose_poster.py ART.png OUT.jpg --title "FILM TITLE" --layout wide-top \
  --tagline "One line tagline" --credits "a film by … | Studio Name" --date "Coming soon" \
  --scrim 0.5 --size 2000x3000
```

- Layouts: `wide-top` (T1), `giant-bottom` (T2), `serif-center` (T3), `side-vertical` (T4). `--ink` / `--accent` take hex colours
  from the palette; `--scrim` adds a soft dark band behind the title when the art is busy there.
- Letterbox bars in the art are trimmed automatically before the crop.
- Then export the other formats from the same art: `--size 1600x2000` (4:5) and `--size 1080x1920` (9:16, re-check that the title
  does not cover the subject).

## 5. QC

1. Thumbnail test passes; one idea only.
2. Title, tagline, credits are spelled exactly; nothing overlaps a face.
3. Palette matches the card (run `reference-style-builder/scripts/palette.py` on the poster).
4. No generator text, watermark or logo anywhere in the art.
5. Characters are recognisable when the poster depends on them.

## Never

- Never let the image model draw the title or credits.
- Never use a reference the user has not marked as liked to steer the style.
- Never fill the poster edge to edge with detail; the negative space is the design.
