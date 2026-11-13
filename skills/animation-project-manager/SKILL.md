---
name: animation-project-manager
description: Project manager for the animation layer of a video (presentation, ad, explainer, landing-page film). Reads the brief and the edit, breaks it into beats, and for every beat picks the animation that will make it look best from the catalogs (code-motion-catalog 3D styles, motion-graphics-director blocks, cinematic-motion-graphics, seamless-motion-loops, animation-effects-catalog tricks for AI video), sets the rhythm (fast montage blocks against 3D chapters), plans the sound, writes one ANIMATION_PLAN with sources, timings, assets and cost, waits for approval, routes each build to the right skill, assembles and checks the result. Use when the user says "make it look cooler", "add animations to the video", "which animation fits here", "plan the motion for this presentation", "make the presentation longer but better", "mix 3D and montage", or when an edit feels flat. Triggers - animation plan, motion plan, animation project manager, add effects to the video, make the edit cooler, pick animations from the catalog.
---

# Animation project manager

## This project first (binding)
1. **Study this project:** the brief, the script or edit plan, the approved frames, clips and references, `LESSONS.md`.
   Say in concrete terms what exists before planning.
2. **Learn from this project's results:** after approval or rejection, write what worked and what failed to `LESSONS.md`.
3. **Stay inside this project:** no images, fonts, music, copy or names from other projects.
4. **Examples here are samples.**
5. **General lessons** go to the catalogs, without project names.

## The catalogs it chooses from
| Need of the beat | Catalog / skill | Typical pick |
|---|---|---|
| One product, one claim, a premium hero or end card | `code-motion-catalog` | Studio Product (light is the story, macro passes, lock-up) |
| A list, ranking, numbers, a claim that should land | `code-motion-catalog` | Split-Flap Board (hero row in amber) |
| A process, a stack, how something works | `code-motion-catalog` | Layer Stack (sheets lift, a pulse goes down and back) |
| Charts, kinetic type, explainer boards, collage | `motion-graphics-director` (block library), `hyperframes` | kinetic slams, count-ups, boards |
| Period, documentary, maps, title and end cards in a film look | `cinematic-motion-graphics` | route maps, stamps, lower thirds |
| Background under titles, filler between shots | `seamless-motion-loops` | brand-colour loop |
| AI video shots that must feel cinematic | `animation-effects-catalog` | camera moves, contact, performance tricks |
| Real footage or approved stills of the project | the project itself | living stills, frame bursts |

## Workflow
1. **Beat sheet.** List the beats of the piece with their job (hook, promise, proof, how it works, result, call to action),
   target length and formats. If the user says "longer but better", add chapters, not padding.
2. **Pick per beat.** For each beat give 1 recommended option and 1 alternative from the table above, one line each with
   what it adds. Prefer the project's real material first, code animation second, new generation last (cost).
3. **Rhythm plan** (from the edit-pattern study used by `otf-presentations`):
   - open on something already beautiful: a 3D macro or a living still, no text in the first 1.5 s;
   - accelerate and release: fast blocks of 0.3-1.6 s shots, then a 3D chapter of 7-9 s as a breather, then fast again;
   - one hero effect per beat; never two neighbouring shots at the same scale;
   - flash cuts (2 frames to near-white) only on accents; the end holds 3-4 s.
4. **Sound plan.** 3D chapters keep their own score; a bed (code-motion-catalog `score-template.html`) under the fast
   blocks that steps back under the chapters; a whoosh into every flash, a hit on it, one hit per kinetic word, shutters
   on frame bursts, clicks on timeline snaps; mix to about -14 LUFS for the web.
5. **Write `ANIMATION_PLAN.md`** in the project's edit folder: a table of beats with start, length, source skill, style,
   on-screen text, assets needed, sound, cost (0 for code), and a list of assumed facts. Show it and wait for the user's OK.
6. **Route the builds:** code pieces -> `code-motion-catalog` (storyboard stills first), HTML/HyperFrames blocks ->
   `hyperframes` / `otf-presentations`, AI shots -> the generation skills with `animation-effects-catalog` tricks.
7. **Assemble and check:** one composition; `frame-crop-guard` on every aspect; a contact sheet of 8-10 frames from the
   final MP4; loudness; legibility on a phone (big words, nothing cut at the edges); then deliver.

## Rules
- Titles: large, uppercase, a stylish display face that fits the brand; accents in one brand colour.
- No made-up numbers or claims on screen; boards without a source say what happens, not how much.
- Every paid generation waits for the user's yes; code animations and existing material come first.
- Keep it lean: plan from what is on disk, do not launch research agents for a motion plan.
