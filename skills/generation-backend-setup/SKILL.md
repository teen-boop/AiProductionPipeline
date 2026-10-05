---
name: generation-backend-setup
description: >-
  First step before any image or video generation in a film project. Asks the
  user which generation backend they can connect — a command-line tool (CLI),
  an HTTP API, an MCP connector already available in Claude, or nothing — and
  connects it safely: keys stay in environment variables or the OS keychain and
  are never written to project files, printed or committed. It tests the
  connection with the smallest possible call, sets the parallel-job limit, and
  records the choice (names of env vars only, never values) in
  pipeline.config.json. If nothing can be connected, it switches to MANUAL MODE
  and still runs the pipeline: asks for references, sorts them into a clean
  folder structure, and hands over a prompt list plus a ready-to-use manual pack
  (one folder per frame with prompt + references). Use at the start of a
  project, when generation fails because no backend is configured, when the user
  asks how to connect a tool or API, or when the user says they have no API and
  will generate by hand.
user-invocable: true
---

# Generation Backend Setup

The pipeline works with **any** backend, or with none. This skill decides which,
connects it safely, and makes sure the rest of the pipeline knows the answer.

## Step 1 — Ask (one short question, never assume)

Ask the user, in their language:

> How will we generate images and video for this project?
> 1. **CLI** — a command-line tool installed on this computer (a vendor's agent CLI, ComfyUI CLI, etc.)
> 2. **API** — an HTTP API with a key (image/video model providers)
> 3. **Connector** — a generation tool already connected to Claude (MCP)
> 4. **None / by hand** — I will paste prompts into a web app myself

Also ask:
- **cost:** free, subscription or paid credits;
- **parallel jobs:** how many may run at once;
- **video:** whether video goes through the same backend or is always pasted by hand.

If MCP tools for image or video generation are already visible in this session, mention them as option 3.

## Step 2a — CLI / API / Connector

1. **Credentials — non-negotiable rules:**
   - Keys live ONLY in environment variables (e.g. set in the user's shell profile) or the OS keychain. The user sets them themselves; Claude never asks them to paste a key into the chat.
   - Never write a key into any project file, config, prompt pack, log, commit or chat message. Never `echo` / `print` / `cat` a key. Pass keys to tools through the environment only.
   - If a key appears in output by accident, stop, tell the user to rotate it, and do not repeat it.
   - Add the backend's local state files (if any) to the project's `.gitignore`.
2. **Find the entry point:**
   - for a CLI: its path and `--help`;
   - for an API: the base URL and the model or endpoint names the user wants;
   - for a connector: the tool names.
   Read the docs from the vendor's official source if needed.
3. **Test with the smallest possible call.** Use a status, model list or account check. If only a real generation will prove the connection, ask first and say what it costs.
4. **Know the failure modes before going live:**
   - concurrency limit;
   - rate limit;
   - typical latency;
   - whether tasks can be cancelled;
   - whether results must be downloaded by a thread or job id.
   Plan to:
   - retry rate limits with a wait, never a tight loop;
   - never re-submit a job whose remote task is still running — poll it and adopt its result;
   - never exceed the user's parallel limit.
5. **Record the setup** in `<project>/pipeline.config.json` (template: `assets/pipeline.config.example.json`):
   - backend type, name, command or endpoint, model preferences;
   - the **names** of the env vars it needs;
   - `max_parallel`, `cost`.
   Never write values into it.

## Step 2b — Manual mode (nothing to connect)

Manual mode is a full route, not a dead end:

1. **Ask for references.** Characters (several angles or ages if the character ages), locations, props and vehicles, style or mood frames, and any images to recreate. The user can drop them into one inbox folder (e.g. `<project>/references/_inbox`).
2. **Look at every image** (open each one), then propose a role for each:
   - category: Characters / Locations / Props / Style / Recreate;
   - the name of the person, place or thing;
   - a short label (e.g. `age_39_bust`).
   The user confirms or corrects. Never guess silently who the main character is.
3. **Sort them** with `scripts/organize_refs.py`:
   ```bash
   python3 scripts/organize_refs.py --scan  --src <project>/references/_inbox
   python3 scripts/organize_refs.py --src <project>/references/_inbox --dest <project>/references --map mapping.json
   ```
   This copies (or `--move`s) the files into `references/<Category>/<name>/NN_<label>.<ext>` and writes `references/INDEX.md` + `references/index.json`. Every later prompt points at these paths.
4. **Give the prompt list.** For every shot of the scene or storyboard, write:
   - the prompt — follow the prompt blocks of `manual-image-pack` / `cinematic-prompt-writer`: REFERENCES → SCENE → CHARACTER LOCK → domain locks → LOOK + OPTICS → FORMAT;
   - the exact references to attach, in order, as paths from `references/INDEX.md`.

   Deliver it as `PROMPTS.md`, and, unless the user only wants the list, as a manual pack via `manual-image-pack` (one folder per frame with PROMPT.txt and the reference images already copied in). Video prompts are given as copy-paste text in the same way.
5. Write `pipeline.config.json` with `"type": "manual"`, so later steps do not try to call a backend.

## Step 3 — Hand off

Tell the user in two or three lines:
- what is connected, or that manual mode is on;
- where the config and references are;
- what comes next.

Then return to `ai-visual-production-director` (or `visual-story-pipeline`) for the next phase. Re-run this skill whenever the user gets a new tool or key, or a backend stops working. Generation can switch between backend and manual at any time; the manual pack and intake keep the project consistent either way.
