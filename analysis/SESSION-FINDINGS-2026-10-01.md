# Path to Greatness (3 LTC) — round 6, 2026-10-01

Third analysis session on this repository (rounds in
`SESSION-FINDINGS-2026-09-30.md`). Everything below was re-derived or newly
tested here; the oracle still prints `SELFTEST OK` on this machine. New tooling
this round: `tools/clue2_pixels.py`, `tools/clue2_ink.py`,
`tools/clue2_positional.py`.

---

## 1. HEADLINE — the clue poems are lyric collages (NEW, partly CONFIRMED)

**Clue 5's poem is not original. Five of its eight lines are verbatim quotations
from five different prog/metal songs.** This was never recorded anywhere in the
repository. The background was found by phrase search and every quote below is
matched word-for-word.

| Clue-5 line | Verbatim source | Artist / song | Year / album |
|---|---|---|---|
| 4 `To shelter my ship on the flood` | `I know a ninth, when need I have / To shelter my ship on the flood` | **Falkenbach — "Hávamál"** | 2005, *Heralding – The Fireblade* |
| 5 `We used to swim the same moonlight waters` | opening line, identical | **Nightwish — "Ghost Love Score"** | 2004, *Once* (also live, *End of an Era*) |
| 6 `Dragged by the force of some inner tide` | `Dragged by the force of some inner tide / At a higher altitude with flag unfurled` | **Pink Floyd — "High Hopes"** | 1994, *The Division Bell* |
| 7 `No longer will we wait for your answers` | `No longer... will we wait for your answers / Back to the hell where you've come from` | **Coheed and Cambria — "Three Evils (Embodied in Love and Shadow)"** | 2003, *In Keeping Secrets of Silent Earth: 3* |
| 8 `With the stars in the sky our guide` | `With the stars in the sky our guide / Voyage ever onwards` | **Alestorm — "Treasure Island"** | 2017, *No Grave But the Sea* |

Lines 1–3 (`Charting the eight wonders`, `A thousand maps drawn with blood`,
`A bit of help from each line`) return no lyric hit; line 2's phrase appears in
an unrelated astronomy forum poem and its source is **unidentified**.

The same collage habit is visible elsewhere in the puzzle:

- **Clue 1** is a rewrite of Lennon's "Imagine" ("living life in peace" →
  "Livin' life today"), which the repository already knew.
- **Clue 8's two worked examples are album track titles** — but the *reason* the
  panel chose them is Metallica's "Enter Sandman": "Exit light, enter night".
  `Exit Light` and, by the same register, `Ghost March` are the author's own
  track titles chosen so that the lyric falls out.

**Interpretation for the route tree.** The clue images are assembled from song
material: lyrics, song titles, and the author's own album. That makes the
"eight wonders" of line 1 (`Charting the eight wonders`) most plausibly **eight
songs** — a playlist the poem quotes from — not eight monuments, and it makes
`A bit of help from each line` an instruction to take one piece from each
quoted song. The 20-character answer is the extraction; the mechanism (title?
next word? album? year? track number?) is open.

Cheap falsifiable consequences of this reading, in order:
1. find the sources of lines 1–3 (2 more quotes → 5 known sources becomes 8);
2. check whether the eight quoted songs' album **initials** / **years** /
   **track numbers** assemble the three Roman numerals (12772 / 5210 / 12061) —
   if they do, the numeral decoding and the pictograms collapse together;
3. check whether the six non-triangle pictograms are the **album covers** or
   **song symbols** of the quoted songs (needs the pictograms named).

---

## 2. CONFIRMED this round

| # | Fact | Evidence |
|---|---|---|
| **R6-C1** | The album order is independently re-verified: track 5 = Ghost March, track 6 = Nocturnal Sugars, track 8 = Daylight Brings, track 13 = Seconds of Dream; 13 tracks, 2021-01-07. | `itunes.apple.com/lookup?id=1548289299&entity=song` re-run here; per-track durations match C2 of round 5. |
| **R6-C2** | Therefore clue 8's example `8 → Ghost March → R` **cannot** mean "the number is the track index" (track 8 is Daylight Brings, whose 8th letter is `t`, not `r`). The round-5 witness-consistent reading is the only simple rule that reproduces both examples. | Direct arithmetic against the re-verified list. |
| **R6-C3** | Clue 2's 10th cell is a capital **`J`**, not `I`. A 10×8 ASCII render of that glyph (`#######`, top bar then a left-curving hook) is `J`; the round-5 OCR read `fIDfeFm` and was wrong. | `tools/clue2_ink.py`, per-cell glyph render of `clues/clue2_scramble.jpg`. |
| **R6-C4** | The 41-cell clue-2 string splits **exactly 15 capitals + 26 non-capitals** (21 lowercase + 5 dashes). 26 = the alphabet; 15 = the answer length. | `[c for c in s if c.isupper()]` / complement, counted here. |
| **R6-C5** | Clue 5's poem is a lyric collage (see §1). | Phrase search; five exact matches from five different artists. |

### New negative on the clue-2 image (ink, not geometry)

Per-character luminance / colour / ink-coverage measured for all 41 cells of the
string line (`tools/clue2_ink.py`). **No cell is drawn in a different shade,
weight or tint** — the only outliers are the five dashes (positions 2, 32, 34,
35, 36), which have ~46–53 ink pixels against 150–270 for letter cells. So the
"answer letters are highlighted" hypothesis is **REFUTED**: the clue gives the
41-cell string in one uniform ink, and the answer must come from the instruction.

---

## 3. New negatives this round

| Family | Space | Result |
|---|---|---|
| **Positional displacement** — each cell gets a displacement (value / ordinal / index / distance-to-dash / dash-count / constant), signed by case, then the string is re-ordered by new position; readings are the capitals, the letter stream, and every 15-letter window | 1,409 distinct 15-char candidates × 2 skies = 2,818 | 0 (`tools/clue2_positional.py`) |
| Stable case-partition (capitals-first / lowercase-first), all circular rotations, all stride permutations mod 41 | included above | 0 |
| Keyboard-scramble: QWERTY↔Dvorak both ways, one-key row shifts, A–Z Caesar shift of the raw string and of the capital string | included above | 0 |

Every one of these is a family the round-2..5 sweeps did **not** cover: those
moved the *letters* (arithmetic on capital values); these move the
*characters*. They also fail, which further narrows clue 2 to a non-positional,
non-keyboard reading.

---

## 4. Tooling delivered

- `tools/clue2_pixels.py` — rotates the clue-2 panel upright, runs tesseract TSV
  on it, and prints the line grouping; confirms the three-line layout.
- `tools/clue2_ink.py` — segments the 41-cell string line into per-cell windows
  and reports mean luminance, RGB, ink coverage and an ASCII glyph render.
  Found R6-C3 and the "no highlight" negative.
- `tools/clue2_positional.py` — the positional / partition / rotation / keyboard
  family above, tested against both pinned skies.

---

## 5. Route tree (round 6, ranked by expected value per hour)

```
META-THEME: the clue poems embed song references (clue 1 Lennon, clue 5 five
prog/metal songs, clue 8 Metallica). Treat "answer = song material" as a
first-class hypothesis across all clues.

SEGMENT 2  chess(12) + wonders(20)          <-- NEW best entry point
├── WONDERS
│   ├── poem = lyric collage (CONFIRMED for lines 4-8) ... NEW
│   │   ├── identify lines 1-3 -> full set of quoted songs (search)
│   │   ├── test 8-song album-initials / years / track numbers against
│   │   │     12772 / 5210 / 12061 (mi/km/mi)
│   │   └── name the six non-triangle pictograms as album/cover symbols
│   ├── (old) pictograms = places -> haversine ......... REFUTED (round 5)
│   └── numerals as (track, letter) pairs, real tracklist ... OPEN
└── CHESS
    ├── 14 pieces -> 12 chars, case preserved
    ├── "a symbol that's flown" = international code of signals ... OPEN
    └── "Order in the court" / "front lines to the throne" = promotion path
        -> OPEN; check the poem lines for lyric sources too (search returned 0)

SEGMENT 4  scramble(15) + sky(17)
├── SKY
│   ├── witness-consistent 71520219618128920 ........... UNCONFIRMED, unique
│   ├── "number = track index" ......................... REFUTED (R6-C2)
│   └── repo reading 58112171456182114 ................. UNCONFIRMED
└── SCRAMBLE  (still the single bottleneck)
    ├── arithmetic / running / linear features .......... REFUTED (879k)
    ├── positional / partition / rotation / keyboard .... REFUTED (new, 1.4k)
    ├── English 15-letter words ......................... REFUTED (8.8k)
    ├── "answer letters highlighted in the image" ....... REFUTED (new, ink)
    └── 15 capitals + 26 non-capitals split ............. NEW STRUCTURE,
            untested as a substitution/alphabet-key reading

SEGMENT 1  imagine(16) + beach(16)
├── beach = 15 measured notes + 1 convention char ....... OPEN (20 s/convention)
└── imagine = the lyric word replaced by 19410712 ....... OPEN
        (NEW: clue 1 is a song rewrite, so read it as a lyric masquerade)

SEGMENT 3  wasd(8) + ship(24)
├── grid: the 8 no-predecessor roots -> 8 chars
│      (4 arrow-roots carry exactly D,W,A,S; 4 numbered stars) ... reading OPEN
└── ship: the Titanic montage described by the author ............ OPEN
```

---

## 6. One-line status

No segment solved. The new structural fact is that **the clue poems are
assembled from song lyrics/song titles** — clue 5's lines 4–8 quote Falkenbach,
Nightwish, Pink Floyd, Coheed and Cambria and Alestorm verbatim — which makes
the "eight wonders" most likely a playlist and points segment 2's `wonders` half
at song material rather than geography. Clue 2 remains the bottleneck for
segment 4 and is now refuted on *positional*, *keyboard*, *arithmetic* and
*image-highlight* readings alike.
