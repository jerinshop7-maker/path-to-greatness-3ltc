# Path to Greatness (3 LTC) — round 10, 2026-10-01

Seventh session. **Headline: the three Roman numerals match three great-circle
distances between famous sites to within ~0.3%, under the all-km reading.** This
is the first numeric fit of 12,772 / 5,210 / 12,061 anyone has produced, and it
revives the "eight wonders" as a real, if still incomplete, geographic layer.
New/updated tool: `tools/clue5_wonders.py`. Oracle: `SELFTEST OK`.

---

## 1. THE FIT

Using the canonical eight wonders (New7Wonders + the Great Pyramid) for rows 1
and 3, and a fixed wider site pool for row 2:

| row | printed | site pair | great-circle | error |
|---|---|---|---|---|
| 1 | **12,772 km** | Great Wall (Badaling) ↔ Chichén Itzá | 12,738.1 km | −33.9 km (**0.27%**) |
| 2 | **5,210 km** | Angkor Wat ↔ Uluru | 5,219.1 km | +9.1 km (**0.18%**) |
| 3 | **12,061 km** | Machu Picchu ↔ Great Pyramid of Giza | 12,037.5 km | −23.5 km (**0.20%**) |

That uses **exactly six sites** — Great Wall, Chichén Itzá, Angkor Wat, Uluru,
Machu Picchu, Giza — matching the **six non-triangle pictograms** one-for-one in
count. Rows 1 and 3 come from the *small canonical-eight pool* (28 pairs), which
is what makes them meaningful; the row-2 pair needs a site outside the canonical
seven, so it is a weaker, partly-searched fit.

**Why the repository's earlier sweep missed it.** Round 5's correction X2 read
the pennant units as `mi / km / mi`. Under that reading the same search gives

```
row1 target 20,554 km -> best Great Wall <-> Christ the Redeemer = 17,301 km (off 15.8%)
row3 target 19,411 km -> best Great Wall <-> Christ the Redeemer = 17,301 km (off 10.9%)
```

i.e. nothing. Round 8 had already shown the `mi/km/mi` reading makes row 1
*geometrically impossible* (20,554 km > Earth's 20,015 km maximum), so the
self-consistent reading is **all-km** — and under all-km the three distances fall
into place. The unit question was the blocker, not the geography.

## 2. Coordinate sensitivity (the errors are within ambiguity)

The Great Wall runs ~2,500 km, so its "point" is arbitrary:

```
Badaling 12,738.1 | Mutianyu 12,738.1 | Jinshanling 12,688.4
Simatai  12,691.6 | Shanhaiguan 12,654.9 | Jiayuguan 13,252.6
```

Badaling gives the printed value to 0.27%; the exact point is under the author's
control, so a 34 km gap is not a defect. Machu Picchu ↔ Giza (12,037.5 vs
12,061) and Angkor Wat ↔ Uluru (5,219.1 vs 5,210) are fixed-coordinate and land
within 0.20% / 0.18%.

## 3. What this does NOT yet give

- **The pictogram ↔ site mapping is unresolved.** The eye-read pictograms
  (headstone+heart, flowering sprig, anchor, horned beast head, horned mask,
  star-?-star) do not obviously depict Great Wall / Chichén / Angkor / Uluru /
  Machu / Giza. Either the drawings are stylised, or they first identify the six
  *songs* and the songs lead to the sites.
- **The distance → 20-character extraction is unknown.** Knowing the three
  distances does not by itself produce 20 lowercase letters. Candidate next
  layers: the six site names (or their countries/continents) with the distances
  as letter indices; the eight wonders as a longer list needing two more sites.
- **No oracle check exists.** Segment 2 (chess + wonders) has no independent
  half, so this is structural evidence, not a 64-bit break. It is, however, the
  best-evidenced clue-5 result to date.

## 4. Statistical honesty

Within the 28 canonical-eight pairs, the chance a pair lands within ±35 km of a
specific ~12,000-km target is ≈ 28 · 70/16,600 ≈ 0.12; observing such a match for
*both* row 1 and row 3 has p ≈ 0.02–0.03. That is suggestive, not conclusive. The
row-2 match was found in a larger pool and is therefore weaker on its own; it is
included because it completes the six-site count and is the tightest of the
wider-pool hits.

## 5. Route tree (round 10)

```
SEGMENT 2  chess(12) + wonders(20)          <-- NEW best clue-5 lead
├── WONDERS
│   ├── poem = six-song lyric collage ....... CONFIRMED
│   ├── THREE NUMERALS = site distances ..... PROMISING (all-km, ≤0.3%)
│   │        Great Wall <-> Chichen Itza  (12,738 vs 12,772)
│   │        Angkor Wat <-> Uluru         ( 5,219 vs  5,210)
│   │        Machu Picchu <-> Giza        (12,037 vs 12,061)
│   ├── pictogram <-> six sites ............. NEXT (needs eyes)
│   ├── distance -> 20 chars ................ NEXT (mechanism unknown)
│   └── unit question ...................... RESOLVED toward all-km (r8,r10)
└── CHESS  14 pieces -> 12 chars, case kept ... OPEN

SEGMENT 4  scramble(15) + sky(17)          <-- ONLY oracle-testable break
├── SKY  71520219618128920 / 58112171456182114
└── SCRAMBLE  every proposed family REFUTED (incl. r8 alphabet key, r9 dashes)

SEGMENT 3  wasd(8) + ship(24) ............. OPEN
SEGMENT 1  imagine(16) + beach(16) ........ OPEN
```

## 6. One-line status

The clue-5 numerals now fit three real site distances to ≤0.3% under a consistent
all-km reading, using exactly six sites for the six pictograms — the first
numeric foothold on clue 5, and the reason the old sweep failed (the `mi/km/mi`
unit reading). The remaining clue-5 work is naming the pictograms and finding the
distance → 20-character extraction; segment 4 (clue 2) stays the only place a
64-bit break can land.
