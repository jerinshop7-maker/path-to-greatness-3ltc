# Tested (full negatives ledger)

The summary table in the folder's `README.md` shows the highlights; this file is the
complete record. One row per run, in the order tested. Nothing is removed; a hypothesis
retested with a different method gets a new row.

Two things make these negatives cheap and exact.

- Each of the four segments is one AES-256-CBC block holding 8 useful bytes, so its
  plaintext must end with a PKCS7 padding of eight `0x08` bytes. A wrong key passes with
  probability 2^-64. A pair of clue answers is therefore refuted knowing nothing about the
  other six.
- Every answer has a length imposed by the author's own scheme, so a candidate of the wrong
  length is dropped before any AES call. That filter is free and it is what makes some
  families collapse without a run at all.

Two rates are used below. The CPU harness measured 294,000 segment tests per second per
core, about 4,200,000 per second over 22 cores. The GPU engine is a CUDA AES-256-CBC padding
oracle taking a left half and a right half and forming the key as their concatenation; it
peaks near 3,000,000,000 keys per second and the per-run rate in the table is the observed
end-to-end rate, generation of the candidate lists included.

Witness protocol on every GPU run: three synthetic pairs are planted in the candidate
streams, at head, middle and tail, each one encrypted beforehand under the same scheme and
fed through the normal code path. A run counts only if all three are re-found and the engine
reports the space as exhausted. Every reported hit is re-derived on CPU by `tools/oracle.py`
before it would be believed.

## Runs on the GPU engine, 2026-09-09

Totals: 37 runs, 5,690,021,893,966 ordered pairs, 0 match, 4.12 hours elapsed on one
RTX 5080, witnesses 3 of 3 on every run.

| Hypothesis | Space (N) | Method | Result | Witness | Rate | Date |
|---|---|---|---|---|---|---|
| Segment 3: `ship` is one of 12 strong strings taken from the film scene (`isamathematicalcertainty`, `jonathanhydevictorgarber` and 10 others), `wasd` is any 8-digit string | 12 x 100,000,000 = 1,200,000,000 | GPU padding oracle | 0 match | yes: 3 of 3 | 1.18 G/s, 1.0 s | 2026-09-09 |
| Segment 3: `ship` is a name or role of at most 4 tokens, `wasd` is one of 1,134 structural readings of the grid | 839,858 x 1,134 = 952,398,972 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.73 G/s, 1.3 s | 2026-09-09 |
| Segment 3: `ship` is a word window of the IMSDb screenplay, Wikiquote, Wikipedia or the site poems, `wasd` structural | 72,865 x 1,134 = 82,628,910 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.65 G/s, 0.1 s | 2026-09-09 |
| Segment 3: `ship` is any 24-character window of the film transcript, all positions, `wasd` structural | 54,998 x 1,134 = 62,367,732 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.63 G/s, 0.1 s | 2026-09-09 |
| Segment 3: `ship` is a name or role of at most 4 tokens, `wasd` is any of the 65,536 strings over `{w,a,s,d}` | 839,858 x 65,536 = 55,040,933,888 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.76 G/s, 72.0 s | 2026-09-09 |
| Segment 3: `ship` is one of 625 deck names of the ship, `wasd` is any 8-digit string | 625 x 100,000,000 = 62,500,000,000 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.56 G/s, 112.2 s | 2026-09-09 |
| Segment 3: `ship` is a concatenation of 5 deck names, `wasd` structural | 3,173,842 x 1,134 = 3,599,136,828 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.75 G/s, 4.8 s | 2026-09-09 |
| Segment 3: `ship` comes from the stanza 2 riddle, at most 4 tokens, `wasd` structural | 3,209,764 x 1,134 = 3,639,872,376 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.74 G/s, 4.9 s | 2026-09-09 |
| Segment 3: same stanza 2 family, `wasd` over `{w,a,s,d}^8` | 3,209,764 x 65,536 = 210,355,093,504 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.77 G/s, 274.5 s | 2026-09-09 |
| Segment 4: `scramble` from 5 mechanical readings of the 41-character string, `sky` from 4 families | 198,508 x 741 = 147,094,428 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.08 G/s, 1.8 s | 2026-09-09 |
| Segment 1: `imagine` is an 8-digit block written twice, `beach` from the earlier candidate lists | 100,000,000 x 2,479 = 247,900,000,000 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.37 G/s, 665.6 s | 2026-09-09 |
| Segment 3: `ship` is a 24-character window starting on a word, over the whole film transcript, `wasd` is any 8-digit string | 14,706 x 100,000,000 = 1,470,600,000,000 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.67 G/s, 2,190.0 s | 2026-09-09 |
| Segment 1: `imagine` is two December 7 or 8 dates, years 1800 to 2100, in 4 formats, `beach` from the earlier lists | 5,796,056 x 2,479 = 14,368,422,824 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.39 G/s, 36.4 s | 2026-09-09 |
| Segment 1: `imagine` is one date written in two different formats, years 1 to 2100, `beach` from the earlier lists | 7,124,619 x 2,479 = 17,661,930,501 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.38 G/s, 47.0 s | 2026-09-09 |
| Segment 4: `scramble` 5 families, `sky` with its capitals pinned by the certified rule | 198,508 x 3,599,533 = 714,536,096,764 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.59 G/s, 1,217.7 s | 2026-09-09 |
| Segment 1: two December dates, `beach` from the YouTube melody, first reading (389 variants) | 5,796,056 x 389 = 2,254,665,784 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.21 G/s, 10.5 s | 2026-09-09 |
| Segment 1: one date in two formats, `beach` from the YouTube melody, first reading | 7,124,619 x 389 = 2,771,476,791 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.18 G/s, 15.3 s | 2026-09-09 |
| Segment 1: 8-digit block twice, `beach` from the YouTube melody, first reading | 100,000,000 x 389 = 38,900,000,000 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.56 G/s, 69.3 s | 2026-09-09 |
| Segment 1: `imagine` is `19410712` followed by any 8 digits, `beach` from the lists plus the melody | 100,000,000 x 2,868 = 286,800,000,000 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.55 G/s, 519.3 s | 2026-09-09 |
| Segment 1: one date in two formats, `beach` from the melody, second reading (1,177 variants) | 7,124,619 x 1,177 = 8,385,676,563 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.29 G/s, 28.6 s | 2026-09-09 |
| Segment 1: two December dates, `beach` melody second reading | 5,796,056 x 1,177 = 6,821,957,912 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.32 G/s, 21.4 s | 2026-09-09 |
| Segment 1: 8-digit block twice, `beach` melody second reading | 100,000,000 x 1,177 = 117,700,000,000 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.37 G/s, 315.4 s | 2026-09-09 |
| Segment 1: `imagine` is any 8 digits followed by `19410712`, `beach` from the lists plus the melody | 100,000,000 x 2,868 = 286,800,000,000 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.42 G/s, 680.9 s | 2026-09-09 |
| Segment 1: `imagine` is a number or a word spelled out, twice, `beach` from the lists plus the melody, third reading | 15,262 x 6,243 = 95,280,666 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.27 G/s, 0.4 s | 2026-09-09 |
| Segment 1: one date in two formats, `beach` melody fourth reading (3,804 variants, sixth note read as D# or as E) | 7,124,619 x 3,804 = 27,102,050,676 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.32 G/s, 84.0 s | 2026-09-09 |
| Segment 1: two December dates, `beach` melody fourth reading | 5,796,056 x 3,804 = 22,048,197,024 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.33 G/s, 66.2 s | 2026-09-09 |
| Segment 1: `imagine` spelled out in words, `beach` melody fourth reading | 15,262 x 3,804 = 58,056,648 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.23 G/s, 0.2 s | 2026-09-09 |
| Segment 1: `imagine` is a date written in letters, month abbreviated or full, twice, `beach` from the widest melody family | 319,545 x 13,215 = 4,222,787,175 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.28 G/s, 14.9 s | 2026-09-09 |
| Segment 1: 8-digit block twice, `beach` melody third reading with one extra character (43 encodings) | 100,000,000 x 3,764 = 376,400,000,000 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.33 G/s, 1,149.5 s | 2026-09-09 |
| Segment 1: 8-digit block twice, `beach` written as note names or solfege syllables | 100,000,000 x 560 = 56,000,000,000 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.23 G/s, 242.8 s | 2026-09-09 |
| Segment 1: one date in two formats, `beach` as note names | 7,124,619 x 560 = 3,989,786,640 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.18 G/s, 22.2 s | 2026-09-09 |
| Segment 1: date in letters twice, `beach` as note names | 319,545 x 560 = 178,945,200 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.12 G/s, 1.4 s | 2026-09-09 |
| Segment 1: `imagine` is `1941`, any 8 digits, then `0712`, `beach` from the lists plus the melody | 100,000,000 x 6,243 = 624,300,000,000 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.25 G/s, 2,453.7 s | 2026-09-09 |
| Segment 1: `19410712` then any 8 digits, `beach` melody fourth reading | 100,000,000 x 3,804 = 380,400,000,000 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.21 G/s, 1,796.5 s | 2026-09-09 |
| Segment 1: 8-digit block twice, `beach` read from degree 0 and chromatically | 100,000,000 x 2,617 = 261,700,000,000 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.20 G/s, 1,340.3 s | 2026-09-09 |
| Segment 2: `chess` is 4 pieces in algebraic notation, `wonders` from the earlier structured encodings | 360 x 130,656 = 47,036,160 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.22 G/s, 0.2 s | 2026-09-09 |
| Segment 1: any 8 digits then `19410712`, `beach` melody fourth reading | 100,000,000 x 3,804 = 380,400,000,000 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.28 G/s, 1,382.0 s | 2026-09-09 |

## Earlier passes on the CPU harness, 2026-09-08

| Hypothesis | Space (N) | Method | Result | Witness | Rate | Date |
|---|---|---|---|---|---|---|
| Segment 3: `wasd` is the four movement letters, `ship` is the first family built from the image (174 tokens concatenated 1 to 3 deep) | 10,900,000,000 ordered pairs, `{w,a,s,d}^8` exhaustive | CPU harness on 22 cores | 0 match | yes: head, middle, tail | 4,200,000/s | 2026-09-08 |
| Segment 2: `chess` is the 14 pieces minus exactly 2, in 6 notations and about 18 orders, case inversion included, against the structured `wonders` encodings | 861,000,000 ordered pairs | CPU harness, exhaustive over the reduction | 0 match | yes | 4,200,000/s | 2026-09-08 |
| Segment 1: `imagine` is a pair of calendar dates (188,276 dates, 4 formats, 36 anchor days, each written twice) | 63,330,856 candidates | CPU harness | 0 match | yes | 294,000/s per core | 2026-09-08 |
| Segment 4: `sky` under the capital pinning `n = v - 4`, unique solution under `1 <= n <= len(title)` | 3,599,533 values, exhaustive over the pinned space | CPU enumeration, then GPU crossing above | space exhausted, 0 match in the crossing | yes | n/a | 2026-09-08 |

## Families excluded without running anything

These cost nothing because the author fixed the answer lengths.

| Hypothesis | Why it is excluded | Date |
|---|---|---|
| The clue 6 melody is Do-Re-Mi, the Lost theme, Zelda, Mario, Tetris, Star Wars or 14 other well-known tunes | 18 of the 20 cannot produce 16 characters for 15 notes under any of the 840 encodings tried. Arithmetic only, no oracle call | 2026-09-08 |
| Solfege syllables written out, or bare initials, or all degrees 1 to 7 at one digit | minimum 30 characters, or exactly 15, never 16 | 2026-09-08 |
| Any transcription of a segment ciphertext whose 22nd base64 character is not `A`, `Q`, `g` or `w` | a 16-byte ciphertext leaves only 2 useful bits in that character. This caught one real misreading of segment 3 (`O` against `Q`) | 2026-09-09 |
| Reading each value of clue 8 as a single letter index | two of the values need a track title of 18 letters or more, and only one of the 13 titles is that long. Splitting into digits is forced | 2026-09-08 |

## Observations that closed a channel

| Claim | Scope of the negative | Witness | Date |
|---|---|---|---|
| `ship` is a string written inside the hidden image of `Ship.png` | 24 characters planted at the real size and the real contrast are re-read, even at 61 percent of that contrast; nothing comparable is in the image. The payload is a picture | yes, legibility witness | 2026-09-08 |
| The hidden image comes from a texture of the game | 198 textures extracted from the build, SSIM and correlation, mirrored and not: best real score 0.106 against a planted copy at 1.000 | yes | 2026-09-08 |
| The two faces are real 1912 passengers or crew | about 700 targeted photographs, including the 206 portrait plates of the 1911 source volume: best real score 0.76 against witnesses at 0.92 to 0.99. They are actors in the 1997 film | yes | 2026-09-09 |
| `Beach.png` carries image steganography | 24 bit planes in 2 scan directions, local contrast at 6, 12 and 25 times, and 0 bytes after the IEND chunk. The sand grain co-varies across the three channels, which is a drawn texture | yes | 2026-09-08 |
| The three numbers of clue 5 are great-circle distances between monuments | haversine over the New7Wonders plus Giza plus 21 monuments, both units, tolerance 60: no coincidence under 6 miles. 12,772 miles is also more than half the Earth's circumference | yes | 2026-09-09 |
| Clue 4 is a chess problem | Stockfish 17, 20 seconds, multipv 4: no forced mate, no unique move, and the position is in no database. It encodes the position, it does not ask a question about it | yes | 2026-09-08 |
| The game demo hides a positional music player, so "the first fifteen you hear" depends on where the player stands | the level has one AudioSource playing the whole album from t = 0 on loop; the `PositionMusicPlayer` and `Phonograph` classes exist in the assembly but no instance is present, checked over all 2,174 MonoBehaviours of the level | yes | 2026-09-09 |
| The clue-5 numerals are great-circle distances among the canonical eight wonders under the all-km reading (round 10) | round-11 audit: rows 1 and 3 each match exactly one canonical pair, but row 1 is 539 km past pi*R under the measured `mi/km/mi` pennants, row 2 lies outside the canonical range and needs a widened pool, the joint coincidence is ~1.8% before forking-path corrections, and the pictograms do not depict the sites. Status UNPROVEN, not confirmed | tool `clue5_geo_audit.py` | 2026-10-01 |
| The clue-5 pictograms and row pennants can be isolated by red-crayon colour segmentation | INCONCLUSIVE, not a refutation: the corridor's parquet floor is deep red (4.3% of floor pixels lie inside the crayon mask), the largest connected component is a 23,439 px floor blob, and no colour transform tried separates the drawings. Superseded for the *pennants* by `clue5_pennant.py` below, which keys on R−G and isolates components | tool `clue5_ink.py` | 2026-10-01 |
| The clue-5 pennants do not all point the same way (correction X2) | CONFIRMED by pixels, not eye-read: thresholding R−G and measuring each pennant's normalised per-column ink-height profile gives mast/point row 1 LEFT/RIGHT, row 2 RIGHT/LEFT, row 3 LEFT/RIGHT — i.e. right/left/right = units mi/km/mi. Identical at every cut from 110 to 150 | tool `clue5_pennant.py` | 2026-10-01 |
| Two cheap clue-5 coincidences: row-1 pair lengths 9+11 = 20 chars; the six songs' album years (Σ 12,023) plus track numbers (Σ 38) = 12,061 (row 3) | 4 of 28 canonical pairs sum to 20 (P≈0.14); exactly one exact hit in ~35 metadata combinations. Recorded as coincidences, not leads | checked by hand + `clue5_geo_audit.py` | 2026-10-01 |
| Clue 3's one-to-one star/entry pairing shows the grid is deliberately constructed | round-12 null model: 200,000 random placements of 4 stars + 4 entries on the 10×10 grid give a perfect nearest-entry matching 6.2% of the time, and a perfect matching with every nearest strictly unique 3.4% of the time (~1 in 30). The pairing is a common property of 4 points on a grid, not evidence of authorship | tool `clue3_graph_audit.py` | 2026-10-01 |
| "Cycle order" fixes a single clue-3 candidate | REFUTED: nothing on the 92-cycle marks a start cell. Rotating to begin at each of the four entry cells, in both walk directions, yields 8 distinct 8-char candidates (`5d2w1s4a` `2w1s4a5d` `1s4a5d2w` `4a5d2w1s` `4a1s2w5d` `1s2w5d4a` `2w5d4a1s` `5d4a1s2w`). The round-12 pick `a4d5w2s1` is the forward rotation starting at 4A, i.e. 1 of 8, chosen with no clue-based reason | tool `clue3_graph_audit.py` | 2026-10-01 |
| A clue-3 candidate can be tested against the oracle before clue 7 is solved | REFUTED: segment 3's AES-256 key is `clue3 (8) ‖ clue7 (24) = 32` bytes, and `oracle.py --segment` requires both halves. The eight 0x08 padding bytes live in the single block produced by the full key, so no partial filter exists. `oracle.py` rejects a lone clue-3 candidate with an argparse error | tool `clue3_graph_audit.py` + `oracle.py` | 2026-10-01 |
| Clue 2's eight anagram words can be assigned to the eight ciphertext chunks by letter-multiset / case relations, and the permutation then yields the answer | REFUTED, two independent reasons. (a) Word lengths (2,5,8,7,4,8,3,4) equal chunk lengths exactly, including which pairs share a length, so only 2!×2! = 4 assignments are length-compatible — there is no constraint problem to solve. (b) The 15 capitals are read positionally from one fixed 41-cell string, so chunk labels never enter the extraction and all 4 assignments give byte-identical output `BPEFJDFPOCDBDNB`. The permutation is unobservable; only the chunk *boundaries* could matter, and both candidate boundary sets are already recorded | tool `clue3_root_encoding.py` | 2026-10-01 |
| Clue 7's answer is a 24-character sentence describing the montage (`andrewsmay...` / `the...will founder` register) | 4 of 4 rejected against the segment-3 ciphertext: `andrewsandismayviewplans`, `andrewsandismayontitanic`, `andrewsdrawstheshipplans`, `theoceanlinerwillfounder` — all NO MATCH paired with `d3w1as24`. Scope: these refute the *pairs*, conditionally on the clue-3 half, and do not refute `d3w1as24` itself. The object-label register (`titanicplans`, `shipfounder`) remains untested and is a different family | tool `oracle.py` | 2026-10-01 |

## Round 18 negatives, 2026-10-01 (the round-15..17 write-ups)

Run through `tools/segsweep.py` (restored this round), which normalises as the
author's `fix_clues.script` does, reports the candidates dropped on length (none
below), and plants a witness per call. Every run: witness re-found, 0 hits.
Family definitions and the derivation audit are in
`SESSION-FINDINGS-2026-10-01j.md`.

| Hypothesis | Space (N) | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Segment 3: `ship` is the side-elevation/bulkheads register (13 exact-24 strings), `wasd` is one of the 1,290 retained clue-3 readings | 13 x 1,290 = 16,770 | CPU `segsweep` | 0 match | yes | 2026-10-01 |
| Segment 3: same 13 strings, `wasd` is any of `{w,a,s,d}^8` | 13 x 65,536 = 851,968 | CPU `segsweep` | 0 match | yes | 2026-10-01 |
| Segment 3: `ship` is the IV-derived founder/fall register (3 exact-24 strings), `wasd` structural | 3 x 1,290 = 3,870 | CPU `segsweep` | 0 match | yes | 2026-10-01 |
| Segment 3: same 3 strings, `wasd` over `{w,a,s,d}^8` | 3 x 65,536 = 196,608 | CPU `segsweep` | 0 match | yes | 2026-10-01 |
| Segment 2: `chess` is one of 4 case-preserving piece orderings, `wonders` is every single deletion of the 21-letter Roman string (14 distinct) plus `chartingeightwonders` | 4 x 15 = 60 | CPU `segsweep` | 0 match | yes | 2026-10-01 |
| Segment 4: `scramble` from the re-derived instruction-word family (32), the literal running-sum family (20) and the write-ups' 7 verbatim strings, `sky` either 17-digit candidate | 58 x 2 = 116 | CPU `segsweep` | 0 match | yes | 2026-10-01 |

| Claim | Scope of the negative | Witness | Date |
|---|---|---|---|
| The round-15..17 clue-2 instruction-word strings are generated by the rule the write-ups state | the rule, re-implemented and enumerated over 32 conventions (word->chunk assignment x positional/compact alignment x WITH/YOUR add-or-neutral x A=1/A=0 x chunk-rule/cell-rule), contains `ekmmhjcyiolfxit` at Hamming distance 1 and the other three at 3, 12 and 13; the strings themselves were still tested against both skies and are 0 | yes | 2026-10-01 |
| `dtyeimhtiawruik` implements round 17's running-sum reading | CONFIRMED as a derivation (1-based conversion, no dash reset, emit after adding); REFUTED as an answer, 0 match against both skies | yes | 2026-10-01 |
| Segment 3 can be attacked with new `ship` families | bounded negatively: the two new registers plus the full `{w,a,s,d}^8` space give 1,069,216 cumulative pairs with 0 matches (round 18 total across all segments: 1,069,392) | yes | 2026-10-01 |

## Round 19 negatives, 2026-10-01 (the round-19 write-up)

| Hypothesis | Space (N) | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Segment 4: `scramble` from the **widened** character-aligned anagram-word family (key source = word A=0 / word ASCII / position-in-word / position-in-chunk / chunk's first ciphertext char; operation +/-; output mod-26 letter or printable ASCII; positional or compact alignment; 4 word assignments), `sky` either 17-digit candidate | 69 x 2 = 138 | CPU `segsweep` | 0 match (5 candidates dropped on length — the ASCII-output variants can contain a space, which `fix_clues.script` removes — and reported) | yes | 2026-10-01 |
| Clue 5: the three numerals as a pairwise metadata feature of the six confirmed quoted songs (all pairwise differences, sums and length products over year / track / title, artist and album lengths / title ASCII sum / quoted-line index, letters and words, plus six-way sums) | 643 distinct feature values, exact and ±1 / ±9 / ±35 | CPU search | 1 exact hit, and it is the **six-way** `Σyears + Σtracks = 12,061` already recorded as a coincidence in round 11; **0 pairwise hits** at any tolerance | n/a | 2026-10-01 |

| Claim | Scope of the negative | Witness | Date |
|---|---|---|---|
| Clue 5's "pair of songs, one metadata number" model can produce rows 1 and 3 | **BOUNDED OUT, not swept**: every non-geographic pairwise feature in the write-up's list is bounded below 12,000 (release-date gap max 8,782 days; any single duration < 1,200 s and all six < 3,600 s; track number ≤ 13; title length ≤ 80 letters). Only a surface distance in km (≤ π·R = 20,015 km) or a six-way sum can reach 12,772 / 12,061, and the distance pairs are refuted (round 8). Row 2's 5,210 remains the only reachable pair target, already a ~9 km near-miss | n/a | 2026-10-01 |

## Round 20 negatives, 2026-10-01 (the round-20 write-up)

| Hypothesis | Space (N) | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Segment 3: `ship` is the **full/initial name register** (`jbruceismay`, `thomasandrews`, `edwardsmith`, `victorgarber`, `jonathanhyde`, `bernardhill`, `jbismay`, `tandrews`, `esmith`, plus `and`/`the`/`of` and `titanic`/`ship`/`drawing`/`plans`/`liner`/`ocean`), every string exactly 24 chars, `wasd` structural | 272 x 1,290 = 350,880 | CPU `segsweep` | 0 match — includes the write-up's `jbruceismaythomasandrews` against all 1,290 | yes | 2026-10-01 |
| Segment 3: the 34 full-name **pair** strings (incl. `jbruceismaythomasandrews`, `thomasandrewsjbruceismay`, `thomasandrewsedwardsmith`, `edwardsmiththomasandrews`), `wasd` any of `{w,a,s,d}^8` | 34 x 65,536 = 2,228,224 | CPU `segsweep` | 0 match | yes | 2026-10-01 |
| Segment 4: `scramble` from the clue-2 **marker** families (capital position / value / ordinal / delta / ASCII indexing the ciphertext, the instruction in sentence and display order, and the alphabet), the **instruction-window** family (every 15-char window of both instruction orderings), and the **word-chunk feature** shifts (capital count / lowercase count / word length per chunk), `sky` either 17-digit candidate | 237 x 2 = 474 | CPU `segsweep` | 0 match | yes | 2026-10-01 |

| Claim | Scope of the negative | Witness | Date |
|---|---|---|---|
| Clue 7's answer can be a caption, name or nameplate written in the recovered image | **CLOSED BY MEASUREMENT, not by another family**: the payload plane is line art (ink 0.250) and tesseract 5.5.0 over it at 1:1/2x/4x, both polarities, psm 6/7/11, whole-plane and per-element and per-candidate-text-line, returns 52 strings of >=3 alphanumerics, all noise. There is no text in the montage to caption | `tools/clue7_montage_scan.py` | 2026-10-01 |
| The hidden image has a second payload layer | the sign channel `R != G` is pure noise (ink 0.501, block-std 0.032) against the structured parity payload (ink 0.250, block-std 0.197); the carrier is exactly `R = G + d`, `d in {-1,0,+1}`, with `G == B` | `tools/clue7_montage_scan.py` | 2026-10-01 |
| The Puzzling StackExchange question 122638 ("An anagrammed logic puzzle!") is an independent record of clue 2 | **REFUTED as a source**: posted 2023-10-09, two years after P2G was announced (2021-07-25); one non-accepted partial answer, no solution. Its only new information is the author's comment that "the answer is in the form of a phrase/sentence", which the 15-character instruction-window family now tests (0) | StackExchange API (question/answers/comments) | 2026-10-01 |

## Uncertified, does not count

| Hypothesis | Space (N) | What went wrong | Status |
|---|---|---|---|
| Segment 4, wave F | 6,110,000,000 ordered pairs | the process exited 0 but wrote no verdict line, so there is no evidence the sweep reached the end | to be replayed; it is not counted in any total above |

## Round 21 (2026-10-01) — a capability, and a correction to the method

| Hypothesis | Space (N) | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Clue 7's payload is a **dither** rather than line art | 2,073,600 px; run-length + uniform-block statistics vs synthetic line-art and dither controls | `tools/clue7_montage_recover.py` | **dither** — runs 1.71/5.12 and uniform-8x8 0.1165, against controls 2.48/21.26 & 0.3303 (line art) and 1.80/2.23 & 0.0000 (dither) | yes, synthetic controls | 2026-10-01 |
| The recovered montage contains text | recovered montage, 3 scales, 2 polarities, psm 6/11/12 | OCR | 0 words; fragments only (`2eamesiatreRE`, `Sears`, `Baty`) | yes | 2026-10-01 |
| The payload is a dither of the G-channel photograph | block-mean correlation, n=4/8/16 | correlation | **+0.0925 / +0.1020 / +0.1084** — no; the payload is a *different* photograph | yes | 2026-10-01 |
| The C engine equals pycryptodome on real keys | 3,504 keys | `tools/seg3_crosscheck.py` | 0 disagreements, full 16-byte plaintexts compared | yes | 2026-10-01 |

### The structural negative that reframes every earlier clue-7 run

`{w,a,s,d}^8` (65,536) and `{0-9}^8` (100,000,000) **both exclude every mixed
string**, and all 1,290 retained clue-3 readings are mixed — each contains at
least one digit and at least one of `w/a/s/d`, including the repo's strongest
`d3w1as24`. So every clue-7 negative recorded in rounds 14–20 was computed
against a clue-3 space that could not have held its own best candidates. Those
negatives are **doubly conditional** (they assume a clue-3 half, and they sweep
the wrong alphabet) and must not be cited as refuting a clue-7 string outright.

### Solo sweep — clue-7 candidates vs the COMPLETE clue-3 space

Each candidate is swept against all `wasd0123456789^8` = 1,475,789,056 clue-3
answers, so these are **unconditional**, not joint.

| clue-7 candidate | clue-3 space swept | keys | result | witness |
|---|---|---|---|---|
| `victorgarberjonathanhyde` | `wasd0123456789^8` | 1,475,789,056 | **no match** | yes, re-found |
| `jonathanhydevictorgarber` | `wasd0123456789^8` | 1,475,789,056 | see `tools/clue7_solo_sweep.py` output | yes |
| `edwardsmiththomasandrews` | `wasd0123456789^8` | 1,475,789,056 | see sweep output | yes |
| `thomasandrewsedwardsmith` | `wasd0123456789^8` | 1,475,789,056 | see sweep output | yes |
| `smithandrewsdeckplanlast` | `wasd0123456789^8` | 1,475,789,056 | see sweep output | yes |
| `thenightmovestomakerofit` | `wasd0123456789^8` | 1,475,789,056 | see sweep output | yes |
| `thecoldnightmovestomaker` | `wasd0123456789^8` | 1,475,789,056 | see sweep output | yes |
