---
name: location-state-dials
description: >-
  Keeps one location consistent while its STATE changes across a story: wear, wetness, light/power, tidiness, crowd, weather, time of
  day, damage, smoke/haze, season. Each location gets a small DIALS block where every dial has a value AND a sentence saying what that
  value means in THIS place ("wetness 7 = puddles in the stone joints, wet sheen on the counter, no standing water inside"). Named
  presets ("morning open", "after the storm", "abandoned 10 years") are combinations of dial values, so "the same room at a different
  moment" is reproducible. Each dial is tagged with its cost: prompt-only change, or needs a new reference plate. Use when the same
  location appears in different moments, times, weather or conditions; when frames of one room drift between scenes; or when asked
  for "same place, later / at night / after X".
user-invocable: true
---

# Location State Dials

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

A location reference (plate, room map) fixes the GEOMETRY. The dials fix the STATE. Without them every prompt re-describes
"rainy" or "messy" in new words and the room changes character from shot to shot.

## 1. The dials (pick the ones the story touches; 3–6 per location)

| Dial | 0 | 10 |
|---|---|---|
| wear | brand new, clean edges | worn through, chipped, patched |
| wetness | bone dry | flooded, everything dripping |
| light / power | all practicals on, bright | no power, single torch or moonlight |
| tidiness | staged, nothing out of place | ransacked, objects on the floor |
| crowd | empty | packed shoulder to shoulder |
| weather (exteriors) | still clear sky | storm, horizontal rain, wind |
| time of day | pre-dawn | late night (write the clock time, e.g. 21:40) |
| damage | intact | burnt / broken / collapsed |
| haze / smoke | crisp air | thick haze, beams visible |
| season / growth | bare winter | overgrown summer |

## 2. Write the DIALS block once per location

```
LOCATION L2 · kitchen · plate: references/Locations/kitchen/plate_master.png
DIALS (value · what it means HERE · cost)
  wetness 2 · a ring of water by the sink, everything else dry · prompt
  light   6 · ceiling bulb off, warm under-cabinet strip on, window daylight · prompt
  tidiness 4 · one pan on the stove, two mugs by the kettle, chairs pushed in · prompt
  wear    5 · chipped tile edge left of the stove, faded curtain · plate
```

- The "what it means here" sentence names concrete, visible objects in this room. A number alone does nothing in a prompt; the
  sentence is what gets pasted.
- **Cost tag:** `prompt` = the plate stays valid, only the text changes. `plate` = the state changes geometry or materials so much
  (flooded floor, fire damage, overgrowth, a crowd) that a new reference plate of that state must be generated first (from the master
  plate, "same room, same camera, change only …").

## 3. Presets

Name the combinations the story needs and keep them next to the block:

```
PRESET "morning open"   wetness 1 · light 8 · tidiness 3 · crowd 0
PRESET "after the storm" wetness 8 (plate) · light 2 · tidiness 7 · damage 3 (plate)
```

A shot line then says only: `Location L2 kitchen, preset "after the storm"` and the prompt writer pastes the sentences of every dial
in that preset, in the same words every time.

## 4. Use in prompts

- Paste the preset's sentences into the still prompt's location line and into the video prompt's LOOK / LIGHT lines.
- When a dial changes INSIDE a video shot (lights go out, rain starts), write it as an event on the timeline:
  `2–3 s: the power dies — light dial 6 → 1: only the window remains, the strip light goes dark`.
- Add the dial values of each shot to the continuity ledger so neighbouring shots can be checked.

## 5. QC

Compare frames of the same preset side by side: the named objects in each dial sentence must be present and the same (the ring of
water, the chipped tile). A frame that contradicts a dial sentence is a reject with that sentence as the fix line.

## Never

- Never describe a state with mood words only ("gloomy, messy"); always the visible objects.
- Never change a `plate`-cost dial by prompt alone; generate the state plate first.
- Never let two presets of the same location use different wording for the same dial value.
