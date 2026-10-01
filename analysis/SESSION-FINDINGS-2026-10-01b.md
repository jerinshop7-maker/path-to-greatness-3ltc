# Path to Greatness (3 LTC) — round 7, 2026-10-01 (the music layer)

Fourth analysis session. Round 6 (`SESSION-FINDINGS-2026-10-01.md`) established
that clue 5's poem is a lyric collage. This round *hardens* that, corrects one of
its errors, and records the first oracle-checkable test the music corpus permits.
Oracle still prints `SELFTEST OK`. New tool: `tools/clue5_music.py`.

---

## 1. HEADLINE — line 2 IS a lyric quote; the round-6 "unidentified" is wrong

Round 6 said line 2, `A thousand maps drawn with blood`, returned "no lyric hit;
its source is **unidentified**", and dismissed the single web match as "an
unrelated astronomy forum poem".

**That is wrong. Line 2 quotes Vintersorg — "Astral and Arcane" (album *Cosmic
Genesis*, 2000).** The real lyric is

> *"I open the atlas to solitary spheres, **thousand maps drawn with blood**"*

The "unrelated astronomy forum" is the CosmoQuest thread *Astronomy in poetry and
song*, and its snippet is the Vintersorg lyric itself: the forum was quoting the
song, exactly as the author did. The author simply prefixed `A` to make the
poem's metre scan (the same light-touch rewrite as `living life in peace` →
`Livin' life today` in clue 1).

So clue 5 now has **six verbatim lyric sources, not five**:

| line | quote | source | album | year | track |
|---|---|---|---|---|---|
| 2 | `...thousand maps drawn with blood` | **Vintersorg — "Astral and Arcane"** | *Cosmic Genesis* | 2000 | 1 |
| 4 | `To shelter my ship on the flood` | **Falkenbach — "Havamal"** | *Heralding – The Fireblade* | 2005 | 3 |
| 5 | `We used to swim the same moonlight waters` | **Nightwish — "Ghost Love Score"** | *Once* | 2004 | 9 |
| 6 | `Dragged by the force of some inner tide` | **Pink Floyd — "High Hopes"** | *The Division Bell* | 1994 | 11 |
| 7 | `No longer will we wait for your answers` | **Coheed and Cambria — "Three Evils"** | *In Keeping Secrets of Silent Earth: 3* | 2003 | 4 |
| 8 | `With the stars in the sky our guide` | **Alestorm — "Treasure Island"** | *No Grave But the Sea* | 2017 | 10 |

Every source is independently verifiable: the Vintersorg line is on Genius,
darklyrics and the band's own Spotify; the Havamal line is the Edda's famous
ninth stanza and is Falkenbach track 3; the Nightwish line is the *opening*
line of track 9; the Floyd and Coheed lines are exact; the Alestorm line opens
track 10. Track numbers are album metadata, not inferences about the puzzle.

---

## 2. CONFIRMED this round

| # | Fact | Evidence |
|---|---|---|
| **R7-C1** | Clue 5 line 2 = Vintersorg "Astral and Arcane" (*Cosmic Genesis*, 2000, track 1). | Phrase search; the forum hit is a quotation of this song. |
| **R7-C2** | Clue 5 has **six** identified lyric sources (lines 2,4,5,6,7,8), each with independently confirmed album + year + track number. | Table above; `tools/clue5_music.py`. |
| **R7-C3** | Lines 1 and 3 (`Charting the eight wonders`, `A bit of help from each line`) return **no** lyric hit in any phrasing tried, including with the leading article stripped — the same trick that recovered line 2. They are the author's own instruction, not quotes. | Multiple phrase searches. |
| **R7-C4** | Clues 4, 6 and 7 are **not** lyric collages: their poem lines return no web lyric hit. The collage habit is specific to clue 5 (plus clue 1's Imagine rewrite). | Phrase searches for clue 4's "period of madness"/"order in the court", clue 7's "great undertaker"/"frigid ocean", clue 6's "counting starts with a deer". |
| **R7-C5** | The author's **second** album, *Archaic Reveries* (2018), has **exactly 8 tracks**: Age of Lamps, Lost and Found, Welcome to the Mansion, Effugium, On the Other Side, Alone, Seven Miles, The Regents. | Amazon Music album B07DQH55PC, read here. |

---

## 3. The "eight wonders" is now a fork, not a guess

Line 1 says `Charting the eight wonders`. Two concrete readings:

**(a) The canonical 8 wonders of the world** = the New7Wonders **plus** the Great
Pyramid of Giza (the "eighth"). This is the standard reason a list has *eight*
and not seven, and it is exactly the reading round 5 refuted numerically: the
haversine sweep over New7Wonders + Giza (+21 other monuments) failed under both
units. So the *list* is plausible; the *distances* still don't reproduce
12,772 / 5,210 / 12,061 (and 12,772 mi = 20,554 km is beyond any great-circle
distance, ~20,004 km, so row 1 cannot be a simple surface distance under `mi`).

**(b) The author's own 8-track album _Archaic Reveries_.** Clue 8 already uses
the author's *first* album as its dictionary, and `eight` is a suspiciously exact
match for the track count. Note track **7 is literally "Seven Miles"** — a
distance-themed title on an 8-track album, in a clue whose panels carry `mi` and
`km`. This is the reading I would test first, because it stays inside material
the author controls.

Both survive; neither is proven. The author's own album is the cheaper to test.

---

## 4. New negatives

| Family | Space | Result |
|---|---|---|
| **Music-corpus clue-2 answer**: every 15-character window of the normalised titles/artists/albums (all six quotes + both of the author's albums + all *Seconds of Dream* tracks), plus the joined-corpus windows, as the clue-2 half of segment 4 | 462 candidates × 2 pinned skies = **924 pairs** | **0** (`tools/clue5_music.py`) |
| Lines 1/3 as lyric quotes | all phrasings tried | 0 hits → they are instructions (R7-C3) |
| Clues 4/6/7 as lyric collages | all phrasings tried | 0 hits (R7-C4) |

The music-corpus test is the only oracle-checkable experiment this material
affords: **clue 5 cannot be oracle-tested**, because segment 2 needs the 12-char
chess answer as well as the 20-char wonders answer. Everything about clue 5's
*mechanism* is therefore hypothesis, and must be judged structurally, not by a
64-bit oracle. Stating this plainly matters, because round-6/round-7 write-ups
risk presenting clue-5 structure as though it were testable.

---

## 5. Leading (unproven) structural hypothesis

```
clue 5
  8-line poem
    ├── line 1  "Charting the eight wonders" ............ INSTRUCTION
    ├── line 2  → Vintersorg   "Astral and Arcane"  ...... CONFIRMED
    ├── line 3  "A bit of help from each line" .......... INSTRUCTION
    ├── line 4  → Falkenbach   "Havamal" ................ CONFIRMED
    ├── line 5  → Nightwish    "Ghost Love Score" ....... CONFIRMED
    ├── line 6  → Pink Floyd   "High Hopes" ............. CONFIRMED
    ├── line 7  → Coheed       "Three Evils" ............ CONFIRMED
    └── line 8  → Alestorm     "Treasure Island" ........ CONFIRMED
            ↓  SIX source works
       SIX non-triangle pictograms  (2 per row × 3 rows)
            ↓
       THREE rows × a Roman numeral  (12772 / 5210 / 12061 ; units mi/km/mi)
            ↓
       ONE 20-character answer
```

Tentative pictogram ↔ song reading (first pass, unverified — the drawings need
better eyes): `star-?-star`→Astral and Arcane, `headstone+heart`→Ghost Love
Score, `anchor`→Treasure Island, flowering sprig→High Hopes, horned beast→
Havamal, horned mask→Three Evils. Four of six fit naturally; sprig and mask are
guesses. The step-2 obligation is to make the pairing *systematic* or drop it.

---

## 6. Route tree (round 7, ranked by expected value per hour)

```
META-THEME: the image clues are built from music (clue 1 Imagine, clue 5 six
prog/metal quotes, clue 8 track titles). Treat song material as first-class.

SEGMENT 4  scramble(15) + sky(17)          <-- ONLY oracle-testable hot spot
├── SKY  71520219618128920 .... best candidate (reproduces both witnesses)
│        58112171456182114 .... repo structural candidate
│        value-as-index into tracks .... PROVEN IMPOSSIBLE
└── SCRAMBLE (the bottleneck; 800k+ hypotheses, 0)
    ├── arithmetic / positional / keyboard / permutation / ordering-key .. 0
    ├── music-corpus 15-windows .............................. 0 (NEW, R7)
    └── ??? non-arithmetic reading of the 15 capitals

SEGMENT 5/2  chess(12) + wonders(20)       <-- NOT oracle-testable alone
├── WONDERS
│   ├── six lyric sources now CONFIRMED (R7)
│   ├── "eight wonders" fork:
│   │      (a) New7Wonders + Giza ....... list ok, distances fail
│   │      (b) Archaic Reveries (8 tracks) ... NEW, test first
│   ├── pictograms ↔ songs (systematic pairing) ... step-2 obligation
│   └── numerals → 20 chars: mechanism still unknown
│         (numeral digit-sums 19/8/10, mod-26 F/J/W, factors 2²·31·103 /
│          2·5·521 / 7·1723 — none yet meaningful)
└── CHESS  14 pieces → 12 chars, case kept; "symbol that's flown" flag idea

SEGMENT 1  imagine(16) + beach(16)
├── beach = 15 measured notes + 1 convention char ..... OPEN
└── imagine = the Imagine lyric with a number substituted ..... OPEN
        (clue 1 is a *song rewrite*, so read it as a lyric masquerade)

SEGMENT 3  wasd(8) + ship(24)
├── 8 no-predecessor roots → 8 chars (53214124 / 2415+1234) ..... OPEN
└── ship = the Titanic montage described ........................ OPEN
```

---

## 7. Practical next steps (concrete, in order)

1. **Settle the "eight wonders" fork.** Pull the *Archaic Reveries* lyric/artwork
   and test whether its 8 track titles can be read by clue 5's three numerals —
   cheap, author-controlled, parallels clue 8.
2. **Make the pictogram↔song pairing systematic.** If the 6 drawings map
   bijectively to the 6 confirmed songs, that is strong; if not, drop the pairing
   and keep only the "8/6 musical sources" fact.
3. **Re-attack clue 2** (the one segment-4 blocker). The 15 capitals are
   `BPEFJDFPOCDBDNB`; the instruction is "with your capital, addition. to the
   lower, subtract." Music-corpus words fail; consider that "capital"/"lower"
   may be *typographic case* and the 5 dashes are operators, not letters.
4. **Clue 1 as a lyric masquerade**: the replaced word and `19410712`.

---

## 8. One-line status

Clue 5's poem is a six-song lyric collage (line 2 newly confirmed as Vintersorg's
"Astral and Arcane"; lines 1 and 3 are the author's instruction). The
"eight wonders" is now a two-way fork — the canonical New7Wonders+Giza list, or
the author's own 8-track *Archaic Reveries* — and the music corpus supplies no
clue-2 answer (924 pairs, 0). Segment 4 (clue 2) remains the only segment that
can be oracle-tested, and therefore the only place a real break can land.
