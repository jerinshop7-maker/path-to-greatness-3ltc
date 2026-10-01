#!/usr/bin/env python3
"""Clue 3, round 12: an audit of the *graph structure* argument, not a new reading.

Round 11 was spent on clue 5.  This tool checks the round-12 claim that clue 3's
100-cell pointer graph is "deliberately constructed" in a way that isolates four
exceptional cells, and that pairing the four numbered stars with them by proximity
yields an 8-character clue answer.

WHAT IS VERIFIED HERE (reproducible, from the repo's own transcription):
  1. The 92-cycle / 4 entry cells / 4 stars decomposition is exactly right.
  2. Every entry cell's successor lies inside the cycle, one step in.
  3. The nearest-entry pairing is UNIQUE and a PERFECT MATCHING under both
     Manhattan and Euclidean distance, so the pairing is not a metric artefact.
  4. Star order 1,2,3,4 -> 2W,1S,5D,4A -> "2w1s5d4a" (or "w2s1d5a4" letter-first).

WHAT THIS TOOL ALSO SHOWS, AGAINST the round-12 enthusiasm:
  5. The perfect-matching property is NOT rare.  Over 200k random placements of
     4 stars and 4 entries on the 10x10 grid, a one-to-one nearest pairing occurs
     ~6% of the time and a perfect-matching-AND-all-unique pairing ~3.3% of the
     time.  So the bijection is a mild coincidence, not a fingerprint of design.
  6. "Cycle order" is NOT well defined.  Nothing privileges a starting cell on
     the 92-cycle, so it yields 4 rotations plus their reversals = 8 distinct
     8-char candidates, not 1.  The round-12 candidate a4d5w2s1 is the forward
     rotation starting at 4A; picking it needs an argument the puzzle has not
     given.
  7. Letter-first vs number-first ("w2s1d5a4" vs "2w1s5d4a") is unforced.  The
     grid writes number first, so the string as-the-cells-read is 2w1s5d4a.
  8. SUPERSEDED by round 13.  The nearest-star rule in section 3 is an operation
     the clue never states, so it is not needed at all: reading the SAME eight
     root cells in row-major order and keeping the letter for an arrow-root and
     the number for a star-root gives d3w1as24 directly.  See
     tools/clue3_root_encoding.py.  The pairing above is retained only as a
     record of the route that was tried.

THE DECISIVE POINT (section 8):
  Neither candidate can be tested.  Segment 3's AES key is clue3 || clue7 =
     8 + 24 = 32 bytes.  tools/oracle.py requires BOTH halves; there is no
     per-clue oracle.  So the round-12 plan "test w2s1d5a4 / a4d5w2s1 first"
     is not executable -- clue 7 must be solved before either string can be
     refuted, let alone confirmed.  Any candidate list that stops at clue 3 is
     untested, and an untested list must not be reported as a breakthrough.

Every number above is printed so a reader can disagree independently.
"""

import random
import sys

from wasd_grid import N, build, cell, rc, succ

# Transcribed positions (0-indexed flat).
ENTRY = {              # the four cells with a successor but no predecessor
    (0, 1): "5D",
    (3, 8): "2W",
    (7, 9): "4A",
    (8, 0): "1S",
}
STAR = {1: (4, 6), 2: (8, 2), 3: (1, 3), 4: (8, 8)}
STAR_PAIR = {1: "2W", 2: "1S", 3: "5D", 4: "4A"}


def flat(rc_):
    return rc_[0] * N + rc_[1]


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def euclid(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def walk_cycle(out, start):
    cyc = [start]
    j = out[start]
    while j != start:
        cyc.append(j)
        j = out[j]
    return cyc


def section(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def main():
    out, ind = build()

    section("[1] THE GRAPH DECOMPOSITION (confirmed)")
    stars = [flat(p) for p in STAR.values()]
    entries = [flat(p) for p in ENTRY]
    print("cells                       : %d" % (N * N))
    print("cells with no successor     : %d  (the four numbered stars)"
          % sum(1 for i in range(N * N) if out[i] is None))
    print("cells with no predecessor  : %d  (4 stars + 4 entry cells)"
          % sum(1 for i in range(N * N) if i not in ind))
    cyc = walk_cycle(out, succ(entries[0]))
    print("longest cycle               : %d cells" % len(cyc))
    print("100 - 92 = 8 = 4 entries + 4 stars   -> the split is exact")

    section("[2] EACH ENTRY CELL ENTERS THE CYCLE IN ONE STEP")
    for (r, c), lab in ENTRY.items():
        i = flat((r, c))
        s = succ(i)
        print("  r%dc%d = %s -> r%dc%d   (cycle position %d)"
              % (r + 1, c + 1, lab, rc(s)[0] + 1, rc(s)[1] + 1, cyc.index(s)))

    section("[3] STAR -> NEAREST ENTRY CELL")
    for name, metric in (("manhattan", manhattan), ("euclidean", euclid)):
        print("  metric = %s" % name)
        targets = []
        for n in (1, 2, 3, 4):
            sp = STAR[n]
            ds = sorted((metric(sp, e_rc), ENTRY[e_rc]) for e_rc in ENTRY)
            (d0, lab0), (d1, _) = ds[0], ds[1]
            targets.append(lab0)
            print("    star %d (r%dc%d) -> %s   d=%.4g  runner-up %.4g  %s"
                  % (n, sp[0] + 1, sp[1] + 1, lab0, d0, d1,
                     "UNIQUE" if d0 < d1 else "TIE"))
        bij = len(set(targets)) == 4
        print("    one-to-one across all four stars: %s" % ("YES" if bij else "no"))
        print("    matches the claimed 2W/1S/5D/4A:  %s"
              % ("YES" if targets == ["2W", "1S", "5D", "4A"] else "no"))

    section("[4] THE RESULTING 8-CHARACTER CANDIDATES")
    s_num = "".join(STAR_PAIR[n] for n in (1, 2, 3, 4))
    s_let = "".join(STAR_PAIR[n][1] + STAR_PAIR[n][0] for n in (1, 2, 3, 4))
    print("  star order, number-first (how the grid writes the cells): %s" % s_num.lower())
    print("  star order, letter-first                                 : %s" % s_let.lower())
    print("  NOTE: letter-first vs number-first is UNFORCED.  Nothing in the")
    print("        clue states which order the two glyphs are read in.")

    section("[5] NULL MODEL: IS THE ONE-TO-ONE PAIRING SURPRISING? NO.")
    random.seed(20261001)
    cells = [(r, c) for r in range(N) for c in range(N)]
    trials = 200000
    bij = both = 0
    for _ in range(trials):
        pick = random.sample(cells, 8)
        st, en = pick[:4], pick[4:]
        asg = [sorted((manhattan(s, e), e) for e in en) for s in st]
        if len({a[0][1] for a in asg}) == 4:
            bij += 1
            if all(a[0][0] < a[1][0] for a in asg):
                both += 1
    print("  %d random placements of 4 stars + 4 entries on the 10x10 grid:" % trials)
    print("    nearest-entry assignment is a perfect matching : %5.1f%%" % (100.0 * bij / trials))
    print("    ...and every star's nearest is strictly unique : %5.1f%%" % (100.0 * both / trials))
    print("  The observed structure is common.  A bijection here is NOT evidence")
    print("  of deliberate construction on its own.")

    section("[6] 'CYCLE ORDER' IS AMBIGUOUS -- 8 CANDIDATES, NOT 1")
    print("  Nothing on the 92-cycle marks a starting cell.  The only rotations")
    print("  that mean anything are the ones that start AT an entry cell (4 of")
    print("  them); each can also be walked forwards or backwards.  So:")
    seen = []
    for direction, tour in (("forward", cyc), ("reversed", cyc[::-1])):
        starts = [(tour.index(succ(flat(k))), ENTRY[k]) for k in ENTRY]
        for _, first in sorted(starts):
            off = tour.index(succ(flat(next(k for k in ENTRY if ENTRY[k] == first))))
            rot = tour[off:] + tour[:off]
            pos = {v: k for k, v in enumerate(rot)}
            s = "".join(ENTRY[(r, c)] for (r, c) in
                        sorted(ENTRY, key=lambda k: pos[succ(flat(k))]))
            if s not in seen:
                seen.append(s)
                print("    %-9s starting at %s -> %s -> %s"
                      % (direction, first, s, s.lower()))
    print("  distinct candidates from 'cycle order': %d" % len(seen))
    for x in seen:
        print("      %s%s" % (x.lower(), "   <- the round-12 pick" if x == "4A5D2W1S" else ""))
    print("  The round-12 pick a4d5w2s1 is the FORWARD rotation starting at 4A.")
    print("  That is a choice among %d, and the clue supplies no reason to" % len(seen))
    print("  prefer it.  A 'principled alternative' here is a family, not a peer.")

    section("[7] THE DECISIVE CONSTRAINT: NEITHER CANDIDATE IS TESTABLE")
    try:
        import oracle
        l3, l7 = oracle.ANSWER_LEN[3], oracle.ANSWER_LEN[7]
    except Exception:
        l3, l7 = 8, 24
    print("  segment 3 AES-256 key = clue3 (%d) || clue7 (%d) = %d bytes"
          % (l3, l7, l3 + l7))
    print("  tools/oracle.py takes BOTH halves.  There is no per-clue oracle and")
    print("  no partial-padding filter, because the padding lives in the single")
    print("  AES block produced by the full 32-byte key.")
    print()
    print("  => 'test w2s1d5a4 / a4d5w2s1 first' CANNOT BE EXECUTED.")
    print("     Clue 7 must be solved first.  Until then this list is untested,")
    print("     and an untested list is a hypothesis, not a breakthrough.")

    section("VERDICT (round 12): the structural decomposition is CORRECT and")
    print("reproducible.  But the two 'principled' readings are not two readings:")
    print("star order has an unforced glyph order (2 candidates), cycle order has")
    print("no start cell (8 candidates), and the one-to-one pairing that makes the")
    print("star reading look tight occurs ~3% of the time by chance.  Nothing here")
    print("can be confirmed until clue 7's 24 characters exist.")
    print()
    print("SUPERSEDED (round 13): the nearest-star rule above is an operation the")
    print("clue never states, so it is unnecessary.  Reading the same eight root")
    print("cells in row-major order -- letter for arrows, number for stars -- gives")
    print("d3w1as24 with no invented metric.  See tools/clue3_root_encoding.py.")
    print()
    print("Companion result this round, on clue 5: tools/clue5_pennant.py")
    print("measures the three pennants by pixels and confirms correction X2")
    print("(units mi / km / mi), which closes round 10's all-km geography as a")
    print("solution outright: row 1's 12,772 in miles is 539 km past pi*R.")
    print("=" * 78)


if __name__ == "__main__":
    main()