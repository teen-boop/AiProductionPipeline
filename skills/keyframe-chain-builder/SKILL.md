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

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

A chain is 2–4 stills of ONE continuous shot. Video models interpolate between a start and an end frame, so the stills must be the same
world at different moments. If they differ in anything you did not ask for — a second car, a mirrored building, a new face, a new grade —
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
   - A hot pan is handed over by its handle, never thrown at a person.
   - Nobody stands in the path of a moving vehicle.
   - Poured liquid falls straight down and settles level.
   - When the power is cut the lamps go dark and the fan stops turning.
   - Ask yourself: "would a stunt coordinator allow this?"
2. **Time moves forward.** If minutes or hours pass between keyframes:
   - People have moved, turned, left or been replaced. **Never the same person in the same pose** across a time-lapse.
   - Small details progress too: parked cars, shop shutters, lamps (off → lit), shadows, cups on a table, birds.
3. **Same camera side, same orientation.**
   - The subject keeps its facing (a car nose pointing left stays pointing left), the pavement stays on the same side, and the horizon keeps its height.
   - A camera move is allowed only if it is stated ("dollies forward along the same pavement toward the car").
4. **One of each hero.** Only one car, one bride, one raven. Shots from inside the car must not show the vehicle the camera sits in as a second
   car (see `generation-failure-fixes`).

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

## 7. Continuous movement across many shots (dance, fight, sport)

When limbs teleport, feet slide or motion resets at every cut, build the sequence from a light storyboard and a pose chain.
Full method in [references/storyboard-to-motion.md](references/storyboard-to-motion.md). The short version:

- **Script first:** a timecoded shot list where every shot names its ENTRY and EXIT pose, and shot N's exit is shot N+1's entry.
  Write the action as physics (approach, contact, transfer of force, recovery, cloth settling a beat late), never as adjectives.
- **Pick the lane:** one scripted Seedance run when the sequence fits the model's duration cap (plates + board + 2 or 3 photoreal
  key frames as references); chained per-shot runs (start frame = boundary still N-1, end frame = boundary still N) past the cap,
  when the sequence must open on an exact pose, or when someone leaves frame and returns.
- **Draw the board LIGHT:** thin pale pencil on bare paper. A heavily drawn or photoreal board leaks its arrows and numbers into
  the video as objects. In the prompt, DEFINE the marks as the director's planning guides instead of prohibiting them.
- **Gate every panel twice** (artifacts, then spot-the-difference against the plate: counts, part-to-whole, costume, screen
  side). A board-level pass averages defects away.
- **Check the delivery every 0.5 s**, not only at the cuts: a leaked marking can fade in mid-shot.
