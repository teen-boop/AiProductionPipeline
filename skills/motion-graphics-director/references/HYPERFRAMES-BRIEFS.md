# HyperFrames briefs: launch films, logo animations, 20 styles

A library of complete briefs for motion graphics built in code with HyperFrames (HTML + GSAP rendered to MP4). Every name,
product, colour and line in this file is invented sample data. Replace it with the project's own brand, facts and fonts.

Source: a tutorial on making launch videos and logo animations with Claude Code and HyperFrames (2026-11). Its main lesson:
a one-line request gives centred text in default colours. A long, sectioned brief and several render-and-critique rounds give
a studio-grade film.

## Contents
1. The eight sections of a brief, and why each one matters
2. BRIEF-LAUNCH: 20 s product launch film (full sample)
3. BRIEF-LOGO: 6 s logo animation (full sample)
4. BRIEF-LOGO-VARIANTS: two more concepts in the same chat
5. BRIEF-LOGO-AUTO: let Claude invent the logo idea
6. BRIEF-WRITER: get a model to write the brief for you
7. BRIEF-TEMPLATE: blank template
8. STY-01 to STY-20: twenty style briefs
9. How to use this library in our projects (binding notes)

---

## 1. The eight sections

| Section | What it fixes | Must contain |
|---|---|---|
| PRODUCT (or TOPIC, BRAND) | What the film is about | One-line description, the promise, the features or points in order |
| STORY | Structure and the throughline | Scene order, ONE visual thread that never leaves the screen, how each scene turns into the next, the ending |
| FORMAT | Technical target | Size and aspect, fps, exact length, file type (plus an alpha version for logos) |
| LOOK | Taste | The feeling in one line, exact hex for background, text and ONE accent, named fonts per role, what to avoid |
| MOTION | Life | Camera always moving, real depth (3D tilt, soft shadows, far blur), real motion blur, readability |
| SOUND | Feel and sync | Music and every effect made in code, BPM, scene changes on the beat, one sound per action on its exact frame |
| QUALITY CHECK | Quality | Render, look at a frame every 0.5 s (0.25 s for logos), critique as a senior motion designer, fix, repeat 4+ rounds, log each round |
| RULES | Autonomy | Do not stop to ask, make every decision, deliver the MP4, confirm sound, list fixes per round |

The two sections that change the result most:
- **STORY: "every scene transforms into the next, nothing fades or cuts"** plus one throughline object (a line, a shape, a colour)
  that ends as part of the logo.
- **QUALITY CHECK: the multi-round self-critique.** The first render is a draft. Quality comes from rounds 2 to 5.

---

## 2. BRIEF-LAUNCH (sample: a note-taking app called Loop)

```
Create a 20 second launch video for a note taking app called Loop, using HyperFrames.

PRODUCT
- Loop is a note taking app for busy people who write notes and never look at them again.
- Promise: your notes come back when you need them.
- Show three features in this order:
  Capture: get a thought down in seconds.
  Connect: related notes link themselves.
  Resurface: old notes come back at the right moment.

STORY
- Hook, three features, logo. You design the scenes and write the words.
- One idea runs through the whole video: a single red line that never leaves the screen.
  It ends as the loop in the logo.
- Every scene must transform into the next one. Nothing fades or cuts. For example
  the logo opens into the app, or a headline melts into the logo.
- No scene may be a headline on the left with a card on the right.
- End on the "loop" wordmark, a short tagline and a small "Available now" label.

FORMAT
- 1920x1080, 16:9, 60 fps, exactly 20 seconds, exported as an MP4.

LOOK
- Premium and calm, like a launch film from a top design studio. Lots of empty space.
- Background #F2EFE9, text #15140F, one accent color only, red #E5432D.
- The final logo scene flips to a dark background, #141413, with a soft red glow.
- Headlines in Instrument Serif. App text in Geist. Small labels in Geist Mono.
- Build the app screens in code so they look like a real, finished product.
- Avoid: gradients, stock icons, more than one accent color, anything that looks like a template.

MOTION
- The camera is always moving slowly. Nothing sits frozen on screen.
- Give it real depth: tilt the app window in 3D, soft shadows, blur on things far away.
- Real motion blur like a film camera: render extra in-between frames and blend them.
- Keep app screens big enough that every word is easy to read.

SOUND
- Make the music and every sound effect in code. No stock files, no samples.
- Soft, warm, minimal music at about 100 beats per minute. Scene changes land on the beat.
- A sound for every action: typing, lines drawing, notes landing, the logo.
- Every sound sits on the exact frame of the thing it belongs to.

QUALITY CHECK
- When the first version is done, render it and look at a frame from every half second.
- Critique it the way a senior motion designer would: story, layout, spacing, type, timing,
  depth, readability, and whether the sound matches the picture.
- Fix everything you find, render again, and critique again.
- Do at least four full rounds before you consider stopping. After each round, write
  down what was weak and what you changed.
- After that, keep going until a full critique finds nothing left to fix and it looks
  perfect and premium, like a senior motion designer made it. There is no limit on rounds.

RULES
- Don't stop and don't ask me anything. Skip any approval steps and make every
  decision yourself.
- When it's finished, give me the final MP4, confirm it has sound, and list what you
  fixed in each round.
```

---

## 3. BRIEF-LOGO (sample: the Loop wordmark)

```
Create a premium 6 second logo animation for a note taking app called Loop, using HyperFrames.

BRAND
- Loop is a note taking app where your notes come back when you need them.
- The feeling: calm, smart, premium.

LOGO
- Design the logo first, then animate it.
- A lowercase wordmark: loop. Clean rounded strokes, all the same thickness.
- The two o's are one continuous line, like a loop that never ends. That line is red.
- The l and the p are near black.
- It must still read clearly when it is tiny.

IDEA
- A note leaves and comes back around. One red line travels away, curves back and
  closes into the loop. The animation must physically become the logo.
- Do not fade or scale the logo into view.

TIMING
- 0 to 1s: a single red dot appears and starts to move.
- 1 to 3s: it draws one line that travels out across the frame and curves back.
- 3 to 4.5s: the line closes into the two o's. The l and the p are drawn from the same line.
- 4.5 to 6s: the logo settles in the exact centre. The tagline "Notes that come back around."
  is written out underneath. The last second is completely still.

LOOK
- Background #F2EFE9, logo #15140F, accent red #E5432D. No other colors.
- Tagline in Instrument Serif.
- Lots of empty space. The logo takes up about a third of the width.
- Avoid: light streaks, particle bursts, glowing outlines, lens flares, 3D spins, gradients.

MOTION
- One continuous movement from the first frame to the last. No cuts.
- The line starts fast and lands soft, with a tiny overshoot when the loop closes.
- Real motion blur on the fast part of the line.

SOUND
- Make every sound in code. No stock files.
- A soft pen sound while the line draws, a gentle click when the loop closes, and one
  warm low note under the final logo.
- Every sound sits on the exact frame of the thing it belongs to.

FORMAT
- 1920x1080, 16:9, 60 fps, exactly 6 seconds, exported as an MP4.
- Also export a second version with a transparent background, so I can place it over
  other videos.

QUALITY CHECK
- Render it and look at a frame from every quarter second.
- Critique it the way a senior motion designer would: the logo shape, spacing, centring,
  the path of the line, the timing, and whether the sound matches the picture.
- Fix everything you find, render again, and critique again.
- Do at least three full rounds. Then keep going until a full critique finds nothing left
  to fix and it looks perfect and premium, like a senior motion designer made it.

RULES
- Don't stop and don't ask me anything. Skip any approval steps and make every
  decision yourself.
- When it's finished, give me both files, confirm the MP4 has sound, and list what you
  fixed in each round.
```

The idea that makes a logo animation work: **the animation physically becomes the logo** (a line that closes into a letter, a
shape that folds into the mark). Never fade or scale a finished logo into view.

---

## 4. BRIEF-LOGO-VARIANTS (send in the same chat after BRIEF-LOGO)

```
create another 2 variations, completely different logo look, idea, and timing. Make one 3 seconds long and the other 4 seconds long
```

In the sample, this produced a 3 s concept and a 4 s concept, each with a different idea. Use it to give the client a choice of three.

---

## 5. BRIEF-LOGO-AUTO (replace LOGO, IDEA and TIMING in BRIEF-LOGO with this)

```
IDEA
- Come up with your own idea for how the logo appears. Pick one strong concept that fits
  the brand, and make the animation physically become the logo instead of fading it in.
- Design the logo yourself if I haven't given you one, and keep it simple enough to read
  when it is tiny.
- Choose the timing yourself, but keep the last second completely still on the finished logo.
```

Re-run it as many times as you like to get a different concept each time.

---

## 6. BRIEF-WRITER (paste into any chat model, fill in the first line)

```
I want to make a motion graphics video with Claude Code and HyperFrames. Here's what it is: [describe the video, the product or topic, and roughly how long it should be]. Write me a detailed prompt for it with these sections: PRODUCT (or TOPIC), STORY, FORMAT, LOOK, MOTION, SOUND, QUALITY CHECK and RULES. Be specific: exact hex colors, named fonts, how each scene turns into the next, what the camera does, and what sound plays on each action. In QUALITY CHECK, tell Claude to render it, look at a frame every half second, critique it like a senior motion designer, fix everything and repeat for at least four rounds. Avoid anything that looks like a template.
```

---

## 7. BRIEF-TEMPLATE

```
Create a [length] second [type of video] for [product, brand or topic], using HyperFrames.

PRODUCT
- [What it is and who it's for, in one line.]
- Promise: [the one thing the viewer should remember].
- Show [number] [features or points] in this order: [list them].

STORY
- [The structure, for example: hook, three features, logo.] You design the scenes and write the words.
- One idea runs through the whole video: [a visual thread, like a line, a shape or a color].
- Every scene must transform into the next one. Nothing fades or cuts.
- End on [the logo, a call to action or a final message].

FORMAT
- [1920x1080, 16:9 or 1080x1920, 9:16], 60 fps, exactly [length] seconds, exported as an MP4.

LOOK
- [The feeling, for example: premium and calm, or loud and playful.]
- Background [hex], text [hex], one accent color only, [hex].
- Headlines in [font]. Body text in [font].
- Style: [any style from section 8, for example: glassmorphism].
- Avoid: [anything you don't want, for example: gradients, stock icons, anything that looks like a template].

MOTION
- The camera is always moving slowly. Nothing sits frozen on screen.
- Give it real depth: soft shadows, blur on things far away.
- Real motion blur: render extra in-between frames and blend them.

SOUND
- Make the music and every sound effect in code. No stock files.
- [Music style] at about [number] beats per minute. Scene changes land on the beat.
- Every sound sits on the exact frame of the thing it belongs to.

QUALITY CHECK
- Render it and look at a frame from every half second.
- Critique it the way a senior motion designer would: story, layout, spacing, type, timing,
  readability, and whether the sound matches the picture.
- Fix everything you find, render again, and critique again. Do at least four full rounds.

RULES
- Don't stop and don't ask me anything. Make every decision yourself.
- When it's finished, give me the final MP4 and list what you fixed in each round.
```

---

## 8. Twenty style briefs

Short on purpose: the style name alone changes the result a lot. For a polished film, drop the style into BRIEF-TEMPLATE.
To any of them add the review loop line:

### REVIEW-LOOP line (append to any style brief)
```
Then render it, look at a frame from every half second, critique it like a senior motion designer, fix everything you find and repeat for at least three rounds.
```

| ID | Style | Good for | Signature move |
|---|---|---|---|
| STY-01 | Particles | channel intro, title | thousands of particles swirl into the name, then scatter as the camera pushes through |
| STY-02 | Liquid morph | app explainer | one glossy blob morphs object to object, no hard cuts |
| STY-03 | Holographic | product reveal | iridescent product built in code, labels float in one at a time |
| STY-04 | Neon glow | event promo, vertical | neon tubes draw the text on a wall with a flicker as each lights |
| STY-05 | Wireframe 3D | how it works | object assembles part by part while the camera orbits, labels snap in |
| STY-06 | Glassmorphism | app UI showcase | frosted cards over a blurred background, camera drifts across |
| STY-07 | Kinetic typography | quote reel | each word moves, scales or flips in on the beat, one key word in accent |
| STY-08 | Isometric | process explainer | a small isometric world, one glowing object travels through the steps |
| STY-09 | Clay 3D | friendly brand intro | squishy bouncy mascot crosses rounded clay hills to the logo |
| STY-10 | ASCII art | developer tool launch | terminal types, ASCII art builds character by character, logo resolves from text |
| STY-11 | Gradient mesh | podcast intro | slow flowing mesh gradients settle behind a clean serif name |
| STY-12 | Comic book | feature announcement | three panels, halftone, thick outlines, the camera moves panel to panel |
| STY-13 | Split-flap | stats reveal | departure-board flaps clatter to each number, sound on every flip |
| STY-14 | Retro VHS | throwback ad | scan lines, colour bleed, tracking glitch, chunky chrome text |
| STY-15 | Halftone | history explainer | magazine pages of halftone dots slide across with big year labels |
| STY-16 | Bauhaus | data visualisation | circles, squares and triangles build the bars on a strict grid |
| STY-17 | Pixel art | milestone celebration | pixel character runs a level, banner drops with pixel confetti |
| STY-18 | Blueprint | product breakdown | white line drawings on blue grid, exploded view with measurements |
| STY-19 | Art deco | invitation | gold geometric lines and fans draw themselves and frame the text |
| STY-20 | Neo-brutalism | social announcement | flat blocks with thick borders and hard shadows slam into place |

### STY-01 Particles (channel intro)
```
Create a 10 second YouTube channel intro for a space channel called Orbit Lab, using HyperFrames. Style: particles. Thousands of tiny white particles drift in from a black background, swirl together into the channel name, hold for a beat, then scatter as the camera pushes through them. One accent color, cool blue #4DA3FF. 1920x1080, 60 fps, with a soft whoosh and a low synth swell made in code.
```
### STY-02 Liquid morph (app explainer)
```
Create a 15 second explainer for a budgeting app called Penny, using HyperFrames. Style: liquid morph. One glossy green blob morphs into a wallet, then a pie chart that splits into spending categories, then a checkmark with the line "Know where every dollar goes." Off white background, smooth organic motion with no hard cuts. 1920x1080, 60 fps, soft bubbly sounds made in code.
```
### STY-03 Holographic (product reveal)
```
Create a 12 second product reveal for a smart ring called Halo, using HyperFrames. Style: holographic. The ring is built in code and spins slowly in a dark space with iridescent, color shifting reflections. Three thin labels float in beside it, one at a time: sleep tracking, heart rate, 7 day battery. End on the name. 1920x1080, 60 fps, airy shimmering sound made in code.
```
### STY-04 Neon glow (event promo, vertical)
```
Create a 10 second vertical promo for a Friday night gaming tournament, using HyperFrames. Style: neon glow. Glowing pink and cyan tubes draw the event name, the date and "$500 prize pool" onto a dark brick wall, with a soft flicker as each one lights up. 1080x1920, 9:16, 60 fps, electric buzz and a punchy beat made in code.
```
### STY-05 Wireframe 3D (how it works)
```
Create a 20 second explainer on how a drone flies, using HyperFrames. Style: wireframe 3D. A white wireframe drone assembles itself part by part on a black background while the camera orbits it. Label the motors, the propellers, the battery and the flight controller as each part snaps in, then show the propellers spinning up. 1920x1080, 60 fps, soft mechanical clicks made in code.
```
### STY-06 Glassmorphism (app UI showcase)
```
Create a 15 second showcase for a weather app called Skye, using HyperFrames. Style: glassmorphism. Frosted glass cards float over a soft blurred sky: today's forecast, an hourly strip and a rain alert, each sliding in with depth and soft shadows while the camera drifts across them. Build the app screens in code so they look like a real product. 1920x1080, 60 fps, gentle ambient music made in code.
```
### STY-07 Kinetic typography (quote reel, vertical)
```
Create a 12 second vertical quote video, using HyperFrames. Style: kinetic typography. The quote "You don't need more time. You need fewer things." appears word by word, with each word moving, scaling or flipping into place on the beat. Bold sans serif, black text on cream, with one key word in red. 1080x1920, 9:16, 60 fps, a minimal beat at 110 BPM made in code.
```
### STY-08 Isometric (process explainer)
```
Create a 20 second explainer showing how an online order gets from checkout to your door, using HyperFrames. Style: isometric. A small isometric world with a phone, a warehouse, a delivery van and a house. A glowing parcel travels through each step while the camera glides along with it, and a short label appears at each stop. Soft pastel colors. 1920x1080, 60 fps, playful sounds made in code.
```
### STY-09 Clay 3D (friendly brand intro)
```
Create a 10 second intro for a dog walking app called Wagly, using HyperFrames. Style: clay 3D. A soft claymation style dog mascot bounces in, picks up a leash and trots across rounded clay hills toward the app logo. Warm, cheerful colors and squishy, bouncy motion. 1920x1080, 60 fps, cute boing and footstep sounds made in code.
```
### STY-10 ASCII art (developer tool launch)
```
Create a 15 second launch video for a command line tool called Forge, using HyperFrames. Style: ASCII art. The whole video is made of green monospace characters on black: a terminal types the install command, ASCII art of an anvil builds itself character by character, and the Forge logo resolves out of scrolling text. 1920x1080, 60 fps, keyboard clicks and a low hum made in code.
```
### STY-11 Gradient mesh (podcast intro)
```
Create an 8 second podcast intro for a show called Slow Money, using HyperFrames. Style: gradient mesh. Soft, slowly flowing mesh gradients in deep blue and warm orange fill the frame, then the show name fades up in a clean serif and the gradients settle behind it. Calm and premium. 1920x1080, 60 fps, a warm piano chord and a soft swell made in code.
```
### STY-12 Comic book (feature announcement)
```
Create a 15 second feature announcement for a to-do app's new "focus mode", told as a three panel comic, using HyperFrames. Style: comic book. Panel one: a stressed character buried in notifications. Panel two: they tap focus mode with a big "CLICK!" sound effect. Panel three: calm, with the feature name in a bold speech bubble. Halftone shading, thick outlines, the camera moves panel to panel. 1920x1080, 60 fps, punchy comic sound effects made in code.
```
### STY-13 Split-flap (stats reveal)
```
Create a 12 second year in review video for a small business, using HyperFrames. Style: split-flap, like an old airport departures board. Rows of flaps clatter and flip to reveal the numbers one at a time: 2,400 orders, 1,100 new customers, 98% five star reviews. End on "Thank you" flipping into place. 1920x1080, 60 fps, mechanical flap sounds made in code that sync to every flip.
```
### STY-14 Retro VHS (throwback ad)
```
Create a 15 second retro ad for a coffee brand called Morning Fuel, styled like an 80s TV commercial, using HyperFrames. Style: retro VHS. Scan lines, color bleed, a tracking glitch at the start, chunky chrome text, a spinning coffee cup and a cheesy "Wake up to something better!" tagline. 1920x1080, 30 fps, a synth jingle and tape hiss made in code.
```
### STY-15 Halftone (history explainer)
```
Create a 20 second history of the smartphone, using HyperFrames. Style: halftone, like a printed magazine. Four eras of phones, from a brick phone to a modern smartphone, each in bold halftone dots with a big year label, sliding across like pages of a magazine. Limited palette: black, cream and one red. 1920x1080, 60 fps, paper and page turn sounds made in code.
```
### STY-16 Bauhaus (data visualisation)
```
Create a 15 second animated chart showing a company's revenue growing over five years, using HyperFrames. Style: Bauhaus. Bold circles, squares and triangles in red, yellow and blue build the bars, then stack and rearrange into the final number. Strict grid, flat colors, clean geometric type. 1920x1080, 60 fps, rhythmic percussion made in code, with a hit on every bar.
```
### STY-17 Pixel art (milestone celebration, vertical)
```
Create a 10 second celebration for a fitness app when a user hits a 30 day streak, using HyperFrames. Style: pixel art. A tiny pixel character runs across a retro game level, collects 30 coins, then a "LEVEL UP: 30 DAY STREAK" banner drops in with pixel confetti. 1080x1920, 9:16, 60 fps, 8-bit chiptune sounds made in code.
```
### STY-18 Blueprint (product breakdown)
```
Create a 20 second breakdown of how a mechanical keyboard works, using HyperFrames. Style: blueprint. White technical line drawings on a deep blue grid. The camera zooms into one key, and the keycap, switch, spring and circuit board separate into an exploded view with measurement lines and labels. 1920x1080, 60 fps, a satisfying key clack and soft drafting sounds made in code.
```
### STY-19 Art deco (invitation)
```
Create a 12 second animated invitation for a New Year's Eve gala, using HyperFrames. Style: art deco. Gold geometric lines and fan shapes draw themselves on a black background and frame the event name, date and dress code in elegant deco type. Slow, luxurious motion. 1920x1080, 60 fps, a jazzy brass sting made in code.
```
### STY-20 Neo-brutalism (social announcement, vertical)
```
Create a 10 second vertical announcement for a design tool launching a free plan, using HyperFrames. Style: neo-brutalism. Chunky blocks of flat yellow, pink and black with thick borders and hard drop shadows slam into place, with oversized text: "NEW", "FREE PLAN", "Start today". Snappy, confident motion. 1080x1920, 9:16, 60 fps, punchy click and thud sounds made in code.
```

---

## 9. How to use this library in our projects (binding notes)

1. **Fill the template from the project, never from the samples.** Brand facts, hex colours and fonts come from the project's
   brand files or site (`motion-style-core`). A number on screen needs a source; otherwise say what happens, not how much.
2. **Fonts are chosen per style** (cinematic pairing plus one accent). Default sans and serif families on everything read as
   cheap. Test each font at its real size in a snapshot before the full render.
3. **RULES "do not ask" covers free code renders only.** Any paid generation (images, AI video, voice) still waits for the
   user's yes, with the cost stated. References are approved before any video.
4. **Self-critique rounds are mandatory for every motion piece**, even when the brief does not ask for them: frames every 0.5 s
   (0.25 s for logos) on a contact sheet, a written critique per round, at least three rounds, a log of what changed.
5. **Prefer briefs where something physically becomes the result** (a line closes into the mark, parts fold into the logo,
   flaps flip into the word). Fades, slides and glows on flat type were rejected as "template" in real projects.
6. **When a style needs real 3D** (product hero, lacquer or metal object, mirror floor, light sweeps), build it with
   `code-motion-catalog` (three.js) instead of CSS 3D; use these briefs for story, timing, sound and the critique loop.
7. **No long dashes** (em or en) in any on-screen text.
8. HyperFrames contract still applies (`hyperframes` skill): every timed element is a clip, one paused timeline, no
   `Date.now()` or unseeded random, `npx hyperframes check --json` before render, transparent logo version via
   `render --format mov` (ProRes 4444).
