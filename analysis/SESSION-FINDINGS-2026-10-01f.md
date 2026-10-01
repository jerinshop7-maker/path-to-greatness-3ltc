# Path to Greatness (3 LTC) — round 11, 2026-10-01

Eighth session. **Headline: round 10's headline is downgraded.** The all-km
great-circle fit is real arithmetic but it is *post-hoc, unit-inconsistent, and
structurally unsupported by the pictograms*; it is **UNPROVEN**, not the "best
clue-5 result to date". The independent pixel re-check of the pennants that
round 6 asked for was run and is **inconclusive** (the parquet floor is itself
deep red). New tools: `tools/clue5_geo_audit.py`, `tools/clue5_ink.py`.
Oracle still `SELFTEST OK`. Clue 5 cannot be oracle-tested (segment 2 needs
clue 4 as well), so every clue-5 verdict here is structural.

---

## 1. The audit (`tools/clue5_geo_audit.py`)

### 1a. The triple re-derives exactly (round 10 reproduces)

| row | printed | pair | great-circle | error |
|---|---|---|---|---|
| 1 | 12,772 | Great Wall ↔ Chichén Itzá | 12,738.1 | −33.9 km (0.27%) |
| 2 | 5,210 | Angkor Wat ↔ Uluru | 5,219.1 | +9.1 km (0.18%) |
| 3 | 12,061 | Machu Picchu ↔ Giza | 12,037.5 | −23.5 km (0.20%) |

### 1b. Uniqueness inside the canonical eight: this part is good

Within the 28 canonical-eight pair distances, each of rows 1 and 3 is matched by
**exactly one** pair, at every tolerance tried (±0.5%, ±1%, ±2%):

```
row1 -> Great Wall <-> Chichen Itza         (the only pair)
row3 -> Machu Picchu <-> Great Pyramid      (the only pair)
row2 -> NONE
```

So the two hits are not one-of-many inside that pool. That is the strongest
thing said for the reading, and it is worth keeping.

### 1c. But the unit reading is the fatal problem

Correction **X2** (the authoritative eye-read) measures the pennants
**right / left / right** = `mi / km / mi`. Under that reading:

```
row1  12,772 mi = 20,554.5 km   IMPOSSIBLE  (pi*R = 20,015.1 km)
row2   5,210 km =  5,210.0 km   possible
row3  12,061 mi = 19,410.3 km   possible
```

Row 1 is **539 km past the Earth's maximum surface distance**. Round 10 resolves
this by switching to all-km — but all-km is precisely what X2's measured
pennants **contradict**. So the fit is only internally consistent if the pennant
reading is wrong, and the pennant reading is the one piece of evidence measured
from the image. The two halves of the clue-5 story cannot both hold as written.

### 1d. Row 2 is post-hoc

5,210 km lies **outside** the canonical-eight range for that target: the nearest
canonical distances bracket it at 4,559 and 6,073 km, with nothing close. Row 2
exists only after widening to a freely chosen site pool (the round-10 pool adds
20 sites, 190 more pairs). A hit found after widening the search space is not
evidence of the same kind as a hit inside a fixed pool.

### 1e. Null model

Monte-Carlo over 20,000 random 8-site sets, tolerance ±35 km (round 10's error):

```
P(some pair within +/-35 km)   row1 0.128   row2 0.104   row3 0.138
joint (row1 AND row3)          ~ 0.018
```

So a single arbitrary target is matched ~13% of the time by a random site set,
and the joint rows-1-and-3 coincidence is ~1.8% **before** the garden-of-forking-
paths corrections (the unit reading was chosen after the fact, and row 2 required
a widened pool). Round 10's p ≈ 0.02–0.03 was, if anything, slightly generous.

### 1f. The pictograms do not depict the sites

Round 10 itself concedes the eye-read pictograms — headstone+heart, flowering
sprig, anchor, horned beast head, horned mask, star-?-star — "do not obviously
depict Great Wall / Chichén / Angkor / Uluru / Machu / Giza". A geographic
reading has to explain *why the six drawings are six landmarks*; it cannot, so
the fit floats free of the only visual layer the clue actually supplies.

**Verdict:** the arithmetic is exact, but the claim rests on a unit reading the
image contradicts, a post-hoc row, and a pictogram layer that does not support
it. Status **UNPROVEN** (round-8's "geography DEAD" and round-10's "PROMISING"
reconcile to this).

---

## 2. The pennant re-check (`tools/clue5_ink.py`) — INCONCLUSIVE

Round 6 asked for a fresh pixel measurement of the pennants because the unit
reading controls every number downstream. It was run:

```
red-crayon mask (R>205 & G<145 & B<145): 100,834 px (2.74% of frame)
artwork region (x 1050-1500, y 660-1140): 32,333 px
largest connected component: 23,439 px
right-floor pixels inside the mask: 4.3%
```

The clue-5 scene is a rendered stone corridor whose **parquet floor is itself
deep red**, inside the same colour range as the red crayon. The floor therefore
merges with the drawings, component segmentation returns floor tiles as single
giant blobs, and the pennants cannot be separated from the tiles. No colour
transform tried here fixes it. This is recorded as an **inconclusive negative**:
X2's eye-read remains the *only* pennant measurement, so the `mi / km / mi`
reading stands by default, and the conflict in §1c is unresolved by pixels.

---

## 3. Two cheap coincidences, tested and dismissed

| Curiosity | Test | Result |
|---|---|---|
| "row-1 pair lengths 9 + 11 = **20** = the answer length" | name lengths of all canonical-eight pairs summing to 20 | **4** of 28 pairs sum to 20 (P≈0.14) — a coincidence, **not** a lead |
| The six quoted songs' album years sum to 12,023; plus their track numbers (Σ=38) = **12,061** = row 3 | 5 base sums (years/tracks/artists/song-lens/album-lens) and all 1–3 fold sums vs the three numerals | exactly **one** exact hit in ~35 combinations — **coincidence**, recorded so it is not re-swept |

Neither is evidence. Both are in the ledger so the next agent does not re-derive
them.

---

## 4. Route tree (round 11)

```
SEGMENT 4  scramble(15) + sky(17)     <-- ONLY oracle-testable break
├── SKY   71520219618128920 / 58112171456182114
└── SCRAMBLE  every proposed family REFUTED (r6-r9); non-arithmetic reading OPEN

SEGMENT 2  chess(12) + wonders(20)    <-- NOT testable alone
├── WONDERS
│   ├── six lyric sources ............................. CONFIRMED
│   ├── geography (round 10) ..... UNPROVEN (r11 audit: unit conflict, post-hoc row 2)
│   ├── pennant/unit question ........................ INCONCLUSIVE by pixels (r11)
│   ├── "eight wonders" -> Archaic Reveries (8 tracks)  OPEN (author-controlled)
│   ├── pictogram <-> six songs ...................... OPEN (needs eyes; music layer)
│   └── numerals -> 20 chars ......................... mechanism unknown
└── CHESS  flags / promotion .......................... OPEN

SEGMENT 3  wasd(8) + ship(24) ....................... OPEN
SEGMENT 1  imagine(16) + beach(16) .................. OPEN
```

## 5. One-line status

Round 10's geography fit is downgraded to UNPROVEN by its own contradictions —
all-km is required by the numbers but contradicted by the measured pennants, row 2
is post-hoc, and the pictograms do not depict the sites; the pixel re-check of
the pennants is inconclusive because the corridor floor is deep red, so X2 stands.
Clue 5 remains untestable and segment 4 (clue 2) is still the only place a 64-bit
break can land.
