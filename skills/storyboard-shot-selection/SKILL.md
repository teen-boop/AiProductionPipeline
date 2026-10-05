---
name: storyboard-shot-selection
description: Determines, for every beat in a script, WHY a specific shot size/type (establishing, wide, full, cowboy, medium, medium close-up, close-up, extreme close-up, group shot, over-the-shoulder, POV, dutch angle) is the correct cinematographic choice for that beat, and writes that reason directly into the storyboard shot description. Prevents two adjacent shots in a sequence from sharing the same underlying purpose or framing without narrative justification. Use when building a storyboard/raskadrovka shot list, choosing which plan/shot type fits a beat, or reviewing a shot list for redundant back-to-back framings. Triggers on shot size, plan type, which shot to use, storyboard shot list, why this shot, redundant shots back to back, raskadrovka.
---

# Storyboard Shot Selection (Shot-Size Rationale)

## Why this exists

Choosing a shot size is not a style flourish — every shot size exists to serve one specific narrative job. A storyboard built by cycling through shot types for variety, rather than deriving each one from what the beat actually needs, produces sequences where two adjacent panels do the same job (or worse, where the wrong shot type is used for the job — an establishing shot used for a reaction, or a close-up used to show a location). This skill makes the reason for each shot explicit and checkable, instead of implicit and assumed.

## When this runs

At the storyboard-building stage of `loveart-video-animation`, on the drafted text shot list — same stage as `storyboard-continuity-tracker`, and typically run together with it, before any image is generated. `storyboard-shot-selection` governs *why this shot type, here*; `storyboard-continuity-tracker` governs *does this shot's state follow from the last one*. `storyboard-reference-assembly` runs later, at generation time, to attach the right assets.

## Shot taxonomy and the narrative job each one does

Use a shot type only for the job it is defined for below. Do not pick a shot type for visual variety alone — if you can't state which job it's doing, it's the wrong choice for that beat.

- **Establishing shot** — orients the viewer: where are we (city, building, room)? Use only as the first shot of a scene/location, or when the location itself changes. **Never use it for performance or reaction** — it carries no emotional or gestural information and shouldn't be asked to. Can be a drone shot, static tripod shot, or a moving/steadicam shot that still functions as orientation.
- **Wide shot** — shows the character existing *in* the space, not just the space itself. Job: establish the character's relationship to their environment (e.g. entering a room, being small/alone in a location).
- **Full shot** — tighter than wide; character visible head-to-toe (occasionally trimmed slightly at the top for headroom). Job: read gesture and body language while still showing the character connected to their surroundings — the first shot size where "what is the character *doing* with their body" becomes legible.
- **Cowboy shot** — tighter than full, roughly mid-thigh up. Job: an action is being performed AND its performance/gesture needs to read clearly (e.g. sitting down, placing an object on a table) — action plus visible physicality at the same time.
- **Medium shot** — waist up. The default workhorse. Job: read both emotion (face is clear) and physical contact with other objects/characters/subjects in the scene at the same time (e.g. character interacting with a pet, an object). Use this as the default when a beat needs "emotion + contact with something," not a specialized job below.
- **Medium close-up / close-up** — close-up is chin to crown, typically longer lens. Job: emotion, specifically — a beat where the character feels something worth emphasizing (upset, saying something serious, a strong reaction). Use close-up when the beat's whole point IS the emotion, not as a generic "let's get closer" choice.
- **Extreme close-up** — an isolated detail. Job: put a hard accent on one specific, narratively important detail — text of a letter, a ring on a hand, a tear falling from an eye. Use only when there is a single concrete detail the story needs the viewer to specifically notice, not for general intensity.
- **Group shot** — width similar to a medium or cowboy shot, sometimes wider. Job: multiple characters in frame, showing them interacting with the world and with each other.
- **Over-the-shoulder (OTS)** — job: usually dialogue between two characters; also usable to show "the rest of the scene" from behind/beside a character while they do something (e.g. reading a screen), letting the viewer see both the character's presence and what they're looking at in one frame.
- **POV** — the camera becomes a character's own eyes; job: put the viewer directly in the character's perceptual position for something specifically worth seeing as they see it.
- **Dutch/low/high angle** — angle, not size; used for a deliberate psychological/spatial effect (imbalance, power, scale) layered on top of whatever size is otherwise chosen for the beat.

## User-Dictated Shot Lists (Authoritative)

Often the user dictates the exact shot breakdown directly, scene by scene, in a terse
format like: "1. Medium shot — takes the ramen off the shelf, cat drinking milk in the
background. Close-up — pours water in. Medium shot — takes the matcha and leaves, cat
darts out ahead of her." When this happens:

- The user's stated shot sizes, order, and action-per-shot are **authoritative** — do not
  override them with independently-derived shot-selection choices from the taxonomy below.
- This skill's job shifts from *choosing* shot types to *recording the rationale* for the
  ones given (so the "why" is still documented per shot) and *flagging* problems: two
  adjacent user-given shots that would look identical in framing, a shot whose stated size
  doesn't match what the taxonomy says that job needs (flag it, don't silently fix it -
  ask), or a continuity gap between what one shot ends on and the next starts on.
- Write up the dictated list in the same structured format as an auto-derived one (shot
  type, reason, timing) immediately after the user gives it, and update the relevant
  seedance/storyboard file(s) right away - don't wait to batch several scenes' dictation
  before writing anything down.
- Work through the episode in the order the user dictates it (typically scene by scene,
  shot by shot) rather than jumping ahead to scenes not yet covered.

## Process

1. **Read the scene/beat list.** For every beat, identify what the beat actually needs, in plain terms: orientation, gesture/action, emotion, contact with an object/subject, a specific detail accent, a relationship between multiple characters, or a dialogue exchange.

2. **Map that need to the one shot type whose defined job matches it**, using the taxonomy above. If a beat seems to need two things at once (e.g. both orientation and gesture), pick the size whose job description most centrally covers it, and consider whether the beat is really two beats.

3. **Write the reason inline, next to the shot type, in the shot description** — not as a separate detached note, but attached to the shot itself, e.g.:
   ```
   Shot 3 — Cowboy shot (reason: she sits down and places the matcha on the table —
   action + visible gesture, not yet close enough for pure emotion)
   ```
   This makes the justification checkable later, by the user or by a follow-up pass, without having to re-derive it from scratch.

4. **Check adjacency across the whole shot list.** No two consecutive shots should serve the same job/reason with a similar framing, unless the script genuinely repeats that job back-to-back for a deliberate reason (rare — usually a sign two shots should be merged, one removed, or one's job changed). If shot N and shot N+1 are both "medium shot, reason: emotion" with nothing distinguishing why both are needed, that's a redundancy to fix before generation, not a stylistic choice to preserve.

5. **Flag any beat that doesn't cleanly map to a defined job.** Don't force a shot type onto a beat that doesn't need one of the jobs above — ask whether the beat needs a shot at all, or whether it's better folded into an adjacent shot's description.

6. **A correct label is not enough — verify the generated result actually looks different.** Two adjacent shot types that are visually close in framing (most commonly medium shot vs. cowboy shot, or full shot vs. wide shot) can come back from generation at nearly the same crop and camera distance even when their assigned jobs/reasons are genuinely different — the label was right, but the model didn't render enough of a visual gap between them. When writing the generation prompt for shots like this, don't rely on the shot-type name alone to produce differentiation: explicitly specify a distinguishing camera angle (e.g. 3/4 side angle vs. frontal, slightly lower/higher) or an explicit crop-tightness delta ("noticeably closer than the previous panel, cropping in tighter on the hands") so the two panels are unmistakably distinct frames, not just differently-labeled versions of the same one. After generation, check adjacent panels against each other visually, not just against their text descriptions — if two panels could be swapped without anyone noticing, that's the same failure as a redundant shot, just caught one step later.

## Output

Each shot in the finalized list carries its shot type AND its one-line reason, e.g.:

```
1. Establishing shot (reason: orient the viewer — this is the character's apartment, first shot of the scene)
2. Wide shot (reason: she enters and exists in the room, holding matcha — space + presence, not yet gesture)
3. Cowboy shot (reason: sits down, places matcha on table — action + visible gesture)
4. Medium shot (reason: reaches toward the cat on the desk — emotion + contact with a subject)
5. Close-up (reason: her reaction to the cat's stubbornness — the beat's whole point is the emotion)
6. Extreme close-up (reason: the email text on the laptop screen — a single specific detail the story needs noticed)
```

If two adjacent entries would read the same with the reason stripped out, that is the signal to revise before any image gets generated.
