# Deliverables - aspects, cutdowns, specs and naming

Fill `00_BRIEF/DELIVERABLES.md` from the tables below at Step 3 (so every shot is planned for every aspect) and verify
every row at Step 6.

## 1. Aspect sizes

| Aspect | Delivery size | 4K variant | Typical use |
|--------|---------------|------------|-------------|
| 16:9 | 1920x1080 | 3840x2160 | website hero, YouTube, pre-roll, event screens, pitch decks |
| 2.39:1 inside 16:9 | 1920x1080 with bars at about 138 px top and bottom | 3840x2160 | cinematic master when the brief allows letterbox |
| 9:16 | 1080x1920 | 2160x3840 | Reels, Shorts, TikTok, Stories |
| 1:1 | 1080x1080 | 2160x2160 | feeds, marketplaces |
| 4:5 | 1080x1350 | 2160x2700 | Instagram and Facebook feed |

Letterbox bars belong only in the 16:9 cinematic master. Vertical, square and 4:5 versions are full frame.

## 2. Safe zones (plan at Step 3, check at Step 5)

- **Title-safe** for all aspects: keep text and logo inside the central 90 % of width and height.
- **9:16 platform UI:** keep text, faces and the product out of the top about 14 % (account name, close button) and the
  bottom about 20-25 % (caption, buttons); keep the right edge about 12 % clear of text (action icons).
- **4:5 and 1:1 feeds:** the first frame becomes the cover crop; keep the subject central.
- Captions sit above the lower UI band in 9:16, inside title-safe in other aspects.

## 3. Reframing strategy

1. Decide the **hero aspect** from the brief (where most viewers watch). Generate and design for it first.
2. For each shot, mark the **protected area** in the shot list: the region that must survive in every aspect (face, the
   product, the action point).
3. When the hero aspect is 16:9 and 9:16 is also needed, compose with the protected area within the central third, or
   generate a native vertical still for shots where the action spans the width.
4. Reframe shot by shot with keyframed position (a pan inside the crop may follow the action), never a blind centre crop.
5. Run `frame-crop-guard` on every composition that crops a source; fix LOST_SUBJECT and FACE_CUT flags before render.
6. Re-check graphics per aspect: titles and the end card are laid out per aspect, not scaled.

## 4. Cutdown matrix

| Cut | Structure | Rule |
|-----|-----------|------|
| 90 / 60 s master | full concept | built first only if ordered; otherwise the 30 s is the master |
| 30 s | hook, setup, turn, payoff, brand moment | the default hero length |
| 15 s | hook, turn, payoff, brand moment (setup folded into the hook) | re-cut, not a trim of the first 15 s |
| 6 s bumper | one striking image, one claim, logo | built from the strongest shot; sound-off readable |
| Text-free master | each length without titles and claim cards | for localization and broadcaster re-versioning |

Cutdowns are new edits. The brand moment always survives; the hook may change to a stronger shot for short feeds.

## 5. Language versions

- One master edit, then per language: on-screen text cards, captions, VO (if any), share copy.
- Text expands in some languages (German and French often 20-35 % longer than English); design cards with room and test
  the longest language first.
- Test the typeface renders every script used (Latin, Cyrillic, Greek, Arabic, CJK); switch to a covered family rather
  than letting fallback fonts appear.
- VO is re-timed per language; picture cuts may shift a few frames. Keep J and L cuts.

## 6. Technical specs (defaults; the platform or client spec wins)

| Item | Default |
|------|---------|
| Frame rate | 24 fps (23.976 only if the client's broadcast chain needs it); keep one rate across all versions |
| Video codec | H.264 High profile, yuv420p, for web and social; ProRes 422 HQ master on request |
| Bitrate | 1080p about 16-20 Mbps; 4K about 45-60 Mbps |
| Audio | AAC 48 kHz stereo, 320 kbps; WAV 48 kHz 24-bit stems on request |
| Loudness | social and web about -14 LUFS integrated, true peak -1 dBTP; broadcast per region (EBU R128 -23 LUFS or -24 LKFS) |
| Captions | .srt and .vtt per language, timed to the encoded file |
| Cover frame | one still per aspect, chosen frame, no platform UI baked in |
| Colour | Rec.709, full checks on a calibrated display or scopes |

## 7. Naming

Use the client naming rule of `delivery-package`, with the cut length inside the title field:

```
<Client>_<Title>-<cut>_<aspect>_<LANG>_v<NN>.mp4
Acme_Launch-30_16x9_EN_v01.mp4
Acme_Launch-15_9x16_DE_v02.mp4
Acme_Launch-06_1x1_EN_v01.mp4
Acme_Launch-30_16x9_TEXTLESS_v01.mp4
```

- `<cut>`: 90, 60, 30, 15, 06.
- `<aspect>`: 16x9, 9x16, 1x1, 4x5, 239 (letterboxed master).
- `<LANG>`: two-letter code, or TEXTLESS for text-free masters.
- Versions never overwrite: a change is a new `v<NN>`.

## 8. Share copy per platform

For each platform and language: a caption that leads with the feeling (not the feature list), the claim in the client's
words, the call to action, alt text that describes the film for screen readers, hashtags in the brand's tone (few and
specific), and the AI-generated imagery disclosure where the platform or client requires it.

## 9. Final verification

For every file in the matrix:
- `render-cut-verification` on the encoded file (cut strip, black and flash scan, stream lengths, loudness, true peak).
- Aspect, size, frame rate, duration and naming match this sheet.
- Product contact sheet approved; claim text matches the brief character for character.
- `delivery-package` builds the package with checksums and the delivery note.
