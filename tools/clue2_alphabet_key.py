#!/usr/bin/env python3
"""Clue 2, round 8: the "26 non-capitals = alphabet key" route.

The one clue-2 property nobody has swept is structural and exact:

    the 41-cell string is 15 capitals + 26 non-capitals (21 lowercase + 5 dashes)

26 is the alphabet size.  Every earlier clue-2 family treated the non-capitals
as *context numbers* (counts/sums/distances) or moved characters around; none
treated the 26 non-capital cells as an *ordered alphabet* that the 15 capitals
index into.  The clue's own instruction -- "WITH YOUR CAPITAL, ADDITION.  TO THE
LOWER, SUBTRACT." -- is at least consistent with reading the 15 capitals through
the 26 non-capitals.

This tool builds that family:

  * number the 26 non-capitals A..Z in reading order (and the 21 lowercase
    separately 1..21);
  * for each capital, take a key = one of  a dozen non-capital features (rank of
    the nearest preceding/following non-capital, count before/after, distance,
    dash count, the non-capital's own letter value, ...);
  * form a letter as (capital value +- key + shift) mod 26 in both a=1 and a=0
    bases, plus the pure-substitution reading ``key`` alone, plus an
    ordering-key reading (sort the capitals by their key);
  * emit every exactly-15-character result and test it against both pinned
    clue-8 skies through the segment-4 oracle.
"""
import itertools
import sys

sys.path.insert(0, "tools")
from oracle import segment_oracle  # noqa: E402

S = "s-bcBPEFfJDfeFmksmPOkChDhrgBqjD-i---ffeNB"
assert len(S) == 41

CAP = [i for i, c in enumerate(S) if c.isupper()]
NON = [i for i, c in enumerate(S) if not c.isupper()]
LOW = [i for i, c in enumerate(S) if c.islower()]
DASH = [i for i, c in enumerate(S) if c == "-"]
assert len(CAP) == 15 and len(NON) == 26 and len(LOW) == 21 and len(DASH) == 5

NON_RANK = {i: k for k, i in enumerate(NON, 1)}     # 1..26, reading order
LOW_RANK = {i: k for k, i in enumerate(LOW, 1)}     # 1..21
CAP_RANK = {i: k for k, i in enumerate(CAP, 1)}
CV = lambda c: ord(c) - 64       # A=1
LOV = lambda c: ord(c) - 96      # a=1

SKIES = {"witness": "71520219618128920", "repo": "58112171456182114"}

cands = {}


def emit(s, tag):
    if s and len(s) == 15 and s.isalpha():
        cands.setdefault(s.lower(), tag)


def prev_of(i, pool):
    c = [p for p in pool if p < i]
    return c[-1] if c else None


def next_of(i, pool):
    c = [p for p in pool if p > i]
    return c[0] if c else None


def feature(i, name):
    """Return an integer key for capital at i (or None if undefined)."""
    pn, nn = prev_of(i, NON), next_of(i, NON)
    pl, nl = prev_of(i, LOW), next_of(i, LOW)
    if name == "prev_nc":
        return NON_RANK[pn] if pn is not None else None
    if name == "next_nc":
        return NON_RANK[nn] if nn is not None else None
    if name == "prev_nc_val":
        if pn is None:
            return None
        return LOV(S[pn]) if S[pn].islower() else 0
    if name == "next_nc_val":
        if nn is None:
            return None
        return LOV(S[nn]) if S[nn].islower() else 0
    if name == "nr_before":
        return sum(1 for p in NON if p < i)
    if name == "nr_after":
        return sum(1 for p in NON if p > i)
    if name == "lw_before":
        return sum(1 for p in LOW if p < i)
    if name == "lw_after":
        return sum(1 for p in LOW if p > i)
    if name == "dist_prev_nc":
        return i - pn if pn is not None else None
    if name == "dist_next_nc":
        return nn - i if nn is not None else None
    if name == "prev_low_rank":
        return LOW_RANK[pl] if pl is not None else None
    if name == "next_low_rank":
        return LOW_RANK[nl] if nl is not None else None
    if name == "prev_low_val":
        return LOV(S[pl]) if pl is not None else None
    if name == "next_low_val":
        return LOV(S[nl]) if nl is not None else None
    if name == "dash_before":
        return sum(1 for p in DASH if p < i)
    if name == "dash_after":
        return sum(1 for p in DASH if p > i)
    if name == "cap_rank":
        return CAP_RANK[i]
    if name == "idx":
        return i
    raise ValueError(name)


FEATURES = ["prev_nc", "next_nc", "prev_nc_val", "next_nc_val", "nr_before",
            "nr_after", "lw_before", "lw_after", "dist_prev_nc", "dist_next_nc",
            "prev_low_rank", "next_low_rank", "prev_low_val", "next_low_val",
            "dash_before", "dash_after", "cap_rank", "idx"]


def letters_from(nums, base):
    """base 'a1': 1->a ; base 'a0': 0->a."""
    out = []
    for n in nums:
        if base == "a1":
            out.append(chr((n - 1) % 26 + 97))
        else:
            out.append(chr(n % 26 + 97))
    return "".join(out)


def main():
    n_keys = 0
    for feat in FEATURES:
        keys = [feature(i, feat) for i in CAP]
        if any(k is None for k in keys):
            continue
        n_keys += 1
        capv = [CV(S[i]) for i in CAP]
        for op in ("+", "-", "key-", "key+"):
            for shift in range(26):
                nums = []
                for k, v in zip(keys, capv):
                    if op == "+":
                        nums.append(v + k + shift)
                    elif op == "-":
                        nums.append(v - k + shift)
                    elif op == "key-":
                        nums.append(k - v + shift)
                    else:
                        nums.append(k + shift)
                for base in ("a1", "a0"):
                    emit(letters_from(nums, base),
                         "alg|%s|%s|+%d|%s" % (feat, op, shift, base))
        # pure substitution: key alone (shift sweep already covered above as key+)
        # ordering-key: sort capitals by their key, read the capitals
        for rev in (False, True):
            order = sorted(range(15), key=lambda j: (keys[j], j), reverse=rev)
            emit("".join(chr((capv[j] - 1) % 26 + 97) for j in order).lower(),
                 "algorder|%s|rev%d" % (feat, rev))

    print("features usable:", n_keys)
    print("distinct 15-char candidates:", len(cands))

    tested = hits = 0
    for sc, tag in cands.items():
        for sky, kn in SKIES.items():
            tested += 1
            r = segment_oracle(4, (sc + sky).encode())
            if r:
                hits += 1
                print("MATCH!!! scramble=%s (%s) sky=%s (%s) -> %s"
                      % (sc, tag, sky, kn, r.hex()))
    print("tested %d pairs, hits %d" % (tested, hits))
    return 0


if __name__ == "__main__":
    sys.exit(main())
