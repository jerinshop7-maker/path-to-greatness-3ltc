#!/usr/bin/env python3
"""Round 20 -- two genuinely new families, both oracle-testable.

A. CLUE 7: the FULL-NAME family.
   The write-up's `jbruceismaythomasandrews` is new: the earlier sweeps used
   `ismay`/`andrews`/`smith`/`hyde`/`garber` as bare surnames and 4-token
   permutations of `ismay andrews smith titanic`.  A full name with its initial
   ("jbruceismay", 11 chars) had never been generated.  This family builds every
   length-24 string from those full/initial forms (and a small set of ship
   context words), sizes it BEFORE sweeping (the round-14 lesson), and crosses
   it with the 1,290 retained clue-3 readings; the full-name pairs are
   additionally crossed with the whole {w,a,s,d}^8 space.

B. CLUE 2: the 15 capitals as MARKERS, not operands.
   The panel supplies TWO 41-character strings, and the analysis has only ever
   used the mixed-case one as the operand stream:
     C = the ciphertext                s-bcBPEFfJDfeFmksmPOkChDhrgBqjD-i---ffeNB
     I = the instruction sentence      withyourcapitaladditiontothelowersubtract
   (the same 41 letters in sentence order; display order is another permutation
   of them).  If the 15 capitals are *extraction markers*, they select letters
   out of the other 41-cell stream.  This tool generates that family -- position
   markers and value markers indexing C, I (both orders) and the alphabet --
   plus the write-up's "the answer is a phrase" reading as every 15-character
   window of both instruction orderings, plus the word-chunk features (capital
   count / lowercase count / word length per chunk) as shifts.

Every sweep goes through tools/segsweep.py (normalisation, reported length
drops, a planted witness per call).
"""

from __future__ import annotations

import itertools
import sys

sys.path.insert(0, ".")

from segsweep import sweep                          # noqa: E402

# ---------------------------------------------------------------- clue 7 -----
# Full / initial forms the earlier sweeps did not contain.
NAMES = [
    "jbruceismay", "jbismay", "bruceismay", "ismay",
    "thomasandrews", "tandrews", "andrews",
    "edwardsmith", "esmith", "smith",
    "victorgarber", "garber", "jonathanhyde", "hyde",
    "bernardhill", "hill",
]
SHIPWORD = ["titanic", "ship", "drawing", "plans", "liner", "ocean"]
GLUE = ["and", "the", "of"]

# Curated semantic candidates in the same new register.
CURATED = [
    "jbruceismaythomasandrews",
    "thomasandrewsjbruceismay",
    "thomasandrewsedwardsmith",
    "edwardsmiththomasandrews",
    "jbruceismaycaptainsmith",
    "captainsmithjbruceismay",
    "titanicjbruceismaythomas",
    "jbruceismaythomasandrew",
    "theshipanditsbuilderhe",     # 3+4+3+3+7 = ... checked by the length filter
    "shipbuilderanditscaptain",
    "makerandcaptainandships",
    "thegreatundertakeratsea",
]

TARGET = 24


def ship_family():
    """Every exactly-24 string built from the new name forms."""
    out = {}

    def add(s, tag):
        if len(s) == TARGET:
            out.setdefault(s, tag)

    # full/initial name pairs
    for a, b in itertools.permutations(NAMES, 2):
        add(a + b, "pair:%s+%s" % (a, b))
        # with a glue word between them
        for g in GLUE:
            add(a + g + b, "pair:%s+%s+%s" % (a, g, b))
    # one or two names + a ship word
    for a in NAMES:
        for w in SHIPWORD:
            add(a + w, "name+ship:%s+%s" % (a, w))
            add(w + a, "ship+name:%s+%s" % (w, a))
    for a, b in itertools.permutations(NAMES, 2):
        for w in SHIPWORD:
            add(a + b + w, "pair+ship:%s+%s+%s" % (a, b, w))
            add(a + w + b, "pair+ship:%s+%s+%s" % (a, w, b))
    for s in CURATED:
        add(s, "curated")
    return {k: v for k, v in out.items()}


# ---------------------------------------------------------------- clue 2 -----
S = "s-bcBPEFfJDfeFmksmPOkChDhrgBqjD-i---ffeNB"
assert len(S) == 41

I_SENT = ("with" + "your" + "capital" + "addition" + "to" + "the" + "lower"
          + "subtract")
I_DISP = ("ot" + "rleow" + "utbrctsa" + "aacpilt" + "hwti" + "dioiatdn"
          + "het" + "ryuo")
assert len(I_SENT) == 41 and len(I_DISP) == 41, (len(I_SENT), len(I_DISP))
# The two instruction orderings must be permutations of the same 41 letters
# (a transcription check on the displayed anagrams).
assert sorted(I_SENT) == sorted(I_DISP), "instruction orderings disagree!"
# The ciphertext is NOT the same multiset: it is 36 letters + 5 dashes across
# 41 cells, while the instruction is 41 letters.  They correspond positionally
# (chunk for chunk), which is exactly why the marker reading is worth testing.
assert len(S) == 41 and sum(1 for c in S if c == "-") == 5
assert sum(1 for c in S if c.isalpha()) == 36

CAP_POS = [i + 1 for i, c in enumerate(S) if c.isupper()]      # 1-based
CAP_VAL = [ord(c) - 64 for c in S if c.isupper()]              # A=1
CAP_ORD = list(range(1, len(CAP_POS) + 1))
CAP_DELTA = [1] + [CAP_POS[i] - CAP_POS[i - 1]
                   for i in range(1, len(CAP_POS))]            # 15 values
ALPHA = "abcdefghijklmnopqrstuvwxyz"

WORD_LENS = [2, 5, 8, 7, 4, 8, 3, 4]
CHUNKS, _o = [], 0
for _L in WORD_LENS:
    CHUNKS.append((_o, _o + _L))
    _o += _L
assert _o == 41
# per word-chunk: capital count, lowercase count, chunk length
CHUNK_CAP = [sum(1 for c in S[a:b] if c.isupper()) for a, b in CHUNKS]
CHUNK_LOW = [sum(1 for c in S[a:b] if c.islower()) for a, b in CHUNKS]


def marker_family():
    """The 15 capitals as markers indexing another 41-cell stream."""
    out = {}
    targets = {"I_sent": I_SENT, "I_disp": I_DISP, "C": S,
               "C_lower": S.lower(), "alpha": ALPHA}
    selectors = {
        "pos": CAP_POS,                     # 1-based position in the string
        "pos0": [p - 1 for p in CAP_POS],
        "val": CAP_VAL,                     # A=1 alphabet value
        "val0": [v - 1 for v in CAP_VAL],
        "ord": CAP_ORD,                     # 1..15
        "ord0": [o - 1 for o in CAP_ORD],
        "delta": CAP_DELTA,                 # gap to the previous capital
        "ascii": [ord(c) for c in S if c.isupper()],
    }
    for tn, t in targets.items():
        for sn, sels in selectors.items():
            chars = [t[v % len(t)] for v in sels]
            out.setdefault("".join(chars), "marker|%s|%s" % (tn, sn))
    # value -> letter of the alphabet, ignoring the target stream
    for sn, sels in selectors.items():
        out.setdefault("".join(chr(97 + v % 26) for v in sels),
                       "mod26|%s" % sn)
    return {k: v for k, v in out.items() if len(k) == 15}


def window_family():
    """The write-up's 'the answer is a phrase': every 15-char window of the
    instruction in both orderings."""
    out = {}
    for name, t in (("I_sent", I_SENT), ("I_disp", I_DISP)):
        for i in range(len(t) - 15 + 1):
            out.setdefault(t[i:i + 15], "window|%s|%d" % (name, i))
    return out


def chunk_shift_family():
    """Shift each capital by a feature of its own word-chunk."""
    out = {}
    feats = {"chunk_caps": CHUNK_CAP, "chunk_lower": CHUNK_LOW,
             "chunk_len": WORD_LENS}
    for fname, fv in feats.items():
        for shift in range(26):
            for op in (1, -1):
                for base in (0, 1):
                    chars = []
                    for ci, (a, b) in enumerate(CHUNKS):
                        for j in range(a, b):
                            ch = S[j]
                            if not ch.isupper():
                                continue
                            v = (ord(ch) - 65) + base
                            x = v + op * fv[ci] + shift
                            chars.append(chr(97 + x % 26))
                    out.setdefault("".join(chars),
                                   "chunk_shift|%s|op%+d|shift%d|base%d"
                                   % (fname, op, shift, base))
    return {k: v for k, v in out.items() if len(k) == 15}


def main():
    print("=" * 78)
    print("A. CLUE 7 -- the full-name family (new register)")
    print("=" * 78)
    fam = ship_family()
    print("family size: %d strings of exactly %d characters"
          % (len(fam), TARGET))
    print("all exactly 24 chars: %s" % all(len(s) == 24 for s in fam))
    for s in sorted(fam)[:10]:
        print("    %s" % s)
    if len(fam) > 10:
        print("    ... and %d more" % (len(fam) - 10))

    print("\nA1. full-name pairs x the full {w,a,s,d}^8 space "
          "(65,536 each)")
    pairs = sorted({s for s, t in fam.items() if t.startswith("pair:")}
                   | {"jbruceismaythomasandrews",
                      "thomasandrewsjbruceismay",
                      "thomasandrewsedwardsmith",
                      "edwardsmiththomasandrews"})
    pairs = [s for s in pairs if len(s) == 24]
    print("    pair strings: %d" % len(pairs))
    w8 = ["".join(p) for p in itertools.product("wasd", repeat=8)]
    sweep(3, w8, pairs, "clue7 full-name x wasd^8")

    print("\nA2. the whole new family x the 1,290 retained clue-3 readings")
    sys.path.insert(0, ".")
    from clue3_ship_cross import fam_a, fam_b, fam_c, fam_d, fam_e, fam_f
    u = set()
    for fn in (fam_a, fam_b, fam_c, fam_d, fam_e, fam_f):
        u |= {v for v in fn().values() if len(v) == 8}
    c3 = sorted(u)
    print("    clue-3 readings: %d" % len(c3))
    sweep(3, c3, sorted(fam), "clue7 full-name x 1290")

    print("\n" + "=" * 78)
    print("B. CLUE 2 -- the 15 capitals as markers, and the phrase reading")
    print("=" * 78)
    print("two independent 41-character streams (transcription check passed):")
    print("    C = %s" % S)
    print("    I = %s" % I_SENT)
    print("    I = %s   (display order)" % I_DISP)
    print("capital positions (1-based): %s" % CAP_POS)
    print("per-chunk capital counts:    %s" % CHUNK_CAP)
    mk = marker_family()
    wn = window_family()
    cs = chunk_shift_family()
    print("\nmarker family (capitals index C / I / alphabet): %d" % len(mk))
    for s in sorted(mk)[:10]:
        print("    %-16s %s" % (s, mk[s]))
    print("instruction-window family: %d" % len(wn))
    print("chunk-feature shift family: %d" % len(cs))
    pool = dict(mk)
    for s, v in wn.items():
        pool.setdefault(s, v)
    for s, v in cs.items():
        pool.setdefault(s, v)
    print("distinct clue-2 candidates to cross: %d" % len(pool))
    sweep(4, sorted(pool), ["71520219618128920", "58112171456182114"],
          "clue2 markers+windows+chunk")

    print("\nVERDICT lines above. A 0-hit family refutes the pairs; it does not")
    print("refute either half of a segment on its own.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
