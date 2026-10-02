# Path to Greatness (3 LTC) — round 21, 2026-10-01

Fifteenth session. **The headline is a correction, and it invalidates the method
rounds 14–20 used to read clue 7's hidden image.**

The red-parity plane of `clues/Ship.png` was never "line art". It is a
**dithered photograph**, and one line of code — block-averaging — makes it
legible. Every conclusion drawn from looking at it at 1:1 is therefore suspect,
and two are demonstrably wrong: the *element order is reversed* from what round
20 recorded, and the "no text / caption branch closed by measurement" negative
was reached by a method that could not have detected text even if it were there.

Oracle `SELFTEST OK`. New tools: `tools/clue7_montage_recover.py`,
`tools/seg3_cross.c`, `tools/seg3_witnesses.py`, `tools/seg3_crosscheck.py`,
`tools/clue7_solo_sweep.py`.

---

## 1. CORRECTION, and it is the important one: the payload is a DITHER

Rounds 14–20 measured `ink ≈ 0.25` in the red parity plane, concluded from that
that the payload was **line art**, ran OCR on it at 1:1 / 2x / 4x, got nothing,
and closed clue 7's "caption / nameplate" branch *by measurement*.

None of that follows. A one-bit-per-pixel reduction of a photograph is a
dither. It is not legible at 1:1 — which is exactly why every direct view looked
like static — but it is trivially legible once averaged, because the mean of the
parity bits over an n×n block *is* the source's local luminance.

`tools/clue7_montage_recover.py` measures the distinction rather than arguing
it, against synthetic controls:

| statistic | this payload | synthetic line art | synthetic dither |
|---|---|---|---|
| mean run of ones, horizontal | **1.71** | 2.48 | 1.80 |
| mean run of zeros | 5.12 | 21.26 | 2.23 |
| uniform 8×8 blocks | **0.1165** | 0.3303 | 0.0000 |
| uniform 16×16 blocks | **0.0792** | — | — |
| block-mean mass in middle bins (n=8) | **0.789** | — | — |

A dither has no long runs and almost no uniform blocks, because every pixel is
an independent coin flip whose probability is set by local brightness. Line art
is the opposite: long empty runs (21.26 here), many uniform blocks. The payload
matches the dither on every statistic.

**The recovery is one line:**

```python
bm = (parity & 1).reshape(h//8, 8, w//8, 8).mean(axis=(1, 3))
```

At n = 8 the montage is plainly readable. At n = 4 more detail returns.

## 2. The recovered montage, and it inverts round 20's X7b

Rendered montage: **two male portraits flanking a ship's bow and foremast**, in a
continuous-tone photograph.

| position | what is actually there |
|---|---|
| **left** | male portrait, **heavy drooping moustache**, receding hair |
| centre | the ship's bow and foremast with standing rigging |
| **right** | male portrait, clean-shaven, heavy jaw, looking down |

**CORRECTION to X7b.** Round 20 recorded "the right-hand portrait carries a
heavy drooping moustache, which matches Bernard Hill's Captain Edward Smith,
not Victor Garber's Thomas Andrews", and `IMAGE-TRANSCRIPTION.md` §8 carries the
same claim. In the recovered montage the heavy moustache is on the **LEFT**
portrait. The right portrait is clean-shaven.

How that happened is worth recording as a general hazard: at 1:1 the plane is
noise, and a face read out of noise can be mistaken for its neighbour or its
mirror. Round 20 itself flagged X7b as "a judgement about line-art strokes, not
about a photograph" and downgraded it — the right instinct, the wrong reason.

I checked orientation rather than assuming it: the poem is legible and
unmirrored in the G channel at the top right, so the plane is not flipped and the
portraits were not swapped by a display artefact.

**What this does to the identity question.** The left portrait's heavy drooping
moustache reads as Bernard Hill's Captain Edward Smith. The right, clean-shaven
portrait is *not* Smith. Round 14's "Andrews on the right" is also unsupported.
So **neither round 14 nor round 20 named the two men correctly**, and the
actor-pair family that the 24-character length seems to favour
(`jonathan`(8)+`hyde`(4)+`victor`(6)+`garber`(6) = 24) rests on an
identification the image does not support. It is still exactly 24 characters,
which is a real coincidence, but it is now a coincidence about a *guess*.

This does **not** revive the name families. It only removes the last
pixel-based support for them.

## 3. The G channel has never been rendered, and it is a clean Titanic photograph

Round 20 established that `R = G + d` with `d ∈ {-1,0,+1}` and `G == B`
everywhere. I re-verified both: d counts −1 → 779,763, 0 → 1,035,124,
+1 → 258,713, and `G == B` on 100% of pixels. But that analysis only ever
produced *statistics*. Rendering the channel as a picture gives the obvious
thing nobody had looked at: **the visible image is a clean black-and-white
photograph of RMS Titanic under full sail, bow to the right**, with the clue-7
poem typeset at the top right.

Two consequences:

1. Stanza 1 — "a red sky at night / not the least bit significant / a channel
   for light" — describes exactly this construction, and is confirmed as the
   *mechanism*.
2. **The payload is a different photograph from the base image.** Block-mean
   correlation between the parity plane and G is **+0.0925 / +0.1020 / +0.1084**
   (n = 4 / 8 / 16) — essentially zero, either polarity. So the red-LSB picture
   is not a dither of the Titanic photograph; it is its own image.

That is why the montage was never legible in the first place, and it means the
author's construction is: *carry the real ship photograph in G and B where it is
plainly visible, and hide a different picture in red's parity bit*. The clue is
a ship in both layers.

## 4. Round 20's "no text in the montage" — the conclusion survives, the argument does not

OCR of the **recovered** montage (three scales, both polarities, psm 6/11/12)
returns fragments like `'2eamesiatreRE'`, `'RaBianWoteegps3oeOSRRRSeeNata'`,
`'Sears'`, `'Baty'`. None is a word. The negative conclusion holds.

But it is a much weaker negative than round 20 claimed. Round 20 ran OCR on the
raw 1-bit plane, where a 4-pixel-tall glyph is destroyed by dither noise, and
attributed the failure to "no text exists". The correct statement is: *the
recovered montage contains no legible text*. A caption too degraded to survive
1-bit dithering cannot be excluded by any amount of OCR at any resolution,
because the information is gone — but that is a different claim, and a narrower
one.

The "caption branch is closed" conclusion therefore **stands**, for a reason
that should be restated: a 24-character caption could never have been legible
through a 1-bit channel, so it was never recoverable from the payload, and the
visible layer carries no caption either.

## 5. A new capability: testing clue 7 ALONE

Clue 3 is closed as a source (`tools/clue3_closure.py`: digits redundant on
96/96 arrow cells, the 92-cycle hides no message, every step-size-consistent
extraction enumerated). So pairing a clue-7 candidate with a clue-3 reading is a
guess about a closed source — which is why 3.0M pairs across rounds 18–20
produced nothing attributable.

There is also a sharper problem, which I think is the real reason those rounds
could never have worked. Earlier runs swept `{w,a,s,d}^8` (65,536) and `{0-9}^8`
(10⁸). **Neither can contain a mixed answer**, and all 1,290 retained clue-3
readings are mixed — each needs letters and digits, including `d3w1as24`. Every
clue-7 negative in rounds 14–20 was computed against a clue-3 space that could
not have held the best candidates.

`tools/seg3_cross.c alpha` sweeps the full `wasd0123456789^8` = **1,475,789,056**
per clue-7 candidate. A string that fails is refuted **unconditionally**.

**Engine, and why it is built this way.** The C file contains decryption only.
An earlier version also carried a forward cipher to plant witnesses in-process;
its decrypt matched pycryptodome while its encrypt did not, so the forward
cipher was **removed rather than trusted**, and witness generation moved to
`tools/seg3_witnesses.py` (pycryptodome).

`seg3_cross.c selftest` re-derives the S-box from its own definition —
multiplicative inverse in GF(2⁸) plus the affine map — and requires all 256 bytes
to match, plus an independent `ISBOX ∘ SBOX = id` check. That check caught two
transcription errors in my own first draft of the tables, and then caught a
second bug of its own: the derivation left `inv_tbl[0]` uninitialised and read it
back, so the selftest failed on roughly one run in four with identical output
either way. Fixed by zeroing the table; 20 consecutive clean runs since. That
bug was in the *verification* code, not the search, and
`tools/seg3_crosscheck.py` — which compares against pycryptodome and is
deterministic — passed throughout, before and after. It is recorded here because
a flaky self-test is exactly the kind of thing that should invalidate
conclusions, and the right response is to find and fix it rather than to keep
running sweeps and hope.

`tools/seg3_crosscheck.py` is the validation that matters for a search engine:
it takes 3,504 keys — the repo's structural clue-3 readings crossed with its
clue-7 candidates, plus a uniform spread over all 14 alphabet characters — and
requires the C engine's full 16-byte plaintext to equal pycryptodome's on every
one. **0 disagreements.** A zero-hit result only means something if the engine
would have found a real answer, and this is the test that establishes it.

Rate: measured ~2.4M keys/s/core, so ~10 minutes per clue-7 candidate.

**The list is 7 strings, deliberately.** An unconditional negative costs ~10
minutes, so this buys a complete sweep of the clue-3 side for a few *considered*
readings — not breadth over generated families. `tools/clue7_solo_sweep.py`
holds the list and reports each result with its own scope.

### The full first pass: 10,330,523,392 keys, 0 matches, 7/7 certified

| clue-7 candidate | register | keys swept | result | wall time |
|---|---|---|---|---|
| `victorgarberjonathanhyde` | actor pair | 1,475,789,056 | **no match** | 6.7 min |
| `jonathanhydevictorgarber` | actor pair, other order | 1,475,789,056 | **no match** | 7.6 min |
| `edwardsmiththomasandrews` | character pair | 1,475,789,056 | **no match** | 10.1 min |
| `thomasandrewsedwardsmith` | character pair, other order | 1,475,789,056 | **no match** | 10.3 min |
| `smithandrewsdeckplanlast` | deck plans | 1,475,789,056 | **no match** | 10.3 min |
| `thenightmovestomakerofit` | stanza-2 fate | 1,475,789,056 | **no match** | 10.2 min |
| `thecoldnightmovestomaker` | stanza-2 fate | 1,475,789,056 | **no match** | 10.2 min |

**7 of 7 runs re-found their planted witness before reporting.** Measured rate
~2.4M keys/s/core, so ~10 minutes per candidate rather than the 19 I estimated —
which makes this cheaper than expected and therefore worth repeating on the next
considered readings.

This is the first batch of clue-7 negatives in the repository that are
**unconditional**. None of them depends on a clue-3 reading being right.

What it does *not* do is narrow the search space of clue 7 in any useful way: it
removes four registers (all of them name-based, plus two fate phrasings) and
leaves the answer unidentified. But it removes them *properly*, which the 3.0M
pairs of rounds 18–20 did not.

## 6. Ledger

| finding | status |
|---|---|
| red-parity payload is a **dither**, not line art | 🟢 **CONFIRMED** by measurement against synthetic controls |
| montage recovered legibly by block-averaging | 🟢 **CONFIRMED** — one line of numpy |
| montage = two male portraits + a ship's bow, continuous-tone | 🟢 **CONFIRMED** (now actually visible) |
| **X7b has the portraits reversed** | 🔴 **CORRECTED** — heavy moustache on the **LEFT**; right is clean-shaven |
| round 14's "Andrews on the right" | 🔴 **NOT SUPPORTED** by the image |
| neither prior round named the two men correctly | 🟢 **CONFIRMED** — the identity is fully open |
| `jonathanhyde`+`victorgarber` = 24 chars | 🟡 a real length coincidence about an unsupported identification |
| G (= B) channel is a clean RMS Titanic photograph | 🟢 **CONFIRMED** — never rendered before this round |
| payload is a *different* photograph from the G base image | 🟢 **CONFIRMED** — block-mean corr ≈ +0.09/+0.10/+0.11 |
| poem is legible, unmirrored, in G at top right | 🟢 **CONFIRMED** (orientation check) |
| "no text in the montage" | 🟡 **survives, weakened** — reached by a method that could not have found text |
| "caption branch closed by measurement" | 🟡 stands, but the reason must be restated (§4) |
| pre-round-21 clue-3 spaces cannot hold a mixed answer | 🟢 **CONFIRMED** — `{w,a,s,d}^8 ∪ {0-9}^8` excludes every retained reading |
| C engine == pycryptodome on 3,504 real keys | 🟢 **CONFIRMED**, 0 disagreements |
| C engine selftest (S-box re-derivation, 256/256) | 🟢 **CONFIRMED** — and it caught an uninitialised `inv_tbl[0]` in its own derivation that made it fail ~1 run in 4; fixed, 20/20 clean |
| 7 clue-7 candidates (actor pairs, character pairs, deck plans, stanza-2 fate) | 🔴 **REFUTED unconditionally** — 10,330,523,392 keys, 0 matches, 7/7 witness-certified |
| segment 3 solved / full puzzle solved | 🔴 no |

## 7. Where this leaves the puzzle

The bottleneck has moved, and the move is the useful part.

Rounds 18–20 closed clue 7 by generating 3.0M strings against 1,290 clue-3
readings. That was the wrong axis twice over: the clue-3 readings are guesses
about a **closed** source, and they were swept against a space that **cannot
contain** the mixed answers the grid best supports.

What is now available is a complete sweep of the clue-3 side. That converts clue
7 from untestable into testable-at-least-alone, at 19 minutes per candidate.

```text
ROUND 21 STATE
  oracle              SELFTEST OK
  clue 3              closed as a source; but now ENUMERABLE in full
  clue 7 carrier      exact (|R-G| <= 1, payload = red parity)
  clue 7 payload      recovered: two portraits + a bow, a dithered photo
  clue 7 identity     OPEN, and both prior readings were wrong
  new engine          clue-7-alone sweep, 1.48e9 clue-3 answers per candidate,
                      cross-validated against pycryptodome

=== live levers ======================================================
  L1  The solo sweep is now ~10 min per candidate, so the bottleneck is
      *choosing* candidates, not sweeping them. The next pass should spend
      its effort on naming registers that survive the recovered montage,
      not on more generated strings.
  L2  Identify the two men from the RECOVERED montage. This is now a
      normal image-identification job on a legible photograph, not a
      judgement about line-art strokes -- and it is external, so it needs
      the 1997 film frames. Every name family depends on it.
  L3  The G channel is a clean Titanic photograph. Whether the author
      intended anything to be read off the VISIBLE layer has never been
      asked; stanza 1 points at red, but nothing excludes the visible
      image being part of the answer.
  L4  clue 5's six pictograms: still a human-eye job.
=== do NOT ==========================================================
  D1  more generated clue-7 strings vs 1290 clue-3 readings -- 3.0M
      pairs, 0, and the readings come from a closed source
  D2  OCR of the raw parity plane -- it cannot resolve dithered glyphs
  D3  clue-5 metadata arithmetic -- bounded out (r19)
  D4  clue-2 arithmetic/alignment variants -- closed (r18-r20)
```