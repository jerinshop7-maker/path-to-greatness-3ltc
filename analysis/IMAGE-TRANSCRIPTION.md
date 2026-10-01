# Image transcription — every clue file, read visually

**Why this file exists.** Every text-bearing element of all nine clue files has now
been read *by eye* from the actual images (not OCR). This document is the
authoritative transcription. Where it disagrees with `analysis/leads.md`,
`analysis/tested.md`, or `analysis/SESSION-FINDINGS-2026-09-30.md`, **this file
wins** — and every disagreement is called out as a CORRECTION.

Method: each JPEG was cropped and upscaled 3–10× with LANCZOS and read directly.
Glyph geometry (column positions, Roman-numeral vincula, pennant orientation) was
measured in pixels. All files are 2560×1440 except `Beach.png` (400×316).

---

## 0. Global corrections found by reading the images

| # | Correction | Where it was wrong |
|---|---|---|
| **X1** | **Clue 5's poem has 8 lines, not 4.** Lines 1, 5, 6, 7 were missing. | `author-posts.md`, `leads.md`, `tested.md`, `SESSION-FINDINGS` all quote only 4 lines |
| **X2** | **Clue 5's pennants do NOT all point the same way.** Row 1 points **right**, row 2 **left**, row 3 **right**. Therefore the units are **mi, km, mi** — not "all km". | the pasted analysis §6 ("each ending in a pennant whose point faces left") |
| **X3** | **The Roman numerals carry vincula (overbars).** X̅M̅MDCCLXXII = 12,772 (not 2,782). The repo's values were right, but only because the overbar was applied; the *letters* are 11+4+6 = **21**, against a **20**-character answer. | never stated anywhere |
| **X4** | **Clue 2's second text line is indented** relative to line 1 (starts ~6–7 monospace cells right). | dropped by OCR in `SESSION-FINDINGS` §5c |
| **X5** | **Clue 8's panel carries far more than the two examples**: 13 question marks, a curved arrow, a decorative key/paths/padlock, and three emoji icon groups. | `author-posts.md` records only the two examples and the string |
| **X6** | **Clue 5 pictogram 1 of row 1 is a headstone with a heart**, not a map/location pin. | (nobody had transcribed the pictograms at all) |

---

## 1. `clues/clue3_wasd.jpg` — clue 3, "wasd", 8 characters

Scene: an orange sandstone corridor, brick walls, Greek-key floor border, two
lit wall torches. A translucent parchment panel on the far wall.

Title, in quotes, lowercase: `"wasd"`

Below it a **10 × 10 grid**. Each cell holds a **digit + a filled triangular
arrow** in one of four orientations: `▲` `▼` `◀` `▶`. Four cells instead hold a
**five-pointed star** with a number instead of an arrow. Verified full transcription:

```
row 1:  7▼ 5▶ 2▶ 8▼ 3▼ 1▶ 5▼ 7◀ 4▼ 1◀
row 2:  2▶ 4▶ 1▲ 3★ 5▶ 5▼ 6▼ 6▼ 2◀ 1▼
row 3:  3▼ 6▶ 3▶ 1▶ 4▼ 7▼ 6▼ 1▲ 8◀ 3◀
row 4:  3▶ 5▶ 5▶ 3▲ 5▶ 2▼ 1◀ 3▼ 2▲ 1▼
row 5:  1▲ 6▶ 3▶ 3▼ 1◀ 4▲ 1★ 4▲ 2▼ 9◀
row 6:  2▶ 3▲ 3▲ 3▲ 4▲ 3▼ 2▶ 4▼ 4▲ 6◀
row 7:  5▲ 5▲ 4▶ 3▼ 3◀ 5◀ 3◀ 2▶ 6◀ 6▲
row 8:  2▶ 4▲ 3▲ 5▶ 2▲ 4◀ 2▼ 2◀ 5▲ 4◀
row 9:  1▼ 4▲ 2★ 4▶ 4▲ 4▶ 2◀ 3▲ 4★ 8◀
row 10: 9▶ 4▲ 6▲ 2◀ 2▲ 3◀ 6◀ 1▶ 4◀ 4▲
```

The four stars are numbered **1** (r5c7), **2** (r9c3), **3** (r2c4), **4**
(r9c9) — i.e. the star numbers are *not* in reading order. This transcription is
encoded in `tools/wasd_grid.py` and reproduces the repo's claimed structure exactly.

## 2. `clues/clue2_scramble.jpg` — clue 2, "scramble", 15 characters

**The whole panel is stored rotated 90° counter-clockwise** (text reads
bottom-to-top). After rotating 90° CW, the panel is a dark screen with three
typewriter-font lines in pale grey, left-aligned on a monospace grid:

```
line 1:  ot rleow utbrctsa aacpilt hwti
line 2:  <indent> dioiatdn het ryuo          <- indented ~6-7 cells (CORRECTION X4)
line 3:  s-bcBPEFfJDfeFmksmPOkChDhrgBqjD-i---ffeNB
```

Line 3 is set in a **smaller** monospace than lines 1–2 (measured pitch ≈ 20.5 px
vs ≈ 28.9 px) because it is 41 characters long. Line 1 occupies monospace columns
0–29, line 2 starts at column ≈ 6.5.

The eight anagrams, **as displayed** (scrambled letters, scrambled order), with
their lengths — the lengths sum to exactly 41, the length of line 3, so they
partition it in *display* order:

| displayed anagram | word | len | segment of line 3 (display order) |
|---|---|---|---|
| `ot` | TO | 2 | `s-` |
| `rleow` | LOWER | 5 | `bcBPE` |
| `utbrctsa` | SUBTRACT | 8 | `FfJDfeFm` |
| `aacpilt` | CAPITAL | 7 | `ksmPOkC` |
| `hwti` | WITH | 4 | `hDhr` |
| `dioiatdn` | ADDITION | 8 | `gBqjD-i-` |
| `het` | THE | 3 | `--f` |
| `ryuo` | YOUR | 4 | `feNB` |

Re-ordered into the **sentence** the words spell ("with your capital, addition.
to the lower, subtract.") the same 41 characters partition differently:

| sentence position | word | len | segment |
|---|---|---|---|
| 1 | WITH | 4 | `s-bc` |
| 2 | YOUR | 4 | `BPEF` |
| 3 | CAPITAL | 7 | `fJDfeFm` |
| 4 | ADDITION | 8 | `ksmPOkCh` |
| 5 | TO | 2 | `hD` |
| 6 | THE | 3 | `hrg` |
| 7 | LOWER | 5 | `BqjD-` |
| 8 | SUBTRACT | 8 | `---ffeNB` |

String statistics (both re-verified): 41 cells; **15 capitals** (at cells
5,6,7,8,10,11,14,19,20,22,24,28,31,40,41 → `BPEFJDFPOCDBDNB`); 21 lowercase;
**5 dashes** at cells 2, 32, 34, 35, 36.

## 3. `clues/clue1_imagine.jpg` — clue 1, "imagine", 16 characters

Poem, centred, in a serif face on parchment (matches the repo exactly):

```
Imagine all the people
Livin' life today
Imagine life was taken
Left a number in its place
Imagine that number of years
Past that fateful day
Imagine it written twice
The infamous way
```

and beneath it, alone: **`19410712`**

## 4. `clues/clue4_chess.jpg` — clue 4, "chess", 12 characters (the only clue that keeps its case)

Scene: an orange corridor; a parchment panel on the right holds a poem in a
blackletter/gothic face, and to its left a chessboard on a wooden table.

Poem:
```
A period of madness
From a symbol that's flown
Order in the court
From the front lines to the throne
```

Board read square by square (white pieces light with dark outline, black pieces
solid dark; **white is at the bottom**, so the top row is rank 8):

```
        a    b    c    d    e    f    g    h
   8    .    .    .    .   [R]   .    .    .
   7   [R]  [K]  [p]   .    .   [p]   .    .
   6    .   [p]   .   [p]   .   [N]  [p]   .
   5    .    .    .    .    .    .   [N]   .
   4    .    .    .   [B]   .    .    .    .
   3    .   [Q]  [P]   .    .    .    .    .
   2    .    .   [K]   .    .    .    .    .
   1    .    .    .    .    .    .    .    .
```

FEN: `4r1k1p1/pp3np1/8/6N1/3B4/1QP5/2K5/8 w - - 0 1`
Counts: **14 pieces** — black Re8, Ra7, Kb7, Nf6, pawns c7 f7 b6 d6 g6;
white Ng5, Bd4, Qb3, Pc3, Kc2. White 5, black 9.

## 5. `clues/clue5_wonders.jpg` — clue 5, "wonders", 20 characters

Scene: an orange corridor. **Left wall carries the word `KM`**; **right wall
carries `mi`** (both in a light serif face; the left one is partly occluded by a
torch). Parquet floor with a Greek-key border.

Parchment panel: an **8-line poem** (CORRECTION X1) and **three rows**, each row =
three pictograms followed by a Roman numeral with a vinculum and then a **pennant**.

```
1  Charting the eight wonders
2  A thousand maps drawn with blood
3  A bit of help from each line
4  To shelter my ship on the flood
5  We used to swim the same moonlight waters
6  Dragged by the force of some inner tide
7  No longer will we wait for your answers
8  With the stars in the sky our guide
```

The nine pictograms, hand-drawn in red crayon outline:

| row | pictogram 1 | pictogram 2 | pictogram 3 | numeral (with vinculum) | value | pennant points |
|---|---|---|---|---|---|---|
| 1 | **headstone with a heart**, rounded-top slab, heart carved in the middle, **zigzag bottom edge** | the triangle glyph, **rotated apex-down** | **flowering branch / sprig** — stem, leaves, a small flower | `X̅M̅MDCCLXXII` (bar over `XM`, 11 letters) | **12,772** | **RIGHT** |
| 2 | **anchor** | the triangle glyph, **apex-up** | **beast / dragon head**, horns, ears, angry brows, eye, fangs | `V̅CCX` (bar over `V`, 4 letters) | **5,210** | **LEFT** |
| 3 | **horned mask**, two horns, rectangular face, two eyes | the triangle glyph, **apex-up** (identical to row 2) | **star ? star** | `X̅M̅MLXI` (bar over `XM`, 6 letters) | **12,061** | **RIGHT** |

The **triangle glyph** is one drawing used three times, verified pixel by pixel: a
triangle with a **crossbar across its flat edge** and one half filled solid while
the other half is left outlined. In row 1 it points **down** (crossbar on top,
right half solid); rows 2 and 3 point **up** (crossbar at the bottom, left half
solid) — i.e. row 1 is the exact 180° rotation of rows 2/3. Because the same
symbol is reused with only its orientation changed it is behaving as a **direction
indicator**, not as three separate landmarks — leaving **six** non-triangle
pictograms.

Pennant direction is **→ ← →**. `KM` is on the left wall, `mi` on the right, so
**row 1 = miles, row 2 = kilometres, row 3 = miles** (CORRECTION X2). This is
**CONFIRMED by pixels**, not only by eye — see `tools/clue5_pennant.py` and
round 12 in `SESSION-FINDINGS-2026-10-01g.md`; it isolates the crayon by
thresholding R−G (background floor/wall sit at ≈ 80, crayon at 120–255, clean
bimodal gap) and measures the normalised per-column ink-height profile of each
pennant, mast end → point end:

| row | profile, left → right | mast | point |
|---|---|---|---|
| 1 | `0.03 0.93 0.57 0.52 0.51 0.43 0.36 0.36 0.31 0.28 0.27 0.24 0.18 0.10 0.03` | LEFT | **RIGHT** |
| 2 | `0.03 0.09 0.18 0.19 0.24 0.27 0.34 0.33 0.37 0.43 0.49 0.52 0.55 0.88 0.13` | RIGHT | **LEFT** |
| 3 | `0.10 0.91 0.54 0.52 0.48 0.43 0.36 0.36 0.34 0.27 0.27 0.22 0.18 0.10 0.06` | LEFT | **RIGHT** |

Stable at every threshold from 110 to 150. (Round 12's write-up in
`SESSION-FINDINGS-2026-10-01g.md` §5 reports an outer-fifth mass statistic
instead — `0.333/0.063`, `0.059/0.338`, `0.336/0.070` — computed from a
connected-component crop. Both statistics were run on the same image and agree on
the verdict; the table above is what the committed tool prints.)
Values: 12,772 mi · 5,210 km · 12,061 mi
(= 20,554 km · 5,210 km · 19,411 km).

**Row 1 is therefore impossible as a great-circle distance on Earth**: 20,554 km
exceeds the maximum π·R = 20,015 km by 539 km, which closes the all-km geography
reading as a solution to clue 5.

Roman-numeral **letter counts are 11 + 4 + 6 = 21**, against a 20-character
answer (CORRECTION X3) — one letter too many, which is itself a clue.

## 6. `clues/00111111.jpg` — clue 8, "sky", 17 characters

Same corridor scene. Panel contents, top to bottom (CORRECTION X5):

1. **Decorative art**: a purple **key**; two winding dark-teal **paths** with
   arrowheads, each with a purple **?** beside it; a purple **padlock**; a short
   teal path stub below the padlock.
2. A row of three red emoji-like icons: a **film/camera** glyph, a **retro
   television/computer** glyph with two antennae, and **three five-pointed stars**.
   A tiny `×` sits below the middle icon.
3. The **rule panel**:
   ```
   4 → Exit Light → T
   8 → Ghost March → R
        (curved red arrow)
     ? ? ? ? ? ? ? ? ? ? ? ?          <- exactly 13 question marks
     e h k - b q N E F R U n -        <- 13 cells, underlined
   ```
4. Below: a red **anchor** and a red **horned/angry face** (the same icon family
   as clue 5's pictograms), each with a `?`.

The string is `ehk-bqNEFRUn-`: 11 letters, dashes at cells **4** and **13**.

## 7. `clues/Beach.png` — clue 6, "beach", 16 characters (via `qr1.jpg`)

A pixel-art beach: pale sky, turquoise sea with a white breaking wave, wet sand,
and a palm tree on the right. Poem overlaid in a small dark sans-serif:

```
This time we change the channel
And traverse to lost dimensions
Here we find a pattern
That demands our full attentions
Our counting starts with a deer
Our pattern starts with the sun
Note the first fifteen you hear
Write them up and this step's done
```

## 8. `clues/qr2.jpg` → `Ship.png` — clue 7, "ship", 24 characters

The PNG itself was not retrieved in this session; the poem recorded in
`author-posts.md` is taken from the lossless demo texture. Re-verify when the
file is available.

## 9. `clues/computer_screen.jpg` — the encryption scheme

Fully confirmed, character for character, against `author-posts.md`. Four windows
on a dusk-mountain background with an open chest at the foot.

`litecoin_wallet.txt - NextBestText.exe`
```
Public address:
LUtL7qnm3gzxKjHcfVLSjydqhhinTVmTmS

Private key (WIF, encrypted with super_key):
dxIx52zhnXodWi36dEx/kJV59Udj4xh3vR5vmeuoyXTNCE8VOaTmVkVctDpK0XNHYJA6G+m/jT4fSU9VejXYgg==

AES 256-bit, CBC, IV: goodluck_havefun
```

`super_key_segments.sheet - TheSheetsBeneath.exe`
```
id  segment (encrypted)              bytes  iv                     key
1   I2c6TXU/Z1oCKnEQTWZUvg==          0-7    few_n_far_btween      clue 1 + 6
2   RWaBo4ChEOM/i+MLy2NUpg==          8-15   nocturnal_sugars      clue 4 + 5
3   16GmtUINaYuN7f1RlBO5sQ==          16-23  colors_on_leaves      clue 3 + 7
4   7CZlZjwCMGUb/TZm07b9dg==          24-31  seconds_of_dream      clue 2 + 8
```

`clues.sheet - TheSheetsBeneath.exe`
```
id  clue      sk_seg  bytes
1   imagine   1       0-15
2   scramble  4       0-14
3   wasd      3       0-7
4   chess     2       0-11
5   wonders   2       12-31
6   beach     1       16-31
7   ship      3       8-31
8   sky       4       15-31
```

`fix_clues.script - FlipTheScript.exe`
```
1  foreach clue:
2      clue.answer.remove_spaces()
3      if clue.id != 4:
4          clue.answer.to_lowercase()
5
6  // A monkey on a typewriter wrote this
7  //  at some point in time.
```

Seg3 NOTE: segment 3's IV `colors_on_leaves` is **not** a track on the 13-track
album "Seconds of Dream"; the other three IVs are tracks 1, 6 and 13.

## 10. Answer lengths (from `clues.sheet`, confirmed)

| id | clue | segment | bytes in key | length | case |
|---|---|---|---|---|---|
| 1 | imagine | 1 | 0–15 | 16 | lowercased |
| 2 | scramble | 4 | 0–14 | 15 | lowercased |
| 3 | wasd | 3 | 0–7 | 8 | lowercased |
| 4 | chess | 2 | 0–11 | 12 | **case preserved** |
| 5 | wonders | 2 | 12–31 | 20 | lowercased |
| 6 | beach | 1 | 16–31 | 16 | lowercased |
| 7 | ship | 3 | 8–31 | 24 | lowercased |
| 8 | sky | 4 | 15–31 | 17 | lowercased |
