#!/usr/bin/env python3
"""Clue 2, round 9: dashes as operators / capital-lowercase PAIRING.

The round-8 sweep treated each capital cell independently.  The pasted round-8
analysis makes the case that the clue is an *expression*: "WITH YOUR CAPITAL,
ADDITION.  TO THE LOWER, SUBTRACT."  -- capitals add, lowercase subtract, and
the 5 dashes (positions 2,32,34,35,36) split the string into groups.  This tool
builds the family that cell-by-cell sweeps miss:

  (1) DASH-GROUP features.  Each capital takes a key from its dash-delimited
      group: group index, group length, group capital/lowercase counts, the sum
      of the lowercase before/after it *within its group*, the distance to the
      nearest dash, the number of dashes before it, ...  Letter =
      (capital +- key + shift) mod 26 in both bases.

  (2) CAPITAL-LOWERCASE PAIRING.  Every capital is paired with a lowercase
      operand chosen by a rule (nearest before/after, the whole group's first/
      last/sum/extreme, the k-th lowercase overall) and combined:
      (cap + low), (cap - low), (low - cap), (low + low_before - ...).

  (3) DASH AS THE SUBTRACT OPERATOR: the value of everything after the nearest
      dash, etc.

Every exactly-15-character result is tested against both pinned skies.
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

CV = lambda c: ord(c) - 64
LOV = lambda c: ord(c) - 96
SKIES = {"witness": "71520219618128920", "repo": "58112171456182114"}

# dash-delimited groups: list of (start, end) inclusive ranges between dashes
bounds = [-1] + DASH + [len(S)]
GROUPS = [(bounds[k] + 1, bounds[k + 1] - 1) for k in range(len(bounds) - 1)]


def group_of(i):
    for gi, (a, b) in enumerate(GROUPS):
        if a <= i <= b:
            return gi, a, b
    return None


cands = {}


def emit(s, tag):
    if s and len(s) == 15 and s.isalpha():
        cands.setdefault(s.lower(), tag)


def letters(nums, base):
    return "".join(chr((n - 1) % 26 + 97) if base == "a1"
                   else chr(n % 26 + 97) for n in nums)


def feat_grp(i, name):
    gi, a, b = group_of(i)
    lows = [j for j in LOW if a <= j <= b]
    caps = [j for j in CAP if a <= j <= b]
    if name == "grp":
        return gi
    if name == "grp_len":
        return b - a + 1
    if name == "grp_caps":
        return len(caps)
    if name == "grp_lows":
        return len(lows)
    if name == "grp_lowsum":
        return sum(LOV(S[j]) for j in lows)
    if name == "grp_capsum":
        return sum(CV(S[j]) for j in caps)
    if name == "grp_bal":
        return sum(LOV(S[j]) for j in lows) - sum(CV(S[j]) for j in caps)
    if name == "lowsum_before":
        return sum(LOV(S[j]) for j in lows if j < i)
    if name == "lowsum_after":
        return sum(LOV(S[j]) for j in lows if j > i)
    if name == "lowcnt_before":
        return sum(1 for j in lows if j < i)
    if name == "lowcnt_after":
        return sum(1 for j in lows if j > i)
    if name == "dash_before":
        return sum(1 for d in DASH if d < i)
    if name == "dash_after":
        return sum(1 for d in DASH if d > i)
    if name == "dist_prev_dash":
        p = [d for d in DASH if d < i]
        return i - p[-1] if p else 0
    if name == "dist_next_dash":
        n = [d for d in DASH if d > i]
        return n[0] - i if n else 0
    if name == "prev_low":
        p = [j for j in LOW if j < i]
        return LOV(S[p[-1]]) if p else 0
    if name == "next_low":
        n = [j for j in LOW if j > i]
        return LOV(S[n[0]]) if n else 0
    if name == "prev_low_in_grp":
        p = [j for j in lows if j < i]
        return LOV(S[p[-1]]) if p else 0
    if name == "next_low_in_grp":
        n = [j for j in lows if j > i]
        return LOV(S[n[0]]) if n else 0
    if name == "idx":
        return i
    raise ValueError(name)


GRP_FEATS = ["grp", "grp_len", "grp_caps", "grp_lows", "grp_lowsum", "grp_capsum",
             "grp_bal", "lowsum_before", "lowsum_after", "lowcnt_before",
             "lowcnt_after", "dash_before", "dash_after", "dist_prev_dash",
             "dist_next_dash", "prev_low", "next_low", "prev_low_in_grp",
             "next_low_in_grp", "idx"]


def pair_feat(i, name):
    """A lowercase operand paired with the capital at i."""
    lows = [j for j in LOW]
    if name == "nearest_prev":
        p = [j for j in lows if j < i]
        return LOV(S[p[-1]]) if p else None
    if name == "nearest_next":
        n = [j for j in lows if j > i]
        return LOV(S[n[0]]) if n else None
    if name == "first_overall":
        return LOV(S[lows[0]])
    if name == "last_overall":
        return LOV(S[lows[-1]])
    if name == "allsum":
        return sum(LOV(S[j]) for j in lows)
    if name == "grp_first":
        _, a, b = group_of(i)
        gl = [j for j in lows if a <= j <= b]
        return LOV(S[gl[0]]) if gl else None
    if name == "grp_last":
        _, a, b = group_of(i)
        gl = [j for j in lows if a <= j <= b]
        return LOV(S[gl[-1]]) if gl else None
    if name == "grp_sum":
        _, a, b = group_of(i)
        gl = [j for j in lows if a <= j <= b]
        return sum(LOV(S[j]) for j in gl) if gl else None
    if name == "grp_min":
        _, a, b = group_of(i)
        gl = [j for j in lows if a <= j <= b]
        return min(LOV(S[j]) for j in gl) if gl else None
    if name == "grp_max":
        _, a, b = group_of(i)
        gl = [j for j in lows if a <= j <= b]
        return max(LOV(S[j]) for j in gl) if gl else None
    raise ValueError(name)


PAIR_FEATS = ["nearest_prev", "nearest_next", "first_overall", "last_overall",
              "allsum", "grp_first", "grp_last", "grp_sum", "grp_min", "grp_max"]


def main():
    capv = [CV(S[i]) for i in CAP]

    # (1) dash-group features
    n1 = 0
    for f in GRP_FEATS:
        keys = [feat_grp(i, f) for i in CAP]
        n1 += 1
        for op in ("+", "-", "r-", "r+"):
            for shift in range(26):
                nums = []
                for k, v in zip(keys, capv):
                    if op == "+":
                        nums.append(v + k + shift)
                    elif op == "-":
                        nums.append(v - k + shift)
                    elif op == "r-":
                        nums.append(k - v + shift)
                    else:
                        nums.append(k + shift)
                for base in ("a1", "a0"):
                    emit(letters(nums, base), "grp|%s|%s|%d|%s" % (f, op, shift, base))

    # (2) capital x lowercase pairing
    n2 = 0
    for f in PAIR_FEATS:
        ops = [pair_feat(i, f) for i in CAP]
        n2 += 1
        for op in ("+", "-", "r-", "r+"):
            for shift in range(26):
                nums = []
                ok = True
                for o, v in zip(ops, capv):
                    if o is None:
                        ok = False
                        break
                    if op == "+":
                        nums.append(v + o + shift)
                    elif op == "-":
                        nums.append(v - o + shift)
                    elif op == "r-":
                        nums.append(o - v + shift)
                    else:
                        nums.append(o + shift)
                if ok:
                    for base in ("a1", "a0"):
                        emit(letters(nums, base), "pair|%s|%s|%d|%s" % (f, op, shift, base))

    # (3) dash as subtract operator: value of the segment after the nearest dash,
    #     signed by case
    for f in ("dist_next_dash", "dist_prev_dash"):
        keys = [feat_grp(i, f) for i in CAP]
        for op in ("+", "-"):
            for shift in range(26):
                nums = [(v + k + shift if op == "+" else v - k + shift)
                        for k, v in zip(keys, capv)]
                for base in ("a1", "a0"):
                    emit(letters(nums, base), "dash|%s|%s|%d|%s" % (f, op, shift, base))

    print("group features:", n1, "| pair features:", n2)
    print("dash groups:", [S[a:b + 1] for a, b in GROUPS])
    print("distinct 15-char candidates:", len(cands))

    # group-level arithmetic readout (6 groups -> not 15 chars, shown for insight)
    for gi, (a, b) in enumerate(GROUPS):
        seg = S[a:b + 1]
        cs = sum(CV(c) for c in seg if c.isupper())
        ls = sum(LOV(c) for c in seg if c.islower())
        print("  group %d %-30r caps=%2d lows=%2d cap-low=%4d"
              % (gi, seg, cs, ls, cs - ls))

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
