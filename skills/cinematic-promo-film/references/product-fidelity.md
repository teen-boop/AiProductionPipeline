# Product fidelity - keeping a real product exact across generations

Image and video models love to "improve" objects: they round corners, add buttons, swap materials, invent a second logo
and turn label text into plausible nonsense. In a promo this is not a style problem, it is a factual error the client
will reject (and in some categories a legal problem). This file is the lock.

## 1. Principle

The product is **attached, never described into existence**. Every shot where the product is visible carries the product
reference sheet as an image reference, a fixed product line in the prompt, and a role line. Any legible text or logo in
the final film comes from the client's real artwork, composited, not generated.

## 2. Inputs to collect (Step 0)

| Input | Why |
|-------|-----|
| Real photos: front, three-quarter, side, back, top, label close-up, in a hand for scale | shape, proportions and scale |
| Colour spec: hex or Pantone of body, cap, label, accents; finish (matte, gloss, satin, metallic) | colour and material |
| Vector artwork of label and logo | legible text in post |
| 3D model or CAD file, if one exists | best source for packshots and hard angles |
| Variants (sizes, colours) and which one this film shows | avoids mixing variants |
| What the product must never look like (dents, wrong orientation, open in unsafe ways) | banned states |

If only one photo exists, say so: fidelity at unseen angles will be weak, so plan shots that show the known side, or ask
the client for more photos before generation starts.

## 3. Build the product reference sheet (Step 2)

1. Clean the real photos: neutral grey background, even soft light, no reflections of the photographer, colour checked
   against the spec. If a photo must be re-lit, re-light with local tools; never let a model redraw the object.
2. Lay out a sheet: three-quarter hero view large, front, side, back and a label close-up smaller, a scale strip (product
   next to a hand or a ruler).
3. Write `PRODUCT_LOCK.md`:
   - **Product line** (pasted verbatim into every prompt with the product; 25-45 words): object type, exact silhouette words,
     proportions as ratios ("height about 2.4 times width"), materials and finishes, colours by name with hex, label
     position, counts of distinctive features ("two buttons on the right side", "four screws on the base").
   - **Role line** for the sheet: "controls this product's shape, proportions, colour, materials and label layout only -
     never the background, light or camera".
   - **Measured targets:** aspect ratio of the silhouette from the photos, main colours in Lab measured on the clean photos,
     feature counts.
   - **Banned states** from the brief.
4. Approve the sheet with the user before any scene generation.

## 4. Prompting rules

- Attach the product sheet in every shot where the product is visible; attach the style frame last (style references
  after content references, per `style-lock-guard`).
- Paste the product line verbatim. Do not paraphrase it per shot, do not add adjectives like "sleek" or "futuristic" that
  invite a redesign.
- Describe the scene and light around the product, not the product itself, beyond the product line.
- Keep the product at a size the model can hold: very small in frame (under about 5 % of the area) it melts; extremely
  large and cropped it gets reinvented. Hero shots work best with the product at 20-50 % of frame height.
- One product per frame unless the brief needs several; multiple copies drift independently.
- Text on the product: prompt it as "label artwork as in the reference, small and soft" and plan to composite the real
  label in post wherever it is legible.
- Shallow depth of field is your friend: put the focal plane on the most recognisable feature; let secondary details fall
  soft rather than letting the model invent them sharp.

## 5. Shot strategies by product visibility

| Visibility | Strategy |
|------------|----------|
| None (world, people, effect) | no sheet needed; keep the brand palette and the product's colour as a motif |
| Soft (out of focus, in background, in motion) | sheet attached; silhouette and colour must match; text may be soft |
| Hero (in focus, large, label visible) | sheet attached; QC every take; plan a label composite |
| Packshot (final held frame) | composite: approved generated environment + real product photo or 3D render, matched light and grade, shadow and reflection painted in |

## 6. Video (image-to-video) rules

- Start from an approved still that already passed QC; give the end frame too when the model supports it.
- Move the camera around a still product; avoid the product rotating, opening or deforming unless the brief needs it.
- Keep clips 4-5 s; longer clips drift more.
- Use moves that keep the product's silhouette readable: slow push, small arc (under about 20 degrees), slide, rack focus.
  Avoid fast orbits that require the model to invent the unseen back.
- Inspect the **middle** of every take (frames at 25 %, 50 %, 75 %), not only the first and last; morphing usually happens
  mid-clip and recovers by the end frame.
- If a take is perfect except for a short morph, use only the clean part in the edit; note the usable in and out in the log.

## 7. QC checklist (every frame and every take with the product)

Run on the contact sheet from `frame-qc-contact-sheet`, with the product sheet beside each frame.

| # | Check | Pass when |
|---|-------|-----------|
| 1 | Silhouette | overlay of the outline on the reference at the same angle matches; no extra or missing parts |
| 2 | Proportions | height to width ratio within about 3 % of the measured target (same viewing angle) |
| 3 | Colour | main colours within a small Lab distance of the targets after the grade (aim for delta E under about 5 on the body colour; the grade may shift light, never hue of the product) |
| 4 | Material and finish | matte stays matte, metal stays metal, transparency correct |
| 5 | Feature counts | buttons, holes, screws, seams, stripes as specified |
| 6 | Label layout | label in the right place, right size, right orientation; no second logo |
| 7 | Text | no invented legible text; any legible text is the real artwork (composited) |
| 8 | Scale | size relative to hands, faces and furniture is plausible and consistent |
| 9 | State | not open, broken, dirty or used in a banned way |
| 10 | Variant | same variant (size, colour) as the brief, in every shot |
| 11 | Physics | sits on surfaces, casts a shadow, reflections agree with the light, hands hold it believably |
| 12 | Motion (video) | no morph, melt or swap at 25 / 50 / 75 % of the take |

Write one line per failed frame: shot id, check number, what is wrong, proposed fix. A frame that fails any of checks 1-7
or 10 is rejected, even if it is the most beautiful frame in the batch.

## 8. Fixes, cheapest first

1. **Re-roll** the same prompt with the sheet attached (models vary; one more take often fixes a small drift).
2. **Tighten the prompt:** move the product line earlier; remove adjectives near the product; reduce scene complexity.
3. **Change the framing:** the product smaller, softer or partly occluded, if the story allows.
4. **Region fix:** inpaint only the product region using the product sheet as the reference; keep the rest of the frame.
5. **Composite:** cut out the real product photo or a 3D render, match perspective, light direction, colour temperature,
   grain and depth of field, paint contact shadow and reflections. This is the default for packshots and legible labels.
6. **Label replace in video:** track the label surface in the editor or compositor and replace it with the vector artwork;
   keep it slightly soft to match the shot.
7. **Cut around it:** use only the frames that pass; restructure the shot with an insert.

Record which fix was used in `generation-log` so the recipe can be repeated for the next shot.

## 9. Talent with the product

People holding or using the product combine two locks: the identity lock (`character-identity-lock-setup`) and this one.
Generate the person's shot first with the product soft or absent, then bring the product into the hand by a change-to
edit from that frame with the product sheet attached, or composite it. Hands are the weak point: check finger count, grip
and contact on every take.

## 10. Sign-off

Before Step 5, show the client a product-only contact sheet: every frame where the product is visible, next to the
reference sheet. The client approves product fidelity separately from the story and the look.
