#!/usr/bin/env python3
"""Round 4: wide clue-2 sweep against the two pinned clue-8 skies.

New structural families relative to rounds 2/3:
  * equal-rank pairing: k-th capital with k-th lowercase (in order / reversed /
    sorted by value), added or subtracted, with shifts and alphabet maps;
  * linear combos of up to three context features with coefficients in -2..2;
  * permutation families (capitals re-ordered by a context key);
  * character-at-position families (take a letter out of the 41-cell string);
  * running signed totals sampled at capitals, with dash resets and value bases.
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
CV = lambda c: ord(c.upper()) - 64
LV = lambda c: ord(c) - 96

SKIES = {"witness": "71520219618128920", "repo": "58112171456182114"}

cands = {}


def emit(s, tag):
    if len(s) == 15 and s.isalpha():
        cands.setdefault(s.lower(), tag)


# ---------------- equal-rank capital/lowercase pairing ----------------
CAPS = [S[i] for i in CAP]
LOWS = [S[i] for i in LOW]
orders = {
    "order": LOWS,
    "rev": LOWS[::-1],
    "val": sorted(LOWS, key=CV),
    "valrev": sorted(LOWS, key=CV, reverse=True),
}
for on, lo in orders.items():
    for k in range(15):
        pass
    for op in ("+", "-"):
        for base in (1, 0):
            for c in range(26):
                w = []
                for k in range(15):
                    a = CV(CAPS[k])
                    b = CV(lo[k])
                    n = a + b + c if op == "+" else a - b + c
                    w.append(chr((n - base) % 26 + 97))
                emit("".join(w), "pair|%s%s c%d b%d" % (on, op, c, base))
# k-th capital with k-th lowercase but capital indexed from the end
for op in ("+", "-"):
    for c in range(26):
        w = []
        for k in range(15):
            a = CV(CAPS[14 - k])
            b = CV(LOWS[k])
            n = a + b + c if op == "+" else a - b + c
            w.append(chr((n - 1) % 26 + 97))
        emit("".join(w), "pairZ|%s c%d" % (op, c))

print("after pairing families:", len(cands))

# ---------------- context features ----------------
def ctx(i):
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
    signed = 0
    for j in range(i):
        signed += CV(S[j]) if S[j].isupper() else -LV(S[j])
    return {
        "z": 0,
        "k": CAP.index(i) + 1,
        "i": i,
        "prev": LV(S[prev_low]) if prev_low is not None else 0,
        "next": LV(S[next_low]) if next_low is not None else 0,
        "rbs": sum(runB), "rbc": len(runB), "rbf": runB[0] if runB else 0,
        "rbl": runB[-1] if runB else 0,
        "ras": sum(runA), "rac": len(runA), "raf": runA[0] if runA else 0,
        "ral": runA[-1] if runA else 0,
        "signed": signed,
        "d": sum(1 for x in DASH if x < i),
        "lb": sum(1 for j in range(i) if S[j].islower()),
        "la": sum(1 for j in range(i + 1, len(S)) if S[j].islower()),
    }


CTX = {i: ctx(i) for i in CAP}
FEAT = sorted(CTX[CAP[0]].keys())
print("features:", FEAT)

# two- and three-feature linear combos
for combo_size in (1, 2, 3):
    feats = [f for f in FEAT if f != "z"]
    for combo in itertools.combinations(feats, combo_size):
        for coeffs in itertools.product((-2, -1, 1, 2), repeat=combo_size):
            for c in range(0, 26, 1):
                w = []
                for i in CAP:
                    n = CV(S[i]) + c
                    for f, a in zip(combo, coeffs):
                        n += a * CTX[i][f]
                    w.append(chr((n - 1) % 26 + 97))
                emit("".join(w), "lin|%s" % str(tuple(zip(combo, coeffs))))
        if combo_size >= 2 and len(cands) > 4_000_000:
            break
print("after linear families:", len(cands))

# ---------------- permutation families ----------------
keys = {
    "val": lambda i: CV(S[i]),
    "prev": lambda i: CTX[i]["prev"],
    "next": lambda i: CTX[i]["next"],
    "rbs": lambda i: CTX[i]["rbs"],
    "ras": lambda i: CTX[i]["ras"],
    "i": lambda i: i,
    "signed": lambda i: CTX[i]["signed"],
}
for kn, kf in keys.items():
    for rev in (False, True):
        order = sorted(CAP, key=kf, reverse=rev)
        for op in ("+", "-"):
            for c in range(0, 26, 1):
                w = []
                for i in order:
                    n = CV(S[i]) + c if op == "+" else CV(S[i]) - c
                    w.append(chr((n - 1) % 26 + 97))
                emit("".join(w), "perm|%s rev%d %s c%d" % (kn, rev, op, c))
print("after permutation families:", len(cands))

# ---------------- character-at-position families ----------------
for f in FEAT:
    for op in ("+", "-"):
        for mod in (41, 40, 39, 33, 26, 15):
            for k in range(mod):
                w = []
                for i in CAP:
                    x = CTX[i][f]
                    p = (i + x + k) % mod if op == "+" else (i - x + k) % mod
                    ch = S[p]
                    w.append(ch.upper() if ch.isalpha() else "")
                s = "".join(w)
                if s.isalpha():
                    emit(s, "charpos|%s%s mod%d+%d" % (f, op, mod, k))
print("after charpos families:", len(cands))

# ---------------- running families ----------------
for valmode in ("alpha", "idx", "one"):
    for res in (True, False):
        for c in range(0, 26, 1):
            for base in (1, 0):
                w = []
                tot = 0
                for j, ch in enumerate(S):
                    if ch == "-":
                        if res:
                            tot = 0
                        continue
                    v = CV(ch) if ch.isupper() else LV(ch)
                    if valmode == "idx":
                        v = j
                    elif valmode == "one":
                        v = 1
                    tot += v if ch.isupper() else -v
                    if ch.isupper():
                        w.append(chr((tot + c - base) % 26 + 97))
                s = "".join(w)
                if s.isalpha():
                    emit(s, "run|%s res%d c%d b%d" % (valmode, res, c, base))
print("after running families:", len(cands))

# ---------------- test ----------------
tested = 0
hits = 0
for sc, tag in cands.items():
    for skn, sky in SKIES.items():
        tested += 1
        r = segment_oracle(4, (sc + sky).encode())
        if r:
            hits += 1
            print("MATCH!!! scramble=%s (%s) sky=%s -> %s" % (sc, tag, skn, r.hex()))
print("distinct scramble candidates:", len(cands))
print("tested %d pairs, hits %d" % (tested, hits))
