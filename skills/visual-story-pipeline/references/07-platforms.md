# Platform-specific operational notes

General principle before using any platform: some platforms/models expose true identity-lock via a
reference-image input (e.g. `image_urls`), others only expose a style-influence knob (e.g.
`style_images`) that does NOT preserve identity. Check which kind of input a model/platform offers
before relying on it for a specific real person's face. When multiple platforms are viable, run a
small side-by-side test using the same subjects on each before committing production to one.

## Lovart (via a CLI wrapping its Agent API)

**Setup**
- Two credentials required: `LOVART_ACCESS_KEY` and `LOVART_SECRET_KEY` (an `ak_...`/`sk_...` pair).
  Verify both are set and valid with a lightweight call (`upload` or `projects --json`) before
  committing to a full batch — an invalid/rotated key fails everything mid-batch, and it's cheaper
  to catch with one small call than after several submissions are already in flight.
- The `lovart-api` skill install via `npx skills add` may only copy documentation (README/SKILL.md),
  NOT the actual `scripts/agent_skill.py` the docs reference. Verify the script file actually exists
  before assuming the CLI is ready — if missing, clone `github.com/lovartai/lovart-skill` and copy
  `skills/lovart-skill/scripts/agent_skill.py` into the installed skill's `scripts/` folder.
- `set-mode --unlimited` switches the account to free/queued generation (no credit spend);
  `set-mode --fast` costs credits with no queue. Confirm which mode the user wants as part of
  platform setup, don't wait to be told reactively mid-batch.
- **The mode setting does not survive a credential change.** If `LOVART_ACCESS_KEY`/`SECRET_KEY` are
  rotated or replaced mid-project (e.g. after an auth failure), the account associated with the new
  keys resets to its own default mode — `set-mode --unlimited` called on the old credentials does
  NOT carry over. Re-run `query-mode` (and `set-mode --unlimited` again if needed) immediately after
  any credential change, before submitting more generations — otherwise a batch can silently run on
  paid credits when the user asked for free/unlimited mode.
- **Model + mode + cost — ask, don't assume, before the first generation.** Run `query-mode` and
  read its `unlimited_list` for the models actually available to this account before picking one.
  Then ask the user: which model (`--prefer-models`), free/unlimited or paid/fast, and — if the
  platform doesn't expose a clean per-generation credit cost through this CLI (it generally doesn't
  for standard image generation; the `pending_confirmation`/`estimated_cost` flow only fires for
  flagged high-cost operations like video) — say so plainly rather than inventing a number, and
  point to the platform's own dashboard/billing page for exact pricing.

**Submitting and polling**
- `upload --file <path>` returns a URL usable as an `--attachments` argument for `chat`.
- `chat --prompt "..." --project-id <id> --attachments <url1> <url2> --prefer-models
  '{"IMAGE":["generate_image_nano_banana_pro"]}' --json --download --output-dir <dir>` submits and
  (if it completes fast enough) downloads. Long generations routinely exceed the client-side timeout
  and return `"final_status":"timeout","status":"running"` — the job is still running server-side.
  Extract the `thread_id` and poll with `result --thread-id <id> --json --download --output-dir
  <dir>` until `"status":"done"`.
- **A returned client-side response (even "timeout") does not mean the server-side slot is free.**
  Only count a thread as finished, and its concurrency slot freed, once `result --thread-id` reports
  `"done"` — submitting new jobs based on the local CLI process having exited will hit the
  concurrency error below.
- **Run each submission as a properly backgrounded process** (the harness's own background-task
  mechanism, not shell `&`/`wait` inside one call with a hard timeout) — otherwise the outer timeout
  can kill the submission before the thread is even created, silently losing the job.

**Concurrency**
- The concurrency cap is NOT reliably 6–10 in practice — it can be as low as 2 simultaneous threads
  depending on account/plan state. Exceeding it returns `"Error: Concurrent task limit reached."`
  immediately, with no queue. Don't trust a documented/assumed cap: start conservative (assume 2),
  and only add more once you've confirmed a slot is truly free (per the point above) — just wait for
  a slot and resubmit the exact same request rather than guessing higher.
- Jobs can come back `"status":"abort"` with empty `items` and no error message, for no apparent
  content-related reason — this can be transient (a fresh resubmission of the identical request can
  succeed). If the identical request aborts twice in a row, stop retrying blindly and report it to
  the user instead of trying a third time.
- Congestion is real and can last 30–60+ minutes with zero status change across repeated polls — a
  known platform behavior, not a sign anything is broken. Poll at increasing intervals (5 → 10 → 15
  → 25 min) rather than tight-looping. Basic connectivity (listing projects/threads) can work fine
  even while actual generation is congested — check both separately when diagnosing "Lovart is down"
  vs. "the generation queue is backed up."

**Aspect ratio and resolution**
- Lovart has no dedicated aspect-ratio or resolution parameter (unlike Krea) — both must be stated
  explicitly in the prompt text itself (e.g. "4:3 aspect ratio, 2K resolution, ..."). Confirm this
  is actually being honored in the first test image; don't assume prompt text alone is reliably
  respected.

**Automation gotchas (when scripting a submit/poll loop)**
- On macOS's default bash (3.2), `declare -A` associative arrays with numeric-looking or zero-padded
  keys (e.g. `[08]=...`) can throw spurious "value too great for base" or "unbound variable" errors.
  Avoid the combined `declare -A NAME=( [key]=val ... )` initializer syntax for anything but the
  simplest literal keys; prefer a `case` statement mapping IDs to values instead — it's portable and
  doesn't hit this class of bug.
- If a driver script's job-tracking state lives in a directory, do NOT delete/clean up that state
  directory while the script might still be running (even in the background) — a still-running poll
  loop that finds its state gone can conclude nothing was ever submitted and silently restart the
  entire batch. Confirm the process has actually exited (e.g. `ps aux | grep <script>`) before
  cleaning up its state.

## Krea (via its public API / MCP)

- `get_upload_url` returns a presigned URL good for 3 hours and reusable for multiple files — POST
  each file to it with `curl -F "file=@path"`, response contains the asset URL to use as
  `image_urls`.
- `generate_image` with `model: "google/nano-banana-pro"` (or `nano-banana-2`) and
  `input.image_urls: [<uploaded-url>]` gives true identity-locked face-reference generation — a good
  option when another platform is congested.
- Respects an explicit `aspect_ratio` field (e.g. `"4:3"`) — set it precisely; don't rely on prompt
  text alone for aspect ratio on platforms that support a dedicated parameter.
- Jobs generally complete in under a minute — no persistent queueing problem observed.
- When downloading multiple completed jobs in one batch, map each output file strictly by `job_id` →
  its own returned URL — do not assume request order is preserved when scripting parallel downloads.
  A positional mismatch here silently saves the wrong image under the wrong shot's filename; always
  QC after a batch download, not just after generation.
