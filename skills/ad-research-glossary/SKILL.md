---
name: ad-research-glossary
description: Research a company, product or topic for ads and commercials and hand the script stage one file, the Ad Glossary - the audience's own words, the product's terms in plain language, an audience breakdown into targetable categories, a pain-to-problem-to-answer map, keywords, a proof bank, a do-not-say list and ready ad-line formats. Use at the start of any ad, commercial or promo, when asked to research a brand or website for ads, to find pains, problems, terms, keywords or hooks, to "use the right words" for an audience, or before writing any ad script. Triggers - ad research, ad glossary, research this site for ads, pains and keywords, terms and concepts, what words does the audience use, prepare the script stage.
---

# Ad Research Glossary

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

Stage 1 of the ad pipeline: **research -> script -> images -> video -> titles -> edit -> effects and sound -> final**.

The script stage writes badly when it has to guess the words. This skill ends in one file, `AD_GLOSSARY.md`, that holds every word, claim and angle an ad is allowed to use. Nothing else from the research travels forward.

## Inputs

Ask only for what is missing:

1. The company URL, or a topic if there is no company.
2. Who the ads talk to (industry, role, size). If unknown, the research proposes it.
3. The ad goal (trial, demo, sale, awareness) and platforms.
4. Depth: **lean** (default), **standard**, or **deep**.

| Depth | What is read | Use when |
|---|---|---|
| Lean | Research already on disk, plus the site's home, pricing, one feature or industry page and testimonials | Default. A first set of ads. |
| Standard | Lean, plus 10 to 20 audience sources (forums, comments, reviews) with links | A campaign. |
| Deep | Standard, plus competitor ads and review platforms | Only when the user asks. It costs many times more. |


## Step 0. Look in this brand's own folder first

Before any web call, check whether research for THIS brand already exists: its folder in the research library, its own project folder, files the user attached for it. Synthesize from those. Research done for other brands is out of bounds, even in the same industry.

If nothing exists for this brand, say so and research it from its link. With an empty folder the lean level is not enough for audience words: add a small audience pass (three to five searches) and state that cost before running it.

## Step 1. Product pass (the brand's words)

Read the site. For each feature the ads might mention, record:

- the brand's own term, exactly as written;
- the plain version a customer would say out loud;
- the plan it belongs to and any caveat (add-on, coming soon, not on the entry plan);
- the page link and the date checked.

Also record what the site does **not** offer when the audience would expect it. Those items go to the do-not-say list.

List every number the company claims (results, time or money saved, ratings, user counts). Mark each one: proven by a named source, self-reported with a footnote, or contradicted elsewhere on the same site.

## Step 2. Audience pass (their words)

Collect verbatim phrases from where the audience really talks: forums, video comments and captions, review sites, community groups. For each phrase keep the text exactly, who says it, the topic, the link and the date.

- Sort every phrase into an **audience category** (see Step 2b). Each category has its own problem, and no hook is shared across categories.
- Keep the everyday vocabulary (what they call the work, the buyer, the price, the product) and note the corporate words they never use.
- Also collect what **their customers say to them**. Objections make the strongest hooks.
- Treat promotional posts as suspect. A "discussion" that names a product in every reply is an ad. Leave it out or mark it.
- A phrase with no link is still useful for wording. Mark it as unsourced and never attribute it on screen.

## Step 2b. Audience categories (who each ad talks to)

Break the audience into categories before mapping pains. A category is a group that shares ONE problem and can be targeted on its own: by situation (new to the category, comparing options, unhappy with the current tool), not by demographics alone. Five to eight is usual. Give each a short code (A1, A2, ...).

For each category record: who they are, their one problem, two or three of their phrases with links, where to reach them, the product's answer, and a caution (what the product cannot honestly promise this group). Name the best hook found so far; it must make sense with no picture and no brand next to it.

A category with no real phrases behind it is a guess: mark it as a hypothesis.

## Step 3. Pain map

One row per pain, tagged with the category codes it belongs to. Every category needs at least one pain row. Every column is required; write "none" rather than leaving a gap.

| Cat. | Pain in their words | The problem behind it | What the product does | Proof we can show | Result line for the ad |
|---|---|---|---|---|---|

The result line states what the customer **gets**, not what hurts. If no product feature answers the pain, the pain does not go in an ad.

## Step 4. Keywords

Three lists: what they type into search, hashtags seen in real use, and copy keywords grouped by the job the product does. Mark targeting ideas as untested unless they were checked inside the ad platform.

## Step 5. Proof bank and do-not-say list

**Proof bank:** named customer quotes and numbers, each with exact wording and a status. A growth story needs a real, checkable customer.

**Do not say:** unsourced statistics, claims the site contradicts, features that do not exist, anything in the top complaint themes from reviews, phrasing the owner has rejected.

## Step 6. From words to ads

Turn the pain map into line formats the script stage can fill. Keep the formats that fit the account; these are a starting set:

| Format | Pattern |
|---|---|
| Secret | The secret [who] use to [result] |
| Growth story | How one [audience] company went from A to B |
| Promise | [Result] before / again / first |
| Their rule, our tool | [Their saying]. [Product answer]. |
| Handle the rest | [What you do]. [Chores]. We handle the rest. |
| Customer said | "[Audience], have you ever heard: [objection]?" |
| Deadline | [Season fact]. [Act now]. |

Rules for every line:

- It ends on the result. One line, one button.
- It is built from the audience's phrases.
- A hook carries its own context: read cold, it says who it is for, what situation they are in and what they get. A short fragment is an on-screen line, not a hook.
- It makes no claim that is not in the proof bank.
- On-screen text follows this project's text rules.
- Never put a real customer's name next to a generated face.

## Output: `AD_GLOSSARY.md`

Write the file in the project's research folder using `references/glossary-template.md`. The ten sections are fixed, so the script stage always knows where to look:

1. Snapshot
2. Audience categories
3. Audience words
4. Product words and the plain version
5. Pain map
6. Keywords
7. Proof bank
8. Do not say
9. From words to ads
10. Handoff to the script stage: the top five angles in order with their category, and what is thin

Every row carries a status: **Site**, **Linked**, **Archive** (unsourced), **Self-reported**, or **Do not use**.

## Handoff contract

The script stage may use:

- any audience phrase for wording;
- product terms only in their plain version and only with their caveat respected;
- proof with status Site or Linked on screen; Self-reported only with the company's footnote; Archive never on screen.

If the script needs a word, number or feature that is not in the glossary, the glossary is updated first.

## Check before you hand over

- Every category has a code, real phrases and at least one pain row.
- Every pain row has a category, a product answer and a result line.
- Every number has a status. No statistic without a source survived.
- The do-not-say list covers add-ons sold as included and features that do not exist.
- The "what is thin" note is honest: missing case studies, unsourced quotes, untested targeting.
- You read back to the user what was reused from disk and what was newly researched.
