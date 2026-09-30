#!/usr/bin/env python3
"""Clue 2, round 5: use the image LAYOUT.

The clue-2 image is rotated 90 degrees (all text runs vertically in the source
JPEG); OCR of the rotated image recovers the eight anagram words, and they are
displayed in a scrambled order:

    TO  LOWER  SUBTRACT  CAPITAL  WITH  ADDITION  THE  YOUR

which unscrambles to "WITH YOUR CAPITAL ADDITION TO THE LOWER SUBTRACT".

Their lengths (2,5,8,7,4,8,3,4) sum to exactly 41, the length of the mixed-case
string, so the words label eight consecutive segments of the string.  This file
tests the resulting families: reorder the segments into sentence order, shift
each capital by its segment's word, etc.
"""
import itertools
import sys

sys.path.insert(0, "tools")
from oracle import segment_oracle  # noqa: E402

S = "s-bcBPEFfJDfeFmksmPOkChDhrgBqjD-i---ffeNB"
assert len(S) == 41
DISPLAY = ["ot", "rleow", "utbrctsa", "aacpilt", "hwti", "dioiatdn", "het", "ryuo"]
CANON = {"ot": "TO", "rleow": "LOWER", "utbrctsa": "SUBTRACT", "aacpilt": "CAPITAL",
         "hwti": "WITH", "dioiatdn": "ADDITION", "het": "THE", "ryuo": "YOUR"}
SENT = [CANON[w] for w in DISPLAY]  # displayed words, canonical spelling
CORRECT = ["WITH", "YOUR", "CAPITAL", "ADDITION", "TO", "THE", "LOWER", "SUBTRACT"]
inv = {CANON[w]: w for w in DISPLAY}
CORRECT_SCRAMBLED = [inv[w] for w in CORRECT]

CV = lambda c: ord(c.upper()) - 64
SKIES = {"witness": "71520219618128920", "repo": "58112171456182114"}

segs, pos = [], 0
for w in DISPLAY:
    segs.append(S[pos:pos + len(w)])
    pos += len(w)
assert pos == 41
print("display segments:")
for w, s in zip(DISPLAY, segs):
    print("  %-9s %r" % (CANON[w], s))

by_word = {CANON[w]: segs[i] for i, w in enumerate(DISPLAY)}
T = "".join(by_word[w] for w in CORRECT)
print("sentence-order string:", T)
print("permutation correct->display:", [DISPLAY.index(w) + 1 for w in CORRECT_SCRAMBLED])

cands = {}


def emit(s, tag):
    if len(s) == 15 and s.isalpha():
        cands.setdefault(s.lower(), tag)


def run_families(X, prefix):
    CAP = [i for i, c in enumerate(X) if c.isupper()]
    LOW = [i for i, c in enumerate(X) if c.islower()]
    DASH = [i for i, c in enumerate(X) if c == "-"]
    # running
    for vs in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
        for res in (True, False):
            for c in range(26):
                for base in (1, 0):
                    tot, w = 0, []
                    for ch in X:
                        if ch == "-":
                            if res:
                                tot = 0
                            continue
                        v = CV(ch)
                        tot += vs[0] * v if ch.isupper() else vs[1] * v
                        if ch.isupper():
                            w.append(chr((tot + c - base) % 26 + 97))
                    if len(w) == 15:
                        emit("".join(w), "%s|run%s res%d c%d b%d" % (prefix, vs, res, c, base))
    # per-capital local features
    def feats(i):
        pl = max([j for j in LOW if j < i], default=None)
        nl = min([j for j in LOW if j > i], default=None)
        rB = []
        j = i - 1
        while j >= 0 and X[j].islower():
            rB.append(ord(X[j]) - 96)
            j -= 1
        rB.reverse()
        rA = []
        j = i + 1
        while j < len(X) and X[j].islower():
            rA.append(ord(X[j]) - 96)
            j += 1
        return {"prev": ord(X[pl]) - 96 if pl is not None else 0,
                "next": ord(X[nl]) - 96 if nl is not None else 0,
                "rbs": sum(rB), "ras": sum(rA), "rbc": len(rB), "rac": len(rA),
                "pls": sum(ord(X[j]) - 96 for j in range(i) if X[j].islower()),
                "nls": sum(ord(X[j]) - 96 for j in range(i + 1, len(X)) if X[j].islower()),
                "plo": sum(1 for j in range(i) if X[j].islower()),
                "nlo": sum(1 for j in range(i + 1, len(X)) if X[j].islower())}
    F = {i: feats(i) for i in CAP}
    for f in F[CAP[0]]:
        for op in (1, -1):
            for c in range(26):
                w = [chr((CV(X[i]) + op * F[i][f] + c - 1) % 26 + 97) for i in CAP]
                emit("".join(w), "%s|cap%+d%s c%d" % (prefix, op, f, c))


run_families(S, "S")
run_families(T, "T")
print("after positional families:", len(cands))

# word-informed families: each capital shifted by its segment's word
def cap_positions(seglist, words):
    """yield (capital char, word, ordinal-in-segment) for a segmentation"""
    for w, seg in zip(words, seglist):
        k = 0
        for ch in seg:
            if ch.isupper():
                yield ch, w, k
                k += 1


for seglist, words, pfx in ((segs, DISPLAY, "disp"),):
    items = list(cap_positions(seglist, words))
    for wordmode in ("cyc", "revcyc", "first", "last"):
        for op in (1, -1):
            for c in range(26):
                out = []
                for ch, w, k in items:
                    wl = list(w) if wordmode in ("cyc",) else \
                         list(w)[::-1] if wordmode == "revcyc" else \
                         [w[0]] if wordmode == "first" else [w[-1]]
                    s = CV(wl[k % len(wl)]) if wl else 0
                    out.append(chr((CV(ch) + op * s + c - 1) % 26 + 97))
                emit("".join(out), "%s|word%s%+d c%d" % (pfx, wordmode, op, c))
    for op in (1, -1):
        for c in range(26):
            for wm in ("len", "sum"):
                out = []
                for ch, w, k in items:
                    s = len(w) if wm == "len" else sum(CV(x) for x in w)
                    out.append(chr((CV(ch) + op * s + c - 1) % 26 + 97))
                emit("".join(out), "%s|word%s%+d c%d" % (pfx, wm, op, c))
print("after word families:", len(cands))

# sentence-order segments with their (correct-order) words
segs_c = [by_word[w] for w in CORRECT]
words_c = [[CANON[x] for x in DISPLAY if CANON[x] == w][0] for w in CORRECT]
items = list(cap_positions(segs_c, [inv[w] for w in CORRECT]))
for wordmode in ("cyc", "revcyc", "first", "last"):
    for op in (1, -1):
        for c in range(26):
            out = []
            for ch, w, k in items:
                wl = list(w) if wordmode == "cyc" else \
                     list(w)[::-1] if wordmode == "revcyc" else \
                     [w[0]] if wordmode == "first" else [w[-1]]
                out.append(chr((CV(ch) + op * CV(wl[k % len(wl)]) + c - 1) % 26 + 97))
            emit("".join(out), "sent|word%s%+d c%d" % (wordmode, op, c))
print("total distinct candidates:", len(cands))

tested = hits = 0
for s, tag in cands.items():
    for kn, sky in SKIES.items():
        tested += 1
        if segment_oracle(4, (s + sky).encode()):
            hits += 1
            print("MATCH!!!", s, tag, kn)
print("tested %d pairs, hits %d" % (tested, hits))
