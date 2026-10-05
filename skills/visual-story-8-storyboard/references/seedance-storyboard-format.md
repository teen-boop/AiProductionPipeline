# Seedance storyboard + animation-description format

Two paired deliverables per mini-scene, and their styles MUST match each other:
1. a **single storyboard image** (a panel grid) showing the beats of the shot, rendered in the
   exact same visual style as the finished stills;
2. a **written Seedance animation prompt** in the dense structured format below.

The storyboard image is the visual plan; the written prompt is what actually drives Seedance. The
one rule that breaks everything if ignored: **the STYLE described in the written prompt must be the
same style shown in the storyboard image** — same film stock, palette, lighting, camera discipline.
If the storyboard looks like flat Wes-Anderson pastel but the prompt says "handheld documentary
grain," the video will fight itself.

## The single storyboard image

- One image, laid out as an even grid of panels (2×2 for a 4-beat shot, 2×3 for 6 beats).
- Each panel = one beat of the mini-scene, in sequence, left-to-right, top-to-bottom.
- Every panel is rendered in the project's locked visual style (paste the STYLE LOCK block into the
  generation prompt) — this is a storyboard *in the finished look*, not rough sketches.
- Attach the scene's approved face-locked still as a reference so the character/costume/location
  match what's already been produced.
- Thin clean gutters between panels; no text/numbers/arrows baked into the image unless the user
  wants them (they can drift/garble — prefer clean panels and keep beat numbering in the written
  prompt).
- Generate/test with **GPT Image 2.0**, but only via a **direct single-image generation call** —
  Krea's `generate_image` with model `openai/gpt-image-2`. **Do NOT use Lovart's `chat` endpoint for
  a storyboard grid.** Confirmed by direct test: Lovart `chat` is an *agent* — it decomposes a
  "4-panel storyboard" prompt into per-panel steps, charges credits per step (17 for the first, then
  another 16 for the next, etc.), and its first output was a single full-body character portrait,
  not a grid. A storyboard grid must be ONE image from ONE generation. GPT Image 2 is also NOT in
  Lovart's free/unlimited tier — it prompts for paid-credit confirmation there. So: for the grid,
  use Krea direct `openai/gpt-image-2` (paid, but one image per call, no agent decomposition). Free
  nano-banana-pro can also produce a single-image grid if cost is the priority.

## The written Seedance animation prompt (dense format)

Use the CAMERA / LOOK / STYLE / CHARACTER / SETTING / SCENES structure, with embedded beat-by-beat
action and dialogue. This is the format validated in-project. Keep animation direction in English;
keep spoken lines in the story's language (e.g. Russian), clearly marked as voice for a separate
recording — video models generate ambience reliably, and Seedance can lip-sync, but dialogue is laid
in during editing for control.

```
CAMERA: [the project's camera discipline — e.g. locked-off symmetrical tripod, static; or a single
slow tracking move. Name what the camera is NOT doing if it must stay still.]

LOOK: [film stock, grain, lighting behavior, palette, contrast — copied to match the STYLE LOCK
block and the storyboard image exactly.]

STYLE: [tone/mood and how the character moves — deadpan/measured, brisk, etc.]

CHARACTER: [name — dense physical + costume description in words. Note: video models block real-face
photo uploads, so identity here comes from text, not an attached photo.]

SETTING: [the location, described richly enough to match its reference sheet.]

SCENES:
[Beat 1 action.]
"[spoken line, in story language]"
[Beat 2 action.]
[Beat 3 action.]
...each beat = one storyboard panel, same order.
```

Per Seedance's own guidance: about **3 strongly distinct beats per generation** land reliably; keep
each beat under ~2.5s and fully staged if you want more. Avoid `slow`/`gentle`/`soft` (they trigger
unwanted slow-motion) — prefer `smooth`/`steady`/`precise`. Full Seedance prompting mechanics live
in the platform's own prompting guide; fetch it before submitting actual video.

## Style-match checklist before delivering

- [ ] STYLE LOCK block pasted verbatim into BOTH the storyboard-image prompt and the written
      animation prompt.
- [ ] Storyboard image's palette/lighting/grain visibly matches the finished stills.
- [ ] The written LOOK section describes that same palette/lighting/grain in words.
- [ ] Beat count in the storyboard grid = beat count in the SCENES list, same order.
- [ ] Character costume + location match their approved reference sheets.
