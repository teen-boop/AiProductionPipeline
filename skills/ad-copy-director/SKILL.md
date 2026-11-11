---
name: ad-copy-director
description: Entry point for ad and commercial texts. Takes a topic, a brand or a few keywords, looks them up in the ad research library (one Ad Glossary per brand), and writes texts built only from researched words - hooks, on-screen ad lines, headlines, captions, button labels, title cards and short video scripts. Routes to ad-research-glossary when the library has no research for the brand or the keyword. Use when asked to write ads, hooks, ad copy, captions, slogans, taglines, title text or a commercial script for a brand or topic, to "generate texts for this keyword", or when it is unclear which ad skill to start with. Triggers - write ads for, hooks for, ad copy, ad texts, keyword to ads, caption for the ad, commercial script, what do we say about X.
---

# Ad Copy Director

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

Entry point for the words in the ad pipeline: **research -> texts and script -> images -> video -> titles -> edit -> effects and sound -> final**.

This skill never writes from memory. It looks the request up in the research library and writes only with what it finds there. If the library is empty for the topic, the research runs first.

## The research library

One folder per brand, each holding the `AD_GLOSSARY.md` written by the `ad-research-glossary` skill.

```
<library root>/
  <brand-slug>/AD_GLOSSARY.md
  <brand-slug>/texts/AD_TEXTS_<topic>.md     <- what this skill writes
```

Library root: the `AD_LIBRARY` environment variable, else `~/ad-research-library`. A project may keep its glossary elsewhere and link it into the library.

Look things up with the script, not by reading whole files:

```bash
python3 scripts/lookup.py --list                  # brands in the library
python3 scripts/lookup.py -b BRAND price fresh     # rows that use these words (a brand is always required)
python3 scripts/lookup.py -b BRAND --section 8    # the whole do-not-say list
python3 scripts/lookup.py -b BRAND --section 2    # the audience categories
python3 scripts/lookup.py -b BRAND -c A6          # everything tagged for one category
python3 scripts/lookup.py -b BRAND -c A6 price    # one category, narrowed by keyword
```


## Step 1. Read the request

Settle four things. Take them from the request when they are there; ask one short question only for what changes the output.

| Item | Default |
|---|---|
| Brand or topic | Required |
| Keywords | From the request; else the top angles in section 10 of the glossary |
| Text type | On-screen ad lines |
| Audience category | One category per text. If the request names none, show the category list (section 2) and ask which, or write one small set for each of the top three |

## Step 2. Find the research

1. Run `lookup.py --list`. If the brand has no glossary, stop writing and run `ad-research-glossary` (lean depth) first.
2. Run `lookup.py -b BRAND <keywords>`. Add plain synonyms the audience would use (price, cost, fee, bill).
3. If nothing matches, say so. Do not write around the gap: either pick the nearest pain row and tell the user which one, or update the glossary first.
4. Pull the target category with `-c CODE`. Read its row in section 2: the one problem, where it is reached and its **caution**. The caution is binding for every text aimed at that category.
5. Always read section 8 (do not say) for the brand before writing a single line.

## Step 3. Pick the material

Work one category at a time. A text written for one category is never reused for another: each has its own problem and its own words.

From the matched rows take, for each text:

- one **pain row** (section 5) tagged with the target category: the pain, the product answer and the result line;
- one or two **audience phrases** (sections 2 and 3) for the wording;
- the **plain product term** with its caveat (section 4);
- **proof** only if its status allows it (section 7).

Status rules: Site and Linked may appear on screen. Self-reported only with the company's footnote. Archive is for wording only, never attributed. Do not use means do not use.

## Step 4. Write

Write a small batch first: five to eight texts, or one set per audience category. Show it before producing more.

| Text type | Shape | Limits |
|---|---|---|
| Hook | First words of a video or the top line | Passes the context test below: who, situation, what they get. Usually 8 to 14 words, built from an audience phrase |
| On-screen ad line | One line plus one button, under a picture | Ends on the result; may be short because the picture gives the context; no second tagline |
| Headline | Platform headline under the creative | Up to about 40 characters |
| Primary text / caption | Two to four short sentences | Pain in their words, the answer, the offer, one call to action |
| Button | Two or three words | Matches the promise: "See how", "See the secret", "Start free" |
| Title card | Text animated on screen | Three to six words per card, one idea each |
| Video script, 15 to 30 s | Hook, pain, answer, proof, result, call to action | One pain row per script; every line shootable |

## What counts as a hook

A hook must carry its own context. Read it cold, with no picture, no brand and no line before it. A stranger has to be able to tell three things:

1. **Who** it is for (the category, named or unmistakable).
2. **The situation** they are in (the problem or the moment).
3. **What they get** by staying (a result, an answer, or an open question worth the next second).

If one of the three is missing, it is a fragment, not a hook. Length follows from that: usually 8 to 14 words.

| Fragment (no context) | Hook (context inside) |
|---|---|
| [Short question]? Start here. | [Audience, named]: you don't need [what they think they lack] to [result]. |
| [Two-word warning]. [Command]. | [Audience]: [the moment the problem happens] is why [the cost they pay]. |
| Stop [annoying thing]. | [Audience]: stop [what they do now] until [the bad outcome]. |

The examples are patterns on purpose. Fill them only with words from the brand being worked on, never with lines written for another brand.

Formats that carry context by design: "The secret [who] use to [result]", "How one [kind of business] went from A to B", "[Who], has a client ever said: [objection]?".

Short lines without context still have a place, but as **on-screen ad lines or title cards** that sit under a picture, never as the hook.

Line formats to fill come from section 9 of the glossary (secret, growth story, promise, their rule and our tool, handle the rest, customer said, deadline).

Rules for every text:

- It ends on what the customer gets.
- It uses the audience's words and none of the words listed as "avoid".
- It respects every caveat: an add-on is not described as included.
- No number that is not in the proof bank.
- No long dashes in on-screen text.

## Step 5. Check and trace

Before showing anything, check each text against section 8 and drop or fix what fails. Then tag every text with where it came from, so a reader can audit it:

`A6 · pain 4 · phrase "Ready before the doors open" (Archive, wording only) · term: same-day pickup (Site)`

## Output

Write `texts/AD_TEXTS_<topic>.md` in the brand's library folder, or in the project's research folder when the user is working inside a project:

1. Request: brand, keywords, text type, audience.
2. What the library returned: the pain rows and phrases used.
3. The texts, grouped by audience category, each with its trace line.
4. Left out and why: lines dropped by the do-not-say check, keywords with no research.
5. Next stage: which texts go to image prompts, which to title cards, which to the script.

## Routing

| The request is really | Go to |
|---|---|
| No research for this brand or keyword | `ad-research-glossary` |
| A full story or long-form script | the pipeline's script skills |
| Animated title text from these lines | the title and motion-graphics stage |
| Static ad images from these lines | the image stage |

## Check before you hand over

- Every text has a trace line that points at real glossary rows.
- Every hook passes the context test: who, situation, what they get.
- Nothing from the do-not-say list survived.
- Every text names its one category, and respects that category's caution.
- The batch is small and grouped by audience category.
- You told the user which keywords had no research behind them.
