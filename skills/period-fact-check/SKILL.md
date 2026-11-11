---
name: period-fact-check
description: >-
  Verifies the historical facts of a shot BEFORE its prompt is written — dates, time of day, liveries and paint schemes, construction
  stage, who was where, what machines and uniforms looked like — from a real source (encyclopedia article, museum page), records the facts
  in the plan, and turns each one into an explicit prompt line. Also answers the user's "why does X look like this?" with sourced facts.
  Use when a shot depicts a real historical event, vehicle, building, place or person; when the user sends a source link (e.g. Wikipedia); or
  when QC finds an anachronism.
user-invocable: true
---

# Period Fact Check

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

AI models draw the *typical* version of a thing. History is specific. Some examples of the gap:
- a vehicle in its special-event colours is not the vehicle in its usual livery;
- a building under construction has no roof yet;
- an event at dawn is not the same event at noon.

Every shot of a real event gets a short fact pass.

## 1. List the checkable claims of the shot

For each shot, write what the image will assert:
- **When:** the date and the time of day. The weather too, if recorded.
- **Where:** the city and the exact place, plus the architecture and materials there.
- **What:** the object's state on that date: colours and livery, stage of construction, damage, lights on or off, how many of a
  signature feature.
- **Who:** which people were present, and who did what. Who arrived first, and who was *not* there.
- **Equipment and dress:** uniforms, tools, vehicles and printed matter of the exact year.

## 2. Check them against a source

- Prefer the article the user sent. Otherwise use an encyclopedia or museum page.
- Search inside the page for the key words and quote the relevant sentence to yourself.
- Note conflicts. Example: one source says the paint scheme was two colours, another names four specific colours.
  Prefer the more specific, cited source and tell the user which one you used.

## 3. Write the facts down

- Put the verified facts at the top of the plan or job file: one line each, with the source.
- Later fixes reuse these lines instead of re-researching.

## 4. Turn every fact into a prompt line

Write positive facts plus the negative that the model gets wrong by default:
```
ACCURACY: <vehicle> in its <year> paint scheme in colour A, colour B and colour C — no colour D; the stripes cover the roof too.
ACCURACY: at this stage the building is a BARE frame — no roof, no windows, no signage.
ACCURACY: Person A was not present at the event; Person B arrived an hour later and did the task.
```

## 5. When the user asks "why does it look like this?"

Answer with the sourced fact in 3–5 sentences: what it was, why it was used, and when it applied to this shot. Then offer the
alternatives and their accuracy trade-off, for example "the accurate colours / the usual livery for recognisability (less accurate)".
Let the user choose before you regenerate.

## Never

- Never invent a precise number, name or quote without a source. Say "about" or leave it out.
- Never let a recognisability wish silently override a verified fact. Make it a visible, user-approved choice.
