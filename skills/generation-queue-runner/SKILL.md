---
name: generation-queue-runner
description: >-
  Operating rules for running a batch of image generations through a connected backend (CLI/API/MCP) with a small pool of workers:
  concurrency limits, claim files, hard back-off on "rate limit" / "concurrent task limit", never re-submitting a running remote task,
  never auto-confirming a cost step, paid/fast mode only with explicit user approval and an automatic switch back, and sequential waves
  for chained frames. Use whenever you start, scale, pause or debug generation workers, or when generation stalls ("busy", rate limited,
  nothing arriving).
user-invocable: true
---

# Generation Queue Runner

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

## Workers

- One worker per process. Each worker claims a job by writing a claim file `.claim_<result>`, generates it, saves `RESULT_k.png` into the
  job folder and releases the claim.
- Start at the user's stated limit. If none is given, start with **2–3 workers**. Raise it only when the user allows it. Free tiers
  rate-limit fast.
- A job is skipped when any of these exist: `RESULT_k`, `.failed_RESULT_k`, `.cost_RESULT_k` (waiting for the user), or a
  `ref_*.txt` placeholder (its start frame is not delivered yet).

## When the backend says busy or rate-limited

- **Back off hard.** Wait 300 s after "Rate limit", 90 s after "concurrent task limit". Never retry every few seconds: N workers × 1
  request a minute keeps the limit triggered forever.
- If the limit stays for more than ~10 minutes, stop all workers, wait 10–15 minutes and probe once with a cheap status call. Restart
  with fewer workers.
- When you stop workers, remove their stale `.claim_*` files and `_tmp_*` folders. Otherwise those jobs are never picked up again.
- There is usually **no cancel API**. A request stuck in the remote queue blocks a slot until it finishes or the user cancels it in the
  web UI. Tell the user; do not keep submitting.

## Money

- **Never confirm a cost step yourself.** Write a `.cost_` marker and skip the job. The user decides.
- Use paid or fast mode only when the user explicitly asks ("use the paid mode", "use the fast mode today"). Pair it with a guard that switches
  back to the free mode when the queue empties or at midnight.

## Quote, then one, then the batch

Before any batch that costs money or a long queue:

1. Print ONE quote line and wait for the user's yes: `N items · S seconds of video (or N images) · ≈C credits · balance B`
   (read the balance from the backend; if it cannot be read, say "balance unknown").
2. Run the FIRST item alone. Show it, run frame QC on it, and continue only when it passes (or the user approves).
3. Then run the rest in rolling batches of about 10, so a bad prompt never burns the whole batch.

## Chained frames

- Frames generated *from* other frames (change-to, keyframe chains) run in **waves**:
  1. deliver and QC wave N;
  2. then pack wave N+1 from the delivered files.
- If a start frame is redone, mark the dependent job `.failed_` ("superseded") before a worker claims it. If it was already claimed,
  discard its result.
- After you edit a prompt, check whether a worker claimed that job *before* the edit (log timestamp). That result will follow the old
  prompt.

## Watching

- Use one monitor that reports every N finished frames plus every error, rate limit and "nothing left". Don't print every log line.
- A monitor expiring is not a failure. Check the log and re-arm it.

## Never

- Never re-submit a job whose remote task is still running. Poll it and adopt its late result.
- Never print or store API keys. Keep them in environment variables only.

## Stale-result traps (check your runner for both)

- **A failed run must never return an old image.** If the runner copies "the newest image in the job folder", a generation that
  produced nothing hands back the previous attempt and reports ok. Move earlier results aside (`_prev/`) before each run, and
  compare the new file's checksum with the rejected versions after the batch: identical bytes = the regeneration did not happen.
- **Cache uploaded references by content, not by path.** When a reference (product master, key frame) is regenerated under the
  same file name, a path-keyed upload cache keeps sending the OLD picture to the model. Key the cache on path + size + mtime
  (or a hash).
