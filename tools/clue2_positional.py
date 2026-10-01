#!/usr/bin/env python3
"""Clue 2, round 6: POSITIONAL families (new).

Every previous clue-2 sweep changed the *letters*: capital values were shifted
by context numbers and the 15 capitals re-emitted. None of them moved the
*characters themselves*. But the clue is literally called "scramble", and its
instruction -- "With your capital, addition. To the lower, subtract." -- reads
naturally as a displacement: capitals travel forward, lowercase travels back.

This tool builds that family:
  * each cell gets a displacement d  (value / ordinal / index / distance /
    word-length / constant), signed by case or not;
  * new position = old position +/- d;
  * the string is re-ordered by the new position (stable), or binned;
  * readings are taken: the reordered string's letters, its capitals, its
    first 15 letters, its lowercase, etc.

Also tests two non-displacement ideas from the same sentence: a stable
case-partition ("capitals first" / "lowercase first") and a circular rotation
by the number of capitals.
"""
import itertools
import sys

sys.path.insert(0, "tools")
from oracle import segment_oracle  # noqa: E402

S = "s-bcBPEFfJDfeFmksmPOkChDhrgBqjD-i---ffeNB"
assert len(S) == 41
SKIES = {"witness": "71520219618128920", "repo": "58112171456182114"}

POS = {i: ch for i, ch in enumerate(S)}
CAP = [i for i, c in enumerate(S) if c.isupper()]
LOW = [i for i, c in enumerate(S) if c.islower()]
DASH = [i for i, c in enumerate(S) if c == "-"]
ORDI = {i: k for k, i in enumerate(CAP, 1)}
CV = lambda c: ord(c) - 64
LOV = lambda c: ord(c) - 96


def prev_dash(i):
    return max([d for d in DASH if d < i], default=-1)


def next_dash(i):
    return min([d for d in DASH if d > i], default=len(S))


def displace(i, mode):
    ch = S[i]
    v = CV(ch) if ch.isupper() else (LOV(ch) if ch.islower() else 0)
    if mode == "val":
        return v
    if mode == "one":
        return 1
    if mode == "idx":
        return i
    if mode == "ord":
        return ORDI.get(i, 0)
    if mode == "prevd":
        return i - prev_dash(i)
    if mode == "nextd":
        return next_dash(i) - i
    if mode == "dashcnt":
        return sum(1 for d in DASH if d < i)
    return 0


def reorder(signed, sgn_cap, sgn_low):
    """Return the string re-ordered by new position."""
    keyed = []
    for i, ch in enumerate(S):
        d = signed[i]
        if ch.isupper():
            d *= sgn_cap
        elif ch.islower():
            d *= sgn_low
        else:
            d = 0
        keyed.append((i + d, i, ch))
    keyed.sort(key=lambda t: (t[0], t[1]))
    return "".join(c for _, _, c in keyed)


def readings(X):
    out = set()
    caps = "".join(c for c in X if c.isupper()).lower()
    lows = "".join(c for c in X if c.islower())
    letters = "".join(c for c in X if c.isalpha()).lower()
    if len(caps) == 15:
        out.add(caps)
    # every 15-letter window of the re-ordered letter stream (new: was endpoints only)
    for stream in (letters, X.lower()):
        for start in range(0, max(0, len(stream) - 14)):
            w = stream[start:start + 15]
            if w.isalpha():
                out.add(w)
    return out


cands = {}


def emit(s, tag):
    if len(s) == 15 and s.isalpha():
        cands.setdefault(s.lower(), tag)


for mode in ("val", "one", "idx", "ord", "prevd", "nextd", "dashcnt"):
    signed = {i: displace(i, mode) for i in range(len(S))}
    for sgn_cap, sgn_low in ((1, -1), (-1, 1), (1, 1), (-1, -1)):
        X = reorder(signed, sgn_cap, sgn_low)
        for r in readings(X):
            emit(r, "disp|%s cap%+d low%+d" % (mode, sgn_cap, sgn_low))

# stable case partitions
lows_seq = "".join(c for c in S if not c.isupper())
caps_seq = "".join(c for c in S if c.isupper())
for X, tag in ((lows_seq + caps_seq, "lower-then-cap"),
               (caps_seq + lows_seq, "cap-then-lower")):
    for r in readings(X):
        emit(r, "part|" + tag)

# circular rotations: every offset and every step
for off in range(len(S)):
    X = S[off:] + S[:off]
    for r in readings(X):
        emit(r, "rot|%d" % off)
for step in range(1, len(S)):
    X = "".join(S[(i * step) % len(S)] for i in range(len(S)))
    for r in readings(X):
        emit(r, "step|%d" % step)

# keyboard layouts (monkey/typewriter): qwerty <-> dvorak and row shifts
QW = "qwertyuiopasdfghjklzxcvbnm"
DV = "pyfgcrlaoeuidhtnsqjkxbmwvz"
AZ = "abcdefghijklmnopqrstuvwxyz"
maps = {
    "qw-dv": str.maketrans(QW, DV),
    "dv-qw": str.maketrans(DV, QW),
    "qw-left": str.maketrans(QW, QW[1:] + QW[:1]),
    "qw-right": str.maketrans(QW, QW[-1:] + QW[:-1]),
    "az-shift": str.maketrans(AZ, AZ[1:] + AZ[:1]),
}
for mn, tbl in maps.items():
    for src in (S, caps_seq):
        X = src.translate(tbl)
        if len(X) == 15 and X.isalpha():
            emit(X.lower(), "kbd|%s" % mn)
        for r in readings(X):
            emit(r, "kbd|%s" % mn)

print("distinct candidates:", len(cands))
hits = 0
tested = 0
for sc, tag in cands.items():
    for sky, kn in SKIES.items():
        tested += 1
        res = segment_oracle(4, (sc + sky).encode())
        if res:
            hits += 1
            print("MATCH!!! scramble=%s (%s) sky=%s (%s) -> %s" % (sc, tag, sky, kn, res.hex()))
print("tested %d pairs, hits %d" % (tested, hits))

# show anything that is a real English dictionary word / contains one
try:
    words = set()
    with open("/usr/share/dict/words") as f:
        words = {w.strip().lower() for w in f}
    hits2 = [c for c in cands if c in words]
    print("dictionary hits:", hits2)
except Exception as e:
    print("no system dictionary:", e)
