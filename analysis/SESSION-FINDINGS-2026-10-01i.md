# Path to Greatness (3 LTC) — round 14, 2026-10-01

Eleventh session. **Clue 7's carrier was retrieved and read for the first time,
which retires the repo's biggest gap and corrects a description that three
rounds of candidates were built on. 1.61 million segment-3 key pairs swept, zero
matches. Clue 3 is now provably a closed source. Clue 4's SAN-mate reading is
refuted.** Oracle still `SELFTEST OK`.

New tools: `tools/clue7_ship_extract.py`, `tools/clue7_ship_family.py`,
`tools/clue7_desc_sweep.py`, `tools/clue7_family_size.py`, `tools/clue4_san.py`,
`tools/sfengine.py`, `tools/clue3_closure.py`, `tools/clue3_ship_cross.py`.

---

## 1. REFUTED as a discovery: "the numbers are step sizes"

Round 14 opened by reporting that the repository "incorrectly assumed the
numbers in the 10x10 grid were just labels for adjacent cells. They are STEP
SIZES." **That is not a correction.** `tools/wasd_grid.py` has read the digit as
a multiplier since it was written; `succ()` computes

```python
r, c = r + dr * n, c + dc * n      # n IS the step size
```

and round 12's 92 + 4 + 4 = 100 decomposition was itself derived under that rule.
The premise of the "massive structural breakthrough the previous analyst missed"
is false.

## 2. CONFIRMED, and this is the load-bearing new fact: the digits are REDUNDANT

The converse of §1 is new, checkable, and stronger than anything in the
breakthrough write-up (`tools/clue3_closure.py` part 1). For **all 96 arrow
cells** the printed digit is *forced* by the cell's position, its arrow, and the
cell that arrow lands on — **zero exceptions**.

> The digits carry no information the arrows have not already stated. No
> extraction that reads the digits can recover anything the pointer graph does
> not already give.

So round 13's economy argument for `d3w1as24` is not merely convenient, it is
**forced** — and the round-14 programme of mining the digits cannot pay off,
because there is nothing in them.

## 3. CONFIRMED (round 12, reproduced), with one correction

`tools/clue3_closure.py` part 2 rebuilds the 92-cycle and its string exactly,
and the four entries land on cycle indices **6, 9, 13, 80** as claimed.

**Correction.** Round 14 lists the sources as `5, 2, 1, 4` and reads the entry
letters as `sada`. Row-major source order is `5, 2, 4, 1`, and the letters at the
four entry indices spell **`saad`** — r8c10 = 4A enters at index 80 → `a`,
r9c1 = 1S enters at index 13 → `d`. These are round 12 findings, not round 14.

## 4. REFUTED: all four proposed routes

`tools/clue3_ship_cross.py`, real AES parameters, witnesses re-found 3/3 on every
run.

| family | distinct 8-char clue-3 readings | pairs | match |
|---|---|---|---|
| A root readings (`d3w1as24` et al.) | 4 | 24 | 0 |
| B route 1 — sources × stars, all 70 slot choices | 70 | 420 | 0 |
| C route 2 — source directions/values | 15 | 90 | 0 |
| D route 3 — all 85 windows of the 92-cycle | 82 | 492 | 0 |
| E route 4 — all permutations of `ddsaaadw` | 1,120 | 6,720 | 0 |
| F coordinate index, 3 orders | 2 | 12 | 0 |
| **total** | **1,290 distinct** | **7,758** | **0** |

Both proposed `ship` strings are exactly 24 characters and were genuinely
tested: `ismayandrewsanddeckplans`, `andrewsandismaydeckplans`.

## 5. BREAKTHROUGH: clue 7's carrier recovered, and its montage corrected

`analysis/IMAGE-TRANSCRIPTION.md` §8 said the PNG "was not retrieved in this
session". It is now. `clues/qr2.jpg` decodes (OpenCV `QRCodeDetector`) to
`https://tinyurl.com/y28knqz3`, which resolves to a public Google Drive file
`1jzxIFQGmTnR3EB42bd-DPEJfe655XbhG`. Fetched and saved as **`clues/Ship.png`**,
2,896,530 bytes, 1920×1080 RGBA, alpha uniformly 255, **G and B identical**, so
the payload is confined to the red channel.

`tools/clue7_ship_extract.py` reproduces all of this.

### 5a. The poem, now first-hand, replacing the §8 placeholder

```
A red sky at night
Not the least bit significant
A channel for light
And a ship so magnificent

The cold, dark night
Moves towards its maker
The vast, frigid ocean
The great undertaker
```

Stanza 1 is the **extraction instruction**, and it is exactly what the round-14
recommendation ("the hidden picture in the red low bit plane") already assumed
without the clue having been read. Confirmed numerically — the eight red bit
planes have set fractions 0.250 / 0.498 / 0.501 / 0.511 / 0.422 / 0.614 / 0.651 /
0.792, and only plane 0 is both a low plane and structured:

| plane | mean | verdict |
|---|---|---|
| **0** | **0.250** | **the montage** |
| 1 | 0.498 | noise (verified visually: pure static) |
| 2 | 0.501 | noise |
| 3 | 0.511 | noise |
| 4–7 | 0.422–0.792 | ordinary image content |

There is **no second layer**: no pixel of plane 0 carries a further LSB after
removing a local box blur, so the montage is not itself a nested container.

### 5b. CORRECTION: the montage is not "Ismay and Andrews and deck plans"

On the recovered plane the middle element is **a ship's line drawing** — a hull
seen from the bow quarter with rows of deck openings, the foremast and its
standing rigging above. Not a photograph, and not a floor plan.

The right-hand portrait carries a **heavy drooping moustache**, which matches
Bernard Hill's Captain Edward Smith, not Victor Garber's Thomas Andrews. Rounds
13 and 14 both assert "Andrews on the right"; the recovered pixels contradict
that. Left-hand portrait is a narrower face with a high brow.

So **three rounds of candidates were aimed at a picture nobody had looked at.**
That, not the candidate strings, is why they all failed.

## 6. NEW NEGATIVES on segment 3, 1.61 M pairs, zero matches

All sweeps use the real AES-256-CBC parameters and re-find three planted
witnesses.

| sweep | clue-3 readings | clue-7 strings | pairs | match |
|---|---|---|---|---|
| round-14 routes × hand-picked ship (§4) | 1,290 | 6 | 7,758 | 0 |
| name families (§7) | 4 | 312 | 1,360 | 0 |
| bounded description family (§8) | 4 | 399,986 | 1,599,944 | 0 |
| **total** | | | **1,609,062** | **0** |

Read the scope as round 13 insisted: these are **joint** refutations. They refute
the *pairs*. They do not refute `d3w1as24` on its own, and they do not refute
the ship half given a clue-3 half outside these families.

## 7. The 24-character length does real work — and two groups hit it exactly

Clue 7 needs exactly 24 characters. Two name groups sum to exactly 24:

| group | sum |
|---|---|
| `ismay`(5) + `andrews`(7) + `smith`(5) + `titanic`(7) | **24** |
| `jonathan`(8) + `hyde`(4) + `victor`(6) + `garber`(6) | **24** |

So each admits all 4! = 24 orderings *automatically at the right length*. All 48
were swept (§6, `tools/clue7_ship_family.py`), plus 288 two-names-plus-a-boat
strings and 4 prose strings — 312 in total, zero matches.

Note the second group: `bernard`(7) + `hill`(4) + `victor`(6) + `garber`(6) = 23.
The **24** coincidence therefore fits the Hyde/Garber pair, i.e. it is weak
evidence *against* the moustached right-hand portrait being Smith. Worth keeping
as a live tension, not a conclusion.

## 8. NEW METHOD CORRECTION: `sweep` on generated lists is a trap

Round 14 recommends "run `oracle.py --stdin-segment 3` with a generated list".
Two things about that are wrong, and both cost real time here.

**(a) The generator overflows.** `tools/clue7_family_size.py` measures it with a
hard cap:

| max words | strings of exactly 24 chars |
|---|---|
| 2 | 8 |
| 3 | 16,581 |
| 4 | 400,010 (cap hit) |
| 5 | 400,009 (cap hit) |

Growth is by concatenation, so it does not converge. **Three shell processes were
killed by memory** during this session while generating it. Measure the family
before sweeping it.

**(b) Wrong-length candidates are dropped silently.** The first draft of this
round's hand-picked `ship` list was 19 strings of which **13 were not 24
characters** (`andrewssirjohnishmay` = 20, `sirjohnandrewsandismay` = 22, …).
`segsweep.sweep` discards them, so the run reported a clean negative while
testing 6 of 19. `tools/clue7_desc_sweep.py` therefore prints the drop count and
sweeps in 20,000-pair chunks so peak memory is flat.

## 9. NEW: clue 4 is not a mating line

Clue 4 is the **only** answer that keeps its case, and 12 characters *with
uppercase* plus a chess position looks like a mate-in-N in SAN. That had never
been run against an engine. `tools/clue4_san.py` + `tools/sfengine.py`, Stockfish
17 with NNUE, 1 thread.

Position rebuilt from `IMAGE-TRANSCRIPTION.md` §4:
`4r3/rkp1p3/1p1p1np1/6N1/3B4/1QP5/2K5/8 w - - 0 1` — valid, 14 pieces, matching
the transcription square for square.

| check | result |
|---|---|
| evaluation at 3 s / 8 s | `+98` / `+57` cp, no mate score |
| white first moves searched | 33 |
| forced mate at 2 s/move | **none** |

**The 12-character case-preserved answer is not a white mating line.** This does
not refute chess notation generally — a 12-character SAN *line* need not mate —
but the strongest form of the hypothesis is dead.

Two engine lessons recorded in `sfengine.py`: stockfish emits `info string` lines
for NNUE loading that carry neither score nor pv, so the last `info` line is not
the deepest search; and sending `quit` immediately after `go` truncates a depth-22
search to depth 1, which silently turns a mate search into a null result. Both
produced a false "no mate" before being fixed.

## 10. Ledger

| finding | status |
|---|---|
| "digits are step sizes" corrects the repo | 🔴 **REFUTED** — `wasd_grid.py` always did this |
| digits redundant with (position, arrow, successor) | 🟢 **CONFIRMED**, 96/96, new |
| 92-cycle, entry indices 6 / 9 / 13 / 80 | 🟢 CONFIRMED (round 12, reproduced) |
| entry letters spell `sada` | 🔴 **CORRECTED** → `saad` |
| route 1 / 2 / 3 / 4 | 🔴 no match, 7,758 pairs |
| `clues/Ship.png` retrieved | 🟢 **CONFIRMED**, 2,896,530 bytes, 1920×1080 |
| clue 7's poem transcribed first-hand | 🟢 **CONFIRMED**, replaces the §8 placeholder |
| red LSB plane 0 is the montage | 🟢 CONFIRMED — 0.250 ink, planes 1–3 pure noise |
| no second / nested layer in the montage | 🔴 no nested LSB found |
| montage middle is "deck plans" | 🔴 **CORRECTED** — a ship's line drawing |
| montage right-hand man is Andrews (Garber) | ⚠️ **CONTRADICTED** — heavy moustache, reads as Smith (Hill) |
| 312 name-family ship strings | 🔴 no match |
| 399,986-string description family | 🔴 no match, 1,599,944 pairs |
| **segment-3 total this round** | 🔴 **1,609,062 pairs, 0 matches** |
| clue 4 answer is a white mating line | 🔴 **REFUTED** — 33 first moves, no forced mate |
| clue 3 solved | 🔴 no |
| full puzzle solved | 🔴 no |

## 11. Why clue 3 is now closed, not merely hard

`d3w1as24` remains the best clue-3 reading and §2 strengthens it. But the reason
it cannot be improved is structural:

- the **digits** are redundant — nothing to mine (§2);
- the **arrows** are fully consumed by the 92-cycle string, and all 85 windows
  plus all 1,120 coordinate-letter permutations fail (§4);
- the **four star labels** are the only unconstrained data in the grid, and all
  70 + 15 arrangements of them against the sources fail (§4).

The clue-3 grid is a **closed source**. Further grid readings cannot produce a
testable pair; only new information about clue 7 can move segment 3. That is now
a proof-shaped statement, not a guess about search effort.

## 12. Route tree after round 14

```
ROUND 14 STATE
  oracle            SELFTEST OK
  clue 3            CLOSED (digits redundant; 1,290 readings all swept)
  clue 7            carrier RECOVERED, poem read, montage corrected; 1.61M pairs, 0
  clue 4            SAN-mate reading refuted
  clue 5            mi/km/mi confirmed by pixels; 6 pictograms unnamed
  segment 3         key = clue3(8) + clue7(24); clue 3 side exhausted
  none solved

=== A. clue 7 — now that the file is in hand ===========================
  A1  Fix the identification of the two faces. The right-hand one has a heavy
      moustache; the 24-length coincidence prefers Hyde+Garber. Resolve this
      with the actual 1997 stills, not from memory. Everything downstream is
      a naming family, so this is the one fact that matters.
  A2  Ask whether the answer is NAMES at all. 1.61M pairs say no sentence.
      The untried register is what the author would TYPE to point at the
      picture, e.g. the deck-plan *drawing* as a caption.
  A3  The middle drawing may be a real published Titanic cutaway. If so, its
      caption or figure number is a 24-character candidate no one has tried.

=== B. clue 4, narrowed ===============================================
  B1  12-character SAN LINES that do not mate. clue4_san.py gives the position.
  B2  "Order in the court / From the front lines to the throne" points at a
      CHECK, not a mate. Enumerate check-giving 12-character lines.
  B3  "From a symbol that's flown" (leads.md §5) is untouched: international
      code of signals, one letter per flag, 14 pieces on the board, 12 wanted.

=== C. clue 5 =========================================================
  C1  The six non-triangle pictograms still need a human eye. No sweep
      replaces recognition.
  C2  mi/km/mi is CONFIRMED by pixels. Stop re-litigating all-km.

=== D. Do NOT spend time here =========================================
  D1  more clue-3 grid readings       -- CLOSED, §11
  D2  clue-2 word/chunk assignment    -- REFUTED round 13, output invariant
  D3  40,320 interleavings            -- REFUTED round 13, it is 8!
  D4  clue-5 all-km geography         -- REFUTED rounds 11-12
  D5  unsized generated description families -- measure first, §8
```