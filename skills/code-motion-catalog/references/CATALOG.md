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
- **Boards never carry made-up numbers.** Without a source, rows say what happens (AUTO, LOCKED, CHECKED); only the
  sourced claim gets a number.
