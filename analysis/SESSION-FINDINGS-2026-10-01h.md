# Path to Greatness (3 LTC) — round 13, 2026-10-01

Tenth session. **One confirmation, one refutation, and one correction.**

The headline: `d3w1as24` is a **cleaner** clue-3 encoding than anything before it
— it needs no invented metric — and it reproduces exactly. But it is still
**untestable**, and the two routes proposed alongside it do not survive contact
with the repo's own transcription. New tool: `tools/clue3_root_encoding.py`.
Oracle still `SELFTEST OK`.

---

## 1. CONFIRMED: `d3w1as24` reproduces

The eight cells with no predecessor, read row-major, keeping the WASD letter for
an arrow-root and the number for a star-root:

| cell | value | token |
|---|---|---|
| r1c2 | 5D | D |
| r2c4 | 3★ | 3 |
| r4c9 | 2W | W |
| r5c7 | 1★ | 1 |
| r8c10 | 4A | A |
| r9c1 | 1S | S |
| r9c3 | 2★ | 2 |
| r9c9 | 4★ | 4 |

→ **`d3w1as24`**, exactly 8 characters.

This is a genuine improvement on round 12's `w2s1d5a4`, and the reason is
specific: the nearest-star construction required pairing each star with its
nearest entry cell, an operation **the clue never states**. `d3w1as24` uses only
the eight root cells the graph already proves, in reading order, with the
clue's own WASD alphabet. No invented rule. That is the economy argument, and it
holds.

The same eight cells also give `53214124` (every cell's number, 8 chars).

**Status: derived hypothesis, NOT a solution.** Segment 3's key is
`clue3 (8) ‖ clue7 (24)`, so it cannot be tested until clue 7 exists. Ranking
it first is reasonable; calling it a breakthrough is not.

## 2. REFUTED: the 40,320 interleaving family

Round 13 quoted `4! × 4! × C(8,4) = 70 × 576 = 40,320`. The arithmetic is right,
but the phrasing conflates two different families, and the difference decides
whether a search is worth running:

| family | size |
|---|---|
| both groups in reading order | **70** |
| one group's order free | 1,680 |
| both groups' order free | 40,320 |

40,320 = 8! — eight distinct symbols in arbitrary order. A family that lets
both orders float is not a reading of the grid, it is a permutation search over
the whole string. **70 is the honest grid-faithful family.** Don't spend an hour
on the other 40,250.

## 3. REFUTED: the clue-2 word ↔ chunk assignment

This was promoted as Route B, "the most important unexplored structural
interpretation". It cannot work, for two independent reasons.

**(a) There is almost nothing to solve.** Word lengths are 2,5,8,7,4,8,3,4; chunk
lengths are 2,5,8,7,4,8,3,4 — identical, *including which two words share each
length*. So length alone pins 6 of 8 words. The number of length-compatible
assignments is 2! × 2! = **4**, not a rich constraint-satisfaction problem.

**(b) The permutation is unobservable.** The 15 capitals are read
**positionally** out of one fixed 41-cell string. Chunk labels never enter the
extraction, so relabelling which word owns a chunk cannot move a capital. All
four assignments produce byte-identical output:

```
'' + 'BPE' + 'FJDF' + 'POC' + 'D' + 'BD' + '' + 'NB'  =  BPEFJDFPOCDBDNB
```

So there is no permutation to determine. The only thing that can change the 15
characters is the chunk **boundaries**, not the labels — and both candidate
boundary sets (display order and sentence order) are already recorded in
`analysis/IMAGE-TRANSCRIPTION.md`. Route B is closed.

## 4. CORRECTION: round 13's star prose has two labels swapped

Round 13 wrote "`*1 (r2c4) → 5D`" and "`*3 (r5c7)`". The transcription has
**★3 at r2c4** and **★1 at r5c7**. The nearest-root pairing itself is unaffected
(`*1→2W, *2→1S, *3→5D, *4→4A`) because the numbers were swapped in the prose
while the pairing was not — but the prose should not be trusted over
`tools/wasd_grid.py`.

## 5. The SHIP negatives are real but conditional

Four 24-character descriptions were tested against the segment-3 ciphertext with
the real AES parameters, paired with `d3w1as24`:

| clue-7 candidate | verdict |
|---|---|
| `andrewsandismayviewplans` | NO MATCH |
| `andrewsandismayontitanic` | NO MATCH |
| `andrewsdrawstheshipplans` | NO MATCH |
| `theoceanlinerwillfounder` | NO MATCH |

`theoceanlinerwillfounder` being exactly 24 characters and still failing is a
real result — it kills the most attractive sentence-shaped candidate.

**But read the scope carefully.** These are *joint* refutations. They refute the
**pair**, not `d3w1as24` on its own, and they refute the ship half only *given*
this clue-3 half. Since clue 3 is unconfirmed, the correct ledger entry is
"4 of 4 pairs rejected", not "the ship family is dead". If clue 3 later resolves
differently, these four ship strings are untested again.

## 6. Ledger

| finding | status |
|---|---|
| `d3w1as24` from the 8 root cells | 🟢 CONFIRMED as an encoding; 🟡 as an answer |
| `d3w1as24` beats `w2s1d5a4` on economy | 🟢 CONFIRMED — no invented metric |
| grid-faithful interleaving family = 70 | 🟢 CONFIRMED |
| 40,320 is a grid-faithful family | 🔴 REFUTED — it is 8!, a permutation search |
| clue-2 word↔chunk assignment | 🔴 REFUTED — 4 assignments, output invariant |
| 4 ship descriptions × `d3w1as24` | 🔴 no match (conditional on clue 3) |
| ★1/★3 labels in round 13 prose | 🔴 CORRECTED — ★3 is r2c4, ★1 is r5c7 |
| `d3w1as24` testable now | 🔴 NO — segment 3 needs clue 7 |
| clue 3 solved | 🔴 no |
| full puzzle solved | 🔴 no |

## 7. Where this leaves the puzzle

Unchanged from round 12 in one important respect: **clue 7 is the bottleneck.**
That is now three rounds running, and the reason is structural rather than
incidental — segments 1, 2, 3 and 4 each pair one clue with clue 6, 5, 7 and 8
respectively, but only clue 7 has *no partner already constrained*. Clue 3's
answer is 8 characters and fully determined by a clean encoding; clue 7's is 24
and has nothing. Every other clue has a shorter partner, so their oracle tests
are closer to reachable.

The useful lead from this round is not a candidate, it is the observation that
the *author's* description register for clue 7 is unexplored — five
sentence-shaped strings failed, but they were all `andrewsmay...`/`the...will
founder` shapes. Object-label registers (`titanicplans`, `shipfounder`,
`founderingship`) and their 24-character expansions have not been tested, and
they are a different family, not more of the same.

Next step remains `tools/clue7_candidates.py`, now with the scope discipline
from §5: test the clue-7 half against a *set* of clue-3 candidates, and report
the pairs, so the negatives stay attributable.