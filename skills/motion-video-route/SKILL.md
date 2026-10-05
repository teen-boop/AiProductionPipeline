---
name: motion-video-route
description: The VIDEO route for motion graphics — producing animated collage/explainer clips with video models (Gemini Omni Flash first, Seedance as fallback) from a locked master style sheet. Covers the safe route (style ref → image → video) versus the fast route (style ref + prompt → video), the image-prompt and video-prompt templates, the mandatory style restatement inside video prompts, the big-blocks rule of thumb, the known-faces workaround, and model routing. Use when a shot wants dynamic camera, collage depth, parallax or paper-diorama motion rather than exact numbers. Triggers on omni flash, image to video, reference to video, style sheet to video, collage clip, camera move clip, seedance vs omni, video prompt, alert wash, paper diorama.
---

# Motion Video Route

Companion to `motion-style-core` (produces the master style sheet) and `motion-graphics-director` (routes and owns the prompt library).

## Which sub-route

| | SAFE ROUTE | FAST ROUTE |
|---|---|---|
| Flow | style ref → **image** → video | style ref + prompt → video |
| For | complex scenes, text, people, **logos, faces** | simple scenes, big shapes |
| Rule | `COMPLEX = LOCK THE FRAME` | `SIMPLE = SKIP THE FRAME` |

When a shot carries a logo or a recognizable person, always take the safe route. Generate and approve the still first; a bad frame becomes a bad clip at four times the cost.

## Rule of thumb — what these models can and cannot do

✅ big blocks · logos · chunky headline type
❌ fine type · micro-detail · dense small labels

`LESS MOTION = SAFER.` Long clip → simple movement. Wild dynamics are fine only in short cuts where you will use just a fragment. **One committed cinematic move per clip** — the camera is an actor, not a spectator.

Anything with real numbers, axes or counting values belongs in the CODE route. Do not fight this.

## Image prompt template

```
Use the attached style sheet for MATERIALS ONLY — <textures, cutout treatment,
type, grain>. Do NOT copy the sheet's layout or its flatness: every clip is a deep
3D paper diorama — cutouts are physical layers separated in real space, strong
shallow depth of field, foreground elements crossing close to the lens. The camera
is an actor: it flies between layers, orbits, dives, whips, racks focus — one
committed cinematic move per clip. Backgrounds change per clip, always within the
sheet's palette. ALERT WASH means the entire frame floods to the hot accent tone in
one beat. Motion: springs with overshoot, staggered entrances, ticking counters.

SHOT:
Background: <...>. FG: <...>. <camera move>. Settle at <...>.

AUDIO: <sound design only — paper pops, whooshes, stamps, ticks>. No music. No narration.

AVOID: no flat single-plane composition, no static locked-off camera, no glossy
plastic CG, no full-colour midground portraits, no warped or gibberish text, no
invented logos, no watermarks, no music, no voice-over, no narration, no lyrics.
```

**"MATERIALS ONLY, not layout"** is mandatory. Without it the model reproduces the style sheet's grid instead of its language.

## Video prompt template (~600 characters, four slots)

```
STYLE: <restate the locked look in one dense sentence — surface, cutout treatment,
palette with the one accent, type, grain, never glossy CG>. Match the look of the
attached frame exactly and keep it consistent through the whole shot.

ACTION: <what moves, staggered, in order>. One continuous move, no cuts. End <...>.

AUDIO: <sound design only>. No music, no narration.

AVOID: no camera cuts, no new text, no warped letters, no music, no voice-over.
```

**Restating STYLE is not optional even when the frame is attached.** Dropping the style block makes the model transform the look mid-clip. This is the single most common failure on this route.

## Locking style, swapping action

The prompt has a frozen half and a moving half:

| Frozen | Moving |
|---|---|
| STYLE · AUDIO · AVOID | SHOT / ACTION |

Across a series, change only the SHOT block. Change the background deliberately, when you want variety — not by accident.

## Known faces

Video models block recognizable people. Workaround that also improved the look:
1. Generate the still in an image model that allows it.
2. Image-to-image pass to lay **black bars over the eyes**.
3. Feed that frame to the video model.

## Model routing

| Model | Use for | Watch out |
|---|---|---|
| **Omni Flash** | default — best reference understanding, best typography, best physics, cheapest of the top tier | resolution is modest; details and motion can be soft |
| **Seedance 2.0/2.5** | cinematic stills and photoreal shots | mangles numbers and faces in motion-graphics contexts |
| Kling 3.0 | — | no reference mode, start-frame only; unusable for this system |

For a Seedance shot, hand off to `seedance-prompt-writer` / `cinema-director-v3` rather than using the templates above.

## QC pass before accepting a clip

1. Did the style hold end to end, or drift after ~2 seconds?
2. Is every visible word one of the approved samples — no invented text?
3. Are people still halftone black-and-white, not full colour?
4. Any warped letterforms at small sizes? If yes, that element belongs in the CODE route.
5. Exactly one camera move, or did it cut?
6. One hero accent, or did red leak into ordinary fills?
