---
name: script-extractor
description: >-
  Parses source material — a formatted screenplay (sluglines, character
  cues, action lines) OR any free narrative text (a short story, a novel
  excerpt, a literary adaptation, prose fiction with dialogue) — scene by
  scene (or scene-equivalent unit, for prose with no formal scene markers),
  and extracts five categories of detail per unit: locations (INT/EXT,
  day/night, inferring the time-of-day when it isn't explicitly stated),
  characters present, props, key physical actions, and wardrobe/appearance
  details. Every extracted detail stays explicitly tied to the specific
  scene and circumstance it came from — never flattened into a
  project-wide list disconnected from context — and the output doubles as
  a cross-reference index so the same recurring character/prop/wardrobe
  fact (established once) can be reused correctly in every later scene.
  This is the step that turns raw source material into the input
  `character-identity-lock-setup`, `storyboard-reference-assembly`, and
  the prompt-writing skills need — and those downstream skills should
  treat this skill's per-scene entries and cross-reference index as the
  authoritative source for a shot's day/night, wardrobe, and location
  facts, not re-derive them independently. Use whenever the user hands
  over an actual screenplay OR any other narrative text/story (PDF or
  plain text) and wants it broken down for production/reference planning.
  Triggers on extract the script, extract this story, break down this
  screenplay, break down this text, script extraction, scene breakdown
  by category, parse this script, parse this story, script to categories,
  extract details from this narrative.
---

# Script Extractor

## Why this exists

A formatted screenplay already contains almost everything a production
needs — locations, characters, props, actions, wardrobe — but it's
embedded in prose and dialogue, scattered across scenes, and often
implicit (a slugline with no time-of-day, a character introduced by a
generic V.O. cue and only named two lines later, a wardrobe detail stated
once that silently applies to every later appearance of that character).
Read as a flat script, none of that is directly usable as production
input. This skill is the extraction pass that turns it into structured,
per-scene, cross-referenced data — the actual prerequisite for locking
character references or writing a single generation prompt.

The non-negotiable design constraint, stated by the user who commissioned
this skill: **every extracted detail must stay linked to the specific
scene and circumstance it occurred in.** A prop, an action, a wardrobe
note extracted without its scene context is much less useful than the
same fact tied to "this happens in scene 9, at night, on the roof, while
Trinity is being chased" — the scene context is what a later prompt
actually needs.

## Where this sits relative to other skills

This is the **true first step**, upstream of everything else in this
skill family, for **any narrative source material** — a formatted
screenplay (sluglines, ALL-CAPS character cues, action lines) or free
narrative prose (a short story, a novel excerpt, a literary adaptation,
prose fiction told through narration and quoted dialogue). Both are
in scope; see "Working from free narrative prose" below for how
segmentation and character resolution differ for that case.

This is still distinct from `storyboard-narrative-breakdown`, which takes
a specific kind of prose: continuous camera-direction narrative
explicitly describing a shot-by-shot visual sequence ("camera flies
toward the poster, then we see the window, then..."). That kind of text
is already halfway to a shot list — it has no scenes or characters to
extract, only a camera path. A short story or novel excerpt is the
opposite: it has scenes, characters, dialogue, and physical detail, but
no camera direction at all. If the input describes what the camera does,
use `storyboard-narrative-breakdown`. If the input is a screenplay or a
story/narrative with characters and events, use this skill instead — a
narrative breakdown skill would have nothing to segment by (no camera
cues to find), and this skill would have nothing to extract from pure
camera-direction prose (no characters, props, or wardrobe to speak of).

Downstream of this skill:
- `character-identity-lock-setup` — uses this skill's character list (with
  their established wardrobe/appearance notes) to know which characters
  need a locked reference set and what their default look is.
- `storyboard-reference-assembly` — uses this skill's per-scene location/
  prop/character lists to know what needs to be attached to each shot.
- `storyboard-shot-selection` / `storyboard-continuity-tracker` — operate
  on the shot list a narrative/prompt-writing skill builds from this
  skill's scene breakdown.
- The project's prompt-writing skill (`cinematic-prompt-writer` or
  equivalent) — turns individual scene entries into actual generation
  prompts, once this skill has surfaced what belongs in each one.

## The five extraction categories

For every scene, pull out:

1. **Location** — the slugline's location name, INT or EXT, and DAY or
   NIGHT. See "Resolving missing day/night" below — this is the one
   category that routinely needs inference, not just reading.
2. **Characters** — everyone present or speaking in the scene, by their
   resolved real identity (see "Resolving V.O./generic cues" below), not
   just the cue-line label if that label is a placeholder.
3. **Props** — physical objects the scene calls out specifically, not
   generic set dressing. A prop belongs in the list if the scene singles
   it out by name and it does or could recur, gets handled/interacted
   with, or matters to the story (a gun, a specific vehicle, a telephone
   booth) — not "a table" mentioned once in passing with no further
   significance.
4. **Actions** — the scene's key physical actions/beats, each attributed
   to whoever performs it. Prioritize actions that would need to be shown
   visually (a fight move, a chase beat, a specific gesture) over
   incidental blocking ("she stands up") unless the incidental blocking is
   itself the point of a shot.
5. **Wardrobe/appearance** — any costume, appearance, or physical-detail
   note the scene states, whether it's a one-time description ("a woman
   in black leather") or an explicit standing rule for a recurring
   character/group ("they wear dark suits and sunglasses even at night").

## Resolving missing day/night

A screenplay's sluglines don't always restate the time of day on every
scene — once established, later scenes in the same continuous
stretch of action often drop it. **Infer the missing time-of-day from
the nearest preceding scene that stated one explicitly, and carry it
forward through every subsequent scene UNLESS the text itself narrates a
time skip** (a line like "the next morning," a scene explicitly slugged
with the other time-of-day, a clear gap in the action). Mark every
inferred (not explicitly stated) day/night value as **[inferred]** in the
output so it's checkable and distinguishable from what the script actually
says — don't silently present an inference as if it were stated.

## Resolving V.O./offscreen/generic cues to real identities

A character is sometimes first introduced by a functional cue label
(`MAN (V.O.)`, `WOMAN (V.O.)`, `VOICE`) and only identified by name a few
lines later, in an action line or by another character addressing them.
Read forward before finalizing the character list for a scene — if a
generic cue is resolved to a named identity anywhere in that scene or the
immediately following context, use the real name in the extraction (and
note the resolution, e.g. "`MAN (V.O.)` → Cypher, named in the action line
below"). Keep genuinely generic, unnamed role characters (a nameless COP,
a LIEUTENANT with no other name given) as their role label — don't invent
a name that isn't in the script — but do note when the same generic label
recurs across scenes and whether it's plausibly the same individual or a
new one each time (flag the ambiguity rather than silently assuming
either way).

## Working from free narrative prose (no screenplay formatting)

A short story, novel excerpt, or literary adaptation carries the exact
same five categories of detail as a screenplay — it just embeds them in
narration and quoted dialogue instead of sluglines and cue lines. Extract
identically; only segmentation and character resolution need a different
technique:

- **Segmenting into scene-equivalent units.** Prose usually signals its
  own scene breaks — a centered divider (`◆ ◆ ◆`, `***`, `—`), a section
  heading, a chapter break, or a paragraph that abruptly relocates the
  action or jumps time. Treat any of these as a scene boundary, same as a
  slugline. If the text gives no explicit marker anywhere, segment by
  the same signal anyway: a new "scene" starts wherever the location
  changes or a clear time jump occurs, even mid-paragraph.
- **Location and day/night come from descriptive narration, not a
  header.** Infer INT/EXT from what's described (a room, hallway,
  stairwell, phone booth interior → INT; a street, roof, alley, rooftop →
  EXT) and day/night from explicit wording ("despite the deep night,"
  "across the nighttime rooftops," "the middle of the afternoon") when the text states it,
  or by carrying forward the nearest earlier explicit value per the same
  rule as screenplays (mark it **[inferred]**) when it doesn't.
- **Character resolution runs through narration and speech tags, not cue
  lines.** A speaker is identified by a dialogue tag ("said Cypher," "she
  answered") or by the narrator naming them directly in a nearby sentence
  ("The man's name was Cypher. The woman, Trinity.") rather than an
  ALL-CAPS cue. Resolve pronouns (he/she/they, or their equivalent) to
  the nearest explicit named antecedent, and flag as an ambiguity (per
  the rule above) any pronoun that could plausibly point to more than one
  recently-named character of the same gender/role.
- **Props, actions, and wardrobe extract exactly as they would from a
  screenplay** — they're simply phrased as narration ("a woman in
  tight black leather" instead of a wardrobe note in an action line)
  rather than as a formal description line.
- Everything else — the per-scene output format, the cross-reference
  index, flagging ambiguities instead of resolving them silently — applies
  identically regardless of source format.

## Process

1. **Determine whether the source is a formatted screenplay or free
   narrative prose**, and segment accordingly:
   - **Screenplay:** segment by slugline. A `CONTINUED:` marker at a page
     break is the same scene continuing, not a new one — merge it back
     into the scene it continues rather than treating it as separate.
     Keep the script's own scene numbers if present (including
     sub-numbered inserts like "A10") since later steps and
     cross-references will want to cite them.
   - **Free narrative prose:** segment per "Working from free narrative
     prose" above — explicit dividers/headings where present, location or
     time shifts where they aren't. Number the resulting units sequentially
     (Scene 1, Scene 2, ...) since prose rarely numbers its own scenes.

2. **Read the whole source once before extracting anything**, the same
   way `storyboard-narrative-breakdown` reads a full narrative first — a
   later scene can retroactively resolve an identity or establish that an
   earlier "unspecified" time-of-day should be read a certain way.

3. **For each scene, in order, fill in all five categories** using the
   rules above. Leave a category empty rather than padding it with
   nothing-content ("no notable props") if a scene genuinely has nothing
   for it.

4. **Build the cross-reference index** after the per-scene pass: for
   every character, prop, and location that recurs, note which scene
   first establishes its defining visual detail (a wardrobe rule, a
   specific look, a prop's exact description) and which later scenes it
   reappears in. This is what lets a downstream skill reuse "Agents wear
   dark suits and sunglasses even at night" (established once) instead of
   restating or re-deriving it for every later Agent scene.

5. **Flag ambiguities explicitly** rather than resolving them silently —
   an unnamed recurring role whose sameness across scenes is unclear, a
   time-of-day inference that could be wrong if a cut scene skipped time,
   a prop description that changes slightly between mentions. These are
   exactly the kind of gap that becomes a visible continuity error once
   images are generated; surfacing them in text is much cheaper to fix.

## Output format

```
## Scene [number] — INT/EXT. LOCATION — DAY/NIGHT [+ "[inferred]" if not explicitly stated]
- **Characters:** [resolved names/roles, with any V.O./cue-resolution note]
- **Props:** [scene-specific props, or "none notable"]
- **Actions:** [key physical beats, each attributed to who performs it]
- **Wardrobe/appearance:** [costume/appearance notes stated in this scene, or "none stated"]
```

Repeat per scene, in script order. Finish with:

```
## Cross-reference index

### Characters
- [Name/role] — first established: Scene [N] ([defining detail]); appears in: [scene list]

### Recurring props
- [Prop] — first established: Scene [N] ([description]); appears in: [scene list]

### Locations
- [Location] — [INT/EXT], [day/night, noting any inferred values]; scenes: [scene list]

### Flagged ambiguities
- [one line per ambiguity, naming the scenes involved]
```
