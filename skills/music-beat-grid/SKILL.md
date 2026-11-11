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

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

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

## 7. Music video from generated shots (the two soundtracks)

Music written inside a generated shot restarts in a new key at every cut, so the score always comes from outside the video
model: the supplied master. What the model makes is only the sound bolted to the picture. Decide before generating (adapted from
scenario-labs/skills `scenario-seedance-music-video`, MIT):

- **Song alone:** generate every shot without audio. Lay the master once at the end and stream-copy it, so the delivered
  soundtrack is the master bit for bit.
- **Song over the shots' own sound:** generate with audio, every prompt naming only what the scene makes after "Diegetic sound
  only:" (heels on wet asphalt, room tone). Never name an instrument or genre and never write "no music": both have triggered
  audio refusals or a self-scored shot. Mix the clips under the master at 0.1 to 0.3 gain, master at unity.

Per shot: generate one or two seconds longer than its slot for a trim handle. To land an action on a beat inside a shot,
timecode it from the clip's start: beat time minus the shot's start in the edit, plus any planned head trim. One camera move and
one dominant action per shot; a prompt describing a sequence makes the model cut inside the clip. When a state must carry across
a cut, pass the outgoing state as the next shot's first frame (reference mode restarts every shot from its base state).

Assembly rules: each shot runs until the next one starts (no gaps), every start snaps to a frame of the grid, clips are conformed
to one fps and size first, and the master is never trimmed, normalized, faded or re-encoded by hand. Song alone, after the
picture-only concat:

```
ffmpeg -i cut_silent.mp4 -i audio/master.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -shortest out.mp4
```

(use `-c:a copy` when the master is AAC already). Record the master's hash (`shasum -a 256`) in the edit notes and check it is
unchanged before delivery.

Judging clips: a sparse contact sheet makes a continuous camera move look like a hard cut. Measure: downscale to about 160x90,
take the mean absolute difference between consecutive frames, and call it a cut only where it spikes far above the clip's own
baseline. Watch the delivery once with sound and once muted.

## Never

- Never beat-lock by default; ask, and default to holds for slow pieces.
- Never use the full-band phase when it disagrees with the kick phase.
- Never splice in the middle of a beat or without a short crossfade; a click at the join is a fail.
- Never generate or buy music without a yes on the service and cost, and never lift music from a reference.
- Never claim a cut is on the beat without running `snap` on the final cut times.
