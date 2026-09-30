# Path to Greatness (3 LTC) — session findings, 2026-09-30

Independent session on top of the repository's own analysis. Everything below was
re-derived or newly tested here; nothing is copied on faith. The oracle is
`tools/oracle.py` (repo) — its `--selftest` prints `SELFTEST OK` on this machine
after two import fallbacks were added for Python 3.14 (see Tooling).

## 1. CONFIRMED this session

| # | Fact | Evidence |
|---|---|---|
| C1 | The oracle is intact and reproduces its published guarantees. | `python3 tools/oracle.py --selftest` → T1–T9 all OK, including the canonical secp256k1 vectors for privkey 1, the synthetic witnesses on both AES layers, the 0x30 escrow decode, and base64 canonicity of all four 16-byte ciphertexts (22nd char g/g/Q/g). |
| C2 | **The album tracklist used by the repository is wrong.** The real 13 tracks, in order, are: 1 Few and Far Between, 2 The Suffocating Carrier, 3 The Surrogate, 4 Exit Light, 5 Ghost March, 6 Nocturnal Sugars, 7 All Art Must Die, 8 Daylight Brings, 9 Hills of Life, 10 As Seen From Afar, 11 The Great Adventure, 12 Sequels, 13 Seconds of Dream. | iTunes lookup API, collection id 1548289299, releaseDate 2021-01-07, trackCount 13 (full per-track durations retrieved). The durations sum to exactly 3,426,218 ms, the same total the repository certified for the album audio embedded in the demo. `nocturnal_sugars` is track 6 (the repo assumed 2); `allartmustdie` is correctly track 7; `few_n_far_btween` is track 1, `seconds_of_dream` track 13. |
| C3 | **Clue 8's rule is exactly "the n-th letter of the track title, spaces removed" (1-based), and both author examples verify against the real titles.** 4 → Exit Light → `exitlight[4] = t` → T. 8 → Ghost March → `ghostmarch[8] = r` → R. | Direct check; the two examples are only consistent with the real list (the repo's guessed list made the second example look like a positional track pairing). |
| C4 | The clue-8 string is `ehk-bqNEFRUn-`: 13 cells, dashes at cells 4 and 13, 11 letters; their alphabet positions concatenated give **58112171456182114 = exactly 17 digits = the required answer length**. | Reproduced arithmetic. |
| C5 | Clue 2's 41-cell string `s-bcBPEFfJDfeFmksmPOkChDhrgBqjD-i---ffeNB` contains **exactly 15 capitals** (BPEFJDFPOCDBDNB) and 21 lowercase letters and 5 dashes; 15 = the clue-2 answer length, 36 letters total, 41 cells. | Reproduced count; matches the repo's count of 15 capitals and dash positions 2,32,34,35,36. |
| C6 | The clue-1 image really prints the poem and the number `19410712`; the clue-8 panel really reads `4 -> Exit Light -> T` / `8 -> Ghost March -> R`; `computer_screen.jpg` really carries the published scheme. | OCR (tesseract 5.5.0) of the served JPEGs, text matches `clues/author-posts.md` character for character where legible. |

### Why C2 matters (it confirms the repo's counting argument)

**Correction, added in round 3.** An earlier draft of this section claimed three
titles are ≥18 letters (`fewandfarbetween` 18, `thesuffocatingcarrier` 22,
`thegreatadventure` 18) and that this voided the repo's counting argument. That
was a length error. The real title lengths, spaces removed, are

```
1 fewandfarbetween 16   6 nocturnalsugars 15  11 thegreatadventure 17
2 thesuffocatingcarrier 21   7 allartmustdie 13     12 sequels 7
3 thesurrogate 12       8 daylightbrings 14   13 secondsofdream 14
4 exitlight 9           9 hillsoflife 11
5 ghostmarch 10        10 asseenfromafar 14
```

Exactly **one** title is ≥18 letters (`thesuffocatingcarrier`, 21), so the repo's
counting argument was right after all. It is in fact stronger than "positional":
the clue needs two values ≥18 (cells 10 and 11: `R`=18, `U`=21) and only one
title is that long, so **no assignment of the 11 letter-cells to distinct tracks,
positional or not, can read the cell value as an index into its assigned track.**
This kills the "non-positional pairing" hope (lead 4, and the pasted analysis's
starred next target) outright. Reproduced by `tools/seg4_sky_track.py`, which also
re-runs the 78 increasing injections.

## 2. New negatives (certified runs, this machine)

Engine: `tools/sweep.c`, a single-block AES-256-CBC **decryption** padding oracle
written for this session. Certified three ways: (a) FIPS-197/SP 800-38A AES-256
vector `603deb…dff4` / `6bc1bee2…172a` → `f3eed1bdb5d2a03c064b5a7e3db181f8`;
(b) a stage-by-stage decrypt trace identical to pycryptodome (`tools/dectrace.py`);
(c) planted witnesses re-found on segments 1 and 3 and a near-miss control that
stays silent (`tools/witness.py`). Throughput measured **≈4.9 M keys/s single core**
(10^8 keys in 20.5 s).

| Wave | Space | Result | Note |
|---|---|---|---|
| Segment 1: imagine = any 8-digit block written twice, beach = `536531#276755365` | 10^8 | 0 match | independently reproduces the repo's headline negative |
| Same, beach = `5365312767553655` | 10^8 | 0 match | new |
| Same, beach = `5536531276755365` | 10^8 | 0 match | new |
| Same, beach = `53653#1276755365` | 10^8 | 0 match | new |
| Same, beach = `naeeffcatoeitmnn` (album-cumsum reading, see below) | 10^8 | 0 match | new |
| Same, beach = `gtngtftanaggtngt` (degree→track-initials reading) | 10^8 | 0 match | new |
| Segment 1: 112,344 distinct 8-digit dates written twice, crossed with 10 melody conventions (1,123,440 pairs) | 1.1e6 | 0 match | date wave incl. 19410712 / 12071941 / 07121941 in both formats |
| Segment 1: anchor `19410712` + words (`imagine`, `johnlennon`, `peace`, …) × melody | 100 | 0 match | lead 2 sketch |
| Segment 4: scramble = the 15 capitals in order, reversed, rotated (all 15 rotations), lowercase-only, mixed | 18 | 0 match | crossed with sky = `58112171456182114` |
| Segment 4: 60 capital/lowercase arithmetic orderings and shifts of the 15 capitals (sort keys incl. value ± count/sum/first/last/max/min/span of the lowercase before/after, placement permutation, index walks) | 60 | 0 match | `tools/scramble_battery2.py` |
| Segment 4: 13 further mechanical scramble readings (value-position walks, ±1 shifts, running totals mod 26, between-capital groups) | 13 | 0 match | `tools/seg4_battery.py` |

Album-aware beach readings generated from the real tracklist (NEW family, all
16 chars): degree→track letter (`tertefhmrmttert` is 15; 0-based `rtmrthetmtrrtmr`
is 15), note-index-in-track, cumulative-degree walk over the joined album
(`naeeffcatoeitmnn`), degree→track-initials (`gtngtftanaggtngt`). Two of these
were swept at 10^8 each (above); the families that produce 15 characters need a
16th-character convention chosen before they can be swept, which is exactly the
same open question as the ledger's lead 1.

## 3. Clue-8 decode search (all failed, but the search is now exhaustive over the stated rule space)

`tools/sky_decode.py` and `tools/sky_search.py` enumerate, with the REAL
tracklist: (i) 1:1 cell→track with offsets −3…+3 in both bases; (ii) every
increasing injection of the 11 letter-cells into the 13 tracks (78) × both bases
→ 0 valid; (iii) all 1,820 splits of the 17 digits into 13 one/two-digit values,
1-based and 0-based → 0 valid (0-based has no solution at all; 1-based fails at
the value 17 cell); (iv) digit i → track i cycling, both bases → produces
`notehnmdleesoettt` (1-based) — "note" is a coincidence, the tail is not text;
(v) 17 digits as positions in the joined album (173 letters) → `naffefffandfaeffa`,
not text.

Conclusion: either the 17 digits are the literal answer string (the repo's
reading, `sky = 58112171456182114`), or the cell↔track pairing is not positional
and not ordered.

## 4. Tooling delivered (all in `tools/` unless noted)

- `sweep.c` / `sweep` — certified AES-256 L1 padding-oracle brute forcer.
  Mask classes: `.` printable ASCII, `0` digits, `?` all bytes, `r` mirror the
  byte 8 positions earlier (for "the same 8-digit block written twice"), any
  other character = fixed. `sweep test` runs the FIPS vector + full trace.
  Usage: `tools/sweep <seg 1-4> <template32> <mask32> [ct-b64]`.
- `witness.py` — plants a synthetic witness (payload + PKCS7) for any segment.
- `dectrace.py` — stage-by-stage Python decrypt trace for cross-checking.
- `aesdiff.py` — encryption-side round-by-round diff used to find the engine bugs
  (wrong MUL3 table, wrong MixColumns coefficients, out-of-order final
  AddRoundKey, 16-byte-only hex decode, and a table build order that left
  `MUL2` half zero — encryption never notices, decryption refuses to work).
- `candidates.py`, `seg4_attempts.py`, `seg4_battery.py`, `scramble_battery2.py`,
  `sky_decode.py`, `sky_search.py`, `beach_candidates.py`.
- `seg4_exhaustive.py` — round-2 systematic clue-2 x clue-8 cross (28,168 pairs, 0).
- `seg4_sky_track.py` — round-3: corrected track lengths, the impossibility proof,
  the systematic track-selector x letter-index family, the witness-consistent
  scheme, and the cross (22,308 pairs, 0).
- `seg4_clue2_sweep.py` — round-3: 12,826 arithmetic clue-2 rules against both
  pinned skies (25,652 pairs, 0).

## 5. Route tree (ranked by expected value per hour)

```
SEGMENT 1  imagine(16) + beach(16)
├─ (a) beach = 15 melody digits + ONE convention character  ── cheapest
│   ├─ convention ∈ {#1/1#/1b/2/2b for the 6th note; low-octave markers for
│   │   B4/A#4 (pos 9, 11); sol-as-0; degree+octave; solfege with the bend}
│   ├─ test: for each convention string (16), sweep imagine = 8-digit block
│   │   twice (10^8, 20 s) → 32 conventions/hour/core
│   └─ this is the ONLY half-read half-left segment: the notes are measured
│      (A#5 F#5 B5 A#5 F#5 D#5 F5 C#5 B4 C#5 A#4 A#5 F#5 B5 A#5, key D#/F#)
└─ (b) imagine ≠ repeated 8-digit block
    ├─ the repo swept the whole 10^8 repeated-block space against ~3k beach
    │   readings; if (a) keeps failing, imagine is a word/date-hybrid
    └─ test: imagine = the lyric with the replaced word ("livinliftoday" +
        number, "peace79", "1941…" hybrids); 16-char candidates are free to
        test against a short beach list via tools/oracle.py --segment 1

SEGMENT 3  wasd(8) + ship(24)
├─ (a) wasd over the real grid alphabet {0-9,w,a,s,d}^8 = 1.48e9 → 5 min/wave
│   └─ run against 2–3 fresh ship strings from the description family
│      (24 chars, e.g. deckplansandrewsandismay, thedeckplansandtwofaces)
└─ (b) identify the 8 no-predecessor cells as the answer letters: read the grid
    image `clues/clue3_wasd.jpg` by hand (the 1,134 "structural readings" are a
    formalisation, not a transcription — a human reading of the 100 cells is the
    cheap unlock), then the ship side is one 24-char string to guess

SEGMENT 4  scramble(15) + sky(17)
├─ (a) sky = 58112171456182114 (structural, 17 = 17) — then scramble is the only
│   unknown; 60+ mechanical capital rules refuted here
├─ (b) get the 8 anagram words from the clue-2 image: tesseract fails on the
│   styled font; next step is a HUMAN read of `clues/clue2_scramble.jpg`
│   (the transcription in the repo only has the string, not the anagrams)
└─ (c) the cell↔track pairing for clue 8 is non-positional: search permutations
    of the 13 cells to the 13 tracks that make all 11 values valid indexes
    (tooling exists: sky_decode.py)

SEGMENT 2  chess(12) + wonders(20)
├─ (a) name the six pictograms of clue 5 (needs eyes; the km/mi distance reading
│   is refuted by haversine) → then 12772 / 5210 / 12061 as (track, letter)
│   pairs with the REAL tracklist (13 titles now known)
└─ (b) chess: 14 pieces → 12 characters keeping case; "a symbol that's flown" →
    international code of signals (flags) is the untried dictionary
```

## 5b. Round 3 (2026-09-30, later): clue 8 pairing re-derived, clue 2 swept

### N7 — the witness-consistent clue-8 scheme (UNCONFIRMED, leading candidate)

The two author examples are not illustrations of "number = track index". They fix
the operation's two branches exactly:

- `4 -> Exit Light -> T`: cell 4 is a **dash**; its track is its own position
  (4 = Exit Light) and the letter is that track's 4th character, `t`.
- `8 -> Ghost March -> R`: cell 8 is `E`, value 5; its track is its **alphabet
  value** (5 = Ghost March), and the letter is that track's 8th character, `r`.

So the rule the panel states is: *the letter index is the cell's position; the
track is selected by the cell's value (wrapped into 1..13), or by its position
when the cell is a dash.* Applying it to `ehk-bqNEFRUn-` gives the 13 letters

```
g a e t u i f r l h i t a        (cell 4 -> 't', cell 8 -> 'r')
```

whose alphabet positions concatenate to 18 digits. Dropping the **trailing**
dash cell (a terminator, and the only reading that yields the required length)
gives exactly 17 digits:

```
71520219618128920        = G A E T U I F R L H I T  (cells 1..12)
```

This candidate (a) reproduces both author witnesses, (b) is the only variant of
its family that does (`tools/seg4_sky_track.py` prints the whole family), and
(c) lands on the required 17. It is nevertheless **UNCONFIRMED**: it does not
pass segment 4 against any of 3,718 clue-2 candidates (22,308 pairs, 0 hits) nor
against 12,826 arithmetic clue-2 rules with both skies (25,652 pairs, 0 hits,
`tools/seg4_clue2_sweep.py`). Treat it as the best clue-8 hypothesis so far; the
bottleneck it exposes is clue 2.

### N8 — pasted third-party claims checked

| Claim | Verdict |
|---|---|
| `ESHIPJKCBNLINSG` from "capital + nearest preceding lowercase" is a lead | **REFUTED.** It is already in the round-2 candidate set (family `A\|prev_low++0\|a1`); its segment-4 verdict with sky = digits is NO MATCH. It is a coincidence, not a lead (the 5-scheme line is stronger and also does not pass). |
| `DTYEIMHTIAWRUIK` from signed running arithmetic | **REFUTED**, and already covered by the round-2 `running_mod26` family. |
| clue 8's 17 digits are a first-layer encoding, 13 cells map non-positionally to 13 tracks | **REFUTED as stated** (see the correction above: value-as-index is impossible for *every* assignment). |
| the dashes at cells 4 and 13 give a 3+8 split that explains the 17 length | **Not a constraint**: dashes at 4 and 13 delimit 3 and 8 letters; the trailing dash is a terminator, and the 17 length comes from decimal concatenation, not from the split. |
| clue 5's/4's "maritime convergence" | Untested (needs the pictograms and the chess position read by a person); no computational content yet. |

## 5c. Round 4 (2026-09-30, later still): the clue-2 image is rotated, and its
scrambled word order partitions the string

### N9 — the clue-2 image layout (NEW, structural)

The clue-2 JPEG stores all of its text **rotated 90 degrees**; that is why every
previous OCR attempt failed and why the anagrams were never transcribed. Rotating
the crop 270 degrees and running tesseract recovers three lines:

```
ot rleow utbrctsa aacpilt hwti
dioiatdn het ryuo
s-bcBPEFfJDfeFmksmPOkChDhrgBqjD-i---ffeNB
```

The eight anagram words are `ot rleow utbrctsa aacpilt hwti dioiatdn het ryuo`,
i.e. TO LOWER SUBTRACT CAPITAL WITH ADDITION THE YOUR — the instruction, **with
the words themselves displayed in scrambled order** (display rank of the correct
words is `[5,8,4,6,1,7,2,3]`). And the eight word lengths
`2,5,8,7,4,8,3,4` sum to **exactly 41**, the length of the mixed-case string, so
the words partition the string into eight segments:

```
TO       's-'          CAPITAL  'ksmPOkC'
LOWER    'bcBPE'       WITH     'hDhr'
SUBTRACT 'FfJDfeFm'    ADDITION 'gBqjD-i-'
                       THE      '--f'
                       YOUR     'feNB'
```

The two capitals of `Correction` aside, this is a concrete, previously
unrecorded fact about the clue and a new family (reorder the segments into
sentence order before decoding, shift each capital by its segment's word, etc.).

### N10 — the "ENTR" reverse-index signal is the repo's old family, and it is
impossible as a complete rule

With `track = cell position` and `index = len(title) - value - 1` (0-based), the
first usable cells give `E N T R` (`fewandfarbetween[10]=e`,
`thesuffocatingcarrier[12]=n`, `thesurrogate[0]=t`, `ghostmarch[7]=r`). This is
**already the repo's** `n = len - v` reading (leads.md lead 4), which gives
`ent_r??bs???`. It is not a new route, it silently drops **five** of the twelve
letter-cells (values 17, 14, 18, 21, 14 are all out of range), and it is
impossible as stated: `u`=21 needs a title of 22+ letters and the longest title in
the album is 21. Forward indexing is likewise impossible (values 18 and 21 both
need the single 21-letter title). Marked **REFUTED as a complete rule**, and
**not a lead** — a prefix that only survives by discarding 5/12 cells is not
signal.

### N11 — round-4 negatives

| Family | Space | Result |
|---|---|---|
| clue 2: linear combos of up to 3 context features (coeffs -2..2, all shifts/bases) | 793,116 distinct scrambles x 2 skies | 0 |
| clue 2: equal-rank capital/lowercase pairings, permutation-by-key, char-at-position, running with dash resets | included above | 0 |
| clue 2: all 8,846 distinct 15-letter English words (dwyl/english-words) x 2 skies | 17,692 | 0 |
| clue 2: album-indexed selection (value/position as track, any index) | 330 | 0 |
| clue 2: the layout families (sentence-order segments, word Vigenere, raw capitals of the reordered string) | 1,768 (+740) | 0 |

Tools: `tools/seg4_clue2_wide.py`, `tools/clue2_layout.py`.

## 5d. Route tree (round 4)

```
SEGMENT 4  scramble(15) + sky(17)          <-- highest structural confidence
├── SKY
│   ├── repo reading: 58112171456182114 .......... UNCONFIRMED structural
│   ├── witness-consistent scheme -> 71520219618128920 ... UNCONFIRMED,
│   │        both author witnesses reproduced; UNIQUE in its family
│   └── value-as-index into tracks ................ PROVEN IMPOSSIBLE (any
│            assignment; needs 2 titles >= 18, only one exists)
└── SCRAMBLE (now the single bottleneck; 803k+ hypotheses, 0 hits)
    ├── capitals only ............................ REFUTED
    ├── local / running / linear arithmetic ..... REFUTED (793k)
    ├── 15-letter English words ................. REFUTED (8.8k)
    ├── album-indexed selection ................. REFUTED
    └── image layout: words partition the string ... NEW, families REFUTED so far

SEGMENT 1  imagine(16) + beach(16)
├── beach = measured 15 notes + 1 convention char  OPEN (convention sweep is 20 s)
└── imagine = "Livin' life today" replacement      OPEN (not the raw date)

SEGMENT 3  wasd(8) + ship(24)
├── grid: 8 no-predecessor cells -> the 8 chars     OPEN (needs a human read)
└── ship: plain description of the Titanic montage   OPEN

SEGMENT 2  chess(12) + wonders(20)
├── six pictograms (navigation/flags?)              OPEN (needs a human read)
└── chess 14 pieces -> 12 chars, "symbol that's flown"  OPEN
```

## 6. One-line status

No segment solved. Segment 4 is the most constrained: the sky has a unique
witness-consistent candidate and the whole segment now hinges on the 15-character
clue-2 answer, against which 800k+ hypotheses have failed. The clue-8
value-as-index pairing is proved impossible, and the clue-2 image's scrambled word
order (which partitions the string by word length) is the newest structural lead.
