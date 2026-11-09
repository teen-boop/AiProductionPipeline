# Prompt engineering: style lock, continuity, weather, and coverage

This is the mechanical core of keeping a whole project looking like one production instead of a
pile of unrelated generations. Read `02-reference-taxonomy.md` first — this file assumes the
photographic mode, light, DOF, and atmosphere of the project's style have already been identified.

## The STYLE LOCK block

Build this once per project, after the style references are read and the first masters are
approved. Keep it as a standing block of text and paste it **verbatim** into every production
prompt for the project — never re-derive or re-paraphrase the look from memory per-prompt, that's
exactly how drift creeps in over a long shot list.

```
STYLE LOCK:
Photographic mode: [cinematic film still / editorial fashion photography / other — see 02-reference-taxonomy.md]
Light: [named source(s) and behavior, e.g. "saturated crimson and cool cyan neon, low-key, volumetric in rain"]
Depth of field: [shallow with foreground blur / flat sharp-throughout]
Atmosphere: [haze / grain / desaturation / rain / etc, named explicitly]
Colour palette: [explicit named palette, e.g. "warm sandy tones, red desert cliffs, bright midday sun" or "deep red/cyan neon, black shadow"]
Film / technical: [e.g. "heavy film grain, anamorphic widescreen" or "flat lighting, sharp focus throughout"]
Aspect ratio: [locked value from project setup]
```

Update it only when the user deliberately changes the project's visual direction (e.g. a new
episode's palette shift) — and when that happens, treat it as a new STYLE LOCK version, not a
silent edit; note what changed and why so a later shot doesn't accidentally revert.

## Master shot + continuity/weather propagation

**Master shot.** The first approved wide/establishing/two-shot of a location becomes that scene's
master reference. Every other shot in that scene (close, medium, insert, two-shot) attaches the
master image as a reference, not just a text re-description — text-only re-description lets the
model reinvent architecture/furniture/decor differently each time even for the "same" room.

**Weather and physical-state propagation.** If the master shows rain, snow, fog, mud, or any other
environmental condition, every character entering that space afterward must show physically
consistent evidence of it — this is not automatic, state it explicitly:
- Wet hair, water droplets or dark damp patches on shoulders/fabric, a damp sheen on exposed skin,
  mud or wet grime on footwear, for anyone who just came in from rain.
- Fogged/condensation-streaked glass, wet floor reflecting available light, consistent puddle
  placement, for the environment itself across shots.
- The reverse also holds: don't let a character who has been indoors and dry for the whole scene
  suddenly show wet hair with no story reason.
- If real time has passed and a character has genuinely dried off or changed, say so explicitly in
  the prompt — otherwise assume continuity, not a fresh, decontextualized version of the character.

**Recurring-prop and detail lock.** Any object that recurs across multiple shots (a cord, a
suitcase, a key, a costume accessory, a specific stain or tear) needs its description held EXACTLY
constant in every prompt — same color/material/size words, pasted verbatim, not re-described from
memory. Treat the character's full current appearance in a scene (costume pieces, glasses on/off,
hairstyle state, wetness/dirt level, accessories) as a fixed string reused shot-to-shot within that
scene.

## Full prompt skeleton for a production shot

Once masters and character sheets exist, assemble every subsequent shot in this shape:

```
[Change to / Establish] [framing + action for this shot]

STYLE LOCK:
[paste the project's STYLE LOCK block verbatim]

Character: [locked clothing + wetness/dirt state + props, verbatim from the scene's fixed description]
Location: [locked architecture + lighting + weather, verbatim from the master]
[mandatory face clause — see 05-character-lock.md]
```

**Attachment order** (see `05-character-lock.md` for the full character-identity version of this
rule): master shot → character sheet (if one exists for this character) → real face photo →
approved portrait. Restating the locked details in text even when the master/sheet is attached
makes consistency more reliable than relying on the image reference alone.

## "Change to..." — generating consistent variants from an approved image

Once a shot is generated and approved, produce variants — a different framing, action, gaze
direction, or even an entirely different location — while keeping everything else (costume,
identity, style, props) locked, by using that approved image itself as a reference and writing a
prompt that starts with "Change to..." describing only what's different.

This is the primary mechanism for building scene coverage (wide → close-up, gaze/interaction
shifting) or relocating an established character look into a new setting, without redescribing
everything from scratch and risking drift. It's meant for depicting the **next beat of action inside
the same mini-scene** — not an unrelated new shot. Treat a mini-scene as a sequence of beats
(notices something → reacts → moves → resolves); each "Change to..." generation is the next moment
in that continuous beat.

How to apply:
- Attach the approved/generated image as one reference. If the character has a real face photo on
  file, also attach that photo — always, even here (see `05-character-lock.md`). Never rely on the
  base image alone for identity.
- Structure as: "Change to [the next beat/framing/action]: [describe only what changes], keep/same
  [the specific costume and identity details worth restating explicitly]."
- Three common variant types:
  1. **Reframing** — same scene, tighter/wider crop. "Change to a close-up of the person [doing
     some detail action]."
  2. **Redirecting attention** — same scene/framing, gaze or interaction changes. "Change to the
     character looking at [the second character/object]."
  3. **Relocating** — same character/costume/identity, entirely new location and action. "Change to
     a wide shot of the person [doing X] in [new setting]."
- Even when relocating, still carry over the STYLE LOCK block — a "Change to" prompt is not exempt
  from it.

## Coverage for dialogue and animation continuity

When a scene needs multiple angles of the same beat (e.g. shot/reverse-shot dialogue coverage, or a
sequence meant to be cut together or used as animation keyframes):

1. Generate the master two-shot/group shot first. Get it approved.
2. For each character's close-up, use `Change to a [tight/medium] close-up of [character], [specific
   action/expression]` with the master attached AND that character's face reference(s) attached.
3. Restate every locked detail in text on every close-up — clothing, wetness/dirt state, props,
   hair state — even though the master is attached as a reference. This is what prevents a close-up
   from quietly reinventing a detail the wide shot established.
4. For the next beat in the same exchange, chain from the most recent approved shot via another
   `Change to...`, not back from the original master — coverage should follow the actual sequence of
   moments, not radiate independently from a single source shot.

This produces a shot sequence that can be cut together or used as keyframes without continuity
breaks — same room, same wetness, same costume, same props, shot to shot.

## Character reference sheet (turnaround) — before heavy multi-angle coverage

Before generating many different angles/close-ups of a character (especially new characters), first
generate a 4-view turnaround sheet — see `assets/character-sheet-basic.md` for the template — and
use it as an additional locked reference alongside the real photo and approved hero portrait. This
catches drift a single front portrait can't reveal (body proportions, back/side hairstyle, costume
from other angles). For characters needing heavier coverage or a locked alternate state (wet,
injured, costume change), see `assets/character-sheet-full.md` and
`assets/character-sheet-state.md`.
