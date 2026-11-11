---
name: theme-research-module
description: Swappable THEME module for a montage-format series (e.g. a fixed format such as "an ordinary moment with one twist", cut to the beat). Researches a new theme/era before any story or image work - theme brief, reality bank (places, rituals, types, props), twist bank, annotated reference board (real archive photos + camera-of-the-era look + film stills + wardrobe/props + local surreal tradition), anachronism check - and gates on user approval. Use whenever the user picks a new theme/era/world for an existing series format, says "new theme", "research the theme", "collect references for <era>" for a themed series, or when the theme changes mid-series.
---

# Theme Research Module

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

A series has a fixed FORMAT (camera rule, story rule, edit rule) and a swappable THEME. This skill builds one theme module so the rest of the pipeline (story -> style lock -> refs -> clips -> beat edit) can run unchanged.

## Output: one folder per theme
```
<project>/themes/<theme-slug>/
  THEME_BRIEF.md       era window, world, camera-of-the-era, red lines, user picks
  REALITY_BANK.md      places / rituals / types / props (what is ORDINARY)
  TWIST_BANK.md        one impossible thing per anchor, nobody reacts
  REFERENCE_BOARD.md   annotated refs + draft STYLE LOCK (English)
  FACT_CHECK.md        anachronism pass
  refs/{camera,places,rituals,types,props,wardrobe,surreal}/
```
Chat with the user in their language; prompt text and STYLE LOCK stay in English.

## Steps
0. **Brief.** Pin the era window FIRST (e.g. "Port A 1955-65" vs "Port A 1985-95" are different worlds and different cameras). Ask the user to choose; never mix eras inside one clip.
1. **Reality bank.** Four lists: places, rituals, types (people), props. Offer candidates, user ticks. These are the "ordinary" half of every story.
2. **Twist bank.** For each anchor write 1-2 impossible things. Rules: exactly ONE impossible element; everyone in frame ignores it; prefer reassigning a period object (object gets a new role) or a scale/gravity break; keep sensitive groups (veterans, victims, real people) respectful; no real criminals' names or faces.
3. **Reference hunt** (parallel subagents is fine; candidates only, no downloads yet):
   - real documentary photos of the era per place/ritual/type (photo archives, Wikimedia Commons, editorial photo essays);
   - CAMERA OF THE ERA: the consumer device people actually filmed with (8mm film, VHS-C, Hi8, early digicam, phone), its date stamp font/position, artifacts;
   - film/TV stills for wardrobe, light, locations;
   - wardrobe and props photos;
   - the local surreal tradition (artists, films) to set the tone of the twist.
   Each candidate: id, URL actually seen (never invented), source, year, 2-4 named color blocks, light, subject placement/scale, pose/gaze, texture, "what we take", period confidence.
4. **Board.** Merge candidates into REFERENCE_BOARD.md, best 2-4 per item, plus a draft STYLE LOCK block derived from the camera refs.
5. **Fact check.** Run `period-fact-check` over reality bank + twist bank + board (flag props/cars/clothes outside the era window).
6. **Gate.** Show the board; the user picks. Ask permission before downloading chosen images (filename, source, size) into refs/. Only after approval: story step and `reference-style-builder` / `style-lock-guard`.

## Next in the chain
story-trainer / visual-story-2-script (stories from ticked twists) -> reference-style-builder + style-lock-guard -> character-identity-lock-setup (if recurring people/brand) -> seedance-prompt-writer / cinema-director-v3 (one-take clips) -> music-beat-grid -> nle-timeline-assembly -> video-color-grade. Test batch before full production; stop after reference images and wait for approval before any video.
