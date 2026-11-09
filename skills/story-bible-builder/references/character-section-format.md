# Character Section Format

How each character appears in the final assembled bible. Match this shape.

---

## Structure per character

```markdown
### [NAME] — *[Role tag]*

**Visual:** [Hair] [skin] [signature identity markers — piercings, scars, permanent physical features]. [Face structure — one line]. [Body / posture default]. [Default expression]. [Any locked "never" clauses — no beauty mark, no teeth-showing smile, etc.]

**Function in the story:** [What they represent, what role they play, what they were built/born to be, what they became]

**Backstory:** [Origin, formative period, key pre-story events. One short paragraph or a few bullets.]

**Present-tense psychology:** [Where they are RIGHT NOW as the story begins. What they're carrying. What they don't yet know. What they're about to face.]

**Speech:** "[prompt-ready dialogue descriptor — register, texture, cadence, vocabulary, volume]"

**Movement:** "[prompt-ready movement descriptor — gesture quality, combat posture if relevant, tics, gait]"

**Stillness:** "[prompt-ready stillness descriptor — what they do at rest, hands, weight, expression, breath]"

**Suno (if music scope):** "[prompt-ready singing voice descriptor — register, timbre, style, signature move]"

[Optional bold sub-beats for specific narrative threads — e.g., a hidden relationship, a secret, a recurring pattern. Use sparingly and only when locked.]
```

---

## Rules

1. **The four prompt-ready descriptors (Speech, Movement, Stillness, Suno) must be in quotes.** They're engineered to drop verbatim into future prompts — either as standalone prompt inputs, or as feeder blocks for a video prompt director skill (like `cinema-worldbuilder-pro-20`). Specifically:
   - **Speech** feeds the Sound Bed block or dialogue direction
   - **Movement** and **Stillness** feed the Subject Lock block
   - **Suno** feeds vocal casting for music prompts
   That's the whole point — the descriptors are formatted this way so they slot in cleanly.

2. **Never use the character's name inside the quoted descriptors.** Refer by trait ("low-register voice," "cocked-hip stance"). Names drift models. Names live in the header only.

3. **Visual block is one dense line.** Not a bulleted list of features. One flowing sentence-fragment block with commas and periods. Easier to scan, easier to paste into a prompt as a character anchor.

4. **Function comes before backstory.** What they ARE in the story matters more than where they came from. Function is what future Claude uses to write scenes. Backstory is context.

5. **Present-tense psychology is what makes the bible alive.** It tells future Claude where the character is emotionally at the current story moment, so scenes are anchored in the right beat.

6. **Bold sub-beats are optional.** Use them for locked narrative threads (a hidden relationship, a secret, a recurring pattern). Don't force them. If a character's arc is straightforward, skip.

---

## Reference the demo bible

The example excerpts reference file (`example-bible-excerpts.md`) contains a full character section (MAREN from the HOLLOWTIDE demo) in this exact format. If the user has never seen one, show them that section as a reference. That's the density and shape to hit.
