# Path to Greatness (3 LTC) — round 12, 2026-10-01

Ninth session. **The clue-3 graph decomposition is real and reproduces exactly —
and the plan built on top of it cannot be executed.** The 92-cycle / 4 entry cells
/ 4 stars split is confirmed from the repo's own transcription, and the
star-nearest pairing is genuinely one-to-one. But the pairing is *not* rare
(~3% of random placements), "cycle order" is *not* well defined (8 candidates,
not 2), and the decisive fact stands: **segment 3's key is clue 3 ‖ clue 7 =
8 + 24 bytes, so no clue-3 candidate can be tested until clue 7 is solved.**

Oracle still `SELFTEST OK`. New tool: `tools/clue3_graph_audit.py`.

---

## 1. What is CONFIRMED (reproducible, `tools/clue3_graph_audit.py`)

From `tools/wasd_grid.py`'s transcription of `clue3_wasd.jpg`, using the
authoritative n-step pointer rule and the repo's WASD mapping (W=up, A=left,
S=down, D=right):

| property | value |
|---|---|
| cells | 100 |
| no successor | 4 — the four numbered stars |
| no predecessor | 8 — the 4 stars + 4 entry cells |
| longest cycle | **92 cells** |
| split | 100 − 92 = 8 = 4 entries + 4 stars, exact |

The four entry cells and their one-step entry into the cycle:

| cell | value | successor | cycle position |
|---|---|---|---|
| r1c2 | 5D | r1c7 | 0 |
| r4c9 | 2W | r2c9 | 3 |
| r8c10 | 4A | r8c6 | 74 |
| r9c1 | 1S | r10c1 | 7 |

The four stars (numbers *not* in reading order, per the transcription): ★1 r5c7,
★2 r9c3, ★3 r2c4, ★4 r9c9.

**The nearest-entry pairing is one-to-one and unique under both metrics** — this
part of round 12 is solid, and it is not a distance artefact:

| star | nearest entry | Manhattan | runner-up | Euclidean | runner-up |
|---|---|---|---|---|---|
| ★1 | 2W | 3 | 6 | 2.24 | 4.24 |
| ★2 | 1S | 2 | 8 | 2.00 | 7.07 |
| ★3 | 5D | 3 | 7 | 2.24 | 5.39 |
| ★4 | 4A | 2 | 5 | 1.41 | 5.00 |

So star order 1,2,3,4 → 2W, 1S, 5D, 4A reproduces, as `w2s1d5a4`.

## 2. What is NOT confirmed

### 2a. The one-to-one pairing is a mild coincidence, not a fingerprint

Round 12 presented the bijection as evidence that the grid is "deliberately
constructed". Over **200,000** random placements of 4 stars and 4 entries on the
10×10 grid:

- nearest-entry assignment is a perfect matching: **6.2%**
- ...and every star's nearest is strictly unique: **3.4%**

~1 in 30 random draws looks like this. The pairing being clean is a pleasant
property of 4 points on a 10×10 grid, not evidence of authorship. It does not
establish that the author intended the stars to index the entry cells.

### 2b. Letter-first vs number-first is unforced

`2W` reads as `w2` or `2w`. Nothing in the clue states the glyph order. The grid
*writes* number-first, so the string as the cells read is **`2w1s5d4a`**, not
`w2s1d5a4`. Both are 8 characters, both fit the length filter, and both are
untested. The letter-first form is chosen for symmetry ("all four WASD
directions, one digit each") — aesthetic, not evidential.

### 2c. "Cycle order" is a family of 8, not a candidate

Nothing on the 92-cycle marks a starting cell. Rotating the cycle so it starts
at each of the four entry cells, and allowing either walk direction, yields
**8 distinct** 8-character candidates:

```
5d2w1s4a   2w1s4a5d   1s4a5d2w   4a5d2w1s     <- forward
4a1s2w5d   1s2w5d4a   2w5d4a1s   5d4a1s2w     <- reversed
```

The round-12 pick `a4d5w2s1` is the forward rotation starting at 4A — one of
eight. Calling it "an alternative ordering that must also be tested" treats it
as a peer of the star reading when it is actually one arbitrary member of a
rotation family that the clue gives no way to pin down. Any of the 8 would have
been equally defensible to write down, and only one was.

## 3. The decisive constraint: neither candidate is testable

This is the point that invalidates the round-12 action plan, and it was stated
in round 12 itself but then not followed through:

```
segment 3  key = clue3 (8) || clue7 (24) = 32 bytes   IV colors_on_leaves
```

`tools/oracle.py` requires **both** halves. There is no per-clue oracle and no
partial-padding filter, because the eight 0x08 padding bytes live in the single
AES block produced by the full 32-byte key. Verified:

```
$ python3 tools/oracle.py --segment 3 w2s1d5a4 <anything>
usage: oracle.py: error: argument --segment: expected 3 arguments
```

So the plan's step ① — "TEST WASD CANDIDATES" before anything else — **cannot be
executed**. Clue 7's 24 characters must exist first. Until then the clue-3
candidate list is an untested hypothesis, and the repo convention is explicit
that an untested list is not a breakthrough: *do not upgrade a hypothesis to a
fact without a run that shows the output*.

This is worth stating plainly because it inverts the priority order. Clue 7 is
the bottleneck, not clue 3, and it was already the case that clue 3 could not be
solved first. Round 12 found an elegant structure and then queued it behind a
step that does not exist.

## 4. Clue 7 is the real target, and the register idea is the one live lead

Given §3, clue 7 deserves the effort. The useful observation in round 12 is not
the candidate list — it is that clue 7 needs **24 characters**, which is a hard
filter that quotation and name families cannot satisfy (they are all far
shorter), and which therefore actively favours a long descriptive phrase. The
poem's own vocabulary is the seed material:

> A red sky at night / Not the least bit significant / A channel for light /
> And a ship so magnificent
>
> The cold, dark night / Moves towards its maker / The vast, frigid ocean /
> The great undertaker

`tools/beach_candidates.py` exists for exactly this shape of job (a length-fixed
descriptive battery against the oracle) and clue 7 has no equivalent yet. That
is the concrete next step, and it is a tool that does not exist.

Note the extraction difficulty is unchanged: 24 characters is ~10^16, so this is
only tractable with a *principled generator*, never a sweep. Any family must be
generated from the poem's own words and the montage's own imagery.

## 5. Clue 5: X2 is now CONFIRMED by pixels

Round 11 closed `clue5_ink.py` as INCONCLUSIVE. `tools/clue5_pennant.py` finishes
the job, and it changes clue 5's status from an eye-read to a measurement.

Method: threshold on **R−G** rather than absolute red (measured floor R−G ≈ 80,
wall ≈ 82, so the split no longer depends on surface brightness), then isolate
**connected components** and take the three largest. That last step is what round
11's approach lacked and what the earlier draft of this tool got wrong: the
pennant is a *bounded object*, and the three survivors are all ~2,000 px with a
~84 × 67 bbox at exactly the three row heights — so they are the pennants, not
scenery. Direction comes from the component's own column-height profile (mast
thick, point tapering).

| row | bbox | outer-fifth mass left / right | margin | point |
|---|---|---|---|---|
| 1 | y 719–785, x 1396–1479, 2012 px | 0.333 / 0.063 | 81% | **RIGHT** |
| 2 | y 861–927, x 1394–1477, 2021 px | 0.059 / 0.338 | 83% | **LEFT** |
| 3 | y 997–1063, x 1391–1475, 2083 px | 0.336 / 0.070 | 79% | **RIGHT** |

**Stable at every threshold from 110 to 150** (identical directions, margins
79–83%); above 150 the components dissolve. So `right / left / right` is a
measurement, not a coin flip, and correction **X2 in `IMAGE-TRANSCRIPTION.md` is
independently CONFIRMED**.

*(A note added in round 13: the committed `tools/clue5_pennant.py` reports this
same result as a normalised per-column ink-height profile rather than an
outer-fifth mass — row 1 `0.03 0.93 0.57 … 0.10 0.03`, row 2
`0.03 0.09 0.18 … 0.88 0.13`, row 3 `0.10 0.91 0.54 … 0.10 0.06`. Two
implementations of the same measurement, same verdict, stable across thresholds
110–150. The transcription now quotes both.)*

This *strengthens* round 11's main negative. With units mi/km/mi, row 1's 12,772
is 539 km past π·R — geometrically impossible. The all-km triple is now
refuted on its own stated terms rather than merely UNPROVEN, and the geography
branch is closed as a solution.

**One limit, stated plainly:** this tool measures *arrow shape*. The step from
"points right" to "means mi" rests on X2's note about which wall carries which
label, which this tool does not re-verify. The arrows are now measured; the
label placement is still a transcription.

### A process note worth recording

The earlier draft of `clue5_pennant.py` printed "row 1 → LEFT, row 2 → LEFT,
row 3 → LEFT" and then printed "rows 1 and 3 point RIGHT". It hardcoded a
conclusion that its own measurements contradicted. Had that output been pasted
into the findings as a confirmation, the repo would have gained a fabricated
CONFIRMED — the exact failure mode `AGENTS.md` warns about. The tool now refuses
to print a conclusion it did not derive, and reports a mixed pattern as
"matches neither X2 nor its mirror" rather than forcing it.

## 6. Clue 5: everything else unchanged

The geography branch is closed as a solution (§5). The six-song layer
(Vintersorg, Falkenbach, Nightwish, Pink Floyd, Coheed, Alestorm) and the track
numbers {1, 3, 4, 9, 10, 11} remain independently sourced. Note the track-number
set was already tested in round 11 and recorded as a coincidence (exactly one
exact hit in ~35 metadata combinations), so it is **not** a new lead despite
being re-proposed this round.

## 7. Round 12 ledger

| finding | status |
|---|---|
| 92-cycle / 4 entries / 4 stars decomposition | 🟢 CONFIRMED, exact |
| each entry enters the cycle in one step | 🟢 CONFIRMED |
| star-nearest pairing is one-to-one and unique | 🟢 CONFIRMED (Manhattan + Euclidean) |
| pairing indicates deliberate construction | 🔴 REFUTED as evidence — ~3.3% by chance |
| pennants point right / left / right | 🟢 **CONFIRMED by pixels**, stable 110–150 |
| correction X2 (units mi/km/mi) | 🟢 CONFIRMED (upgrades round 11 INCONCLUSIVE) |
| all-km geography as clue-5 solution | 🔴 **CLOSED** — 12,772 mi is 539 km past π·R |
| `w2s1d5a4` / `2w1s5d4a` | 🟡 hypothesis, **untestable** |
| `a4d5w2s1` | 🟡 1 of 8 rotation-family members |
| cycle order well defined | 🔴 REFUTED — no start cell, 8 candidates |
| clue 3 testable before clue 7 | 🔴 REFUTED — segment 3 key needs both halves |
| clue 3 solved | 🔴 no |
| full puzzle solved | 🔴 no |

## 8. Next step

Build a clue-7 descriptive battery (`tools/clue7_candidates.py`) against the
24-character length, generated from the poem's vocabulary and the montage's
imagery — because until clue 7 exists, no clue-3 candidate can be refuted or
confirmed, and the oracle's 2^-64 false-positive rate makes the payoff exact
when it lands. Clue 5's geography branch is closed and should not consume more
effort; the live clue-5 thread is the 21 Roman letters against a 20-character
answer.