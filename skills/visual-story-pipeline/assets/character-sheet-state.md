# Character sheet — state/weather variant

Use when a character needs a LOCKED alternate physical state that will recur across multiple shots
or scenes — soaked from rain, muddy, injured/bandaged, a mid-story costume change, exhausted/disheveled,
etc. Generate this *in addition to* the character's basic or full sheet, never as a replacement for
it — it's a variant layer on top of the locked base identity.

```
Create a character reference panel showing the SAME character from [basic-sheet / full-sheet — link
which one] in a specific altered state, for consistent AI generation of this state across multiple
scenes.

Base identity: [restate the locked face/hairstyle/build from the character's existing sheet —
copy verbatim, do not re-describe from memory]

State to lock: [name the exact state, e.g. "soaked from heavy rain" / "mud-streaked from a fall" /
"freshly bandaged left forearm" / "changed into [specific new costume, full fabric/color detail]"]

State-specific details to hold constant across every future shot using this state:
- [e.g. "hair damp and darkened, plastered to forehead and temples"]
- [e.g. "dark damp patches on shoulders and upper back of the jacket, fabric visibly heavier/wetter"]
- [e.g. "water droplets on exposed skin, slight sheen"]
- [e.g. "mud spatter pattern on lower legs and boots, same placement and density every shot"]

Layout: Front Portrait + Full Body Front, plain neutral grey studio background, same lighting as
the character's base sheet.

Style & Consistency: identical face, proportions, and base costume/identity as the character's
locked base sheet — only the named state changes. Preserve the state-specific details exactly as
listed above.

Requirements: neutral grey background only, no text/labels/logos/watermarks/extra props beyond
what's named above/extra characters.
```

Attach the character's base sheet and real face photo alongside this prompt.

## Using a state variant in production

When a scene calls for this character in this state (e.g. the master shot establishes rain and this
character has just come in from it — see the weather-propagation rule in
`04-prompt-engineering.md`), attach the state-variant panel alongside the base sheet and real face
photo, and say so explicitly in the prompt:

> "Use the attached state-variant panel for the [wet/muddy/injured/etc.] appearance. Match the
> [specific state details] exactly."

Once a state variant is approved, treat its listed details as locked text to copy verbatim into
every prompt using that state — same as any other recurring-detail lock.
