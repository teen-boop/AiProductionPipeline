# Product and explainer animations built in code (three.js)

Code-built 3D motion graphics: no generator credits, no model drift, the real product shape and colour every frame.
Use them for a product hero shot, a lock-up, a numbers board or a "how it works" explainer, and cut them into an ad
or a presentation next to the AI-generated shots.

## The kit (`kit/`)
- `lib/stage.js` STAGE kit: one clock (`S.seek(t)` builds the whole frame for time t), accumulation rendering (motion blur,
  true depth of field, soft area shadows, anti-aliasing), bloom, filmic / neutral / AgX tone, vignette, grain, a code-built
  light environment, a real mirror floor, canvas textures, text planes, `K.track` / `K.path` / `K.spring`, seeded `K.rng`.
- `lib/sound.js` SOUND kit: synthesized Web Audio score (ticks, whooshes, dings, beds, pads), the same call plays live in the
  player and renders offline for the MP4.
- `player.html?style=<file>` loads three.js 0.187 (import map), the kits and `styles/<file>.js`; play / scrub / sound.
- `render.mjs` headless Chrome with GPU:
  - `node render.mjs stills <style> <dir> 0.5,2,4` storyboard stills at 16 samples;
  - `node render.mjs video <style> <out.mp4>` every frame at full samples, sound mixed at -15 LUFS.
- Copy `kit/` into the project (`04_EDIT/product3d/`), write the style in `styles/`, never edit the kits.

## Workflow (always)
1. Content block first: product finishes / rows / layers, copy lines, the schedule (times shared by picture and sound).
2. Storyboard: 3-6 stills from the real scene code, notes per beat (time, exact text, what moves, camera, sound), list of
   assumed facts and numbers. Wait for the user's OK.
3. Render MP4, look at frames, fix framing and legibility (phone first), then cut it into the edit.
4. `update(t)` sets the whole scene for t: no `Math.random`, no `Date`, nothing that builds up between calls.

## Styles

### Studio Product (family: products and screens)
- **Look:** one product in a near-black seamless studio on a black mirror floor, carved out of the dark by strip softboxes,
  one restrained line of type beside it.
- **The idea that makes it work:** the product stays still and the LIGHT is the story. A graded key strip sweeps across it
  four times while its colour runs through a day; a counter or clock ticks with the light and lands inside the lock-up line.
- **Build:** a softbox rig computed per pixel (each box is a rectangle of light with size, distance, angle, power, colour,
  feather; reflections stay crisp on metal and wide on matte paint); every part is a turned profile `[radius, y, fillet]`
  with real fillets, because the thin bevel is what catches the strip light. Finishes: powder coat with orange-peel bump,
  turned steel with lathe-line bump, wood from a canvas grain texture, rubber / silicone with a light coat.
- **Camera:** one continuous `K.path` move: macro pass 1 (cap / collar), macro pass 2 (the mark), pull back to the whole
  product left of centre, slow push still moving on the last frame. Focus follows its own path; the aperture closes as it
  pulls back.
- **Adapting to a new product:** replace the profile list and finishes from the approved product card, keep the rig, the
  studio and the camera grammar. A debossed mark = a slightly darker, glossier alpha patch just proud of the wall.
- **Pitfalls seen:** a two-line lock-up at 150 px runs off a 1920 frame; keep lines under ~1050 px (128 px Inter 600).
  Never invent a product claim for the counter: a clock of the day works when there is no verified number.

### Split-Flap Board (family: flat content made physical)
- **Look:** a mechanical departure board at night, black flaps with worn off-white print in a dark steel frame, one amber row
  for the point that matters, a back-lit amber header.
- **Motion:** every cell rattles forward through a fixed drum order (`' A..Z0..9.-/%:'`) until it lands, column after
  column, row after row; the flap accelerates as it falls (`angle = PI * frac^1.6`).
- **Build:** one glyph atlas, four instanced half-flap meshes (top static, bottom static, falling front, falling back) with
  a per-instance glyph attribute; instance colour lerps to amber on the hero row after it lands.
- **Camera:** close and sideways on the first rows, one pull-back, gentle push to the hero row. For phone viewing end with
  the board filling about 85% of the frame width.
- **Rules:** names <= 10 columns, values right-aligned; the hero row is the claim. Every number on the board needs a source.

### Layer Stack (family: diagrams with depth)
- **Look:** a stack of thin frosted glass sheets with white printed diagrams, aqua edge glow, dark plinth, satin floor; one
  amber for the answer.
- **Motion:** the closed block opens top first (each sheet on a damped spring, a little overshoot); labels draw in as each
  sheet settles; a white bead drops through the same pad on every sheet (each flashes), climbs back in amber, and the result
  appears on the top sheet.
- **Build tricks:** glass that keeps full-strength reflections while the body is nearly clear (shader patch on
  `opaque_fragment`); glass shadows by randomly discarding shadow texels per sub-render (light for bare glass, dark for print);
  labels on a camera-facing group on render layer 1 so the floor does not mirror them.
- **Explainer rule:** the picture tells the story, words are small labels; end on the result, not a slogan.
- **Use for:** any process or stack: a pipeline, a tech stack, a product teardown (one sheet per layer).

### Pass Explode (family: diagrams with depth)
- **Look:** one rounded footage card floating in a warm near-black void; it opens into a stack of render passes behind it
  (depth grey, position magenta-to-violet, wireframe solve, blue point cloud), each with a small dark label chip.
- **The idea that makes it work:** every pass is generated from the SAME source in the shader (one depth map, one subject
  matte), so the silhouettes line up across all cards and the stack reads as "the same shot, seen as data".
- **Motion:** the card yaws to about -35 deg and pitches 8 deg in 0.55 s while the passes slide back along its normal on
  damped springs (stagger 0.05 s, spacing about 0.55 card widths); labels land 0.6-1 s apart, each with a red glow sweep;
  the stack telescopes back into one card (0.6 s, ease in) and lands on the next shot with a rim flash.
- **Build tricks:** SDF rounded-rect shader for mask, 1 px rim and outer glow in one pass (the plane is bigger than the
  card to leave room for the glow); point cloud = Points sampled from the same depth, pushed TOWARD the camera, additive,
  size by depth, drawn after its own card; wireframe = a grid bent by depth in the shader. Labels are a 2D overlay placed
  by projecting each card's corner, in a staircase (front card highest) with a thin leader line, so they never overlap.
- **Camera:** aims at a point about a third of the way into the open stack (so it stays centred while opening and
  closing), backs off as it opens, slow truck (about 3% of frame width per second) while open. The collapse is the cut.
- **Pitfalls seen:** the glow margin has uv outside 0..1; `pow()` of a negative there returns NaN, which blooms into a
  white blob over the whole stack: clamp uv before the scene function. Passes from different sources never line up and
  kill the idea; more than 5 cards becomes a slide deck; labels on the cards themselves get mirrored and skewed.
- **Use for:** a footage-to-data explainer, a VFX or AI pipeline step, "what is inside this shot".

### Lens Portal (family: transitions)
- **Look:** a 2D card shrinks inside a closing dark iris with a red ring; the iris IS the glass of the product's lens, so
  the next frame is that lens with the card still glowing inside it, then a fast pull back to the whole product. Reverse
  version: a crash zoom into the lens whose bokeh becomes the next logo or icon.
- **The idea that makes it work:** on the switch frame the iris radius equals the projected radius of the lens glass
  (set the camera distance from it: `dist = glassR / (irisR * tan(fov / 2))`), the iris ring sits at the real ring's
  radius and is as thin, and the lens glass shows the same crop of the card as an emissive map that fades in 0.2 s.
  Nothing else may appear on that frame: the studio lights, the other lenses and the body highlights come up only
  during the pull back.
- **Motion:** iris close 0.6 s ease in; hold 0.12 s; pull back 0.9 s ease out expo (FOV 20 to 35 deg, to the product at
  about 70% of frame width); slow push to the end; the red rings light one by one (0.1 s apart) under the headline.
- **Build tricks:** the iris is a full-screen quad inside the scene (vertex shader ignores the camera, drawn last); after
  the switch the same quad draws radial speed lines (`fract(atan(p) * 90 / TAU)`, masked by radius) with strength = camera
  speed; accumulation motion blur does the rest.
- **Pitfalls seen:** iris and glass differing by more than about 3% in radius shows the cut; a thick, bloomed iris ring
  against a thin real ring shows it too; lights already on at the switch make the neighbours pop in.
- **Use for:** moving between footage / UI worlds and the product, product-to-app handover, a reveal of a logo from a lens.

### Glass UI Explainer (family: products and screens)
- **Look:** the software's panels as dark frosted glass floating in 3D in a warm void (two blurred colour orbs behind them):
  hairlines, small UI text, data drawn as glowing warm particles and soft glow bars; one red accent for the active state.
- **The idea that makes it work:** one continuous camera take through the UI instead of screen recordings: dive into the
  timeline, pull back to the window, slide onto the node panel, end on the export pill, so the product logic reads as a
  place.
- **Motion:** beats every 0.5-1.5 s (a playhead wipe, the tab underline, inputs fusing into a node, a progress pill);
  camera moves 0.8-1.0 s ease in-out between slow drifts (`K.track` with a drift key after every move). During the dive
  the camera rides with the playhead so the wipe stays in frame.
- **Build tricks:** every panel a canvas texture at 384 px per unit on a plane; data wave = Points inside a waveform
  envelope, brighter where the playhead has passed; fuse lines = `K.tube` with a growing draw range (whole rings only);
  a lit node = an outline glow (canvas stroke with shadow blur, additive), never a fill over its label; glow bars =
  gradient times soft side falloff pushed above 1 for bloom; export pill = SDF pill with a fill and two cross-faded labels.
  A long list can sit on a rotating cylinder with brightness by cos(angle).
- **Pitfalls seen:** framing the whole window on the first try cuts its edges, keep about 10% air; real UI text below about
  18 px at 1080p is unreadable on a phone, keep only the labels that carry the story; no invented numbers on sliders.
- **Use for:** software or pipeline explainers, "how the app works" chapters, feature lists.

## Cutting a code animation into an ad
- Studio Product is the hero / end card; a 2-4 s slice of the lock-up replaces a generated product still.
- Split-Flap and Layer Stack are explainer inserts for presentations and landing pages.
- Render at the edit's frame rate; keep the grade of the generated shots in mind (the code pieces are darker and cleaner,
  so use them at section changes, not mid-scene).

## Sample files in `kit/styles/`
| File | Style | Sample content | Length |
|---|---|---|---|
| `studio-product.js` | Studio Product | TIDE, an invented steel bottle with a bamboo cap and silicone loop; the light is the clock, dawn to dusk | 8 s |
| `split-flap.js` | Split-Flap Board | what an AI production pipeline does at each stage; the last row is the claim in amber | 8 s |
| `layer-stack.js` | Layer Stack | how a brief becomes an ad: six glass sheets, a bead down and back, the result on the top sheet | 9 s |
| `pass-explode.js` | Pass Explode | a dusk street plate (built in the shader) opening into depth, position, solve and point cloud, landing on the next shot | 6 s |
| `lens-portal.js` | Lens Portal | a night-street card swallowed by the middle lens of an invented five-lens sensor bar, pull back to the product | 3.2 s |
| `glass-ui.js` | Glass UI Explainer | an invented editing app: timeline dive, tab change, fuse node, export pill, red-lead words | 9 s |

Each file = content block + schedule + build(S) + sound(k). A new piece usually changes only the content block and the
product profile; keep the look, the light and the camera grammar.

## Using the pieces in a longer edit (learned on a presentation for a landing page)
- **3D chapters as breathers.** Fast HTML / montage blocks (0.3-1.6 s shots) with full 3D chapters (7-9 s) between them:
  the contrast is what makes the edit feel expensive. Open on a 3D macro (no text) for 3-4 s, then cut to fast kinetic type.
- **Slices for short cuts.** In a 20-25 s cut use the last 2-2.5 s of a board (the hero row landing) and a 1.5x speed
  slice of a layer stack (the pulse going down and back).
- **End card.** The studio lock-up replaces a flat end card; for 9:16 / 1:1 / 4:5 render a no-text pass (`NO_TEXT=1`),
  crop on the product and set the type in the edit (object-position computed so the product is centred:
  `p = (x_product * W_scaled - W_window / 2) / (W_scaled - W_window)`).
- **Sound.** Each 3D chapter keeps its own score; a synthesized bed (`score-template.html` + `score.mjs`) runs under the fast
  blocks and steps back (pad, low gain) under the 3D chapters; a whoosh into every flash cut, a hit on it, one hit per
  kinetic word, a shutter per frame in a frame burst, clicks when clips snap onto a timeline. Mix with ffmpeg
  (`adelay` per chapter, `amix normalize=0`, `loudnorm I=-14`).
- **Three worlds, portals between them.** A launch film can alternate a studio product world, a footage / data world and a
  UI world; switch worlds through a portal (Lens Portal, a crash zoom, a Pass Explode collapse) or on a music hit, never
  with a plain dissolve.
- **Red-lead word reveal.** For small lines: the newest word arrives in the accent colour and turns white when the next word
  lands (0.15-0.35 s later); one tick per word. It gives reading rhythm without big type (sample in `glass-ui.js`).
- **Studio Product extras.** Lenses or LEDs that light up one by one (emissive rings + bloom, a blip per light) make a
  calm end shot; a 3/4 top view on a 12 deg turntable carries a feature list.
- **Boards never carry made-up numbers.** Without a source, rows say what happens (AUTO, LOCKED, CHECKED); only the
  sourced claim gets a number.
