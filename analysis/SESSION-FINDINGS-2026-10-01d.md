# Path to Greatness (3 LTC) — round 9, 2026-10-01

Sixth session. A pasted round-9 analysis proposed clue 2 as an *expression*
(dashes as operators, capitals/lowercase as paired operands) — the one clue-2
reading cell-by-cell sweeps miss. It is now tested and refuted, and several
factual errors in the pasted text are corrected. New tool:
`tools/clue2_expression.py`. Oracle: `SELFTEST OK`.

---

## 1. Clue 2 — dashes-as-operators / capital–lowercase pairing: REFUTED (new family)

The exact structure is confirmed: the 5 dashes sit at 1-based positions
2, 32, 34, 35, 36 and split the string into six groups

```
g0 's'   g1 'bcBPEFfJDfeFmksmPOkChDhrgBqjD'   g2 'i'   g3 ''   g4 ''   g5 'ffeNB'
```

The pasted hypothesis: capitals are outputs, lowercase are operands, dashes are
operators/groups. `tools/clue2_expression.py` sweeps it:

| sub-family | what it does | space |
|---|---|---|
| dash-group features | each capital keyed by its group index/length/counts/balances, lowercase-sum before/after **within its group**, distance to nearest dash, dash counts | 20 features × 4 ops × 26 shifts × 2 bases |
| capital↔lowercase pairing | each capital paired with one lowercase operand (nearest before/after, group first/last/sum/min/max, overall first/last/sum) then combined | 10 operands × 4 ops × 26 shifts × 2 bases |
| dash-as-subtract | segment distance to the nearest dash as the operator amount | 2 features × 2 ops × 26 × 2 |

```
distinct 15-char candidates: 1976  ×  2 pinned skies  =  3952 pairs  ->  0 hits
```

So the dash/pairing reading is closed too. Clue 2 is now refuted on **every**
family proposed to date: per-cell arithmetic, running/linear arithmetic,
positional displacement, rotation/stride, keyboard substitution, anagram
permutation, ordering key, image highlight, the 26-non-capital alphabet key, and
now dash-group/pairing expression. The bottleneck is a reading none of these
touches.

---

## 2. Corrections to the pasted round-9 text

| Pasted claim | Verdict |
|---|---|
| "title lengths are 16, 7, 15, 9, 11, 14" | **Wrong.** Spaces removed: `astralandarcane`=**15**, `havamal`=7, `ghostlovescore`=**14**, `highhopes`=9, `threeevils`=**10**, `treasureisland`=14. |
| "the image has nine pictogram positions, not six — the 6↔6 model is incomplete" | **Not a correction.** The repo already recorded that the triangle glyph is *one drawing reused three times* (rotated), i.e. 9 drawn glyphs = 3 triangle instances + **6** non-triangle pictograms. The 6-count is the repo's, already accounting for the nine positions. |
| "12,772 miles cannot be an ordinary great-circle distance" | **Correct, and already recorded** (round 8: row 1 = 20,554 km vs the 20,015 km maximum). |
| "line 2 upgraded to confirmed" | Already round 7. |
| "clue 2 dashes are the cleanest unexplored feature" | Tested and refuted here (§1). |
| Roman numerals `XMMDCCLXXII / VCCX / XMMLXI`, counts 11+4+6=21 | Consistent with `IMAGE-TRANSCRIPTION` (11+4+6=21) and the values 12,772 / 5,210 / 12,061. |

---

## 3. The one clue-5 route still untried: *Archaic Reveries* as "the eight wonders"

Both round-7 and round-9 converge on the same top clue-5 experiment, and it is
the only clue-5 route not yet attempted:

- the author uses his **own** first album, *Seconds of Dream* (13 tracks), as
  clue 8's dictionary;
- the author's **second** album, *Archaic Reveries* (2018), has **exactly eight**
  tracks — a literal match for `Charting the eight wonders`;
- one of them is titled **"Seven Miles"**, on a clue whose panels carry `mi`/`km`
  and three distance-like numerals.

This is the reading I would attack first on clue 5. **Caveat, stated plainly:**
clue 5 is **not oracle-testable** — segment 2 needs the 12-char chess answer as
well — so any result here is structural, not a 64-bit break.

---

## 4. Route tree (round 9)

```
SEGMENT 4  scramble(15) + sky(17)     <-- ONLY oracle-testable break
├── SKY   71520219618128920 (best) / 58112171456182114 (repo)
└── SCRAMBLE  ~800k+ hypotheses, 0
    ├── arithmetic / running / linear .................. REFUTED
    ├── positional / rotation / stride ................. REFUTED
    ├── keyboard ....................................... REFUTED
    ├── anagram permutation / ordering key ............. REFUTED
    ├── image highlight ................................ REFUTED
    ├── 26-non-capital alphabet key .................... REFUTED (r8)
    └── dash-group / capital-lowercase pairing ......... REFUTED (r9, 3,952)

SEGMENT 2  chess(12) + wonders(20)     <-- NOT testable alone
├── WONDERS
│   ├── six lyric sources ............................. CONFIRMED
│   ├── "eight wonders" → Archaic Reveries (8 tracks) .. NEXT (author-controlled)
│   ├── geography / landmark distances ................ DEAD (unit impossible, r8)
│   ├── numerals as (track,letter) into a real tracklist ... OPEN
│   └── pictograms ↔ songs ............................ unverified
└── CHESS  flags / promotion / "symbol that's flown" ... OPEN

SEGMENT 3  wasd(8) + ship(24)
├── 53214124 / 2415+1234 ............................. OPEN
└── ship (Titanic montage) ........................... OPEN

SEGMENT 1  imagine(16) + beach(16)
├── beach = 15 notes + 1 convention .................. OPEN
└── imagine = lyric masquerade ....................... OPEN
```

---

## 5. One-line status

The pasted clue-2 expression route (dash groups + capital/lowercase pairing) is
refuted (3,952 pairs, 0), completing the closure of every proposed clue-2 family;
the pasted fact-list also carries three errors (title lengths, the "nine
pictograms" non-correction, and it repeats round 8's unit result). Clue 5's one
untried, author-controlled route — *Archaic Reveries*' eight tracks as "the eight
wonders" — is the next test, while segment 4 (clue 2) stays the only place a
64-bit break can land.
