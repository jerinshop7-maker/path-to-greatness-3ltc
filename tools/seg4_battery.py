#!/usr/bin/env python3
"""Clue 2 (scramble) mechanical battery x clue 8 (sky) readings, segment 4.

String: s-bcBPEFfJDfeFmksmPOkChDhrgBqjD-i---ffeNB  (41 cells)
Instruction (the anagram line): "With your capital, addition /
to the lower, subtract."  15 capitals, 21 lowercase, 5 dashes.
"""
import sys
import itertools
sys.path.insert(0, "tools")
from oracle import segment_oracle  # noqa: E402

S = "s-bcBPEFfJDfeFmksmPOkChDhrgBqjD-i---ffeNB"
CAPS = "".join(c for c in S if c.isupper())
LOWS = "".join(c for c in S if c.islower())
L = len(S)
assert L == 41 and len(CAPS) == 15

cands = {}
cands["caps"] = CAPS.lower()
cands["caps_rev"] = CAPS[::-1].lower()
cands["lows_trunc"] = LOWS[:15]
cands["lows_tail"] = LOWS[-15:]

# 1) letters at the positions given by each capital's alphabet value
for base in (0, 1):
    v = [ord(c) - 64 - base for c in CAPS]
    s = "".join(S[i] if 0 <= i < L else "?" for i in v)
    cands["caps_as_pos_base%d" % base] = s
    # iterated: apply the same walk twice
    s2 = "".join(S[ord(S[i]) - 64 - base] if 0 <= ord(S[i]) - 64 - base < L else "?"
                 for i in v)
    cands["caps_as_pos_iter%d" % base] = s2

# 2) +1 for capitals, -1 for lowercase, then keep capitals of the result
shift = []
for c in S:
    if c == "-":
        shift.append("-")
    elif c.isupper():
        shift.append(chr((ord(c) - 65 + 1) % 26 + 65))
    else:
        shift.append(chr((ord(c) - 97 - 1) % 26 + 97))
shift = "".join(shift)
cands["shift_keepcaps"] = "".join(c for c in shift if c.isupper()).lower()
cands["shift_keep_newcaps"] = "".join(c for c in shift if c.isalpha())[:15]

# 3) running capital-add / lower-subtract total at each capital -> letters
run = []
tot = 0
for c in S:
    if c.isupper():
        tot += ord(c) - 64
        run.append(tot)
    elif c.islower():
        tot -= ord(c) - 96
vals = run
cands["running_mod26"] = "".join(chr((v - 1) % 26 + 97) for v in vals)
cands["running_abs_mod26"] = "".join(chr((abs(v) - 1) % 26 + 97) for v in vals)
cands["running_diff"] = "".join(chr((vals[i] - vals[i - 1] - 1) % 26 + 97)
                                for i in range(1, len(vals)))
print("running totals at capitals:", vals)

# 4) take letters between consecutive capitals (the "lower" between the caps)
groups = []
cur = ""
for c in S:
    if c.isupper():
        groups.append(cur)
        cur = ""
    elif c.islower():
        cur += c
groups.append(cur)
cands["lowers_between"] = "".join(g[:1] for g in groups if g)[:15]
cands["lowers_between_tail"] = "".join(g[-1:] for g in groups if g)[:15]

# 5) drop lowercase entirely -> 15 caps already; try caps interleaved with the
#    dashes and the *last* lowercase of each run
cands["caps_lastlows"] = "".join(
    (CAPS[i] + (groups[i][-1] if i < len(groups) and groups[i] else ""))
    for i in range(len(CAPS)))[:15].lower()

print("candidate count:", len(cands))

SKY = {
    "digits": "58112171456182114",
    "digits_as_letters": "ehkbqnefrun",  # wrong length, filtered
}
hits = 0
tested = 0
for name, sc in cands.items():
    for sky_name, sky in SKY.items():
        if len(sc.lower()) != 15 or len(sky) != 17:
            continue
        tested += 1
        r = segment_oracle(4, (sc.lower() + sky).encode())
        if r:
            hits += 1
            print("MATCH! scramble=%r (%s) sky=%s -> %s" % (sc, name, sky_name, r.hex()))
print("tested:", tested, "hits:", hits)
for k, v in cands.items():
    print("%-22s %r" % (k, v))
