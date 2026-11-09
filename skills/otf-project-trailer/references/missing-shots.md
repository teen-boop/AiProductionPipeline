# Missing shots: generation requests

When a beat has no usable material, the skill writes a request. It never generates, queues or spends credits by itself: the
user approves each request, the service and the cost first.

## 1. Decide if a shot is really missing

A beat is a gap only when none of these work:
- a different take of the same scene (check `rejected_sheet.jpg` with the user);
- a reframe of an approved frame for the target format (`frame-crop-guard`);
- a living still made from an approved still (3-8 % push plus one moving layer);
- moving the beat, or shortening the structure.

Typical real gaps: the cold-open detail, a peak image bigger than anything shot, a 9 s teaser hold, a vertical-safe hero.

## 2. Write the request

Append one block per shot to `<run>/GENERATION_REQUESTS.md`:

```markdown
## GR-03 - beat 6 (peak) - 4 s
Why: no image bigger than the hero shots; the peak needs the full ship against the storm.
Based on: <relative path of the closest approved frame> (continuity of place, light, lens)

### Still (start frame)
Route: image model of the project backend (e.g. Lovart / Nano Banana), or manual pack.
Prompt:
  <scene in one sentence> <subject, action already in progress>
  <the project's style block, copied whole from the style lock; never shortened>
  <cinematic optics: lens and focal length, shallow depth of field, explicit anamorphic traits
   (oval bokeh, horizontal flares from a named practical), film stock and grain>
  <light: a named physical source, warm practicals against a cool sky if the lock says so, deep blacks>
References (in order): 1 = <continuity frame>, 2 = <character or prop ref>, last = <director style frame>
Lint: style-lock-guard lint -> OK

### End frame (only for first+last chaining)
Made FROM the start frame with keyframe-chain-builder ("change to"): same place, people, light and lens, time moved forward.

### Video
Route: image-to-video model of the backend (e.g. Kling), start frame (+ end frame), 5 s, generate 1 s longer than the slot.
Prompt:
  <one small, motivated camera move that follows a detail (push-in 5 % toward the lantern as it swings)>
  <one dominant action, physically plausible, time moves forward; nobody frozen in a pose>
  <the second motion layer: smoke, rain, water, light>
  <no on-screen text, no music; diegetic sound only if the backend makes sound>
Estimated cost: <credits or price from the backend config>   Status: WAITING FOR YES
```

Rules:
- Vocabulary comes from the style lock and from the source prompts embedded in the director's references, not from
  generic "cinematic" words. Run `style-lock-guard lint` on every still prompt; a failing prompt is not shown as ready.
- Period projects run `period-fact-check` on the request before it is offered.
- Small camera moves only: push, drift, slow pan or tilt that follows something in the frame. No orbit, no crash zoom, no
  drone flythrough unless the shot is already that.
- Video prompts follow the project's video-prompt skill (`cinema-director-v3`, `seedance-prompt-writer`, or the one the
  project uses) and `video-clip-continuity-chain` when the shot continues another clip.

## 3. Route

- Connected backend: whatever `generation-backend-setup` saved in `pipeline.config.json`. Respect its concurrency limit.
- Manual mode: build a pack with `manual-image-pack` (one folder per frame, references copied and numbered). The user
  generates and drops `RESULT_1.png` back; the pack skill files it.
- Log every call with `generation-log`.

## 4. Gate and intake

1. Show the requests with cost. Generate only the ones the user says yes to.
2. Results: `frame-qc-contact-sheet` on the stills, `style-lock-guard compare` against the references, the user approves.
3. Clips: look at start, middle and end frames; trim handles; conform to 24 fps.
4. Re-run `pick_material.py` so the new shots enter the ranking with their real paths, then update the plan.
