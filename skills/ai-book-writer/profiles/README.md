# Book profiles

The skill's core is book-agnostic. It never ships a real book, a real author's bible or canon. Everything
specific to one book lives in a **private profile in the writer's own project**, which the skill reads when it
is there and ignores when it is not.

## Where the skill looks

In the writer's project folder (the folder the session is working in), in this order:

1. `BOOK_PROFILE.md`: a single file, good for most books.
2. `book-profile/`: a folder, for bigger books, with any of:
   - `bible.md`: characters, world, timeline, relationships.
   - `tone.md`: voice, POV and tense rules, sentence rhythm, words to use and never use, two or three sample
     paragraphs the writer considers on-voice.
   - `canon.md`: facts that may not change without the writer's explicit decision.
   - `exceptions.md`: deliberate departures from the generic rules (see below).

If both exist, the folder wins and `BOOK_PROFILE.md` is treated as its summary. The skill reads the profile at the
start of every mode, before `BOOK_LEDGER.md`.

## What to put in a profile

```
# BOOK PROFILE - [working title]

Language of the prose: [e.g. English, Russian, Spanish]
Narration: POV [first / close third / rotating by chapter / omniscient], tense [past / present]
Audience and shelf: [genre, age band, comparable books]

## Voice
- [3-6 rules, e.g. "short declaratives in action scenes", "no adverbs on dialogue tags"]
- Sample paragraph(s): [pasted from the writer's own approved prose]

## Canon (do not change without asking)
- [fact] (source: chapter N)

## Characters (one block each)
- [name]: want, wound, how they talk, what they never do

## Exceptions to the generic rules
- [e.g. "Chapter 7 is a diary in first person", "the prologue is in present tense"]

## Linter settings
--expect-tense [past|present] --expect-pov [first|third]
```

## Priority

1. The writer's instruction in the current conversation.
2. The book profile (canon, voice, declared exceptions).
3. The skill's generic rules (`references/`).

Structural hard rules (one owner, THEREFORE / BUT joints, a real price, a shown change) still apply; a profile
can only change *how* they are met (for example, a rotating POV gives each chapter a different owner).

## Privacy

- Keep the profile in your project or in a private repository. Never commit it to a public copy of this skill.
- If you install the skill locally and want profiles next to it, use `profiles/<book-slug>/` in your **local**
  copy only and add that folder to your `.gitignore`. Only this README is published.
- The skill does not copy profile content into anything it publishes (shot lists and prompts carry only what a
  scene needs).
