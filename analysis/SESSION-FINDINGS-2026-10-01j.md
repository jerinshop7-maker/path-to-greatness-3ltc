# Path to Greatness (3 LTC) — round 18, 2026-10-01

Twelfth session. **Every candidate the round-15..17 write-ups propose was run
against the real oracle: 1,069,392 pairs, zero matches.** The load-bearing new
result is a *derivation audit*: the write-ups' clue-2 strings are largely not
reproducible from the rule they describe, so they cannot be regenerated or
extended. Oracle `SELFTEST OK`.

New tool: `tools/round18_battery.py`. Restored: `tools/segsweep.py` (see §5).

---

## 1. The round-15..17 proposals, and what each run covered

The repo's own record ends at round 14 (`SESSION-FINDINGS-2026-10-01i.md`).
Rounds 15..17 arrived from outside it. Each sweep below goes through
`tools/segsweep.py`, which normalises both halves exactly as the author's
`fix_clues.script` does, drops wrong-length candidates **and reports how many**,
plants a witness, and refuses to report a verdict if the witness is not
re-found. No candidate was dropped on length this round.

| family | clue-3 side | clue-7 side | pairs | hits |
|---|---|---|---|---|
| side-elevation register | 1,290 retained readings | 13 exact-24 strings | 16,770 | 0 |
| side-elevation × `{w,a,s,d}^8` | 65,536 | same 13 | 851,968 | 0 |
| founder/fall register | 1,290 retained readings | 3 exact-24 strings | 3,870 | 0 |
| founder/fall × `{w,a,s,d}^8` | 65,536 | same 3 | 196,608 | 0 |
| chess × Roman deletions | 4 piece orderings | 14 deletion strings + 1 | 60 | 0 |
| clue-2 family × sky | 58 clue-2 readings | 2 sky candidates | 116 | 0 |
| **total** | | | **1,069,392** | **0** |

Read §3 of round 14 again before quoting the clue-3 column: the 1,290 retained
readings are the union of families A–F, and a 0-hit run refutes the *pairs*, not
either half.

## 2. The clue-2 derivation audit (the real new result)

Rounds 15–17 hand the repo two families and five "concrete outputs". None of the
outputs may be taken on trust, so both families were **re-derived from the
displayed anagram words** in `tools/round18_battery.py` and compared.

Ciphertext (authoritative, `IMAGE-TRANSCRIPTION.md`):
`s-bcBPEFfJDfeFmksmPOkChDhrgBqjD-i---ffeNB`, 41 cells, 15 capitals
`BPEFJDFPOCDBDNB` at 1-based cells 5,6,7,8,10,11,14,19,20,22,24,28,31,40,41.
Its eight length-compatible chunks are `s-` `bcBPE` `FfJDfeFm` `ksmPOkC` `hDhr`
`gBqjD-i-` `--f` `feNB` (lengths 2,5,8,7,4,8,3,4), and the eight anagram words
`TO LOWER SUBTRACT CAPITAL WITH ADDITION THE YOUR` fit them by length.

### 2a. The instruction-word family IS reproducible — once the conversion is fixed

The reading is: each word is the per-capital shift key, aligned positionally
across its chunk; `LOWER`/`SUBTRACT` subtract, `CAPITAL`/`ADDITION`/`WITH`/`YOUR`
add; one output letter per capital cell. The write-up's first output

```
ekmmhjcyiolfxit
```

matches this rule in **14 of 15 characters**. The re-derived member is

```
ekmmhjcyiomfxit          (SUBTRACT,ADDITION)|(WITH,YOUR)|positional|A=1
```

differing only at position 11 (`m` vs `l`, the cell-24 capital `D` in chunk
`hDhr`/`WITH`). A deliberate search over all 32 enumerated members of the family
(4 assignments × positional/compact alignment × WITH-YOUR add/neutral × A=1/A=0
× chunk-rule/cell-rule) puts the nearest member at **1** character for
`ekmmhjcyiolfxit`, but at **3, 12 and 13** characters for the other three
strings (`ekmmhjcyiodfxnb`, `dnbyiofxekmmhjc`, `lityiofxekmmhjc`). So:

> One write-up string is the described rule with a single slip. The other three
> are not in the family the write-up says produced them, and are not reachable
> by any of its enumerated conventions. The write-up gives no derivation, so
> they cannot be extended into a family — only tested as given, which is what
> §1 does (all 0).

### 2b. The running-sum string IS reproducible

Round 17's literal reading — scan left to right, uppercase adds its alphabet
value, lowercase subtracts, dash does nothing, one output per capital — yields

```
dtyeimhtiawruik          running|A=1|no-reset|emit-after|map to 1..26
```

exactly, once the total is converted back to a letter 1-based. The earlier 0-based
conversion of the same rule gives a different string, which is why this is worth
stating: the write-up's string pins the conversion, and the rule is then real.
It was tested against both sky candidates: 0.

## 3. The sky half is still a candidate, not a fact

Rounds 15–17 describe `71520219618128920` as "CONFIRMED" and "the only variant
that hits the 17-character length". The repo's position is unchanged and should
hold until segment 4 passes:

```text
clue 8 mechanism (dash: position->track; letter: value wrapped 1..13 -> track;
                  cell position -> letter index)    CONFIRMED
71520219618128920                                  UNCONFIRMED, 0/116 this round
```

Two things the write-ups get right and that this round re-checked: the mechanism
reproduces both author examples, and the deleted-Roman candidate they pick
(`xmmdcclxxivccxxmmlxi`) is genuinely inside the 20-character Roman family
(§1). What the write-ups call "the 92-cycle spells a perfect WASD string" is
round 12/14's finding that the 92-cycle string **is** the arrow content read in
walk order — it is not an independent discovery, and round 14 proved the digits
carry nothing extra (§2 of `...01i.md`).

## 4. The one round-17 observation that stands up

`colors_on_leaves` is the segment-3 IV and **is** the only one of the four that
is not a track title on *Seconds of Dream* (the others are track 1
`few_n_far_btween`, track 6 `nocturnal_sugars`, track 13 `seconds_of_dream` —
verified directly in `oracle.SEGMENTS`). So the anomaly is real:

```text
IV anomaly (colors_on_leaves is not an album track)   CONFIRMED
IV -> "leaves fall" -> "will founder" inference       UNCONFIRMED
its three exact-24 candidates                         REFUTED as pairs (3,870)
```

## 5. Repo repair: `tools/segsweep.py` was missing

`tools/clue3_ship_cross.py`, `tools/clue7_ship_family.py` and
`tools/clue7_desc_sweep.py` all `from segsweep import sweep`, but the module was
a round-14 working file that never got committed, so those three tools could not
run from a clean checkout. It is restored here with the two properties round 14
requires of a sweeper: normalisation + **reported** length drops, and a planted
witness per call. The 1,290 retained readings above are reproduced through
`clue3_ship_cross` families A–F (`A=4, B=70, C=15, D=82, E=1120, F=2`), which
confirms the restored driver agrees with the round-14 union.

## 6. Ledger

| finding | status |
|---|---|
| side-elevation register, 13 strings × 1,290 retained readings | 🔴 0 match, 16,770 pairs |
| side-elevation register × `{w,a,s,d}^8` | 🔴 0 match, 851,968 pairs |
| founder/fall register, 3 strings × 1,290 retained readings | 🔴 0 match, 3,870 pairs |
| founder/fall register × `{w,a,s,d}^8` | 🔴 0 match, 196,608 pairs |
| chess orderings × full Roman single-deletion family (14 distinct) + `chartingeightwonders` | 🔴 0 match, 60 pairs |
| clue-2 instruction-word family (re-derived, 32 members) + running-sum (20) + write-up verbatim (7) × both skies | 🔴 0 match, 116 pairs |
| `ekmmhjcyiolfxit` | 🟢 reproducible to 14/15 under the described rule (1 slip) |
| `lityiofxekmmhjc`, `dnbyiofxekmmhjc`, `ekmmhjcyiodfxnb` | ⚠️ **not reproducible** from any enumerated convention (nearest 3–13 chars) |
| `dtyeimhtiawruik` | 🟢 reproducible (rule as stated, 1-based conversion) — still 0/2 |
| `withyourcapital`, `capitaladdition` | 🔴 0 match (independently re-run here) |
| clue 8 mechanism | 🟢 CONFIRMED (unchanged) |
| `71520219618128920` | 🟡 UNCONFIRMED (unchanged) |
| `colors_on_leaves` is not an album track | 🟢 CONFIRMED |
| `tools/segsweep.py` restored | 🟢 CONFIRMED |
| segment 3 solved | 🔴 no |
| full puzzle solved | 🔴 no |

## 7. Route tree after round 18

```text
ROUND 18 STATE
  oracle            SELFTEST OK
  clue 3            CLOSED as a source (round 14); +1,069,216 pairs this round
  clue 7            side-elevation and founder/fall registers REFUTED as pairs
  clue 2            write-up family cannot be regenerated; running-sum real, 0/2
  clue 4            piece-orderings x Roman deletion, 0
  clue 5            Roman 21->20 deletion family, 0
  none solved

=== A. clue 7 — the only live lever ================================
  A1  The picture, not the naming. Round 14 measured a heavy moustache on the
      right-hand portrait and round 15's external cross-check disagrees; the 24
      length coincidences straddle the same split. This is still unresolved and
      still decides the register.
  A2  A published caption/figure number for the middle cutaway (round-14 A3)
      remains untried with a real catalogue in hand.
=== B. clue 2 =====================================================
  B1  Any new reading must be stated as a generating rule, not a string list:
      this round shows strings without derivations cannot be extended.
  B2  The 15-capital / 26-non-capital split is still the only exact structure.
=== C. clue 4 / clue 5 ============================================
  C1  "A symbol that's flown" -> International Code of Signals is untouched.
  C2  The six pictograms still need a human eye (leads.md §5).
=== D. Do NOT spend time here =====================================
  D1  more side-elevation / founder-fall spellings   -- REFUTED, §1
  D2  more clue-3 mutations                          -- CLOSED, round 14
  D3  clue-5 all-km geography                        -- REFUTED, rounds 11-12
```
