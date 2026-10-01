# Path to Greatness (3 LTC) — round 19, 2026-10-01

Thirteenth session. A round-19 write-up from outside the repo proposes three
routes. Two are testable here and both close; the third is a naming family whose
two obvious sub-registers round 18 already swept. **The useful new result is a
proof-shaped bound:** under the write-up's own "pair of songs" model, no
non-geographic feature can reach rows 1 or 3 at all. Oracle `SELFTEST OK`.

New tool: `tools/round19_battery.py`.

---

## 1. What the write-up proposes, and what it is worth

| its route | status after this round |
|---|---|
| Clue 5 = six rebus icons → six confirmed songs → three directed *pair* relationships → extraction | 🔴 the pair model is **bounded below two of its three targets** (§2) |
| Clue 5 = the 21 Roman letters vs the 20-character answer is intentional | 🟡 already tested: round 18 swept all 14 distinct single deletions × 4 chess orderings, 60 pairs, 0. Re-proposal, not a new route |
| Clue 2 = the eight anagram words are character-aligned operands | 🔴 widened family tested: 138 pairs, 0 (§3) |
| Clue 7 = the answer is the caption/name of the recovered drawing | 🟡 round 18 already swept the side-elevation/bulkheads and founder/fall registers (1,069,216 pairs, 0). Whatever is left here must be a *found* caption, not a generated one |
| Clue 4 = flags + court/order/"front lines to the throne" | 🟡 untested, but segment 2 is `chess ‖ wonders`, so it cannot be tested alone |
| Clue 1 = `19410712` twice + `536531#276755365` fails the oracle | 🟢 correct, and already in the ledger (round 5 / `tested.md`) |

Two of the write-up's own claims are right and already recorded: the six quoted
lines sit at poem lines 2,4,5,6,7,8 with lines 1 and 3 the author's instruction;
and the artist-origin geography supplies no candidate for rows 1 or 3 (round 8).

## 2. Clue 5: the pair model is bounded, not merely unswept

The write-up asks that the numbers not be restricted to geography and lists
candidate features: artist-origin distance, release-date difference, track-number
arithmetic, duration difference, lyric-length difference, title-length
arithmetic, ASCII distance. `tools/round19_battery.py` does two things.

### 2a. Reachability: a feature that cannot reach the target is refuted for every pair

The three targets are **12,772 / 5,210 / 12,061**. The features the write-up
names are all bounded by facts already fixed in this repo:

| feature | maximum reachable | why |
|---|---|---|
| release-date gap, in days | **8,782** | the extreme release years in the set are 1994 and 2017 (1994-01-01 → 2017-12-31), whatever the exact days |
| song duration, in seconds | < 1,200 (one song), < 3,600 (all six) | the longest quoted song is Ghost Love Score, ≈10 minutes |
| album-year difference | 23 | years are fixed metadata |
| track number | ≤ 13 | the albums hold at most 13 tracks |
| title length, in letters | ≤ 40 one title, ≤ 80 two | the longest title here is 21 letters with its parenthetical |

**So under the write-up's own pair model, rows 1 and 3 cannot be any
non-geographic pairwise feature.** Only two things can reach ≥ 12,000:

- a **surface distance in km** between two places (≤ π·R = 20,015 km) — and the
  only such pairs are artist origins, which round 8 tested and which supply
  **no** candidate anywhere near rows 1 or 3; and
- a **six-way sum** over the whole set — which is not a pair, and which is the
  round-11 coincidence (`Σyears` 12,023 + `Σtracks` 38 = 12,061).

That is a bound, not a sweep: it closes the "two songs, one metadata number"
reading of rows 1 and 3 for every feature in the write-up's list, and for
anything else of that kind the write-up must name a new feature.

### 2b. Exhaustive search over every feature the repo can measure

643 distinct feature values were formed from the six songs — per-feature
pairwise differences, sums and (for length-like features) products, plus
six-way sums — and compared against the targets.

| tolerance | hits |
|---|---|
| ±0 | **1** — `Σyears + Σtracks = 12,061` = row 3 |
| ±1 | 1 |
| ±9 | 1 |
| ±35 | 2 — the above, plus `Σyears + Σtitle-lengths = 12,092` (Δ31) |

Both hits are **six-way sums**, i.e. the same class as the coincidence round 11
already recorded and dismissed. There is **no pairwise hit at any tolerance**,
which is exactly what §2a predicts. Row 2 (5,210) remains the only target any
pair feature could reach, and round 8 found only a ~9 km near-miss for it.

**Verdict:** the six-rebus-icon → six-song observation is real and stays as a
*structural* lead (C5.2, and `IMAGE-TRANSCRIPTION.md` §5 for the drawings), but
its intended payoff — three directed pairs measured by the three numerals — is
now refuted for rows 1 and 3 and unsupported for row 2.

## 3. Clue 2: the widened character-aligned family is closed

Round 18 re-derived the narrow instruction-word family (alphabet-rank shift,
A=0/A=1) and got 32 members. The write-up asks for a wider net: alphabetic rank,
ASCII difference, ASCII sum, position within the instruction word, position
within the chunk, and dashes as null/skip.

`round19_battery.py` enumerates: the 4 length-compatible word assignments ×
key alignment (positional / compact) × key source (`word` A=0, `word` ASCII,
position-in-word, position-in-chunk, first ciphertext char of the chunk) ×
operation (+/−) × output conversion (mod-26 letter / printable ASCII), read out
at the 15 capital positions.

```
74 distinct 15-character candidates
69 after normalisation (5 dropped on length: the ASCII-output variants can
   contain a space, which fix_clues.script removes)
69 x 2 skies = 138 pairs   ->   0 hits   (witness re-found)
```

So the write-up's own family produces nothing, and the earlier narrow version
produced nothing. Clue 2's remaining hope is a reading that is neither
arithmetic, nor positional, nor a permutation, nor this alignment.

## 4. Corrections to the round-19 write-up

| its claim | verdict |
|---|---|
| the 21-vs-20 Roman mismatch is a new clue | 🟡 true as a *fact* (X3), but already tested: round 18 swept all single deletions (14 distinct) × 4 chess orderings, 0 |
| the six icons → six songs mapping is "strong" | 🟡 it is a **plausible rebus inference**, not confirmed; the repo's own tentative pairing had sprig and mask as guesses, and the icon→song order is what the numerals would have to select |
| "the six source lines occur at 2,4,5,6,7,8 … missing 1 and 3" | 🟢 correct and already recorded (C5.3) |
| "band-origin distance is dead" | 🟢 correct (round 8), but note it is dead *by measurement*, while §2a above kills the wider pair model *by bound* |
| "the repository's answer register for clue 7 must become a caption" | 🟡 partly done: round 18 swept the drawing-description registers. A caption can only be tested if the actual drawing is **identified** — that is the open step, not another generated phrase |

## 5. Ledger

| finding | status |
|---|---|
| pair model: no non-geographic pair feature can reach rows 1 or 3 | 🟢 **PROVEN**, bound (max 8,782 days / <3,600 s / ≤13 / ≤80) — closes the write-up's list |
| 643 measured features vs the three targets | 🔴 1 exact hit, and it is the six-way `Σyears+Σtracks = 12,061` recorded in round 11 as a coincidence; 0 pairwise hits |
| clue-2 widened aligned-word family × both skies | 🔴 0 match, 138 pairs (5 candidates dropped on length and reported) |
| clue-5 six icons → six songs | 🟡 structural lead, unverified pairing (unchanged) |
| clue-5 Roman 21→20 | 🔴 already tested round 18, 0 |
| clue-7 caption route | 🟡 needs the actual drawing identified |
| clue-4 flags | 🟡 untestable alone (segment 2 needs both halves) |
| segment 3 solved / full puzzle solved | 🔴 no |

## 6. Route tree after round 19

```text
ROUND 19 STATE
  oracle            SELFTEST OK
  clue 5            six-song layer CONFIRMED; pair-metadata model BOUNDED OUT
  clue 2            widened aligned-word family closed (138 pairs, 0)
  clue 7            generated caption registers closed (round 18); needs the
                    real drawing identified
  clue 3            closed as a source (round 14)
  clue 4            untestable alone
  none solved

=== live levers, in order ==========================================
  L1  Identify the middle drawing in Ship.png (round-14 A3, still open).
      Everything clue-7 can be is downstream of knowing what that drawing is.
  L2  Resolve the portrait split (round 18 §7): the pixel reading says Smith;
      the 24-length coincidence says Hyde+Garber. Still unresolved.
  L3  Name the six clue-5 pictograms (leads.md §5) -- a human eye, not a sweep.
  L4  Clue 2: a reading that is neither arithmetic, positional, permutational,
      nor an instruction-word alignment. The 15/26 split is the only exact
      structure left.
=== do NOT ========================================================
  D1  more clue-5 metadata arithmetic      -- BOUNDED OUT, §2
  D2  more clue-2 aligned-word variants     -- CLOSED, §3
  D3  more clue-3 grid readings             -- CLOSED, round 14
  D4  more clue-7 generated captions        -- CLOSED, round 18
```
