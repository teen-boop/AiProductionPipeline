---
name: independent-frame-critic
description: >-
  An outside-eyes review loop for a batch of generated stills or video clips. The agent that wrote the prompts stops seeing their
  flaws, so a FRESH reviewer (a subagent, a second session, another model or a person) gets only the references, the frames and one
  intent line per frame, never the prompts or our reasoning. It scores the batch 1-10 on eight fixed categories, names at most five
  fixes ranked by damage, and gives every frame a keep / fix / reject verdict. A batch passes at no category below 6 and a mean of 7
  or more; rounds are logged, capped, and stopped when three rounds in a row fail to beat the best one. Use after mechanical QC
  (frame-qc-contact-sheet) and before frames go into the storyboard, the hand-off folder or a video prompt; when the user says "get a
  second opinion", "critique this batch", "independent review", "fresh eyes", "is this good enough", "why does it still look off";
  or when you have fixed the same batch twice and it still is not landing. Every frame with a locked face also gets the
  identity triple check (same-scale crops, a fresh critic, then in context at delivery size). Includes scripts/critic_log.py
  and scripts/face_compare.py.
user-invocable: true
---

# Independent Frame Critic

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

## Why

`frame-qc-contact-sheet` catches mechanical defects: bars, wrong count, a wrong face in a crop. It does not catch "this whole batch
looks like a first draft", because the agent running it is the same agent that wrote the prompts. After a few rounds it reads its own
intentions into the pictures. A reviewer with no history sees the frames the way the director will.

The loop is simple and it is where quality comes from:
1. look at the result;
2. name the problem precisely;
3. fix it at its source, so a regeneration keeps the fix;
4. check the fix in a view that actually shows it;
5. get an outside opinion before calling it done.

## 1. Build the critic packet

Make one folder per round: `qc/critic/round_<N>/`. Put in it:

| File | What | Rule |
|---|---|---|
| `refs/` | The director's style frames, the identity busts of every character on screen, the location master or the `ROOM_MAP.md` wall references, locked prop sheets | Copies, numbered `ref_1_<role>.png`. Only references that apply to these frames. |
| `frames/` | The frames under review, or 3 stills per clip (first, middle, last) | 6-8 frames per round. More and the reviewer skims. Split a big batch into several rounds. |
| `sheet.jpg` | One contact sheet of the frames (`frame-qc-contact-sheet` / `contact_sheet.py`) | Labelled with the frame IDs the reviewer must use. |
| `INTENT.md` | One line per frame: ID, shot size, what the script beat says happens, time of day | The story intent only. |

Never put in the packet:
- the prompts, the FIX lines or the reasons a frame was made the way it was;
- earlier critic rounds or your own QC notes;
- "this one is the best" or any other hint.

The reviewer must judge the pictures, not our plans for them.

## 1a. Identity triple check (every frame with a known face)

One look is not enough: a face that is "close" passes a tired eye, and a face pasted onto a body passes a quick glance at
thumbnail size. Any frame that shows a locked character (a real person, a recurring cast member) goes through THREE separate
passes before it is used in a storyboard, a hand-off or a video. One "no" in any pass rejects the frame.

1. **Pass 1, same-scale crops.** Run `scripts/face_compare.py --ref <character sheet or approved bust> --out compare.jpg <frames>`.
   It puts every face in the frame next to the reference face at the same size. Compare, feature by feature: face shape and
   weight, eyes (colour, spacing, lids), nose, mouth, moustache or beard (shape and colour), hairline and haircut, scars and
   marks, apparent age. Write one line per frame: `same / not same + the differing features`.
2. **Pass 2, a fresh critic on the crops.** A NEW reviewer (section 2) gets only `compare.jpg` and the reference sheet, no
   prompts, no intent, no pass-1 notes, and answers per face: "Is this the same person as REF? yes / no / unsure, which
   features differ? Does the face look pasted in (lighting, grain, skin texture, edge or scale different from the rest of the
   frame)?". `unsure` counts as no.
3. **Pass 3, in context at delivery size.** Look at the frame exactly as the viewer will see it (the 16:9 frame AND the 9:16
   crop, at the size it plays in the video), with a second fresh reviewer, and ask the same two questions. This catches faces
   that only pass as a crop, and composites that only show at full frame.

Rules:
- A frame labelled APPROVED, "fixed" or "locked" in a promo or tutorial must pass all three passes; a promo that shows a
  drifted face as the good example destroys the claim it makes.
- A frame shown as a REJECT must be visibly wrong at playback size (pass 3). If the reject and the fix look alike, cut the
  pair; it proves nothing.
- A pasted-in or face-swapped look (lighting, grain or skin that does not match the shot) is a reject even when the
  likeness is right. Regenerate the whole shot with the sheet attached; do not patch the face again.
- Record the three verdicts in the round log (`critic_log.py`), with the frame ID.
- When a frame fails on identity, never attach the failed frame (or an older take of the same shot) as the composition
  reference for the regeneration: the model copies the wrong face back from it. Regenerate from the character sheets plus a
  text description of the scene; an already approved frame of the same character may be attached as an extra identity reference.
- A frame that passes pass 1 can still fail pass 2 or 3 (a missing scar, hair colour, a 9:16 crop that loses the face). Fix
  small misses with a minimal edit of the passing frame, then run all three passes again on the edit.

## 2. Run the reviewer in a fresh context

Pick the first route that is available:
1. **A subagent** (for example Claude Code's Agent tool) given only the packet path and the brief below.
2. **A second session or another vision model**, given the same brief and files.
3. **Manual:** hand the folder and the brief to a person, and wait for their JSON or their notes.

Use a NEW reviewer every round. A reviewer that saw round 1 starts defending or chasing its own earlier notes.

Copy-ready reviewer brief (fill the brackets):

```
You are reviewing frames for a film made with image and video generators. The images whose names start with ref_ are the
director's references: the look, the faces, the location, the props. The images in frames/ are the work under review; sheet.jpg
shows them together with their IDs. INTENT.md says what each frame must show.

The references define the WORLD and the LOCKS, not the exact picture. Faces must match the identity references and the look must
match the style frames closely. Framing, staging and the parts of a place the references never showed are the maker's choice and
are not marked down for being different.

The bar: [a frame a director would accept for the storyboard and for animation / a hero still for a poster or a pitch].
Open every frame at FULL size before scoring plausibility; a contact sheet hides wrong limbs and extra fingers. Do not nitpick: nothing an editor would fix in a minute, nothing that is merely a different choice.

Score the batch 1-10 in each category (7 = solid and usable, 9 = exceptional):
- world_fit: the same kind of place, period and world as the references; nothing from another era or city;
- identity: every in-focus face and costume matches its reference; the right number of each character;
- look: grade, contrast, palette, grain and lens character match the style frames; nothing flat, grey or glossy-CG;
- light: motivated light with real sources; not flat, muddy or blown out; consistent across the batch;
- composition: each frame is well composed for its shot size; eye-lines and screen direction make sense;
- plausibility: nothing floating, melted, merged, duplicated or physically impossible; hands and contact read; count every
  person's arms, hands and fingers and trace each limb back to its own body (an arm reaching a table or a product from
  the wrong side, or from nobody, is a reject); every person is placed where their action needs them;
- text_signage: no garbled text, no real brands or logos, no captions or watermarks; any wanted signage reads;
- story_beat: each frame shows what its INTENT line says.

Then list at most FIVE fixes, most damaging first. Only problems that would stop the director from using a frame. Each fix names
the frame ID, the precise problem ("the tabletop lamp has no light pool on the table", not "the lighting is off") and one line that
would fix it. If the batch is good, say so and list fewer or none.

Finally give every frame one verdict: keep, fix or reject, with five words of reason.

Answer ONLY with JSON:
{"scores": {"world_fit": 0, "identity": 0, "look": 0, "light": 0, "composition": 0, "plausibility": 0, "text_signage": 0,
 "story_beat": 0},
 "fixes": [{"frame": "ID", "problem": "...", "fix": "..."}],
 "frames": {"ID": {"verdict": "keep|fix|reject", "why": "..."}},
 "summary": "two sentences"}
```

Save the answer as `qc/critic/round_<N>/critique.json`.

## 3. Log the round and read the verdict

```
python3 scripts/critic_log.py add qc/critic/LOG.json qc/critic/round_<N>/critique.json --label "round <N>: <what changed>"
python3 scripts/critic_log.py status qc/critic/LOG.json
```

`status` prints the scores of every round, the best round, and one decision:
- **PASS:** no category below the floor (default 6) and the mean at or above the bar (default 7). Raise them for hero work with
  `--floor 7 --bar 8`.
- **CONTINUE:** fix and run another round.
- **STALLED:** three rounds in a row did not beat the best total so far. Stop iterating.
- **CAPPED:** the round limit (default 5) is used up.

Use `python3 scripts/critic_log.py check critique.json` first if the reviewer's JSON looks hand-made; it reports missing categories
and out-of-range scores.

## 4. Act on the fixes

1. Take the fixes in the order given. Do not cherry-pick the easy ones.
2. Restate each in your own log as a precise defect + the frame IDs it touches. A fix that touches every frame (a grade, a light
   habit, a recurring prop) goes into the shared style block, the scene state sheet or the room map, not into one prompt.
3. Fix it at the source:
   - the prompt file gets a `FIX:` line (from `generation-failure-fixes` when one exists);
   - a wrong face goes through `identity-fix-pass`;
   - a look problem goes through `style-lock-guard`;
   - a continuity problem goes into `scene-continuity-lock`.
   A fix made only by hand-picking a lucky re-roll is lost on the next regeneration.
4. Regenerate only the frames marked fix or reject. Keep the rejected files as `_rejected_vN_*`.
5. **Check every fix in a view that shows it.** Thumbnails hide most defects:
   - faces: `face_crops.py` next to the identity bust;
   - continuity: `pair_sheet.py` of the previous and next frame;
   - hands, contact, small props, signage: a 100% crop of that region;
   - light: the frame next to the style frame at the same size.
   Do not send the next round until you have seen the fix yourself.
6. Build the next packet from scratch (step 1) and run a new reviewer (step 2).

## 5. Stop rules

- **PASS:** deliver the frames whose last verdict is keep. Frames still marked fix or reject are not delivered, even when the batch
  passes.
- **STALLED or CAPPED:** stop. Deliver the best round's keep frames, and report to the user: the best scores, the fixes that did not
  land and your guess why (the generator cannot do it, a reference contradicts the intent, the bar is too high for this shot).
  Ask what to change: the references, the intent or the bar. More rounds of the same will not help.
- A round that scores lower than the previous one means the last change hurt. Revert that change before trying the next fix.

## 6. Report

Give the user a short table after every round:

| Round | Mean | Lowest category | Decision | Top fix |
|---|---|---|---|---|

Then the per-frame verdicts of the last round. Keep reasons to one line.

## 7. Keep a lessons line

Anything that cost more than ten minutes (a fix that only worked phrased one way, a defect only visible in a crop) gets one line in
the project's `NOTES.md`. If it is a reusable model failure, add it to `generation-failure-fixes` as well. The next session reads
`NOTES.md` first.

## Never

- Never let the agent that wrote the prompts be its own critic for the pass decision. Self-QC is step 0, not this step.
- Never show the reviewer the prompts, earlier critiques or what you hope it says.
- Never reuse a reviewer across rounds.
- Never mark a frame down for differing from a reference in framing or staging when the reference only defines the world. Mark it
  down hard when it breaks a lock: face, costume, look, period, a prop's state.
- Never accept a vague fix ("improve the lighting"). Rewrite it as a named, located defect before acting on it.
- Never keep iterating after STALLED or CAPPED. Report and ask.
- Never deliver a frame you have not looked at yourself, whatever the reviewer said.
- Never send more than 8 frames in one round, and never send frames without their intent lines.
