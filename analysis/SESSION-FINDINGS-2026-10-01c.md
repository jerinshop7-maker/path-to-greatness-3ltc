# Path to Greatness (3 LTC) — round 8, 2026-10-01

Fifth session. A pasted round-8 analysis proposed two concrete routes: (A) treat
clue 2's **26 non-capital cells** as an alphabet key, and (B) revive clue 5 as
**geographic distances between the songs' origins**. Both are now tested. One is
refuted; the other is weakened by arithmetic. New tools:
`tools/clue2_alphabet_key.py`, `tools/clue5_geo.py`. Oracle: `SELFTEST OK`.

---

## 1. Clue 2 — the "26 non-capitals = alphabet key" route: REFUTED (new family)

The structural fact is real and exact: the 41-cell string is **15 capitals +
26 non-capitals** (21 lowercase + 5 dashes). Every earlier clue-2 family used the
non-capitals as *context numbers* or moved characters; none treated the 26 cells
as an ordered alphabet the capitals index into.

That family is now swept (`tools/clue2_alphabet_key.py`): number the 26
non-capitals A..Z in reading order (and the 21 lowercase separately), take each
capital's key as one of 18 features (rank of the nearest non-capital before/
after, count before/after, distance, dash count, the non-capital's own letter
value, capital rank, raw index, ...), and form each letter as
`(capital value ± key + shift) mod 26` in both 1- and 0-based alphabets, plus
the pure-substitution reading and an ordering-key sort.

| Family | Space | Result |
|---|---|---|
| 26-non-capitals-as-alphabet key | **894 distinct 15-char candidates × 2 skies = 1,788 pairs** | **0** |

So the 26 is *exact but not yet a key*. The bottleneck on clue 2 is still a
non-arithmetic reading of the 15 capitals, and the "just count the non-capitals"
versions are now covered.

---

## 2. Clue 5 — the geographic revival is weakened by hard arithmetic

The pasted route: pair the six songs'/bands' **origin cities**, call the Roman
numerals distances, and treat the pennant as the direction. `tools/clue5_geo.py`
does the honest arithmetic.

**(a) The repo's unit reading is geometrically impossible.** The permissible
reading (formerly X2) is `mi / km / mi`. That makes row 1

```
12,772 mi = 20,554.5 km
```

but the **maximum great-circle distance anywhere on Earth is 20,015.1 km**
(πR, R = 6371.0088 km). Row 1 is **540 km beyond any surface distance on the
planet.** So under `mi/km/mi`, row 1 cannot be a great-circle distance at all —
which means either the pennant/unit assignment is not actually `mi/km/mi`, or the
numerals are not distances.

**(b) Read as all km, all three are possible** (12,772 / 5,210 / 12,061 km). That
is a self-consistency argument for *all-km* over `mi/km/mi`, and it reopens the
unit question the repo considered settled. It does **not** by itself confirm
anything.

**(c) No band-origin pair produces row 1 or row 3.** Scanning all 15 pairwise
great-circle distances between the six origin cities (Skellefteå, Germany,
Kitee, London, Nyack NY, Perth UK), in km and miles, **every value's closest
target is row 2 (5,210)** — nothing comes near row 1 or row 3:

| pair | distance | closest printed target |
|---|---|---|
| Nyack ↔ Perth | **5,185 km** | row 2 (5,210) |
| London ↔ Nyack | 5,538 km | row 2 |
| Skellefteå ↔ Nyack | 6,165 km | row 2 |
| Kitee ↔ London | 2,157 km | row 2 |
| (…all remaining pairs ≥ 1,000 km from any target…) | | |

And the same calculation with the *city-centre* endpoint the pasted text quotes,
NYC ↔ Perth, gives **5,219 km** (printed row 2 = 5,210 km) — a 9 km near-miss,
not exact. So a "six bands, three pairwise distances" model has **no candidate at
all for rows 1 and 3**, and at most one near-miss for row 2. That is a real
constraint, not a lead.

---

## 3. Corrections to the pasted round-8 text

| Pasted claim | Verdict |
|---|---|
| "Ghost Love Score = 6" | **Wrong.** Nightwish "Ghost Love Score" is **track 9** of *Once* (2004). The pasted text's own earlier section lists the right album but the track table in §4 says 6. |
| "five exact lyric quotations" with line 2 "upgraded" to confirmed | Consistent with round 7 — line 2 = Vintersorg "Astral and Arcane" is indeed confirmed. |
| "the mi/km/mi unit issue makes the old all-km interpretation invalid" | Reversed: the arithmetic here favours **all-km**, because `mi/km/mi` puts row 1 beyond the planet. |
| "5210 km is especially interesting" | Only a ~9–25 km near-miss, and it is the *only* row with any near-miss; see §2c. |
| "clue-2 26 non-capitals is the next route" | Tested and refuted (§1). |

---

## 4. Where this leaves the routes

```
SEGMENT 4  scramble(15) + sky(17)     <-- still the ONLY testable break
├── SKY    71520219618128920 ....... best
│          58112171456182114 ....... repo
└── SCRAMBLE  800k+ hypotheses, 0
    ├── arithmetic / running / linear ............ REFUTED
    ├── positional / rotation / keyboard ......... REFUTED
    ├── anagram permutation / ordering key ....... REFUTED
    ├── image highlight .......................... REFUTED
    ├── 26-non-capitals alphabet key ............. REFUTED (NEW, 1,788)
    └── ???  (non-arithmetic reading of the 15 capitals)

SEGMENT 2  chess(12) + wonders(20)    <-- NOT testable alone
├── WONDERS
│   ├── six lyric sources ...................... CONFIRMED
│   ├── "eight wonders" fork:
│   │      (a) New7Wonders + Giza .............. list ok, distances fail
│   │      (b) Archaic Reveries (8 tracks) ..... untested, author-controlled
│   ├── geography revival ...................... WEAKENED (§2): unit reading
│   │        makes row 1 impossible; no pair gives rows 1/3
│   └── pictograms ↔ songs ..................... still unverified
└── CHESS  flags / promotion .................. OPEN

SEGMENT 3  wasd(8) + ship(24)
├── 53214124 / 2415+1234 ...................... OPEN
└── ship (Titanic montage) .................... OPEN

SEGMENT 1  imagine(16) + beach(16)
├── beach = 15 notes + 1 convention ........... OPEN
└── imagine = lyric masquerade ................ OPEN
```

---

## 5. One-line status

Clue 2's last structural hope (the exact 26 non-capitals) is now a certified
negative (1,788 pairs, 0), and the clue-5 geography revival fails on arithmetic:
its own `mi/km/mi` units put row 1 540 km beyond the Earth's maximum distance,
and no band-origin pair supplies rows 1 or 3. Segment 4 (clue 2) remains the only
segment that can be oracle-tested, and therefore the only place a real break can
land; the most valuable remaining clue-5 test is the author-controlled
`Archaic Reveries` 8-track reading, which has not been tried.
