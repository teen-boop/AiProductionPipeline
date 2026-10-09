---
name: animation-effects-catalog
description: Growing catalog of proven tricks that make AI video (Seedance 2.x, Higgsfield, Kling, Veo) look cinematic and impressive — organised by HERO TYPE (tiny creatures, giants vs tiny humans, real animals, surreal anatomy, painted/puppet/material characters, levitation, falling/action humans, face recast) and by EFFECT (camera, physics and contact, performance, voice and sound, light and integration, workflow modes, negative blocks). Each entry gives when to use it and a copy-ready English phrase. Use while writing or upgrading any video/animation prompt, when a shot feels flat, fake, floaty or staged, when a character type is unusual, or when the user pastes a strong prompt to "learn from" — then extract its new tricks and append them here. Triggers on усилить анимацию, эффекты для анимации, каталог подсказок, сделать впечатляюще, научись у этого промпта, how to make this shot better, cinematic tricks, video prompt tips.
---

# Animation effects catalog

A library, not a template. `cinema-director-v3` gives the prompt its spine; this catalog supplies the *moves* that make it hit. Pick 3–6 entries that fit the shot — never paste the whole catalog.

## How to use
1. Identify the **hero type(s)** in the shot → read that section of `references/CATALOG.md` (section A).
2. Identify what the shot must *feel* like (speed, weight, wonder, comedy, fear, tenderness) → pick from sections B–F.
3. Identify the **workflow mode** (text-to-video, start-frame image-to-video, video-to-video recast, placeholder/blocking video, multi-scene edit) → section G.
4. Close with the matching **negative block** template → section H.
5. Write the chosen tricks into the prompt as concrete sentences in the right spine slot (ASSETS, CAMERA, ACTION, PHYSICS, ACTING, AUDIO, LOCKS) — never as a disconnected tag list.

## How to grow the catalog ("научись у этого промпта")
When the user pastes a strong prompt:
1. Read it fully. For every technique ask: *is it already in CATALOG.md?* If yes, only add a sharper example phrase if it is clearly better.
2. Add each NEW technique as one entry in the right section: **name — when — copy-ready phrase**. Generalise names and props (no brand names, no specific people), keep the phrase reusable.
3. Add a line to the SOURCE LOG at the bottom of CATALOG.md (date, short description of the source prompt, which entries it added).
4. If the trick changes how prompts must be *structured*, also add one line to `cinema-director-v3`.
5. If the skill lives in a git repo (e.g. AiProductionPipeline), commit and push when the user asks.

## Rules
- Every trick must produce a visible pixel or an audible sound. Mood words are not tricks.
- Measured beats vague: metres, centimetres, degrees, seconds, step counts.
- One trick per need. Two tricks doing the same job dilute each other.
- The user's project rules (identity references, style lock, continuity sheet) always win over a catalog entry.
