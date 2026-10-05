# Multi-Shot Adaptation Inside One Location

## Principle

When a master / wide shot of a location already exists, every subsequent prompt that stays in the same location must be written as an adaptation of that master image.

The goal is visual continuity suitable for animation editing: same clothing appearance, same background elements, same lighting, same color palette.

## Typical Sequence

1. Prompt 1 → Wide shot (master). Character sitting on sofa, full environment visible, face already correct.
2. Prompt 2 → Close-up of face. Must keep the same t-shirt collar, same sofa texture at the edges, same light direction.
3. Prompt 3 → Medium shot or slight angle change. Still locked to the same master.
4. Prompt 4 → Detail (hands, object). Background and clothing still match the master.

## How to Write the Adapted Prompt

Always include language similar to:

"Using the provided master wide-shot image as the strict visual base, create a [close-up / medium shot / new angle] of [subject]. 
Keep the exact same clothing, the exact same background elements and colors, the exact same lighting and art style. 
Only change the camera framing and focus as required by the script. 
Do not regenerate or reinterpret the environment or the costume."

## What Must Stay Identical

- Clothing color, folds, logo absence/presence, fabric look
- Background furniture, walls, windows, props
- Lighting direction, color temperature, shadows
- Overall art style and rendering quality

## What May Change

- Framing (wide → close-up)
- Camera height or slight angle
- Focus point (face, hands, object)
- Small action or expression required by the current script beat
- Crop

## Output Note

In the final prompt list always mark adapted prompts clearly:

Prompt 3 (adaptation of Prompt 1 master wide shot):
...
Base image: result of Prompt 1
