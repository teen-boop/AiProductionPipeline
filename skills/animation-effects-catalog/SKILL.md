---
name: animation-effects-catalog
description: Interactive shot-by-shot prompt builder AND growing catalog of proven tricks that make AI video (Seedance 2.x, Higgsfield, Kling, Veo) look cinematic and impressive — organised by HERO TYPE (tiny creatures, giants vs tiny humans, real animals, surreal anatomy, painted/puppet/material characters, levitation, falling/action humans, face recast) and by EFFECT (camera, physics and contact, performance, voice and sound, light and integration, workflow modes, negative blocks). Each entry gives when to use it and a copy-ready English phrase. Use while writing or upgrading any video/animation prompt, when a shot feels flat, fake, floaty or staged, when a character type is unusual, or when the user pastes a strong prompt to "learn from" — then extract its new tricks and append them here. Triggers on boost the animation, effects for animation, tips catalog, make it impressive, learn from this prompt, how to make this shot better, cinematic tricks, video prompt tips.
---

# Animation effects catalog

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

A library, not a template. `cinema-director-v3` gives the prompt its spine; this catalog supplies the *moves* that make it hit. Pick 3–6 entries that fit the shot — never paste the whole catalog.

## INTERACTIVE MODE — shot by shot, together with the user (default when building a new animation)

The user chooses; Claude proposes. Never write the whole prompt alone in this mode.

**Stage 0 — setup (once per scene):** confirm target model/length, the list of shots with timings, references/tags, and the scene's emotion in one line. Show it as a short table and ask "go?".

**Stage 1 — per shot, CAMERA:** offer 3–4 camera options for THIS shot, each one line: rig + move + lens + what it gives emotionally (e.g. "dolly push-in, 32mm — calm, draws us into the group"; "handheld arc, 80mm — intimate, alive"; "locked-off wide — deadpan comedy"; "low insert — detail, suspense"). Mark one as recommended. Pull options from CATALOG section B and the hero type in section A.

**Stage 2 — per shot, ENHANCEMENTS:** offer 4–6 enhancement options (multi-select) from the catalog that fit this shot and hero type — e.g. "already in progress", "insert detail", "hold on the empty frame", "task → trigger → reaction", "contact before motion", "exposure jump", "scale by props", "SFX beat / silence". One line each, with what it adds.

**Stage 3 — per shot, ASSEMBLE:** write only this shot's block (CAMERA with forbidden moves · WHAT WE SEE · ACTION with timestamps · physics/sound notes) from the chosen options and show it. Ask: keep / change one thing.

**Stage 4 — next shot.** Repeat 1–3. Keep a running list of chosen options so later shots stay consistent (e.g. if shot 1 is locked-off deadpan, suggest contrast for shot 2).

**Stage 5 — scene assembly:** wrap the approved shot blocks with the scene-level parts (FORMAT with absolute cuts, LOOK, NO TEXT, SCRIPT/SCALE/GEOMETRY locks, REFERENCES, ACTING TASKS, SOUND score, NEGATIVE, RECAP), save to the project's prompts folder, and report the word count.

Rules: use AskUserQuestion with short options (camera = single choice, enhancements = multi-select) when available; otherwise a numbered list. One shot per round. Respect choices even if Claude would pick differently — but say in one line if a choice breaks continuity or the model's limits.

## How to use
1. Identify the **hero type(s)** in the shot → read that section of `references/CATALOG.md` (section A).
2. Identify what the shot must *feel* like (speed, weight, wonder, comedy, fear, tenderness) → pick from sections B–F.
3. Identify the **workflow mode** (text-to-video, start-frame image-to-video, video-to-video recast, placeholder/blocking video, multi-scene edit) → section G.
4. Close with the matching **negative block** template → section H.
5. Write the chosen tricks into the prompt as concrete sentences in the right spine slot (ASSETS, CAMERA, ACTION, PHYSICS, ACTING, AUDIO, LOCKS) — never as a disconnected tag list.

## How to grow the catalog ("learn from this prompt")
When the user pastes a strong prompt:
1. Read it fully. For every technique ask: *is it already in CATALOG.md?* If yes, only add a sharper example phrase if it is clearly better.
2. Add each NEW technique as one entry in the right section: **name — when — copy-ready phrase**. Generalise names and props (no brand names, no specific people), keep the phrase reusable.
3. Add a line to the SOURCE LOG at the bottom of CATALOG.md (date, short description of the source prompt, which entries it added).
4. If the trick changes how prompts must be *structured*, also add one line to `cinema-director-v3`.
5. If the skill lives in a git repo, commit and push only when the user asks.

## Rules
- Every trick must produce a visible pixel or an audible sound. Mood words are not tricks.
- Measured beats vague: metres, centimetres, degrees, seconds, step counts.
- One trick per need. Two tricks doing the same job dilute each other.
- The user's project rules (identity references, style lock, continuity sheet) always win over a catalog entry.
