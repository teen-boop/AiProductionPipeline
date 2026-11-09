# Script development

This phase turns the user's idea (or an existing script) into a finished story. Skip straight to
"Working from a finished script" below if the user already has a complete script they want to use;
otherwise run the full questionnaire.

## If the user has an idea (no finished script yet)

Ask the user, in one pass:

1. **Which structure to use** (pick one, or a named combination):
   - Save the Cat (Blake Snyder's 15 beats)
   - The Hero's Journey (Campbell/Vogler's 12 stages)
   - Three-Act Structure
   - Sequence Approach (8 sequences)
2. **Genre and story type** (Monster in the House / Rags to Riches / The Quest / Voyage and Return /
   Tragedy / Rebirth / Comedy / etc.)
3. **A short description of the idea, protagonist, setting, and what matters most to the user about
   this story.**
4. **Desired length of the final text** (e.g. a short story of 1500–2500 words / an extended
   synopsis / a full-length story / etc.)

Then, strictly in this order:
1. **Outline** — a detailed beat-by-beat/stage-by-stage skeleton following the chosen structure
   exactly, naming every beat/stage with 2–4 sentences on what happens in it.
2. **Synopsis** — a connected synopsis, 1–1.5 pages.
3. **Final story** — using the outline and synopsis, write the complete, finished story at the
   requested length. It must:
   - Be cohesive and read as a finished piece, not a draft/outline-with-prose-filler
   - Weave in every beat of the chosen structure organically
   - Give the protagonist a clear transformation
   - Carry real stakes
   - Land a strong emotional arc, and feel complete/resolved at the end
4. Only after delivering the final story, ask what the user wants to deepen or change — specific
   scenes, dialogue, characters, alternate endings, etc.

Always keep in mind while writing: the protagonist needs a clear transformation, stakes must be
real, the story must produce genuine emotion, and the chosen structure's rhythm must be respected
throughout — don't let the beats blur together or get skipped.

## Reference templates

These are ready-to-use operating prompts for this phase — paste one directly to the model as-is
rather than paraphrasing it.

Use the master combined prompt below as the default operating instructions for this phase; the
per-structure prompts are for when the user names one specific structure directly and wants a
leaner, single-structure-only pass.

### Master combined script-development prompt (default)

```
You are a screenwriter. Your only goal is to deliver a finished, complete story.

Workflow (do not deviate):

1. Ask me for the structure, genre, idea, protagonist, and desired length of the final text.
2. Build a detailed skeleton following the chosen structure.
3. Write a synopsis.
4. Only after that, write the **final, full story**.

Important rules for the final story:
- It must fully match the chosen structure
- Every stage/beat must be woven organically into the narrative
- The story must feel cohesive, not like a "draft"
- The ending must feel complete, with the protagonist's transformation landing

Start by asking me questions.
```

### Save the Cat (15 beats)

```
You are a screenwriter working strictly by Blake Snyder's "Save the Cat" method.

Create a story using the 15 required beats:

1. Opening Image
2. Theme Stated
3. Set-Up
4. Catalyst
5. Debate
6. Break into Two
7. B Story
8. Fun and Games
9. Midpoint
10. Bad Guys Close In
11. All Is Lost
12. Dark Night of the Soul
13. Break into Three
14. Finale
15. Final Image

My idea: [insert your idea]
Genre: [specify]
Protagonist: [briefly describe]

First, give the full skeleton for all 15 beats (2–4 sentences per beat).
Then give a connected synopsis.
After that, ask what to refine.
```

### The Hero's Journey (12 stages)

```
You are a master of mythological storytelling. Build stories strictly according to the 12 stages
of the Hero's Journey (Campbell + Vogler):

1. Ordinary World
2. Call to Adventure
3. Refusal of the Call
4. Meeting the Mentor
5. Crossing the First Threshold
6. Tests, Allies, Enemies
7. Approach to the Inmost Cave
8. The Ordeal
9. Reward
10. The Road Back
11. Resurrection
12. Return with the Elixir

My idea: [insert]
Genre/type: [specify]
Protagonist: [describe]

First, lay out each of the 12 stages in detail.
Then give a cohesive synopsis.
After that, suggest ways to strengthen the emotional arc.
```

### Three-Act Structure

```
Create a story using the classic three-act structure:

Act 1 (Setup) — 25%
Act 2 (Confrontation) — 50% (with a clear Midpoint)
Act 3 (Resolution) — 25%

My idea: [insert]
Genre: [specify]

First, break the story into three acts with key turning points.
Then write an extended synopsis.
```

### Sequence Approach (8 sequences)

```
Create a story using the Sequence Approach method: exactly 8 sequences, each a complete mini-story
with its own beginning, middle, and end.

My idea: [insert]

First, describe all 8 sequences.
Then connect them into a cohesive synopsis.
```

## Working from a finished script

Work from it directly — skip the questionnaire and outline/synopsis steps, but still read the whole
script before moving to production, so mini-scenes and beats can be extracted accurately.

## Test batch → full production

Once the script exists and references are understood: draft prompts for a small sampling of
mini-scenes across different parts of the script (max 7–8 images) — not the whole story yet.
Additional references can be requested here if a needed look/location/prop isn't covered by what's
on hand. Generate the test batch, get **explicit user approval** (style, color, identity-lock
fidelity, aspect ratio — everything), and only then write the complete set of prompts for every
mini-scene and move to full production.

## Prompt series per mini-scene

The story is a sequence of mini-scenes. Each gets ONE central/anchor prompt, plus additional prompts
scaled to how many discrete actions happen inside it: a simple establishing shot needs 1–2 prompts;
a multi-action sequence (walks → meets someone → boards a train) needs 5–6+, one per discrete beat.
The real face reference can be attached directly in the same generation as the scene (no strict
two-pass requirement) as long as face fidelity holds.
