---
name: visual-story-pipeline
description: End-to-end pipeline for turning a story idea (or an existing script) into a finished narrative AND a consistent, identity-locked, continuity-correct sequence of AI-generated images or video. Covers project setup (working folder, references hierarchy, resolution, aspect ratio, project type), screenwriting via industry-standard structures (Save the Cat / Hero's Journey / Three-Act / Sequence Approach), reference analysis and style-locking, character-sheet-based identity lock, continuity/weather propagation across coverage, test-batch approval gates, multi-platform generation (Lovart/Krea), and QC. Style-agnostic. Use whenever a user wants a creative+production partner for going from a story idea or script to a produced sequence of AI-generated images/video with consistent, real-photo-locked characters — not just an image-prompt generator.
---

# Visual story production pipeline

Turns an idea (or existing script) into a finished story, then into a style-consistent,
identity-locked, continuity-correct sequence of AI-generated images or video. Nothing here depends
on one specific visual style — swap in whatever look the project needs and the pipeline still
applies.

Detailed material lives in `references/` and `assets/` — this file is the operating checklist. Load
the referenced file when you reach that phase; don't try to hold every detail in this one document.

## 0. Project setup — ALWAYS ask this first, before anything else

Ask the user, in one pass, before touching references, script, or a single generation:

1. **Working folder.** Where does this project live? Create/confirm it before anything else. Inside
   it, build a references hierarchy per `references/02-reference-taxonomy.md` — don't dump files
   loose in the project root.
2. **Resolution.** 2K or 4K.
3. **Aspect ratio.** 16:9, 9:16, 1:1, 4:3, or other — an explicit answer, never inferred from the
   references. Lock this in before the first test generation, not after — redoing a completed batch
   for the wrong aspect ratio is expensive rework, not a hypothetical.
4. **Project type.** Series/TV, film, commercial/ad, music video, or other — determines how much of
   the pipeline repeats per episode. See the decision tree in §6.

## 1. Pipeline phases, in order

1. **References** — study and lock the project's visual style before writing a single prompt. See
   `references/02-reference-taxonomy.md`.
2. **Script** — from idea or existing draft, to a finished story. See
   `references/03-script-structures.md`.
3. **Prompt engineering setup** — extract the STYLE LOCK block, build character sheets, establish
   masters. See `references/04-prompt-engineering.md` and `assets/character-sheet-*.md`.
4. **Location and prop references, per scene, as the script locks.** For each scene, once its script
   is final: generate one medium character shot that also clearly shows the location behind them
   (this doubles as that location's canonical reference), and a dedicated reference image for any
   other recurring subject or prop the scene introduces. See
   `references/09-location-and-prop-references.md` — mandatory, not optional, for any project with
   more than a couple of locations/recurring props.
   **4a. Room map (mandatory for every interior).** Run `location-room-map`: from the location
   photo build the full room (floor plan, all 4 walls, windows on ≤2 adjacent walls, at least one
   door, one of each recurring object), and generate each wall as its own reference. Reverse/OTS
   shots attach the wall that is actually behind the subject.
   **4b. Scene continuity lock (mandatory for every multi-shot scene).** Run `scene-continuity-lock`:
   scene state sheet (seat map, props and their states, light, camera axis), check each prompt
   against the previous AND next prompt, paste the CONTINUITY block into every prompt, QC each frame
   against it.
5. **Test batch → approval gate** — max 7–8 images sampling across the script, explicit user
   approval, before full production. Can request additional references here.
6. **Full production** — every mini-scene, using the locked style/characters/masters/locations/props
   from steps 3–4.
7. **QC** — before delivery, every time. See `references/08-qc-and-fixes.md`.

Don't skip or reorder these. A prompt written before the STYLE LOCK block exists, a scene shot before
its location/prop references exist, or a full batch run before the test batch is approved, is the
failure mode this pipeline exists to prevent.

## 2. Core non-negotiable rules

These are the rules that have caused real rework when skipped. Full detail and templates are in the
linked reference file; this is the checklist form.

- **Atmosphere always carries over from a reference, even when the subject doesn't.** Photographic
  mode, light source/behavior, depth of field, and atmospheric quality (haze/grain/etc.) transfer
  from any reference to any new prompt, regardless of what character/scene/story-beat is different.
  → `references/04-prompt-engineering.md`
- **STYLE LOCK block, copied verbatim into every prompt.** Built once per project from the style
  references and the first approved masters. Never re-derive the look from memory per-prompt.
  → `references/04-prompt-engineering.md`
- **Master shot + continuity/weather propagation.** The first approved wide/establishing/two-shot of
  a location is the master; every later shot in that scene attaches it. Weather and physical state
  (wet, dirty, disheveled) shown in the master must show up on any character entering that scene
  after it — never generate a "clean, dry" character walking straight out of established rain.
  → `references/04-prompt-engineering.md`
- **Locations and recurring props get their own locked reference images, generated before they're
  reused across scenes** — same discipline as character references, not a lighter version of it. A
  scene's first character shot doing double duty as that location's reference, plus a standalone
  reference for any recurring object, both attach to every later generation that reuses them.
  → `references/09-location-and-prop-references.md`
- **Face reference + approved portrait, always, no exceptions.** Real face photo AND the locked
  approved portrait attach to every generation featuring that character, in that order, alongside
  the character sheet when one exists. One face photo per person in a multi-character frame.
  → `references/05-character-lock.md`, `assets/character-sheet-*.md`
- **Character rework = persona AND narrative function, together, in the same pass.** A new look
  without a new reason for that character to be in the scene isn't a finished rework.
  → `references/05-character-lock.md`
- **Character identity change ⇒ forget prior generations of that character.** Don't patch continuity
  onto a discarded identity — regenerate clean against the new reference. (Distinct from a *minor*
  correction, which patches the existing shot in place — see `references/08-qc-and-fixes.md`.)
- **Test batch is a mandatory gate**, not a formality — get explicit approval before spending on full
  production.
- **QC every delivered image before calling it done** — not just the composition, every panel/region.
  → `references/08-qc-and-fixes.md`

## 3. Continuity & weather propagation — quick reference

(Full mechanics, prompt skeleton, and worked example in `references/04-prompt-engineering.md`.)

- Establish a **master** shot per location/scene; every subsequent shot in that scene attaches it as
  a reference, not just a text re-description.
- If the master shows rain/snow/fog/mud, every character who has just entered that space needs
  visible physical evidence of it (wet hair, damp fabric, droplets, mud on boots) — stated explicitly
  in the prompt, not left to the model to infer.
- Every locked visual detail (a specific stain, a torn sleeve, a prop, a hairstyle state) is copied
  **verbatim** across every prompt in the same mini-scene, never re-described from memory.
- Coverage for dialogue/animation: master two-shot first, then per-character close-ups via
  `Change to...` from that master, restating locked details each time even with the master attached.

## 4. Character sheets — identity lock at scale

Templates in `assets/`, escalating by how much coverage a character will get:

| Template | File | Use for |
|---|---|---|
| **Animation prototype map** | `assets/character-sheet-prototype.md` | **Default for anything animated or recurring.** Four close-up head angles (front / three-quarter / profile / back) in a 2x2 grid on the left, one headless full-length view on the right, nothing in the hands |
| Basic 4-view turnaround | `assets/character-sheet-basic.md` | Minor/secondary characters |
| Full production sheet | `assets/character-sheet-full.md` | Leads and recurring characters |
| State/weather variant | `assets/character-sheet-state.md` | A locked state (wet, injured, dirty, costume change) needed across multiple scenes |
| Location 4-angle turnaround | `assets/location-sheet-basic.md` | Any location reused across more than one scene — mandatory alongside the scene's character-in-location shot, see `references/09-location-and-prop-references.md` |
| Prop 4-view turnaround | `assets/prop-sheet-basic.md` | Any recurring prop/object extracted from a scene's prompt — same four-part template shape as the character sheet, see `references/09-location-and-prop-references.md` |

Generate the relevant sheet(s) before heavy multi-angle coverage of a character. Attach sheet + real
face photo + approved portrait together, in that order, for every subsequent generation of that
character. See `references/05-character-lock.md` for the full attachment-order rule.

## 5. Test batch → full production

Draft prompts for a small sampling of mini-scenes across different parts of the script (max 7–8
images) — not the whole story. Additional references can be requested here if something the script
needs isn't covered by what's on hand. Generate, then get **explicit** user approval — style, color,
identity-lock fidelity, aspect ratio, everything — before writing the full prompt set and moving to
full production.

## 6. Decision tree — how much of this repeats

| Situation | What to do |
|---|---|
| Brand-new project | Full §0 → §1 pipeline, start to finish |
| New episode, same project (series/season) | Skip §0's questionnaire and the script-structure choice if already established; go straight to that episode's script + production. Never compress the established STYLE LOCK block or master references — reuse them exactly. |
| Character rework (new look/persona) | Full §2 character-rework rule (persona + narrative function together) + a dedicated small test batch of the new scene action, approved before full coverage |
| Minor identity correction (wrong photo, small costume fix) | Patch technique in `references/08-qc-and-fixes.md` — don't regenerate the whole project |
| Full identity change/swap | Forget prior generations of that character per §2 — clean-slate regeneration, no continuity patching |

## 7. Budget / platform discipline

- **Before the first generation on any platform, ask the user, explicitly, in one pass:**
  1. **Which model** to generate with (if the platform offers a choice).
  2. **Which mode** — free/unlimited (queued, no credit spend) or paid/fast (costs credits, no
     queue) — never assume, never default silently to whichever the account happens to be in.
  3. **What it will cost**, to the extent the platform exposes that — a per-generation credit cost,
     a rate, or an explicit "I can't determine exact cost from here, check your platform dashboard"
     if the CLI/API genuinely doesn't expose it. Don't guess a number; say plainly when cost isn't
     knowable from where you're standing.
  Re-ask/re-verify mode after any credential change mid-project — see the note in
  `references/07-platforms.md`, mode does not carry over across a key rotation.
- Ask before spending paid credits, unless the user has already said "use your judgment" for this
  project.
- Stick to the platform(s) the user specified; make that path succeed rather than silently switching.
- Platform-specific mechanics (Lovart, Krea — auth, concurrency limits, aspect-ratio handling,
  upload/attach flow) are in `references/07-platforms.md`. Read it before the first submission on a
  platform you haven't used yet this project.

## 8. Output file organization

Default (projects without the location/prop-reference workflow): one folder per full generation
pass, plain filenames inside: `output/V1/<shot-name>.png`, `output/V2/<shot-name>.png`, ... Never
invent ad-hoc batch-name folders (`test_batch_01`, `round3`), never mix two versions' files in one
folder, never overwrite a prior version.

**Scene-scoped scheme (use this once the project has location/prop references, per §1 step 4):**
```
Scene_<NN>_v<version>/
  Tests_v<version>/          -- exploratory/rough attempts, not yet approved
  Working_frames_v<version>/ -- approved shots actually used in the cut
```
Version the whole scene folder when a scene gets reworked; keep tests separate from approved working
frames. See `references/09-location-and-prop-references.md` for the matching reference-folder
structure (`01_References/Locations/`, `01_References/Props/`).

Whichever scheme is active, `ls` sorted shows the version history directly — that's the invariant,
not the specific folder names.

## 9. When something is unclear

Ask the user, especially early in a new project before its specific pattern is established. Study
every task-scoped reference folder in full before writing prompts against it — don't rely on a
style-label shortcut.
