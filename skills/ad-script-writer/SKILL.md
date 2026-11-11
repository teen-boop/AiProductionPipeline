---
name: ad-script-writer
description: Write a short ad or commercial script (6, 15, 20 or 30 seconds) as a beat sheet from the ad research library - one audience category, one pain, one result - with picture, spoken words, on-screen text and sound in one table, every line traced to the Ad Glossary, plus the production handoff (cast, location, props, title cards) for the image and video stages. Use after ad research and ad texts exist and a script is needed for a filmed scene, a person talking to camera, or a motion-graphics ad; when asked to turn a hook, a pain or an ad line into a commercial script, to write a 15 or 30 second spot, or to make script versions per audience category. Triggers - ad script, commercial script, 15 second ad, 30 second spot, beat sheet, script for this hook, script per category.
---

# Ad Script Writer

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

Stage 2 of the ad pipeline: **research -> texts and script -> images -> video -> titles -> edit -> effects and sound -> final**.

A script here is a beat sheet. It tells the image, video, title and sound stages exactly what to make, and every word in it comes from the brand's Ad Glossary.

## Inputs

| Item | Default |
|---|---|
| Brand | Required. Must have a glossary in the research library. |
| Audience category | Required: one code (A1, A2, ...). One script serves one category. |
| Pain row | The first pain row tagged with that category |
| Length | 15 s |
| Format | Filmed scene |
| Aspect | 9:16, with 1:1 and 16:9 noted if asked |

Formats:

- **Filmed scene:** people and places, generated or shot. Voice-over or one line of dialogue.
- **To camera:** one person from the audience speaks to the lens.
- **Motion graphics:** text, photos and product screens, no actors.

If the brand has no glossary, or the category has no pain row, stop and run `ad-research-glossary` first.


## Step 1. Pull the material

Use the library lookup from the `ad-copy-director` skill; do not read whole glossaries.

```bash
python3 ../ad-copy-director/scripts/lookup.py -b BRAND -c A6          # the category: problem, words, caution, pains
python3 ../ad-copy-director/scripts/lookup.py -b BRAND --section 8    # do not say
```

Write down, before any beat: the category's one problem, its **caution**, the pain row, two audience phrases, the plain product term with its caveat, and the proof allowed on screen (or "no proof").

## Step 2. One-sentence premise

> A [length] [format] ad that shows [category] how they [result], by [what the product does].

If the sentence needs "and", the script has two ideas. Cut one. Get this sentence right before writing beats.

## Step 3. Choose the shape

| Length | Beats | Shape |
|---|---|---|
| 6 s | 2 to 3 | Hook, result, brand |
| 15 s | 4 | Hook, pain, answer, result with brand |
| 20 s | 5 | Hook, pain, turn, result, brand |
| 30 s | 6 to 7 | Hook, pain, turn, answer, proof, result, brand |

- Every joint between beats reads as **"but"** or **"therefore"**, never "and then".
- The **hook** lands in the first 3 seconds and carries its own context: who it is for, the situation, what they get. It may be spoken, on screen, or split: a customer's line spoken while the context sits on screen.
- The **pain** is shown, not explained: one concrete moment from the audience's day.
- The product enters at the **turn**, as the answer. It never opens the ad.
- The **result** is visible in the picture: the person has the thing the result line promises.
- The **brand** beat is the logo, one line and one button. Nothing else.

## Step 4. Write the beat sheet

One table. Every row is one beat.

| # | Time | Picture | Spoken | On-screen text | Sound | Trace |
|---|---|---|---|---|---|---|

- **Time:** `0 to 3 s`. Beats join with no gap and end on the stated length.
- **Picture:** one action in one place, something a camera could record. Name who, where, and what they do. No "montage of".
- **Spoken:** mark the voice: `VO:`, `OWNER:` or `CUSTOMER:`. Speech budget is 2.3 words a second with 20% air, so about 28 words for 15 s and 55 for 30 s. No beat above 3 words a second.
- **On-screen text:** short lines under the picture. No long dashes. Do not repeat the spoken line word for word unless it is a caption.
- **Sound:** only real actions: the door bell, the cup set down, the page turn. Music as one note for the whole ad.
- **Trace:** category, pain number, phrase or term with its status.

Rules that hold for every script:

- One category, one pain, one result.
- Wording comes from audience phrases; none of the glossary's "avoid" vocabulary.
- The category caution and the do-not-say list are binding.
- Proof on screen only with status Site or Linked. One customer's words are presented as one customer's words.
- **Never invent the product's interface.** Use real screenshots supplied by the client, or keep the phone screen out of focus. Say which in the picture column.
- Never a real customer's name next to a generated face.

## Step 5. Production handoff

Under the beat sheet, list what the next stages need:

1. **Cast:** each person with age range, look, wardrobe, and which beats they appear in.
2. **Location:** each place with time of day and the light.
3. **Props:** including the phone and what is on its screen.
4. **Title cards:** every on-screen text in order, marked hook, support or brand line.
5. **Voice:** the clean spoken script with the word count.
6. **Sound and music:** the real sounds per beat and the music direction.
7. **Needed from the client:** logo file, product screenshots, permission for any quote.
8. **Asset sources:** for every image, font and logo the ad will use, where it comes from: this brand's site, this project's folder, or "to be supplied". Nothing from another project.

## Step 6. Check

Run the mechanical check, then the reading check.

```bash
python3 scripts/check_script.py path/to/AD_SCRIPT_file.md
```

It verifies that beats join, the length is right, speech fits the budget and no long dash slipped in. Fix the script, not the thresholds.

Then read it once as the audience: does the first three seconds say who this is for? Is the result visible? Did any line break the caution?

## Output

`scripts/AD_SCRIPT_<category>_<topic>_<length>s.md` in the brand's library folder:

1. Request and premise sentence
2. Material pulled from the library
3. Beat sheet
4. Production handoff
5. Left out and why
6. Open points for the client

Write one script first. Offer the other categories or lengths only after it is approved.

## Routing after the script

This skill stops at the script. Generation is done by the pipeline's existing skills; do not write new generation rules here.

| Next step | Existing pipeline skill |
|---|---|
| Brand look and reference set | `reference-style-builder` (style card from the brand's own photos) |
| Cast references | `character-identity-lock-setup` |
| Shot size per beat | `storyboard-shot-selection` |
| Still prompts | `cinematic-prompt-writer` |
| One keyframe per beat, as a chain | `keyframe-chain-builder` |
| Frame checks | `frame-qc-contact-sheet`, then `independent-frame-critic` |
| Video prompts | `seedance-prompt-writer` or `cinema-director-v3`, with `video-clip-continuity-chain` |
| To-camera packaging | `retention-packaging-plan` |
| Motion graphics and titles | `hyperframes`, `cinematic-motion-graphics` |
| Sound | `opus-sound-layer`, from the Sound column |

Pass each of them the script file: the beat sheet and the production handoff are their brief. Stop for the user's approval after the reference images and before any video.
