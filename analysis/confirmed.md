# Confirmed findings — consolidated register

Every claim in this repository that is marked **CONFIRMED**, in one place, with
its evidence and the tool or file that produced it. Sources: `analysis/IMAGE-TRANSCRIPTION.md`
(authoritative for every clue image — it wins over all other files), the round
files `analysis/SESSION-FINDINGS-*.md`, `analysis/tested.md` (negatives),
`analysis/leads.md` (open leads), and `tools/oracle.py` (`--selftest`).

How to read it

- **CONFIRMED** means one of: a measurement from the pixels, a run that
  reproduced a published witness, a source read directly, or a proof. It does
  **not** mean "solved" — no segment is solved and this puzzle is open.
- A confirmed *structure* is not a confirmed *answer*. The distinction is kept
  explicit below, because three rounds of clue-7 candidates were built on an
  unread picture and a mis-stated board.
- Negatives live in `analysis/tested.md`; open leads in `analysis/leads.md`.
  This file carries only what is established, plus §7 (what is **not**).
- Last updated: round 21 (`SESSION-FINDINGS-2026-10-01m.md`).

---

## 1. The puzzle's own machinery

| # | Fact | Evidence |
|---|---|---|
| M1 | Escrow address `LUtL7qnm3gzxKjHcfVLSjydqhhinTVmTmS` is a valid Litecoin P2PKH address; WIF version 0xB0, address version 0x30. | `oracle.py --selftest` T1; decode of the address |
| M2 | The published scheme is real: a 32-byte `super_key` cut into four 8-byte segments, each AES-256-CBC encrypted under its own 16-character IV with a key = two clue answers concatenated as raw ASCII. | `clues/computer_screen.jpg`, transcribed in `IMAGE-TRANSCRIPTION.md` §9; `oracle.py` reproduces it |
| M3 | Each segment ciphertext is one AES block holding 8 useful bytes, so its plaintext must end in eight `0x08` bytes: a per-segment oracle with false-positive rate 2⁻⁶⁴, needing nothing from the other six answers. | `oracle.py` docstring; selftest T6 (witness re-found, 0 false positives on 1024 keys) |
| M4 | Segment table, exactly: seg 1 `few_n_far_btween` (clues 1+6, bytes 0–7), seg 2 `nocturnal_sugars` (4+5, 8–15), seg 3 `colors_on_leaves` (3+7, 16–23), seg 4 `seconds_of_dream` (2+8, 24–31). | `IMAGE-TRANSCRIPTION.md` §9; `oracle.SEGMENTS` |
| M5 | Answer lengths and case, from `clues.sheet`: imagine 16, scramble 15, wasd 8, chess **12 and case-preserved**, wonders 20, beach 16, ship 24, sky 17 → 128 characters = four 32-byte keys. | `IMAGE-TRANSCRIPTION.md` §10; `oracle.ANSWER_LEN` |
| M6 | `fix_clues.script` removes spaces everywhere and lowercases every clue **except clue 4**. | `IMAGE-TRANSCRIPTION.md` §9; `oracle.normalise_answer` |
| M7 | The oracle reproduces its published guarantees on this machine. | `python3 tools/oracle.py --selftest` → `SELFTEST OK` (T1–T9), re-run every round including round 18 |
| M8 | A wrong-length candidate is dropped before any AES call, so a family of the wrong length collapses for free. | `oracle.py`; every sweeper reports its drop count |

## 2. Clue by clue

### Clue 1 — `imagine`, 16 (segment 1, with clue 6)

| # | Fact | Evidence |
|---|---|---|
| C1.1 | The poem is eight lines on parchment and the number **`19410712`** is printed below it, alone. | `IMAGE-TRANSCRIPTION.md` §3 |
| C1.2 | The poem is a rewrite of Lennon's "Imagine" ("living life in peace" → "Livin' life today"). | Round 6 §1; the clue-1 image itself |

### Clue 2 — `scramble`, 15 (segment 4, with clue 8)

| # | Fact | Evidence |
|---|---|---|
| C2.1 | **The whole panel is stored rotated 90° counter-clockwise.** Rotating it upright recovers the three text lines. Every OCR-only attempt failed for this reason. | `IMAGE-TRANSCRIPTION.md` §2; `tools/clue2_pixels.py` |
| C2.2 | Line 3, the ciphertext, is exactly `s-bcBPEFfJDfeFmksmPOkChDhrgBqjD-i---ffeNB` — 41 cells. | Eye-read; quoted identically in `IMAGE-TRANSCRIPTION.md` §2 and `oracle.py` |
| C2.3 | The 41 cells are **15 capitals + 26 non-capitals** (21 lowercase + 5 dashes). The 15 equals the answer length; the 26 equals the alphabet. | Reproduced counts; `IMAGE-TRANSCRIPTION.md` §2 |
| C2.4 | The 15 capitals are `BPEFJDFPOCDBDNB`, at 1-based cells 5,6,7,8,10,11,14,19,20,22,24,28,31,40,41. The 5 dashes are at cells 2,32,34,35,36. | Reproduced; `IMAGE-TRANSCRIPTION.md` §2 |
| C2.5 | The 8 anagram words are `TO LOWER SUBTRACT CAPITAL WITH ADDITION THE YOUR` (displayed scrambled), and their lengths `2,5,8,7,4,8,3,4` sum to **exactly 41**, so they partition the string in display order: `s-` `bcBPE` `FfJDfeFm` `ksmPOkC` `hDhr` `gBqjD-i-` `--f` `feNB`. | `IMAGE-TRANSCRIPTION.md` §2; `tools/clue2_layout.py` |
| C2.6 | Re-ordered into the sentence ("with your capital, addition. to the lower, subtract.") the same 41 cells partition differently (`s-bc` `BPEF` `fJDfeFm` `ksmPOkCh` `hD` `hrg` `BqjD-` `---ffeNB`). Both boundary sets are recorded. | `IMAGE-TRANSCRIPTION.md` §2 |
| C2.7 | Cell 10 is a capital **`J`**, not `I` (an earlier OCR read `fIDfeFm`). | `tools/clue2_ink.py`, per-cell glyph render |
| C2.8 | No cell is drawn in a different shade, weight or tint: **the answer letters are not highlighted**. The only outliers are the 5 dashes (≈46–53 ink px vs 150–270). | `tools/clue2_ink.py` |
| C2.9 | The clue-2 word↔chunk assignment has **no free parameter that matters**: lengths pin 6 of 8 words and the 15-capital extraction is positional, so all 4 length-compatible assignments give the identical string `BPEFJDFPOCDBDNB`. | `tools/clue3_root_encoding.py` |

### Clue 3 — `wasd`, 8 (segment 3, with clue 7)

| # | Fact | Evidence |
|---|---|---|
| C3.1 | The 10×10 grid, transcribed cell by cell (digit + one of ▲▼◀▶, four ★ cells). Full table in `IMAGE-TRANSCRIPTION.md` §1, encoded in `tools/wasd_grid.py`. | Two independent eye-read passes, agreeing cell for cell |
| C3.2 | The rule is a **step-size pointer** (digit = multiplier, arrow = direction); the four stars are numbered **1** (r5c7), **2** (r9c3), **3** (r2c4), **4** (r9c9) — **not** in reading order. | `tools/clue3_closure.py`; `IMAGE-TRANSCRIPTION.md` §1 |
| C3.3 | Graph decomposition, exact: **one 92-cell cycle**, **4 one-step entry cells**, **4 stars with no successor**; 92 + 4 + 4 = 100. | `tools/clue3_graph_audit.py`, reproduced |
| C3.4 | The four entries join the cycle in one step at cycle indices **6, 9, 13, 80**, spelling **`saad`** in row-major source order. | `tools/clue3_closure.py` part 2 |
| C3.5 | There are **8 cells with no predecessor**: the 4 stars + 4 arrow roots; the 4 arrow roots carry all four WASD directions, one each. | `tools/wasd_grid.py` |
| C3.6 | **The digits are redundant.** For all **96/96** arrow cells the printed digit is forced by (position, arrow, successor). No extraction that reads the digits can recover anything the pointer graph does not already give. | `tools/clue3_closure.py`, 0 exceptions |
| C3.7 | `d3w1as24` — the 8 root cells row-major, WASD letter for an arrow-root and number for a star-root — is a clean 8-character encoding needing no invented metric. The same 8 cells give `53214124`. | `tools/clue3_root_encoding.py` |
| C3.8 | The star→nearest-entry pairing is **one-to-one and unique under both Manhattan and Euclidean** distance (→ `w2s1d5a4`). | `tools/clue3_graph_audit.py` |
| C3.9 | The 92-cycle string is exactly the **arrow content of 92 cells read in walk order**; it hides no message (no window, Caesar shift or substitution yields English). | `tools/clue3_closure.py` §3 |
| C3.10 | **No clue-3 candidate can be tested yet**: segment 3's key is `clue3 (8) ‖ clue7 (24)`, and the PKCS7 padding lives in the single block of the full key, so there is no partial filter. | `tools/oracle.py --segment` requires three arguments; round 12 §3 |

### Clue 4 — `chess`, 12, **case preserved** (segment 2, with clue 5)

| # | Fact | Evidence |
|---|---|---|
| C4.1 | The poem is `A period of madness / From a symbol that's flown / Order in the court / From the front lines to the throne`. | `IMAGE-TRANSCRIPTION.md` §4 |
| C4.2 | The board, read square by square (white at the bottom): rank 8 `4r3`; rank 7 `rkp2p2`; rank 6 `1p1p1np1`; rank 5 `6N1`; rank 4 `3B4`; rank 3 `1QP5`; rank 2 `2K5`; rank 1 `8`. **14 pieces**: black Re8, Ra7, Kb7, Nf6, pawns c7 f7 b6 d6 g6 (lowercase); white Ng5, Bd4, Qb3, Pc3, Kc2 (uppercase) — black 9, white 5. Case matters here because clue 4 is the only answer that keeps it. | `IMAGE-TRANSCRIPTION.md` §4 table + its piece list |
| C4.3 | The FEN **printed** in `IMAGE-TRANSCRIPTION.md` §4 is malformed and disagrees with the table it sits under; the round-14 quote is malformed too. The table-derived FEN `4r3/rkp2p2/1p1p1np1/6N1/3B4/1QP5/2K5/8 w - - 0 1` is the one that parses, with 14 pieces. | Round 18 check: both printed strings have rank sums ≠ 8 and only 12 pieces; the table form sums to 8 on every rank |
| C4.4 | 14 pieces − 2 kings = 12 = the answer length: the natural reduction is the 12 non-king pieces, case preserved. | Arithmetic; structural only, not a solved answer |

### Clue 5 — `wonders`, 20 (segment 2, with clue 4)

| # | Fact | Evidence |
|---|---|---|
| C5.1 | The poem has **8 lines** (lines 1, 5, 6, 7 were missing from earlier files): `Charting the eight wonders` … `With the stars in the sky our guide`. | `IMAGE-TRANSCRIPTION.md` §5 (CORRECTION X1) |
| C5.2 | The poem is a **six-song lyric collage**. Lines 2,4,5,6,7,8 quote verbatim: Vintersorg "Astral and Arcane" (*Cosmic Genesis*, 2000, track 1); Falkenbach "Havamal" (*Heralding – The Fireblade*, 2005, track 3); Nightwish "Ghost Love Score" (*Once*, 2004, track 9); Pink Floyd "High Hopes" (*The Division Bell*, 1994, track 11); Coheed and Cambria "Three Evils" (*In Keeping Secrets…*, 2003, track 4); Alestorm "Treasure Island" (*No Grave But the Sea*, 2017, track 10). | Rounds 6–7; `tools/clue5_music.py`; phrase search, each matched word-for-word |
| C5.3 | Lines 1 and 3 are the author's own instruction, **not** quotes (no lyric hit in any phrasing). | Round 7 §R7-C3 |
| C5.4 | The three Roman numerals carry **vincula**: `X̅M̅MDCCLXXII` = 12,772; `V̅CCX` = 5,210; `X̅M̅MLXI` = 12,061. Their **letters are 11 + 4 + 6 = 21**, against a 20-character answer — a hard off-by-one. | `IMAGE-TRANSCRIPTION.md` §5 (CORRECTION X3) |
| C5.5 | The nine pictograms = the triangle glyph **used three times** (rotated 180° in row 1) + **six** non-triangle pictograms: headstone-with-heart, flowering sprig, anchor, beast/dragon head, horned mask, star-?-star. | `IMAGE-TRANSCRIPTION.md` §5–6 (CORRECTION X6) |
| C5.6 | The pennants point **right / left / right**, measured from pixels (stable at every threshold 110–150), and `KM` is on the left wall, `mi` on the right → units **mi / km / mi**. | `tools/clue5_pennant.py` (CORRECTION X2, confirmed by pixel measurement) |
| C5.7 | Therefore row 1's value is 12,772 mi = 20,554 km, which **exceeds Earth's maximum great-circle distance π·R = 20,015 km by 539 km**: row 1 cannot be a surface distance under the measured units. | Arithmetic; `IMAGE-TRANSCRIPTION.md` §5 |
| C5.8 | The author's second album *Archaic Reveries* (2018) has **exactly 8 tracks**, one of them titled "Seven Miles". | R7-C5, album metadata B07DQH55PC |

### Clue 6 — `beach`, 16 (segment 1, with clue 1)

| # | Fact | Evidence |
|---|---|---|
| C6.1 | The poem is eight lines (`Our counting starts with a deer` … `Note the first fifteen you hear`), over a pixel-art beach. | `IMAGE-TRANSCRIPTION.md` §7 |
| C6.2 | The melody source is the author's own video "Seconds of Dream – Path to Greatness Soundtrack" (2019), monophonic; **the first fifteen notes are measured** by FFT to within 1 cent: A#5 F#5 B5 A#5 F#5 D#5 F5 C#5 B4 C#5 A#4 A#5 F#5 B5 A#5, key F# major / D# minor. | `leads.md` §1 (measurement, not a guess) |
| C6.3 | 16 characters for 15 notes, so exactly one note costs two characters; the 6th note bends between D#5 and E5. The **convention** is open (C6.3 is a constraint, not an answer). | `leads.md` §1 |
| C6.4 | The melody is **not** a well-known tune: 18 of 20 candidate tunes cannot produce 16 characters for 15 notes under any of 840 encodings. | `analysis/tested.md`, arithmetic only |

### Clue 7 — `ship`, 24 (segment 3, with clue 3)

| # | Fact | Evidence |
|---|---|---|
| C7.1 | **The carrier is recovered**: `clues/qr2.jpg` → `https://tinyurl.com/y28knqz3` → Google Drive file `1jzxIFQGmTnR3EB42bd-DPEJfe655XbhG`, fetched as `clues/Ship.png` (2,896,530 bytes, 1920×1080, RGBA). | `tools/clue7_ship_extract.py` |
| C7.2 | Channel structure: alpha uniformly 255, **G and B identical**, so the payload is confined to the **red channel**. | Measured; `IMAGE-TRANSCRIPTION.md` §8 |
| C7.3 | Its own poem is now first-hand (8 lines), and **stanza 1 is the extraction instruction**: "a red sky … a channel for light" → red channel, "the least bit significant" → least significant bit. | `IMAGE-TRANSCRIPTION.md` §8 (CORRECTION X8) |
| C7.4 | **Red bit plane 0 is the hidden montage** (set fraction 0.250) and is the only structured low plane (planes 1–3 are 0.498/0.501/0.511, pure static). | Measured; `tools/clue7_ship_extract.py` |
| C7.5 | **There is no nested layer**: after removing a local box blur from plane 0, no pixel carries a further LSB. | `IMAGE-TRANSCRIPTION.md` §8 |
| C7.6 | The montage's middle element is the ship's **bow and foremast** with standing rigging. It is **not** "deck plans". | `IMAGE-TRANSCRIPTION.md` §8 (CORRECTION X7, refined round 21) |
| C7.7 | **WITHDRAWN — see C7.14/C7.15.** The claim that the right-hand portrait carries the heavy moustache was read off the raw 1-bit plane and has the two portraits **reversed**. | **WITHDRAWN**, round 21, `SESSION-FINDINGS-2026-10-01m.md` §2 |
| C7.8 | **The carrier is exact**: `R = G + d` with `d in {-1, 0, +1}` for every pixel (100% within ±2), and `G == B` everywhere. So the author perturbed the red channel by at most one unit against a base image carried in G/B, and the payload is the red **parity** bit. | `tools/clue7_montage_scan.py`, round 20 §1a |
| C7.9 | **No second payload layer**: the red LSB plane is structured (ink 0.250, block-std 0.197) while the sign channel `R != G` is pure noise (ink 0.501, block-std 0.032). Independent method from round 14's box-blur test, same conclusion. | round 20 §1a |
| C7.10 | **WITHDRAWN.** "The montage is line art (~0.25 ink)" was an inference from ink fraction alone. Round 21 measures it as a **dither**: mean horizontal run of ones **1.71** / zeros **5.12** and uniform 8x8 blocks **0.1165**, against synthetic line-art controls of 2.48 / 21.26 and 0.3303, and dither controls of 1.80 / 2.23 and 0.0000. | **REFUTED**, round 21, `tools/clue7_montage_recover.py` §1 |
| C7.11 | **There is no legible text in the montage.** Confirmed on the **recovered** montage: OCR at three scales, both polarities, psm 6/11/12 returns only fragments (`'2eamesiatreRE'`, `'Sears'`), never a word. **Weakened**: round 20 ran OCR on the raw 1-bit plane, where dither noise destroys glyphs, so it could not have found text even if present. | round 21, `tools/clue7_montage_recover.py` §6 |
| C7.12 | The two portrait regions are **different images**: normalised correlation −0.059 (mirrored −0.058, rot180 +0.054). | round 20 §1b |
| C7.13 | **The payload is a dithered photograph and is recovered legibly by block-averaging**: `bm = (parity & 1).reshape(h//8,8,w//8,8).mean(axis=(1,3))`. At n = 8 the montage is plainly readable; at n = 4 more detail returns. | round 21, `tools/clue7_montage_recover.py` §3 |
| C7.14 | **The recovered montage is two male portraits flanking the ship's bow**: the left portrait has a **heavy drooping moustache**; the right portrait is **clean-shaven**. **Orientation is not mirrored** — the poem is legible and unmirrored in G at the top right. | round 21, `montage_n08.png` / `montage_n04.png` |
| C7.15 | **The identity of the two men is OPEN.** Round 20's "moustache => Smith" had the portraits reversed, and round 14's "Andrews on the right" is unsupported. The left moustache is *consistent with* Bernard Hill's Smith, but that is an inference from a photograph, not a measurement. | round 21, `SESSION-FINDINGS-2026-10-01m.md` §2 |
| C7.16 | **The G channel is a clean black-and-white photograph of RMS Titanic under full sail, bow to the right**, with this clue's poem typeset top-right. Never rendered in this repository before round 21. | round 21, `clue7_G_channel.png` |
| C7.17 | **The payload is a *different* photograph from the G-channel base image**: block-mean correlation between the parity plane and G is +0.0925 / +0.1020 / +0.1084 (n = 4/8/16). The author carries the real ship photograph visibly in G/B and hides a different picture in red's parity bit. | round 21, `tools/clue7_montage_recover.py` §2 |

### Clue 8 — `sky`, 17 (segment 4, with clue 2)

| # | Fact | Evidence |
|---|---|---|
| C8.1 | The panel carries the two worked examples `4 → Exit Light → T` and `8 → Ghost March → R` above exactly **13 question marks** and the 13-cell string `ehk-bqNEFRUn-` (dashes at cells 4 and 13). | `IMAGE-TRANSCRIPTION.md` §6 (CORRECTION X5) |
| C8.2 | **The operation is confirmed as a dual-branch rule**: `4 → Exit Light → T`. Cell 4 is a *dash*, so its track is its own position (track 4 = `exitlight`) and the letter is that track's 4th character, `t`. `8 → Ghost March → R`: cell 8 is `E` (value 5), so its track is the alphabet value wrapped into 1..13 (track 5 = `ghostmarch`), and the letter is the track's 8th character, `r`. | Reproduced against the real tracklist; `oracle.py` finding 3 |
| C8.3 | The *number* in each example is the cell's **position**; the *track* is chosen by the cell's **value** (letter) or **position** (dash). This is the only simple rule that reproduces both witnesses — which is why "number = track index" is refuted (track 8 is `daylightbrings`, whose 8th letter is `t`, not `r`). | R6-C2 |
| C8.4 | Reading the cells that way gives 13 letters `g a e t u i f r l h i t a`; dropping the trailing dash terminator (cells 1–12) gives alphabet positions that concatenate to exactly **17 digits**: `71520219618128920`. | `tools/seg4_sky_track.py`, prints the whole family |
| C8.5 | The album is `Seconds of Dream` (2021-01-07, 13 tracks), in order: 1 Few and Far Between, 2 The Suffocating Carrier, 3 The Surrogate, 4 Exit Light, 5 Ghost March, 6 Nocturnal Sugars, 7 All Art Must Die, 8 Daylight Brings, 9 Hills of Life, 10 As Seen From Afar, 11 The Great Adventure, 12 Sequels, 13 Seconds of Dream. Durations sum to exactly 3,426,218 ms, the certified total for the album audio in the game demo. | iTunes lookup, collection 1548289299 (`SESSION-FINDINGS-2026-09-30.md` C2); re-verified as R6-C1 |
| C8.6 | **Value-as-index is impossible for every assignment**: the clue needs two cell values ≥ 18 (18 and 21) but only **one** title is ≥ 18 letters (`thesuffocatingcarrier`, 21). So no assignment of the 11 letter-cells to distinct tracks, positional or not, can read the cell value as an index into its assigned track. | `tools/seg4_sky_track.py`; the repo's original counting argument was right |
| C8.7 | Both author example titles are the author's own tracks, chosen so the Metallica lyric "Exit light, enter night" falls out. | Round 6 §1 (interpretation of the choice; the titles themselves are C8.5) |

## 3. Cross-cutting confirmed facts

| # | Fact | Evidence |
|---|---|---|
| X1 | The clue poems are assembled from **song material**: clue 5 quotes six prog/metal songs verbatim; clue 1 rewrites "Imagine"; clue 8's dictionary is the author's own album. | Rounds 6–7 |
| X2 | Clues **4, 6 and 7 are not lyric collages** — their lines return no lyric hit. The collage habit is specific to clue 5 (plus clue 1's rewrite). | R7-C4 |
| X3 | Segment 3's IV `colors_on_leaves` is **not** a track on the 13-track album; the other three IVs are tracks 1, 6 and 13. | `IMAGE-TRANSCRIPTION.md` §9; re-verified round 18 in `oracle.SEGMENTS` |
| X4 | `tools/segsweep.py` is restored: the round-14 driver three committed tools import (`clue3_ship_cross.py`, `clue7_ship_family.py`, `clue7_desc_sweep.py`) had never been committed. It normalises, **reports** length drops, and plants a witness per call. | Round 18; the 1,290 retained clue-3 readings reproduce through it |
| X5 | The 1,290 retained clue-3 readings are the union of `clue3_ship_cross` families A–F (A=4, B=70, C=15, D=82, E=1120, F=2). | Round 14 §4; re-derived round 18 |
| X6 | **The clue-3 spaces swept before round 21 cannot hold the repo's own best clue-3 answers.** `{w,a,s,d}^8` (65,536) and `{0-9}^8` (10⁸) both exclude any *mixed* string, and all 1,290 retained readings are mixed — they need letters and digits. Every clue-7 negative in rounds 14–20 was therefore computed against a space that could not have contained `d3w1as24`. | Arithmetic on the alphabets; round 21 §5 |
| X7 | **The C search engine agrees with pycryptodome byte for byte** on 3,504 real keys (the repo's structural clue-3 readings × clue-7 candidates, plus a uniform spread over all 14 alphabet characters), comparing full 16-byte plaintexts under the real segment-3 ciphertext and IV. | `tools/seg3_crosscheck.py`, 0 disagreements |
| X8 | The C engine's **selftest re-derives the S-box** from its definition (multiplicative inverse in GF(2⁸) plus the affine map) and requires 256/256 agreement, plus `ISBOX ∘ SBOX = id`. This caught two transcription errors in the tables as first written. | `tools/seg3_cross.c selftest` |
| X9 | Clue 7 **can now be tested on its own**: `seg3_cross alpha` sweeps all `wasd0123456789^8` = **1,475,789,056** clue-3 answers per clue-7 candidate, at ~1.3M keys/s (~19 min). A string that fails is refuted **unconditionally** rather than conditionally on a guess about a closed source. | `tools/seg3_cross.c`, `tools/clue7_solo_sweep.py` |

## 4. Confirmed impossibilities and exact boundaries

These are proven, and they save whole searches. Each is a CONFIRMED statement
about a *family*, not about a single candidate.

| # | Statement | Evidence |
|---|---|---|
| N1 | Clue 8's value-as-index pairing is impossible for every assignment (needs two titles ≥ 18 letters; one exists). | C8.6 |
| N2 | The clue-3 digits are redundant with (position, arrow, successor) in all 96 arrow cells — nothing to mine there. | C3.6 |
| N3 | Clue 3's grid is a **closed source**: digits redundant, the 92-cycle fully consumed (all 85 windows fail), and the four star labels are the only unconstrained data (all 70+15 arrangements fail). Only new information about clue 7 can move segment 3. | Round 14 §11 |
| N4 | Clue 3 cannot be tested before clue 7 exists (the key is both halves). | C3.10 |
| N5 | "Cycle order" is a family of **8**, not a candidate: nothing marks a start cell (4 entries × 2 directions). | Round 12 §2c |
| N6 | The star→nearest-entry pairing being clean is **not** evidence of authorship: ~3.4% of random placements of 4 stars + 4 entries look the same. | Percentages from 200,000-trial null model, round 12 §2a |
| N7 | The clue-3 "40,320 interleavings" is 8!, a permutation search, not a reading of the grid; the grid-faithful family is **70**. | Round 13 §2 |
| N8 | Clue 2's word↔chunk permutation is unobservable (all 4 length-compatible assignments give identical output). | C2.9 |
| N9 | The clue-5 all-km geography solution is **closed**: under the measured units row 1 is 539 km past π·R, and no band-origin pair supplies rows 1 or 3. | C5.7; rounds 8, 11–12 |
| N10 | Reading each clue-8 value as a single letter index is impossible (two values need a title ≥ 18 letters; one exists). | Same counting argument as N1 |
| N12 | Clue 7's answer cannot be a caption, name or nameplate written in the recovered image: **the montage contains no text** (OCR negative over three scales, both polarities, three page-segmentation modes). The characters must be derived from what is depicted, and generated description families are exhausted (3.0 M pairs across rounds 14–20). | C7.11; round 20 §1b |
| N11 | Clue 5's "two songs, one metadata number" model **cannot produce rows 1 or 3**: every non-geographic pairwise feature is bounded below 12,000 — release-date gap max 8,782 days, any single duration < 1,200 s and all six < 3,600 s, track number ≤ 13, title length ≤ 80 letters. Only a surface distance in km (≤ π·R = 20,015 km) or a six-way sum can reach 12,772 / 12,061, and the distance pairs are refuted. Row 2 (5,210) is the only reachable pair target. | Round 19 §2a (bound); round 8 (no origin pair near rows 1/3); round 11 (the six-way coincidence) |

## 5. Confirmed negatives with their measured scope

Full ledger in `analysis/tested.md`. The headline totals, because a 0-hit result
is only meaningful with its space size:

| Family | Space | Result |
|---|---|---|
| Segment 1, `imagine` = any 8-digit block twice, across the whole 10⁸ space, against many `beach` readings | ~10⁸ per reading, dozens of readings | 0 match |
| Segment 1, date families (one date in two formats, two December dates, spelled-out dates), 1–2100 | up to 7.1 M date pairs × beach families | 0 match |
| Segment 3, `ship` name/actor/quote/deck-name families and a 399,986-string description family | 1,609,062 pairs | 0 match |
| Segment 3, round-18 side-elevation + founder/fall registers, alone and over `{w,a,s,d}^8` | 1,069,216 pairs | 0 match |
| Segment 2, `chess` = 14 pieces − 2, in 6 notations × ~18 orders × structured `wonders` | 861,000,000 pairs | 0 match |
| Segment 4, clue-2 families (arithmetic, positional, keyboard, permutation, ordering-key, English words, 26-non-capital key, dash/pairing, music corpus, instruction-word, running-sum) | 800,000+ hypotheses; 714.5 G pairs in one crossing | 0 match |
| Round 18 total (all segments) | 1,069,392 pairs | 0 match |
| Control channels closed: image steganography in `Beach.png`; strings written inside `Ship.png`; the two faces as real 1912 people; the melody as 18/20 known tunes; `CrimsonGrid` as the carrier; clue 4 as a forced mate (Stockfish, 33 first moves — see X9 for the position caveat) | — | all negative, with witnesses |

## 6. Corrections this register inherits as settled

| # | Correction | Source |
|---|---|---|
| X1 | Clue 5's poem has 8 lines, not 4. | `IMAGE-TRANSCRIPTION.md` §0 |
| X2 | Clue 5's pennants are → ← → → units **mi / km / mi** (not all km). | §0; C5.6 |
| X3 | The Roman numerals carry vincula; the letters are 21 against a 20-character answer. | §0; C5.4 |
| X4 | Clue 2's second text line is indented; the panel is rotated 90° CCW. | §0; C2.1 |
| X5 | Clue 8's panel carries 13 question marks, decorative key/paths/padlock and icon groups, not just the two examples. | §0; C8.1 |
| X6 | Clue 5 pictogram 1 of row 1 is a headstone with a heart, not a map pin. | §0 |
| X7 | `Ship.png`'s middle element is the ship's bow and foremast, not deck plans. **The right-portrait moustache claim was withdrawn in round 21 — the portraits were reversed.** | §0; C7.6, C7.14 |
| X11 | **Clue 7's payload is a dithered photograph, not line art.** Every element identity recorded in rounds 14–20 was read off the raw 1-bit plane and is unreliable; block-averaging recovers a legible image. | Round 21, C7.10 (withdrawn), C7.13 |
| X12 | The **G channel is a clean photograph of RMS Titanic** (bow right) with the poem typeset top-right, and the payload is a *different* photograph from it (block-mean corr ~ +0.10). | Round 21, C7.16–C7.17 |
| X8 | Clue 7's red-LSB mechanism is stated by its own poem, stanza 1 — it was assumed before the file was read. | §0 |
| X9 | The clue-4 FEN printed in §4 (and quoted in round 14) is **malformed** and disagrees with the board table; the table-derived FEN is `4r3/rkp2p2/1p1p1np1/6N1/3B4/1QP5/2K5/8 w`. | Round 18, §C4.3 |
| X10 | The album tracklist used by the earliest analysis was wrong; the real 13-track list is C8.5 (`nocturnal_sugars` is track 6, not 2). | `SESSION-FINDINGS-2026-09-30.md` C2 |

## 7. What this register does NOT confirm

Listed so these are never cited as facts. Each is a live hypothesis with its
status; the detail is in the round files and `analysis/leads.md`.

| Item | Status |
|---|---|
| `sky = 71520219618128920` | 🟡 **UNCONFIRMED** — the mechanism is confirmed (C8.2) and this is the unique witness-consistent candidate, but it has not passed segment 4 against any clue-2 family (0/116 in round 18) |
| `sky = 58112171456182114` | 🟡 UNCONFIRMED (repo's earlier structural candidate) |
| `wasd = d3w1as24` | 🟡 CONFIRMED as an **encoding**, unconfirmed as an answer, and untestable until clue 7 exists |
| Every clue-7 `ship` string so far | 🔴 0 match — and every pre-round-21 negative is **doubly conditional**: it assumed a clue-3 half, and it swept a clue-3 alphabet that cannot hold any mixed answer (X6). The solo sweep (X9) is the fix. `victorgarberjonathanhyde` is now refuted unconditionally. |
| The two faces' identities | ⚠️ **FULLY OPEN, and both prior readings were wrong.** Round 21 recovered the montage and shows the heavy moustache on the **left** portrait with the right one clean-shaven (C7.14), so round 20's "Smith on the right" is withdrawn and round 14's "Andrews on the right" is unsupported. It now needs external identification against the 1997 film frames. |
| The full-name clue-7 register (`jbruceismay`, `thomasandrews`, `edwardsmith`, initials, incl. `jbruceismaythomasandrews`) | 🔴 0 match — 350,880 pairs against the 1,290 retained clue-3 readings and 2,228,224 against `{w,a,s,d}^8` |
| A caption/name/nameplate as the clue-7 answer | 🔴 **CLOSED by measurement** (N12) |
| The Puzzling StackExchange puzzle 122638 as an independent source for clue 2 | 🔴 **REFUTED** — it post-dates P2G by two years (2023-10-09 vs 2021-07-25) and has no posted solution; its only new information is the author's phrase/sentence hint, and the 15-character instruction-window family it motivates is 0/108 |
| The clue-5 pictograms ↔ the six songs/sites | 🟡 unverified pairing (4 of 6 fit naturally; sprig and mask are guesses) |
| The clue-5 three-numeral → 20-character extraction | 🟡 mechanism unknown |
| Six rebus icons → six songs → three **directed pairs** measured by the three numerals | 🔴 the pair-model payoff is bounded out for rows 1 and 3 (N11: **0 pairwise hits in 643 measured features**); the icon↔song pairing itself stays a plausible but unverified inference |
| `Charting the eight wonders` = New7Wonders+Giza or the author's 8-track album | 🟡 open fork (geography closed as a solution, C5.7) |
| The clue-4 "symbol that's flown" = International Code of Signals | 🟡 untested |
| Clue-4 `chess` = 14 pieces − 2 kings, ordered "front lines to the throne" | 🟡 structural only |
| The clue-4 SAN-mate refutation (Stockfish, round 14) | ⚠️ **conditional** — the position string quoted there is malformed and disagrees with the board table (X9); it should be re-run against `4r3/rkp2p2/1p1p1np1/6N1/3B4/1QP5/2K5/8 w` before being relied on |
| The clue-2 instruction-word and running-sum readings | 🔴 family tested, 0 match; the external write-up's other strings are not reproducible from the rule it states |
| Clue 1's `imagine` = the literal number rather than a date | 🟡 the date family is exhausted, this reading is open |
| The 16th character of `beach` | 🟡 convention open; the 15-note measurement itself is confirmed (C6.2) |
| Any segment solved | 🔴 no |
| The puzzle solved | 🔴 no |
