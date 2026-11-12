# Ad pace and designed transitions (companion to cinema-director-v3)

Use this file when a prompt is written for an ad or a fast reel, and whenever a generation slot (from `reference-rough-cut`)
carries a transition in or out that is not a plain cut. The 16-slot spine stays as it is; this file only decides what goes into
HEADER, CAMERA, ACTION TIMING and LOCKS, and what is left to the edit.

## 1. Pace: generate long, cut short

Ad edits cut far shorter than a generator draws one shot well. Measured on premium spots, the median shot is 1.0-1.8 s,
energetic sport and dance edits cut 40-70 times a minute with 20-40% of shots under 0.5 s, and premium lifestyle films cut
20-35 times a minute with a long held ending.

- **Never ask the model for 0.4 s shots.** Generate each planned shot as a 2-3 s segment (or a 4-8 s single take that contains
  several usable moments) and cut the 0.3-1.0 s you need in the edit. Name the HARVEST WINDOW in the slot: which second of the
  generation becomes the cut.
- A multi-shot prompt keeps segments at 1.5-2.5 s (the runtime guide in SLOT 1). Faster rhythm is built in the edit from those segments.
- **Speed ramps, flash frames, echo trails, graphic slides and dissolves are edit work.** Keep the generation real-time (SLOT 1
  default) and do the effect in the NLE or HyperFrames. Prompting a ramp gives soft, smeared motion everywhere.
- Copy the pace SHAPE of the reference, not only its speed: calm hold, burst, calm hold; or accelerate into a long final hold.
  Plan one still moment per 10-15 s; a reel that is fast all the time feels slow.

## 2. What makes a shot read as dynamic

- **Lens close to the action.** Ultra-wide (FOV 95-110 degrees) at 0.5-1.5 m from the subject, low (knee or ground height);
  speed reads against foreground that rushes past. A long lens (FOV 15-25 degrees) only for compression shots (runner against a
  wall of traffic).
- **The camera answers the subject.** Whip pans follow a head turn or a throw, the camera rises with a jump and drops with a
  landing, then settles within 6-10 frames.
- **Foreground occluders.** A pillar, a shoulder, a door frame or fabric crosses the lens every few seconds; that is also where cuts hide.
- **Measured speed.** `camera travels 3 m in 1 s`, `pan of 90 degrees in 0.25 s`, `product rotates one full turn in 2 s`.
  Without numbers the model drifts to a slow average.
- **Motion blur is a choice.** Ask for natural 180-degree-shutter motion blur on moving parts; ask for strong directional smear
  only inside a whip window (the 4-6 frames you will cut inside).
- **Hands and products in macro.** One insert of a hand acting on the product every 3-5 shots (press, pour, lace, tap) with the
  surface contact visible: dust lifts, liquid beads, fabric creases.
- **Light changes as events.** A flare peak, a door opening onto sun, a strobe burst: a timed change of light gives the edit a
  cut point and the eye a beat.

## 3. Transition handoffs (two clips meet at one cut)

Every designed transition is written as an EXIT on clip A (its last 0.3-0.6 s) and an ENTRY on clip B (its first 0.3-0.6 s), in
ACTION TIMING with timecodes and in CAMERA. Direction, speed and screen position must be identical on both sides. Write the
transition as camera and subject action only; words like "transition", "dissolve", "wipe effect" or "cut to" inside a prompt make
the model draw an effect.

| Kind | Clip A exit | Clip B entry | Edit |
|---|---|---|---|
| WHIP_PAN | camera whips right at ~360 degrees/s for the last 0.25 s, frame smears horizontally | starts mid-whip, same direction and speed, settles on the subject by 0.3 s | cut in the middle of the smear, 2-4 frames each side |
| WHIP (smear cut) | the action peaks (swing, head turn, throw) and smears for 4-6 frames | starts inside the same motion, already blurred, settles | cut on the fastest frame |
| BODY_WIPE | a shoulder or fabric passes 20-40 cm from the lens and fills the frame, left to right | fabric leaves the frame left to right, revealing the new place | cut when the frame is fully covered |
| OBJECT_WIPE | a page, card or note flies across the lens and covers it | the same object clears the frame in the same direction | cut at full cover; object colour identical |
| CAMERA_BLOCK | the subject jumps or throws something straight at the lens; the frame goes black or fully blurred | opens from black or blur, ultra-wide low angle, subject landing | cut on the black frame |
| PUSH_IN | slow push-in to macro until one texture fills the frame (paper fibre, fabric weave, liquid surface) | starts on the same texture, pulls back to reveal a new place | cut on the texture |
| PORTAL | camera flies at a flat surface (painting, screen, window) and passes through it | starts inside the new world, same vector and speed | cut at the surface plane |
| SPIN | camera rolls 90-180 degrees with blur in the last 0.3 s | starts mid-roll in the same direction, levels out | cut mid-roll |
| MATCH_CUT | ends on a held composition: object centred, set size and position | first frame repeats that object's size and position in a new world | straight cut; build the pair of first frames with `keyframe-chain-builder` |
| PRODUCT_PUSH | the product is pushed toward a gap (slot, door, hand) and leaves frame | the product arrives on the other side at the same speed | cut as it leaves frame |
| FLASH | a light source flares to near white in the last 3-4 frames | opens from the flare's falloff | 2-4 frames of white or coloured flare added in the edit |
| ECHO, GRAPHIC_SLIDE, DISSOLVE | generate the move clean on a dark or plain set | | done entirely in the edit |

Build both sides from frames, not from prose when the generator accepts a start frame: extract clip A's last frame and use it as
clip B's first-frame reference (or generate the A-end and B-start keyframes together as a pair). After generation, check the
two sides on a frame strip (`render-cut-verification` cut strips) before the cut is accepted: same direction, same speed, no flash
of a third image.

## 4. Copying motion from a reference clip

A slot from `reference-rough-cut` names a reference clip and its in point. Translate it into measured words in CAMERA and ACTION
TIMING: rig and height, FOV, direction, distance, speed, when the move starts and stops, where the subject sits in frame on the
first and last frame. When the target model accepts a video reference, attach the reference trimmed to the slot as a MOTION
reference only, and say so in its role line: `@Video 1: camera move and timing only, never its people, clothes, location, logos
or text`. Never pass frames with logos, burnt-in subtitles or real people as image references.

## 5. Pre-delivery check for ad prompts

- Each segment 1.5 s or longer; the harvest window named for every planned cut shorter than that.
- Every non-CUT transition has an EXIT on A and an ENTRY on B with the same direction, speed and screen position.
- No effect words (transition, dissolve, wipe, ramp, slow motion) inside the prompt body.
- At least one hand-or-product insert per 3-5 shots, one still beat per 10-15 s.
- Camera speeds and distances written in numbers.
