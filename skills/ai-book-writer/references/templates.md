# Templates

All cards are in **English**, whatever language the book is written in. Copy them verbatim and fill the brackets.
Quotes from the manuscript (audit anchors) stay in the manuscript's language. Connector notation and rules:
`causality.md`.

---

## 1. SCENE CARD

```
SCENE [ch.scene, e.g. 3.2] - [working title]
Chapter: [N]  |  Owner: [name]  |  Place / time: [where, when]
Point (one sentence, sketch test): [what this scene is as a standalone number]
Chapter beat carried: [which beat of the chapter circle this scene delivers]
Hand-off in: [THEREFORE | BUT] from scene [N-1] beat 8: [what produced this need]

1. YOU ........ [the owner's normal in these pages, shown by action]
        | THEREFORE / BUT
2. NEED ....... [what they want here and now, tactically]
        | THEREFORE / BUT
3. GO ......... [crossing the line: which tactic they choose, and what going already costs]
        | THEREFORE / BUT
4. SEARCH ..... [resistance: attempt 1 - BUT - attempt 2 - BUT - attempt 3]
        | THEREFORE / BUT
5. FIND ....... [they get it, distorted: exactly how it is distorted]
        | THEREFORE / BUT
6. TAKE ....... [what they lose for good]
        | THEREFORE / BUT
7. RETURN ..... [how they come back, carrying the price]
        | THEREFORE / BUT
8. CHANGE ..... [visible action / object / line / refusal impossible at beat 1]

HAND-OFF OUT: [THEREFORE | BUT] -> need of scene [N+1]: [which]

Partial circles in the scene:
  [name] - beats [which]: [one line]

Prose notes: POV [first/third, whose] | tense [past/present] | enter at [beat] | leave at [beat]
Threads: opens [thread id] | pays off [thread id]

Checks:
  [ ] one owner             [ ] find != need            [ ] price cannot be restored
  [ ] change is shown       [ ] no "and then" joint     [ ] point not shared with another scene
  [ ] hand-off in and out   [ ] beats 3-6 carry ~2/3 of the words
```

---

## 2. CHAPTER CARD

```
CHAPTER [N] - [title]
Owner: [name]  |  Scenes: [count]
Chapter point / epigraph: [optional]
Hand-off in: [THEREFORE | BUT] from chapter [N-1] change: [what]

Chapter circle:
1. YOU ........ [ ] -> scene [ ]
2. NEED ....... [ ] -> scene [ ]
3. GO ......... [ ] -> scene [ ]
4. SEARCH ..... [ ] -> scenes [ ]
5. FIND ....... [ ] -> scene [ ]
6. TAKE ....... [ ] -> scene [ ]   (bigger than any scene price inside the chapter)
7. RETURN ..... [ ] -> scene [ ]
8. CHANGE ..... [ ] -> scene [ ]

Chapter connector chain:
1 --[ ]--> 2 --[ ]--> 3 --[ ]--> 4 --[ ]--> 5 --[ ]--> 6 --[ ]--> 7 --[ ]--> 8

Scene hand-off chain:
S1 --[ ]--> S2 --[ ]--> S3 ==[ ]==> chapter [N+1]

Hand-off out: [THEREFORE | BUT] -> need of chapter [N+1]: [what]
Book beat moved: [which beat of the book circle this chapter advances]
Threads opened: [ids]   Threads paid off: [ids]
```

---

## 3. BOOK CARD

```
BOOK - [title]
Language: [prose language]  |  POV plan: [single / rotating / first person]  |  Tense: [past / present]
Protagonist(s): [who]  |  Antagonist: [who]

Book circle (protagonist):
1. YOU ........ [world and normal before everything]
2. NEED ....... [through-line want] | TRUE NEED: [what they actually need]
3. GO ......... [point of no return - chapters: ]
4. SEARCH ..... [chapters: ] - [what the whole middle is busy with]
5. FIND ....... [chapters: ] - [gets the want, distorted]
6. TAKE ....... [chapters: ] - [what is lost for good]
7. RETURN ..... [chapters: ]
8. CHANGE ..... [chapters: ] - [how it is proven on the page]

Antagonist circle (sparse): need [ ] | price [ ] | change [ ]
Side circles: [name] - which beats they carry, where they start, where they break off

Want / need gap: the hero thinks they want [ ], they actually need [ ].
  Moment they see it: [chapter / scene]
```

---

## 4. AUDIT REPORT (Mode B)

```
AUDIT: [chapter / scene], [word count], language: [ ]

-- WHAT IS THERE -----------------------------------
[scene card filled from the actual text;
 each beat with a 3-6 word anchor quote, or MISSING]

-- CHAIN -------------------------------------------
1 --THEREFORE--> 2 --BUT--> 3 --AND THEN (dead)--> 4 ...
[every dead joint marked]

-- LINTER (scripts/prose_lint.py) ------------------
[counts per category; only the hits that survived reading in context, with line numbers]

-- DIAGNOSIS (most severe first) -------------------
1. [defect] - [why it breaks the scene for the reader]
2. ...

-- FIXES -------------------------------------------
[for each defect: exactly what to insert / cut / move, with the location in the text.
 Not general advice: a decision. Rewrites in the book's language.]

-- WHAT WORKS (leave alone) ------------------------
[what holds the scene up, so that the fix does not break it]
```

---

## 5. SEARCH-BEAT WORKSHEET (beat 4 of a big scene)

```
Goal on entry: [what they are trying to get]
Attempt 1: [tactic] -> BUT [how it failed] -> [what they learned or kept]
Attempt 2: [tactic grown out of failure 1] -> BUT [how it failed] -> [what they learned or kept]
Attempt 3: [tactic at the limit] -> THEREFORE [opens onto the find]
Inner shift between 4 and 5: [what they understand about themselves that makes beat 7 possible]
How the shift is shown (not told): [gesture / object / line]
```
