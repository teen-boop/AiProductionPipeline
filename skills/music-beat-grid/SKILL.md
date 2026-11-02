---
name: music-beat-grid
description: >-
  Puts a music-driven edit (teaser, sizzle, showreel, montage, announcement) on a MEASURED beat grid: measures the track's real
  period and downbeat phase (kick band, so off-beat hats cannot pull every cut half a beat late), maps the energy per bar to find
  intro, riser, drop, break and return, splices the track to the target length on beat boundaries, lays chapters on the grid as a
  frame-exact cut sheet (with an accelerating flurry before the ending), and checks finished cut times against the grid. Use when
  the user says "cut it to the music", "on the beat", "beat sync", "make it 15/30 seconds with this track", "where is the drop",
  "the cuts feel late", or when building a fast montage in otf-presentations or an NLE. Includes scripts/beat_grid.py.
user-invocable: true
---

# Music Beat Grid

> **Optional — ask first.** Before using this skill, ask the user whether this edit should follow the music's beat grid at all (many premium pieces cut to the picture, not the beat). Run it only on a yes, and only when there is a final music track.

Our measured rhythm guide (`otf-presentations/references/EDIT_PATTERNS.md`) found that most premium AI reels are long holds and
that montage cuts in the references were NOT beat-locked. So beat sync is a choice, not a default. When the user does want a
music-driven cut, this skill makes it exact. Loudness, ducking and SFX mixing belong to `dialogue-audio-finish`.

## 1. Decide if the cut should be beat-locked

Ask once: "Lock the cuts to the music, or keep holds and let the music sit under them?"
- Locked: montages, flurries, sizzles, showreels, social teasers with a strong track.
- Not locked: one-take living stills, slow pieces, dialogue scenes. Then use this skill only to find the drop for one hit.

## 2. Get a track you may use

The user's licensed track, or a generated one. Generation is a paid call: name the service and cost and wait for a yes. Never
take music from a reference video. Write the source and license into `audio/MUSIC_SOURCE.txt`.

## 3. Measure

```
python3 scripts/beat_grid.py measure audio/track.wav --bars --json audio/grid.json
```

- Use the **kick-band phase**. When the script warns that the full-band phase disagrees, the hats are winning; trust the kick.
- Give `--bpm` when you know the nominal tempo; generated tracks drift from their prompt (asked 128, measured 129). Put the
  measured value, not the asked one, in any on-screen tempo label.
- In the bar table, a jump of about 8-10 dB in the low band is the drop. Note intro, riser, drop, break, return.

## 4. Splice to length (optional)

When the track is longer than the edit, cut it on beat boundaries with ffmpeg: each segment starts about 12 ms before its grid
point (so the transient survives) and joins with a 10-15 ms crossfade:

```
ffmpeg -i track.wav -filter_complex "[0:a]atrim=start=A1:end=B1,asetpts=PTS-STARTPTS[s0];[0:a]atrim=start=A2:end=B2,asetpts=PTS-STARTPTS[s1];[s0][s1]acrossfade=d=0.012[a]" -map "[a]" bed.wav
```

with `A = phase + beat * period - 0.012`. A typical 15 s structure at about 128 BPM (32 beats): intro and build 16 beats ending on
the drop's downbeat, drop 8, a break 4 under the flurry, then the return hit and a tail. Optionally duck the half beat before the
drop (about -16 dB) so the hit lands harder. Re-measure the spliced bed: its kick phase should be within about 25 ms of 0.

## 5. Cut sheet

```
python3 scripts/beat_grid.py sheet --period 0.4688 --phase 0.0 --fps 24 --length 15 \
  --chapters "Open:4, Build:8, Drop:8, Flurry:4, End:rest"
```

Paste the table into the storyboard or shot list. Rules for the edit:
- Hard cuts, flashes and inverts land within 2 frames of a beat or half beat. Animation moves on the off-beats.
- Accelerate, then hold: roughly 75 % development, 13 % flurry (one beat per cut, then half beats), 12 % resolve on a held end.
- The ending is a hold or a light event, never a cut on the last frame of the music.
- Shot length still follows the picture: a beat-locked cut does not justify a shot that says nothing.

## 6. Build and check

Build in `otf-presentations` (HyperFrames: compute every time as `phase + n * period`, never type seconds by hand) or in the NLE
via `nle-timeline-assembly`. Then check the real cut times:

```
python3 scripts/beat_grid.py snap --period 0.4688 --phase 0.0 --fps 24 --cuts "1.88,3.75,5.63"
```

Anything flagged OFF GRID is moved or justified. Then `render-cut-verification` on the encoded file, and `dialogue-audio-finish`
for the final mix and loudness.

## Never

- Never beat-lock by default; ask, and default to holds for slow pieces.
- Never use the full-band phase when it disagrees with the kick phase.
- Never splice in the middle of a beat or without a short crossfade; a click at the join is a fail.
- Never generate or buy music without a yes on the service and cost, and never lift music from a reference.
- Never claim a cut is on the beat without running `snap` on the final cut times.
