---
name: period-fact-check
description: >-
  Verifies the historical facts of a shot BEFORE its prompt is written — dates, time of day, liveries and camouflage colours, construction
  stage, who was where, what machines and uniforms looked like — from a real source (encyclopedia article, museum page), records the facts
  in the plan, and turns each one into an explicit prompt line. Also answers the user's "why does X look like this?" with sourced facts.
  Use when a shot depicts a real historical event, ship, vehicle, place or person; when the user sends a source link (e.g. Wikipedia); or
  when QC finds an anachronism.
user-invocable: true
---

# Period Fact Check

AI models draw the *typical* version of a thing. History is specific. Some examples of the gap:
- a ship in its wartime colours is not the ship in its usual livery;
- a hull on the slipway has no funnels yet;
- a ramming at dawn is not a ramming at noon.

Every shot of a real event gets a short fact pass.

## 1. List the checkable claims of the shot

For each shot, write what the image will assert:
- **When:** the date and the time of day. The weather too, if recorded.
- **Where:** the city and the exact place, plus the architecture and materials there.
- **What:** the object's state on that date: colours and livery, stage of construction, damage, smoke or no smoke, how many of a
  signature feature.
- **Who:** which people were present, and who did what. Who rescued whom, who did *not* stop.
- **Equipment and dress:** uniforms, tools, vehicles and newspapers of the exact year.

## 2. Check them against a source

- Prefer the article the user sent. Otherwise use an encyclopedia or museum page.
- Search inside the page for the key words and quote the relevant sentence to yourself.
- Note conflicts. Example: one source says the camouflage was black and white, another says brown, dark blue, light blue and white.
  Prefer the more specific, cited source and tell the user which one you used.

## 3. Write the facts down

- Put the verified facts at the top of the plan or job file: one line each, with the source.
- Later fixes reuse these lines instead of re-researching.

## 4. Turn every fact into a prompt line

Write positive facts plus the negative that the model gets wrong by default:
```
ACCURACY: <ship> in 1917–18 dazzle camouflage in brown, dark blue, light blue and white — no black, no grey; the stripes cover the funnels too.
ACCURACY: on the slipway the hull is BARE — no funnels, no masts, no superstructure.
ACCURACY: she did not stop to pick up survivors; the survivors in the water were rescued later by another ship.
```

## 5. When the user asks "why does it look like this?"

Answer with the sourced fact in 3–5 sentences: what it was, why it was used, and when it applied to this shot. Then offer the
alternatives and their accuracy trade-off, for example "the accurate colours / the usual livery for recognisability (less accurate)".
Let the user choose before you regenerate.

## Never

- Never invent a precise number, name or quote without a source. Say "about" or leave it out.
- Never let a recognisability wish silently override a verified fact. Make it a visible, user-approved choice.
