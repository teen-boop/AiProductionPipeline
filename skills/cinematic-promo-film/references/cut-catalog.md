# Cut catalog - cinematic transitions for a promo film

A generated promo is assembled from many 4-5 s clips that were never shot together. The cut is where the audience
decides whether it is one film or a slideshow. Most cuts in a good promo are **plain cuts placed well**; the special ones
below are spices.

## Choosing rules

1. **Plan the cut before generating.** A match cut or a whip only works when both clips were prompted for it. Write the
   transition into the shot list for the outgoing and the incoming shot.
2. **One family per film.** Pick a transition family that fits the look (organic: light flash, focus, occlusion; kinetic:
   whip, motion match; classic: match cut, dip). Mixing families reads as a template.
3. **At most one or two effect transitions per 30 s.** Everything else is a cut on action, a cut on a look, or a hold.
4. **Cut on movement, hold on meaning.** Cut while something moves; hold when the feeling needs to land (the payoff, the
   claim).
5. **Sound leads.** In a promo the sound of the next shot often arrives before its picture (J cut). That alone makes most
   cuts feel intentional.
6. **Count frames, not seconds.** At 24 fps a flash is 2-4 frames, a whip blur 4-6 frames each side, a dip 8-16 frames.

## The catalog

### Cut on action
- **What:** cut in the middle of a movement; the movement continues in the next shot from a new angle or size.
- **When:** most cuts in the setup and turn; hands, steps, a lid opening, a pour.
- **Prompt both sides:** the outgoing clip ends mid-action; the incoming start frame shows the same action slightly later,
  same direction of travel, same side of the line.
- **Build:** cut about 2-3 frames after the motion peak in the outgoing shot; start the incoming shot so the action
  overlaps by 1-2 frames.
- **Avoid:** crossing the 180-degree line; a hand that changes side.

### Match cut on shape
- **What:** a round thing becomes another round thing in the same screen position (a pupil to a lens, a moon to a watch
  face, a coffee surface to a vinyl record).
- **When:** world-to-product transitions, metaphor concepts, the turn.
- **Prompt both sides:** state the shape's position and size in frame explicitly in both prompts ("a circle centred,
  filling one third of frame height"); same camera height; similar tonal value.
- **Build:** align in the edit with a small scale or position nudge (under 5 %); a 2-frame soft cut is allowed.
- **Avoid:** shapes that only match at one size; if you need more than 10 % correction, regenerate.

### Match cut on motion
- **What:** the direction and speed of movement carries across the cut (a swing left becomes a car turning left).
- **When:** energetic launches, montages in the turn.
- **Prompt both sides:** same screen direction, same speed adjective, same lens length feel.
- **Build:** cut at peak velocity on both sides; motion blur should be similar.
- **Avoid:** reversing screen direction without a reason.

### Graphic match on colour or light
- **What:** a dominant colour or light shape continues (a red brake light becomes the red product cap).
- **When:** brand colour moments, transitions into the packshot.
- **Prompt both sides:** name the exact colour (hex from the style card) and where it sits in the frame.
- **Build:** a plain cut; a 2-4 frame cross-dissolve only if the luminance differs.

### Whip pan
- **What:** a fast camera pan blurs out of one shot and into the next.
- **When:** changing location with energy; hiding a cut between two generated clips.
- **Prompt both sides:** outgoing clip ends with "camera whips fast to the right, heavy horizontal motion blur";
  incoming clip starts "camera arriving from a fast whip from the left, motion blur resolving". Same direction.
- **Build:** keep 4-6 blurred frames each side; add a directional blur in the edit if the generated blur is weak; match
  blur strength at the cut frame; a short whoosh in sound design, only if motivated.
- **Avoid:** more than two whips per film; whips in a calm, elegant concept.

### Light flash
- **What:** a burst of light (a lens flare, a practical turning on, sun through a gap) whites out the frame for a moment.
- **When:** the turn, the reveal, time jumps, a hidden cut in a continuous-move concept.
- **Prompt both sides:** outgoing ends with a light source flaring toward the lens (warm, in the style card's palette);
  incoming starts overexposed and settles.
- **Build:** 2-4 frames peak, tinted to the practical's colour, never pure digital white; exposure ramp 4-6 frames in and out.
- **Avoid:** using it as a default; on a dark, moody film more than one flash cheapens it.

### Dip to black
- **What:** fade to black, a beat of darkness, fade up.
- **When:** before the brand moment; between chapters in 60-90 s films; after the hook if the setup is a new world.
- **Build:** 8-16 frames out, 0-12 frames of black, 8-16 frames in. Pair with a silence or a held note.
- **Avoid:** dipping inside the turn; it kills momentum.

### Smash cut
- **What:** an abrupt cut from quiet to loud (or the reverse), picture and sound together.
- **When:** the hook, the turn in a contrast concept.
- **Build:** hard cut on the frame; the sound changes on the same frame with no fade.
- **Avoid:** using it twice; the second one is never a surprise.

### Focus pull transition
- **What:** the outgoing shot racks out of focus to soft bokeh; the incoming shot starts soft and racks in.
- **When:** elegant concepts, emotional beats, the world-to-product fold.
- **Prompt both sides:** "focus racks to the background until the subject is fully soft, oval anamorphic bokeh" and the
  reverse for the incoming start.
- **Build:** cut at the softest frame of both clips, ideally on bokeh of similar colour; 2-6 frame dissolve allowed.

### Occlusion wipe
- **What:** a foreground object (a passer-by, a pillar, a hand, a door edge) crosses the lens and fills the frame; the cut
  hides inside it.
- **When:** continuous-move concepts, location changes.
- **Prompt both sides:** outgoing ends with a dark foreground element crossing close to the lens left to right; incoming
  starts with a similar element leaving frame left to right.
- **Build:** cut on the frame where the frame is fully covered; match the occluder's tone.

### Push-in to cut
- **What:** a slow push toward a detail, cut at the end of the push to the next scale (detail to macro, or macro to wide).
- **When:** the hook to the setup; the payoff into the packshot.
- **Build:** cut just before the push decelerates.

### Jump cut (same framing)
- **What:** same framing, time skips forward.
- **When:** a craft or day-in-the-life concept to compress a process; energetic social cutdowns.
- **Prompt:** keyframe chain with locked camera, the subject state changed between frames.
- **Avoid:** in elegant concepts; it reads as an error unless it repeats as a pattern (three or more).

### J cut and L cut
- **What:** J cut: the next shot's sound starts before its picture. L cut: the current sound continues over the next picture.
- **When:** whenever VO, dialogue or a strong product sound exists; the default for joining story beats.
- **Build:** lead by 6-18 frames; for VO, a sentence may start on the outgoing shot and finish on the incoming.

### Sound bridge
- **What:** one continuous sound (a heartbeat, a ticking, rain, an engine) carries across several cuts and ties them.
- **When:** montage in the turn, the continuous-move concept.

### Cross-dissolve
- **What:** both images overlap briefly.
- **When:** only for time passing or memory. Keep under 12 frames unless the dissolve itself is the image.
- **Avoid:** as a default join; it is the most obvious sign of a template edit.

### The hold
- **What:** no cut; the shot plays to completion.
- **When:** the payoff and the claim. In a 30 s film at least one shot should run 3 s or more.

### The cut to the brand moment
- **What:** the last transition, from story to claim and logo.
- **Options:** cut to a held packshot and lay the claim over it; dip to black and bring the claim up on black; a light
  flash that resolves into the logo card. Choose one that matches the family.
- **Build:** leave 6-12 frames of pure image before the first letter appears; the logo appears on or just after a musical
  downbeat; hold the logo at least 1.5 s; the last frame is a held frame, not a cut on the final note.

## Edit checklist

- Every special transition was planned in the shot list on both sides.
- No more than two effect transitions per 30 s; one family only.
- No screen-direction flips without a reason; the 180-degree line holds.
- At least one hold of 3 s or more; the claim is readable twice.
- J and L cuts used wherever sound can lead.
- Each cut checked frame by frame in the encoded file (`render-cut-verification`).
