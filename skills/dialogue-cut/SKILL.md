---
name: dialogue-cut
description: >-
  Builds a dialogue or voice-over cut from several takes against the script. Each take is transcribed by DaVinci Resolve
  (subtitles from audio, phrase cues), and every script line is matched to every reading of it (normalised text, any language). Each reading
  gets a score for completeness, extra words, fillers, a following redo cue ("scratch that", "take two", or the Russian equivalents) and word
  confidence. The best one is picked, frame-snapped and written as a CANDIDATE cut (dialogue_cut.candidate.json)
  with runner-ups and flags (LOOSE, MISSING, FILLERS), plus subtitles on the record timeline. A human listens and
  approves before it becomes dialogue_cut.json. Use when the user records a voice-over or narration in several
  takes, says "pick the best takes", "cut the VO to the script", "remove the flubs", "assemble the narration", or
  when generated clips with speech (Seedance, Kling, Veo) must be trimmed so that no word is cut. Hands the edges
  to dialogue-audio-finish.
user-invocable: true
---

# Dialogue Cut

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

The script is the spine; the takes are material. This skill finds every attempt at every line, scores them and proposes one
reading per line. It never decides alone: the output is a candidate that a person listens to. Edges come from word timings,
which speech recognition gets right only to about 50 to 100 ms, so `dialogue-audio-finish` measures and moves every edge
before anyone calls the cut finished.

Method adapted from the Eyeline editing system (MIT, see the repository README); rewritten for this pipeline, any language,
standard library only, using DaVinci Resolve's own transcription instead of a separate speech model.

## 1. Inputs (read only)

- The approved script as plain text, one spoken line per line, `## Title` for chapters. For generated clips: the dialogue lines
  of the shot list, in order.
- The takes: WAV or video files. Never edit or overwrite them; every cut points back to them with source times.
- The transcript per take, from **DaVinci Resolve** (default; no extra install, works for English and Russian):
  1. In a dedicated project (or a dated folder of the current one), put each take on its own new timeline. Never use the
     user's cut.
  2. Create subtitles from the audio. With the Resolve MCP this is `timeline_ai create_subtitles` (`background: true`, then
     poll `resolve_control job_status`). By hand: Timeline > Create Subtitles from Audio.
  3. Read the cues back. With the MCP, `timeline get_transcript` (`with_timecodes: true`) saved as `<take>.cues.json`. By
     hand, export the subtitle track as `<take>.srt`.
  4. Note the timeline start (usually `01:00:00:00`) and pass it as the offset (`take01.srt:/abs/take01.wav@01:00:00:00`).

  Resolve gives phrase cues, not words. The selector spreads each cue over its words, which is enough to find the right
  reading, but every edge then MUST be measured by `edge_qa.py`.

  Two more Resolve tools help:
  - `timeline propose_cuts` (dry run): fillers, long pauses and repeated lines straight from the subtitle track. A good
    second opinion.
  - `media_pool_item transcribe_audio` / `get_transcription`: clip-level text only, without times. Fine for checking what a
    clip says, useless for edges.
- Optional, when word-level times exist from another transcriber: word JSON (`{word, start, end, probability}`, Whisper
  format accepted). Settings that matter there:
  - `temperature 0`;
  - no conditioning on previous text;
  - a filler-heavy initial prompt, so "um" and "uh" stay visible.
- Ask once, only if missing: frame rate of the timeline (default 24), and whether subtitles are needed.

## 2. Pick the readings

```
python3 scripts/take_select.py --script script.txt \
  --takes take01.srt:/abs/take01.wav@01:00:00:00 take02.cues.json:/abs/take02.wav@01:00:00:00 \
  --out edit/dialogue --fps 24 --srt
```

What it does:
- **Normalises script and words the same way:** case, the Russian yo letter folded to ye, curly quotes, hyphens, punctuation, common English contractions
  and number words. Fillers (en and ru) are kept aside, not matched.
- **Finds every attempt** of a line inside every take (a take often holds three tries of the same sentence). It aligns with a
  sequence matcher from each place where one of the line's first three words occurs.
- **Scores each reading:**
  `100*recall - 2.5*extra words - 2*fillers + 4*mean word confidence`, minus 35 when a redo cue follows within 3 s, plus 2
  for the last attempt of the line in that take.
- **Names:** transcribers spell invented names as common words (in a test, Resolve heard "Riz! Riz!" as "rice Rice"). Pass `--alias rice=riz` per name before trusting a MISSING flag.
- **Chooses:** the best reading with recall at least 0.6. Otherwise the best with at least 0.3, flagged `LOOSE`. Otherwise
  `MISSING`: ask for a pickup. Never paper over a missing line with a partial one.
- **Snaps to the frame grid:** in is floored and out is ceiled, so a clip never shortens its own words. Edges are padded
  (80 ms before, 120 ms after) as a candidate only.

Outputs, never overwriting the approved plan:
- `dialogue_cut.candidate.json`: clips in record order with `source`, `in`, `out`, `record_in`, `words`, score, flags and up
  to three alternatives.
- `dialogue_cut.candidate.md`: the review table.
- `subtitles.candidate.srt`: at most 84 characters per cue in two balanced lines of about 42, at most 6 s, a new cue after any
  gap over 0.7 s, a 0.3 s tail that never runs into the next cue.

## 3. Edges and levels

Run `dialogue-audio-finish` step 1 (`edge_qa.py plan ... --apply`) on the candidate. It flags clipped onsets, cut-off words
and sibilant tails, dead air, cuts inside continuous speech, and level jumps between takes. It writes moved edges to a new
file. Read every flag.

## 4. Review (a person listens; required)

Show the user the table and the flagged edges, then say how to listen: play the candidate export, not the clips one by one.
The rules of the review:
- Read the script next to a transcript of the **exported audio**. A clip label or the candidate's own words list is not
  evidence of what is heard.
- Listen to the first and last sound of every changed clip, in context. A short silence before a final t, k, p or d is
  normal; a fixed extra pad on every clip can instead double a word from the next phrase.
- Compare neighbouring clips from the same take: a contiguous interval needs no split; an overlapping one repeats a syllable.
- A linking word ("and", "so", or the same in the take's language) between two lines of the same take belongs to the first line when the gap is under
  2 s and the link is at most four words.
- Speech recognition spells a mispronounced word correctly. Text matching cannot hear a flub; only listening can.
- Any change goes into a new candidate. When the user approves, copy the candidate to `dialogue_cut.json` and keep the
  previous approved file in `edit/dialogue/history/dialogue_cut.<YYYYMMDD-HHMMSS>.json`. Write through a temp file plus
  rename, never in place.

## 5. Hand over

- To `nle-timeline-assembly`: each clip becomes an audio event (`file` = source, `src_in`/`src_out` = the approved edges).
  When picture and sound edges differ, the picture is frame-snapped and the audio keeps its exact edges (see
  dialogue-audio-finish).
- To `retention-packaging-plan` and captions: the word timings of the **final export**, re-transcribed, never the script.
- To `render-cut-verification`: `dialogue_cut.json` is accepted as the cut list (clip durations accumulate to record times).

## Generated clips with speech (Seedance, Kling, Veo)

The same tools apply when the "takes" are generated clips:
- Transcribe each clip.
- Put the shot's dialogue line in the script.
- Let the selector find where the line sits inside the clip. Then trim there instead of trimming by eye. A trim on a round
  number (11.6 s) often lands 50 to 100 ms into a word.
- The generated clip may say a different line than ordered (models invent dialogue). A `LOOSE` or `MISSING` flag is the first
  sign of that. Regenerate or rewrite the line; do not cut around it.

## Never

- Never overwrite a take, the approved `dialogue_cut.json` or a previous candidate.
- Never mark a cut approved, clean or perfect without a listening pass by the user.
- Never fill a missing line from a partial reading without saying so.
- Never use the script text as the subtitle or caption source for the final video; transcribe the export.
