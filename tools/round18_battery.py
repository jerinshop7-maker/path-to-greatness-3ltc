#!/usr/bin/env python3
"""Round 18 -- execute the round-15..17 test plan against the real oracle.

The repo's own record ends at round 14 (`analysis/SESSION-FINDINGS-2026-10-01i.md`).
Rounds 15..17 arrive from outside it and propose five candidate families.  This
tool runs each one against the real AES-256-CBC segment oracle, using the repo's
own retained candidate sets rather than the write-ups' hand transcriptions, and
labelling every family with its measured size.

What is tested

  S3 side-elevation register   the 13 exact-24 strings the rounds call the
                               "side elevation / watertight bulkheads" reading of
                               the recovered montage, crossed with the 1,290
                               retained clue-3 readings (families A-F of
                               tools/clue3_ship_cross.py).
  S3 founder / fall register   the 3 exact-24 strings derived from the clue-3 IV
                               `colors_on_leaves` -> fall -> "will founder".
  S2 Roman-letter deletion     4 case-preserving clue-4 piece orderings crossed
                               with EVERY single-character deletion of the
                               21-letter Roman string (not just the one the
                               write-up picks) plus `chartingeightwonders`.
  S4 clue-2 instruction words  the "word-aligned instruction-key" family,
                               re-derived here from the displayed anagram words
                               rather than taken on trust, plus the literal
                               running-sum reading, plus the write-ups' verbatim
                               strings, x both 17-digit sky candidates.

Every sweep goes through tools/segsweep.py, which plants a witness and reports
how many candidates it dropped on length, so "0 hits" is attributable.
"""

from __future__ import annotations

import argparse
import itertools
import sys

sys.path.insert(0, ".")

from segsweep import sweep                          # noqa: E402
from clue3_ship_cross import (fam_a, fam_b, fam_c,   # noqa: E402
                              fam_d, fam_e, fam_f)

# ----------------------------------------------------------------- clue 7 ----
# The round-16/17 "grounded side-elevation register": what the recovered middle
# object (a ship's line drawing) and the screenplay's own words ("a side
# elevation showing the watertight bulkheads") license.  All exactly 24 chars.
SIDE_ELEVATION = [
    "sideelevationofbulkheads",
    "shipdrawingwithbulkheads",
    "sideelevationdrawingplan",
    "titanicsideelevationplan",
    "titanicsideelevationview",
    "andrewspointstobulkheads",
    "andrewspointstoelevation",
    "andrewsexplainsbulkheads",
    "watertightbulkheadsplans",
    "sideelevationandbulkhead",
    "elevationofbulkheadsplan",
    "sideelevationofshipplans",
    "sideelevationofhullplans",
]

# Round 17's IV bridge: clue 3's IV `colors_on_leaves` is the only one that is
# not an album track, so it is read as a hint (leaves -> fall) onto the scene's
# phrase "Titanic will founder".
FOUNDER_FALL = [
    "titanicwillfounderinfall",
    "thetitanicfoundersinfall",
    "theshipwillfounderinfall",
]

# ----------------------------------------------------------------- clue 4 ----
# The board is 14 pieces; the answer is 12 characters and keeps its case, so the
# natural reduction is "the 12 non-king pieces".  These four orderings all
# preserve the board's exact piece multiset (see round 16/17 for the ordering
# arguments: front lines -> throne, pawns first).
CHESS = [
    "pppppPnNBrrQ",
    "PpppppNnBrrQ",
    "rrppppnpNBQP",
    "PNBQpppppnrr",
]

# ----------------------------------------------------------------- clue 5 ----
# 12,772 / 5,210 / 12,061 as Roman letters = XMMDCCLXXII VCCX XMMLXI = 21
# letters, against an answer length of 20.  The write-up fixes one deletion
# (row 1's rightmost I); the honest family is all 21 single deletions.
ROMAN = "xmmdcclxxiivccxxmmlxi"
WONDERS_EXTRA = ["chartingeightwonders"]

# ----------------------------------------------------------------- clue 2 ----
S = "s-bcBPEFfJDfeFmksmPOkChDhrgBqjD-i---ffeNB"
assert len(S) == 41, len(S)
CHUNK_LENS = [2, 5, 8, 7, 4, 8, 3, 4]           # TO LOWER SUBTRACT CAPITAL …
CHUNKS, _off = [], 0
for _L in CHUNK_LENS:
    CHUNKS.append((_off, _off + _L))
    _off += _L
assert _off == 41

ADD_WORDS = {"CAPITAL", "ADDITION"}
SUB_WORDS = {"LOWER", "SUBTRACT"}
# The write-ups' verbatim strings (rounds 15/16/17).  Tested as given, and each
# one is reported against the family re-derived below so a derivation mismatch
# is visible rather than hidden.
VERBATIM = [
    "ekmmhjcyiolfxit", "lityiofxekmmhjc", "dnbyiofxekmmhjc",
    "ekmmhjcyiodfxnb", "dtyeimhtiawruik",
    "withyourcapital", "capitaladdition",
]

SKIES = ["71520219618128920", "58112171456182114"]


# ================================================================== helpers ==
def clue3_retained():
    """The round-14 retained clue-3 side: union of families A-F, length 8."""
    u = set()
    per = {}
    for name, fn in (("A", fam_a), ("B", fam_b), ("C", fam_c),
                     ("D", fam_d), ("E", fam_e), ("F", fam_f)):
        vals = {v for v in fn().values() if len(v) == 8}
        per[name] = len(vals)
        u |= vals
    return sorted(u), per


def word_family():
    """Re-derive the 'word-aligned instruction-key' family the rounds describe.

    For each of the 4 length-compatible assignments of the 8 anagram words to
    the 8 ciphertext chunks: the word's letters are the per-capital shift key.
    LOWER and SUBTRACT chunks subtract; CAPITAL, ADDITION and (the write-up's
    second list) WITH/YOUR add; TO and THE carry no capital, so their neutral
    behaviour never binds.  Enumerated conventions:

      align  positional (every cell, dash/lowercase included, consumes a key
             letter) or compact (only capital cells do)
      value  1-based A=1 algebra (the natural reading of the instruction words)
             or 0-based A=0
      rule   'chunk' (the word decides +/-) or 'cell' (every capital adds)
      with   WITH/YOUR add, or are neutral (the write-up leaves this open)

    Output is one lowercase letter per capital cell -> every string is 15 chars.
    """
    out = {}
    for eight in (("SUBTRACT", "ADDITION"), ("ADDITION", "SUBTRACT")):
        for four in (("WITH", "YOUR"), ("YOUR", "WITH")):
            words = ["TO", "LOWER", eight[0], "CAPITAL", four[0], eight[1],
                     "THE", four[1]]
            for align in ("positional", "compact"):
                for neutral in (1, 0):               # 1 = WITH/YOUR add
                    for base in (1, 0):              # A=1 or A=0
                        for rule in ("chunk", "cell"):
                            chars = []
                            for (start, end), w in zip(CHUNKS, words):
                                seen_caps = 0
                                for j in range(start, end):
                                    c = S[j]
                                    if not c.isupper():
                                        continue
                                    if align == "positional":
                                        ki = (j - start) if base == 0 \
                                            else (j - start + 1) - 1
                                    else:
                                        ki = seen_caps
                                    seen_caps += 1
                                    ki = min(ki, len(w) - 1)
                                    if rule == "chunk":
                                        if w in SUB_WORDS:
                                            op = -1
                                        elif w in (ADD_WORDS | {"WITH",
                                                                "YOUR"}):
                                            op = 1
                                        else:
                                            op = neutral
                                    else:
                                        op = 1           # every capital adds
                                    if base == 1:
                                        v = ord(c) - 64
                                        k = ord(w[ki]) - 64
                                        idx = (v + op * k - 1) % 26
                                    else:
                                        v = ord(c) - 65
                                        k = ord(w[ki]) - 65
                                        idx = (v + op * k) % 26
                                    chars.append(chr(97 + idx))
                            s = "".join(chars)
                            if len(s) == 15:
                                out.setdefault(s, "assign=%s|%s|align=%s|"
                                                    "with=%d|base=%d|rule=%s"
                                               % (eight, four, align, neutral,
                                                  base, rule))
    return out


def running_family():
    """Round 17's literal reading: scan the 41 cells left to right, uppercase
    adds its alphabet value, lowercase subtracts, dash does nothing, and one
    output character is emitted when an uppercase cell is processed.

    The write-up does not fix the conversion back to a letter, so both natural
    ones are enumerated (0-based chr(97+n%26) and 1-based chr(97+(n-1)%26)),
    along with the start value, the dash-reset rule and the emit timing."""
    out = {}
    for base in (0, 1):
        for reset in (False, True):
            for before in (False, True):
                for start in (0, 1):
                    for om in ("zero", "one"):
                        tot, chars = start, []
                        for c in S:
                            if c == "-":
                                if reset:
                                    tot = 0
                                continue
                            v = (ord(c.upper()) - 65) + base
                            if c.isupper():
                                if before:
                                    chars.append(_run_letter(tot, om))
                                    tot += v
                                else:
                                    tot += v
                                    chars.append(_run_letter(tot, om))
                            else:
                                tot -= v
                        out.setdefault("".join(chars),
                                       "running|base=%d|reset=%s|before=%s|"
                                       "start=%d|map=%s"
                                       % (base, reset, before, start, om))
    return out


def _run_letter(n, om):
    return chr(97 + (n % 26 if om == "zero" else (n - 1) % 26))


# ==================================================================== main ==
def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--wasd8", action="store_true",
                    help="also cross the new clue-7 registers with the full "
                         "{w,a,s,d}^8 space (1,048,576 pairs)")
    args = ap.parse_args()

    print("=" * 78)
    print("ROUND 18 -- the round-15..17 test plan, on the real oracle")
    print("=" * 78)

    c3, per = clue3_retained()
    print("\nclue-3 retained readings: %d distinct (families A-F: %s)"
          % (len(c3), ", ".join("%s=%d" % kv for kv in per.items())))
    assert all(len(s) == 8 for s in c3)

    # ---- S3 side-elevation / founder-fall -----------------------------------
    print("\n" + "-" * 78)
    print("S3  clue-7 side-elevation and founder/fall registers")
    print("-" * 78)
    for name, lst in (("side-elevation", SIDE_ELEVATION),
                      ("founder/fall", FOUNDER_FALL)):
        bad = [s for s in lst if len(s) != 24]
        print("%-16s %2d strings, all exactly 24 chars: %s"
              % (name, len(lst), not bad))
        for s in lst:
            print("    %s" % s)
        sweep(3, c3, lst, name)
        if args.wasd8:
            w8 = ["".join(p) for p in itertools.product("wasd", repeat=8)]
            sweep(3, w8, lst, name + " x wasd^8")

    # ---- S2 chess x Roman deletion ------------------------------------------
    print("\n" + "-" * 78)
    print("S2  clue-4 piece orderings x clue-5 Roman-letter deletions")
    print("-" * 78)
    deletions = sorted({ROMAN[:i] + ROMAN[i + 1:] for i in range(len(ROMAN))})
    print("Roman base string: %s (%d letters)" % (ROMAN, len(ROMAN)))
    print("single-deletion positions: %d -> %d distinct strings (all length %d);"
          " repeats collapse"
          % (len(ROMAN), len(deletions), len(deletions[0])))
    chosen = "xmmdcclxxivccxxmmlxi"
    print("write-up's pick %s is in the family: %s"
          % (chosen, chosen in deletions))
    for s in CHESS:
        assert len(s) == 12, s
    sweep(2, CHESS, deletions + WONDERS_EXTRA, "chess x roman-deletion")

    # ---- S4 clue-2 families x sky -------------------------------------------
    print("\n" + "-" * 78)
    print("S4  clue-2 instruction-word and running-sum families x sky")
    print("-" * 78)
    words = word_family()
    running = running_family()
    verb = [s for s in VERBATIM if len(s) == 15]
    print("instruction-word family (re-derived): %d distinct 15-char strings"
          % len(words))
    print("literal running-sum family:           %d distinct" % len(running))
    print("write-up verbatim strings (len 15):   %d of %d"
          % (len(verb), len(VERBATIM)))
    for s in VERBATIM:
        if len(s) == 15:
            where = ("word-family" if s in words else
                     "running-family" if s in running else "NOT reproduced")
            print("    %-18s %s" % (s, where))
    pool = dict(words)
    for k, v in running.items():
        pool.setdefault(k, v)
    for s in verb:
        pool.setdefault(s, "verbatim")
    print("distinct clue-2 candidates to cross: %d" % len(pool))
    sweep(4, sorted(pool), SKIES, "clue2 family x sky")

    print("\n" + "=" * 78)
    print("VERDICT: see per-family hit counts above. A 0-hit family is a JOINT")
    print("refutation of the pairs tested in it; it does not refute either half")
    print("of a segment on its own (oracle.py L1 is a filter, not an answer).")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
