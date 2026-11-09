# Motion timing for cinema

Documentary graphics move like a camera operator and a hand with a pen, not like an interface. Slower eases, longer holds, one idea
at a time. All numbers are at 24 fps (1 frame = 41.7 ms).

## 1. Read time

- **Rule:** fully readable hold >= max(1.5 s, words / 3). Count numbers, dates and initials as words. `spec_lint.py` enforces it
  (`--wps` and `--min-hold` adjust it for a slower audience or a second language).
- The hold starts when the entrance ends, not when it starts. A typewriter line is readable only after its last character.
- Add about 0.5 s for a line the viewer must compare or calculate (two dates, a number against a silhouette).
- Two texts that enter together are one reading unit: sum their words.
- If the hold does not fit the narration beat, cut words (ask the user), do not speed the reading.

## 2. Eases and durations

| Move | Ease | Duration (frames at 24) |
|---|---|---|
| Fade in / out of type | `sine.inOut`, `sine.out` | 12-20 in, 14-20 out |
| Short travel (8-24 px) with a fade | `sine.out`, `power2.out` | 14-24 |
| Line or ink draw-on | `power1.inOut` (or `none` with a slow-in at stops) | by length: 300-500 px per second |
| Typewriter | stepped, one character per 2-4 frames | |
| Rule / underline draw | `power2.inOut` | 18-30 |
| Count-up to a final value | `power2.out` / `power3.out` | 30-48, then hold |
| Camera push or drift | `sine.inOut` or `none` | the whole shot, 2-6 % scale total |

Never `back`, `elastic` or `bounce`; never an overshoot past a held value; never a scale-pop entrance. Everything lands and stops.

## 3. Structure of one graphic

1. **Arrive** with the narration's naming word (in-time = start of that word; see the board recipes in `motion-graphics-director`).
2. **Build** in reading order, at most three elements moving at once; the rest staggered by 6-12 frames.
3. **Hold** still. The only motion allowed during a hold is one slow camera drift or push (one camera move per graphic) and the grain.
4. **Leave** on a cut, a dissolve, or a slow fade at the end of the sentence, never in the middle of a word. Between graphics the
   transition is the exit; no slide-outs.

## 4. Primitive vocabulary (cinema versions)

| Primitive | What it looks like | GSAP shape (seek-safe) |
|---|---|---|
| `ink_draw` | a pen line travelling along a path | `strokeDashoffset` from length to 0 |
| `marker_ride` | a ship or pin travelling with the line head | proxy progress -> `getPointAtLength` in `onUpdate` |
| `typewriter` | characters struck one by one | proxy count -> per-character opacity in `onUpdate` |
| `stamp_press` | a rubber stamp or letterpress strike | opacity 0 -> 1 over 2 frames + 1 px blur -> 0 over 4; no scale |
| `ink_pool` | a dot at a stop that spreads | circle radius 0 -> r, `sine.out`, 10-14 frames |
| `clock_settle` | minutes ticking, slowing onto the event | proxy minutes -> formatted text, `power2.out` |
| `count_settle` | a number counting and settling exactly | proxy value -> formatted text, tabular numerals |
| `rule_draw` | a ledger or underline rule | `scaleX` 0 -> 1, origin left |
| `rack_reveal` | a plane comes into focus | blur 6 px -> 0 + opacity, on a non-text plane |
| `push_in` | the camera leans into the plate | wrapper scale 1.00 -> 1.04 over the shot |
| `drift_hold` | the camera breathes during a hold | wrapper x/y 6-12 px over the hold |
| `paper_slide` | a document slid onto the desk | y 20-40 px + slight rotation 0.5-1 degree, `sine.out` |
| `iris` / `dip` | open from or close to black | radial mask or a black solid, 12-24 frames |
| `highlight_pen` | a grease-pencil or ink underline under a phrase | `background-size` or path draw, after the text settles |

Every state is derived from the timeline position (a proxy tween with `onUpdate`), never from a call that fires once, a timer or the
wall clock. Delayed elements use `fromTo` with an explicit hidden start.

## 5. Sync

- Lock the graphic to the cut: in-point on a frame of the cut plan, out-point on a cut or the end of a sentence.
- Use `music-beat-grid` only when the edit is cut on music; a documentary graphic usually follows the voice, not the beat.
- A count, a clock or a line arriving at a stop lands on the stressed word.
