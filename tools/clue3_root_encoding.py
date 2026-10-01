#!/usr/bin/env python3
"""Clue 3, round 13: verify the D3W1AS24 encoding, and settle two claims that
were re-proposed without being re-derived.

PART 1 -- the new root-cell encoding.  Round 13 proposed D3W1AS24 as the
strongest purely structural clue-3 candidate: take the 8 cells with no
predecessor, read them row-major, and keep the WASD letter for an arrow-root or
the number for a star-root.  It reproduces exactly:

    r1c2=5D->D  r2c4=3*->3  r4c9=2W->W  r5c7=1*->1
    r8c10=4A->A r9c1=1S->S r9c3=2*->2  r9c9=4*->4   =>  d3w1as24

That is genuinely cleaner than round 12's W2S1D5A4, which needed a
nearest-neighbour rule the clue never states.  It is still a derived hypothesis,
NOT a solution: segment 3's key is clue3(8) || clue7(24), so it cannot be tested
without clue 7.  This tool shows the number-only variant 53214124 too, since both
fall out of the same eight cells.

PART 2 -- the interleaving count.  Round 13 quoted "4! x 4! x C(8,4) = 70 x 576
= 40,320".  The arithmetic is right but the phrasing conflates two families, and
the distinction decides how big a search is worth running:

    both group orders fixed (display order)      70
    one group order free                        1,680
    both group orders free (40,320 total)    40,320

40,320 is the size of a family that lets the ORDER of both groups float, which
means it is no longer a reading of the grid -- it is an enumeration over 8!
arrangements of 8 distinct symbols, i.e. over the same space as permuting 8
characters arbitrarily.  70 is the honest size of "keep both groups in reading
order, choose which slots are letters".  Printed so the next reader does not
re-derive it.

PART 3 -- the clue-2 word/chunk bipartite proposal, which does NOT work.  Round 13
proposed solving an 8x8 assignment between the eight anagram words and the eight
same-length ciphertext chunks, using letter-multiset and case relations to
determine the permutation.  The premise is wrong in a way that is cheap to show:

  * The eight word lengths are 2,5,8,7,4,8,3,4 and the eight chunk lengths are
    2,5,8,7,4,8,3,4 -- IDENTICAL, including which two words share each length.
    So length alone already pins 6 of 8 words, leaving only 2! x 2! = 4
    length-compatible assignments, not a rich constraint problem.
  * Worse, the extraction is INVARIANT under all 4.  The 15 capitals are read
    positionally out of one fixed 41-cell string; the chunk labels do not enter.
    Relabelling which word owns a chunk cannot move a capital.  The output is
    byte-identical ('BPE'+'FJDF'+'POC'+'D'+'BD'+'NB') for all four assignments.

So the permutation is not merely small, it is not observable in the output.  The
only thing that can change the 15 characters is the chunk BOUNDARIES, not the
labels -- and both candidate boundary sets (display order and sentence order)
are already recorded in analysis/IMAGE-TRANSCRIPTION.md.

PART 4 -- a correction to round 13's prose.  It lists "*1 (r2c4) -> 5D" and
"*3 (r5c7)".  The transcription has *3 at r2c4 and *1 at r5c7: the two labels are
swapped.  The nearest-root pairing itself is unaffected (*1->2W, *2->1S, *3->5D,
*4->4A), because the prose swapped the numbers but not the pairing.  Recorded so
the next session does not trust the prose over the tool.
"""

import math
import sys
from collections import Counter

from wasd_grid import N, build, cell, rc, succ

STAR_LABELS = {1: "r5c7", 2: "r9c3", 3: "r2c4", 4: "r9c9"}

# clue 2, from analysis/IMAGE-TRANSCRIPTION.md
LINE3 = "s-bcBPEFfJDfeFmksmPOkChDhrgBqjD-i---ffeNB"
WORDS = ["TO", "LOWER", "SUBTRACT", "CAPITAL", "WITH", "ADDITION", "THE", "YOUR"]
DISPLAY_SEGS = [(0, 2), (2, 7), (7, 15), (15, 22), (22, 26), (26, 34), (34, 37), (37, 41)]
SENTENCE = [("WITH", 4), ("YOUR", 4), ("CAPITAL", 7), ("ADDITION", 8),
            ("TO", 2), ("LOWER", 5), ("SUBTRACT", 8), ("THE", 3)]


def section(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


def root_cells():
    _, ind = build()
    return [i for i in range(N * N) if i not in ind]


def clue3_encoding():
    section("[1] ROOT-CELL ENCODING (reproduces d3w1as24)")
    roots = root_cells()
    letters, numbers = "", ""
    print("  the %d cells with no predecessor, in row-major order:" % len(roots))
    for i in roots:
        n, d = cell(i)
        r, c = rc(i)
        tok = str(n) if d == "*" else d
        letters += tok
        numbers += str(n)
        print("    r%-2dc%-2d = %-4s -> %s" % (r + 1, c + 1, "%d%s" % (n, d), tok))
    print("\n  arrow=letter, star=number      -> %s   (len %d)"
          % (letters.lower(), len(letters)))
    print("  every cell's number            -> %s   (len %d)" % (numbers, len(numbers)))
    ok = letters.lower() == "d3w1as24"
    print("\n  matches the proposed d3w1as24 : %s" % ("YES" if ok else "NO"))
    print("  advantage over w2s1d5a4: needs no nearest-neighbour rule, which the")
    print("  clue never states.  Reading order alone produces it.")
    print("  STATUS: derived hypothesis. Still untestable -- segment 3 needs clue 7.")


def interleavings():
    section("[2] HOW BIG IS THE INTERLEAVING FAMILY, REALLY?")
    fixed = math.comb(8, 4)
    print("  C(8,4) = %d   (keep BOTH groups in reading order)" % fixed)
    print("  %d x 24  = %d   (one group's order free)" % (fixed, fixed * 24))
    print("  %d x 24 x 24 = %d  (BOTH orders free)" % (fixed, fixed * 24 * 24))
    print()
    print("  The 40,320 figure is correct arithmetic but it is the size of a family")
    print("  in which the order of BOTH groups floats.  Eight distinct symbols in")
    print("  8! = 40,320 arrangements -- i.e. it is a permutation search over the")
    print("  whole string, not a reading of the grid.  70 is the honest size of the")
    print("  grid-faithful family. Do not spend an hour on the 40,320.")


def clue2_assignment():
    section("[3] CLUE 2: THE 8x8 WORD/CHUNK ASSIGNMENT HAS NO FREE PARAMETER")
    wl = [len(w) for w in WORDS]
    cl = [b - a for a, b in DISPLAY_SEGS]
    print("  word lengths : %s  sum=%d" % (wl, sum(wl)))
    print("  chunk lengths: %s  sum=%d" % (cl, sum(cl)))
    print("  identical    : %s" % ("YES" if wl == cl else "no"))
    cnt = Counter(wl)
    amb = 1
    for L, c in sorted(cnt.items()):
        if c > 1:
            grp = [w for w in WORDS if len(w) == L]
            amb *= math.factorial(c)
            print("    length %d shared by %-18s -> %d! ways"
                  % (L, ", ".join(grp), c))
    print("  length-compatible assignments: %d" % amb)
    print("  (6 of 8 words are pinned by length alone.)")

    print("\n  ...and the 15 capitals are INVARIANT under all of them:")
    def caps():
        out = []
        for a, b in DISPLAY_SEGS:
            out.append("".join(c for c in LINE3[a:b] if c.isupper()))
        return out
    base = caps()
    print("    all %d assignments give the same 15 characters:" % amb)
    print("      %s" % " + ".join(repr(c) for c in base))
    print("      = %s  (len %d)" % ("".join(base), sum(len(c) for c in base)))
    print()
    print("  REASON: the capitals are read POSITIONALLY out of one fixed 41-cell")
    print("  string.  Chunk labels never enter the extraction, so relabelling which")
    print("  word owns a chunk cannot move a character.  The permutation is not")
    print("  merely small -- it is UNOBSERVABLE in the output.")
    print()
    print("  The only thing that can change the answer is the BOUNDARIES.")
    print("    display order  : %s" % (DISPLAY_SEGS,))
    tot = 0
    parts = []
    for w, L in SENTENCE:
        parts.append("%s(%d)" % (w, L))
        tot += L
    print("    sentence order : %s  totalling %d cells" % (" ".join(parts), tot))
    print("  Both are already recorded in analysis/IMAGE-TRANSCRIPTION.md, so the")
    print("  label-permutation attack has nothing left to decide.")


def star_correction():
    section("[4] CORRECTION TO ROUND 13's PROSE")
    print("  round 13 wrote: '*1 (r2c4) -> 5D' and '*3 (r5c7)'.")
    print("  transcription : *3 is at r2c4, *1 is at r5c7 -- the labels are swapped.")
    print("  the pairing itself is unaffected, because the numbers were swapped")
    print("  while the nearest-root assignment was not:")
    _, ind = build()
    roots, starpos = [], {}
    for i in range(N * N):
        if i in ind:
            continue
        n, d = cell(i)
        if d == "*":
            starpos[n] = rc(i)
        else:
            roots.append(i)
    for n in (1, 2, 3, 4):
        sp = starpos[n]
        ds = sorted((abs(sp[0] - rc(e)[0]) + abs(sp[1] - rc(e)[1]),
                     cell(e)[0], cell(e)[1]) for e in roots)
        print("    *%d (r%dc%d) -> %d%s   d=%d"
              % (n, sp[0] + 1, sp[1] + 1, ds[0][1], ds[0][2], ds[0][0]))
    print("  trust tools/wasd_grid.py over prose.")


def main():
    print("Clue 3, round 13: verification and two refutations")
    clue3_encoding()
    interleavings()
    clue2_assignment()
    star_correction()
    print()
    print("=" * 78)
    print("VERDICT: d3w1as24 CONFIRMED as a clean structural encoding -- it needs")
    print("no invented metric, and it is the best purely structural clue-3 reading")
    print("so far. It remains UNTESTABLE until clue 7's 24 characters exist.")
    print("REFUTED: the 8x8 word/chunk assignment for clue 2. Lengths pin 6 of 8")
    print("words, and the 15-capital extraction is byte-identical across all 4")
    print("surviving assignments, so the permutation is unobservable. Not a lead.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())