#!/usr/bin/env python3
"""Segment 4: the two structural readings nobody has crossed yet.

scramble (15): the 15 capitals of "s-bcBPEFfJDfeFmksmPOkChDhrgBqjD-i---ffeNB"
               in order -- "With your capital, addition / To the lower,
               subtract" = keep the capitals, drop the lowercase.
sky (17):      "ehk-bqNEFRUn-" letters -> alphabet positions, concatenated
               decimal = 58112171456182114 (17 digits, exact length).
"""
import sys
sys.path.insert(0, "tools")
from oracle import segment_oracle, ANSWER_LEN  # noqa: E402

S = "s-bcBPEFfJDfeFmksmPOkChDhrgBqjD-i---ffeNB"
caps = "".join(c for c in S if c.isupper())
print("capitals in order:", caps, len(caps), "(need", ANSWER_LEN[2], ")")
lowers = "".join(c for c in S if c.islower())
print("lowers in order  :", lowers, len(lowers))

SKY_DIGITS = "58112171456182114"
assert len(SKY_DIGITS) == ANSWER_LEN[8]

scramble_vars = {
    "caps-in-order": caps,
    "caps-reversed": caps[::-1],
    "caps-swapped-case": caps.lower(),
    "lowers-in-order": lowers,
    "caps+lowers-trunc": (caps + lowers)[:15],
}
# also: every rotation of the caps (the anagrams may define a start point)
for i in range(1, 15):
    scramble_vars["caps-rot%d" % i] = caps[i:] + caps[:i]

hits = 0
n = 0
for name, sc in scramble_vars.items():
    if len(sc.lower()) != ANSWER_LEN[2]:
        continue
    n += 1
    key = (sc.lower() + SKY_DIGITS).encode()
    r = segment_oracle(4, key)
    print("%-20s %-15s %s" % (name, sc, "MATCH!!!" if r else "no"))
    if r:
        hits += 1
        print("super_key bytes 24-31 =", r.hex())
print("tested", n, "scramble variants x sky-digits:", "HIT" if hits else "no hit")

# bonus: dash positions 2,32,34,35,36 (1-based) as a binary mask over 41 cells?
# 41 cells -> not 15; but the LETTERS (36) with dashes as separators... skip.
# bonus: sky letters -> track-letter lookup needs verified tracklist; instead
# test sky as the 11 letters + dashes (13) -- wrong length, oracle would reject.

# also cross: maybe scramble is the caps WITH their original case (clue 2 is
# lowercased by fix_clues -- the oracle already lowercases; try raw too).
key = (caps + SKY_DIGITS).encode()
print("raw-case attempt:", segment_oracle(4, key) or "no")
