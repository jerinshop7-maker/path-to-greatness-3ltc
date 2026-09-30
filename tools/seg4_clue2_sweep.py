#!/usr/bin/env python3
"""Clue-2 (scramble) sweep with clue-8 (sky) pinned.

If the witness-consistent clue-8 reading is right, segment 4 reduces to *one*
unknown: the 15-character clue-2 answer.  That makes every clue-2 hypothesis a
single oracle call, so the arithmetic rule space can be swept far more widely
than before (millions of rule/value pairs instead of a hand-picked few).

Clue-2 instruction: "With your capital, addition.  To the lower, subtract."
15 capitals, 21 lowercase, 5 dashes, 41 cells.
"""
import itertools
import sys

sys.path.insert(0, "tools")
from oracle import segment_oracle  # noqa: E402

S = "s-bcBPEFfJDfeFmksmPOkChDhrgBqjD-i---ffeNB"
assert len(S) == 41
CAP = [i for i, c in enumerate(S) if c.isupper()]
LOW = [i for i, c in enumerate(S) if c.islower()]
DASH = [i for i, c in enumerate(S) if c == "-"]
assert len(CAP) == 15 and len(LOW) == 21 and len(DASH) == 5
CV = lambda c: ord(c.upper()) - 64
LV = lambda c: ord(c) - 96

SKIES = {
    "witness12": "71520219618128920",   # new scheme, trailing dash-cell dropped
    "repo": "58112171456182114",
}


def context(i):
    """rich integer features for the capital at index i"""
    prev_low = max([j for j in LOW if j < i], default=None)
    next_low = min([j for j in LOW if j > i], default=None)
    runB = []
    j = i - 1
    while j >= 0 and S[j].islower():
        runB.append(LV(S[j]))
        j -= 1
    runB.reverse()
    runA = []
    j = i + 1
    while j < len(S) and S[j].islower():
        runA.append(LV(S[j]))
        j += 1
    lo = max([d for d in DASH if d < i], default=-1)
    hi = min([d for d in DASH if d > i], default=len(S))
    inb = [LV(S[j]) for j in range(lo + 1, i) if S[j].islower()]
    ina = [LV(S[j]) for j in range(i + 1, hi) if S[j].islower()]
    signed = 0
    for j in range(i):
        signed += CV(S[j]) if S[j].isupper() else -LV(S[j])

    def sgn(lst):
        return sum(lst)

    f = {
        "0": 0,
        "k": CAP.index(i) + 1,
        "i": i,
        "prev": LV(S[prev_low]) if prev_low is not None else 0,
        "next": LV(S[next_low]) if next_low is not None else 0,
        "rd": (i - prev_low) if prev_low is not None else 0,
        "nd": (next_low - i) if next_low is not None else 0,
        "rbs": sgn(runB), "rbc": len(runB), "rbf": runB[0] if runB else 0,
        "rbl": runB[-1] if runB else 0, "rbx": max(runB) if runB else 0,
        "rbm": min(runB) if runB else 0,
        "ras": sgn(runA), "rac": len(runA), "raf": runA[0] if runA else 0,
        "ral": runA[-1] if runA else 0, "rax": max(runA) if runA else 0,
        "ram": min(runA) if runA else 0,
        "cbs": sgn(inb), "cbc": len(inb), "cas": sgn(ina), "cac": len(ina),
        "d": sum(1 for d in DASH if d < i),
        "lowbef": sum(len([1 for j in range(i) if S[j].islower()]) for _ in [0]),
        "lowaft": len([1 for j in range(i + 1, len(S)) if S[j].islower()]),
        "signed": signed,
        "all": sum(LV(c) for c in S if c.islower()),
        "capsum": sum(CV(S[j]) for j in CAP),
    }
    return f


FEAT = context(CAP[0]).keys()
CTX = {i: context(i) for i in CAP}
print("features:", len(FEAT))


def build(expr):
    """expr: callable(i)->int shift applied to the capital's own value"""
    out = []
    for i in CAP:
        n = CV(S[i]) + expr(i)
        out.append(chr((n - 1) % 26 + 97))
    return "".join(out)


tested = 0
hits = 0
seen = {}
# single-feature: out = cap + a*f + k
for f in FEAT:
    for a in (-2, -1, 1, 2):
        for k in range(26):
            s = build(lambda i, f=f, a=a, k=k: a * CTX[i][f] + k)
            seen.setdefault(s, "1f|%s*%d+%d" % (f, a, k))
# pairwise: out = cap + a*f1 + b*f2 + k
for f1, f2 in itertools.combinations(FEAT, 2):
    for a in (-1, 1):
        for b in (-1, 1):
            for k in (0, 1, 2, 3, 12, 13, 14, 25):
                s = build(lambda i, f1=f1, f2=f2, a=a, b=b, k=k:
                          a * CTX[i][f1] + b * CTX[i][f2] + k)
                seen.setdefault(s, "2f|%s*%d %s*%d +%d" % (f1, a, f2, b, k))
print("distinct scramble candidates from arithmetic rules:", len(seen))

for sc, tag in seen.items():
    for skn, sky in SKIES.items():
        tested += 1
        r = segment_oracle(4, (sc + sky).encode())
        if r:
            hits += 1
            print("MATCH!!! scramble=%s (%s) sky=%s -> %s" % (sc, tag, skn, r.hex()))
print("tested %d, hits %d" % (tested, hits))
