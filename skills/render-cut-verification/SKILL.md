---
name: render-cut-verification
description: >-
  Checks the ENCODED final video, not the project: a 10-frame strip across every cut (catches one-frame black flashes, ghost or
  stuck layers, a caption over the wrong shot, a duplicated frame), black/flash detection over the whole file, a frame-by-frame
  sheet of the opening seconds, stream checks (audio and video lengths match, last syllable present, frame rate and size as
  ordered), loudness and true peak measured on the delivered file, an optional fresh transcription compared word by word with the
  approved script, and a VERIFY.md that separates what was measured from what was looked at and listened to. Use before calling any
  edit, presentation, reel or assembled timeline export "done"; when the user says "check the render", "verify the export",
  "anything broken at the cuts?", "is it ready to post?". Includes scripts/cut_strips.py.
user-invocable: true
---

# Render Cut Verification

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

`frame-qc-contact-sheet` checks stills; `independent-frame-critic` judges quality with fresh eyes. Neither looks at the joins of
the final encoded file, which is where flashes, drift and clipped words appear. This skill is that mechanical last gate.

## 1. Collect

- The final render (the file that will be delivered, not a preview or the project).
- The cut list on the render's timeline, if there is one: a `dialogue_cut` EDL (`keep` ranges), a cut plan, or a list of times.
  Without one the script falls back to scene detection, which misses dissolves and cuts between similar dark shots: say so.
- The order: aspect ratio(s), frame rate, length, loudness target (YouTube/most platforms about -14 LUFS, true peak at or below
  -1 dBTP, unless `dialogue-audio-finish` set another).
- The approved script, if the video has speech.

## 2. Run

```
python3 scripts/cut_strips.py final.mp4 --out qc/final --cuts-file edit/raw.mistakes-edl.json --expect-duration 41.25
```

Outputs `strip_NN_<time>.jpg` per cut (the red bar marks the last frame before the cut), `opening.jpg` (first 2.5 s, every
second frame), `report.json` and `report.md` with stream lengths, black/flash frames and loudness.

## 3. Look (required, not optional)

Open every strip and the opening sheet. Per cut, check:
- no black, white or empty frame unless it is a designed flash;
- no frame of the previous shot after the cut, no frozen duplicate, no layer that stays after its shot ended;
- captions and graphics belong to the shot they sit on; nothing covers the mouth or the eyes;
- in a dissolve, no jump in the middle.
Opening: frame 0 is meaningful (no black lead-in, no unrelated bumper), the topic or tension is readable muted by about 3 s.

For several aspect ratios, run and look at each render separately. A 9:16 that passes says nothing about the 16:9.

## 4. Listen

Run `dialogue-audio-finish/scripts/edge_qa.py render <file> --cuts-file <plan> --out qc/edges_render` when the video has
speech: it measures joins that land inside sound and level jumps over 7 dB across cuts on the encoded file, and tells you
which joins to listen to first. Then listen to every join and the last word. Compare the end of the audio stream with the end of the video stream (the report flags
more than one frame of difference). If the video has speech, transcribe the FINAL file (DaVinci Resolve: import the render, Create Subtitles from Audio,
read the cues with the MCP `timeline get_transcript`) and
compare it word by word with the approved script around every cut: a transcript can guess a clipped word correctly while a
listener hears it broken, so a match is supporting evidence, not proof. Before comparing, drop the transcriber's silence inventions ("thank you",
"thanks for watching", the Russian "to be continued", a lone "you" in near-silence). Then look for a phrase of 2 to 8 words repeated
back to back: that is a doubled take at a join. For lip sync, compare a face frame on each side of a few
cuts with the same moment in the source.

## 5. Write VERIFY.md next to the render

```
# VERIFY <file name>  <sha256 first 12>  <date>
Measured: streams, durations, fps, size, black frames, loudness/true peak (numbers)
Looked at: N cut strips, opening sheet, every aspect ratio (list)
Listened: joins, last word, music vs voice (or "not available in this session")
Issues found -> fixed -> re-checked: ...
Open limits: ...
```

Say which checks could not be done. A waveform is not a listening pass; an empty issue list from the script is not a visual pass.

## 6. Fix loop

Fix in the project, re-render to a NEW file name, re-run this skill on the new file. Archive superseded renders; never keep two
files that could both be mistaken for the final.

## Never

- Never verify the project or a preview instead of the encoded delivery file.
- Never call a render clean from the script output alone; the strips must be looked at.
- Never measure loudness on a WAV stem and report it as the delivery loudness.
- Never claim a listening or watching pass that did not happen; write "not available".
- Never overwrite the render you are checking; fixes go to a new file.
