---
name: storyboard-narrative-breakdown
description: >-
  Takes a continuous, unstructured narrative description of a sequence (a
  paragraph of prose describing a camera moving through a series of events
  and locations, in any language) and breaks it into a numbered list of
  discrete mini-scenes, each tagged with its location, its event/subject,
  and the visual element (if any) that bridges it to the previous and next
  mini-scene. For each mini-scene, writes the actual generation prompt(s)
  (via `cinematic-prompt-writer` or the current project's own prompt-writing
  skill, whichever applies), embedding the bridging detail explicitly so
  consecutive shots read as one continuous sequence. Use whenever the user
  hands over a paragraph of "camera does X, then Y, then we see Z" narrative
  and needs it turned into an actual, generatable shot list. Triggers on
  break this down into shots, turn this narrative into a shot list, parse
  this sequence, mini-scene breakdown.
---

# Storyboard Narrative Breakdown

## Why this exists

A continuous narrative description ("camera flies to a poster, then rises to
a window, then we see a family, then the smoke from a chimney connects to a
train's smoke...") is written the way a person *thinks* about a sequence —
as one unbroken train of thought — not the way it needs to exist to be
generated, which is as discrete, individually-prompted shots. Two things go
wrong if you skip straight from prose to prompts:

- **Events/locations get merged or split wrong** — a sentence can describe
  two different shots (a window, then separately a chimney) that read as one
  run-on if you don't deliberately cut the prose at the right points.
- **The bridging detail that makes a transition read as continuous gets
  lost** — if the prose says smoke from a chimney becomes smoke from a train,
  and you prompt the chimney shot and the train shot independently without
  both explicitly describing matching smoke, the generated stills won't
  actually cut together as the intended match-transition; they'll just be
  two unrelated images of smoke.

This skill is the deliberate segmentation-and-bridging step between "here's
the sequence I'm imagining" and "here are the prompts."

## Where this sits relative to other skills

This is an **upstream, general-purpose** skill — it works on raw prose in any
project, before any of the following (all of which assume a shot list
already exists in text form):

- `storyboard-shot-selection` — decides the *shot size/type* (wide, medium,
  close-up, etc.) for each beat and why. Run this on the mini-scenes this
  skill produces if you want a rationale-driven size choice per shot rather
  than the wide/medium/close-up triad this skill defaults to (see Step 4).
- `storyboard-continuity-tracker` — validates that each shot's *physical
  state* (pose, position of tracked entities) logically follows the previous
  shot's end-state. Run this after breakdown if the sequence has recurring
  characters/objects whose physical continuity matters beat-to-beat.
- `storyboard-reference-assembly` — attaches the project's locked reference
  images to each shot at generation time.
- `storyboard-camera-continuity-ledger` — run this **alongside** this skill
  (see below): while this skill is writing image prompts, that skill is
  recording the camera-movement and transition-type metadata for the same
  sequence into a persistent ledger, and cross-checks that the bridging
  details this skill embeds in the prompts actually match what the ledger
  recorded. Use both together for any sequence where camera movement and
  cross-shot transitions matter (which is most narrative sequences — a
  static list of unrelated single images doesn't need it).
- `cinematic-prompt-writer` (or the current project's own equivalent, e.g. a
  Lovart-specific prompt skill) — this skill calls into whichever
  prompt-writing skill applies to actually word each mini-scene's prompts,
  rather than reimplementing style/framing logic itself. If the project has
  its own prompt-writing skill, prefer that; otherwise use
  `cinematic-prompt-writer`.

## Process

### 1. Read the whole narrative once, straight through, before segmenting anything

Don't start cutting mid-read — the ending can recontextualize an earlier
beat (e.g. "the drafting-office chalk dust" only makes sense as a *bridge*
once you've read that the previous beat ended on chalk dust from an
equation). Get the whole shape first.

### 2. Segment into mini-scenes at every location change AND every event change

A new mini-scene starts whenever **either**:
- the location changes (a different room, building, city, or setting), or
- the event/subject changes (different action, different subject in focus)
  even if the location hasn't visibly changed.

Do not merge two different subjects into one mini-scene just because the
prose describes them in one breath, and do not split one continuous
action into two mini-scenes just because it's a long sentence. A
transitional device (camera moving from A to B, or A morphing/matching into
B) is its own note on the boundary between two mini-scenes — it is not a
third mini-scene by itself, unless the transition device is itself long or
visually substantial enough to need its own generated frame (e.g. a several-
second sustained match-dissolve might warrant its own transitional shot;
a same-frame instant camera whip usually doesn't).

For each mini-scene, extract:
- **Location/setting** — as concrete as the source text allows (city
  square, a specific room, a factory floor); if the text is vague, note the
  assumption you're making, same as `cinematic-prompt-writer`'s Step 2.
- **Event/subject** — what's actually happening/what the shot is *of*.
- **Incoming bridge** — the specific visual element (if any) that carried
  over from the previous mini-scene (smoke, a hand gesture, a sound source,
  a match-cut shape). Empty/none if this mini-scene is a hard cut with no
  intentional visual bridge.
- **Outgoing bridge** — the visual element (if any) this mini-scene ends on
  that the *next* mini-scene needs to pick up and continue. This is usually
  the same physical element as the next mini-scene's incoming bridge,
  described consistently.
- **Camera action described in the source text**, verbatim or close to it
  (e.g. "camera flies up to the poster," "we pull back") — hand this
  directly to `storyboard-camera-continuity-ledger` (Step 5) rather than
  interpreting it yourself; that skill owns turning it into a formal camera-
  movement term.

Number the mini-scenes in sequence order.

### 3. Sanity-check the segmentation before writing any prompts

Read the mini-scene list back against the original prose once. Two checks:
- Does every noun/action in the source text land in exactly one mini-scene
  (nothing dropped, nothing duplicated)?
- Does every mini-scene with an incoming bridge have a mini-scene before it
  with the *same* element as its outgoing bridge, and vice versa? A bridge
  that's claimed on one side but missing on the other means the
  segmentation missed something — fix it before moving on.

### 4. For each mini-scene, write the prompt(s)

Call the project's own prompt-writing skill if one exists (check for it the
same way `cinematic-prompt-writer` does in its Step 1), otherwise
`cinematic-prompt-writer`. Default to that skill's own shot-size triad
(wide/medium/close-up) unless the mini-scene is simple/small enough that one
size clearly does the job (a single detail insert, e.g. "a hand holding a
telephone," rarely needs a wide establishing variant) — note when you're
deliberately skipping a size and why, don't silently omit it.

**The bridging detail is mandatory, explicit text in the prompt, not an
assumption:** if mini-scene 4 hands off smoke to mini-scene 5, mini-scene
4's prompt(s) must describe that smoke's specific look (density, color,
direction) in a way mini-scene 5's prompt(s) then repeat/continue
consistently (same smoke, same direction, transforming into or matching the
new source). This is the single most common way a generated sequence fails
to read as continuous, and it's checkable — see
`storyboard-camera-continuity-ledger`.

### 5. Hand off camera/transition data

For every mini-scene, pass its recorded camera action and bridge notes to
`storyboard-camera-continuity-ledger` so that skill can log the formal
camera-movement term and transition type, and cross-check your prompts
against it. Do this as you go (mini-scene by mini-scene) rather than saving
it all for the end, so a mismatch gets caught while the context is still
fresh.

## Output format

```
## Mini-scene N — [short label]
- **Location:** ...
- **Event/subject:** ...
- **Incoming bridge:** [element, or "none — hard cut"]
- **Outgoing bridge:** [element, or "none — hard cut"]
- **Camera action (source text):** "..." [verbatim/near-verbatim quote from the narrative]

**Wide:** [prompt]
**Medium:** [prompt]
**Close-up:** [prompt]
```

Repeat per mini-scene, in sequence order. Finish with a one-paragraph
sanity-check note confirming Step 3's two checks passed (or what you fixed).
