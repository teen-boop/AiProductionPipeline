# Chapter ledger: BOOK_LEDGER.md

A book is written over many sessions. The co-writer forgets between them; the ledger does not. `BOOK_LEDGER.md`
lives in the root of the writer's project and holds the book's **structure**: every chapter's circle, a short
summary of every scene card, the connector chain that welds scenes and chapters, and the open promises the book
still owes the reader.

It does **not** hold looks, costumes, injuries, props or who-is-where. Those belong to the companion skill
`story-continuity-ledger` (its own versioned ledger, per chapter). The two ledgers point at each other by chapter
number; neither copies the other.

## When to write to it

- After the writer approves a scene card (Mode A step 10): add the scene row with status `carded`.
- After a draft is finished: status `drafted`, word count, beat weight if markers were used.
- After an audit: status `audited`, the one-line diagnosis, and any thread changes.
- After a chapter card (Mode C): the chapter block and its chain.
- Whenever a thread is opened, moved or paid off.
- Always update `Next action` last, so the next session knows where to start.

Edit in place; keep it short. A scene is one row, not a card. Full cards live in the writer's files (for
example `cards/3.2.md`) and the row links to them.

## Format

```markdown
# BOOK LEDGER - [working title]

Profile: BOOK_PROFILE.md            Continuity: continuity/LEDGER.md (story-continuity-ledger)
Language: [prose language]           Narration: [POV], [tense]
Updated: [date]                      Next action: [one line, e.g. "Card for 4.1: need comes from 3.3 BUT-hand-off"]

## Book circle
1 YOU [ch 1] | 2 NEED [ch 1] | 3 GO [ch 3] | 4 SEARCH [ch 4-11] | 5 FIND [ch 12] | 6 TAKE [ch 13]
7 RETURN [ch 14] | 8 CHANGE [ch 15]
Want / need: [thinks they want] / [actually needs]

## Chapter [N] - [title]                    status: [planned | carded | drafted | audited | final]
Owner: [name]   Chapter beat of the book circle: [which]
Circle: 1 [..] -T-> 2 [..] -T-> 3 [..] -B-> 4 [..] -B-> 5 [..] -T-> 6 [..] -T-> 7 [..] -T-> 8 [..]
Price (6): [what is lost for good]   Change (8): [how it is shown]

| # | Scene | Owner | Point (sketch test) | Need (2) | Find (5) | Price (6) | Change (8) | Out | Status | Words |
|---|---|---|---|---|---|---|---|---|---|---|
| N.1 | [title](cards/N.1.md) | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | T | drafted | 2,140 |
| N.2 | ... | | | | | | | B | carded | |

Chain: N.1 --THEREFORE--> N.2 --BUT--> N.3 ==BUT==> [N+1].1
Hand-off to chapter [N+1]: [the change of this chapter] --[T|B]--> [need of the next chapter]
Audit notes: [one line per audit, newest first]

## Connector chain (whole book)
1.1 -T-> 1.2 -B-> 1.3 =B=> 2.1 -T-> 2.2 -AND THEN (dead, fix)-> 2.3 ...

## Open threads (promises to the reader)
| ID | Promise / question | Planted | Must pay off by | Status | Payoff |
|---|---|---|---|---|---|
| T01 | [what the reader now expects or wonders] | 1.2 | ch 4 | open | |
| T02 | [ ] | 2.1 | ch 9 | paid | 8.3: [how] |
| T03 | [ ] | 2.3 | ch 6 -> ch 8 | moved | reason: [why] |

## Decisions log
- [date] [decision the writer made that later sessions must respect]
```

Notation: `-T->` THEREFORE and `-B->` BUT within a chapter, `=T=>` / `=B=>` across a chapter boundary,
`-AND THEN (dead, fix)->` for a joint still to repair. A dead joint never stays unmarked.

## Thread rules

- A thread is anything the reader now **expects or wonders**: a question, a promise, a planted object (a gun on
  the wall), a stated plan, a secret one character keeps from another.
- Every thread gets a **due chapter** when it is planted. "Some time later" is not a due date.
- At every chapter check, list threads due in this chapter. Each is paid off, consciously moved (with a reason
  and a new due chapter), or cut together with its plant.
- Payoffs are dramatized like beat 8: an action, an object, a line. A thread closed in narration is not paid.
- Threads due in the final third of the book should be fewer and bigger than threads due early.

## Resume procedure (Mode E)

1. Read the book profile, then `BOOK_LEDGER.md` top to bottom.
2. Find `Next action`. If it is missing, find the last scene whose status is below `final`.
3. Read that scene's card (and the draft, if any). Its beat 8 and its `Out` connector define the next scene's
   beat 2.
4. List threads with `Must pay off by` equal to the current or next chapter.
5. Report to the writer in five lines: where the book stands; the hand-off waiting to be used; threads due;
   gaps (scene rows without a card, missing connectors, dead joints still marked); the proposed next step.
6. On approval, continue in Mode A (next scene) or Mode C (next chapter card). Update the ledger after each
   approved card and each finished draft.
7. If the continuity ledger exists, check it for the chapter being written (who wears or carries what, injuries)
   before writing prose; do not copy its content here.

## Ledger health check

- Every scene row has an owner, a point and an `Out` connector.
- No `AND THEN` left unmarked in the chain; every marked one has an owner (who fixes it, when).
- No two rows in a chapter share a point.
- Chapter prices grow over the book; the book's price (beat 6 of the book circle) is the largest.
- No thread is overdue without a `moved` entry.
