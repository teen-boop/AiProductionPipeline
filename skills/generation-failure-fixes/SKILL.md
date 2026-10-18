---
name: generation-failure-fixes
description: >-
  A catalogue of recurring image-model failure modes in period/cinematic production, each with its cause and the exact prompt fix that
  worked. Look up a symptom, apply the fix line, regenerate. Covers duplicated subjects from attached references (a second ship in an
  "on board" shot), names and text leaking from references, letterbox bars, sourceless bokeh orbs, wrong country/architecture drift,
  anachronistic construction states, glossy saturated sunsets, frozen poses across time, unsafe physics, wrong collision geometry and more.
  Use whenever a generated frame is rejected in QC and you need the fix line, or before writing prompts for a shot type that is known to
  fail (on-board POV, crowd + hero, construction, sunsets, newspapers).
user-invocable: true
---

# Generation Failure Fixes

Each entry says what you see, why it happens, and what to change. When a fix works, add a new entry. Keep the one-line fixes literal:
they are pasted into the prompt as an `ACCURACY FIX` / `FIX` line, which overrides anything above it.

## Composition

| Symptom | Cause | Fix |
|---|---|---|
| **A second copy of the hero** (two ships, a second identical liner beside the deck you stand on) | The look reference of the subject is attached to an "on board" shot, so the model draws the reference *as another object* | Remove the subject reference for POV/on-board shots. Describe the deck as "ON BOARD — the camera stands on her own deck; she is the ONLY ship, no other vessel anywhere, only open sea". |
| Hero turns or the camera jumps sides between keyframes | Not stated | "Keep EXACTLY the same orientation as the start frame (bow to the LEFT, quay on the RIGHT)". |
| A collision or contact at the wrong place on the hull | Ambiguous wording | Anchor it in the frame: "her STERN in the FOREGROUND … the cruiser's bow rams her side a few metres forward of the stern". |
| The scale is wrong: a giant object looks like a toy | No size cues | Give metres and a comparison: "each funnel as tall as a five-storey house; the men are tiny beside it". |
| People stand in an unsafe place (on launch ways, under loads) | The model does not reason about danger | "Everyone has stepped back behind the rope barriers; the ways are EMPTY; nobody stands in front of the moving hull". |

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
| The wrong ship name on the hull (the sister ship's name) | The reference image shows a name | "If any name is visible it must be X — never Y. Better: the name too small or soft to read." Paint it out if it persists. |
| Random readable text, mastheads in the wrong language | Newspapers, shop signs | "The only legible word is TITANIC in a big headline; no masthead text, no foreign words". |
| Painted words on a hull ("GREEN") | Colour words read as text | Describe the colours as paint ("a broad green painted band"), and add "NO lettering on the hull". |

## Period and place

| Symptom | Cause | Fix |
|---|---|---|
| Parts that did not exist yet (funnels on a hull still on the slipway) | The model draws the finished object | "The hull is BARE on the slipway — NO funnels, NO masts, NO superstructure (fitted after launch)". |
| A wrong colour scheme for the date (camouflage colours) | Model default | Verify the scheme (`period-fact-check`) and name the exact colours: "brown, dark blue, light blue and white — no black, no grey". |
| Wrong city (Paris arcades instead of Belfast) | "period street" defaults to Paris | Name the city and its materials: "red-brick terraces, wet slate roofs, gas lamps — no Parisian arcades". |
| Smoke from a dummy chimney or funnel | All funnels treated alike | "Smoke ONLY from the first three funnels; the aftmost is a dummy with a clean top". |
| A modern submarine or vehicle | Generic noun | Give the type and its features: "a WWI U-boat: long low hull, small riveted conning tower, deck gun — NOT a WWII U-boat". |
| Smoke from a ship whose fires are out | Default "steamship" | "NO smoke at all — the boiler fires were long out". |

## People and time

| Symptom | Cause | Fix |
|---|---|---|
| The same person in the same pose an hour later | A change-to keeps everything | "TIME HAS PASSED: the night walkers are GONE; dockers push a luggage cart …; no figure stays in the same place or pose". |
| An adult instead of a child (or the reverse) | Age drift | State the exact age and clothes again in the fix line. |
| Women or children in a workplace where they did not work | Mixed crowd default | Name who was there: "ONLY MEN on this line". |
| Unsafe or impossible physics (throwing hot metal, catching bare-handed) | Literal "toss" wording | Rewrite the action safely: tongs to tongs, gloves, tools. Re-check with `keyframe-chain-builder` law 1. |

## Faces

A wrong face (hairline, face width) goes to `identity-fix-pass`. Do not re-roll the whole shot.
