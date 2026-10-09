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
references  ── character-identity-lock-setup · detail-reference-intake · organize_refs.py
   ▼
shot list   ── storyboard-narrative-breakdown · storyboard-shot-selection · continuity ledgers
   ▼
still frames ── cinematic-prompt-writer · storyboard-reference-assembly · manual-image-pack
   ▼
video clips ── cinema-director-v3 · seedance-prompt-writer · video-clip-continuity-chain
   ▼
storyboard + shot-list tracker
```

**Highlights**
- **Identity lock:** the same face at every age or stage of a character, from reference sheets.
- **Continuity ledgers:** camera, weather, props and wardrobe stay consistent from shot to shot.
- **Cinematic look:** a period-cinema prompt style (anamorphic, shallow depth of field, motivated light) that avoids the glossy "AI poster" look.
- **"Change to" chaining:** close-ups and next moments are re-framed from a master frame. Only frames made this way are used as first + last video pairs.
- **Manual generation pack** (`manual-image-pack`): one folder per frame with `PROMPT.txt`, the reference images already copied in and numbered, and an `INFO.txt`. When you drop `RESULT_1.png` into the folder, the skill checks it, crops thin black bars, files it into the project and updates the storyboard and the video prompts.
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

The installer copies every folder in `skills/` and should report **34 skill(s) installed**. Restart Claude Code (or start a new session) afterwards.

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
- `character-identity-lock-setup` — locks a character's face across every age or stage.
- `detail-reference-intake` — catalogues new detail screenshots into the reference index.
- `storyboard-reference-assembly` — resolves every noun in a shot to its locked reference asset.

**Shot list and continuity**
- `storyboard-narrative-breakdown` — turns "camera does X, then Y" prose into a numbered shot list.
- `storyboard-shot-selection` — justifies each shot size by the narrative job it does.
- `storyboard-camera-continuity-ledger`, `storyboard-continuity-tracker` — camera, cut and state continuity between shots.
- `animation-effects-catalog` — growing catalog of tricks that make AI video impressive, by hero type (tiny creatures, giants vs tiny humans, real animals, surreal anatomy, painted/puppet characters, levitation, falls, face recast) and by effect (camera, physics, performance, voice, light, workflow modes, negative blocks). Paste a strong prompt and say "learn from this" to grow it.
- `location-room-map` — turns one location photo into a full room: floor plan, all four walls (windows on at most two adjacent walls, at least one door, one of each object, same decor density as the source), each wall generated as its own reference so reverse shots show the right wall.
- `scene-continuity-lock` — per-scene state sheet (who sits where, prop states, light, camera axis, mirrored order on reverse shots); every storyboard panel and final-frame prompt is checked against the previous and next one, gets a CONTINUITY block, and is QC'd against the sheet.

**Still images**
- `cinematic-prompt-writer` — wide, medium and close-up prompts in one locked cinematic style.
- `manual-image-pack` — hand-generation packs and intake of the results.
- `loveart-video-animation`, `loveart-project-director` — the same phases written for the Lovart platform, if you use it.

**Video**
- `cinema-director-v3` — Seedance 2.0/2.5 and Higgsfield prompts on a locked 16-slot structure: optics, physics, acting, audio, lipsync.
- `seedance-prompt-writer` — Seedance-format prompts that follow a project's own mandatory rules.
- `video-clip-continuity-chain` — clips played back to back stay consistent.
- `seedance-shotlist-tracker` — an interactive production checklist for a batch of clips.

**Motion graphics (a parallel track)**
- `motion-graphics-director`, `motion-style-core`, `motion-design-references`, `motion-remotion-build`, `motion-video-route`.

---

## Repository layout

```
skills/          one folder per skill (SKILL.md + references/ scripts/ assets/)
docs/            pipeline overview and the prompt style template
examples/        example jobs and sections files for manual-image-pack
tools/           check_clean.sh — scans the repo for keys, personal paths and non-English text
install.sh       installer for macOS / Linux / Git Bash / WSL
install.ps1      installer for Windows PowerShell
```

## Contributing

Pull requests are welcome. Before you commit, run `tools/check_clean.sh`. It must report no findings. Never commit keys, tokens, account IDs, personal names, e-mail addresses or absolute paths from your machine.

## License

MIT — see [LICENSE](LICENSE).
