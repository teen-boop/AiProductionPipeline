# Face Replacement Templates

## Master Template (adapt per frame)

Edit Image A only in the face region. Image A is the base and source of truth for everything except facial identity: keep the exact same background, the exact same body pose and position, the exact same [hair description], the exact same [clothing description], the exact same [lighting description], and the exact same [art style]. Do not regenerate, shift, crop, or reinterpret the background or body — treat them as fixed and untouched.

Image B is used strictly as a facial identity reference — take only bone structure, eye shape, nose shape, mouth shape, and general facial likeness from Image B.

Task: Replace only the face inside Image A with a face that has Image B's facial identity, but sculpt and adapt that face to exactly match Image A's existing head angle, head tilt, and gaze direction ([describe the exact gaze, e.g. looking slightly downward and to the side]). Do not import Image B's head angle or pose. Also adapt the new face to express Image A's exact original emotion: [describe emotion, e.g. soft, melancholic, tired, distant expression, eyes half-lowered, lips gently closed]. Do not transfer Image B's expression under any circumstance.

Think of this as sculpting Image B's facial identity onto Image A's existing head pose and expression, not pasting Image B's face as-is. Everything outside the face — hair, clothing, pose, background, lighting, art style — must remain pixel-consistent with Image A.

## Short Version for Quick Use

Keep everything in Image A completely unchanged except the face. Replace only the face with the facial identity from Image B (bone structure, eyes, nose, mouth). Match Image A's exact head angle, tilt, gaze and original emotion. Do not change hair, body, clothes, background, lighting or style.

## Notes

- Prefer GPT Image 2.0 for this operation.
- Always specify the required emotion and head orientation of the current frame.
- If clothing needs a small change (e.g. remove logo), state it explicitly inside the "keep the exact same clothing" clause.
- Secondary characters follow the same rule: each face must be forced to its own locked reference.
