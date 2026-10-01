# Path to Greatness: Treasure Hunt (3.02608794 LTC, OPEN)

Independent cryptanalysis of Justin Patterson's (`jpatt94`) Litecoin treasure hunt
(`p2gtreasure.com`, announced on r/ARG 2021-07-25). The prize is still unspent at
escrow `LUtL7qnm3gzxKjHcfVLSjydqhhinTVmTmS`.

The puzzle: eight clue answers of fixed lengths (16/15/8/12/20/16/24/17 characters)
concatenate to 128 ASCII characters, which are four AES-256-CBC keys, one per pair
of clues. Each key decrypts one 8-byte segment of a 32-byte `super_key`, which
decrypts the WIF blob. Each segment ciphertext is a single AES block holding 8
useful bytes, so its plaintext must end with eight `0x08` padding bytes: a perfect
per-segment oracle with a false-positive rate of 2^-64.

## What this repository contains

- `analysis/IMAGE-TRANSCRIPTION.md` — **every clue image read directly, by eye.**
  Authoritative text for all nine files, with the six corrections this pass found
  (clue 5's missing poem lines, the pennant directions, the Roman vincula, clue 8's
  13 question marks). Wins over the older transcriptions where they disagree.
- `analysis/SESSION-FINDINGS-2026-09-30.md` — Confirmed findings, corrections to
  the prior analysis, every new negative, and the ranked route tree.
- `analysis/SESSION-FINDINGS-2026-10-01.md` — **round 6.** The clue poems are
  lyric collages: clue 5's lines 4–8 quote Falkenbach, Nightwish, Pink Floyd,
  Coheed and Cambria and Alestorm verbatim. The album order and clue-2's `J`
  glyph are re-confirmed; positional/keyboard/in-image-highlight readings of
  clue 2 are refuted.
- `analysis/SESSION-FINDINGS-2026-10-01b.md` — **round 7.** Clue 5 line 2 is
  confirmed as Vintersorg's "Astral and Arcane" (**six** quotes, not five; the
  round-6 "unidentified" was wrong), lines 1 and 3 are the author's
  instruction, and "the eight wonders" forks between New7Wonders+Giza and the
  author's own 8-track *Archaic Reveries*. The music corpus supplies no clue-2
  answer (924 pairs, 0).
- `analysis/SESSION-FINDINGS-2026-10-01c.md` — **round 8.** Clue 2's "26
  non-capitals = alphabet key" route is refuted (1,788 pairs, 0), and the
  clue-5 geography revival fails on arithmetic: under the `mi/km/mi` reading row
  1 is 540 km beyond Earth's maximum great-circle distance, and no band-origin
  pair supplies rows 1 or 3.
- `analysis/SESSION-FINDINGS-2026-10-01d.md` — **round 9.** Clue 2's dash-group
  / capital-lowercase pairing ("expression") route is refuted (3,952 pairs, 0),
  closing every clue-2 family proposed so far; several errors in the pasted
  round-9 fact-list are corrected.
- `analysis/SESSION-FINDINGS-2026-10-01e.md` — **round 10.** The clue-5 numerals
  fit three real great-circle distances to ≤0.3% under the all-km reading
  (Great Wall↔Chichén Itzá 12,738 vs 12,772; Angkor Wat↔Uluru 5,219 vs 5,210;
  Machu Picchu↔Giza 12,037 vs 12,061) using exactly six sites for the six
  pictograms — the first numeric foothold on clue 5. Latest route tree.
- `analysis/SESSION-FINDINGS-2026-10-01g.md` — **round 12.** Clue 3's graph
  decomposition is **CONFIRMED and exact**: a 92-cell cycle, 4 entry cells that
  each join it in one step, and 4 numbered stars, summing to 100. The
  star-nearest pairing is genuinely one-to-one under both distance metrics. But
  it is **not evidence of authorship** (3.4% of random placements look the same),
  "cycle order" yields **8** candidates rather than 1, and — decisively —
  **no clue-3 candidate is testable**, since segment 3's key is clue 3 ‖ clue 7.
  Clue 7 is the bottleneck. Also **confirms correction X2 by pixels**: the three
  pennants measure right / left / right, stable at every threshold from 110 to
  150, which closes round 10's all-km geography as a solution. Latest route tree.
- `analysis/SESSION-FINDINGS-2026-10-01f.md` — **round 11.** An audit downgrades
  round 10's geography fit to **UNPROVEN**: all-km is required by the numbers but
  contradicted by the measured `mi/km/mi` pennants (row 1 is 539 km past the
  Earth's maximum), row 2 is post-hoc, and the pictograms do not depict the
  sites. The independent pixel re-check of the pennants is inconclusive (the
  corridor floor is deep red). Latest route tree.
- `analysis/leads.md`, `analysis/tested.md` — the prior analyst's open leads and
  negative ledger (kept for continuity, see provenance below).
- `clues/` — the nine clue files as served by the puzzle site, plus the two
  lossless carriers reached through the site's QR codes.
- `tools/oracle.py` — the candidate checker (segment oracle, full-address verdict,
  `--selftest`). Two import fallbacks were added so it runs on Python 3.14.
- `tools/sweep.c` — a self-contained AES-256-CBC **decryption** padding-oracle
  brute forcer written for this analysis. Certified against the FIPS-197 /
  SP 800-38A AES-256 vector and against `pycryptodome` stage by stage; planted
  witnesses are re-found and a near-miss control stays silent. Measured
  throughput ≈4.9 M keys/s per core (10^8 keys in 20.5 s).
- `tools/witness.py`, `tools/dectrace.py`, `tools/aesdiff.py` — witness planting
  and the two cross-checks used to certify the C engine.
- `tools/candidates.py`, `tools/seg4_attempts.py`, `tools/seg4_battery.py`,
  `tools/scramble_battery2.py`, `tools/sky_decode.py`, `tools/sky_search.py`,
  `tools/beach_candidates.py` — hypothesis generators and batteries, one per
  segment. Every one reports its own scope.
- `tools/clue3_graph_audit.py` — reproduces clue 3's 92-cycle / 4-entry / 4-star
  decomposition from the authoritative transcription, confirms the star-nearest
  pairing is one-to-one under Manhattan *and* Euclidean distance, then runs a
  200k-trial null model against the "deliberately constructed" claim, enumerates
  the 8-member cycle-rotation family, and shows segment 3 is untestable without
  clue 7.
- `tools/clue5_pennant.py` — measures the three pennants' directions from
  pixels, by thresholding R−G (not absolute red, which the red parquet floor
  defeats) and isolating connected components. Confirms X2 (mi / km / mi) and
  derives every printed conclusion from the measurement.
- `tools/clue5_geo_audit.py` — re-derives round 10's triple, tests its
  uniqueness inside the canonical eight, its unit consistency, its post-hoc
  row 2, and a Monte-Carlo null. `tools/clue5_ink.py` — the reproducible pixel
  attempt at the pictograms/pennants (recorded as inconclusive).

## Confirmed findings (details and evidence in `analysis/SESSION-FINDINGS-2026-09-30.md`)

1. The oracle reproduces its published guarantees on a clean machine
   (`SELFTEST OK`).
2. **The album tracklist used by the prior analysis is wrong.** The real
   "Seconds of Dream" (2021-01-07, 13 tracks) is: 1 Few and Far Between,
   2 The Suffocating Carrier, 3 The Surrogate, 4 Exit Light, 5 Ghost March,
   6 Nocturnal Sugars, 7 All Art Must Die, 8 Daylight Brings, 9 Hills of Life,
   10 As Seen From Afar, 11 The Great Adventure, 12 Sequels,
   13 Seconds of Dream. The durations sum to exactly 3,426,218 ms, the certified
   total for the album audio embedded in the game demo.
3. **Clue 8's operation is "the n-th letter of the track title, spaces
   removed".** Both author examples verify against the real titles:
   `4 → Exit Light → exitlight[4] = t`, `8 → Ghost March → ghostmarch[8] = r`.
   The *number* in each example is the cell's position (cell 4 is a dash, cell 8
   is `E`), and the *track* is chosen by the cell's value (`E`=5 → Ghost March)
   or, for a dash, by its position (4 → Exit Light). Reproducing both witnesses
   this way fixes the rule and yields a 17-digit sky candidate
   `71520219618128920` (`tools/seg4_sky_track.py`). It is UNCONFIRMED — it does
   not pass segment 4 against 3,700+ clue-2 candidates. The bottleneck is clue 2.
4. The prior analysis's "counting argument" that closed clue 8 is **correct**:
   the real title lengths are 16/21/12/9/10/15/13/14/11/14/17/7/14, so exactly
   one title is ≥18 letters and the clue needs two values ≥18 (18 and 21). No
   assignment of the 11 letter-cells to distinct tracks, positional or not, can
   read the cell value as an index into its assigned track.
5. Clue 2's string has exactly 15 capitals, its required answer length.
6. **The clue-2 image stores its text rotated 90 degrees.** Rotating it recovers
   the eight anagram words — TO LOWER SUBTRACT CAPITAL WITH ADDITION THE YOUR —
   displayed in scrambled order; their lengths sum to exactly 41, the string
   length, so they partition the string into eight segments (`tools/clue2_layout.py`).
7. **The clue-8 value-as-index pairing is impossible for every assignment** (the
   clue needs two titles of 18+ letters; the album has one). The "ENTR" signal
   from reverse indexing is the repo's old `len - v` family and silently drops
   5 of 12 cells.
8. Segment 4 now hinges on the 15-character clue-2 answer: 800k+ clue-2
   hypotheses (linear arithmetic, English words, album-indexed, layout-based)
   have been refuted against both pinned skies.

## Running the tools

```bash
pip install pycryptodome          # or pycryptodomex (the oracle falls back)
pip install ecdsa                 # public-key fallback when coincurve is absent

python3 tools/oracle.py --selftest                    # SELFTEST OK
python3 tools/oracle.py --segment 1 <imagine> <beach> # one pair, MATCH / NO MATCH
python3 tools/oracle.py --answers <a1> ... <a8>       # full verdict

gcc -O3 -march=native -o tools/sweep tools/sweep.c    # build the engine
tools/sweep test                                      # FIPS vector + full trace
tools/sweep 1 <template32> <mask32>                   # wave over a key space
```

Mask classes for `sweep`: `.` printable ASCII, `0` digits, `?` all bytes,
`r` mirror the byte 8 positions earlier, any other character = fixed.

## Provenance and attribution

- The puzzle, the clue images, and the prior analyst's `leads.md` / `tested.md` /
  `puzzle.json` / `UPSTREAM-README.md` come from
  [floflo777/open-crypto-puzzles](https://github.com/floflo777/open-crypto-puzzles)
  (`2-mid-prizes/path-to-greatness-treasure-hunt-3ltc`), which catalogues public
  crypto treasure hunts.
- The clue images are the puzzle author's own published files, served by
  `p2gtreasure.com` and delivered through its QR codes; they are included here
  for analysis only.
- Everything under `tools/` except `oracle.py`, and all findings in
  `analysis/SESSION-FINDINGS-2026-09-30.md`, were written in this analysis
  session and are the original work of this repository.

## Status

Open. No segment is solved. The clue poems are assembled from **song lyrics and
song titles**: clue 5 quotes **six** different prog/metal songs verbatim (line 2
= Vintersorg, "Astral and Arcane"; the other five from round 6), and lines 1/3
are the author's instruction. Clue 3's pointer graph is **exactly** 92 cells in
one closed cycle plus 4 one-step entry cells plus 4 numbered stars, and the
star-nearest pairing is one-to-one — but round 12 shows that pairing is a ~3%
chance property, that "cycle order" is an 8-member rotation family rather than a
single candidate, and that **clue 3 cannot be tested until clue 7 is**, since
segment 3's key is `clue3 ‖ clue7`. Clue 7 is therefore the bottleneck, and its
24-character length is a filter that rules out the quotation and name families
outright. Round 10's geography fit (three great-circle
distances from the three numerals) is **UNPROVEN**: round 11 shows all-km is
required by the numbers but contradicted by the measured `mi/km/mi` pennants,
that row 2 is post-hoc, and that the pictograms do not depict the sites; the
pixel re-check of the pennants is inconclusive. Rounds 8–9 closed clue 2's last
proposed families (the 26-non-capital alphabet key; the dash-group /
capital–lowercase pairing). Clue 5 cannot be oracle-tested alone (segment 2 needs
the chess half too), so the only place a real break can land is **segment 4**
(clue 2's 15-character answer). The most valuable next steps are a definitive
pennant measurement, naming the six pictograms against the six songs, and a
reading of clue 2 that none of the closed families touches.
