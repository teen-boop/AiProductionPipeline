---
name: ai-book-writer
description: >-
  Scene engine for writing a book (novel, novella, long-form fiction) with an AI co-writer. Every scene runs
  through Dan Harmon's 8-beat Story Circle for its shape, and every joint between beats is welded with the
  "therefore / but" causality rule, never "and then". Works at three nested scales (book, chapter, scene) and in
  six modes: BUILD a new scene (card first, prose second, prose written in the book's own language once the card is
  approved), AUDIT existing prose (dead joints, missing beats, cheap prices, flat circles, plus prose-level checks:
  POV, tense, enter late, show don't tell, dialogue; includes a stdlib prose linter), CHAPTER / BOOK structure,
  STUCK ladder, RESUME from a BOOK_LEDGER.md, and SCREEN, which turns an approved scene into a shot list and a
  reference list for an AI visual pipeline. Cards and reports are in English; the prose can be in any language
  (English and Russian linter rules built in). Reads an optional private per-book profile (bible, tone, canon) from
  the writer's project. Use whenever the user is writing, planning, fixing or stuck on a book scene or chapter, asks
  for a scene card, beat breakdown, chapter outline or book structure, asks "why doesn't this scene work", wants a
  draft checked, wants to continue a book from where it stopped, or wants a chapter turned into shots. Triggers on
  write my novel, book scene, scene card, story circle, Harmon circle, therefore but, chapter outline, beat
  breakdown, audit my chapter, the scene drags, I'm stuck, continue the book, book ledger, chapter to storyboard.
---

# AI Book Writer

Two sources, one machine:

- **Dan Harmon's Story Circle** gives a scene its *shape*: 8 beats, a descent into the unknown and a return.
- **Trey Parker and Matt Stone's "therefore / but"** gives the *joints*: causation instead of sequence.

Shape without joints is an outline. Joints without shape is a chain of events. Every scene needs both.
The skill is a co-writer: it proposes, the writer decides. It never writes prose on top of an unapproved card.

## Scales

Three nested circles. **The scene is the working unit.**

| Scale | Circle owner | Beats 3 to 6 hold | Typical length |
|---|---|---|---|
| Book | the protagonist's life-want | the whole middle of the book | the book |
| Chapter | the POV character's chapter-want | the chapter's central pressure | 1 to 5 scenes |
| Scene | the POV character's want *in these pages* | the scene's conflict | 1 to 8 pages |

A scene's beat 2 is a *tactical* want ("get past the guard"), never the life-want ("be forgiven"). The
life-want lives on the book circle and leaks into scenes only as pressure.

## Before any mode

1. **Profile.** Look in the writer's project for a book profile (`BOOK_PROFILE.md`, or a `book-profile/`
   folder). If present, read it first: bible, tone, canon rules and declared exceptions (present tense,
   rotating POV) override the generic advice. How a writer sets one up: `profiles/README.md`. The skill never
   ships or invents a real book's profile.
2. **Ledger.** If `BOOK_LEDGER.md` exists in the project, read it before touching any scene (format in
   `references/chapter-ledger.md`).
3. **Language.** Cards, checklists and reports: English. Prose: the book's language, from the profile or from
   the existing text. Quotes from the manuscript stay in the original language.

## Mode routing

Read what the user brings and pick one. If ambiguous, ask once, then commit.

| Mode | The user brings | Do |
|---|---|---|
| **A BUILD** | an intent, a fragment, "I need a scene where..." | card first, approval, then prose |
| **B AUDIT** | written prose | reverse-engineer the circle, run structure + prose checks, deliver fixes |
| **C CHAPTER / BOOK** | a structure question above the scene | build the containing circle, assign its beats to scenes or chapters |
| **D STUCK** | "I don't know what happens next", "the scene won't move" | run the stuck ladder in `references/diagnostics.md` |
| **E RESUME** | "continue the book", a new session on an existing project | read `BOOK_LEDGER.md`, report where the book stands, continue |
| **F SCREEN** | an approved scene or chapter to turn into images or video | `references/screen-bridge.md` |

## Mode A: BUILD a scene

1. **Name the owner.** One POV character owns the scene's circle. Others get partial circles
   (`references/circle.md`, "Several circles in one scene").
2. **Write beats 1 to 8** as one-line statements in the scene card (`references/templates.md`). Write true, not
   pretty. For a big scene, fill the search-beat worksheet for beat 4.
3. **Weld the joints.** Between every adjacent pair of beats write **THEREFORE** or **BUT**. If the honest
   connector is "and then", the pair is dead: change a beat until a real connector fits
   (`references/causality.md`). Not optional, not cosmetic.
4. **Check the find (beat 5).** It must be the want *distorted*. Find equal to need is wish fulfilment.
5. **Check the price (beat 6).** It costs something that cannot be bought back in the next scene, and the owner
   pays it, not a bystander.
6. **Check the change (beat 8).** Visible on the page: an action, an object, a line, a refusal. Never "he was
   no longer the same man".
7. **Hand off.** Beat 8 of this scene produces beat 2 of the next, joined by THEREFORE or BUT. Write the
   connector down.
8. **Sketch test.** State the scene's single point in one sentence. If another scene in the chapter has the
   same point, merge them.
9. **Weight the beats.** Beats 1-2 and 7-8 are short; about two thirds of the words live in 3 to 6
   (`references/circle.md`, "Beat weight").
10. **Stop and show the card.** Wait for approval or edits.
11. **Write the prose** in the book's language, following the profile's voice. Put beat markers (`<!-- B1 -->`
    ... `<!-- B8 -->`) at the start of each beat in the draft so the linter can measure weight; the writer
    deletes them when the scene is final.
12. **Self-audit** the draft with Mode B steps 3 to 5 before handing it over, and update `BOOK_LEDGER.md`.

## Mode B: AUDIT prose

1. Read the whole scene before judging any part of it.
2. Extract the beats actually present, quoting a 3 to 6 word anchor for each. Mark missing beats **MISSING**.
3. Rebuild the connector chain from what happens in the text (`references/causality.md`, "Checking prose, not
   plans") and mark every dead joint **AND THEN**.
4. Run the linter for surface signals:
   `python3 scripts/prose_lint.py scene.md` (add `--json` for machine output, `--expect-tense`, `--expect-pov`
   when the profile declares them). Linter hits are candidates, not verdicts: read each in context.
5. Run the structural failure modes (`references/diagnostics.md`) and the prose checks
   (`references/prose-checks.md`: POV, tense, enter late / leave early, show don't tell, dialogue doing two jobs).
6. Deliver the audit report from `references/templates.md`: what is there, the chain, diagnosis ranked by
   severity, surgical fixes tied to beats and lines, and what works (leave alone). Do not rewrite the whole
   scene unless asked. A scene that works needs no invented problems.

## Mode C: CHAPTER / BOOK

Build the containing circle with the chapter or book card. Assign each of its beats to scenes (or chapters).
Typical three-scene chapter: scene 1 = beats 1-2-3, scene 2 = 4-5, scene 3 = 6-7-8, while each scene still runs
its own full circle inside. Write the hand-off chain across scenes and into the next chapter. Run the
5-minute chapter check (`references/diagnostics.md`). Record the result in `BOOK_LEDGER.md`.

## Mode D: STUCK

Walk the ladder in `references/diagnostics.md` top to bottom and stop at the first rung that frees the scene.
Most often: the find is not yet distorted (beat 5), there is no price (beat 6), or the joint back into the
previous scene is "and then".

## Mode E: RESUME

1. Read the profile, then `BOOK_LEDGER.md`: "Next action", the last scene's beat 8 and its hand-off connector,
   open threads due in the current or next chapter.
2. Report in five lines: where the book stands, the hand-off waiting to be used, threads that are due, any
   ledger gaps (a scene without a card, a missing connector).
3. Continue in Mode A for the next scene, starting from the waiting hand-off. Update the ledger after every
   approved card and every finished draft.
4. Look, injuries, props and who-is-where belong to the companion skill `story-continuity-ledger`; the book
   ledger holds structure only.

## Mode F: SCREEN

Only from an approved card and finished prose. Follow `references/screen-bridge.md`: visual beats (thoughts
converted to action, object or look), the shot table, the REFERENCES_NEEDED list, then hand off to
`script-extractor`, `storyboard-narrative-breakdown`, `storyboard-shot-selection`, `visual-story-4-references`
and `cinematic-prompt-writer`.

## Hard rules

- **One owner per scene circle.** Two drivers and the reader cannot tell whose scene it is.
- **Beat 5 is not beat 2.** The want arrives distorted.
- **No cheap price at beat 6.** A bruise, a delay, a ruined coat are not prices. Devastating relative to scale.
- **Beat 8 is dramatized, never summarized.**
- **Every joint is THEREFORE or BUT**, at every scale, including scene to scene and chapter to chapter.
- **Card before prose.** No prose until the writer approves the card. Then prose only in the book's language.
- **The writer owns the book.** Offer options when a choice changes canon; never silently change a canon fact
  from the profile.

## References

- `references/circle.md`: the 8 beats in depth, geometry and the three crossings, symmetry pairs, beat weight,
  circles for antiheroes, antagonists and side characters, chapter and book circles.
- `references/causality.md`: the canonical THEREFORE / BUT module (shared with other story skills).
- `references/templates.md`: scene card, chapter card, book card, audit report, search-beat worksheet.
- `references/diagnostics.md`: structural failure modes, the stuck ladder, the 5-minute chapter check.
- `references/prose-checks.md`: sentence-level checks with their fixes, mapped to linter output.
- `references/chapter-ledger.md`: the `BOOK_LEDGER.md` format and the resume procedure.
- `references/screen-bridge.md`: scene card to shot list and reference list for the visual pipeline.
- `references/example.md`: an original three-scene story worked end to end, with an audit and its fix.
- `scripts/prose_lint.py`: stdlib prose linter (connectors, telling, beat weight, tense mix, POV drift).
- `profiles/README.md`: how to add a private per-book profile in your own project.
