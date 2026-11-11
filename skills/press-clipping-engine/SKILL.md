---
name: press-clipping-engine
description: Two-phase engine for turning any screenshot into a press/newspaper-style Nano Banana image prompt. Phase 1 (once per reference set) ingests reference images of newspaper/magazine/document mockups, analyzes each concretely (surface, type hierarchy, palette, imagery treatment, annotation device, layout complexity, text-fidelity risk), and writes them into a library of named archetypes under references/archetypes/. Phase 2 (repeatable, per screenshot) reads a user-supplied screenshot, extracts its real content (headline, byline, source, imagery, the one phrase worth emphasizing), picks the best-fitting archetype — staying with the project's already-chosen archetype for consistency across a batch — fills the archetype's template with the real extracted text, and hands back one finished, ready-to-paste Nano Banana prompt. Ships five worked archetypes (vox-clip, editorial-broadsheet, pulp-tabloid, torn-stack, redacted-dossier) as starting points, not house style — a new reference set can add more. Use whenever the user wants a screenshot or image restyled as a newspaper/magazine/document clipping, wants a batch of screenshots processed in one consistent press style, or hands over new style references and asks to build a prompt library from them. Triggers on newspaper style, press clipping, magazine mockup, turn this screenshot into a newspaper, vox style prompt, collage style prompt, redacted document style, tabloid headline, analyze these references and make prompts.
---

# Press Clipping Engine

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

## Why this is a separate skill

One task, two different working rhythms. **Analyzing references** is a rare,
deliberate action: you look at eight images, find in them not one style but
several different devices, and write each one down so you never have to
look at them again. **Processing a screenshot** is a frequent, fast action:
the user drops in an image and needs a finished prompt within a minute, not
a fresh analysis of the visual language from scratch.

The skill separates these two rhythms physically: Phase 1 writes files to
`references/archetypes/`, Phase 2 only reads them.

## Phase 1 — references → archetypes

Runs when the user provides a set of style references (not a single
screenshot to process — specifically references to be used as guidance
from now on).

**A rule, not a formality:** references are analyzed **concretely** —
color blocks, where everything sits, how shapes end — not with a label like
"looks like Vox" or "looks like a poster". A label does not feed the prompt;
a concrete description does.

1. Look at each reference individually. Do not group them up front by
   feel — first write down for each one: the surface (table / flat
   background / card), the type hierarchy, the palette and what the accent
   in it is, the treatment of images inside (halftone / real photo /
   illustration), the annotation device (highlighter / hand-drawn circle /
   redaction bar / stamp / none), the layout complexity (single clipping /
   full page).
2. **Cluster by device, not by subject matter.** A comic mockup and a TV
   series fan mockup are different franchises, but the same device (loud
   headline + hand-drawn red mark) — that is one archetype, not two.
3. For each stable cluster — one file `references/archetypes/<name>.md`
   following the schema in `references/ARCHETYPE-SCHEMA.md` (ten slots,
   always including §8 TEXT FIDELITY RISK — the most common source of
   defects).
4. Look for **genre-wide laws**, not only rules within an archetype:
   this genre almost always has one hot accent color (most often red),
   reserved for exactly one annotation device; torn edges are always torn
   by hand, never cut with scissors; the type hierarchy is always
   masthead → headline → byline/date → body. Write such findings directly
   into the affected archetypes, not into a separate file — duplicate the
   rule in every place where it applies.

**Ready-made library** (sample archetypes, all marked
"not verified by render" — details in each file):

| Archetype | Device | Used for |
|---|---|---|
| `vox-clip` | highlighter behind a headline phrase | one quote-fact, a video frame |
| `editorial-broadsheet` | hierarchy by size, no mark | a long article/thread as a "real magazine" |
| `pulp-tabloid` | hand-drawn red circle/underline | a sensational fact, a loud headline |
| `torn-stack` | no mark — the composition of scraps itself | one quote as a poster/cover |
| `redacted-dossier` | redaction bar + rubber stamp | a leak, a document, an official source |

A new reference set does not replace these files but **adds** archetypes
alongside them — the same way `motion-style-core` keeps `paper-vox` /
`blueprint` / `clay` as examples, not the only option.

## Phase 2 — screenshot → finished prompt

Runs for every screenshot sent in.

### Step 1 — analyze the screenshot, not the archetype
Before choosing a style, extract the **exact** content from the screenshot:
- source type: social media post / article / document / chat / video frame
- all readable text verbatim: headline, dek, author, date, source name —
  copy, do not paraphrase
- **one phrase** worth emphasizing with a mark (not the whole headline —
  a specific word or short phrase around which the meaning of the frame is
  built)
- the image inside, if any: a concrete description (who/what is in the
  frame, shot size, color or b/w in the original — not "a photo of a
  person", but what is actually visible)

### Step 2 — choose the archetype
- If this is **not the first** screenshot in the project/session — **by
  default use the same archetype as before**, for the coherence of the
  series ("so all the screenshots are in one style" is a direct
  requirement). Change the archetype only if the user explicitly asks or
  the source type fundamentally does not fit (for example a document
  arrives while the series has been in `vox-clip` — then ask, rather than
  silently continuing with an incompatible archetype)
- If this is the first screenshot — match the source type and the required
  energy against the archetype table above, name the choice and briefly why
- Record the choice in a project file (`SELECTED-ARCHETYPE.md` next to the
  working materials, if such a folder already exists in the project) — so
  the next screenshot in the same session does not require asking again

### Step 3 — fill in the template
Take the `9. FILL-IN PROMPT TEMPLATE` of the chosen archetype and substitute
the real text from step 1 into the placeholders. Hand back **one** finished,
self-contained prompt — not variants, not half of it with gaps.

**⚠️ Clarify before generating: is the frame final, or will it be animated?**
If the archetype's annotation device (highlighter, hand-drawn
circle/underline) is later meant to be **animated as a separate layer**
(sliding in, being drawn on, appearing on a timing), it is **not baked into
the static generation**. The frame carries only clean text with no
color/mark on top; the mark is added separately in Remotion/After Effects,
as a separate animated layer (for example a highlighter swipe). Otherwise you
end up with two highlighters — one drawn by the generator and one animated
on top — or you have to clean out the first one. Archetypes with such a
device (`vox-clip`, `pulp-tabloid`) have a template variant in §9 for
exactly this case (`vox-clip` → 9-C) — use it by default if the user says
animation comes next, even without a direct request to "remove the
highlight".

**Rule for a real person's name/date** (from `vox-clip §9-B`, applies to
other archetypes too when the same risk exists): if the byline or date is a
real person or an official date rather than a decorative detail, prefer the
variant with an empty line for it, filled in by code, instead of trusting
the generator with a short but error-sensitive name.

**⚠️ Important text is always inserted, never replaced with texture.** If
the user sent text (a paragraph, a quote, a fact) and asks for it to be put
into the frame — by definition that is not decorative filler but the
substance of the material. "Illegible typographic texture" is a working
technique **only** for places where the source has no text at all and the
empty space needs to be covered with a text-like texture. Do not decide on
your own that the text is "not that important" and can be replaced with
texture — if it was sent and called important, it goes into the prompt as
real words, in a large legible font (a large font is the only thing that
lowers the distortion risk for dense text, see §8 in the archetype file).
In this case raise the generation resolution from 2K to 4K — more pixels
give a better chance that small letters come out right.

### Step 4 — QC after generation, mandatory
Every archetype carries its own risk profile (§8 in the archetype file).
After generation:
1. Check against the source text **word for word** — not "looks like the
   headline", but exactly these letters.
2. If the article body is supposed to be illegible texture — check that it
   really is illegible, and not readable lorem ipsum (this has happened
   systematically in practice: the generator inserts it even when the
   prompt explicitly forbids it — the first attempt often fails, be ready
   to retry with a clarification in the same thread).
3. If it diverges — regenerate with the same prompt, do not edit the pixels
   by hand.

## Relation to the motion-* pipeline

If the project already maintains its own `STYLE-PACK` (for example via
`motion-style-core`) with its own palette, fonts and a "names/dates only by
code" rule — **the project's rules take precedence over the archetype's
rules**. This skill produces one static clipping frame; if it is going to be
animated afterward, the finished frame becomes material for
`motion-remotion-build` / `motion-video-route`, and their own discipline
(for example, a rule that all on-screen text is set in code)
applies on top of it, not instead of it.
