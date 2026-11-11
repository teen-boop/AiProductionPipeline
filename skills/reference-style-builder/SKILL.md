---
name: reference-style-builder
description: >-
  Builds a project's REFERENCE SET the right way, by learning from the project's own reference library first: style references
  (images, video frames), saved prompts (references/prompts/*.md with "why it works" notes) and approved frames. It distils a
  measured STYLE CARD (palette as 60/30/10 with hex values measured by script, light, lens and camera height, film stock and grain,
  composition, texture words, period, negatives), then generates the references in a fixed order — style frame → character sheet or
  diptych → empty location plate → prop sheet → keyframes → "change to" close-ups — and writes every reference's ROLE line
  ("look only", "controls face and outfit only", "never its background or pose"). Checks each result against the card (palette
  drift, identity, text leaks) before it is used. Use when starting visuals for a new style or promo, when the user drops new style
  references or prompts, when frames "don't look like the references", or when asked to build character/location/prop references.
user-invocable: true
---

# Reference Style Builder

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

References decide the look before any prompt does. This skill turns a pile of inspiration into a small, ordered, measured reference
set that every later prompt can lean on. It works with any image generator (Lovart, Krea, Higgsfield, Midjourney, by hand).

## 1. Read the library before generating anything

Look in this order and write down what each source contributes:

1. **Style references** (images, frames pulled from reference videos at 2–3 telling moments). Open them; do not judge by file name.
2. **The prompt library** (`references/prompts/*.md` or wherever the project keeps saved prompts). Each entry should hold the prompt
   verbatim plus "why it works" and "what to fix". Reuse its structures (character card, LOOK table, accessory lock, shot fields,
   cut markers), not only its adjectives.
3. **Approved frames** from earlier work (a style frame the user liked is a stronger reference than the original inspiration).
4. **Character references** (persona sheets, real photos) and their standing rules (tags, voice, signature props).

If a source is missing or unreadable (a login wall, a private post), say so and work with what loaded.

## 2. Write the STYLE CARD (one per style)

Measure what can be measured; describe the rest in concrete, visible words.

```
STYLE <id> · <name>
Reference files: <paths>
Palette (measured): 60 <hex> <name> · 30 <hex> <name> · 10 <hex> accent <name and what carries it>
Light: <sources, direction, hardness, colour, time of day — "hard noon sun", not "beautiful light">
Lens / camera: <focal length or FOV, height, distance, fisheye/anamorphic/spherical, movement character>
Film / texture: <stock, grain, halation, bloom, vignette, sharpness>
Composition: <symmetry, horizon, frame-in-frame, negative space, scale of people>
Period / world: <era, place, materials>
Signature device: <the one trick that makes this style recognisable — e.g. frame rotated 90°, frozen time, projected text>
Negatives: <what would break it — glossy AI look, extra colours, readable signage>
```

- Measure the palette with `python3 scripts/palette.py <ref images…>`. It prints dominant colours with their share of the frame and a
  60/30/10 reading where the accent is the most saturated colour covering at least 2% (not merely the third-largest).
- The 10% accent must have an owner in the scene: a hat, a neon sign, a car. Write it into costume, prop or set design, so the
  generator places it rather than tinting everything.
- Keep the card short. Every line must be something a generator can see.

## 3. Build the references in this order

Each step uses the previous step's approved output as a reference. Never skip forward.

| # | Reference | Prompt essentials | Role line used later |
|---|---|---|---|
| 1 | **Style frame** — one hero image in the style | the style card + the style reference attached as "copy the look, colour, lens and grain, not the people" | "look only" |
| 2 | **Character sheet** — mid-grey studio, full-body front/side/back + 3 head angles, even light; or a **16:9 diptych** (full-length + large portrait) graded in the target film stock | identity details listed (face, hair, every garment, shoes, signature prop) | "controls face and outfit only" |
| 3 | **Location plate** — the place EMPTY, same look | "no people", the style card | "the place and its light only" |
| 4 | **Prop sheet** — the recurring objects on grey | exact materials and colours | "controls this object only" |
| 5 | **Keyframes** — hero + plate + props in action | refs 1–4 attached with their role lines | start frames for video |
| 6 | **Change-to close-ups** — re-framed from an approved keyframe | "the SAME moment, re-framed tighter, same light and colour" | first/last pairs |
| 7 | **Storyboard sheet** (optional) — pencil panels of the shots | panels described one by one, "illegible scribbles only" | planning material |

Role lines go into every prompt that uses the reference, for example:
`Image 1 = the LOOK only (soft blue dusk, one warm window light from the left) — copy its light, colour and mood, not its place.
Image 2 = CHARACTER A (face, short grey hair, round glasses, green raincoat) — keep this person exactly. Do not inherit reference backgrounds or poses.`

## 4. Check every result against the card

Before a reference is used by anything downstream:

1. **Palette:** run `palette.py` on the result and compare with the card. A missing accent or a new dominant colour is drift; fix the
   prompt (name the colour's owner) rather than accepting it.
2. **Identity:** compare faces with the character sheet at the same scale (crop both). A thinner, younger or "prettier" face is a
   fail; regenerate with "CRITICAL: exactly the face from the large portrait in image N — <3–4 concrete traits>" and attach an
   approved frame of the same person as a second identity reference.
3. **Text leaks:** storyboard captions and signs often come out readable (sometimes as the prompt's own words). Ask for
   "illegible scribbles only"; if they still appear, crop or mask in the edit and note it.
4. **Watermarks copied from the reference** (e.g. a video-model watermark in a corner): crop in the edit or regenerate.
5. **Duplicates:** when copying frames into a hand-off folder, compare checksums; two different shots must never be the same file.

## 5. Generator behaviour worth knowing (Lovart and similar agents)

- An agent may answer with text and not call the image tool ("done" with no artifact). Retry the same prompt once; if it repeats,
  shorten the prompt or name the model explicitly.
- An attached image can push the agent to a paid *edit* tool and ask for credit confirmation. Never confirm on the user's behalf. For
  pure illustrations (a storyboard sheet), drop the attachment and describe the character in words instead.
- Free/queued modes are fine for references; ask before anything that spends credits (video, upscales, paid edits).
- Keep project and thread per production; copy every accepted result into the project folder with a stable, sortable name
  (two-digit ids: S01…S10, so S10 never sorts between S1 and S2).

## 6. Hand-off

Write a short `REFERENCES.md` next to the images: the style card(s), the list of reference files with their role lines, and which
prompts use which references. Later skills (`cinematic-prompt-writer`, `cinema-director-v3`, `animation-handoff-folder`) read it.

## Never

- Never generate keyframes before the style frame and the character reference are approved.
- Never describe a palette with mood words only ("moody, cinematic"); give hex values and owners.
- Never attach a reference without a role line; an unexplained image leaks its background, pose and light into the result.
- Never write the card or role lines in any language but English when the pipeline is shared with other people.
