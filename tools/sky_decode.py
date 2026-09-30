#!/usr/bin/env python3
"""Comprehensive clue 8 (sky) decoder with the REAL 13-track list.

Certified facts:
  * the string is ehk-bqNEFRUn- (13 cells; dashes at cells 4 and 13, 1-based)
  * answer length 17
  * rule examples: 4 -> Exit Light -> T ; 8 -> Ghost March -> R
  * album: 1 Few and Far Between, 2 The Suffocating Carrier, 3 The Surrogate,
    4 Exit Light, 5 Ghost March, 6 Nocturnal Sugars, 7 All Art Must Die,
    8 Daylight Brings, 9 Hills of Life, 10 As Seen From Afar,
    11 The Great Adventure, 12 Sequels, 13 Seconds of Dream
"""
import itertools

TRACKS = ["fewandfarbetween", "thesuffocatingcarrier", "thesurrogate",
          "exitlight", "ghostmarch", "nocturnalsugars", "allartmustdie",
          "daylightbrings", "hillsoflife", "asseenfromafar",
          "thegreatadventure", "sequels", "secondsofdream"]

CELLS = "ehk-bqNEFRUn-"
letters = [(i, c) for i, c in enumerate(CELLS) if c != "-"]
print("cells:", CELLS, "letters:", "".join(c for _, c in letters))
vals = [(i, ord(c.upper()) - 64) for i, c in letters]
print("cell values (alphabet positions):", vals)

ALPHA = set("abcdefghijklmnopqrstuvwxyz")


def opts(i, v):
    """all candidate letters for cell i with value v under common rules"""
    out = []
    for ti, t in enumerate(TRACKS):
        for mode, idx in (("1based", v - 1), ("0based", v), ("end", len(t) - v),
                          ("end0", len(t) - v - 1)):
            if 0 <= idx < len(t):
                out.append((ti + 1, mode, t[idx]))
    return out


# ---- 1. per-cell same track with 1:1 offset (both directions, 0/1-based) ----
print("\n-- 1:1 cell->track with offset (letters only, tracks in order) --")
for offset in range(-3, 4):
    for base in (1, 0):
        word, ok = [], True
        picks = []
        for cell_i, v in vals:
            ti = cell_i + offset
            if not (0 <= ti < 13):
                ok = False
                break
            t = TRACKS[ti]
            idx = v - base
            if not (0 <= idx < len(t)):
                ok = False
                break
            picks.append((ti + 1, t, v, t[idx]))
            word.append(t[idx])
        if ok:
            print("offset %+d base %d: %s   %s" % (offset, base, "".join(word), picks))

# ---- 2. all increasing injections of the 11 cells into 13 tracks ----
print("\n-- increasing injections (choose 11 of 13 tracks) --")
count = 0
for tracks_used in itertools.combinations(range(13), 11):
    for base in (1, 0):
        word, ok = [], True
        for (cell_i, v), ti in zip(vals, tracks_used):
            t = TRACKS[ti]
            idx = v - base
            if not (0 <= idx < len(t)):
                ok = False
                break
            word.append(t[idx])
        if ok:
            count += 1
            w = "".join(word)
            print("tracks %s base %d -> %s" % ([t + 1 for t in tracks_used], base, w))
print("total valid injections:", count)

# ---- 3. digits split into 13 values, but 0-based and with dashes as cells ----
print("\n-- digit split (58112171456182114) into 13 values, 0-based --")
DIGITS = "58112171456182114"
found = 0
for combo in itertools.combinations(range(1, 17), 4):
    vals2, pos, ok = [], 0, True
    for k in range(13):
        two = pos in combo
        v = int(DIGITS[pos:pos + (2 if two else 1)])
        pos += 2 if two else 1
        vals2.append(v)
    if pos != 17:
        continue
    for base in (1, 0):
        word, ok = [], True
        for k, v in enumerate(vals2):
            t = TRACKS[k]
            idx = v - base
            if not (0 <= idx < len(t)):
                ok = False
                break
            word.append(t[idx])
        if ok:
            found += 1
            print("split %s base %d -> %s" % (vals2, base, "".join(word)))
print("valid 13-way splits:", found)

# ---- 4. the 17 digits as single indexes into the concatenated album ----
print("\n-- 17 digits as 1-based positions in the joined album --")
album = "".join(TRACKS)
print("album length:", len(album))
for d in DIGITS:
    i = int(d) - 1
    print(d, "->", album[i] if 0 <= i < len(album) else "?", end="  ")
print()

# ---- 5. the 17 digits as positions in the FIRST track only (18 letters) ----
print("\n-- 17 digits as positions in 'fewandfarbetween' (18 letters) --")
t1 = TRACKS[0]
print("".join(t1[int(d) - 1] if 0 < int(d) <= len(t1) else "?" for d in DIGITS))
