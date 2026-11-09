# Edit rules

The rhythm guide behind these rules is `otf-presentations/references/EDIT_PATTERNS.md` (measured on premium short pieces).
Read it before the first cut list. Where a trailer needs something that guide avoids (intertitles, a designed silence),
this file says so explicitly. The project's style lock overrides both.

## 1. Music first

- Source, in order: the project's own score; a track the user licenses; a generated track (paid: name the service and cost,
  wait for a yes). Never lift music from a reference video or a stock catalog the user did not choose. Write the source and
  license into `<run>/audio/MUSIC_SOURCE.txt`.
- Measure the track with `music-beat-grid` (`beat_grid.py measure --bars`): period, kick-band phase, and the bar energy
  table (intro, riser, drop, break, return). If it is unavailable, `npx hyperframes beats` gives a simpler grid.
- `music-beat-grid` asks whether to beat-lock. For a trailer the recommended answer is **accents locked, the rest free**:
  lock the cold-open hit, the turn into the escalation, the rhythm break, the peak cluster and the title hit (5-8 cuts);
  let every other cut follow the picture (gesture peaks, motion). For a mood piece: nothing locked.
- Splice the track to the trailer length on beat boundaries (`music-beat-grid` step 4), so the rhythm break is a real
  break in the music and the title lands on a downbeat.
- Generate the cut sheet from the structure's beats: `beat_grid.py sheet --fps 24 --chapters "Open:..., World:..., ..."`.
  After the edit, `beat_grid.py snap` on the final cut times; anything OFF GRID is moved or justified.

## 2. Rhythm

- Accelerate and release: open on 1.3-3 s, shorten through the escalation, the fastest cluster (0.4-0.6 s) just before the
  peak, then a long hold of 1.5-4x the median shot. No shot under 0.5 s in the first 1.5 s.
- Scale alternation: detail / medium / wide; never two neighbours at the same scale; a wide "breath" every 4-6 shots.
- Screen direction: keep the movement direction of the hero across the sequence.
- Faces in about one shot of three or four.
- A still on screen always has a 3-8 % push or drift and a second moving layer; a Ken Burns on a dead still is a fail.
- Never animate a clip the video model already moves, except a 1-3 % push to hide a drift.

## 3. Transitions

Hard cuts by default. Three designed exceptions, each used where it means something:

| Device | When | Recipe |
|---|---|---|
| Overexposure flash | the turn into the escalation, a jump in place or time | 1-2 frames up to near-white holding a ghost of the next shot, 0.30-0.40 s total, hard drop into the new shot. At most 2 per trailer. |
| Dip-to-black breath | between holds in slow pieces | darken over about 6 frames to about 15 %, rise over about 7 frames; never rest on black. One per 8-10 s at most. |
| Rhythm break | once, beat 5 of the full trailer | music cuts out; 0.8-2 s of black or one held image; at most one isolated world sound. This is the only place black is held. |

No wipes, spins, zoom-blurs, glitches, light-leak packs or slide transitions.

## 4. Typography in code

- Fonts come from the glyph-tested pairing in the `otf-presentations` context manifest. A font marked "no Cyrillic" never
  sets a Cyrillic version; check the flag for every language rendered. Load fonts with `@font-face` from files copied into
  the composition.
- Title card: small (about 2-4 % of frame height for the title, half that for the release line), centred or in the negative
  space of the last hold. Faded or typed on (about 0.2 s typing, pattern 28 of the rhythm guide); held at least 1.5 s plus
  0.3 s per word.
- Intertitles (full trailer and teaser only): at most 3, each a fragment of 2-6 words, on holds or on black, never over the
  first 1.5 s or over a fast cluster. Fade in 0.4-0.6 s, hold by the same rule.
- Fact cards (documentary): condensed or mono, small, lower third or centred on black, source in the plan (not on screen,
  unless the project asks).
- Release card: date or "coming soon" and the platform, in the version's language. No URL unless the user gives one.
- Never: a "Part N/M" or "Episode N" label over picture, a watermark, a channel bug, a logo slam, emoji.

## 5. Film look

- The look is the style lock: if it asks for deep blacks, warm practicals against a cool sky and rays, the trailer keeps
  exactly that. Never lift blacks or flatten contrast for a "film" feel when the lock forbids it.
- Grade all picked clips through one look with `video-color-grade` (match to the approved key frame when a clip drifted),
  BEFORE they enter the composition. Keep the `.cube` for the NLE hand-off.
- Grain and halation belong to the picture layer only:
  - if the clips already carry grain, add none;
  - otherwise one deterministic grain plate at low opacity (about 0.04-0.08) over the picture, and a subtle halation (a
    warm, blurred copy of the highlights above about 90 % luma, screen blend, low opacity);
  - never over title text: the text layer sits above the grain;
  - check for banding in dark gradients after encoding; if grain makes the encode smear, lower it.
- Never upscale more than 1.4x. No CSS blur on picture except deliberate depth on a background plate.
- Aspect: render each format from the composition, reframed per format with `frame-crop-guard`; never letterbox a 16:9 cut
  into 9:16.

## 6. Sound

- Music only by default. No SFX unless the user asks; the one isolated world sound in the rhythm break is the exception and
  is listed in the plan.
- Voice-over only when the user asks. Then the script is written in the user's words, timed to the picture, and mixed with
  `dialogue-audio-finish`.
- The ending holds on the music's last chord or tail; never cut on the last frame of the music.
- Delivery loudness about -14 LUFS integrated, true peak at or below -1 dBTP, unless the platform or the user says otherwise.

## 7. Frame rate, versions, language purity

- 24 fps by default (or the frame rate of the timeline it goes into). Conform every clip to 24 fps and one size before
  composing; render with `-f 24`.
- Each language is its own render from its own composition folder (`composition_en/`, `composition_ru/`): every on-screen
  line translated, longer lines re-checked for fit and hold time.
- Language purity: a version shows no text in another script. Before rendering, grep the composition for the other
  script (for Cyrillic: `[\u0400-\u04FF]`); after rendering, look at the frame-check sheet.
- File names: `<slug>_trailer_<lang>_<format>.mp4`, ASCII only.
