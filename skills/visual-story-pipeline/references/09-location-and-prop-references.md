# Location and prop references — build them like character references

**Confirmed directly by the user after observing that skipping this step produces inconsistent
locations/props across scenes: locations and recurring objects need their own dedicated reference
images, generated and locked BEFORE they're used across multiple scenes — the same discipline
already applied to characters, not a lighter-weight version of it.**

## The core workflow, in order

**Confirmed directly by the user: locations get the exact same treatment as characters, including
multi-angle coverage — a single shot is not enough on its own, the same way one character portrait
alone isn't enough for a character who'll get more than a few appearances.**

1. **Once a scene's script is finalized**, generate ONE medium shot of that scene's main character
   close enough to read clearly, but framed so the room/environment behind them is also clearly
   visible. This is the location's first, practical reference — the same role a character's first
   approved portrait plays for identity lock — and it goes straight into production use for that
   scene's actual shots.
2. **Generate a location turnaround sheet for that same location**, using
   `assets/location-sheet-basic.md` (four angles: wide establishing, reverse angle, a recurring
   detail/feature close-up, and a side/alternate angle — mirroring the character-sheet-basic
   four-view template exactly, just applied to the room instead of a person). This is what a
   single character-in-location shot can't provide on its own: coverage of angles that shot didn't
   establish, so a later scene needing the room from a different side doesn't have to invent it.
   Do this for any location that will recur across more than one scene — skip it only for a true
   one-off location that never appears again.
3. Both images — the character-in-location shot AND the location turnaround sheet — go into that
   location's reference folder (see folder structure below). Attach BOTH to every later generation
   set in this location, the same way a character generation always attaches both the real face
   photo and the approved portrait.
4. **Once a scene's prompt is written, read back through it and extract every character and every
   recurring prop mentioned** — this is a literal extraction pass over the prompt text itself, not a
   vague "keep an eye out." A second character, an animal, or an important prop (a telephone, an
   invention, a specific vehicle) that appears in this scene or is set up to reappear in a later one
   all get pulled out this way. Anything meeting that bar gets its own dedicated reference sheet,
   generated from the *same template structure* every time — the four-part shape (Subject
   description → Layout of views → Style & Consistency → Requirements) used in
   `assets/character-sheet-basic.md` is the master pattern; `assets/location-sheet-basic.md` and
   `assets/prop-sheet-basic.md` are the same structure applied to a room and to an object,
   respectively. Don't improvise a different shape per object — the consistent template is what
   makes these sheets reliable to generate and easy to QC the same way every time.
5. **Props and secondary subjects follow the identical discipline as character references** — once
   generated and approved, that image is the canonical reference for that object from then on, the
   same way an approved character portrait is (see `05-character-lock.md`). Attach it to every later
   generation that includes that object, don't re-describe it from memory each time.
6. **If it's unclear whether something needs its own reference** — a background detail that might or
   might not recur, an object whose future importance isn't obvious from the current scene alone —
   ask the user directly which details might be worth locking down, rather than guessing either way.
   Silently skipping a reference that turns out to matter, or generating one for something trivial
   the user never intended to reuse, are both worse than a short clarifying question.
7. **Every later scene that reuses a location or a locked prop must attach every reference image for
   it** — the character-in-location shot AND the turnaround sheet for a location, the standalone
   portrait for a prop — the same way character generations always attach both the face photo and
   the approved portrait. This is what keeps a location looking like the same room and a recurring
   object looking like the same object across scenes that may be generated days apart — text-only
   re-description drifts, image references don't.

## Folder structure

**References — organized by category, same tier as `Characters/`:**
```
01_References/
  Characters/<character-name>/
  Locations/<location-name>/       -- e.g. Locations/ThreeDoorRoom/, Locations/HotelLobby/
  Props/<prop-name>/                -- e.g. Props/BlackTelephone/, Props/RitaInvention/
```
Each location/prop folder holds its canonical reference image(s) — the character-medium-shot that
doubles as the location master, or the standalone prop portrait. When a location or prop gets a
corrected/updated reference later, keep the old one (rename with a version suffix) rather than
overwriting — the same non-destructive discipline as everywhere else in this pipeline.

**Generations — organized by scene, not by batch name:**
```
<project>/Scene_<NN>_v<version>/
  Tests_v<version>/          -- exploratory/rough attempts, not yet approved
  Working_frames_v<version>/ -- approved shots actually used in the cut
```
Example: `Scene_09_v1/Tests_v1/hotel_lobby_wide_attempt1.png`,
`Scene_09_v1/Working_frames_v1/hotel_lobby_wide.png`. This replaces the flatter `output/V1/` scheme
in `SKILL.md` §8 for any project using the location/prop-reference workflow — scope generations to
the scene they belong to, version the whole scene folder when a scene gets reworked, and keep tests
separate from approved working frames so it's obvious at a glance what's actually in the cut.

## Why this is worth the extra step

A location's architecture, color story, and lighting drift just as easily as a face does when it's
only ever re-described in text — a "mint-green three-door room" prompted fresh five times across a
project will not reliably produce the same room five times. Treating the location itself as a
locked reference, generated once and attached everywhere after, is the same fix that already works
for character identity, applied to the space the characters move through. The same logic applies to
any object the story leans on more than once — a torn photograph, a specific gadget, a running gag
prop — its exact appearance needs to survive being generated in a completely different scene weeks
later.
