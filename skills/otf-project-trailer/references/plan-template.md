# TRAILER_PLAN.md template

One page. It is the contract the user approves before anything renders. Paths are relative to the project folder.

```markdown
# Trailer plan: <project title>  (<run id>)

## Brief (from the chat, in the user's words)
- Subject: <film / episode N / series / the pipeline>
- Logline: "<as given>"  (or: assumed, from <doc>)
- Purpose and audience: <...>
- Release line: <date / platform / "coming soon">
- Languages: <en, ru, ...>   Formats: <16:9 master; 9:16; 1:1>   Frame rate: 24
- Must-show: <...>
- Banned: <rejected looks, faces, imagery, words>
- Assumptions: <anything inferred>

## Structure and tone
- Structure: <full 30 s / teaser 15 s / mood / documentary / series / making-of>, because <one line>
- Tone: <preset> + "<freeform direction>"
- The one promise: <the question or feeling the trailer sells>

## Look
- Style lock: STYLE_LOCK.json (required phrases, forbidden phrases), palette <hex x5>
- Grade: <look name / match frame>, LUT <file>
- Grain / halation: <none, clips carry it / plate at 0.06 + halation 0.1>
- Fonts: display <family>, accent <family> (glyph-tested for <languages>)

## Music
- Track: <file>, source and license in audio/MUSIC_SOURCE.txt
- Measured: <BPM measured>, phase <s>, drop at <s>, break at <s>
- Beat lock: accents only (open, turn, break, peak cluster, title) / none

## Beats
| # | Beat | In | Out | Shots | Text on screen | Transition out | Music |
|---|---|---|---|---|---|---|---|
| 1 | Cold open | 0.00 | 2.50 | S01 | none | cut | hit on downbeat 1 |
| ... |

## Shot list (the pick)
| Shot | Beat | Source (relative) | src in-out | Kind | Scale | Face | Motion added | Rank |
|---|---|---|---|---|---|---|---|---|
| S01 | 1 | clips/approved/shot_detail_v2.mp4 | 0.42-2.92 | clip | detail | no | none | 3 |
| ... |

## Gaps -> generation requests
- GR-01 <beat, why>  (see GENERATION_REQUESTS.md)  status: waiting / approved / delivered

## Text per language
| Card | en | ru |
|---|---|---|
| Intertitle 1 | ... | ... |
| Title | ... | ... |
| Release | ... | ... |

## Approvals
- Pick approved: <date, changes>
- Plan approved: <date, changes>
```

## edit/cuts.json

The machine-readable cut list, written from the shot list once the plan is approved. Times on the record side are snapped
to the 24 fps grid. `frame_check_sheet.py` and `render-cut-verification` (`--cuts-file`) both read it, and it converts
directly into the `cutplan.json` of `nle-timeline-assembly`.

```json
{"fps": 24, "length": 30.0, "format": "16:9",
 "shots": [
  {"id": "S01", "beat": "cold open", "src": "clips/approved/shot_detail_v2.mp4",
   "src_in": 0.417, "record_in": 0.0, "record_out": 2.5, "transition_after": "cut"},
  {"id": "S02", "beat": "world", "src": "frames/approved/place_wide.png",
   "src_in": 0.0, "record_in": 2.5, "record_out": 4.25, "motion": {"type": "push_in", "from": 1.0, "to": 1.05},
   "transition_after": "flash"},
  {"id": "T1", "beat": "title card", "kind": "title", "record_in": 26.0, "record_out": 28.5},
  {"id": "E1", "beat": "release card", "kind": "release", "record_in": 28.5, "record_out": 30.0}
 ]}
```

Title, intertitle and release cards are entries in `shots` too (with `kind` and no `src`), so every join, including the
cut into the title, is checked.
