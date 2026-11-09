# Prose checks (sentence level)

The circle and the joints make a scene work as structure. These five checks make it work as *reading*. They run
in Mode B (AUDIT) after the structural pass, and in Mode A as a self-audit before a draft is handed over.

Order of work:

1. Run `python3 scripts/prose_lint.py <file>` (add `--expect-tense` / `--expect-pov` if the book profile declares
   them). It finds **surface signals** with line numbers.
2. Read every hit in context. Keep the real problems, drop the false alarms (a "then" that is genuinely causal,
   a "felt" that is a physical touch, a deliberate tense shift into a flashback).
3. Run the checks below by reading, because most of them cannot be measured.
4. Report in the audit's FIXES block: line, problem, the rewrite in the book's language.

A book profile can declare legitimate exceptions (present tense, rotating POV by chapter, an omniscient
narrator, a diary chapter). Respect them; check consistency *within* the declared rule instead.

| Check | Linter signal | What only reading finds |
|---|---|---|
| POV does not jump | `pov_first_in_third`, `narrator_absent` | head-hopping inside third person |
| Tense holds | `tense_flip`, `tense_mix` (English only) | tense in non-English prose, flashback entry and exit |
| Enter late, leave early | `opening_heavy`, `bottom_thin`, `missing_beat` | throat-clearing, epilogue tails |
| Show, don't tell | `telling` rules, `suddenly`, named emotions | summary where a moment should be |
| Dialogue does two jobs | none | lines that only inform |

---

## POV does not jump

**Rule.** One scene, one point-of-view character (usually the circle's owner). The reader knows only what that
character can see, hear, remember, infer. In first person, the "I" never knows another person's thoughts. In
close third, the narrative never dips into a second head mid-scene.

**Symptoms.**
- "She could tell he was lying" is fine; "He knew she would never find the letter" in her scene is a jump.
- Describing the POV character from outside ("her green eyes flashed") in close third.
- A first-person passage appearing in a third-person book without a frame (letter, diary, quoted thought).

**Fix.**
- Move the other character's inner life to the outside: what the POV character *observes* (a hand that stops, a
  glance at the door, a lie that comes too fast).
- If the second head is essential, end the scene and start a new one owned by the other character, with a
  hand-off connector.
- Frame embedded first person explicitly (italics, a heading, the letter as an object in the scene).

Before: *Ines retuned the A. Hale thought she was too young to remember how Clara played.*
After: *Ines retuned the A. Hale watched her hands the way people watch a child carry a full glass.*

## Tense holds

**Rule.** The narration keeps one base tense (usually past, sometimes present). Shifts are allowed only with a
clear frame: a flashback entered with one or two past-perfect verbs and then continued in simple past, a
present-tense general truth ("Pianos go flat in damp rooms"), dialogue.

**Symptoms.** A paragraph that slides from "she lowered the pitch" to "she plays a chord"; a flashback that never
exits; present-tense commentary that sounds like the author talking.

**Fix.** Pick the base tense from the profile or the first page; convert drifting verbs; mark flashback entry
("had been", two verbs at most) and exit (a concrete present-scene anchor: a sound, an object, a line of
dialogue). For non-English prose the linter does not check tense: read for it.

## Enter late, leave early

**Rule.** Enter the scene as close to beat 3 as possible and leave as soon after beat 8 as possible. Beats 1-2
are context and pressure, compressed; beats 7-8 are a turn and a door, not an epilogue.

**Symptoms.** The scene opens with travel, weather, or the character remembering backstory; the first line of
dialogue arrives on page two; after the change there are paragraphs of reflection or "the next day" summary.

**Fix.**
- Cut the first paragraph and see if anything is lost. Repeat.
- Fold beat 1 into the first action of beat 2 (show the normal *while* it is being broken).
- End on the visible change of beat 8 or on the hand-off line that produces the next scene's need. Move any
  reflection into the next scene's beat 1, as action.
- With beat markers in the draft, the linter warns when beats 1-2 exceed 25 % or beats 3-6 fall below 50 %.

## Show, don't tell (sentence level)

**Rule.** Do not hand the reader the conclusion; hand them the evidence and let them draw it. At sentence level
the usual culprits are filter verbs (*realized, understood, felt, noticed, saw that, knew that*), named emotions
(*she was nervous*), narrator verdicts (*it was clear*), and announced surprise (*suddenly*).

**Fix, by type.**
- **Filter verb:** delete the filter and show the thing. "She noticed the card was in Clara's hand" ->
  "The card was in Clara's hand: the same slanting sevens as the note on the fridge."
- **Named emotion:** replace with what the emotion makes the body or the hands do, or with a choice. "She felt
  nervous" -> "She tuned the same string twice."
- **Verdict:** stage the evidence. "It was clear he meant it" -> "He put the wallet back in the drawer and
  locked it."
- **Suddenly:** cut the word; make the sentence short; put the surprising thing first.
- **Summary instead of scene:** if a beat (especially 4, 6 or 8) is summarized in one sentence, it must be
  dramatized: a moment, in real time, with an action or a line.

Telling is not always wrong. Transitions, compressed time and the narrator's voice may tell on purpose. The test:
is this a moment the reader should *live* (a beat), or a corridor between moments? Beats are shown, corridors
can be told.

## Dialogue does two jobs

**Rule.** Every line of dialogue does at least two things at once: moves the scene (a tactic in beat 3-4, a
demand, a refusal, a lie) **and** reveals character, relationship, subtext or the price. A line that only
delivers information is exposition in quotation marks.

**Symptoms.** "As you know, ..."; characters telling each other what both already know; questions answered fully
and politely; every line on-the-nose about the feeling; tags doing the acting ("she said angrily").

**Fix.**
- Turn information into a tactic: who wants what from whom with this line? Make the line an attempt in beat 4,
  so it can fail (BUT).
- Let people not answer: deflect, answer a different question, answer with an action.
- Move emotion from the tag to a gesture or object; use "said" or nothing.
- Cut any line that survives the test "if I delete it, the scene loses nothing".

Before: *"Clara used to play every evening, before she died two years ago," Hale said sadly.*
After: *"She played at seven," Hale said. "Every evening. You can set your watch." He did not look at his watch.*
