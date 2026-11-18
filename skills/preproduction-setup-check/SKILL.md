---
name: preproduction-setup-check
description: Check that the most important parts of a visual project's setup are done BEFORE any frame or video is generated. From the script it extracts every scene's location, time of day, weather and light state, characters (each needs an approved hero card), wardrobe state, props and detail cards, look reference, camera reference and shot list, writes them into one SETUP manifest, and a script reports every gap per scene (missing hero card, no location card, no time of day, a reference with no role line, no camera ref, unapproved card). Use at the start of any ad, promo, film or series, before a generation batch, when frames drift (face or room changes between shots), or when asked "is the project set up", "what is missing before we generate", "check the setup", "setup audit". Triggers - setup check, preproduction check, what's missing, ready to generate, hero card, location card, time of day.
---

# Preproduction setup check

## This project first (binding)

1. **Study this project.** Read its brief or script, its references folder and the results already approved in it before writing the manifest.
2. **Learn from this project's results.** Read `LESSONS.md` first; it overrides the defaults here.
3. **Stay inside this project.** Cards, refs and paths come from this project's folders only.
4. **Examples here are samples.** Names in this file are invented.

## The rule this skill enforces

No frame is generated until every scene it belongs to passes. Every frame with a recurring person attaches that person's **hero card**; every scene attaches its **location card** and the **detail cards** of the props it shows, plus one **look reference** and one **camera reference**, each with a role line. A person described only in text drifts; a room described only in text changes when the camera turns.

## What a scene needs (the checklist)

| Item | What "done" means | Made with |
|---|---|---|
| Location | named, one location card (empty plate, all walls or a plan for reverse angles) | `location-room-map` |
| Time of day | named (dawn, morning, golden hour, dusk, night) | script |
| State | weather and light dials (wetness, light level, mess) | `location-state-dials` |
| Key light | the ONE named source per scene (window, lamp, low sun) | `cinematic-prompt-writer` |
| Characters | each has an APPROVED hero card: face front, 3/4, profile, full body, hands, jewellery, wardrobe | `character-identity-lock-setup` |
| Wardrobe state | per scene (clean, wet, dusty, sleeves up) | `story-continuity-ledger` |
| Props | each visible prop has a detail card (shape, material, colour, wear) | `reference-style-builder` |
| Look reference | an approved frame or style still, role line "look only" | `reference-style-builder` |
| Camera reference | a still from a real film or commercial, role line "camera only" | `ad-reference-edit-library` |
| Shot list | numbered shots with size, lens, move and the reason for the size | `storyboard-shot-selection` |
| Master shot | the wide that sets light, room and cast; close-ups are made from it | `keyframe-chain-builder` |
| Detail shots | inserts, push-ins and pull-outs listed, not only people shots | `storyboard-insert-ops` |
| Critic | frames pass `frame-qc-contact-sheet` and `independent-frame-critic` | |

Project-wide: style card (palette, light, lens, grain, measured), LESSONS.md, approved look.

## Workflow

1. **Extract.** Read the script and fill `SETUP.json` (template: `python3 scripts/setup_check.py init <project> --scenes "S1:title,S2:title"`). Fill every field from the script; when the script does not say (time of day, weather), propose a value and mark it `"proposed": true`.
2. **Check.** `python3 scripts/setup_check.py check <project>/SETUP.json`. It prints a table per scene and the project items, with OK, MISSING or UNAPPROVED, and exits 1 while anything blocks.
3. **Fill the gaps** with the skills in the table, in the reference order: style card, hero cards, empty locations, prop details, then frames.
4. **Approve.** Show the cards to the user; set `"approved": true` only on their yes.
5. **Generate** only scenes that pass; every prompt names its attachments in order (look, camera, hero card, location, props).

## SETUP.json shape

```json
{"project": "...", "style_card": "path", "lessons": "LESSONS.md", "look_approved": true,
 "characters": {"LEAD": {"hero_card": "path", "approved": true, "details": ["path"]}},
 "props": {"laptop": {"card": "path", "approved": false}},
 "locations": {"CAFE": {"card": "path", "plan": "path", "approved": false}},
 "scenes": [{"id": "S1", "title": "...", "location": "CAFE", "time_of_day": "dusk", "state": {"weather": "dry", "light": 3},
   "key_light": "warm pendant lamp", "characters": ["LEAD"], "wardrobe": {"LEAD": "hoodie"}, "props": ["laptop"],
   "look_ref": {"path": "...", "role": "look only"}, "camera_refs": [{"path": "...", "role": "camera only"}],
   "shots": ["L1", "D1a"], "master": "L6", "details": ["D1a", "D4"]}]}
```
Paths are relative to the project root.
