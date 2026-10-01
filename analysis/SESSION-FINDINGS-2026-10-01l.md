# Path to Greatness (3 LTC) — round 20, 2026-10-01

Fourteenth session. A round-20 write-up proposes one specific new clue-7 candidate
(`jbruceismaythomasandrews`) plus three reassessments. The candidate's whole
register is now swept and closes; the clue-2 "markers" idea is built into a real
family and closes; and the recovered clue-7 image has been **re-measured** in a
way no earlier round did, which settles two things and weakens a third. Oracle
`SELFTEST OK`.

New tools: `tools/round20_battery.py`, `tools/clue7_montage_scan.py`.
Round total: **2,579,578 pairs, 0 matches.**

---

## 1. HEADLINE — clue 7's carrier, measured exactly, and no text in it

Rounds 14–19 described the montage in prose (twice, differently) and swept strings
against it. This round asked the plane itself the cheap questions.

### 1a. The encoding is now exact

```text
R = G + d,  d in {-1, 0, +1}   (agreement |R-G| <= 2: 100%)
G == B                          (every pixel)
R LSB plane      ink 0.2502   block-std 0.1969   <- the montage
G LSB plane      ink 0.5015   block-std 0.0319   <- noise
R != G mask      ink 0.5010   block-std 0.0317   <- noise
d counts: -1: 779,763   0: 1,035,124   +1: 258,713
```

So the author took a base image carried in **G (= B)** and perturbed **R by at
most one unit**, forcing R's parity to the payload bit. Consequences:

- **The payload is exactly the red LSB plane**, and nothing else. The obvious
  *second* channel — the sign of the perturbation, `R != G` — is **pure noise**
  (ink 0.501, block-std 0.032). Rounds 14 already argued there was no nested
  layer from a box-blur test; this is an independent confirmation by a different
  method, and it also rules out a sign-channel payload.
- The perturbation is invisible at 8-bit, so the montage exists only in the
  parity plane. X8's reading of stanza 1 is confirmed as the mechanism.

### 1b. The montage is LINE ART, and there is no text in it

- Global ink 0.250 with stroke-like structure: a halftone photograph plane sits
  near 0.50, so the payload is **line art** (drawn strokes), not a dithered photo.
  Ink rows span **y 43..666** of 1080; the content covers the full width.
- **OCR negative.** `tools/clue7_montage_scan.py` runs tesseract 5.5.0 over the
  plane at 1:1, 2x and 4x, both polarities, `--psm 6/7/11`, on the whole plane and
  on the element crops and on 142 candidate text lines. 52 strings of ≥3
  alphanumerics come back; all are line-art noise (e.g. `eowubrspitwiauo`-class
  strings from fragments, never a word). **Nothing is written in the montage.**
- The two portrait regions are **different images**: normalised correlation
  −0.059 (and −0.058 mirrored, +0.054 rotated 180°). They are not a duplicate or
  a mirror of one another.

**What this settles.** The "the answer is the caption/name/plate of the drawing"
branch (round 14 route A3, round 19 §1) is closed **by measurement**, not by
another generated family: there is no caption to find. The 24 characters must be
*derived from what is depicted*, and the depicted thing is line art.

**What it weakens.** `X7b` ("the right-hand portrait has a heavy moustache, so it
reads as Smith, not Andrews") is a judgement about **line-art strokes**, not about
a photograph. That is materially weaker evidence than round 14 presented, and it
matters, because the portrait identity is what every name-family candidate
depends on. Treat Smith-vs-Andrews as **unresolved**, not as "pixels say Smith".

## 2. The `jbruceismaythomasandrews` family — tested, and closed

The write-up's candidate is genuinely new (earlier sweeps used bare surnames and
4-token permutations of `ismay andrews smith titanic`). `round20_battery.py`
sizes and sweeps the whole register:

| family | strings | crossed with | pairs | hits |
|---|---|---|---|---|
| full/initial name forms + glue + ship words, exactly 24 chars | 272 | the 1,290 retained clue-3 readings | 350,880 | **0** |
| full-name *pairs* (incl. `jbruceismaythomasandrews`, `thomasandrewsjbruceismay`, `thomasandrewsedwardsmith`, `edwardsmiththomasandrews`) | 34 | the whole `{w,a,s,d}^8` space | 2,228,224 | **0** |

The write-up asked specifically for `jbruceismaythomasandrews` × all 1,290 —
that is inside the first row, and it is 0. The exactly-24 property is real
(`jbruceismay` 11 + `thomasandrews` 13 = 24) but it is a *length* property, and
both name groups that satisfy it were already swept in round 14; adding the
initialed forms does not help.

## 3. Clue 2: the "capitals are markers" idea, built and swept

The write-up's re-reading is worth taking seriously because the panel supplies
**two independent 41-cell streams** — the ciphertext and the instruction — and the
analysis has only ever used the mixed-case one as an operand stream:

```text
C = s-bcBPEFfJDfeFmksmPOkChDhrgBqjD-i---ffeNB     41 cells: 36 letters + 5 dashes
I = withyourcapitaladditiontothelowersubtract     41 letters
I' = otrleowutbrctsaaacpilthwtidioiatdnhetryuo    41 letters (display order)
```

`I` and `I'` are permutations of the same 41 letters (asserted in the tool); `C`
is *not* the same multiset — the correspondence is positional, cell for cell.
The tool therefore tests:

| family | members | sweep |
|---|---|---|
| capitals (position / value / ordinal / delta / ASCII) indexing C, I, I', the alphabet | 39 | 39 × 2 = 78 pairs |
| every 15-character window of I and I' ("the answer is a phrase", per the independent puzzle's hint) | 54 | 54 × 2 = 108 |
| each capital shifted by its own word-chunk's capital count / lowercase count / length | 156 | 156 × 2 = 312 |
| **distinct** | **237** | **474 pairs, 0 hits** |

One member is amusing but not a result: the alphabet-indexed ordinal family
gives `abcdefghijklmno`. Nothing hits.

## 4. CORRECTION: the independent puzzle is not independent, and has no solution

Rounds 19–20 call the Puzzling StackExchange question an "independent record".
The chronology says otherwise, and I checked the live record:

| fact | value |
|---|---|
| question | **122638**, "An anagrammed logic puzzle!" |
| posted | **2023-10-09** (creation 1696862…) |
| P2G announced | **2021-07-25** — two years **earlier** |
| answers | 1, score 3, **not accepted**; it reconstructs the anagrams and stops |
| comments by the author (`nomad.lw`) | "it's a riddle + logic puzzle, you've figured out a hint already, work on it!"; "**The answer is in the form of a phrase/sentence**" |
| solution | **none posted** (last answer activity 2023-10-11; author's hint 2023-10-19) |

So the SE post **post-dates** the clue it reproduces: it cannot be a source for
the answer, and it contributes exactly one thing — the author's phrase/sentence
hint, which round 6 had already inferred and which §3 above now tests as a
window family (0). This is consistent with round 6's note and does not reopen
clue 2.

## 5. Ledger

| finding | status |
|---|---|
| payload is a ±1 red perturbation of a G(=B) base image | 🟢 **CONFIRMED** (|R−G| ≤ 1 everywhere) |
| R LSB plane is the payload; `R != G` sign channel is noise | 🟢 **CONFIRMED**, no second layer (independent method) |
| montage is line art (~0.25 ink), y 43..666, full width | 🟢 **CONFIRMED** (measurement) |
| no text anywhere in the montage | 🔴 **OCR negative** — 52 candidates, all noise |
| the two portraits are different images | 🟢 **CONFIRMED** (corr ≈ −0.06) |
| clue-7 "caption/nameplate of the drawing" | 🔴 **CLOSED by measurement** (no text exists) |
| `X7b` "pixels say Smith" | ⚠️ **WEAKENED** — the evidence is line-art strokes, not a photo |
| full-name clue-7 register (272 strings × 1,290) | 🔴 0 match, 350,880 pairs |
| full-name pairs × `{w,a,s,d}^8` | 🔴 0 match, 2,228,224 pairs |
| clue-2 marker / window / chunk-shift families | 🔴 0 match, 474 pairs |
| the SE question is an independent source | 🔴 **REFUTED** — it post-dates P2G by 2 years and has no solution |
| segment 3 solved / full puzzle solved | 🔴 no |

## 6. Route tree after round 20

```text
ROUND 20 STATE
  oracle            SELFTEST OK
  clue 7            carrier exact (|R-G|<=1, payload = R parity, no sign channel);
                    montage = line art with NO text; caption branch CLOSED
  clue 2            marker/window/chunk families CLOSED (474 pairs)
  clue 3            closed as a source (round 14)
  clue 5            six-song layer confirmed; pair-metadata model BOUNDED OUT (r19)
  clue 4            untestable alone
  none solved

=== live levers, re-ranked after round 20 ==========================
  L1  IDENTIFY THE DRAWING FROM OUTSIDE THE PUZZLE. It is line art, it has no
      text, and generated descriptions are exhausted (1.61M + 1.07M + 0.35M
      pairs, 0). The only remaining way to name it is to find the published
      source it was traced from -- a Titanic cutaway/side-elevation figure.
  L2  Resolve the portrait identity. It is now clear the image alone cannot
      settle Smith vs Andrews (line art); this needs the 1997 film frames, i.e.
      an external check, and it decides every name-based clue-7 family.
  L3  The six clue-5 pictograms (leads.md §5): still a human-eye job.
  L4  Clue 2: a reading that is not arithmetic, positional, permutational, an
      instruction-word alignment, a marker cross-read, or an instruction window.
      The exact 15-capital / 26-non-capital split is still the only unused
      structure, and the independent puzzle adds only the phrase/sentence hint.
=== do NOT ========================================================
  D1  more generated clue-7 strings        -- 3.0M pairs, 0 (r18-r20)
  D2  captions/nameplates in Ship.png      -- CLOSED, no text exists (§1b)
  D3  clue-5 metadata arithmetic           -- BOUNDED OUT (r19)
  D4  clue-2 arithmetic/alignment variants -- CLOSED (r18-r20)
  D5  the StackExchange puzzle as a source -- it is derivative (§4)
```
