---
name: visual-story-7-platform-qc
description: STEP 7 of 8 in the sequential visual-story pipeline. Platform operation and quality control. Covers platform-specific mechanics for Lovart and Krea (auth, free/paid mode, concurrency limits, timeout/poll behavior, aspect-ratio handling, real-face-upload restriction on video), the budget/mode confirmation rule, and the QC + identity-fix pass before delivery. Run AFTER visual-story-6-production, and reference its platform notes throughout generation. Runs alongside generation; the pipeline's final deliverable is the storyboard (step 8).
---

# Visual story — Step 5: Platform operation + QC

**Step 5 of 5.** Before this: `visual-story-6-production`. This is the final step, but its platform
notes are needed *throughout* steps 3–4 whenever you actually submit a generation — read
`references/platforms.md` before your first submission on any platform this project, not just at the
end.

## Budget / mode — ask before the first generation on any platform

In one pass, confirm with the user:
1. **Which model** to generate with (if the platform offers a choice).
2. **Which mode** — free/unlimited (queued, no credit spend) or paid/fast (costs credits) — never
   assume, never default silently.
3. **What it will cost**, to the extent the platform exposes it — or say plainly when cost isn't
   knowable from the CLI/API and point to the platform dashboard. Don't guess a number.

Re-verify mode after any credential change mid-project — mode does not carry across a key rotation.
Ask before spending paid credits unless the user already said "use your judgment" for this project.

## Platform mechanics — read before submitting

`references/platforms.md` has the full operational detail for **Lovart** (CLI, upload/attach flow,
`set-mode --unlimited`, client-timeout-then-poll-by-thread-id pattern, concurrency cap, congestion
handling, aspect ratio via prompt text) and **Krea** (presigned upload URLs, `nano-banana-pro`
identity-lock, dedicated `aspect_ratio` field). Two hard-won specifics worth surfacing here:
- **Lovart client timeouts are normal** — a returned `"final_status":"timeout"` means the client
  gave up, not the job. Extract the `thread_id` and poll `result --thread-id` until done. Stuck jobs
  can also occupy the concurrency limit and block new ones.
- **Video models (e.g. Seedance on Krea) block uploads of real human faces** for compliance — so
  video identity must come from text description, not an attached face photo (unlike still-image
  generation on Lovart/Krea, which does use the face photo). Seedance does support lip-synced
  dialogue, not just ambience.

## QC every delivered image — actually look, every time

Before calling anything done, scrutinize every region/panel — blur/ghosting, warped anatomy,
duplicated features, text/logo errors, mismatched lighting, wrong background bleeding in from an
attached reference. Matters most for multi-panel sheets and multi-reference generations. Full
checklist, the continuity-check list for coverage sequences, character-sheet QC, and the two
identity-fix techniques (minor patch-in-place vs. full clean-slate regeneration) are in
`references/qc-and-fixes.md`.

## When done

Scenes generated, QC'd, delivered. The pipeline is complete — loop back to `visual-story-4-references`
for any new character/location/prop a later scene introduces, or `visual-story-2-script` for a new
episode.
