# Edit Patterns from 24 Pinterest References (+1 still)

Source clips: a study set of 24 short reference videos (ids e01 ... e24) and one still (e_still); the files are not bundled.
Contact sheets and raw numbers are not bundled with the skill; the figures below are the record of the study.
Method: ffmpeg scene detection at 0.30 and 0.15 on a 180 px proxy, every cut checked on a contact sheet, beats with `hyperframes beats`, onset hit-rate test against random cut sets, luminance curves (signalstats YAVG) for flashes and burst.

## Headline findings

1. **18 of 24 references are a single uncut take** (median 11.3 s, range 5.2-41.4 s). On Pinterest a "premium AI video" is usually one living still: one strong composition, held 5-40 s, with one slow camera move and one or two small events (lightning, light growing, a figure walking). The edit is the hold. Even the one slow multi-shot piece (e20) uses only 4 shots of 5-10 s in 29 s.
2. **The three real montages (e10, e18, e11) run at 0.13-0.92 s median shot length**, and none of them is beat-locked. Cut timing measured against beats and onsets came out at chance level (e09 3/9 = chance 0.33; e10 0.43 vs random 0.44; e18 0.29 vs random 0.60). The rhythm comes from the pictures (accelerate, then release on a long hold), not from the music grid. Pinterest re-uploads often swap the audio, so treat beat sync as optional polish, never as the structure.
3. **Look consistency carries everything.** Every montage locks one palette (e10 amber/brown, e18 orange/black silhouettes, e11 red/teal, e09 warm gold + cool church interior). Shots can change place, scale and subject freely as long as palette and light direction stay.
4. **Transitions are almost all hard cuts.** The only effects are a 0.3-0.4 s overexposed flash (e09), a 0.47 s dip to black (e20, slow pieces only) and in-shot light flashes (e02 lightning, e15 burst). No wipes, spins, zoom-transitions or glitches anywhere. Note: gradual dips are invisible to scene detection at 0.15; check luminance curves too.
5. **Endings are holds or light events, never a logo slam.** Long final hold (e10 4.1 s, e18 1.3 s), white-out (e15), cut to black (e12), 2 s fade to black into a small typed title card (e20), the subject walking out of frame (e23), or a seamless loop (e09, e11, e16).

## Per-video table

| id | length | aspect | cuts | median shot | music / beat sync | edit idea |
|---|---|---|---|---|---|---|
| e01 | 8.1 s | 4:5 (720x900) | 0 | 8.1 s | music, no cuts to sync | Static wide; man on sofa, wall of fire behind. Motion only in flames and smoke. |
| e02 | 8.0 s | 9:16 | 0 | 8.0 s | ambient, n/a | Static night house + lone figure; 5 lightning flashes (0.17-0.27 s each) are the only "edits". |
| e03 | 24.6 s | 9:16 | 0 | 24.6 s | ambient, n/a | Slow drift with foreground flower parallax; city tower at dusk. |
| e04 | 22.2 s | 9:16 | 0 | 22.2 s | ambient, n/a | Very slow push through dark trees to a lit house. |
| e05 | 19.6 s | 9:16 | 0 | 19.6 s | ambient, n/a | Slow push/reframe on neon CAFE sign, clouds rolling. |
| e06 | 5.2 s | 9:16 | 0 | 5.2 s | silent | B/W high angle; figure walks along a shaft of light. |
| e07 | 5.2 s | 9:16 | 0 (1 hidden) | 5.2 s | silent | Low move through red grass; foreground grass sweeps the lens (1.35-2.0 s) and reveals a cliff: an in-camera wipe. |
| e08 | 12.9 s | 9:16 | 0 | 12.9 s | ambient, n/a | Slow push through backlit grass toward a distant figure. |
| e09 | 20.2 s loop (174.8 s file) | 9:16 | 4 flashes + 2 hard per loop | content shots 2.4-5.0 s | music 139.7 BPM, not synced | Five shots, one man (field / church / candle ECU / bench / cup ECU) joined by 0.33-0.40 s overexposed white-cyan and magenta flashes. |
| e10 | 60.1 s | 9:16 | 56 | 0.92 s | music, not synced | 57-shot golden-hour lifestyle montage of one woman; detail/wide alternation; day to night; ends on a 4.1 s fire hold. |
| e11 | 11.1 s | 9:16 | 91 | 0.13 s | music, not synced | Photo-flip: 92 stills of the same dancer silhouette, 3-4 frames each, neon red/teal, ~5.5 s loop played twice. |
| e12 | 26.2 s | 9:16 split into 2x 16:9 | 1 (to black) | 13.1 s | music 111.9 BPM, not synced | Stacked split screen: man top, woman bottom, both running screen-right. Parallel action, cut to black at 25.87 s. |
| e13 | 10.1 s | 9:16 | 0 | 10.1 s | ambient, n/a | B/W underwater; man sinks with a rose, slow follow. |
| e14 | 6.0 s | 3:4 | 0 | 6.0 s | ambient, n/a | Static; tiny figure in a patch of sunset light that slowly brightens. |
| e15 | 15.0 s | 1:1 | 0 | 15.0 s | music, n/a | Two hands reach; image darkens 4-7.3 s, bursts into light at 7.5-8.7 s, ends in white-out at 14 s. |
| e16 | 6.9 s | 9:16 | 0 | 6.9 s | music, n/a | Static on black; two climbers on giant ladders; seamless 3.45 s loop played twice. |
| e17 | 10.1 s | 9:16 | 0 | 10.1 s | music 136.7 BPM, n/a | Lateral tracking of a runner silhouette; orange light streaks pulse past; teal/orange. |
| e18 | 14.2 s | 9:16 | 17 | 0.75 s | music, not synced | 18-shot sunset friends montage: 1.5 s open, accelerates to 0.4-0.5 s, eases to 0.8-1.1 s, ends on 1.3 s splash. |
| e19 | 20.0 s | 9:16 | 0 | 20.0 s | ambient, n/a | Slow orbit around a cliff-top house; parallax on rocks and water. |
| e20 | 33.5 s (29.2 s picture + 4.3 s title) | 9:16 | 3 dips + fade + title | 8.2 s (picture shots) | music, no beats detected | B/W beach, man on a chair among birds: 4 shots of one moment (wide side, side-to-overhead move, overhead, overhead-to-ground descent) joined by 0.47 s dips to black; 2 s fade out, typed "Memory" title on black. |
| e21 | 12.4 s | 9:16 | 0 | 12.4 s | ambient, n/a | Static low angle on a street sign and lamp at night, snow falling. Object-only living still. |
| e22 | 12.6 s | 9:16 | 0 | 12.6 s | ambient, n/a | Prison yard in rain; one man slowly straightens and bows again; very slow push-in. Performance hold. |
| e23 | 7.3 s | 9:16 | 0 | 7.3 s | music 71.1 BPM, n/a | Side-on pan with a man dragging a burning chair over wet flats; camera stops, he exits frame right, end on the fire. |
| e24 | 41.4 s | 9:16 | 0 | 41.4 s | ambient, n/a | Near-static 41 s hold on a snowy cliff house: lit windows, chimney smoke, red lamp. Longest living still. |
| e_still | - | 3:4 | - | - | - | Silhouette in front of a glowing doorway in a dusk field; grain + motion smear; the target "one frame" look. |

## Patterns

Each pattern: **When**, **Recipe**, **Seen in**, **HyperFrames**. Times assume 30 fps (1 frame = 0.033 s).

### 1. The Living Still (single-take hold)
- **When:** hero/brand shot, mood piece, the 5-25 s loop for Pinterest/Reels, or any shot that is strong enough to carry alone.
- **Recipe:** one composition, 6-25 s. Camera moves 3-8% of frame size over the whole hold (slow push or drift). One secondary motion layer (smoke, clouds, grass, water) plus at most 1-2 discrete events. No cuts.
- **Seen in:** e01, e03, e04, e05, e08, e13, e14, e19, e21, e24 (41 s, the longest).
- **HyperFrames:** one AI clip (or still) in a full-bleed `<div>`; GSAP `fromTo(scale 1.00 -> 1.06, x 0 -> -2%, duration = clip length, ease "none")`. If the source is a still, add a separate moving layer (smoke/grain/cloud video, `mix-blend-mode: screen`, opacity 0.3-0.6) so it is not a Ken Burns slideshow.

### 2. Slow Push to the Light
- **When:** to pull the viewer into a place (a house, a sign, a doorway).
- **Recipe:** push-in at about 0.2-0.4% scale per second (e04: ~22 s, e05: ~20 s), aimed at the single warm light source in a cool frame. The warm source sits on a third line and never leaves frame.
- **Seen in:** e04, e05, e08, e22, e_still.
- **HyperFrames:** `gsap.to(img, {scale: 1.08, transformOrigin: "<x of light> <y of light>", duration: D, ease: "none"})`. Set `transformOrigin` on the light, not the centre.

### 3. Foreground Parallax Veil
- **When:** a wide landscape feels flat; you want depth and "real lens" credibility.
- **Recipe:** a soft, out-of-focus foreground layer (grass, flowers, branches) moves 2-4x faster than the background. Foreground covers 15-35% of frame, mostly the bottom or one edge.
- **Seen in:** e03, e07, e08, e04.
- **HyperFrames:** two layers: background plate `x: -1%` over the shot, foreground cut-out (PNG with alpha or a separate AI clip) `x: -4%`, `filter: blur(6-12px)`.

### 4. Foreground Wipe Reveal (hidden cut)
- **When:** to change location or reveal the payoff without a visible cut.
- **Recipe:** an object crosses the lens and fills 70-100% of frame for 8-18 frames (e07: 1.35-2.0 s), then clears on the new view. Move direction of the wipe = camera move direction.
- **Seen in:** e07.
- **HyperFrames:** clip A, then a dark foreground element (grass PNG, blurred) tweened across the frame `x: 110% -> -110%` in 0.5-0.6 s; swap A for B at the midpoint when the wipe covers > 90%. Keep the same light colour on both sides.

### 5. In-Shot Flash Event (lightning pulse)
- **When:** a static hold needs pulse without cutting; tension; a "beat" in an ambient piece.
- **Recipe (measured, e02):** luminance jumps ~+35% (55 -> 74-83 YAVG). Rise 2-3 frames, hold 2-4 frames, decay 3-4 frames: 0.17-0.27 s total. Spacing irregular: 1.0, 2.0, 1.8, 1.7 s. Sometimes a double flash.
- **Seen in:** e02 (5 flashes in 8 s).
- **HyperFrames:** white or pale-cyan overlay `div`, `mix-blend-mode: screen`; timeline `to(opacity .55, .07s) -> to(opacity .45, .1s) -> to(0, .12s)`. Put the flash on the sky area only (radial-gradient mask) so the subject stays a silhouette.

### 6. Overexposure Flash Transition
- **When:** to join shots that differ in place or time (memory, prayer, "meanwhile"), or every 2-5 s in a slow reel.
- **Recipe (measured, e09):** shot A brightens in 1-2 frames into an overexposed frame (YAVG 157 -> 222 white/cyan) holding a ghost of the next image. Total flash 0.30-0.40 s (about one beat at 140 BPM), then a hard drop into shot B at normal exposure. Use one colour variant (magenta) only once per loop, as the "return to start".
- **Seen in:** e09 (4.97-5.30, 10.07-10.47, 15.03-15.43 white/cyan; 20.17-20.47 magenta).
- **HyperFrames:** at the cut point `t`: shot B under shot A; overlay `#e8fbff` `to(opacity 1, 0.05s)` at t-0.05, cross-fade A->B underneath during the white, then `set(overlay opacity 0)` at t+0.30 (hard out, no fade). For magenta use `#ff6be0` at 0.85 with `mix-blend-mode: screen`.

### 7. Dip-then-Burst
- **When:** climax/product reveal.
- **Recipe (measured, e15):** before the payoff, darken the picture 25-30% over 3 s (YAVG 59 -> 42, 4.0-7.3 s). Then burst to about 4x brightness within 1.0-1.2 s (42 -> 165 at 7.5-8.7 s). Hold the bright state 4-5 s with slow decay. The contrast sells the burst more than the burst itself.
- **Seen in:** e15; the same logic in small in e02 and e14 (light patch grows).
- **HyperFrames:** a black overlay `to(opacity .3, 3s, "sine.inOut")`, then at the burst `to(black 0, .15s)` + a white/warm radial overlay `to(opacity .9, 1s, "expo.out")` + `scale 1.0 -> 1.04`.

### 8. White-Out Ending
- **When:** spiritual, energy, tech-reveal pieces; ending that leads into a title or loop.
- **Recipe:** in the last 0.7-1.0 s ramp to near-white (e15 YAVG peaks ~199 at 14.0-14.3 s), hold 2-6 frames, end.
- **Seen in:** e15.
- **HyperFrames:** full-frame warm white overlay `to(opacity 1, .6s, "power2.in")` ending 0.1 s before the composition end. A title, if any, appears inside the white (dark text) after the peak.

### 9. Cut to Black on Motion
- **When:** ending an action/parallel-action piece.
- **Recipe:** cut straight to black while the subject is still moving (no slow-down, no fade). Hold black 0.3 s max.
- **Seen in:** e12 (25.87 s, 0.33 s of black to the end).
- **HyperFrames:** `set(blackDiv, {opacity: 1}, cutTime)`. No fade.

### 10. Seamless Loop
- **When:** Pinterest/Reels pieces that should replay without a seam (the platform loops the file).
- **Recipe:** last frame equals first frame. Loop units measured: e16 3.45 s, e11 ~5.5 s, e09 20.17 s. Export 2+ loops in one file (e16 2x, e11 2x, e09 8.7x) so watch time beats the loop length.
- **Seen in:** e09, e11, e16.
- **HyperFrames:** build one loop as a sub-timeline and `repeat` it; for camera moves use symmetric yoyo (`yoyo: true`) or a move that returns to the start. For an AI clip, cross-fade the last 8-12 frames into the first frames.

### 11. Photo-Flip Stutter (stills at 3-4 frames)
- **When:** energy/nightlife/fashion beats; turning 20-90 similar AI stills into "motion".
- **Recipe (measured, e11):** each still holds 3 or 4 frames at 30 fps (alternating 0.133/0.100 s; ~8.3 images per second). All stills show the same subject, same silhouette scale and same palette; only pose and background blur change. Motion blur baked into each still. Run 5-6 s, then loop.
- **Seen in:** e11.
- **HyperFrames:** stack N `<img>` with `opacity 0`; timeline `set(img[i], {opacity:1}, i*0.117)` and `set(img[i-1], {opacity:0}, i*0.117)`. Keep subject centred within +-8% of frame width across stills, or it flickers instead of dancing.

### 12. Split-Screen Parallel Action
- **When:** two characters/products heading to the same moment; "two lives" story; comparisons.
- **Recipe:** stack two 16:9 panels in a 9:16 frame, no gutter. Both subjects move in the SAME screen direction at the SAME speed and size (e12: both run screen-right, side view, mid-shot). Each panel is one long take (13-25 s). Matching grade (B/W both).
- **Seen in:** e12.
- **HyperFrames:** two `div`s `height: 50%`, each `object-fit: cover` on its own clip; drive both with one timeline so their camera drifts match (`x` tween identical on both). Hide any AI loop seam with a 0.2-0.4 s motion-blur pass (CSS `filter: blur(2px)` pulse) on both panels at once.

### 13. Silhouette Continuity
- **When:** stitching many AI shots of varying faces/quality into one montage; protecting identity.
- **Recipe:** shoot the sequence against the sun/neon so people are 60-90% silhouette. Faces are shown in at most 1 of 4 shots. Cut on gestures (arm up, jump, spin) which read in silhouette.
- **Seen in:** e18 (almost all shots), e11, e17, e06, e14, e20, e23, e_still; e10 shows the face in about 1 of 3 shots.
- **HyperFrames:** pick shots by silhouette readability; add the same warm backlight glow overlay (radial gradient, `screen`) to every shot so the light source "matches".

### 14. Palette Lock Across Cuts
- **When:** always in a montage.
- **Recipe:** one dominant hue family across 100% of shots (e10 amber/brown from day to night, e18 orange/black, e11 red/teal). Brightness may change (day -> night), hue may not. A cool interior is allowed only when it is a deliberate second "world" that keeps coming back (e09 church vs field).
- **Seen in:** e10, e18, e11, e09, e17.
- **HyperFrames:** one shared CSS filter on the shot container (`filter: sepia(.2) saturate(1.1) hue-rotate(-8deg)` or a LUT applied before import) + the same grain overlay across all shots.

### 15. Detail / Wide / Face Alternation
- **When:** lifestyle and brand montages of 30-60 s.
- **Recipe:** rotate shot types so no two adjacent shots share scale. e10 pattern by position: face close (0-1 s) -> grass detail -> water detail -> landscape wide -> body in grass -> path wide -> porch medium -> silhouette ... Roughly 40% close/detail, 35% medium figure, 25% landscape. A landscape shot appears about every 4-6 shots as a "breath".
- **Seen in:** e10, e09, e18.
- **HyperFrames:** tag each shot `wide|med|close|detail` in the shot list and lint that `tag[i] != tag[i+1]`.

### 16. Accelerate-and-Release Rhythm
- **When:** any 10-20 s montage.
- **Recipe (measured, e18):** shots 1-2: 1.3-1.5 s (establish). Shots 3-10: shrink to 0.4-0.6 s (peak energy at about 30-50% of runtime). Shots 11-17: 0.8-1.1 s (release). Last shot: 1.3 s+. e10 does the same inside 60 s: a fast cluster at 16.6-19.6 s (0.46-0.75 s), steady ~0.9 s middle, final 4.1 s hold.
- **Seen in:** e18, e10.
- **HyperFrames:** generate shot durations from an envelope: `dur = lerp(1.4, 0.45, rampUp) ... lerp(0.45, 1.0, rampDown)`, snapped to whole frames.

### 17. Gesture-Peak Cut
- **When:** cutting between people in motion (dance, run, jump, splash).
- **Recipe:** cut 2-4 frames after the peak of a gesture (arm at highest point, top of jump), so the next shot starts already in motion. Never start a shot on a stationary subject in a fast section.
- **Seen in:** e18 (jump, arms up, spin), e11, e10 (hair toss, splash at 18.2-18.9 s).
- **HyperFrames:** for AI clips, trim in-point to the first frame with visible motion (`startAt` offset); for stills, add a 0.3-0.5 s micro-push (scale 1.0 -> 1.03) so even stills are "moving" at the cut.

### 18. Screen-Direction Lock
- **When:** running/walking/travel sequences, split screens.
- **Recipe:** all moving subjects travel the same screen direction (e12 both left-to-right; e17 runner left-to-right with streaks right-to-left for speed; e09 field walk consistent). Reverse direction only to mark a turning point.
- **Seen in:** e12, e17, e09, e18, e23.
- **HyperFrames:** flip any off-direction AI clip with `transform: scaleX(-1)` (check for text/logos first). Camera drift `x` in the same direction for every shot of the sequence.

### 19. Recurring Location Rotation (A-B-C-D-E-A)
- **When:** short story reels about one character with few assets (5 shots).
- **Recipe:** 4-6 distinct shots of one person, each 2.4-5 s, in a fixed order, joined by flashes, returning to shot A to close the loop. Alternate exterior-warm and interior-cool. Put an extreme close-up (candle profile, cup in hands) after each wide.
- **Seen in:** e09.
- **HyperFrames:** a 5-item array; timeline of [A 5.0][flash .33][B 2.4][C 2.4][flash .4][D 4.6][flash .4][E 4.7][magenta .3] = 20.2 s, then repeat.

### 20. Day-to-Night Arc
- **When:** 30-60 s brand stories that need an ending without words.
- **Recipe:** order shots by time of day: golden afternoon -> sunset -> blue hour (moon at 44.7 s) -> firelight/interior. The last 15% of runtime is night and slower (e10 last 6 shots 0.8-4.1 s).
- **Seen in:** e10; e18 stays in a single sunset (dusk only).
- **HyperFrames:** sort shots by a `light` field; add a slow global `brightness(1 -> .85)` across the piece so even the grade drifts toward night.

### 21. Frame-in-Frame Insert
- **When:** to add one surprising composition inside a fast montage.
- **Recipe:** one 0.4-0.5 s shot where the subject is seen through a door/window/mirror frame, dropped into the fastest part of the montage. Use once.
- **Seen in:** e18 (5.93-6.40 s, couple seen through a doorway), e10 (wing mirror 41.6 s).
- **HyperFrames:** a still or clip with a dark frame mask (`clip-path: inset(...)`) over black or over the previous shot's blurred plate.

### 22. Light-Patch Event
- **When:** a static shot needs a payoff without camera motion.
- **Recipe:** keep the frame locked; animate only a light patch that grows and brightens around a tiny figure over the whole shot (e14: 6 s).
- **Seen in:** e14, e06 (light shaft), e_still (glowing doorway).
- **HyperFrames:** radial-gradient overlay `screen`, `scale .8 -> 1.25`, `opacity .3 -> .8` over the shot, origin on the figure's feet.

### 23. Tiny Figure, Huge World
- **When:** premium/poetic tone; also hides AI face problems.
- **Recipe:** the human occupies 2-8% of frame height in the wide (e06, e14, e19, e02, e16). It is the only figure, placed on a third line, usually back to camera.
- **Seen in:** e01, e02, e06, e14, e16, e19, e20, e24, e_still.
- **HyperFrames:** compose the still this way at generation time; in the edit, never punch in further than 1.1x on these.

### 24. Lateral Speed Track with Light Streaks
- **When:** energy, sport, tech, "moving forward" messages without cuts.
- **Recipe:** side-on tracking; subject stays at a fixed screen x (centre-left); background and light streaks flow past fast. Streak pulses act as the rhythm (~every 0.6-0.8 s in e17).
- **Seen in:** e17.
- **HyperFrames:** subject clip/still static; background layer `x` tween looping; orange streak `div`s with `filter: blur(8px)`, `mix-blend-mode: screen`, tweened `x: 120% -> -120%` in 0.25-0.4 s, staggered.

### 25. Faded Film Texture
- **When:** to make AI images feel shot, not rendered.
- **Recipe:** lifted blacks (shadows never pure black except in B/W pieces), grain, soft highlights, slight motion smear (e_still), light leaks only as transitions (e09). One look for the whole piece.
- **Seen in:** e_still, e09, e10, e18, e03.
- **HyperFrames:** a looping grain video overlay at opacity 0.08-0.15 (`overlay` blend), plus a `curves`-like lift with CSS `filter: contrast(.92) brightness(1.03)`.

### 26. Dip-to-Black Breath
- **When:** slow, melancholic or memory pieces with long shots (5-10 s) of the same moment from different angles; never in a fast montage.
- **Recipe (measured, e20):** shot A darkens over 6 frames to about 15% brightness (YAVG 115 -> 18), shot B rises over 7 frames (18 -> 121): 0.47 s total, no frame of pure black held. Used every 8-10 s (5.87, 15.95, 24.13 s). Same grade on both sides.
- **Seen in:** e20.
- **HyperFrames:** black overlay `to(opacity .85, .2s, "power1.in")` ending at the cut, swap shots at the cut, `to(opacity 0, .23s, "power1.out")`. Do not hold black.

### 27. One Moment, Many Angles (angle progression)
- **When:** a single striking situation (a person, an object, a place) has to fill 20-30 s without new story beats.
- **Recipe (e20):** keep subject, moment and grade fixed; change only the camera position in a deliberate path: wide side (5.9 s) -> continuous move from side to over-shoulder to straight overhead (10.1 s) -> overhead hold while the wave washes in (8.2 s) -> descent from overhead to ground level (5.1 s). Each shot ends further from where the previous one started; the progression itself is the story.
- **Seen in:** e20.
- **HyperFrames:** generate 3-4 AI clips of the same scene with explicit camera paths (side, crane-over, top-down, crane-down) from one locked keyframe; join with pattern 26; order them so the camera's height keeps changing in one direction until the last shot.

### 28. Fade to Black into Typed Title Card
- **When:** an ending that names the piece or the brand without breaking the mood.
- **Recipe (measured, e20):** picture fades linearly for 2.0 s (27.2 -> 29.2 s). During the last 0.25 s of the fade the title types on letter by letter in about 0.2 s ("Me" -> "Memo" -> "Memory"), so text and image overlap briefly. The title then holds on black 3.8 s and fades out in 0.4 s. Title is small (about 2% of frame height), white bold sans, centred just below the middle, with a credit line at half size beneath it.
- **Seen in:** e20.
- **HyperFrames:** `to(blackOverlay, {opacity:1, duration:2, ease:"none"})`; at fadeEnd-0.25 s reveal characters with a `stagger: 0.035` `set` on per-letter spans; hold 3.8 s; `to(title, {opacity:0, duration:.4})`. Keep the title tiny; the black does the work.

### 29. Exit-Frame Ending
- **When:** to end a single-take action shot without a cut or fade.
- **Recipe (e23):** pan with the subject for most of the take, then stop the camera in the last 1.5-2 s and let the subject walk out of frame; the end frame is the object they leave behind (the burning chair). The file ends while the object is still in motion (flames).
- **Seen in:** e23.
- **HyperFrames:** pan tween on the background plate (`x`) that eases to a stop (`ease: "power2.out"`) 1.5-2 s before the end, while the subject layer keeps moving and exits; end the composition 0.3-0.5 s after the subject clears the frame edge.

### 30. Performance Hold
- **When:** a character beat (shame, grief, resolve) that should feel like cinema rather than an ad.
- **Recipe (e22):** one actor, static wide/medium, a single slow physical action repeated or developed over 10-13 s (straighten up, bow, straighten again), very slow push-in, rain or weather as the second motion layer. No cutaways.
- **Seen in:** e22, e13.
- **HyperFrames:** one AI clip, `scale 1.00 -> 1.05` over the whole clip with `transformOrigin` on the face; add a rain overlay at opacity 0.2-0.35. Prompt the clip for a slow, continuous action rather than a pose.

## Rhythm rules (from the measurements)

- **Hold pieces (single take):** 5-41 s; median of the 18 single takes = 11.3 s. Movement 3-8% over the whole take. 0-5 events (e02: 5 flashes in 8 s, one every 1.0-2.0 s).
- **Fast montage (e18, 14 s):** 12 cuts per 10 s. Median 0.75 s, min 0.40 s, max 1.53 s. Opening shot 1.3-1.5 s; peak section 0.4-0.6 s; ending shot >= 1.3 s.
- **Long lifestyle montage (e10, 60 s):** 9-11 cuts per 10 s, very steady (9/10/10/11/10 per 10 s block, then 6 in the last 10 s). Median 0.92 s, min 0.25 s, max 4.1 s (the final shot). Only 7 of 57 shots are > 1.5 s.
- **Story reel with transitions (e09):** content shots 2.4-5.0 s, about 3-4 transitions per 10 s; each flash 0.30-0.40 s.
- **Slow angle-progression piece (e20):** 4 shots of 5.1-10.1 s (median 6.9 s) in 29.2 s of picture = about 1 transition per 10 s; 0.47 s dips; 2.0 s fade-out; 3.8 s title hold. Total runtime 33.5 s, title = 13% of it.
- **Stutter flips (e11):** 0.10-0.14 s per image, ~83 changes per 10 s; never longer than 6 s before looping.
- **Hook (first 1-2 s):** the first shot is either already a full composition with motion (single takes) or a 1.0-1.5 s face/gesture close-up (e10 face in grass at 0-1.0 s; e18 runners at 0-1.5 s). No shot under 0.5 s in the first 1.5 s.
- **Payoff/ending:** final shot 1.5-4x the median shot length (e10 4.5x, e18 1.7x), or a light event (white-out) or cut to black.
- **Slow down before the end:** the last 10-15% of a montage has fewer cuts (e10: 6 cuts in the last 10 s vs 10 before).
- **Beat sync:** none of the references locks cuts to beats. If you sync, sync only the 3-5 accent cuts (open, peak, ending) and let the rest follow the picture.
- **Rule of thumb for a 15 s promo:** 1 hold of 1.5 s + 8-12 shots at 0.5-1.0 s + final hold of 1.5-2.5 s = 11-15 shots.
- **Rule of thumb for a 30 s promo:** 22-30 shots, median 0.9-1.1 s, one fast cluster of 4-6 shots at 0.4-0.6 s around the 40-60% mark, final hold 2.5-4 s.

## Openings and endings

**Openings seen**
- In motion from frame 1: running (e12, e17), walking (e06, e09), gesture (e18). No fade-in from black anywhere.
- Intimate close-up first, world second (e10: face in grass, then grass, then water, then wide landscape).
- Single takes open on the final composition already; the camera move reveals more, it does not establish.

**Endings seen**
- Long, slower hold on a warm/intimate image (e10 fire, 4.1 s; e18 splash, 1.3 s).
- White-out (e15).
- Hard cut to black while moving (e12).
- Seamless loop back to the opening frame (e09, e11, e16).
- Fade to black over 2.0 s with a small typed title arriving at the very end of the fade, held 3.8 s on black (e20).
- Subject walks out of a stopped frame; end on the object left behind (e23).
- Never: logo slam, zoom-out to logo, fast spin.

## Text on screen

Only 1 of the 24 references uses text (e20), and only at the end. No captions, no mid-video titles anywhere.
- **What e20 does:** a single word title ("Memory") plus a tiny credit line, on black, after the picture has faded out. Typed on letter by letter in about 0.2 s during the last frames of the fade, held 3.8 s, faded out 0.4 s. Size about 2% of frame height, white bold sans, centred just below the middle. See pattern 28.
- Keep text off the first 1.5 s and off the fast sections.
- If a title is required, put it on black after a fade (e20), inside a white-out (pattern 8) or over a dark final hold, in negative space. Hold at least 1.5 s plus 0.3 s per word; e20 uses 3.8 s for one word.
- Small beats big: the premium look keeps the title tiny and lets the black frame carry it.

## Mistakes to avoid (vs what the references do)

| Mistake | What the references do |
|---|---|
| Ken Burns on a dead still (zoom on an image where nothing moves). | Every hold has a second motion layer: smoke, clouds, grass, water, light (e01, e03, e05, e13, e14). |
| Cutting fast for the whole piece. | Fast sections are bounded: open on 1.3-1.5 s, peak at 0.4-0.6 s, release, end on a long hold (e18, e10). |
| Fancy transitions (spins, glitches, zoom-blurs, slide wipes). | Hard cuts; at most one flash type (e09) or an in-camera foreground wipe (e07). |
| Every cut on the beat, making it feel mechanical. | Cut timing follows gestures and picture rhythm; beat alignment measured at chance level in all references. |
| Mixed palettes from different AI generations. | One hue family across all shots, two worlds max (e09). Grade every shot through one filter. |
| Faces in every shot (identity drift becomes visible). | Silhouettes, backs, hands, details; faces only 1 in 3-4 shots (e18, e10, e11). |
| Two adjacent shots of the same scale. | Alternate detail/medium/wide; a landscape "breath" every 4-6 shots (e10). |
| Subjects changing screen direction randomly. | Same direction across the sequence and across split panels (e12, e17). |
| Ending on a fade to black after a weak shot, or on a logo slam. | End on the strongest warm hold, a white-out, or a cut to black during motion. |
| Visible loop seams in AI clips. | Seamless loops exported 2x+, or a seam hidden in motion blur (e12 at ~7 s). |
| Big camera moves to "add energy" to a still. | Moves of 3-8% of frame over the whole hold; energy comes from in-frame motion and light. |
| Tiny subject then aggressive punch-in that shows AI artefacts. | Tiny figure stays tiny; scale changes come from cutting to a different shot, not zooming the same one. |
| Holding pure black between shots, or slow 1-2 s cross-dissolves. | Dips to black of 0.47 s that never rest on black (e20), or hard cuts. |
| Big centred title cards mid-video. | One tiny word at the end, on black, after the picture has gone (e20). |

## Changelog

- e20-e24 added: 4 more single takes (e21 object-only still, e22 performance hold, e23 exit-frame ending, e24 41 s still, now the longest) and one slow 4-shot piece (e20) that adds the dip-to-black transition, angle progression, and the first on-screen text (fade into a typed title card). New patterns 26-30. Single takes now 18 of 24 (median 11.3 s, was 10.1 s); text-on-screen and endings sections updated; montage rhythm numbers unchanged.
