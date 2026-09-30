#!/usr/bin/env python3
"""Clue 2 (scramble) mechanics: the 15 capitals are the 15 answer characters,
scrambled. "With your capital, addition. To the lower, subtract." -- use
capital/lowercase arithmetic to order or shift them. Cross with sky=digits.
"""
import sys
sys.path.insert(0, "tools")
from oracle import segment_oracle  # noqa: E402

S = "s-bcBPEFfJDfeFmksmPOkChDhrgBqjD-i---ffeNB"
SKY = "58112171456182114"

caps = [(i, c) for i, c in enumerate(S) if c.isupper()]
lows = [(i, c) for i, c in enumerate(S) if c.islower()]
dashes = [i for i, c in enumerate(S) if c == "-"]
print("caps %d lows %d dashes %d" % (len(caps), len(lows), len(dashes)))

val = {c: ord(c) - 64 for _, c in caps}
lowval = {c: ord(c) - 96 for _, c in lows}


def around(i):
    """lowercase aggregate around the capital at index i"""
    before = [lowval[v] for j, v in lows if j < i]
    after = [lowval[v] for j, v in lows if j > i]
    return before, after


def agg(lst, how):
    if not lst:
        return 0
    if how == "sum":
        return sum(lst)
    if how == "count":
        return len(lst)
    if how == "first":
        return lst[0]
    if how == "last":
        return lst[-1]
    if how == "max":
        return max(lst)
    if how == "min":
        return min(lst)
    if how == "span":
        return abs(lst[0] - lst[-1])
    return 0


letters = "abcdefghijklmnopqrstuvwxyz"
cands = {}


def emit(name, s):
    if len(s) == 15 and all(ch.isalpha() for ch in s):
        cands[name] = s.lower()


# 1) shifts of each capital by lowercase aggregates
for side in ("before", "after"):
    for how in ("sum", "count", "first", "last", "max", "min", "span"):
        for op in ("-", "+"):
            out = ""
            for i, c in caps:
                b, a = around(i)
                v = val[c] + (agg(b if side == "before" else a, how)
                              if op == "+" else -agg(b if side == "before" else a, how))
                out += letters[(v - 1) % 26]
            emit("shift_%s_%s_%s" % (side, how, op), out)
    # modulo by the opposite side's total
    total = sum(lowval[v] for _, v in lows)
    out = "".join(letters[(val[c] + (total if side == "before" else -total) - 1) % 26]
                  for _, c in caps)
    emit("shift_total_%s" % side, out)

# 2) sort the capitals by keys that mix value and counts
keys = {}
for name in ("val",):
    keys["val"] = lambda i, c: val[c]
keys["pos"] = lambda i, c: i
for side in ("before", "after"):
    for how in ("count", "sum"):
        for op in ("+", "-"):
            def mk(side, how, op):
                def f(i, c):
                    b, a = around(i)
                    x = agg(b if side == "before" else a, how)
                    return val[c] + x if op == "+" else val[c] - x
                return f
            keys["%s_%s_%s" % (side, how, op)] = mk(side, how, op)
for kn, kf in keys.items():
    order = sorted(caps, key=lambda t: kf(*t))
    emit("order_%s" % kn, "".join(c for _, c in order))
    emit("order_%s_rev" % kn, "".join(c for _, c in reversed(order)))
    # also: keys give target positions, place capitals at those slots
    pos = sorted(range(15), key=lambda k: kf(*caps[k]))
    out = [None] * 15
    for slot, src in zip(pos, [c for _, c in caps]):
        out[slot] = src
    emit("place_%s" % kn, "".join(out))

# 3) interleave: capitals shifted by the lowercase immediately following, read
#    at positions given by the lowercase total (several moduli)
tot = sum(lowval[v] for _, v in lows)
for mult in (1, 2, 3):
    for div in (41, 36, 26, 15):
        step = (tot * mult) % div
        if step == 0:
            continue
        out = "".join(S[(k * step) % 41] for k in range(15))
        emit("index_walk_%d_%d" % (mult, div), out)

print("candidate count:", len(cands))
hits = []
for name, sc in cands.items():
    for sky_name, sky in (("digits", SKY),):
        r = segment_oracle(4, (sc + sky).encode())
        if r:
            hits.append((name, sc, r.hex()))
print("tested:", len(cands), "hits:", len(hits))
for h in hits:
    print("MATCH", h)
for k in sorted(cands):
    print("%-28s %s" % (k, cands[k]))
