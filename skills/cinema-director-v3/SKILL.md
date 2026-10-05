---
name: cinema-director-v3
description: "Cinema director v3 for Seedance 2.0/2.5 and Higgsfield video prompts. Supersedes earlier cinema-director versions — prefer this one. Establishes the target Seedance version first, since 2.0 caps at 9 image references and 15 seconds while 2.5 allows 50 and 30. Writes production-grade multi-shot prompts on a locked 16-slot spine: shot header, Style Prefix, NO ON-SCREEN TEXT, CRITICAL blocks, Assets, Geometry Map, First Frame, lens locks in FOV degrees, Camera, Light and Colour, Atmosphere, timecoded Action Timing, Physics, Acting, Audio, and a Locks chain. Covers 8K photoreal capture, true-gravity physics, source-bound atmosphere, a dialogue protocol that stops the model inventing its own lines, microphone-proximity audio, hardened music suppression, and the lipsync protocol for attached tracks. Use whenever the user wants a Seedance or Higgsfield video prompt, a music video shot, a dialogue or performance scene, a lipsync sequence, an action sequence, or asks to break a scene into shots for video generation."
---

# Cinema Director v3 — Seedance 2.5 / Higgsfield Prompt Grammar

Every prompt is a production document. Who is in frame, what they look like, where they stand in depth, what they do, how gravity acts on them, how it is filmed, what the air does, what is heard, and what must not drift.

**The model is a physics engine, not a mood board.** It renders what it can see, count, and weigh. Mood words evaporate.

**If a word does not produce a visible pixel or an audible sound, cut it.**

---

## STEP ZERO — TARGET VERSION CHECK

**Establish the target engine before writing a single block.** Two hard ceilings differ between versions, and both change the architecture of the prompt, not just its trim.

| | Seedance 2.0 | Seedance 2.5 |
|---|---|---|
| **Image references** | 9 maximum | 50 maximum |
| **Maximum runtime** | 15 seconds | 30 seconds |

**If the user has not stated the version, ask once, in one line, before prompting.** Do not guess. A 2.5-shaped prompt fed to 2.0 loses references silently and truncates; a 2.0-shaped prompt on 2.5 leaves half the identity budget unspent.

Once stated, it holds for the session unless the user changes it.

### What changes on 2.0 (9 refs / 15s)

Reference slots are scarce, so every slot is contested. Characters first in narrative order, then one shared group wardrobe sheet, then props, then the environment plate, then video or audio last. Collapse where you must: a prop that only needs to read approximately can live inside a character's Asset description instead of taking a slot. Anything past 15 seconds splits into two prompts.

### What changes on 2.5 (50 refs / 30s)

Reference slots stop being scarce, which changes strategy rather than just raising a number:

- **Multi-angle identity.** A character can carry a front reference, a profile, and a detail plate rather than one composite sheet. Identity holds far harder across a long take.
- **Wardrobe, prop and environment references separate cleanly.** No more collapsing a prop into a character line.
- **Every group member gets an individual reference** instead of sharing one corps wardrobe sheet.

**More references is not automatically better.** Every reference must do distinct work. Near-duplicate references blend and produce an averaged face, and a cluttered reference set drifts worse than a tight one. If two references would teach the model the same thing, ship one.

**Long-form 2.5 (16–30s) needs extra anti-drift weight**, because drift compounds with runtime:

- One **anchor reference** held and named across every beat
- The **lens lock declared at the top of every beat**, not just at the head of the prompt
- **Geometry Map restated** at any point the staging materially resets
- **Locks carries the full ordered chain**, every link, no abbreviation

**Runtime available is not runtime required.** A 30-second ceiling does not mean 30-second prompts. Two camera vantages on the same action are still two prompts on 2.5 — that split is about coverage, not about the cap.

---

## WRITE THE VISIBLE

| Instead of | Write |
|---|---|
| she looks stressed | shoulders lift, jaw locks, exhales through the nose, eyes fix on the door |
| the alley feels dangerous | one buzzing bulb 30 metres back, wet brick, standing water, no other figures |
| fast chase | carves through traffic at 110 km/h, leg dragging outside the lane line on turn-in |
| she looks tall next to him | she stands 183cm to his 168cm |
| heavy mech | five-ton mass, cratering the ground on landing |

**Measurables the model reads:** speed in km/h · height in cm · mass in kg or tons · atmosphere as density plus named depth planes · direction as screen-relative or character-relative (always labelled) · emotion rendered in muscle · contact rendered as deformation.

---

## LENGTH DISCIPLINE

A four-shot sequence with four assets lands at **900–1,400 words**. Past that the CRITICAL blocks lose weight against the descriptive body. Every line is a lock, not a flourish.

**Every fact lives in exactly one slot.** Wardrobe lives in Assets and is never re-described in Action Timing — Action Timing names a garment only when it is doing something visible (a hem swinging, hair whipping clear). Light lives in slot 10. Atmosphere lives in slot 11. A prompt that repeats itself reads long without reading specific, and the duplicate dilutes the original.

---

## DELIVERY

Three parts, nothing else:

1. **Bolded title with runtime** — `**Underground garage — entry walk — 8s**`
2. **Numbered reference list** in attach order — max 9 images on 2.0, max 50 on 2.5, plus one video/audio slot
3. **One fenced code block** containing the whole prompt, English only

No preamble, no post-amble. Flag a conflict in one or two lines above the title if one exists.

**A NEGATIVE PROMPT block ships as an optional second code block** — only when the scene has a known drift risk (mixed character designs, locked spatial geometry, identity swaps) or when asked. Group it by failure category, comma-separated, no sentences.

**Iterations deliver directly.** Any tweak to an approved prompt — palette, framing, pose, lens, lighting, wardrobe, staging, duration — ships as the revised full prompt, no confirmation bullets. Re-check only on full scope change: new scene, new character set, new capture family.

**Always ship the full prompt.** Never partial swaps or "replace this line" unless a targeted patch is requested.

**Split rather than overload.** Two camera vantages on the same action are two prompts regardless of version. Anything past the target's runtime ceiling — 15s on 2.0, 30s on 2.5 — is two prompts. Say so and deliver both.

---

## THE SPINE (LOCKED ORDER)

```
1.  HEADER              shot count · runtime · timecodes · cut policy · speed policy
2.  STYLE PREFIX        the invariants — style, operating style, texture, skin, technical
3.  NO ON-SCREEN TEXT   mandatory, always here, never lower
4.  CRITICAL BLOCKS     scene-specific, cap 4
5.  ASSETS              @tag = identity + THIS SCENE action + fidelity assertion
6.  GEOMETRY MAP        absolute frame position and depth planes
7.  FIRST FRAME         what is already happening at frame one
8.  OPTICS              lens lock in FOV degrees, per shot
9.  CAMERA              physicality register and behaviour
10. LIGHT & COLOUR      direction, quality, temperature + the percentage doctrine
11. ATMOSPHERE          air density, depth planes, source-bound vapor
12. ACTION TIMING       timecoded beats, hard cuts inline
13. PHYSICS             mass, deformation, rebound, lag, contact
14. ACTING              face, eyes, brow, liveness
15. AUDIO               diegetic default, or attached-track sole source
16. LOCKS               positive ordered chain of what must hold
```

No mode label. No prose between blocks. No aspect ratio.

---

## SLOT 1 — HEADER

```
4 shots. Total 8 seconds — shot 1 runs 0.0–2.0s, shot 2 runs 2.0–4.0s, shot 3 runs 4.0–6.0s, shot 4 runs 6.0–8.0s. Hard cuts between them, no transitions, no dissolves. All shots real-time, no slow motion, no overcranking, no ramping, no speed change anywhere in this sequence.
```

Single take: `1 continuous shot. Total 10 seconds, no cuts, no transitions. Real-time throughout.`

Timings sum exactly. **Maximum 15 seconds on 2.0, 30 seconds on 2.5.**

Runtime guide: 1.5–2.5s per shot for high-energy cutting · 2.5–4s for narrative and dialogue beats · 4–7s for a held lipsync line · 8–15s for a continuous take.

**Past 15 seconds (2.5 only), the header also declares the shot budget** so the model does not compress the whole sequence into the first third: `9 shots across 24 seconds` reads very differently from `24 seconds`. Long sequences hold better when built as a chain of 2.5–4s beats than as one unbroken take.

**Slow-motion accents are carved out explicitly**, both where they land and in the closing clause: `Brief slow motion on the impact only, 2.0–2.5s. All other footage real-time.`

If cuts must never land mid-word: `the cuts fall between words and never inside a word.`

---

## SLOT 2 — STYLE PREFIX

The invariant capture stack. Labelled lines, front-loaded, never restated later.

```
Style: 8K, photorealism, real organic film grain and halation, high dynamic range, shot on large-format film. NOT a 3D render, NOT a game engine, NOT a game-cutscene aesthetic, NOT a cartoon, NOT anime cel-shading.

Operating style: large-scale realism with intimate handheld closeness, immersive in-camera feel, tactile textures, shallow depth of field on the face, documentary framing, photochemical look.

Texture: matte non-reflective surfaces, lived-in worn materials, organic 65mm film grain, no digital gloss, no plastic sheen.

Skin: pore-level realism — visible pores, fine vellus hair, natural asymmetry, no smoothing, no retouching. Half the face often falls into shadow.

Technical: 8K, real-time 24fps, true 180-degree shutter with a real 1/48 second exposure on every frame, genuine photographic motion blur, each frame blending smoothly into the next. Smooth stable motion, no flicker, no warping, no morphing, no frame interpolation, no frame blending, no ghosting, no double-imaging, no high-shutter video crispness.
```

**The render quad is mandatory and always four items:** `NOT a 3D render, NOT a game engine, NOT a game-cutscene aesthetic, NOT a cartoon.` Add `NOT anime cel-shading` when the material is stylized enough to invite it.

**The cadence clause lives in Technical and nowhere else.** It is the single most important anti-artifact instruction in the prompt, which is why the Style Prefix sits second.

**Strobe quarantine.** When the scene contains strobe or hard flashing light, append to Technical:

```
The stepped, stuttering quality of this sequence comes entirely from the strobe lighting described below — from bodies revealed only in discrete flashes — and never from broken or choppy footage. The camera motion between flashes stays continuous and smooth even while bodies appear to jump between positions.
```

Without the quarantine the model returns genuinely broken footage.

**Named-DP shorthand is permitted and efficient.** `Operating style — HOYTE VAN HOYTEMA:` carries large-format realism, intimate handheld, in-camera feel, atmospheric depth and photochemical rendition in three words. Use a DP whose signature actually matches the scene; never stack two.

---

## SLOT 3 — NO ON-SCREEN TEXT

Mandatory in every prompt, always in this position. Overlay text is generated early in the frame, so the instruction sits early.

```
NO ON-SCREEN TEXT — CRITICAL: no on-screen text of any kind anywhere in frame at any point. No captions, no subtitles, no burned-in dialogue, no auto-captions, no karaoke text, no lower thirds, no titles, no title cards, no credits, no watermarks, no logos, no timecode, no UI overlays, no social-media overlays, no interface elements, no Chinese characters, no Korean characters. The frame is clean of all overlay graphics from first frame to last.
```

**Never carve out in-world text inside this block.** No "other than," no "except for." An exception clause reopens the door and captions return. Physical text that genuinely exists in the scene — garment prints, packaging, signage, a split-flap board — is described separately in Assets or Geometry Map as a physical object with shape, colour, placement and legibility.

Weight it hardest on phone, selfie and talking-head prompts, which pull captions straight from social training data.

---

## SLOT 4 — CRITICAL BLOCKS

Any element the model routinely drops, softens or gets wrong is promoted out of the descriptive body into its own ALL-CAPS named block here.

Format: `THE [THING] — CRITICAL:` followed by one exhaustive paragraph.

| Block | Use when |
|---|---|
| `THE SCRIPT` | any spoken dialogue the model generates — first block, top content priority |
| `THE SINGING` | any lipsync to an attached track — first block, top content priority |
| `THE MOUTH IS ALWAYS VISIBLE` | any lipsync, paired with the above |
| `THE GEOMETRY` | a spatial relationship must not invert (above/below, inside/outside) |
| `THE STAGING` | who stands where must not drift |
| `THE STROBE` / `THE LIGHT CHANGE` | flashing, pulsing, or lighting that shifts mid-take |
| `TWO DISTINCT DESIGNS` | two similar objects or characters that must never merge |
| `NOBODY ELSE IS IN THE FRAME` | any scene that must be empty of extras |
| `EVERYONE IS LIVE` | dialogue or group scenes where backgrounded bodies freeze |
| `THE TONE` | comedic or emotionally specific scenes that could be misread |
| `THE LANGUAGE` | foreign-language dialogue |
| `THE BEAT` | the dramatic point of the shot is a specific reversal |

**Cap at four.** Past that they compete and all of them dilute. Order by importance — early text carries more weight.

Each block is exhaustive within itself. Never split one idea across two. **The block is the instruction; downstream slots only apply it.** Never restate a CRITICAL block in full further down.

---

## SLOT 5 — ASSETS

Every asset is one line: **tag, permanent identity, THIS SCENE action, fidelity assertion.** This merges what used to be a separate identity lock and per-shot action line into a single non-repeating unit.

```
@Image 3 = 177cm, dark bob with blonde balayage ends, centre part, warm fair skin. Navy short-sleeve polo, grey micro-shorts, olive suede wide belt, barefoot. Clean clear face, no beauty marks, no facial markings. Voice strict and focused, mezzo-soprano. THIS SCENE: seated centre of the sofa, speaking, irritation sliding into teasing surprise. 100% match to the reference.
```

**Target 60–110 words per character asset.** Tight enough that five assets don't swamp the prompt.

**Identity components, in order:** height in cm · build and skin · face and bone structure · hair colour, length, styling · permanent markers · makeup · clean-face negations · wardrobe head to toe, one clause per garment · jewellery and nails · voice descriptor · THIS SCENE · fidelity assertion.

**Wardrobe is restated every prompt but written economically.** One clause per garment: colour, fabric, cut, how it sits.

- ❌ *a long-sleeved charcoal-grey cropped top in soft washed matte jersey with a faded mineral-dyed finish, high round neckline, long slim sleeves fitted to the wrist, hem sitting just below the ribcage, the back left open*
- ✅ *a cropped charcoal washed-jersey long-sleeve, high round neck, open back, hem just under the ribcage*

**Permanent features are declared permanent** — `the blunt bangs are permanent and present in every frame`.

**State-conditional identity is declared with its state and its reason** — `no horns in this scene, omit them entirely for continuity, horns are battle-state only`. This prevents the model splitting the difference.

**Known-drift attributes get an inline anti-drift negation** — `BROWN eyes, never blue, never green`.

**Clean-face negations are explicit.** The model invents facial detail otherwise.

**Skin lock:** warm fair or as specified, `rendering true and natural, never cool-shifted, never pale porcelain, never tan`.

**Reference scoping.** State what a reference governs and what it does not:

```
@Image 1 = the location — high-walled ruined city canyon, decayed grey towers, collapsed slabs, debris-littered ground. Controls geography, materials, atmosphere and light direction only.
```

**Group and crew assets** get one shared block: the full uniform, the permitted variation range (`some wear a sheer mesh layer, some have bare arms`), and the anonymity lock (`every masked face identical in styling, no dancer ever unmasked`).

**Prop assets** carry material, scale relative to a hand or body, hardware, finish, how it is held. Scale is the one that fails: `a 20cm combat knife, noticeably shorter than the mech's 40cm forearm — it reads short, not a sword`.

**Reference ordering:** characters first in narrative order, then group wardrobe sheet, then props, then environment plate, then video/audio last. Every character gets its own slot even if visible inside the environment plate — the plate carries world, the sheet carries identity. Renumber cleanly if a reference is added; never leave a stale index.

**On 2.0 the ordering is a rationing scheme** — nine slots, so collapse anything that only needs to read approximately into a neighbouring Asset line. **On 2.5 it is purely a reading order**, and characters can carry multiple angles each. Keep the same sequence either way so the numbering stays predictable.

---

## SLOT 6 — GEOMETRY MAP

Where everything sits in the frame and in depth. **This is the block that stops bodies drifting between cuts.**

```
GEOMETRY MAP: on the dark-green L-sofa — the woman with the black hair and brown eyes on the LEFT, the woman with the dark bob in the MIDDLE, the woman with the ashy-blonde shag on the RIGHT. A beanbag pouffe front-right, in front of the blonde. Windows and corkboard on the wall behind, thrown soft. Depth planes: sofa foreground, standing figure mid-ground, window wall background.
```

**Three things every geometry map states:**

1. **Absolute lateral position** — LEFT, MIDDLE, RIGHT, and what is off-frame in which direction
2. **Depth plane per subject** — foreground, mid-ground, background, and which planes are sharp and which fall soft
3. **Vertical relationship where it matters** — ABOVE, BELOW, inverted, suspended, and never let it invert

**Screen-relative and character-relative direction are always labelled.** `she turns to her OWN right` is not `screen-left`. Pick one per instruction and name it; unlabelled direction inverts about half the time.

**Naming who the frame favours resolves ambiguous framing** — `three-quarter angle, off-centre, favouring the woman in the middle`.

**A locked spatial relationship gets promoted to a CRITICAL block** and defended in the negative prompt. Vertical inversions and above/below pairs are the most drift-prone geometry there is.

**Scatter over lines.** When several figures share a frame, place them at different depths rather than side by side: `scattered at different depths, NOT in a row`. Line-ups read as posed group photos.

---

## SLOT 7 — FIRST FRAME

One or two lines. What is already happening at frame one.

```
FIRST FRAME: already mid-sprint toward the first creature, blade in hand, the others spread around at different depths. No empty establishing frame, no static hold before the action starts.
```

The empty establishing frame is a default the model volunteers and it costs half a second of an eight-second clip. Kill it explicitly. When the reference image is the intended opening composition, say so: `open on the composition of @Image 1 exactly, already in motion`.

---

## SLOT 8 — OPTICS

**The house default is spherical large-format.** Clean glass — natural halation around highlights, creamy focus falloff, subtle lens breathing, natural 180-degree motion blur. **No anamorphic streak flares, no oval bokeh, no artificial flares, no fisheye** unless the user asks for anamorphic by name.

Anamorphic is opt-in per prompt. When requested, state it once here and let the closing Locks carry it.

### FOV degree anchor

The model latches onto **degrees** as a snap value; millimetres read as suggestion. Write the degree first, mm in parentheses. Never use an off-ladder value.

| FOV | mm | Feel | Use for |
|---|---|---|---|
| 180° | fisheye | spherical bulge | POV, dream state, hallucination |
| 107° | 14–16mm | architectural ultra-wide | vast interior scale, epic establishing |
| 84° | 20–24mm | classic wide | full-body blocking, immersive action, environmental establish |
| 63° | 28–35mm | reportage wide | observational, walking alongside, doc feel |
| 47° | 40–50mm | eye-level neutral | universal medium, two-shot, waist-up |
| 34° | 60–70mm | short tele | compressed group, stacked depth planes |
| 29° | 75–85mm | portrait compression | isolated bust, detail on hands, tight coverage |
| 18° | 100–135mm | portrait tight | identity-hold close-up, held emotional beat |
| 12° | 180–200mm | tele detail | hand insert, object close, jewellery, texture |
| 8° | 300–400mm | extreme long lens | anchored-far observation, watchtower |

### Lens lock per segment

```
LENS LOCK SHOT 1 = 84° (22mm) classic wide, low, the sprint immersive.
LENS LOCK SHOT 2 = 29° (80mm) short telephoto, detail on the hands.
LENS LOCK SHOT 3 = 47° (50mm) standard normal, side angle, the swing readable.
No focal drift mid-shot.
```

**Unusual FOVs need a defense battery.** A long lens will be averaged back toward a normal unless you name what it is not:

```
This is a LONG lens — strong telephoto compression, flattened perspective, background pulled in close and thrown soft, only one to three faces sharp at a time, tight crop. NOT wide-angle, NOT large-format coverage, no fisheye, no edge distortion, no deep focus, no full-room coverage.
```

Same in reverse for ultra-wide. **Extreme FOV across several beats drifts fastest** — declare the FOV at the top of every beat, repeat it in Locks, and hold one anchor reference across every beat.

---

## SLOT 9 — CAMERA

Pick one register and hold it. Register governs cant, cut rate, and how much of the frame is allowed to be still.

| Register | Cant | Cuts | Language | Frame |
|---|---|---|---|---|
| **Locked-off** | 0° | 1–2 shots or a oner | tripod-weighted, or an extremely slow push | long held frames, stillness is the subject |
| **Gentle handheld** | 3–10° | 3–5 shots, 2.5–4s | floating, drifting, riding breath, small organic corrections | frames settle and hold before moving on |
| **Heavy handheld** | 12–25° | 4–6 shots, 1.5–2.5s | jolting, bobbing, lurching, snapping corrections, high-frequency vibration underneath | every frame mid-move, the eye can still land |
| **Violent handheld** | 25–45° | 4–6 shots, 1.5–2s | punching in and ripping back, whip-pans, hard surges, violent corrections | nothing settles, the frame never lands |

**Deduce the register from the description; ask only if genuinely split.** Toward locked-off and gentle: grief, memory, waiting, ritual, solitude, portrait, dialogue that matters, "quiet," "still," "slow," "elegant." Toward heavy and violent: a beat drop, choreography, a chase, a fight, a crowd, a crash, a named BPM, "chaotic," "aggressive," "hard," "go crazy."

**Every register except locked-off closes with:**

```
never locked, never stabilized, never mechanically smooth, never gimbal-glide, never floaty drone — real shoulder-mounted mass, weight shifts, breath, human over-correction, every frame mid-move but always smooth and continuous in its own travel.
```

That last clause is load-bearing. Without it, violent handheld returns broken footage rather than energetic footage.

**Dutch cant is a swinging range in degrees** plus `never passing through level, never settling square`.

**Roaming coverage** — a camera that physically travels between subjects — is stated as an explicit behaviour with what it snaps to: `roams between them and zooms onto details, snapping to a singing mouth, a jumping pair of legs, flailing hands, a laughing face, then drifting to the next`.

**A Tier 1 subject inside a Tier 4 camera is a real choice** — a still figure while the camera tears around her. State the split explicitly so the model does not average the two.

---

## SLOT 10 — LIGHT & COLOUR

**Light is described by direction, quality and temperature. Never by fixture name.** No named lamps, no stock codes, no LogC4, no IRE.

```
LIGHT: motivated natural light, one soft key from camera-side and above, soft roll-off, faithful skin tones, no heavy grade. Cool daylight counter-note from the windows behind. Half-faces rolling through shadow as they move.
```

### The colour accent doctrine

Percentages, each nailed to a physical source. This allocates frame area, which a bare palette list does not.

```
COLOUR: ~70% desaturated green-grey room tone and raw concrete; ~20% warm orange-yellow accent from warm daylight and the warm ceiling wash through the netting; ~10% cool daylight blue as a counter-note from the windows.
```

Three bands, roughly 70 / 20 / 10. **Every band names its source.** A colour with no source in frame will not render.

State where blacks sit, what blooms, what flares specular, what holds saturation. Attach every colour to a fabric, a surface or a light source.

---

## SLOT 11 — ATMOSPHERE

**Air is always present. Vapor is always source-bound.**

Real air at real density, filling the entire frame including the foreground — a continuous scattering gradient from lens to horizon, blacks lifted at every depth, high micro-contrast inside the lift.

```
ATMOSPHERE: the air carries real density at every depth — a continuous scattering gradient from the lens to the far wall, blacks lifted at every plane, depth reading in clearly separated layers: [name the actual planes of this shot, nearest to furthest, and how each softens]. Razor skin and fabric texture up close, heavy grain inside the lifted shadows, natural bloom at point light sources. Low macro contrast, high micro contrast. Bodies pass through the air without disturbing it, leaving no wakes and no trails.
```

### The source rule

**Visible vapor shapes only exist when something in frame is physically making them.** Named source, named emission, and nothing anywhere else.

- ✅ *a lit cigarette in her left hand, a thin ribbon of smoke rising off the ember and dissipating within 30cm*
- ✅ *every footfall and impact blasts up dust that blooms and streams off in the wind*
- ✅ *breath condensing in the cold, visible on the exhale only*
- ✅ *steam lifting off the cup surface*

Without a source in frame, close the block:

```
No plumes, no banks, no tendrils, no wisps, no swirls, no rolling, no fog-machine texture, no smoke shapes, no volumetric shafts, no god rays. Nothing in the air is emitted by anything.
```

Naturally foggy exteriors are legitimate — cold morning fog, coastal haze, mist in a ruined city — and read as **uniform density and reduced visibility with distance**, not as shapes moving through frame. Write it as `thick cold fog holding at uniform density, visibility falling off with distance` and keep the shape negations.

**Clean-air scenes state it just as hard:** `the air is clean — no haze, no density, no visible beams, no suspended particulate, full clarity to the back wall`.

**Always name the actual depth planes of the actual shot.** Atmosphere is for depth separation, never for mood.

---

## SLOT 12 — ACTION TIMING

Timecoded beats. Hard cuts on their own line. Every visible body accounted for in every beat.

```
0.0–1.5s (SHOT 1, low charge-leap): sprints at 60 km/h toward the first creature and leaps, rising and driving down, blade in hand, dust torn up beneath.
1.5s HARD CUT
1.5–3.0s (SHOT 2, stomp): comes down and stomps one clawed foot onto the creature's head, crushing it into the ground — skull plate shattering, ichor bursting under the foot, rubble cratering, dust blasting up. Brief slow motion on the impact only, 2.0–2.5s.
3.0s HARD CUT
```

**Silence about a body means it drifts.** Every figure in frame gets an action in every beat, even if the action is small: `in the foreground she shifts and reacts, a small head turn, breathing, listening`.

**EVERYONE IS LIVE.** Backgrounded and foregrounded bodies freeze by default in dialogue scenes. State the counter explicitly: `nobody sits frozen, everyone is reacting throughout`.

**Each figure on her own clock.** For group energy: `each moves differently at her own random timing, deliberately messy, never moving as one`.

**Dialogue is written verbatim in quotes**, with the emotional arc and the physical beat tied to the stressed word:

```
speaks to the woman beside her, lightly teasing without malice: "We've got HER, though." — clear stress on HER — and ON THAT WORD she turns her gaze to her OWN RIGHT and looks and nods directly toward the figure off-camera to her right, a pointed "right there — her" beat.
```

**Synchronized choreography** needs the unison lock plus the anti-mannequin clause: `every dancer hits the same shape at the same moment while carrying her own micro-timing, head angle and limb height inside the count, so the group never reads as identical mannequins`.

**Name four motion layers, always**, even when one is "nothing else moves": character motion · micro-motion (breath, hair, fabric, jewellery) · environmental motion (water, particles, dust) · camera motion, which lives in slot 9.

**Hair and fabric as motion** is first-class on high-energy shots — hair whipping across faces and being pushed clear, fabric lifting and settling, chains swinging with real momentum. It reads as physical truth more than any body description.

---

## SLOT 13 — PHYSICS

True gravity. **The chain is always the same, scaled to the mass in play.**

```
1. Stated mass          — kg, tons, or bodyweight
2. Contact event        — foot lands, body hits, hand grips
3. Deformation          — the receiving surface gives: cushions compress, ground craters, fabric bunches
4. Rebound / recovery   — the surface returns, knees absorb, the body recovers
5. Secondary lag        — hair, loose fabric, cables, hydraulics trail the primary motion
6. Contact shadow       — where the body meets the surface, grounded
7. Closing negation     — nothing floats, nothing slides, nothing teleports
```

Bodyweight scale:

```
PHYSICS: real gravity, inertia and mass — weighted body movement, jumping with real impact and recovery, sofa cushions compressing and rebounding under the jumps, knees absorbing the landings, hair and loose fabric whipping with the motion, accurate contact shadows where feet meet floor and cushion. Nothing floats, nothing slides.
```

Heavy scale:

```
PHYSICS: real five-ton mass — the leap and stomp crush the head with crushing weight, cratering the ground; the swing carries weight into the carapace; the throw follows a true arc with the body's weight; kicks land with heavy follow-through. Hydraulic and cable elements lag the motion. Inside the cockpit the pilot's body and hair jolt with each strike. Bodies tumble with gravity, plates crack and splinter. Nothing floats, nothing teleports.
```

**Effort is physics.** Strain, exhaustion and struggle are rendered in the body, not asserted: `shaking arms, slipping grips, hands slip and catch, the body trembles, boots scrabbling for purchase, hard breathing`.

**Resistance is physics.** A thing that dies or yields does so over time: `it does not die instantly — it thrashes and resists, limbs clawing, before it finally goes limp`.

**Falling debris obeys gravity and is declared harmless** when it should be: `a scatter of pebbles and grit falls past her with real gravity; she is unharmed and keeps climbing`.

**Structures that must hold are declared to hold:** `the rig holds, no fall, no free fall, no snapping cable`.

---

## SLOT 14 — ACTING

```
ACTING: natural eye blinking throughout, active forehead and brow micro-expression, no frozen mask-face, no dead eyes. Forehead and eyebrow movement precisely matches the emotion of each line — brows up on the surprised peaks, scrunching down on the hard belts, foreheads alive throughout.
```

**Brow and forehead matched to the line is the single highest-yield acting instruction.** Faces go slack and generic without it.

**Eyelines are stated as targets** — `they look at each other, never into the lens`. Looking at camera is a strong default and must be suppressed explicitly in observational and documentary work.

**Emotional arcs inside a beat** are written as a slide, not a state: `first slightly irritated, then sliding into teasing surprise`.

**Physical performance negations** where relevant: no mouthed words, no singing, no teeth-baring, unless the scene calls for them.

---

## SLOT 15 — AUDIO

**Default: diegetic only.** Specific physical sounds tied to specific surfaces and materials — footsteps naming the surface, fabric by type, hardware, breath, room tone, environmental ambient.

### The music suppression tail

Every diegetic prompt closes on this, and it is not optional. The model scores anything that looks like content — a conversation, a walk, an emotional beat — unless told not to, and one word of negation is not enough.

```
No music, no score, no lyrics, no singing, no laugh track, no added foley beyond what is physically in frame, no subtitles.
```

Add `no ambient pad, no swell, no drone, no rising tone` on emotional or dramatic material, where the model reaches for underscore hardest. Add `no crowd sound, no chatter, no voices off-frame` on any scene with a population lock, since the model tends to fill an empty exterior with people it did not render.

**Never write song references, lyrics, or track-tied dialogue.** Music is uploaded separately as an audio reference.

**Everything audible names a source in frame.** A sound with no visible cause reads as a mix decision and pulls the model toward scoring. Footfalls name the surface, fabric names its weight, hardware names its material.

**Ambience is named and levelled, not implied.** `Low park ambience — leaves overhead, birds, faint distant traffic` gives the silences something to sit in. An unspecified ambient bed comes back as a pad.

**Silences are assigned to the ambience explicitly** so they do not get scored: `carrying both silences on its own`.

### Proximity-governed dialogue

When speakers hold their own microphones, level is a physical fact, not a mix choice, and it gets its own CRITICAL block:

```
THE MICROPHONE PROXIMITY — CRITICAL: voice level follows mouth-to-microphone distance. Close to the lips a voice is warm and broadcast-present with breath audible on the capsule; lowered, dropped to a lap or swung off-axis by a moving arm it immediately goes thin, distant and roomy with the room audible around it. In this take: [name the exact lines that depart from close and full, and the visible body action causing each]. Everything else is close and full. Transitions are immediate and driven by visible hand movement, never a fade.
```

Name the departures line by line. A general rule with no instances listed produces uniform level.

**Attached-track lock — HARD.** When an audio or video track is attached it is the sole and complete audio source:

```
AUDIO: the attached clip @Video 1 is the sole and complete audio source for this sequence. Generate no additional audio of any kind — no room tone, no foley, no ambience, no breath, no added dialogue, no music.
```

The attached clip also owns all internal timing. Never impose per-beat timing on a lipsync take.

**The unheard-track technique** lets bodies sing without music in the mix:

```
AUDIO: no music in the mix — the track is not audible. Only the voices, loud and a little off-key, singing roughly in time to the unheard 87 BPM beat: "[lyric]". Plus room tone, footfalls, sofa creak, laughter, fabric. No track, no instrumental.
```

**Spoken dialogue is allowed** when a scene has real speech. Line verbatim in quotes, plus delivery physics: mic distance, reverberation, compression, pitch level, accent.

**Non-verbal scenes** state it: `environmental sound and non-verbal effort sounds only — strained grips, hard breathing, an exertion grunt. No spoken words, no dialogue.`

**Slow-motion beats** get their own audio treatment: `slow-motion accents drop ambient under a low pressurized tone`.

---

## SLOT 16 — LOCKS

A positive ordered chain of what must hold. **Not a summary of the prompt** — only what could drift between cuts, phrased as what happens rather than what does not.

```
LOCKS: the sequence runs in order — sprint and leap, stomp the first creature's head into the ground, switch the blade from normal to reverse grip, side-swing kill of a second creature that struggles before dying, throw that body into another, kicks and a blade finish on the rest. Same identity, same blade, same geography and same creature design continuous across all cuts. It reads as genuinely heavy yet fast and brutal. Every shot a different angle and height. Wardrobe identical to each tagged reference, one look per figure, no mixing. Light direction and colour temperature identical across all shots. The air holds uniform density throughout.
```

Standard contents, one line each: **ordered action chain · identity continuity · staging and geometry holds · wardrobe identical to references · permanent markers restated as a short list · environment identical across shots · every shot a different angle and height · light and colour temperature consistent · atmosphere uniform · skin protection.**

**The no-restatement rule.** If a CRITICAL block already locked it, Locks does not repeat it — one clause pointing at it, not a rewrite.

**Skin protection closes the block:**

```
Skin reads true cinematic matte — zero shine on forehead, nose bridge, cheekbones and collarbones, real fine even pore texture, real peach fuzz at the jaw and hairline, real lip surface texture, light absorbed like true subsurface scattering, skin protected and rendering true and natural, never plastic, never doll-skin — no acne, no blemishes, no enlarged or rough pores, fine flattering texture that keeps every face looking good.
```

**The flattering ceiling is locked.** Realism never makes a face look ugly. Where matte-realism and flattering conflict, resolve toward flattering.

**Closing negation tail**, tuned to the scene:

```
No CGI, no rendered look, no digital cleanliness, no plastic surfaces, no AI smoothness, no skin smoothing, no glow, no stiffness, no frozen posing, no stabilized camera, no gimbal glide, no video-look high-shutter crispness, no frame interpolation, no frame blending, no dropped frames.
```

---

## THE DIALOGUE PROTOCOL

**This is for speech the model generates itself. The lipsync protocol below is for speech supplied on an attached track. They are opposites — never mix them.**

Generated dialogue fails one way: the model invents its own lines. It happens when the script is buried in Action Timing at slot 12, competing with four ALL-CAPS blocks above it that never mention speech, while Audio at slot 15 — the slot where speech is actually produced — describes voices but restates no words. The model arrives at generation with a voice profile and no script, so it writes one.

The fix is stating the script **twice, plainly, in the two slots that matter**, and stating it nowhere else in a competing form.

**1. THE SCRIPT is the first CRITICAL block.** Above every other block including staging, geometry and camera. Speaker tags, verbatim lines, in order, with silences marked as beats.

```
THE SCRIPT — CRITICAL: these are the only words spoken in this take. Nothing improvised, added, paraphrased or skipped.

@tag-a: "Okay then what would you do."
@tag-b: "What?"
@tag-a: "Someone's watching this and they wanna make ads that don't suck."
(three seconds of silence — nobody speaks)
@tag-b: "Don't start with the product."

They speak naturally and conversationally at a relaxed pace, the way friends actually talk. Only the speaker's mouth moves — the listener's mouth stays closed or resting, never mouthing along, never forming the other's words.
```

**2. Audio restates the same script verbatim** with per-line delivery attached — proximity, tone, breath state — and closes with the anti-invention clause:

```
AUDIO: fully diegetic. The seven scripted lines above, spoken by the assigned speakers in order, and nothing else — no invented dialogue, no substituted phrasing, no extra sentences.
```

**3. Action Timing carries the line again inside its physical beat**, because that is where mic distance and body action get bound to it. Three statements total is correct here and overrides the no-repetition rule. A fourth form does not help.

**Never write phoneme or mouth mechanics for generated dialogue.** No tongue positions, no jaw-drop descriptions, no lip-rounding, no bilabial closure counts. Those instructions exist to sync a mouth to audio the model already has; when the model is producing the speech, they make it overarticulate, chew its words and deliver robotically. Write the line and the emotional intent, nothing about the face.

**Every non-speaking body gets an explicit silence.** `@tag-b says nothing in this beat:` followed by what she is doing instead. Silence about a listener means the model gives her words.

**Exclusive speech gets its own block when two or more people are in frame.**

```
ONE MOUTH SPEAKS AT A TIME — CRITICAL: each line belongs to exactly one person, and only that person's mouth forms those words. The listener never mouths along, never shadows the syllables, never half-forms the same words, and never looks like the line could be coming from her. Laughing, gasping, sniffing and exhaling are always allowed on the listener; only word-forming is exclusive.
```

Deliberate overlaps and unison lines are carved out explicitly or the model suppresses one speaker: `both mouths form those two words together, in sync, at full volume, both fully visible.`

**Silence is written as a beat with a duration and a filler.** `three full seconds, neither woman speaks and neither mouth forms any word` plus what the ambience carries. Unmarked gaps get filled with invented speech.

**Length discipline is part of this protocol.** A dialogue prompt past roughly 1,200 words drowns its own script — the block stops being loud and starts being one of fifteen things shouting. Cut caveats, cut restated wardrobe, cut anything that does not change a pixel or a sound, before cutting anything from the script block.

---

## THE LIPSYNC PROTOCOL

**For attached-track lipsync only.** When the model generates the speech, use the Dialogue Protocol above instead — the mechanics below actively damage generated delivery.

Lipsync fails for four diagnosable reasons: the lyric was stated abstractly instead of as a score; the mouth got obscured; too many cuts forced per-shot mouth re-initialization; other CRITICAL blocks out-competed the singing instruction.

**1. Promote the singing to the first CRITICAL block.**

```
THE SINGING IS THE PRIMARY SUBJECT — CRITICAL: every other element is secondary. [Description by hair and wardrobe] sings out loud, full voice, mouth open and working hard, for all [X] seconds without stopping. She is a singer delivering a vocal, not a performer mouthing along. Her mouth is the focus of every shot.
```

**2. Write the lyric verbatim, then the mouth mechanics word by word.** Bilabials — **B, M, P** — get maximum emphasis. A visible lip seal is what the eye reads as real lipsync.

```
"TIME" — the tongue taps up behind the teeth on the T, the mouth opens wide on a broad AH travelling into an EE, then BOTH LIPS PRESS FULLY AND VISIBLY TOGETHER AND SEAL SHUT on the M — a complete, unmistakable, hard lip closure with upper and lower lips meeting flat and pressing together, held a beat before releasing.
```

Non-bilabial words still get formation: where the tongue goes, how far the jaw opens, whether lips round or spread, whether teeth touch lip.

**3. State the closure count.** Scan the line for B, M, P — those are the hard seals. F and V are teeth-on-lip, described but not counted. Sustained final vowels are declared held open.

```
THE PATTERN OF CLOSURES: four hard lip seals across the sequence — on the M ending TIME, the M starting ME, the B starting BEEN, the B starting BEFORE — plus a smaller visible closure on the P of UP. Every one of the four is complete, fully visible and unmissable. The mouth is never lazily half-open and never mumbling between them.
```

**4. Lock mouth visibility in its own CRITICAL block.**

```
THE MOUTH IS ALWAYS VISIBLE AND ALWAYS READABLE — CRITICAL: her face is turned toward the lens, her mouth unobstructed, frontal and clearly readable in every single frame of every shot, and it stays readable through the camera movement, through the cant and through every flicker of the light. Nothing ever covers it — no hand, no hair, no arm, no other body.
```

**5. Hand timing to the clip and minimize cuts.** Prefer one continuous take. If cutting, cut between lyric lines or in breaths, never mid-word, and state it in the header.

**Strobe fights lipsync** — hard flash-to-black eats roughly half the closures. When both are wanted, flag it and soften the strobe on the singer only, a fast bright flicker that never drops her face fully to black, while background bodies keep the full treatment.

---

## STROBE GRAMMAR

```
THE STROBE IS THE DEFINING FEATURE — CRITICAL: the space is lit by hard white strobe flashes firing relentlessly on a fast [BPM] pulse. The rhythm is flash, black, flash, black — hard on, hard off, with occasional double and triple stutter runs. Each flash is instantaneous and brilliant, revealing the scene crisply frozen mid-motion, hard-edged and contrasty. Each black interval drops the frame to near-total darkness. No fade in, no fade out, every transition a hard snap. Because the bodies move continuously but are visible only during the flashes, every figure appears to jump between discrete frozen positions. Nothing sits at a comfortable normal exposure at any point.
```

Always pair with: a **secondary light** holding a dim constant glow between hits so forms stay readable in the black · the **cadence quarantine** in Style Prefix · a **continuous-motion clause**: `nothing is ever frozen, held or static between flashes — every body is in continuous motion at all times, it is only the light that stops them`.

**Per-beat light pulsing causes perceived choppiness.** On a report of choppy output, soften the pulse to a slow continuous swell first; if it persists, kill the pulse and go constant.

---

## HOUSE RULES

**No character names anywhere in the prompt body.** Visual descriptors only — hair colour and style, wardrobe, identity markers. Applies universally including staging, geometry and camera lines. Semantic reference tags may alias to a name in the numbered list above the code block, never inside it.

**No aspect ratio.** Set in the UI.

**No internal production context.** No "carried through from the previous scene," no "matching the earlier plate." Every prompt is standalone with everything restated fresh.

**No platform or tool names** in the prompt body.

**No meta-commentary.** Every word describes something visible or audible.

**Age-blind.** Describe by role, hair, wardrobe, identity markers.

**English only inside the code block.** No Simplified Chinese, no bilingual mode.

**Brand names, text and graphics are written verbatim** and described physically alongside — shape, colour, placement, legibility. Naming the thing renders the thing; a paraphrase renders a vague approximation.

**Lighting by direction, quality and temperature only.** Never a fixture name.

---

## STORY BIBLE HANDOFF

When a story bible or canon skill is active, it is the identity and context source and this skill is the cinematography grammar. Pull character voice, movement signature and stillness register into Assets. Pull speech patterns into Audio. Pull aesthetic era and palette into Light & Colour. Layer the bible's production rules on top of House Rules, taking precedence where they conflict.

The bible answers *who and what world*. This skill answers *how it is shot*. Never let bible material leak in as lore or backstory — only as observable physical behaviour. Operate standalone when no bible is present.

---

## PRE-DELIVERY PASS

- [ ] **Target version established — 2.0 or 2.5 — before anything else was written**
- [ ] Reference count within the target's ceiling: ≤ 9 on 2.0, ≤ 50 on 2.5
- [ ] Bolded title with runtime, numbered reference list in attach order, one code block
- [ ] Header timings sum exactly, total ≤ 15s on 2.0 or ≤ 30s on 2.5, speed policy stated
- [ ] Past 15s, shot budget declared and anti-drift weight added (anchor ref, per-beat lens lock)
- [ ] Style Prefix second, render quad present, cadence clause inside Technical
- [ ] NO ON-SCREEN TEXT third, no carve-out clause inside it
- [ ] CRITICAL blocks capped at four, ordered by importance
- [ ] Every character has its own reference slot and its own Asset line with THIS SCENE
- [ ] Fidelity assertion on every asset, reference scoping on the environment plate
- [ ] Geometry Map states lateral position, depth planes, and vertical relationship
- [ ] Direction labelled screen-relative or character-relative
- [ ] First Frame kills the empty establishing hold
- [ ] Lens lock per shot in FOV degrees with mm, unusual FOVs defended
- [ ] Camera register consistent with cut rate and cant, never-settles clause present
- [ ] Colour doctrine in three bands, every band sourced
- [ ] Atmosphere names the actual depth planes; every visible vapor has a source in frame
- [ ] Physics runs the full chain at the right scale, closes with nothing floats
- [ ] Every visible body has an action in every beat
- [ ] Brow and forehead matched to the emotion, eyeline target stated
- [ ] Generated dialogue: THE SCRIPT is the first CRITICAL block, restated verbatim in Audio, and carries no phoneme mechanics
- [ ] Every non-speaking body has an explicit silence in every beat
- [ ] Every silent gap has a stated duration and a named ambience filling it
- [ ] Audio diegetic with the full music suppression tail, or the attached-track sole-source lock
- [ ] Locks is an ordered positive chain, no restatement of CRITICAL blocks
- [ ] Skin protection and negation tail close the prompt
- [ ] No character names, no aspect ratio, no tool names, no mode label
- [ ] Nothing stated twice anywhere

**Repair pass:**

| Symptom | Fix |
|---|---|
| Wardrobe drifting | restate every garment in the Asset, not just the changed one |
| Choppy output | check the cadence clause sits in Style Prefix, then soften or kill any per-beat light pulse |
| Bodies drifting between cuts | tighten Geometry Map, add depth planes and a favours-line |
| Geometry inverting | promote it to a CRITICAL block and defend it in the negative prompt |
| Air reading as fog machine | a vapor has no source in frame — bind it or cut it |
| Figures floating or sliding | the physics chain is missing deformation or contact shadow |
| Background bodies frozen | add EVERYONE IS LIVE and give each an action per beat |
| Lens averaging back to normal | add the not-the-other-thing defense battery |
| Model inventing its own dialogue | THE SCRIPT is not the first CRITICAL block, or Audio never restated the lines verbatim |
| Delivery robotic, overarticulated, chewing the words | phoneme mechanics leaked into a generated-dialogue prompt — strip every mouth instruction |
| Listener mouthing the speaker's words | add the one-mouth-at-a-time block and give every listener an explicit silence per beat |
| Music or underscore appearing | the suppression tail is short — add score, swell, drone and pad by name |
| Invented crowd noise or off-frame voices | ambience unnamed, or the population lock has no audio counterpart |
| Lipsync closures missing | check mouth-visibility block, cut count, and whether strobe is eating the face |
| Extras appearing | add the population lock as its own CRITICAL block |
| Slow motion appearing unbidden | add the explicit no-speed-change line to the header |
| Captions appearing | the text block drifted down, or a carve-out crept into it |
| Long but vague | something is stated twice — find the duplicate and delete the later copy |
| Over the runtime ceiling or overloaded | split into two prompts by camera or by beat |
| References silently dropped | reference count exceeds the target's ceiling — confirm 2.0 vs 2.5 |
| Faces averaging or blending | two references are teaching the same thing — cut one |
| Long take compressing into the first third | declare the shot budget in the header, rebuild as 2.5–4s beats |
| Identity drifting late in a long 2.5 take | add an anchor reference named in every beat, repeat the lens lock per beat |
