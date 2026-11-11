---
name: generation-failure-fixes
description: >-
  A catalogue of recurring image-model failure modes in period/cinematic production, each with its cause and the exact prompt fix that
  worked. Look up a symptom, apply the fix line, regenerate. Covers duplicated subjects from attached references (a second van in an
  "inside the cab" shot), names and text leaking from references, letterbox bars, sourceless bokeh orbs, wrong country/architecture drift,
  anachronistic construction states, glossy saturated sunsets, frozen poses across time, unsafe physics, wrong contact geometry and more.
  Use whenever a generated frame is rejected in QC and you need the fix line, or before writing prompts for a shot type that is known to
  fail (interior POV, crowd + hero, construction, sunsets, signage).
user-invocable: true
---

# Generation Failure Fixes

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

Each entry says what you see, why it happens, and what to change. When a fix works, add a new entry. Keep the one-line fixes literal:
they are pasted into the prompt as an `ACCURACY FIX` / `FIX` line, which overrides anything above it.

## The refine loop (before reaching for a fix)

Two ways to waste a budget: accept the first roll, or reword the whole prompt and re-roll until the money is gone. The loop that
converges (adapted from scenario-labs/skills `scenario-refine-loop`, MIT):

1. **Rubric before generating.** Turn the brief into pass/fail lines a viewer can check ("two headlights", "face matches the
   persona sheet", "no text"), never taste words. A rubric written after seeing the batch inherits the batch's flaws.
2. **Smallest batch** that tests the recipe, at the cheapest tier where every rubric line can still be judged.
3. **Recorded verdict per asset**, citing the rubric: `<index>: pass|fail, <the failed line>`. "Could be better" is not a verdict.
   Use `independent-frame-critic` so the judge never saw the prompt.
4. **Cheapest targeted fix per fail line**, routed per item (never re-roll the whole batch for one failure):

| The verdict says | Fix |
| --- | --- |
| One local defect on a keeper | Masked inpaint, or an edit of the keeper naming that one change (`identity-fix-pass` for faces) |
| A uniform finish is off (grade, tint, crop) | A deterministic pass in code (`video-color-grade`, `frame-crop-guard`), not a re-roll |
| Wrong content, composition or palette | Edit the delta clause, re-run from the approved baseline |
| Identity or style drift | Tighten the enumeration, add or re-role references (`reference-roles-leak-check`) |
| Every line failing | Change the model, keep the prompt |

5. **Change one variable per round,** so the improvement can be attributed.
6. **Regenerate from the baseline, never from the last attempt:** chaining output to output compounds drift.
7. **Hard stop:** a clean round ships. Three rounds without one, or one line failing twice under two different fixes, means report
   to the user, not respin: that is evidence about the model, not bad luck. A tier change (draft to final) is a new generation:
   re-run the keeper's recipe and re-critique it.

When a fix below works for a new symptom, add its row.

## Composition

| Symptom | Cause | Fix |
|---|---|---|
| **A second copy of the hero** (two vans, a second identical van beside the cab you sit in) | The look reference of the subject is attached to an "inside the cab" shot, so the model draws the reference *as another object* | Remove the subject reference for POV/interior shots. Describe the view as "INSIDE — the camera sits in its own cab; it is the ONLY van, no other vehicle anywhere, only open road". |
| Hero turns or the camera jumps sides between keyframes | Not stated | "Keep EXACTLY the same orientation as the start frame (front to the LEFT, kerb on the RIGHT)". |
| A collision or contact at the wrong place on the subject | Ambiguous wording | Anchor it in the frame: "its REAR in the FOREGROUND … the cart's shaft hits its side a metre forward of the rear wheel". |
| The scale is wrong: a giant object looks like a toy | No size cues | Give metres and a comparison: "each column as tall as a five-storey house; the workers are tiny beside it". |
| People stand in an unsafe place (on rail tracks, under loads) | The model does not reason about danger | "Everyone has stepped back behind the rope barriers; the track is EMPTY; nobody stands in front of the moving wagon". |

## Image format and optics

| Symptom | Cause | Fix |
|---|---|---|
| Black letterbox bars, rounded corners, vignette frame | "cinematic" is read as widescreen bars | "Full-bleed 16:9 image filling the whole frame edge to edge, NO letterbox bars, no borders". Then crop the bars with `trim_bars.py`. |
| Bokeh circles or orbs floating in the air or at the bottom of the frame | "anamorphic / bokeh" with no light source | "NO bokeh circles, orbs or light blobs anywhere — no light source there". Flares are allowed only at real lamps or the sun. |
| Blue horizontal streak across the frame | Anamorphic flare overdone | "No horizontal blue lens streaks". |
| Everything sharp, glossy, CGI-like | A change-to prompt sent without the optics and grade blocks | Attach the grade frame LAST and paste the full LOOK + OPTICS blocks into **every** prompt, including the change-to ones. |
| Saturated orange or gold "commercial" sunset | A plain "sunset" | "Restrained sunset: low sun behind thin cloud, muted amber-rose glow fading to slate — NOT orange-saturated; the sun a small white-hot point". |

## Text and names

| Symptom | Cause | Fix |
|---|---|---|
| The wrong name on the subject (a sister model's name) | The reference image shows a name | "If any name is visible it must be X — never Y. Better: the name too small or soft to read." Paint it out if it persists. |
| Random readable text, mastheads in the wrong language | Newspapers, shop signs | "The only legible word is the approved headline word; no masthead text, no foreign words". |
| Painted words on a wall ("GREEN") | Colour words read as text | Describe the colours as paint ("a broad green painted band"), and add "NO lettering on the wall". |

## Period and place

| Symptom | Cause | Fix |
|---|---|---|
| Parts that did not exist yet (a roof on a building still in scaffolding) | The model draws the finished object | "The frame is BARE in its scaffolding — NO roof, NO windows, NO cladding (fitted later)". |
| A wrong colour scheme for the date (a later livery) | Model default | Verify the scheme (`period-fact-check`) and name the exact colours: "cream, dark green and a red lining — no black, no grey". |
| Wrong city (Paris arcades instead of a northern port town) | "period street" defaults to Paris | Name the city and its materials: "red-brick terraces, wet slate roofs, gas lamps — no Parisian arcades". |
| Smoke from a chimney that is not in use | All chimneys treated alike | "Smoke ONLY from the two left chimneys; the right one is cold with a clean top". |
| A too-modern vehicle | Generic noun | Give the type and its features: "a 1910s open-cab lorry: solid tyres, chain drive, wooden bed — NOT a 1940s truck". |
| Smoke from an engine that is not running | Default "steam engine" | "NO smoke at all — the fire was long out". |

## People and time

| Symptom | Cause | Fix |
|---|---|---|
| The same person in the same pose an hour later | A change-to keeps everything | "TIME HAS PASSED: the night walkers are GONE; porters push a handcart …; no figure stays in the same place or pose". |
| An adult instead of a child (or the reverse) | Age drift | State the exact age and clothes again in the fix line. |
| Women or children in a workplace where they did not work | Mixed crowd default | Name who was there: "ONLY MEN on this line". |
| Unsafe or impossible physics (throwing hot metal, catching bare-handed) | Literal "toss" wording | Rewrite the action safely: tongs to tongs, gloves, tools. Re-check with `keyframe-chain-builder` law 1. |

## Products, ads and anatomy

| Symptom | Cause | Fix |
|---|---|---|
| An arm reaching a steering wheel or a product from the wrong side, or from nobody | Interior and over-shoulder close-ups confuse the model | Avoid vehicle-interior close-ups; use a roadside portrait or a front view outside the car. If it must be inside: "she sits in the driver's seat, both of HER OWN hands on the wheel, every limb attached to her own shoulders". Always check at full size. |
| A second copy of the product in the frame (extra sneaker pair, bottle reflection on the floor) | The product master is attached and the model places it twice | "Exactly ONE product in the whole frame, the one she wears or holds; nothing lying around; no floor reflection of it". |
| The scenes show a different product from the product shot | The product master was regenerated after the scenes were made | Regenerate the product shot FROM an approved scene ("exactly the car of image 1"), or regenerate every scene after the new master. Never let the two drift apart. |
| Steam rising from iced drinks | "Coffee" implies hot | "No steam anywhere: it is an iced, cold drink". |
| A real-brand-like mark (bitten-apple cut-out on a laptop, stripes on a sneaker) | Props default to famous designs | Remove the prop or say "plain unbranded lid / no stripes or marks resembling any real brand". |
| A flat black band or colour panel across the top of a packshot | "Keep the upper third empty" read as padding | "The background continues naturally to the top edge; no flat band, panel or rectangle". |
| Readable neon signs in a night city | Night-city default | "All signs are abstract light bars and shapes with no letters of any script". |
| Same-side arm and leg swing in a running pose | Pose prior | "Natural gait: the arm opposite the leading leg swings forward". |

## Faces

A wrong face (hairline, face width) goes to `identity-fix-pass`. Do not re-roll the whole shot.
