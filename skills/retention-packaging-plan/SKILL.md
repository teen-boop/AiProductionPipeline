---
name: retention-packaging-plan
description: >-
  Plans the on-screen "packaging" of a talking-head, explainer or creator-style video as a cue sheet anchored to WORDS, not seconds:
  the 30-second hook formula, a new visual event every 3-5 s in the opening, punch-in cuts on sentence boundaries for single-camera
  presenters, evidence cards with sources, numbers that land, chapter cards, captions by format, two calls to action, a callback
  ending, and the cover frame spliced in as the first frame. Every cue is written as "segment:word" and validated against the word
  timeline before rendering, so re-timed audio never breaks the edit. Engine-agnostic: HyperFrames, Remotion, or NLE titles. Use when
  the user says "package this video", "make it hold attention", "add captions and cards", "it feels slow", "add a hook", "MrBeast
  pacing", "add a chapter card", "make the first 30 seconds stronger", "make the cover the first frame".
user-invocable: true
---

# Retention Packaging Plan

> **Ask first: what kind of video is this?** Before planning, ask the user the video type and destination (e.g. daily social post / reel, talking-head explainer, cinematic promo or trailer, tutorial, film episode). Apply this packaging only to social / creator / explainer formats, and only as far as the user wants; never force retention tricks onto a cinematic promo or a film.

`otf-presentations` and its `EDIT_PATTERNS.md` cover premium cinematic pieces (long holds, few cuts, little text). Creator-style
talking heads and explainers work differently: the picture changes constantly even when the camera does not. This skill plans that
layer.

Pacing figures come from a frame-by-frame study of 25 creator videos.

## 1. Pick the pacing target first

Ask once: platform, length, and "calm, standard or lively?" Then set the target:

| Feel | Cuts per minute | Typical shot | New visual event |
|---|---|---|---|
| Calm review (MKBHD-like) | 5-7 | about 8 s | text almost only for numbers |
| Standard explainer (Vox / Johnny Harris-like) | 10-26 | about 3 s | densest in the first 60 s |
| Lively vertical (MrBeast-like) | 24-25 | about 1.8 s | every 3.3-5 s in the first 30 s |
| Animated explainer (Kurzgesagt-like) | 4.5-10 | no hard cuts, constant motion | a beat every 4-5 s |

Rule for all of them: cuts may be few, stimulation may not stop. In the first 30 s something new appears every 3-5 s.

## 2. The opening (30 s hook)

```
0-3 s    the claim or the action. No greeting, no name, no logo.
3-15 s   turn the claim into visible evidence: a number, a screenshot, a small experiment.
15-30 s  the main question on screen, or a twist.
22-60 s  first chapter card = end of the cold open.
```
AI presenter trick: the first 5-20 s may show no face at all (B-roll, type cards) to hide the hardest lip-sync segment; the presenter
enters by 3-10 s and points at the evidence early.

## 3. The body

- **Punch-ins** (single camera): hard-cut the same take between 1.0x, about 1.18x and about 1.32x at sentence boundaries, with a
  slight left or right offset. Costs nothing and reads as a second camera. Never punch in mid-word.
- The presenter stays full-screen at most about 12 s at a time; then board + presenter picture-in-picture, or presenter + a
  floating object beside them.
- **Evidence**: every number or claim on screen gets a source tag (small, lower left, 3-5 s). Logos inside screenshots are blurred.
- **Numbers that land**: counters snap to the exact final value on the last frame (eased curves stop at 99.9 and round wrong).
- **Chapter cards** every 2-5 minutes on long pieces; a recap board before the end.
- Retention captions (the one question the viewer should keep in mind) on long holds only.

## 4. Captions and on-screen text, by format

- Vertical short, CJK or high-energy: word-by-word animated captions, bold with outline.
- Landscape explainer: bottom subtitles, single line, heavy weight, hard cuts in and out, around y = 92 % of frame height.
- Launch or review: no burned-in subtitles; the screen is for evidence cards and numbers (platform CC covers accessibility).
- English and premium styles: text only for numbers, key terms, and name/time labels.
- Text never covers the presenter's mouth or eyes.

## 5. Calls to action and ending

- Two calls to action: one in the first 15 s or just before the reveal, one at the end.
- End by calling back to the opening (same image, same question). Extras go after the final call to action.

## 6. Write the cue sheet anchored to words

Cue sheet `edit/packaging.json`, one entry per cue:

```json
{"use": "number_card", "at": "3:ninety-nine", "until": "3:end", "text": "$99", "source": "price page, 2026-10"}
```
- `at` / `until` are `"segment:word"`, `"segment:"` (segment start), `"segment:end"`, `"segment:word#2"` (second occurrence), or
  absolute seconds as a last resort.
- Resolve every anchor against the word timeline (from `ai-presenter-talking-head` or any forced-alignment transcript) BEFORE
  rendering. A missing word, a segment number out of range, or two cards overlapping in the same screen zone is an error. Fix the
  sheet, then render.
- Re-voiced or re-timed audio: regenerate the word timeline and re-resolve; never shift cues by hand.

Build in the chosen engine: HyperFrames (one timed clip per cue), Remotion, or NLE titles/markers via `nle-timeline-assembly`.

## 7. Cover as the first frame

Most platforms take frame 0 as the thumbnail, so make the cover and splice it in:
1. Pick a presenter frame: eyes open, mouth closed or smiling, not mid-word (contact sheet of 12 candidates).
2. Layout: small kicker line, hook title (very short), one accent phrase, one subtitle, up to 3 tags, up to 2 evidence cards,
   the AI-presenter label. Must read at 540 px wide.
3. Splice: the cover holds 0.5 s then hard-cuts into the film; the audio is delayed by the same 0.5 s with silence in front;
   same size and frame rate as the film. Limit peaks before re-encoding.
4. Check frames at 0 s, 0.45 s and 0.55 s. Keep a no-cover version as well.

## 8. Check before delivery

Render, then a contact sheet of the start and midpoint of every cue and every mid-transition frame (the tail of one cue can cover the
next at a zero gap). Fix overlaps, empty boards, unreadable text, a picture-in-picture covering content.

## Never

- Never use internet memes, film or TV stills, celebrity faces or another channel's sting. Make original stickers from the project's
  own presenter or characters.
- Never invent a number, price, review or test result; illustrative data is labelled "illustrative" on screen.
- Never use a real person's photo on a name plate without permission; use a silhouette or an original character marked "illustrative".
- Never time cues in raw seconds when a word anchor exists.
- Never put an SFX or a card on every cut; events only.
