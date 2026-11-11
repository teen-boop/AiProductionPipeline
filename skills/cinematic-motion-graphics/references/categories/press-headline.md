# press-headline - archival newspaper, telegram and document reveals

## Intent

The world reacting: a front page, a telegram, an official document, revealed as a physical object in the film's light. The
plate is a still (generated through `press-clipping-engine` or the project's own scan); the motion and every readable word are code.

## When to use

- The narration quotes or summarises what the papers or a message said.
- A turning point is best told by the document that announced it (a telegram, a list of names, a notice).
- Not for invented drama dressed as a real paper: a real masthead with invented text is never presented as genuine.

## Plate (two routes)

1. **Project scan** of a real page (rights cleared): the text is real; transcribe the headline into the spec and cite the issue.
2. **Generated plate** via `press-clipping-engine` (archetypes such as `editorial-broadsheet` or `torn-stack`, the project's chosen
   archetype kept across the batch), after the user's yes. Generated small text is gibberish: ask for the plate **without** a
   readable headline (blank or blurred headline area, period column rules, halftone photo area), then set the approved headline in
   code on top, in a period face, matched in perspective and paper. The masthead is either the real paper's (only with a real
   transcribed headline) or a neutral, user-approved one.

Run the plate prompt through `style-lock-guard` lint before it is sent, and compare the result after.

## Layout

- The page sits like a photographed object: slightly rotated (0.5-2 degrees), lit from one side, edges falling into shadow.
- The headline occupies the upper third of the frame at the hold; the keyword is fully inside title-safe.
- Telegram / cable form: the period form layout (printed form fields, typed or pencilled message); message text typed on.

## Motion

- One camera move: a slow `push_in` toward the headline (or a slow tilt down the column), 3-6 % over the shot.
- `paper_slide` if the page arrives on a desk; `rack_reveal` if it comes into focus.
- `highlight_pen` on the keyword after the text has settled and been readable: a grease-pencil or ink underline, or a soft
  yellowed marker band at low opacity. Never a neon highlighter, never before the reader has read it.
- Torn edge: a hand-torn mask (irregular, slightly fibrous), revealed with a short wipe; never a straight scissor cut.
- Halftone on photos: a fine dot screen (period newsprint), applied to the photo area only, not to type.
- Telegram: `typewriter` per line, or a pencil-written reveal at writing speed.

## Film look

Newsprint is warm grey-yellow, not white; ink is warm black. The page gets the film's grain, its light falloff and vignette. No
drop shadow box: the shadow is the desk's.

## Accuracy

- Paper name, date and edition; the headline wording exactly as printed (with its period spelling and punctuation).
- Telegrams: sender, receiver, time and wording from a source; the form type of that service and year.
- If a headline is a dramatised paraphrase, it is shown as such (no real masthead) and the user approves that choice.

## Spec example

```json
{
  "category": "press-headline", "period": 1900, "fps": 24,
  "canvas": { "w": 1920, "h": 1080, "aspect": "16:9" }, "duration_s": 9, "export": "mp4", "background": "plate",
  "texts": [ { "id": "headline", "text": "<exact headline as printed>", "approved": true, "in_s": 0.0, "enter_s": 0.0, "hold_s": 6.0 } ],
  "accuracy": [ { "claim": "<paper>, <date>, <edition>: headline wording", "source": "<archive / issue reference>", "status": "pending" } ],
  "assets": [ { "role": "page plate", "path": "plates/front_page_blank_headline.png", "origin": "generated", "user_approved": true } ],
  "content": { "document": { "kind": "broadsheet", "headline_area": [420, 140, 1080, 300], "keyword": "<one phrase>" },
               "camera": { "move": "push_in", "scale": [1.0, 1.05] }, "annotation": "highlight_pen" }
}
```

## QC

- Readable headline at the hold, at phone size; no gibberish letters anywhere readable.
- The code-set headline sits in the plate's perspective and paper (no floating clean text).
- Highlight starts after the headline has been readable for at least the read time of the keyword phrase.
