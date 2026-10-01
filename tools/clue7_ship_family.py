#!/usr/bin/env python3
"""Clue 7 (`ship`, 24 characters) — candidate families from the RETRIEVED file.

Route A2 of round 14 is executed here. `clues/qr2.jpg` was decoded, the redirect
followed, and `clues/Ship.png` recovered (1920x1080 RGBA, alpha uniformly 255,
G and B identical). Its own poem reads, read directly off the file this session:

    A red sky at night
    Not the least bit significant
    A channel for light
    And a ship so magnificent

    The cold, dark night
    Moves towards its maker
    The vast, frigid ocean
    The great undertaker

so "the least bit" of "a red ... channel" is the red LSB plane -- confirmed
numerically (red plane 0 is the only structured low plane, ink fraction 0.250,
against 0.498/0.501/0.511 for planes 1-3).

CORRECTION to rounds 13 and 14: the montage's middle element is NOT "deck plans".
On the recovered plane it is a ship's hull going down by the bow with the
foremast and rigging above it -- the Titanic itself. Every description family
built on "and ... deckplans" was therefore aimed at the wrong picture, which is
the likely reason all nine of those strings failed.

The 24-character length now does real work. Three name groups sum to exactly 24:

    ismay(5) + andrews(7) + smith(5) + titanic(7)     = 24
    jonathan(8) + hyde(4) + victor(6) + garber(6)     = 24
    ismay(5) + andrews(7) + captain(7) + titanic(7)   = 26  (too long)

So the first two admit 4! = 24 orderings each, all automatically the right
length. This tool enumerates those and the surrounding register, and sweeps them
against every clue-3 reading that survives round 14.
"""
import itertools
import sys

sys.path.insert(0, ".")
from clue3_ship_cross import CYC, ROOTS, SRC, STAR, ENTRY, CYCSTR, root_token
from segsweep import sweep
from wasd_grid import cell


def clue3_readings():
    """The round-13/14 clue-3 side, all confirmed-reproducing."""
    out = set()
    out.add("".join(root_token(i) for i in ROOTS))          # d3w1as24
    out.add("".join(str(cell(i)[0]) for i in ROOTS))         # 53214124
    out.add("".join(cell(i)[1].lower() for i in SRC)
            + "".join(str(cell(i)[0]) for i in ROOTS if cell(i)[1] == "*"))
    # the four coordinate-index letters, as route 4 proposes
    out.add("".join(CYCSTR[i] for i in sorted(ROOTS)))
    return sorted(s for s in out if len(s) == 8)


def perms(words):
    return sorted({"".join(p) for p in itertools.permutations(words)})


def ship_family():
    fams = {}

    # --- the two exact-24 name groups -------------------------------------
    fams["names4"] = perms(["ismay", "andrews", "smith", "titanic"])
    fams["actors4"] = perms(["jonathan", "hyde", "victor", "garber"])

    # --- three names + a ship word, filtered to exactly 24 -----------------
    def sized(wordsets):
        out = set()
        for ws in wordsets:
            for p in itertools.permutations(ws):
                s = "".join(p)
                if len(s) == 24:
                    out.add(s)
        return sorted(out)

    people = ["ismay", "andrews", "smith", "hyde", "garber", "victor",
              "jonathan", "captain", "officer", "iceberg"]
    boats = ["titanic", "ship", "liner", "sink", "founder", "sinking"]
    combos = []
    for a, b in itertools.combinations(people, 2):
        for c in boats:
            combos.append((a, b, c))
            for conj in ("and",):
                combos.append((a + conj, b, c))
                combos.append((a, b + conj, c))
    fams["people2+boat"] = sized(combos)

    # --- register the recovered image actually supports ---------------------
    more = [
        # the ship is the subject of stanza 1 line 4
        "ismayandrewssmithtitanic", "andrewssmithismaytitanic",
        "titanicismayandrewssmith", "smithandrewsismaytitanic",
        "ismayandrewsthegreattitanic", "thebowgoesdownontitanic",
        "titanicbowdownicebergsink", "andrewssmithatthebowoftitanic",
        "ismayandrewssmithontitanic", "andrewssmiththeicebergship",
        "theuniqueshipoftitanic", "unsinkableshipicebergfounder",
        "twoofficerswatchtitanic", "ismayandrewslookattitanic",
        "andrewssmiththevanishingst", "theicebergandthetitanicshi",
        "andrewsknowsitsgonnafound", "ismayandrewssmithseeitfound",
    ]
    fams["prose"] = sorted({s for s in more if len(s) == 24})

    return {k: v for k, v in fams.items() if v}


def main():
    c3 = clue3_readings()
    print("clue-3 readings (all reproduce): %d" % len(c3))
    for s in c3:
        print("   %s" % s)
    print()

    fams = ship_family()
    total = 0
    hit = False
    for name, lst in fams.items():
        bad = [s for s in lst if len(s) != 24]
        print("[%s] %d strings, all exactly 24 chars: %s%s"
              % (name, len(lst), not bad,
                 ("  DROPPED %d" % len(bad)) if bad else ""))
        for s in lst[:12]:
            print("    %s" % s)
        if len(lst) > 12:
            print("    ... and %d more" % (len(lst) - 12))
        res = sweep(3, c3, lst, name)
        total += len(lst) * len(c3)
        if res:
            hit = True
    print()
    print("TOTAL PAIRS: %d   HITS: %s" % (total, "YES" if hit else "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())