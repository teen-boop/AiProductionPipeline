# The Story Circle at scene scale

Dan Harmon's Story Circle, applied to prose. The same eight beats work for a scene, a chapter and a book; this
file describes them at scene scale and shows how they nest.

## Geometry

The circle is cut by two lines.

**The vertical line is the inner world.** Left half: the character is ignorant, in denial, lying to themselves,
inside an illusion. Right half: they see, are disillusioned, honest, out of denial.

**The horizontal line is the outer world.** Top: the known world, order, consciousness, solid ground. Bottom:
the unknown world, chaos, depth, death. The character dives in dry from a familiar place and comes up wet, but
back into a familiar place.

**Three crossings, three points of maximum change.**

| Crossing | Where | What happens | Usual outcome |
|---|---|---|---|
| Horizontal, going down | beat 3 | outer conflict, first threshold | usually a **loss** |
| Vertical, at the bottom | between 4 and 5 | collision with oneself, one's own beliefs | a **shift of mind** |
| Horizontal, going up | beat 7 | outer conflict, second threshold | usually a **win**, because the shift already happened |

The consequence: **the owner cannot win at beat 7 if nothing shifted inside them between 4 and 5.** If they win
anyway, it is a deus ex machina. Check this pairing in every audit.

## The eight beats

Harmon's word on the left, what it means at scene scale on the right.

### 1. YOU
Who owns the scene and what their normal is **right now**. Not biography: the status quo of these pages. Shown
through action: what they are doing when we come in. A short beat.
*Mistake:* opening on a description of the world instead of the person in it.

### 2. NEED
What breaks the normal and what they want **in these pages**. A tactical want, not a life-want. Often it comes
from outside: a knock, a piece of news, someone else's order.
*Mistake:* putting the book's through-line want here. "Wants redemption" belongs to the book circle. In a scene:
"wants this man to say the address".

### 3. GO
They cross a line and start acting. They choose a **tactic**. Here the scene enters chaos. Sometimes the call is
refused, and then they are pushed into chaos by someone else.
*Mistake:* agreeing too easily. Going should already cost something: time, reputation, a principle.

### 4. SEARCH
The tactic does not work. Resistance, adaptation, escalation. **The longest beat of the scene.** The author's
job here is to put obstacles between the character and the want. Three attempts are the working minimum for a
big scene; one is enough for a short one.
*Mistake:* search as montage ("he searched for three days"). Search is concrete failures, each with its own BUT.

### 5. FIND
They get what they went for, **but not the way they expected**. The find is always distorted. This is the
critical beat: the distortion is what makes a scene a story rather than wish fulfilment.
*Mistake:* the find equals the need exactly.

### 6. TAKE (the price)
They take the find and pay for it. The price must be **impossible to restore in the next scene**. The Dark
Knight gets the Joker and loses Rachel. A frightened boy gains courage and loses his innocence.
*Mistake 1:* a cheap price (a bruise, being late, a ruined suit).
*Mistake 2:* someone else pays, and the owner of the scene does not feel it.

### 7. RETURN
They come back into the recognizable world, carrying the price. The outer conflict resolves in their favour
here, because the inner shift has already happened. A short beat.

### 8. CHANGE
The change is **made visible**. An action, an object, a line, a refusal. Harmon: change has to be made visual.
What they would not have done at beat 1, they do now. Or the reverse: what they would have done, they now refuse.
*Mistake:* "He understood he was no longer the same man." That is not beat 8, it is a report about beat 8.

## Symmetry: checking beats against their pairs

Each beat sits opposite its pair. Pairs check each other.

- **1 and 5**: the two "light" beats, before the want and after it. The normal and what was gained. Do they read
  as the same person in two states?
- **2 and 6**: the want and the price. Both hold the same thing: 2 is *I want*, 6 is *what it really took*. If
  the price does not hit exactly what they wanted, it is the wrong price.
- **3 and 7**: the two crossings between worlds. One way in, one way out. Compare how they enter and how they
  leave: the difference between the two is the scene.
- **4 and 8**: both about finding balance. At 4 they adapt to a foreign world; at 8 they become someone else in
  their own.

If a pair does not rhyme, one of the two beats is usually broken, not the joint.

## Beat weight (word count, not importance)

The circle is even in geometry, not in text. Guide for a scene:

| Beats | Share of words |
|---|---|
| 1 + 2 | 10 to 15 % (short, often merged into one paragraph) |
| 3 | about 10 % |
| 4 | **30 to 35 %** (the bulk) |
| 5 | about 15 % |
| 6 | about 15 % |
| 7 + 8 | 10 to 15 % (short, merged) |

The bottom half (3 to 6) is about two thirds of the scene. If half the text went to beats 1 and 2, the scene
starts too early: cut the entrance. `scripts/prose_lint.py` measures this when the draft carries beat markers;
it warns above 25 % for beats 1-2 and below 50 % for beats 3-6 (looser than the guide, to avoid false alarms).

## Several circles in one scene

**The owner** runs the full circle. Everyone else runs partial, sparse circles with gaps. That is not a flaw; it
is the norm: side characters have no room for eight beats.

**An antihero skips beats, legitimately.** The all-knowing mentor type skips 4 (adapts instantly, already the
smartest in the room) and 8 (does not change). Their circle is thin exactly at the price, because they rarely
land in a situation they do not control.

Book rule: **if the owner systematically skips beat 8, someone else in the scene must carry the change**,
otherwise the scene stands still. Technique: the unchanging hero becomes the instrument of change for the person
next to them.

**The antagonist also walks a circle.** Give them at least 2 (what they want) and 6 (what they pay), or they are
scenery. A villain with a full circle of their own (a want, a fall, a visible change) is stronger than a
well-described one.

## Chapter circle and book circle

Same machine, different scale.

- **Chapter circle:** beats are dealt out to scenes. Usual layout for three scenes: scene 1 = beats 1-2-3, scene
  2 = beats 4-5, scene 3 = beats 6-7-8. One scene can carry one chapter beat while running its own full circle
  inside.
- **Book circle:** beats are dealt out to chapters or parts. The bottom half (3 to 6) is almost the whole book.
- **Circles repeat.** A character runs the circle many times across a book; each new circle enters a different
  unknown world with a different want. An arc is not one circle but a spiral.
- **Characters' circles are out of sync.** They start at different times, move at different speeds and skip
  different beats. That is what makes characters feel alive off the page.
- **Prices scale.** A chapter's price is bigger than any single scene's price inside it; the book's price is the
  biggest of all.
