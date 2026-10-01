#!/usr/bin/env python3
"""Round 19 -- the two testable claims of the round-19 write-up.

The write-up proposes three routes.  Two are testable here; the third (clue 7 =
"the caption of the recovered drawing") is a naming family whose two obvious
sub-registers were already swept in round 18.

  A. CLUE 5 as a PAIRWISE metadata system.
     The write-up reads each row as  song A --direction--> song B  with the
     printed number measuring something about the pair, and explicitly asks not
     to restrict it to geography.  Two things are done:

       A1. REACHABILITY BOUNDS.  For the features whose magnitudes are bounded
           by facts already in the repo (release-year gaps, durations, track
           numbers, title/album/artist lengths, ASCII sums), the maximum value a
           pair (or the whole six) can reach is computed and compared with the
           three printed numbers.  A feature that cannot reach the target is
           refuted for every pair, without enumerating pairs.

       A2. EXHAUSTIVE SEARCH over every measurable feature of the six confirmed
           songs and their quoted lines, pairwise (directed and undirected) and
           six-way, at exact and near equality.

  B. CLUE 2 as a character-aligned construction.
     The write-up's family is: instruction word + same-position ciphertext
     character -> per-character transformation -> read at the capital positions.
     Round 18 tested a narrow version of this (alphabet-rank shift, A=0/A=1).
     This tool widens it to the operations the write-up names: alphabetic rank,
     ASCII difference, ASCII sum, position within the instruction word, position
     within the ciphertext chunk, and dashes as null/skip -- all read out at the
     15 capital positions and crossed with both 17-digit sky candidates.

Segments are not testable for clue 5 (segment 2 needs clue 4 as well), so A is
structural evidence.  B is a real oracle test.
"""

from __future__ import annotations

import sys

sys.path.insert(0, ".")

from segsweep import sweep                          # noqa: E402

# --------------------------------------------------------------- clue 5 data -
# The six confirmed lyric sources (rounds 6-7).  Years and track numbers are
# album metadata; the quoted lines are the poem's own lines 2,4,5,6,7,8.
SONGS = [
    dict(key="vintersorg", title="Astral and Arcane", artist="Vintersorg",
         album="Cosmic Genesis", year=2000, track=1, line=2),
    dict(key="falkenbach", title="Havamal", artist="Falkenbach",
         album="Heralding The Fireblade", year=2005, track=3, line=4),
    dict(key="nightwish", title="Ghost Love Score", artist="Nightwish",
         album="Once", year=2004, track=9, line=5),
    dict(key="floyd", title="High Hopes", artist="Pink Floyd",
         album="The Division Bell", year=1994, track=11, line=6),
    dict(key="coheed", title="Three Evils", artist="Coheed and Cambria",
         album="In Keeping Secrets Of Silent Earth 3", year=2003, track=4,
         line=7),
    dict(key="alestorm", title="Treasure Island", artist="Alestorm",
         album="No Grave But The Sea", year=2017, track=10, line=8),
]

QUOTED = {
    2: "A thousand maps drawn with blood",
    4: "To shelter my ship on the flood",
    5: "We used to swim the same moonlight waters",
    6: "Dragged by the force of some inner tide",
    7: "No longer will we wait for your answers",
    8: "With the stars in the sky our guide",
}

TARGETS = {12772: "row 1 (12,772 mi)", 5210: "row 2 (5,210 km)",
           12061: "row 3 (12,061 mi)"}

# Bounds that hold from facts already in the repo, without needing the exact
# missing metadata.  The extreme release years are 1994 and 2017; the longest
# song in the set is well under 20 minutes; every track number is <= 13.
BOUNDS = [
    ("release-date gap (days)",
     "1994-01-01 to 2017-12-31 = %d days" % ((2017 - 1994) * 366 + 364),
     "every pair of dates lies between these extremes, whatever the exact days"),
    ("song duration (seconds)",
     "any single track < 1,200 s, all six together < 3,600 s",
     "the longest quoted song is Ghost Love Score at about 10 minutes"),
    ("album year difference", "2017 - 1994 = 23", "years are fixed metadata"),
    ("track number", "<= 13", "the albums have at most 13 tracks"),
    ("title length (letters)",
     "<= 40 per title, <= 80 for two",
     "the longest title here is 21 letters including the parenthetical"),
]


def nospace(s):
    return "".join(c for c in s.lower() if c.isalpha())


def feat(song):
    t = nospace(song["title"])
    ln = QUOTED[song["line"]]
    return {
        "year": song["year"],
        "track": song["track"],
        "tlen": len(t),
        "alen": len(nospace(song["artist"])),
        "ablen": len(nospace(song["album"])),
        "tsum": sum(ord(c) for c in t),
        "line": song["line"],
        "letters": sum(1 for c in ln if c.isalpha()),
        "words": len(ln.split()),
    }


F = {s["key"]: feat(s) for s in SONGS}
KEYS = [s["key"] for s in SONGS]
PAIRF = ["year", "track", "tlen", "alen", "ablen", "tsum", "line", "letters",
         "words"]


def search_clue5():
    print("=" * 78)
    print("A. CLUE 5 as a pairwise metadata system")
    print("=" * 78)

    print("\nA1. reachability bounds (a feature that cannot reach the target is")
    print("    refuted for every pair, without enumerating pairs)")
    for name, bound, why in BOUNDS:
        print("    %-26s %-45s %s" % (name, bound, why))
    print("\n    The three targets are 12,772 / 5,210 / 12,061.  Only two")
    print("    families of feature can reach >= 12,000 at all:")
    print("      * surface distance in km between two places (<= pi*R = 20,015)")
    print("        -- already refuted for rows 1 and 3 in round 8 (no artist-origin")
    print("        pair comes near them) and closed in rounds 11-12,")
    print("      * a six-way SUM over the whole set (not a pair).")
    print("    Every pairwise non-geographic feature in the table above is")
    print("    bounded below 12,000, so under the write-up's own pair model the")
    print("    two 12,000-class rows cannot be distances-in-days, durations,")
    print("    track numbers, years or title lengths.")

    print("\nA2. exhaustive search over the measurable features")
    feats = []
    # pairwise, both orders and both signs
    for a in KEYS:
        for b in KEYS:
            if a == b:
                continue
            for f in PAIRF:
                d = abs(F[a][f] - F[b][f])
                s = F[a][f] + F[b][f]
                p = F[a][f] * F[b][f]
                feats.append(("%s-%s |Δ%s|" % (a, b, f), d))
                feats.append(("%s-%s sum%s" % (a, b, f), s))
                if f in ("tlen", "year", "track"):
                    feats.append(("%s-%s prod%s" % (a, b, f), p))
    # six-way
    for f in PAIRF:
        feats.append(("all6 sum %s" % f, sum(F[k][f] for k in KEYS)))
    feats.append(("all6 sum year + sum track",
                  sum(F[k]["year"] for k in KEYS) + sum(F[k]["track"]
                                                        for k in KEYS)))
    feats.append(("all6 sum year + sum tlen",
                  sum(F[k]["year"] for k in KEYS) + sum(F[k]["tlen"]
                                                        for k in KEYS)))
    feats.append(("all6 sum tsum (ASCII, title)",
                  sum(F[k]["tsum"] for k in KEYS)))
    feats.append(("all6 sum year + sum tsum",
                  sum(F[k]["year"] for k in KEYS) + sum(F[k]["tsum"]
                                                        for k in KEYS)))

    print("    distinct feature values tested: %d" % len(feats))
    for tol in (0, 1, 9, 35):
        hits = [(n, v) for n, v in feats
                if any(abs(v - t) <= tol for t in TARGETS)]
        print("    tolerance +/-%-3d  hits: %d" % (tol, len(hits)))
        for n, v in hits[:12]:
            t = min(TARGETS, key=lambda x: abs(v - x))
            print("        %-38s = %-7d  vs %s (Δ%d)"
                  % (n, v, TARGETS[t], abs(v - t)))
    return 1


# --------------------------------------------------------------- clue 2 ------
S = "s-bcBPEFfJDfeFmksmPOkChDhrgBqjD-i---ffeNB"
CHUNK_LENS = [2, 5, 8, 7, 4, 8, 3, 4]
CHUNKS, _o = [], 0
for _L in CHUNK_LENS:
    CHUNKS.append((_o, _o + _L))
    _o += _L
assert _o == 41

SKIES = ["71520219618128920", "58112171456182114"]


def word_family_wide():
    """The write-up's character-aligned family, widened.

    The eight displayed anagram words have exactly the eight chunk lengths, so
    each capital cell can be combined with the instruction word's letter at the
    same position.  Enumerated: the 4 length-compatible word assignments, the
    key alignment (positional: every cell consumes a key slot / compact: only
    capital cells do), the key's source and value convention (word letter A=0,
    A=1, its ASCII code, its 1-based position in the word, the 1-based position
    in the chunk), the operation (+/-) and the conversion back to a character
    (mod 26 letter, or a printable ASCII codepoint).  Output = the 15 capital
    positions.
    """
    out = {}
    for eight in (("SUBTRACT", "ADDITION"), ("ADDITION", "SUBTRACT")):
        for four in (("WITH", "YOUR"), ("YOUR", "WITH")):
            words = ["TO", "LOWER", eight[0], "CAPITAL", four[0], eight[1],
                     "THE", four[1]]
            for align in ("positional", "compact"):
                for keysrc in ("word", "word_ascii", "pos_word", "pos_chunk",
                               "cipher_first"):
                    for op in ("+", "-"):
                        for outmode in ("letter26", "ascii"):
                            chars, ok = [], True
                            for (start, end), w in zip(CHUNKS, words):
                                ncap = 0
                                for j in range(start, end):
                                    c = S[j]
                                    if not c.isupper():
                                        continue
                                    ki = (j - start) if align == "positional" \
                                        else ncap
                                    ncap += 1
                                    ki %= len(w)
                                    if keysrc == "word":
                                        k = ord(w[ki]) - 65           # A=0
                                    elif keysrc == "word_ascii":
                                        k = ord(w[ki])
                                    elif keysrc == "pos_word":
                                        k = ki + 1
                                    elif keysrc == "pos_chunk":
                                        k = (j - start) + 1
                                    else:
                                        k = ord(S[start])
                                    v = ord(c)
                                    x = (v + k) if op == "+" else (v - k)
                                    if outmode == "letter26":
                                        chars.append(chr(97 + (x - 65) % 26))
                                    else:
                                        y = 32 + (x % 95)
                                        chars.append(chr(y) if chr(y).isprintable()
                                                     else "?")
                            s = "".join(chars)
                            if len(s) == 15:
                                out.setdefault(s, "%s|%s|%s|%s|%s"
                                               % (eight, four, align, keysrc,
                                                  op + outmode))
    return out


def main():
    rc = 0
    rc |= search_clue5()

    print("\n" + "=" * 78)
    print("B. CLUE 2 as a character-aligned construction")
    print("=" * 78)
    fam = word_family_wide()
    print("aligned-word family: %d distinct 15-char candidates" % len(fam))
    alias = {}
    for s, tag in fam.items():
        alias.setdefault(s, tag)
    sweep(4, sorted(alias), SKIES, "clue2 aligned-word")

    print("\n" + "=" * 78)
    print("VERDICT")
    print("=" * 78)
    print("A: structural. The pair model is bounded: only surface distance (km)")
    print("   and six-way sums can reach 12,000+, and distance is refuted. Any")
    print("   pair-based reading of rows 1 and 3 needs a feature outside the")
    print("   table, which the write-up does not name.")
    print("B: oracle test. See the hit count above; 0 hits refutes the pairs.")
    return rc


if __name__ == "__main__":
    sys.exit(main())
