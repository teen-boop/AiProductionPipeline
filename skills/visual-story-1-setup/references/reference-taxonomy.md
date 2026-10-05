# Reference taxonomy and how to read a reference

## Folder structure

Every subfolder under the project's references directory is scoped to ONE task category — never a
junk drawer:
- **`Characters/`** — one folder per character, containing real face photos AND a persona/concept
  subfolder. If persona is empty, invent one consistent with the project's established style — don't
  leave it blank, don't ask permission, just do it and flag the new concept for review.
- **`Locations/`** and **`Props/`** — one folder per location and per recurring object, holding the
  canonical reference image(s) generated per scene as the script locks (a location's reference is
  usually the scene's first character medium-shot, doing double duty). See
  `09-location-and-prop-references.md` for the full workflow — this is mandatory alongside character
  references, not an optional extra tier.
- **Title/text-overlay references** (if any) — scoped specifically to title-card/text-overlay design.
  Treat as its own discrete task, not folded into scene generation.
- **`style and color/`** — the single source of truth for consistent style, palette, and lighting
  across every generated image. Check new prompts against this folder's actual contents, not vibes
  or a one-word style label. Once the project has approved masters (§4 in SKILL.md), add them here
  too — real, produced-in-this-project images are an even stronger style reference than mood boards.
- The user's own pasted text prompts count as references too — study their phrasing/color/light
  language as the primary template for new prompts.

**If a references folder contains a series of full prose prompts** (not just mood images), treat
those prompts as the mandatory template for BOTH the script/story AND every generation prompt —
equal or higher priority than mood images. Read every one in full before writing anything new.

## Rule: atmosphere transfers, subject matter doesn't have to

When generating from or inspired by a reference, the new prompt's subject matter can be completely
different from the reference's subject — different character, different scene, different story beat
— but the reference's lighting and cinematic atmosphere must always carry over. Content is free to
change; atmosphere is not.

Before writing a new prompt from any reference, extract and explicitly restate:
1. **Photographic mode** — see the two-mode breakdown below.
2. **Light source(s) and behavior** — e.g. a banker's lamp as sole warm light source, flat even
   studio light, foggy diffused daylight.
3. **Depth-of-field behavior** — shallow with foreground blur, or flat sharp-throughout.
4. **Atmospheric quality** — haze, mist, grain, desaturation.

Carry all four into the new prompt even when swapping in a different character, costume, and
setting. This is a hard requirement, not a nice-to-have — this is what makes a "different scene,
same world" read as the same production rather than a different generation entirely.

## Two photographic modes — identify which one before writing the prompt

A reference library can contain either of these; don't default to one without checking:

- **Cinematic film still** — shallow depth of field, a blurred foreground element, atmospheric
  haze/mood, moody directional lighting. State "shallow depth of field" as its own explicit phrase
  (don't just imply it via "cinematic"), frame as medium close-up rather than medium-wide for a
  character portrait/action moment, and include a softly blurred foreground element (a prop edge,
  railing, bottles, fabric). This combination — not color/prop detail alone — is what produces a
  genuinely filmic look; a batch that drops it drifts toward flat, illustration-like results even
  with identical color-palette language.
- **Editorial fashion photography** — flat, even studio lighting, everything sharp front-to-back,
  bold graphic composition, high-key color blocking. Do NOT impose shallow DOF or foreground blur on
  this mode — it contradicts the reference. State "flat lighting" / "sharp focus throughout"
  explicitly.

Check whether background elements are sharp (editorial) or soft (cinematic) in the actual source
image before choosing — don't guess from a style-label shortcut.

## What a well-built reference-prompt library encodes

Extract the *pattern*, not just phrases:

1. **Specific fabric + color pairing for every garment**, never vague ("chunky knit emerald green
   turtleneck", not "green sweater").
2. **A named practical prop tied to the character's role/action** — always mid-action with something
   specific, never just standing.
3. **Backgrounds: atmosphere, not just blur.** Specific-but-blurred beats generic ("massive orange
   distillation tanks with brass fittings", not "lab equipment"). Layer in: atmospheric haze/mist/
   humidity, a tightly muted 2–3 color palette applied to the WHOLE frame (not just the subject's
   outfit), and often a secondary background figure/action barely visible in the haze for depth (e.g.
   a crouched figure on a bamboo canopy). Name the weather/haze condition explicitly, restate the
   muted palette as covering foreground AND background, and consider one small background
   detail/figure for depth layering.
4. **An explicit, named color-palette statement** as part of the prompt itself.
5. **Purposeful mid-action poses with narrative charge** — examining, gesturing, mid-decision.
6. **A consistent technical/film-grammar suffix** (film stock, grain, depth of field, era) repeated
   across every prompt in the library — load-bearing, not decorative boilerplate.
7. **Every character reads as visually compelling**, styled as close to their real reference photo as
   possible — not a generic or lesser version of anyone else in the cast.

## Checklist before writing any prompt from a visual reference

Don't lean on a style-label shortcut (a director's name, a one-word aesthetic) and hope the model
fills in the gaps. Every time:

1. **Color blocking, not gradients** (if the target style uses it). Name the actual flat color
   blocks per frame explicitly.
2. **Character-as-accent vs. background.** Is the costume a deliberate contrast to the backdrop, or
   a monochrome match? State which.
3. **Scale and placement in frame.** Small subject in a large environment (wide, static), or a close
   portrait crop? Match what the reference actually does.
4. **Pose/gaze mode.** Direct-to-camera vs. candid/profile not acknowledging the camera.
5. **Multi-character arrangement.** A lineup vs. staggered-depth candid figures are different tools —
   check which the reference uses before composing a group shot.
6. Only after naming 1–5, write the prompt.

## Trademark/logo bleed risk

Naming a specific real-world director/franchise/brand in a prompt can bleed trademarked names into
props/signage — the model pattern-matches "in the style of X" into actual proper nouns from X's work
appearing on signage, badges, or props. Proactively add "no real logos, brand names, or text from
existing works" to every vintage-prop/signage-heavy prompt up front. This recurs even after being
caught once — treat it as a standing risk on any project that names a specific stylistic touchstone.
