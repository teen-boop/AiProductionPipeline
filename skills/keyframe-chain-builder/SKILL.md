---
name: keyframe-chain-builder
description: >-
  Builds KEYFRAME CHAINS (K1 → K2 → K3) for micro-stories and transitions that a video model (Kling, Seedance, Veo) plays as first + last
  frame pairs. Each next keyframe is generated FROM the previous one ("change to"), so place, people, light and lens stay identical while
  the moment moves forward. Enforces physical realism, forward-moving time (nobody frozen in the same pose), a locked camera side and
  subject orientation, and the full cinematic style + grade reference on EVERY keyframe — not only the first. Use when the user asks for
  keyframes, micro-stories, "change to" frames, start/end frames, time-of-day transitions (sunset → night, day → overcast), reveal shots,
  or any sequence that will be animated as first + last frame pairs.
user-invocable: true
---

# Keyframe Chain Builder

A chain is 2–4 stills of ONE continuous shot. Video models interpolate between a start and an end frame, so the stills must be the same
world at different moments. If they differ in anything you did not ask for — a second ship, a flipped hull, a new face, a new grade —
the clip morphs instead of moving.

## 1. Design the micro-story on paper first

For each chain, write a single line per keyframe and the motion between them:

```
K1  what we see at the start (camera position, subject, light)
 ↓  motion 1→2  (what physically happens, in seconds)
K2  the same world a moment / an hour later
 ↓  motion 2→3
K3  the payoff
```

Then check each step against the four laws below **before** generating anything.

## 2. The four laws

1. **Physically possible.** Every action must be something real people and objects do safely and plausibly:
   - Hot metal is passed tongs-to-tongs, never thrown at a person.
   - Nobody stands in front of a moving vehicle or hull.
   - Water rises from the low end and finds its level.
   - Lights go out on a dead ship and its funnels stop smoking.
   - Ask yourself: "would a stunt coordinator allow this?"
2. **Time moves forward.** If minutes or hours pass between keyframes:
   - People have moved, turned, left or been replaced. **Never the same person in the same pose** across a time-lapse.
   - Small details progress too: carts, ropes, lamps (lit → put out), smoke, water level, birds.
3. **Same camera side, same orientation.**
   - The subject keeps its facing (a bow on the left stays on the left), the quay stays on the same side, and the horizon keeps its height.
   - A camera move is allowed only if it is stated ("dollies forward along the same quay toward the bow").
4. **One of each hero.** Only one ship, one bride, one raven. On-board shots must not show the vessel the camera stands on as a second
   ship (see `generation-failure-fixes`).

## 3. Generate in waves

- **Wave 1:** all K1 frames, generated in parallel from the normal references and the colour-grade frame.
- **Wave 2:** every K2, made from its *delivered* K1. **Wave 3:** every K3, made from its delivered K2.
- Never pack K(n+1) before K(n) has passed QC. If you redo K(n), stop or discard the K(n+1) that was built on the old version.
- Always build on the **newest delivered version** of the previous keyframe. A redo is delivered as `…_2.png`, `…_3.png`.
  Resolve the newest version by its highest number, never by the hard-coded `…_1.png`.

## 4. Prompt for K2 / K3 (change-to)

Attach the images in this order:
1. The START frame (the previous keyframe).
2. The project's colour-grade frame, always **last**.

Then write:
```
Change to: <what is different now — time, light, positions, details>.
SAME WORLD: keep exactly the same place, people, clothes, light direction, colour grade, film grain and lens look; only what is described changes.
TIME MOVES FORWARD: nobody stays frozen in the same pose; people have moved, turned, left; details have progressed.
<historical / physical accuracy lines>
<the full LOOK + OPTICS + GRADE blocks of the project>   ← the same as K1, never a shortened version
```

A change-to prompt that carries only the start frame and no grade/optics blocks drifts into a glossy "commercial" look: saturated gold
sunrises, everything in focus. That is the most common failure of chains.

## 5. Video prompts

- For each pair, write ONE continuous-shot prompt with what happens between the two frames, timed (`0–5 s: …`), plus a colour lock.
- Label each still so the editor knows the pairing:
  - `KLING: Start = this picture, End = the NEXT picture`;
  - `last keyframe — start frame only` on the final still.

## 6. QC the chain as a sequence

Put K1 | K2 | K3 side by side (see `frame-qc-contact-sheet`, `pair_sheet.py`) and check:
- [ ] the same place and lens, and the subject's orientation unchanged unless the move is stated;
- [ ] each step is physically plausible (law 1);
- [ ] time has visibly moved forward and nobody is frozen (law 2);
- [ ] every keyframe has the series grade and shallow-DOF look, with no colour jump between K1 and K2;
- [ ] no duplicated hero, no new text, no letterbox bars.

Reject the single failing keyframe with a one-line prompt fix, regenerate it, and re-check its neighbours.
