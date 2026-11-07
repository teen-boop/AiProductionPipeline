# AI Production Pipeline
### by One Two Film

A set of **Claude Code skills** for making AI-generated films, from a script or
story idea to consistent, identity-locked storyboard frames and ready-to-paste
video prompts.

The skills are tool-agnostic. You can connect an image or video generator
through a **CLI**, an **API** or an **MCP connector**, or connect nothing and
generate by hand. In manual mode the pipeline still collects your references,
sorts them into folders and hands you every prompt with the exact references
to attach.

> No keys, accounts or personal data are included in this repository, and none are ever written by the skills. See [SECURITY.md](SECURITY.md).

---

## What it does

```
script / story idea
   │  script-extractor · visual-story-2-script
   ▼
generation backend?  ── generation-backend-setup ──►  CLI / API / MCP   (connected, tested)
   │                                              └─►  MANUAL MODE      (prompts + folders)
   ▼
references  ── reference-style-builder · character-identity-lock-setup · detail-reference-intake · organize_refs.py
   ▼
shot list   ── storyboard-narrative-breakdown · storyboard-shot-selection · continuity ledgers
   ▼
still frames ── period-fact-check · cinematic-prompt-writer · keyframe-chain-builder · storyboard-reference-assembly · manual-image-pack
   ▼
generate + QC ── generation-queue-runner · frame-qc-contact-sheet · generation-failure-fixes · identity-fix-pass
   ▼
placement   ── storyboard-insert-ops · animation-handoff-folder · animation-prompts-page
   ▼
video clips ── cinema-director-v3 · seedance-prompt-writer · seedance-edit-prompting (video-cut-timecodes · segment-reference-lock) · video-clip-continuity-chain
   ▼
storyboard + shot-list tracker
```

**Highlights**
- **Identity lock:** the same face at every age or stage of a character, from reference sheets.
- **Continuity ledgers:** camera, weather, props and wardrobe stay consistent from shot to shot.
- **Cinematic look:** a period-cinema prompt style (anamorphic, shallow depth of field, motivated light) that avoids the glossy "AI poster" look.
- **"Change to" chaining:** close-ups and next moments are re-framed from a master frame. Only frames made this way are used as first + last video pairs.
- **Manual generation pack** (`manual-image-pack`): one folder per frame with `PROMPT.txt`, the reference images already copied in and numbered, and an `INFO.txt`. When you drop `RESULT_1.png` into the folder, the skill checks it, crops thin black bars, files it into the project and updates the storyboard and the video prompts.
- **Keyframe chains:** micro-stories and time-of-day transitions as K1 → K2 → K3 stills, each generated from the previous one, so a video model can play them as first + last frame pairs. Physical realism and forward-moving time are checked.
- **Small, single-purpose QC skills:** contact-sheet QC with scripts, a catalogue of failure → fix lines, a head-only identity fix, and worker/rate-limit discipline. Each one does one job, so the pipeline stays stable.
- **Motion-graphics add-on:** Remotion code route plus video route, for charts and explainers.

---

## Install

You need [Claude Code](https://docs.claude.com/en/docs/claude-code/overview). The bundled helper scripts need Python 3 with Pillow (`pip install pillow`).

**macOS / Linux / Git Bash / WSL**
```bash
git clone https://github.com/teen-boop/AiProductionPipeline.git
cd AiProductionPipeline
./install.sh                     # global: ~/.claude/skills
./install.sh /path/to/project    # or only for one project
```

**Windows PowerShell**
```powershell
git clone https://github.com/teen-boop/AiProductionPipeline.git
cd AiProductionPipeline
.\install.ps1                              # global: %USERPROFILE%\.claude\skills
.\install.ps1 -Dest "C:\path\to\project"   # or only for one project
# if blocked: powershell -ExecutionPolicy Bypass -File .\install.ps1
```

The installer copies every folder in `skills/` and should report **66 skill(s) installed**. Restart Claude Code (or start a new session) afterwards.

To check that every skill is complete (front matter, referenced files, scripts compile): `python3 tools/validate_skills.py`.

---

## Quick start

In a new project folder, tell Claude Code what you want, for example:

> Start a new film project. Here is my script. Use the AI Production Pipeline.

The director skill (`ai-visual-production-director`) takes it from there:

1. **Backend.** `generation-backend-setup` asks whether you have a CLI, an API or a connector.
   - Connected: keys stay in environment variables, the connection is tested, and the choice is saved in `pipeline.config.json` (variable *names* only).
   - Nothing to connect: manual mode.
2. **References.** Drop your character, location and prop images into `references/_inbox`. Claude looks at each one, proposes a role, and sorts them into `references/<Category>/<name>/` with an `INDEX.md`.
3. **Shots and prompts.** The script becomes a shot list. Every shot gets a still prompt with its exact references, and every frame gets a video prompt with small, motivated camera moves and a colour lock.
4. **Manual mode.** You get a `MANUAL_GEN/` folder:
   1. open a frame folder;
   2. copy `PROMPT.txt`;
   3. attach `ref_1`, `ref_2`… in order;
   4. generate in your app;
   5. save `RESULT_1.png` back into the same folder.

   Then say *"collect the frames"*.

---

## Skills

**Start here**
- `ai-visual-production-director` — entry point. Works out which phase a request belongs to and runs the right skills in order.
- `generation-backend-setup` — connects a CLI, API or MCP backend safely, or switches to manual mode (reference sorting plus prompt list plus manual pack).

**Script and story**
- `script-extractor` — breaks a screenplay or prose into locations (day/night), characters, props, actions and wardrobe, each linked to its scene.
- `visual-story-1-setup` … `visual-story-8-storyboard` — an alternative fixed, linear 8-step pipeline: setup → script → cast & world → references → exposition → production → platform QC → storyboard.

**References and identity**
- `location-state-dials` — the same location in different states: dials (wear, wetness, light, tidiness, crowd, weather, time, damage, haze, season) with a "means here" sentence, named presets and a cost tag (prompt change vs new plate).
- `reference-style-builder` — learns the look from the project's reference library (style frames, saved prompts, approved frames), writes a measured style card (60/30/10 palette in hex, light, lens, grain, composition) and builds the reference set in order: style frame → character sheet → empty location plate → prop sheet → keyframes → change-to close-ups, each with its role line.
- `character-identity-lock-setup` — locks a character's face across every age or stage.
- `detail-reference-intake` — catalogues new detail screenshots into the reference index.
- `storyboard-reference-assembly` — resolves every noun in a shot to its locked reference asset.

**Shot list and continuity**
- `storyboard-narrative-breakdown` — turns "camera does X, then Y" prose into a numbered shot list.
- `storyboard-shot-selection` — justifies each shot size by the narrative job it does.
- `storyboard-camera-continuity-ledger`, `storyboard-continuity-tracker` — camera, cut and state continuity between shots.
- `animation-effects-catalog` — interactive shot-by-shot prompt builder (camera options → enhancements → assembled block, one shot per round) and a growing catalog of tricks that make AI video impressive, by hero type (tiny creatures, giants vs tiny humans, real animals, surreal anatomy, painted/puppet characters, levitation, falls, face recast) and by effect (camera, physics, performance, voice, light, workflow modes, negative blocks). Paste a strong prompt and say "learn from this" to grow it.
- `location-room-map` — turns one location photo into a full room: floor plan, all four walls (windows on at most two adjacent walls, at least one door, one of each object, same decor density as the source), each wall generated as its own reference so reverse shots show the right wall.
- `scene-continuity-lock` — per-scene state sheet (who sits where, prop states, light, camera axis, mirrored order on reverse shots); every storyboard panel and final-frame prompt is checked against the previous and next one, gets a CONTINUITY block, and is QC'd against the sheet.

**Still images**
- `cinematic-prompt-writer` — wide, medium and close-up prompts in one locked cinematic style.
- `manual-image-pack` — hand-generation packs and intake of the results.
- `loveart-video-animation`, `loveart-project-director` — the same phases written for the Lovart platform, if you use it.
- `period-fact-check` — checks the dates, liveries, construction stage and who was where against a source before prompting, and turns each fact into an ACCURACY line.
- `theme-research-module` — a swappable theme for a fixed series format (for example surreal home-video tapes): pins the era window, builds a reality bank (places, rituals, types, props), a twist bank (one impossible thing nobody reacts to), an annotated reference board with the camera of the era and a draft STYLE LOCK, runs an anachronism check and waits for approval before any download or story work.
- `keyframe-chain-builder` — K1 → K2 → K3 keyframe chains (micro-stories, reveals, sunset → night) for first + last frame video; enforces physical realism, forward-moving time and the full style on every keyframe.

**Generation, QC and placement (one job each)**
- `independent-frame-critic` — fresh-eyes review of a batch: a reviewer who never saw the prompts scores 8 film categories, names up to 5 ranked fixes and gives each frame keep / fix / reject; pass rule, logged and capped rounds. `scripts/critic_log.py`.
- `media-path-verify` — before any export or hand-off: every referenced file really exists, catches drives that remounted under a new name and phantom /Volumes folders; suggests relinks, applies none without a yes. `scripts/verify_media.py`.
- `frame-crop-guard` — checks every crop before a render: real boxes from headless Chrome (vertical layouts included), faces and people in each source with Apple Vision, flags lost or cut faces and bodies, suggests the object-position or a better box, and draws a sheet of every crop window. `scripts/crop_boxes.mjs`, `crop_check.py`, `subjects.swift`.
- `render-cut-verification` — the last gate on the ENCODED file: strips across every cut, black/flash frames, opening seconds, audio/video lengths, loudness and true peak, optional re-transcription. `scripts/cut_strips.py`.
- `style-lock-guard` — always-on look guard: locks the look to the director's own reference frames (and the source prompt embedded in their PNG metadata), lints every prompt before it is sent (required style phrases, no contradicting grade phrases, style frames attached last — wired into the runner as a gate), and measures every result against the references to catch the flat/grey "mediocre" look.
- `generation-queue-runner` — worker pool rules: limits, claim files, hard back-off on rate limits, no auto-confirmed costs, waves for chained frames.
- `frame-qc-contact-sheet` — batch QC on labelled contact sheets, start|end pair sheets and face crops, plus a letterbox-bar trimmer (`scripts/`).
- `reference-roles-leak-check`: one job per reference image (who, where, pose, style, light, palette...), a "do not take" line for each, the most-ignored job first, and a leak check before a frame is kept (no stranger's face, props or colors from the wrong card).
- `video-color-grade`: deterministic grading in local code (ffmpeg + numpy): cinematic looks baked to .cube LUTs, match to the approved key frame, day-for-night, B&W with one kept color, log to Rec.709, look grids and a grading showreel. `scripts/render_looks.py`, `match.py`, `showreel.py`.
- `seamless-motion-loops`: brand-color motion backgrounds as code, rendered to MP4 with a verified seam (frame at LOOP equals frame 0), optional character still on top, plus the same loop as a HyperFrames composition. `scripts/render-loop.mjs`, `loop-template.html`.
- `generation-failure-fixes` — catalogue of recurring model failures (second subject from a reference, leaked names, bars, orbs, wrong city, anachronisms, frozen poses, unsafe physics) with the exact fix line.
- `identity-fix-pass` — fixes a wrong face without re-shooting the frame, verifies it against the identity bust and keeps the storyboard slot.
- `storyboard-insert-ops` — declarative placement ops (replace, after/before, *_late after a beat rebuild, fixes of fixes last) and post-build checks.
- `animation-handoff-folder` — one flat folder of final frames in story order plus one prompt list with first/last-frame pairing, synced after every delivery.
- `animation-prompts-page` — the hand-off folder as one browsable page: picture + prompt + copy button, Kling end frame, filters, search, "done" ticks; rebuilt on every sync and always opened for the user.

**Video**
- `nle-timeline-assembly` — one validated cut plan (in/out, tracks, transitions, markers, music ducking) built in DaVinci Resolve (MCP), Premiere Pro (MCP) or exported as CMX3600 EDL + CSVs; read back after every change. `scripts/cutplan_to_edl.py`.
- `dialogue-cut` — voice-over and dialogue from several takes: DaVinci Resolve's own transcript (subtitles from audio) or any word timings, matched to every script line (any language), each reading scored (completeness, extra words, fillers, redo cues, confidence), the best one frame-snapped into a CANDIDATE cut with runner-ups, flags for loose or missing lines, and subtitles on the record timeline; a person listens before it is approved. Also finds where an ordered line sits inside a generated clip with speech. `scripts/take_select.py`.
- `dialogue-audio-finish` — measures every speech edge at 1 ms (clipped onsets, cut-off words, s/sh/t tails, dead air, cuts inside continuous speech, level jumps between takes) and suggests exact edges; sample-exact audio inside frame-snapped picture with room tone, 12 ms fades, level match, music ducking, and the delivery loudness pass on the final stereo file. `scripts/edge_qa.py`.
- `music-beat-grid` — optional, asks first: measured beat grid (kick-band phase, energy per bar), splices to length on beats, frame-exact cut sheet, checks cuts against the grid. `scripts/beat_grid.py`.
- `retention-packaging-plan` — asks the video type first; for social / creator / explainer cuts: hook, visual events, punch-ins, captions and cards as a cue sheet anchored to words.
- `text-behind-subject` — optional accent: title or number placed between background and subject (matting routes, composite, QC) for covers, title cards and hooks.
- `cinema-director-v3` — Seedance 2.0/2.5 and Higgsfield prompts on a locked 16-slot structure: optics, physics, acting, audio, lipsync.
- `seedance-prompt-writer` — Seedance-format prompts that follow a project's own mandatory rules.
- `seedance-edit-prompting` — Seedance 2.5 Edit / Higgsfield video-to-video: recast characters, wardrobe or backgrounds in existing footage while keeping motion, cuts and timing (asset mapping, identity link, shot order, no effects in recast), persona look and change-request read-back rules, a measured light match between characters and location plates, plus numeric motion-match verification with ffmpeg.
- `video-cut-timecodes` — splits a source video into one timecode block per cut, frame-accurate: hard cuts plus soft cuts (lone score peaks), black frames by luma, duration from the video stream, beat sheets for long takes, and a continuity check. When a block is wrong you choose: re-detect automatically or type the cuts manually (seconds or SS.FF).
- `segment-reference-lock` — assigns references to every block (automatically from the frames, or manually) and writes a LOOK LOCK into every block from the reference descriptions or the base details, plus the block's exact-motion and voice lines (original voice by default; new words only from the user).
- `video-clip-continuity-chain` — clips played back to back stay consistent.
- `seedance-shotlist-tracker` — an interactive production checklist for a batch of clips.

**Presentations**
- `otf-presentations` — OTF Presentations: cinematic announcement / explainer / teaser videos (HyperFrames). Reads the context from the chat and the project's references first (embedded source prompts, style lock, best frames ranked by the look, videos, docs), picks fonts that really render the language (glyph-tested) and an animation vocabulary matched to the look, then plans, composes, checks frame by frame and renders. `scripts/otf_context.py`. Its editing rhythm comes from a measured study of 24 premium short videos (`references/EDIT_PATTERNS.md`: accelerate-and-release, overexposure flash, dip-to-black breath, endings).
- `cinematic-poster-designer` — unusual cinematic film posters: one visual metaphor from a device catalogue (object replaces the head, silhouette window, shard reveal, lone figure in fog, single colour field…), learned only from the poster references the user marks as liked (`LIKED.md`); key art is generated without text and the title, tagline and credits are set in code (`scripts/compose_poster.py`), 2:3 plus 4:5 and 9:16.

- `davinci-series-assembly` — puts a series of finished clips (presentation parts, block reels) on a new DaVinci Resolve timeline in order via the Resolve MCP: validates fps/size, imports into a dated folder, creates a versioned timeline, adds a marker per part, verifies no gaps/overlaps, never deletes anything. `scripts/series_manifest.py` (+ ffmpeg preview master).

**Motion graphics (a parallel track)**
- `motion-graphics-director`, `motion-style-core`, `motion-design-references`, `motion-remotion-build`, `motion-video-route`.

---

## Repository layout

```
skills/          one folder per skill (SKILL.md + references/ scripts/ assets/)
docs/            pipeline overview and the prompt style template
examples/        example jobs and sections files for manual-image-pack
tools/           check_clean.sh — scans the repo for keys, personal paths and non-English text
                 validate_skills.py — checks every skill (front matter, referenced files, scripts compile)
install.sh       installer for macOS / Linux / Git Bash / WSL
install.ps1      installer for Windows PowerShell
```

## Contributing

Pull requests are welcome. Before you commit, run `tools/check_clean.sh` and `python3 tools/validate_skills.py`. Both must report no findings. Never commit keys, tokens, account IDs, personal names, e-mail addresses or absolute paths from your machine.

## License

MIT — see [LICENSE](LICENSE).

The take scoring, edge measurements and board mechanics in `dialogue-cut`, `dialogue-audio-finish` and `motion-graphics-director/references/BOARD-RECIPES.md` were studied in [YouTube-AI-Video-Editing-System](https://github.com/sirioberati/YouTube-AI-Video-Editing-System) by Sirio Berati (MIT) and rewritten for this pipeline.
