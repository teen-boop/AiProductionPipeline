---
name: location-room-map
description: Turns any location reference (usually one photo of one wall) into a COMPLETE, physically plausible room — a top-down floor plan, all four walls described and generated as separate wall references, every door/window/furniture piece fixed in place — so reverse shots, over-the-shoulder shots and close-ups always show the CORRECT wall behind the subject instead of repeating the one wall from the photo. Enforces architecture rules (windows on at most 2 walls, at least one door, one of each recurring object). Run once per interior location, after the location reference exists and before any coverage of that location. Use whenever a scene has more than one camera direction in a room, when a reverse/OTS shot is planned, when generations repeat the same background wall, or the user says "задний фон одинаковый", "сделай всю комнату", "карта локации", "где дверь", "обратная точка". Output in Russian, prompts in English.
---

# Location Room Map

## Why
Image models only know the wall they were shown. Ask for "a reverse shot from behind the sofa" with the photo of the window wall attached, and the model puts the window wall behind the heroes again. The room has no back, no door, and everything the story needs (a TV, a front door) gets pasted in front of the one known wall, sometimes twice. The fix: before coverage, invent the whole room once, lock it, generate each wall as its own reference, and choose the background reference by camera direction.

## Architecture rules (hard)
1. **Four walls, named by compass:** N, E, S, W. The wall shown in the source photo is **N**. The camera of the source photo stands at the S wall looking N.
2. **Windows on at most 2 walls**, and those 2 walls must be **adjacent** (a corner apartment), never opposite. Usually windows sit on N only.
3. **At least one door.** If the source shows windows but no door, put the door on a wall WITHOUT windows: an entrance door (hallway/front door) or an internal door/open doorway (kitchen, bedroom). A living room normally gets both: entrance door + doorway to another room.
4. **One of each recurring object.** One TV, one sofa, one coffee table, etc. Every object gets one fixed position on the plan, and no prompt may add a second one.
5. **Furniture backs onto walls logically.** The sofa back is against a wall or floats with clear space behind it (state which). The TV faces the sofa from the opposite wall. Lamps sit where their light falls in the established shots.
6. **Invented elements must not contradict the source photo.** Keep its floor, ceiling height, moulding, wall colour, era and style on all four walls.
7. **Same density as the source (hard).** Count what the source wall holds (furniture pieces, framed pictures, lamps, shelves, plants, small objects) and give every invented wall a comparable count, layered in depth: floor furniture + wall art + small objects + a light source + one plant or textile. No large empty wall areas, no "show-home" bareness. Repeat the source's signature materials and motifs (same abstract-poster style, same walnut wood, same lamp family, same rug) so every wall reads as the SAME lived-in room. Always attach the source photo when generating a wall.
8. **Light sources are mapped too.** Windows (and what is outside them by day and by night), every practical lamp: wall and position. Night versions inherit the same positions.

## Process
1. **Inventory the source photo**: walls visible, windows (count, wall), doors, every piece of furniture and decor, wall colour, floor, ceiling, era.
2. **Draft the floor plan** as an ASCII top-down map with N at the top: walls, windows `[==]`, doors `/ D`, furniture with names, TV, rug, lamps `*`. Approximate room size in metres.
3. **Describe each wall** N/E/S/W in one locked paragraph (`WALL N — ...`), listing left-to-right what a camera facing that wall sees.
4. **Camera direction table**: camera position → wall facing → wall reference to attach. Include standard setups: wide from TV, reverse from behind/over the sofa, CU on sofa (background = wall behind the sofa), table-level macro.
5. **Seat/zone map** of the main furniture (which seat is left/right when seen from the S and from the N, since a reverse shot mirrors left and right).
6. **Write a wall-generation prompt per missing wall**, attaching the source/master (for style, materials, light) and stating explicitly: "This is the OPPOSITE wall of the attached room, which is NOT visible in the attached image."
7. **Generate the walls → QC → lock** as `REF-<LOC>-<TIME>-WALL-<N|E|S|W>`. QC: density comparable to the source (no bare walls), correct wall content, no windows where the plan has none, door present, no duplicates of single objects, same materials and colour as the source.
8. **Write `ROOM_MAP.md`** in the project's locations folder: plan, wall paragraphs, camera table, seat map, light map, file names. Link it from the project CLAUDE.md.

## Template: wall prompt
```
Reverse view of the same room: this is the [S] wall, the wall OPPOSITE the windows of the attached room — it is NOT visible in the attached image, build it from this description while keeping the same floor, mouldings, wall colour, era and [night] lighting exactly.
WALL [S], left to right: [ ... ].
No windows on this wall. [Exactly one TV.] Same room height and wooden floor as the reference. Camera at the opposite wall, eye level, 4:3, empty room, no people, no animals.
[STYLE LOCK verbatim]
```

## How other skills use the map
- Every coverage prompt for this location gets a `BACKGROUND:` line naming the wall behind the subject and attaches that wall reference **instead of** the generic room photo.
- Storyboard panels and shots also carry a one-line ROOM DENSITY description of the visible wall and attach the room reference, so even pencil panels show the same furnished room, not an empty box.
- `scene-continuity-lock` reads the seat map and camera table from `ROOM_MAP.md`.
