---
name: delivery-package
description: >-
  Builds a ready-to-send package for a client or a platform (client, youtube, youtube_shorts, tiktok, instagram_reels,
  instagram_feed, linkedin, x) from finished videos: checks every file against the target's rules (aspect, duration, size,
  codec, audio, pixel format, fps, resolution, optional loudness in LUFS), blocks anything that fails and any file that is an
  EXTERNAL or PERSONAL reference, names files by the target's rule (client: <Client>_<Title>_<aspect>_<LANG>_v01;
  platforms: <Title>_<platform>_<aspect>_<LANG>), adds matching .srt/.vtt captions and a thumbnail per video, writes
  DELIVERY_NOTE.md and CHECKSUMS.sha256, optionally a zip, into 06_DELIVERY/<YYYY-MM-DD>_<target>[_<client>]/. Never uploads,
  never overwrites an earlier delivery. Use when the user says "prepare the delivery", "package for the client", "export for
  Instagram / TikTok / YouTube", "send the finals", "zip it with checksums", or before any upload or post. Includes
  scripts/deliver.py.
user-invocable: true
---

# Delivery Package

The last step before anything leaves the project. Its job is to catch what goes wrong at the receiving end: wrong aspect
for the placement, too long, a ProRes master sent to a phone app, missing captions, a name nobody can sort, a reference
image that was never ours.

## Workflow

1. **Pick the source**: a title from the finals tree (`--from-final "Promos/03-Rise"`, optionally `--lang EN`), or explicit
   `--files`. Finals come from `final-outputs-organizer`; never deliver raw generations or edit-bin copies.
2. **Dry run** (writes nothing):
   ```
   python3 scripts/deliver.py --project P --target instagram_reels --from-final "Promos/03-Rise" --loudness
   python3 scripts/deliver.py --project P --target client --client "Acme" --from-final "Long_Videos/01-Main_Film" --version 2
   ```
   Every file gets `OK`, `WARN` or `FAIL` with its measured specs.
3. **Fix FAIL lines before anything else.** Typical fixes, each one only after the user's yes, since it creates a new render:
   - wrong aspect for the target: deliver the matching aspect from the finals tree, or ask for a reframe;
   - too long: a cut-down is an editing decision, ask the user;
   - codec / pixel format: re-encode a delivery copy, never the final itself:
     `ffmpeg -i in.mov -c:v libx264 -pix_fmt yuv420p -crf 18 -preset slow -c:a aac -b:a 320k -movflags +faststart out.mp4`
   - a private reference in the list: remove it, tell the user how it got there.
   WARN lines (no captions, loudness off target, below 1080) go to the user as a short list; they decide.
4. **Apply after the user's yes:** same command plus `--apply` (and `--zip` for a single downloadable file).
5. **Report**: the folder path, the file list with sizes, what is auto-generated (thumbnails taken from a frame should be
   replaced with designed covers), and the checksum command the receiver can run: `shasum -a 256 -c CHECKSUMS.sha256`.

## Naming rules

- Client: `<Client>_<Title>_<aspect>_<LANG>_v<NN>.<ext>`. `--version` counts deliveries to that client, not renders.
- Platform: `<Title>_<platform>_<aspect>_<LANG>.<ext>`.
- ASCII letters, digits, `-` and `_` only. No spaces, no Cyrillic, no dates in names (the folder carries the date).
- Captions and thumbnails share the video's name: `<name>.srt`, `<name>_thumb.jpg`.

## Captions and covers

- Captions are picked up when a `.srt` / `.vtt` with the same stem sits next to the source video.
- A cover is picked up from `<stem>_thumb.jpg|png`, otherwise one frame at one third of the video is extracted and flagged.
- On-screen text and captions follow the project's text rules (for example, no long dashes) and the project fonts.

## Rules

- Never upload, post or send. Publishing is a separate step that needs the user's explicit approval.
- Never overwrite a delivery folder; a second delivery the same day needs `--version` or a new target name.
- Platform limits change. Treat the built-in table as a first check; when a file is close to a limit, check the platform's
  current help page before telling the user it will pass.
- Delivered packages are archived later with `versions-and-archive --what delivered`.

## Related skills

`final-outputs-organizer` (source of finals), `reference-library-organizer` (leak check data), `versions-and-archive`,
`render-cut-verification`, `marketing-manager` (posting, only with approval).
