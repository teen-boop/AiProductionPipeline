---
name: animation-prompts-page
description: >-
  Shows the animator's prompts as ONE browsable page instead of a wall of text: every frame of the animation hand-off folder in story
  order with its picture, duration and full prompt, a "copy prompt" button, the end frame of each first/last-frame (Kling) pair, block
  filters, search, "only pairs", and a per-frame "done" tick that is remembered in the browser. Rebuilt automatically whenever the
  hand-off folder is synced, and OPENED for the user every time they ask to see the prompts. Use when the user asks to "show the
  animation prompts", "all prompts", "what's left to animate", wants to work through the animation list, or right after the
  animation-handoff-folder sync.
user-invocable: true
---

# Animation Prompts Page

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

The user animates by hand: open a picture, copy its prompt, paste it into the video tool, and mark it done. One long text file makes
that slow; a page with the picture next to its prompt and a copy button is faster to work through, so it is the default view.

## Build

```
python3 scripts/prompts_page.py <hand-off folder> [--prompts <list>.txt] [--out <page>.html] [--title "<project> — animation prompts"] [--lang en|ru]
```

- **Input:** the flat hand-off folder from `animation-handoff-folder` and its single prompt list. Entries are separated by a line of
  `=` characters, with the header `<file>.png   (<duration>)` and then the prompt.
- **Output:** by default, `<folder>_PROMPTS.html` NEXT TO the folder, never inside it. The hand-off sync deletes every file in the folder
  it doesn't know.
- **Images:** linked relative to the page by their exact on-disk names. Nothing is copied or resized, and the full-resolution picture
  opens on click.
- **Pairs:** an entry whose prompt names `End frame = the picture <file>` (or a storyboard number) is shown as a pair, with THAT frame as
  its end frame. The legacy "the NEXT picture" wording falls back to the next frame, but it is unreliable; fix the list instead.
- **Done ticks:** stored in `localStorage` under a key made from the folder path. They survive rebuilds. They are per browser, which is
  enough for one animator.
- The script prints the frame count and how many pictures are missing. A missing picture means the folder and the list are out of sync,
  so fix the sync first.

## Keep it in sync

Call the page build at the end of the hand-off sync, right after the prompt list is written, so the page can never be older than the
folder. In a project that has a build script, make the page build the last step of that script.

## Always open it

Whenever the user asks to see or work through the animation prompts:
1. Rebuild the page.
2. Open it in their browser: `open "<page>.html"` on macOS.
3. Give the clickable link in the reply.

Do not paste the prompts into the chat. Do not tell the user to open the .txt file.

## Check before handing over

- Render it once (headless Chrome screenshot, or the built-in browser) and look at it:
  - pictures load;
  - Cyrillic names resolve;
  - the copy button and the done tick work.
- **Story order must equal name order.** Frame numbers with letter suffixes must sort the way the story runs. "0440aa" sorts between
  "0440a" and "0440b", not after "0440z". Extend a suffix run with `za, zb, …` (then `zza…`), never `aa`. If the user can't find frames,
  check this first.
