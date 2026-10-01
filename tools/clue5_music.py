#!/usr/bin/env python3
"""Clue 5, round 7: the music layer, made explicit.

Three things this tool does:

(A) Records the *verified* source table for clue 5's lyric collage. Line 2 is
    newly confirmed here as Vintersorg's "Astral and Arcane" (Cosmic Genesis,
    2000); SESSION-FINDINGS-2026-10-01 had it as "unidentified", but the
    astronomy-forum hit it cites is that forum *quoting these very lyrics*.
    Lines 1 and 3 get no lyric hit in any phrasing tried, so they are almost
    certainly the author's instruction, not quotes.

(B) Records the author's *second* album, "Archaic Reveries" (2018), which has
    exactly 8 tracks -- the first concrete candidate for line 1's "eight
    wonders". Clue 8 already uses the author's first album as its dictionary.

(C) Runs the only oracle-checkable experiment this material offers: music-derived
    15-character strings tested as the clue-2 answer against segment 4 with both
    pinned skies. Clue 5 itself cannot be oracle-tested (segment 2 needs the
    chess half as well), so this is the honest use of the music corpus.
"""
import sys

sys.path.insert(0, "tools")
from oracle import segment_oracle  # noqa: E402

# --- (A) clue 5's verified lyric sources, in POEM-LINE order --------------
SONGS = [
    (2, "Vintersorg", "Astral and Arcane", "Cosmic Genesis", 2000, 1),
    (4, "Falkenbach", "Havamal", "Heralding - The Fireblade", 2005, 3),
    (5, "Nightwish", "Ghost Love Score", "Once", 2004, 9),
    (6, "Pink Floyd", "High Hopes", "The Division Bell", 1994, 11),
    (7, "Coheed and Cambria", "Three Evils", "In Keeping Secrets of Silent Earth: 3", 2003, 4),
    (8, "Alestorm", "Treasure Island", "No Grave But the Sea", 2017, 10),
]
# lines 1 and 3 have NO lyric hit in any phrasing tried (checked 2026-10-01)
INSTRUCTIONS = [1, 3]

POEM = [
    "charting the eight wonders",
    "a thousand maps drawn with blood",
    "a bit of help from each line",
    "to shelter my ship on the flood",
    "we used to swim the same moonlight waters",
    "dragged by the force of some inner tide",
    "no longer will we wait for your answers",
    "with the stars in the sky our guide",
]

# --- (B) the author's own two albums ------------------------------------
SECONDS = ["few and far between", "the suffocating carrier", "the surrogate",
           "exit light", "ghost march", "nocturnal sugars", "all art must die",
           "daylight brings", "hills of life", "as seen from afar",
           "the great adventure", "sequels", "seconds of dream"]           # 13
ARCHAIC = ["age of lamps", "lost and found", "welcome to the mansion", "effugium",
           "on the other side", "alone", "seven miles", "the regents"]       # 8


def norm(s):
    return "".join(c for c in s.lower() if c.isalnum())


def show():
    print("clue 5 lyric-collage sources (poem-line order):")
    print("  ln artist              song                    album                              year track")
    for ln, art, song, alb, yr, tr in SONGS:
        print("  %2d %-20s %-23s %-33s %4d %4d" % (ln, art, song, alb, yr, tr))
    print("  lines %s: no lyric hit (instructions)" % INSTRUCTIONS)
    print()
    print("author's own albums (line 8 & 1 candidate 'eight wonders'):")
    print("  Seconds of Dream (2021): %d tracks" % len(SECONDS))
    print("  Archaic Reveries (2018): %d tracks -> %s" % (len(ARCHAIC), ", ".join(ARCHAIC)))
    print()

    # album-initial wordplay available from the six confirmed quotes
    alb_init = "".join(norm(alb)[0].upper() if not norm(alb)[0].isdigit()
                       else "?" for _, _, _, alb, _, _ in SONGS)
    title_init = "".join(norm(song)[0].upper() for _, _, song, _, _, _ in SONGS)
    print("album  initials in line order 2,4,5,6,7,8:", alb_init)
    print("title  initials in line order 2,4,5,6,7,8:", title_init)
    print("  (a 6-letter core; any 8-letter reading needs the two instruction lines)")
    print()

    # the three Roman numerals in the image
    nums = [("12,772", 12772), ("5,210", 5210), ("12,061", 12061)]
    print("the three Roman numerals and cheap numeric facts:")
    for lab, n in nums:
        ds = sum(int(c) for c in str(n))
        print("  %-7s digitsum=%2d  mod26=%2d->%s  factors=%s" %
              (lab, ds, n % 26, chr(n % 26 + 64),
               "*".join(str(p) for p in prime_factors(n))))
    print()


def prime_factors(n):
    f, d = [], 2
    while d * d <= n:
        while n % d == 0:
            f.append(d)
            n //= d
        d += 1
    if n > 1:
        f.append(n)
    return f


# --- (C) oracle-checkable: music 15-char strings vs segment 4 ------------
SKIES = {"witness": "71520219618128920", "repo": "58112171456182114"}


def candidates():
    """15-char lowercase-alnum strings drawn from the music corpus."""
    corpus = []
    for _, art, song, alb, _, _ in SONGS:
        corpus += [art, song, alb]
    corpus += SECONDS + ARCHAIC
    out = {}
    for phrase in corpus:
        s = norm(phrase)
        # the phrase itself, and every 15-window of its full normalisation
        for start in range(0, max(1, len(s) - 14)):
            w = s[start:start + 15]
            if len(w) == 15 and w.isalpha():
                out.setdefault(w, phrase)
    # joined-corpus windows (music words run together)
    joined = "".join(norm(p) for p in corpus)
    for start in range(len(joined) - 14):
        w = joined[start:start + 15]
        if w.isalpha():
            out.setdefault(w, "joined:%d" % start)
    return out


def main():
    show()
    cands = candidates()
    print("music-derived 15-char candidates:", len(cands))
    for w in sorted(cands)[:20]:
        print("   ", w, "<-", cands[w])
    if len(cands) > 20:
        print("    ...")
    hits = tested = 0
    for sc, src in cands.items():
        for sky, kn in SKIES.items():
            tested += 1
            r = segment_oracle(4, (sc + sky).encode())
            if r:
                hits += 1
                print("MATCH!!! clue2=%s (%s) sky=%s (%s) -> %s" % (sc, src, sky, kn, r.hex()))
    print("tested %d pairs, hits %d" % (tested, hits))
    if hits == 0:
        print("=> the music corpus does not supply clue 2's answer in this family.")
        print("=> clue 5's extraction is NOT oracle-testable (segment 2 needs clue 4 too).")


if __name__ == "__main__":
    main()
