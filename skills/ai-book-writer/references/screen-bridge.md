# Screen bridge: scene card to shot list (Mode F)

Turns an approved scene into something a visual pipeline can generate: a list of **visual beats**, a **shot
table**, and a **REFERENCES_NEEDED** list, then hands off to the pipeline skills. Any chapter can go to images or
video this way without re-reading the whole book.

Input: an approved scene card plus the finished prose of that scene (and the book profile, if present).
Output: one markdown file per scene, for example `screen/1.1_shots.md`, in English. Dialogue lines are copied
from the prose in the book's language unless the production says otherwise.

## Step 1. Visual beats

Go through the scene beat by beat (1 to 8) and write each moment as **one visible image**: who, doing what, with
which object, where the eye goes. One visual beat = one thing the camera can see.

The hard part is the inner world. Prose can say "she understood"; a camera cannot. Every thought, feeling or
realization must be converted to an **action, an object, or a look**:

| In the prose | On screen |
|---|---|
| She realizes the card is in the dead wife's hand | She holds the card next to a note pinned on the wall; the same slanting letters |
| He misses his wife | He sets out two cups, then puts one back |
| She is ashamed signing the false sheet | The pen stops halfway through her name; she finishes it fast |
| She decides not to check her own ear any more | The tuning fork is lifted over her knee and put back unstruck |
| Backstory (her teacher's rule) | Cut it, or plant an object that carries it (a worn fork engraved with initials) |

If a beat has no visible equivalent, either it carries voice-over (only if the narrator's voice is part of the
adaptation's style) or the beat needs restaging. Never leave a shot that "shows a thought".

Checks before the table:
- Beat 6 (the price) is a shot, not an implication. The audience must see what is lost.
- Beat 8 (the change) is a shot, and it rhymes with a beat 1 shot (same object or action, different outcome).
- On-screen text (letters, cards, signs) is a generation risk: keep handwriting unreadable in the image and carry
  the words in dialogue, voice-over, or an insert added in the edit.

## Step 2. Shot table

Columns, in this order:

```
| # | scene | visual beat | shot size + why | camera move (small, motivated) | duration | dialogue/VO | references needed | start/end frame |
```

Rules:
- **Duration 4 to 5 s per clip.** A visual beat longer than 5 s becomes two shots chained by start/end frames.
- **Shot size + why:** name the size and the job it does (orientation, gesture, emotion, contact with an object,
  detail accent, relationship, dialogue). No two adjacent shots share the same size and job. The full rationale
  pass is `storyboard-shot-selection`.
- **Camera move:** small and motivated: a slow push toward the detail the character is looking at, a tilt that
  follows a hand, a short follow as someone exits. No orbits or swoops that the story does not ask for. Static is
  a valid choice.
- **Start/end frame:** describe the first and last image of the clip. When action is continuous across a cut, the
  end frame of shot N is the start frame of shot N+1 (that is what lets a video model chain them).
- **References needed:** the IDs from the REFERENCES_NEEDED list, not descriptions.

## Step 3. REFERENCES_NEEDED

One list per scene (merged per chapter when a whole chapter goes to production):

```
REFERENCES_NEEDED - scene [N.M]
Characters (costume per scene):
  [CHAR_ID] - [costume name]: [one-line spec] - scenes [ ]
Locations (with states):
  [LOC_ID] - state [name]: [time of day, light, weather, tidiness, what is open/closed] - shots [ ]
Props (with states):
  [PROP_ID] - [state]: [one-line spec] - shots [ ]
```

Costume and prop **versions across chapters** (a coat that gets torn in chapter 4) are kept by
`story-continuity-ledger`; use its version valid for this chapter and its fixed spec wording.

## Step 4. Hand-off to the pipeline

Name the next skill and what it receives:

1. `script-extractor`: for a whole chapter or several scenes, extract every location (day/night), character,
   prop and wardrobe item per scene from the prose; reconcile with the REFERENCES_NEEDED lists.
2. `storyboard-narrative-breakdown`: when a sequence is continuous movement through events or places, turn the
   visual beats into numbered mini-scenes with bridging elements.
3. `storyboard-shot-selection`: validate each shot size and write its rationale into the shot description; fix
   adjacent shots that do the same job.
4. `visual-story-4-references`: build a reference sheet for every entry in REFERENCES_NEEDED (characters per
   costume, locations per state, props per state) before any shot is generated.
5. `cinematic-prompt-writer`: write the still prompt for each start and end frame, attaching the references
   listed in the table.

Video prompts for the clips come after the stills are approved, with the pipeline's own video-prompt skills.

---

## Worked example: scene 1.1 "The Flat Piano"

From `example.md`: the approved card, with the fixed prose for beats 4 to 8 (lines for beats 1 to 3 are
taken from the full draft, which the example does not reprint). 14 shots, about 64 s.

| # | scene | visual beat | shot size + why | camera move | dur | dialogue/VO | references needed | start/end frame |
|---|---|---|---|---|---|---|---|---|
| 1 | 1.1 | B1 Ines strikes the fork on her knee, holds it to the open piano | MCU: face concentration plus contact with the fork | slow push-in toward the fork as it rises | 4 s | - | INES/work, HALE_FLAT/afternoon, FORK, PIANO/lid-closed | start: Ines bent over keys / end: fork beside her ear |
| 2 | 1.1 | B1 the folded final notice in her open kit case | ECU: detail accent, the pressure under the job | tilt down from her hands into the case | 4 s | - | KIT_CASE/open, NOTICE | start: hands on keys / end: notice fills frame |
| 3 | 1.1 | B2 Hale in the doorway, wallet in hand, sets his condition | Medium: emotion plus contact with the wallet | static, rack focus from Ines to Hale | 5 s | Hale: "I pay when it sounds like Clara's." | HALE/home, WALLET | start: Ines in focus / end: Hale in focus |
| 4 | 1.1 | B3 Ines cancels her next job by phone, eyes on the piano | MCU: the choice on her face | static | 4 s | Ines: "I'll be late. Very late." | INES/work, PHONE | start: phone rising / end: phone lowered |
| 5 | 1.1 | B4 attempt 1: she plays, Hale listens eyes shut | OTS from behind Hale: the relationship, judge and judged | slow lateral drift past his shoulder | 5 s | Hale: "A shop piano. Bright." | HALE/home, INES/work, PIANO/lid-closed | start: Hale's shoulder / end: Ines's hands stop |
| 6 | 1.1 | B4 attempt 2: wallet goes back into the drawer | Insert CU: detail accent, the fee withdrawn | static | 4 s | - | WALLET, DRAWER | start: wallet in hand / end: drawer shut |
| 7 | 1.1 | B4 attempt 3: Hale hums, Ines hears the sour note | CU on Ines: the discovery is the emotion | small push-in on the sour note | 5 s | Hale hums (diegetic) | INES/work | start: Ines listening / end: her head tilts |
| 8 | 1.1 | B4 she lifts the lid, finds the pencil card between the pins | ECU: the card, handwriting unreadable | tilt following the lid up | 4 s | - | PIANO/lid-open, CLARA_CARD | start: lid rising / end: card between pins |
| 9 | 1.1 | B5 the lever hovers over the B flat pin: the choice | CU: emotion, the hesitation | static, held | 5 s | VO (optional): "B flat. Leave it." | INES/work, LEVER | start: lever lifted / end: lever seated on the pin |
| 10 | 1.1 | B6 the lever turns a hair to the left | ECU: detail accent, the act of breaking her own work | micro push-in | 4 s | - | LEVER, PIANO/lid-open | start: lever seated / end: lever turned |
| 11 | 1.1 | B6 she signs "tuned to standard", presses the sticker next to the card | Medium top-down: gesture plus objects in one frame | tilt from sheet to lid | 5 s | - | SERVICE_SHEET, STICKER, CLARA_CARD | start: pen on the line / end: sticker beside card |
| 12 | 1.1 | B7 Hale plays and laughs on the fourth note | Wide: the room, Hale at the piano, Ines small by the window | static | 5 s | Hale laughs | HALE_FLAT/afternoon, HALE/home, INES/work | start: Hale's hands land / end: his head thrown back |
| 13 | 1.1 | B7 at the door he presses Clara's card into her hand | Medium two-shot: the relationship, the object changes hands | short follow onto the hands | 4 s | Hale: "You'll need it next time." | HALE/home, INES/work, CLARA_CARD, CASH | start: door open / end: card in her palm |
| 14 | 1.1 | B8 on the landing she lifts the fork over her knee and puts it back unstruck | Full: body language in the stairwell, rhymes with shot 1 | static; she walks out of frame | 5 s | - | INES/work, LANDING/late-afternoon, FORK | start: fork raised / end: empty landing |

```
REFERENCES_NEEDED - scene 1.1
Characters:
  INES - work: grey cardigan with pushed-up sleeves, dark trousers, canvas tool roll - scenes 1.1, 1.2, 1.3
  HALE - home: brown cardigan, pressed shirt, worn slippers - scenes 1.1, 1.3
Locations:
  HALE_FLAT - afternoon: high-ceilinged living room, upright piano by the wall, low sun through half-drawn
              curtains, dust in the light - shots 1-13
  LANDING - late-afternoon: old stairwell, tiled floor, window light from above - shot 14
Props:
  PIANO - lid-closed / lid-open (tuning pins visible) - shots 1, 5, 8, 10
  FORK - steel tuning fork, worn - shots 1, 14      LEVER - tuning lever, wooden handle - shots 9, 10
  KIT_CASE - open, tools in loops - shot 2          NOTICE - folded final rent notice - shot 2
  WALLET - old leather - shots 3, 6                 DRAWER - sideboard drawer - shot 6
  CLARA_CARD - small card, pencil handwriting, unreadable - shots 8, 11, 13
  SERVICE_SHEET - printed form with a signature line - shot 11
  STICKER - small round guarantee sticker, no legible text - shot 11
  CASH - a few folded notes - shot 13             PHONE - plain mobile phone - shot 4
```

Hand-off: chapter 1 goes to `script-extractor` (all three scenes), then `storyboard-shot-selection` on this
table, then `visual-story-4-references` for the list above, then `cinematic-prompt-writer` for start and end
frames of shots 1 to 14.
