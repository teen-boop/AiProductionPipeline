# Causality: THEREFORE / BUT

> **Shared module.** This file is the canonical source for the "therefore / but" rules. Other story skills
> (a story coach, an outline builder, a screenplay tool) may read it directly instead of keeping their own copy.
> Section headings are stable so they can be cited by name. It has no dependency on the rest of this skill.

The rule from Trey Parker and Matt Stone, in substance: between every two beats of an outline there should be the
word **"therefore"** or the word **"but"**. If what fits between them is **"and then"**, it is not a story, it is
a list. "This happens, *therefore* this happens, *but* this happens, *therefore* that happens."

Causality is not a style ornament. It is the difference between a scene and a chronicle of events.

## Connector meanings

**THEREFORE: consequence.** The previous beat was a **character's choice**, and the next beat is its consequence.
Test: can it be rephrased as "they did X, and the world answered Y"? If yes, THEREFORE is earned.

**BUT: complication.** The world, another character or the truth intervenes and breaks what the character just
got or was about to get. Test: does it get harder for them? If it gets easier, it is not a BUT.

**AND THEN: defect.** Beat B does not grow out of beat A: you could swap them, or drop one, and lose nothing. The
cure is not rewording the joint but **replacing one of the beats**.

Notation used in cards and ledgers:

```
1 --THEREFORE--> 2 --BUT--> 3 --AND THEN (dead)--> 4
```

## Detecting "and then"

Ask of every adjacent pair, in this order:

1. **Swap test.** Swap A and B. Does anything break? If not, the joint is dead.
2. **Delete test.** Delete A. Is B still motivated? If yes, A was not causing B.
3. **Choice test.** Is there a decision by someone between A and B? No decision and no intrusion from the world
   means sequence, not causality.
4. **Rephrase test.** Say the pair aloud with "therefore", then with "but". If both sound false, it is "and then".

Surface words are clues, not proof. A sentence can say "then" and still be causal ("She lied. Then he had no
choice."), and a pair can be dead with no connector word at all, just two paragraphs side by side. Common surface
clues to look for in the text (any language has its own):

- English: "and then", "then", "after that", "next", "later", "meanwhile", "the following day".
- Russian: the equivalents of "and then" / "after that" / "next" (the linter knows them).
- Any language: a paragraph that opens with a time stamp and no reason ("At six, ...", "The next morning, ...").

`scripts/prose_lint.py` reports these clues with line numbers. Each hit means: check the joint, not "rewrite the
word".

## Alternation rhythm

A healthy scene alternates. Diagnose from the chain of connectors:

- `THEREFORE THEREFORE THEREFORE THEREFORE`: logical and predictable. The reader gets ahead of the author. Cure:
  insert a BUT where the character is sure they have won.
- `BUT BUT BUT BUT`: things fall on the character but they never choose. Feels arbitrary; the character is
  passive. Cure: make one BUT a consequence of their own choice, which turns it into a THEREFORE.
- `THEREFORE BUT THEREFORE BUT`: the working rhythm.

Guide for an 8-beat scene: about 4 THEREFORE and 3 BUT, with no run longer than two in a row.

## Where BUT almost always sits

- Between **3 and 4**: the tactic failed.
- Inside **4**: each failed attempt is separated by its own BUT.
- Between **5 and 6**: they got it, BUT here is what it turns into.

## Where THEREFORE almost always sits

- Between **2 and 3**: they wanted, therefore they went.
- Between **6 and 7**: they paid, therefore they come back different.
- Between **7 and 8**: they returned, therefore they act differently from beat 1.

## The hand-off chain

The same rule works **between** scenes and holds a chapter together:

```
Scene N, beat 8 (change)  --[THEREFORE | BUT]-->  Scene N+1, beat 2 (need)
```

If only "and then" honestly fits between two neighbouring scenes, they are two unrelated scenes. Cures, best
first:

1. Change beat 8 of the first scene so that it **produces** the need of the second.
2. Swap the scenes: "and then" often just means the wrong order.
3. Merge the two scenes into one (especially if they also share a point; see the sketch test).
4. Cut one. A scene you can remove without consequences is already cut; it is just still lying in the text.

The same chain at chapter scale: the change of chapter N produces the need of chapter N+1. At book scale a
sequel or the next part follows the same law. Record every link in the book ledger.

## The sketch test

Parker's test: every scene must work **as a standalone number**. Not "move the plot forward" but be something on
its own: funny, frightening, tense, tender.

Practical form: **state the point of the scene in one sentence.** If the sentence only comes out through plot
("here the reader learns that..."), the scene works as an information desk, not as a scene. If two scenes have the
same point, they duplicate each other: merge.

## Checking prose, not plans

In written prose the connectors are invisible and have to be rebuilt. Order:

1. Write down what **actually happens**, in short sentences, paragraph by paragraph. Ignore what the author meant.
2. Between every two, insert the honest connector: the one that fits, not the one you wish fit.
3. Every place where "and then" fits is a hole in the scene. There are usually one to three, and they always
   explain why the scene "doesn't move".
4. Then check the hand-off into the next scene the same way.

Plans lie more easily than prose. A card can say BUT while the written scene delivers AND THEN, because the
complication was summarized in one line instead of dramatized. Always audit the draft, not the card.
