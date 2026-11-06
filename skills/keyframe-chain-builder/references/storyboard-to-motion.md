# Storyboard to continuous motion

How to make a multi-shot performance (dance, fight, chase, sport) play as one take in Seedance: limbs never teleport, feet carry
weight, motion never resets at a cut. Adapted from scenario-labs/skills (`scenario-seedance-storyboard`, MIT); platform calls
removed, the method kept.

## The ten steps

| Step | What | How |
| --- | --- | --- |
| 1. Script | timecoded list, cast and setting agreed first | per shot: number, size, angle, lens or move, action verbs, entry and exit poses |
| 2. Plates | one image per performer who must stay recognizable, several angles | from the locked identity sheet (`character-identity-lock-setup`); extras generic and unnamed |
| 3. Briefs | one line per panel, coverage not pictures | master first, hold the axis, climb the size ladder, punctuate with an insert or reaction |
| 4. Panels | one generation per panel | plates as references, light pencil on bare paper, each at the delivery ratio |
| 5. Gate | two passes per panel, repair one panel at a time | artifacts, then differences (below) |
| 6. Assemble | approved panels into one board | compose the grid in code; approved panels are pasted, never regenerated |
| 7. Approve | script, plates and board shown to the user | reshoot by panel number |
| 8. Frames | two or three photoreal key frames | same plates, delivery ratio; they set the delivered look |
| 9. Video | one scripted run, or chained runs | one of the two lanes |
| 10. Check | delivery clean and carries its sound | sample every half second, match each cut to its panel |

Adjacent shots share an edge by construction: shot 3's exit is shot 4's entry. Name the POSITION as well as the pose: in a
two-person scene a mirrored boundary breaks the cut as hard as a wrong limb.

## Two lanes

**One scripted run.** The sequence fits one job's duration cap (check the current Seedance cap). Pass plates, board and key frames
as references; the plates hold identity, the pose chain holds continuity. Reference mode anchors frame one to the base state of
the reference world, so a sequence that must open on an exact pose belongs in the chained lane.

**Chained per-shot runs.** Past the cap, when each shot needs its own control, or when the opening pose is exact: render each
boundary pose as a still, then run shot N with start frame = still N-1 and end frame = still N. Adjacent shots share a frame both
sides agree on. N shots cost N+1 stills and N runs, and every run has a minimum duration, so more cuts than that floor allows
means fewer shots or more seconds. Land departures, returns and off-camera changes on a boundary still: whatever leaves frame
inside one run is gone for the rest of that run.

## Drawing the board

Thin pale pencil line, bare white paper, the setting in two or three quick lines, no shading, no rendered environment. Measured
by the source authors: a photoreal board leaked its panel number into 6 of 8 delivered shots; a heavily drawn pencil board
rendered its motion arrows as real arrows in shot; the same board redrawn light delivered 48 of 48 frames clean, arrows
included. Draw arrows broad, soft and pale. Generate panels one at a time, then compose the grid, so one bad panel costs one
panel.

Keep the composed board's aspect ratio between 0.4 and 2.5 (Seedance rejects references outside it). For 16:9 panels the board
ratio is 16 x columns / 9 x rows: 4x2 = 3.56 fails, 3x3 = 1.78 and 4x3 = 2.37 pass, a six-panel board wants 2x3 (1.19).

## The coherence gate

Run both passes on every panel; a panel fails if either fails:

1. **Artifacts:** melted finger joints, warped numerals, doubled blade edges (`independent-frame-critic`, `frame-qc-contact-sheet`).
2. **Differences against the plate:** count (hands, fingers, arms, blades, wheels), part to whole (a wheel inside its arch, a
   guard on its own blade, each hand on one arm), costume and livery details, screen side.

A board-level pass hides panel defects: twelve panels average them away. Judge a repair on the checklist, never on a score.
Repair with the correction as a positive requirement ("both wheels the same rim with whitewall tyres, each inside a wheel arch"),
not "not deformed".

What transfers into the video: marks the model reads as objects (heavy drawing), and plan errors (wrong costume, wrong side of
frame, wrong order). What often does not: local prop and limb geometry, which the video model re-derives. Spend one repair on
those, not three.

## The video prompt (scripted lane), seven sections

1. **REFERENCE ROLES.** What each reference governs and what it does not (see `reference-roles-leak-check`). The board is "a
   planning document only: play its N numbered panels in order, one shot per panel"; the key frames are "concept art that
   defines the look".
2. **GUIDES ARE NOT CONTENT.** A prohibition did not work, a definition did: "The storyboard's frame borders, panel numbers,
   caption text and motion arrows are planning guides drawn on paper by the director. They describe the shot, they are not
   objects in the world. None of them exists in the scene and none appears in any delivered frame." Then the short exclusion list.
3. **STARTING STATE.** One sentence of place, one of the opening pose.
4. **TIMELINE.** One entry per beat, each with timecode, `Panel N`, shot size with angle and lens or move, entry pose, exit pose,
   and the action as physics with soft-matter lag.
5. **CAMERA.** Real rigs only (dolly, tripod), no drift where static is asked, a shutter for the blur ("1/48 s on 35mm").
6. **MUST REMAIN UNCHANGED.** Identity, costume, location and light as invariants, plus the anatomy count ("two arms, two legs,
   five fingers on each hand in every frame").
7. **CONSTRAINTS.** Only what the timeline cannot say: duplicated limbs, feet sliding without weight transfer, teleporting,
   watermarks, slow motion, speed ramps, freeze frames. Sound: "Diegetic sound only: heel taps on the boards, fabric, breath, room
   tone." Name the sources; never name an instrument or genre, and never write "no music" (both have failed audio checks).

In the chained lane keep STARTING STATE, TIMELINE (one beat), CAMERA, MUST REMAIN UNCHANGED and CONSTRAINTS without the sound
paragraph; there are no reference roles and no board.

## Checking the delivery

Step through every cut: both sides agree in pose and match the panel. Then sweep the whole clip at two frames a second. Expect
fewer hard cuts than scripted (handoffs often render as camera moves) and cut the delivered take at the scripted points in the
edit (`render-cut-verification`, `nle-timeline-assembly`).
