---
name: dialogue-audio-finish
description: >-
  Finishes dialogue and voice-over audio in a cut. It measures every edge at 1 ms (clipped onsets, cut-off words,
  s/sh/t tails, dead air, cuts inside continuous speech, level jumps between takes) and suggests exact new edges. It
  keeps sample-exact audio edges inside frame-snapped picture edges and fills the gaps with the take's own room tone.
  Each clip gets a 12 ms fade, and speech levels are matched across takes. It also covers ducking the music under
  voice and the delivery loudness pass (-14 LUFS integrated, true peak -1.5 dBTP, measured on the final stereo file).
  Use after dialogue-cut or nle-timeline-assembly, whenever clips with speech are trimmed (including generated
  Seedance, Kling or Veo clips), when the user says "a word is cut off", "the voice jumps", "dialogue is too quiet
  under the music", "mix the voice", "normalise the audio", or before render-cut-verification. Includes
  scripts/edge_qa.py.
user-invocable: true
---

# Dialogue Audio Finish

Picture cuts on frames, sound does not. At 24 fps a frame is 41.7 ms, longer than a consonant. A trim placed by eye or on a
round number lands inside a word more often than not. This skill measures every edge, moves it to a real pause, and mixes the
voice so it sits at the same level from clip to clip and above the music.

Method adapted from the Eyeline editing system (MIT, see the repository README); rewritten for this pipeline.

## 1. Measure the edges

```
python3 scripts/edge_qa.py plan edit/dialogue/dialogue_cut.candidate.json --out qc/edges --apply
```

It accepts a dialogue-cut plan (`source`, `in`, `out`) or a cut plan (`file`, `src_in`, `src_out`). Each clip is measured on
its SOURCE: an 8 ms RMS envelope every 1 ms in two bands, speech 80 to 8000 Hz and sibilants 3500 to 11000 Hz. The room floor
is the 12th percentile.

| Flag | Meaning | Suggested move |
|---|---|---|
| starts inside a sound | onset clipped (the edge is on a loud frame after silence) | back to where the level falls under floor+10, minus 30 ms |
| inside continuous speech | the cut is mid-phrase with no silence around it | to the nearest real pause within 0.6 s |
| ends inside a sound | last word cut off | forward until under floor+10, plus 14 ms |
| cuts an s/sh/t tail | high band still loud past the edge | forward until the tail decays, plus 14 ms |
| dead air | over 90 ms before the first sound, over 110 ms after the last | to the sound, keeping a plosive burst and the decay |
| level jump | over 7 dB between the voiced last 400 ms of a clip and the first 400 ms of the next one from another source | gain, see step 3 |

An edge that sits in a real dip (within 4 dB of the quietest point of ±40 ms, that point 12 dB under the local peak) is
accepted. `--apply` writes `<plan>.edges.json` with `audio_in`/`audio_out` (exact) and `in`/`out` (frame-snapped outward); the
original plan is untouched.

The report also gives, per source:
- speech level (70th percentile of the voiced envelope);
- the gain needed to reach the median of all sources;
- the quietest 1.5 s, to use as room tone.

**Then listen to every flagged edge.** The numbers are evidence. A short silence before a final t, k, p or d looks like a
finished word and is not one.

## 2. Build the edges in the timeline

- Picture: `in`/`out` on the frame grid. Audio: the linked audio item trimmed to `audio_in`/`audio_out`. Split the link in
  the NLE if needed, or lay the dialogue on its own track.
- Where the picture is longer than the audio, fill with the same take's room tone, never digital silence: silence under a
  shot sounds like a dropout.
- Every dialogue clip gets a 12 ms fade at both ends (ffmpeg `afade` with `curve=hsin`, or the NLE's default short crossfade).
  Two clips from the same take that continue each other (gap under about 230 ms) get one join at the envelope minimum and no
  fades.
- Clips from generated video with speech: the model's audio track is the take. Trim it with these edges too; never cut on a
  round number.

ffmpeg for one clip: picture snapped, audio exact, the take's room tone as a bed under the whole clip. Example with in 11.5,
out 15.7083, audio_in 11.504, audio_out 15.703, room tone at 4.0 s:

```
ffmpeg -ss 11.5 -t 4.2083 -i src.mp4 -ss 4.0 -t 4.2083 -i src.mp4 -filter_complex \
 "[0:a]atrim=0.004:4.203,asetpts=PTS-STARTPTS,afade=t=in:d=0.012:curve=hsin,afade=t=out:st=4.187:d=0.012:curve=hsin,adelay=4:all=1[v];\
  [1:a]volume=1[r];[r][v]amix=inputs=2:normalize=0:duration=first[a]" -map 0:v -map "[a]" -c:v libx264 -crf 18 clip.mp4
```

`atrim` is (audio_in - in) to (audio_out - in), the fade-out starts 12 ms before the audio length, `adelay` is
(audio_in - in) in ms. Re-encode the picture: `-c:v copy` after an input seek starts on a keyframe, not on your frame.

## 3. Level match

- Gain each source by `gain_to_median_db` from the report, or by ear when only two sources meet. Keep it as clip gain or a
  `volume=` filter; do not compress takes differently.
- Generated clips vary by up to 10 dB from shot to shot (seen between Seedance scenes). Match them before the music goes under.

## 4. Music under voice

- Bed about 18 dB under the voice. Duck it a further 8 to 10 dB inside every spoken stretch, with ramps of 150 to 300 ms. The
  ramps start before the first word.
- Windows come from the approved dialogue clips' record times (the `duck` field of nle-timeline-assembly).
- Without an NLE, the pipeline's ffmpeg pattern is `volume='if(between(t,A,B),0.16,1)':eval=frame` per window, or
  `sidechaincompress` keyed on the dialogue (threshold about 0.03, ratio 6, attack 20 ms, release 250 ms).
- Never duck a single word. Merge windows closer than 1 s.

## 5. Delivery loudness (on the final mix only)

1. Optional speech polish on the dialogue stem before the mix:
   `highpass=f=70,acompressor=threshold=-26dB:ratio=4:attack=12:release=150:knee=6`.
2. Mix, then two-pass `loudnorm` on the STEREO master: integrated -14 LUFS, true peak -1.5 dBTP, LRA 11. Pass 1 with
   `print_format=json`; pass 2 with the measured values and `linear=true`.
3. A mono voice copied to two channels measures about 3 LU louder than the same mono file. Always measure the file that is
   delivered, never a mono stem.
4. After the cut is approved, never reprocess the approved dialogue WAV again: later steps (graphics, music changes) mix
   against it as it is.

## 6. Check

- `python3 scripts/edge_qa.py render final.mp4 --cuts-file <plan> --out qc/edges_render`: joins inside sound and level jumps
  measured on the ENCODED file.
- Then `render-cut-verification` (strips, loudness, true peak, re-transcription of the export).
- If speech was re-transcribed for captions, drop the transcriber's known silence inventions before using it: "thank you",
  "thanks for watching", the Russian "to be continued" and a lone "you" in near-silence.

## Never

- Never say a word is complete because the script or the transcript says so; listen.
- Never fill gaps with digital silence under picture.
- Never loudness-normalise each clip separately and call that the mix.
- Never overwrite the plan, the takes or the approved WAV; moved edges go to a new file.
