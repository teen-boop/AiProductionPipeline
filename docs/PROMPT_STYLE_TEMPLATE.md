# Prompt blocks for hand-generated frames

Assemble every PROMPT.txt from these blocks, top to bottom. Drop a block that
does not apply (e.g. no character in frame). Prompts are always in English,
even when the user works in another language.

## 1. REFERENCES — what each attached image means
```
The FIRST attached image is the locked LOCATION — stage the scene inside exactly this place (same architecture, objects and light), ignore any text or equipment in it. The other attached images are the identity references for the hero.
```
Variants:
- Object or vehicle lock: `The attached image is the locked look of the <ship/car/creature>.`
- Change-to: `The FIRST attached image is the START frame — change to <a closer shot / a few seconds later> of the SAME moment: same place, light, colour grade, same people.`
- Recreate a composition: `The FIRST attached image is the COMPOSITION reference only — keep its framing, pose, action, setting and mood, but replace the person with our hero and fix everything to the project's period and look.`
- Recreate an archive photo: `The FIRST attached image is a real historical black-and-white photograph — recreate it as a COLOUR frame of a modern period feature film: keep its composition, viewpoint, subject and moment.`

## 2. SCENE (written per frame)
```
<Place>, <date and time of day>, <weather/light>: <who> <does one clear action>, <what is around>. <Shot size and angle — wide / medium / close-up / detail; where the camera is>. <What is sharp, what is soft in front and behind>.
```
For two different shots in one job: `Image 1 — …` / `Image 2 — …`.

## 3. CHARACTER LOCK (per character, with the right age)
```
The hero is <NAME> at age <N> — keep EXACTLY the face of the attached identity references for age <N>: same face shape, eyes, nose, mouth, ears, hairline and hair; <facial hair>. <Costume>.
REALISTIC FACE: a real human face photographed on film — visible pores, natural skin texture and tone variation, fine lines, slight natural asymmetry, natural catchlights. NOT airbrushed, NOT waxy, NOT plastic, NOT CGI. He/She never looks into the camera.
```

## 4. DOMAIN LOCKS (project-specific — keep them in the project's style template)
Examples: a hero object that must stay accurate (counts, colours, markings); period accuracy (`only objects, clothes, vehicles, buildings and technology that existed in <year>`); a night or weather lock; a recurring animal.

## 5. LOOK + OPTICS (always)
```
LOOK: a still frame from a high-end 35mm period feature film shot on a real location — practical, motivated light, real weathered textures, natural imperfect skin, real crowds with varied faces, ages, builds and postures, clothes that are worn and creased; atmospheric haze and depth. NOT a glossy AI illustration, NOT a poster, NOT a catalogue pose, nobody poses for the camera, no plastic faces, no over-sharpened HDR, no centred symmetrical hero pose.

OPTICS: vintage anamorphic cinema lenses, shallow depth of field — subject sharp, foreground and background soft — an out-of-focus foreground element close to the lens on wider shots, atmospheric haze for distance, never the miniature/tilt-shift look; vertical oval bokeh and flares ONLY from real visible light sources; daylight exteriors have no floating bokeh discs. Organic 35mm film grain. ARRI camera, Cooke lenses, 50mm dominant, 75mm for close-ups, subtle handheld tension. Cinematic premium theatrical grade, gritty but beautiful. Ultra realistic.
```
Never write "deep focus". It flattens the image into the miniature look.

## 6. FORMAT (last)
```
Full-bleed 16:9, no black bars, no vignette, no rounded corners, no borders, no captions, no text, no watermark. No visible film camera, crew or modern equipment. Generate exactly <ONE single photograph | 2 variations, each ONE single photograph — not a grid, not a collage>.
```

## Reference attach order — cheat sheet
| Frame type | ref_1 | ref_2… |
|---|---|---|
| Character in a known location | location master frame | identity refs (right age) |
| Character, no location ref | identity bust | identity turnaround |
| Hero object / vehicle | object lock frame | identity refs if a character is present |
| Close-up / next moment (change-to) | the start frame | identity refs |
| Recreate a reference picture | that picture | identity refs / object lock |

## Common failures and the block that fixes them
- Glossy AI poster, posing people → LOOK.
- Everything sharp, toy-like → OPTICS (shallow DOF, haze, foreground element).
- Bokeh discs in daylight → "bokeh ONLY from real visible light sources".
- Duplicate hero object (e.g. two identical ships) when the character stands on it → "only ONE <object> in frame" + put the camera on it.
- Black bars, rounded corners → FORMAT (intake.py also crops thin bars).
- Face drift → attach the identity refs and repeat the age in the text.
