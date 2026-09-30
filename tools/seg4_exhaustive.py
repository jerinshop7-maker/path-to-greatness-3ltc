#!/usr/bin/env python3
"""Segment 4 exhaustive pass: clue 2 arithmetic x clue 8 candidates.

Clue 2 string (41 cells, 0-based here):
  s-bcBPEFfJDfeFmksmPOkChDhrgBqjD-i---ffeNB
  15 capitals, 21 lowercase, 5 dashes at 1,31,33,34,35 (0-based) = 2,32,34,35,36 1-based.
Instruction (the anagram line): "With your capital, addition / to the lower, subtract."

This builds the *systematic* capital/lowercase arithmetic family (not just the
handful in scramble_battery2.py), including dash-boundary resets, constant
shifts, several alphabet mappings, and position-walk outputs, then crosses them
with every plausible 17-character clue-8 reading.
"""
import itertools
import sys
sys.path.insert(0, "tools")
from oracle import segment_oracle  # noqa: E402

S = "s-bcBPEFfJDfeFmksmPOkChDhrgBqjD-i---ffeNB"
assert len(S) == 41
CAP_IDX = [i for i, c in enumerate(S) if c.isupper()]
LOW_IDX = [i for i, c in enumerate(S) if c.islower()]
DASH_IDX = [i for i, c in enumerate(S) if c == "-"]
print("capitals %d at %s" % (len(CAP_IDX), CAP_IDX))
print("dashes at %s (0-based) -> 1-based %s" % (DASH_IDX, [i + 1 for i in DASH_IDX]))
VAL = lambda ch: ord(ch.upper()) - 64          # A=1
LOVAL = lambda ch: ord(ch) - 96                # a=1


def features(i):
    """numeric features for the capital at index i"""
    f = {}
    prev_low = next((j for j in range(i - 1, -1, -1) if S[j].islower()), None)
    next_low = next((j for j in range(i + 1, len(S)) if S[j].islower()), None)
    f["prev_low"] = LOVAL(S[prev_low]) if prev_low is not None else 0
    f["next_low"] = LOVAL(S[next_low]) if next_low is not None else 0
    f["dist_prev"] = i - prev_low if prev_low is not None else 0
    f["dist_next"] = next_low - i if next_low is not None else 0
    # contiguous runs
    runB = []
    j = i - 1
    while j >= 0 and S[j].islower():
        runB.append(LOVAL(S[j]))
        j -= 1
    runB.reverse()
    runA = []
    j = i + 1
    while j < len(S) and S[j].islower():
        runA.append(LOVAL(S[j]))
        j += 1
    for tag, run in (("runb", runB), ("runa", runA)):
        f[tag + "_sum"] = sum(run)
        f[tag + "_cnt"] = len(run)
        f[tag + "_first"] = run[0] if run else 0
        f[tag + "_last"] = run[-1] if run else 0
        f[tag + "_max"] = max(run) if run else 0
        f[tag + "_min"] = min(run) if run else 0
    # chunk index (dash separated) and ordinal
    f["chunk"] = sum(1 for d in DASH_IDX if d < i)
    f["ordinal"] = CAP_IDX.index(i) + 1
    f["idx"] = i
    # lowercase before / after in the same chunk
    lo = max([d for d in DASH_IDX if d < i], default=-1)
    hi = min([d for d in DASH_IDX if d > i], default=len(S))
    inb = [LOVAL(S[j]) for j in range(lo + 1, i) if S[j].islower()]
    ina = [LOVAL(S[j]) for j in range(i + 1, hi) if S[j].islower()]
    f["chunk_before_sum"] = sum(inb)
    f["chunk_after_sum"] = sum(ina)
    f["chunk_before_cnt"] = len(inb)
    f["chunk_after_cnt"] = len(ina)
    return f


FEATS = sorted(features(CAP_IDX[0]).keys())
print("feature set (%d): %s" % (len(FEATS), FEATS))

MIDX = {}
for i in CAP_IDX:
    MIDX[i] = features(i)

cands = {}


def emit(name, s):
    if len(s) == 15 and s.isalpha():
        cands.setdefault(s.lower(), name)


# ---- family A: letter = (capital_value op feature + k) mod 26 ---------------
for feat in FEATS:
    for op in ("+", "-"):
        for k in range(26):
            for mapname in ("a1", "a0", "A1"):
                out = []
                for i in CAP_IDX:
                    v = VAL(S[i])
                    x = MIDX[i][feat]
                    n = v + x + k if op == "+" else v - x + k
                    if mapname == "a1":
                        out.append(chr((n - 1) % 26 + 97))
                    elif mapname == "a0":
                        out.append(chr(n % 26 + 97))
                    else:
                        out.append(chr((n - 1) % 26 + 65))
                emit("A|%s%s+%d|%s" % (feat, op, k, mapname), "".join(out))

print("family A candidates:", len(cands))

# ---- family B: take a character from the string at an arithmetic position ----
for feat in FEATS:
    for op in ("+", "-"):
        for mod in (41, 40, 39, 33, 26, 15):
            for k in range(0, mod):
                out = []
                for i in CAP_IDX:
                    x = MIDX[i][feat]
                    p = (i + x + k) % mod if op == "+" else (i - x + k) % mod
                    ch = S[p]
                    out.append(ch.lower() if ch.isalpha() else "")
                s = "".join(out)
                if len(s) == 15:
                    emit("B|%s%s mod%d +%d" % (feat, op, mod, k), s)

print("families A+B candidates:", len(cands))

# ---- family C: running arithmetic with dash resets, sampled offsets ---------
for mode in ("cum", "cumreset", "alt"):
    for k in range(26):
        out = []
        tot = 0
        for ch in S:
            if ch == "-":
                if mode == "cumreset":
                    tot = 0
                continue
            if mode == "alt":
                tot += VAL(ch) if ch.isupper() else -LOVAL(ch)
            else:
                tot += VAL(ch) if ch.isupper() else -LOVAL(ch)
            if ch.isupper():
                out.append(chr((tot + k - 1) % 26 + 97))
        s = "".join(out)
        if len(s) == 15:
            emit("C|%s+%d" % (mode, k), s)

print("families A+B+C candidates:", len(cands))

# ---- sky candidates (must be 17 chars) --------------------------------------
DIG = "58112171456182114"
SKIES = {
    "digits": DIG,
    "digits_rev": DIG[::-1],
    "digits_sorted_up": "".join(sorted(DIG)),
    "digits_sorted_dn": "".join(sorted(DIG, reverse=True)),
    "digits_shift1": "".join(str((int(d) + 1) % 10) for d in DIG),
    "digits_shift9": "".join(str((int(d) + 9) % 10) for d in DIG),
    "digits_rot2": DIG[2:] + DIG[:2],
    "digits_rot15": DIG[15:] + DIG[:15],
    "letters17": "ehkbqn" + "efrun" + "efrun"[:6],   # 17, placeholder
}
SKIES = {k: v for k, v in SKIES.items() if len(v) == 17}
print("sky candidates:", list(SKIES))

hits = 0
tested = 0
for sc, name in cands.items():
    for skn, sky in SKIES.items():
        tested += 1
        r = segment_oracle(4, (sc + sky).encode())
        if r:
            hits += 1
            print("MATCH!!! scramble=%s (%s) sky=%s (%s) -> %s"
                  % (sc, name, sky, skn, r.hex()))
print("tested %d pairs, hits %d" % (tested, hits))

# ---- verify the pasted 'ESHIPJKCBNLINSG' claim + check it was covered -------
rulev = []
for i in CAP_IDX:
    v = VAL(S[i]) + MIDX[i]["prev_low"]
    rulev.append(chr((v - 1) % 26 + 97))
rule = "".join(rulev)
print("capital + nearest preceding lowercase ->", rule.upper())
print("present in candidate set:", rule.lower() in cands,
      "| family:", cands.get(rule.lower()))
print("its segment-4 verdict with sky=digits:",
      "MATCH" if segment_oracle(4, (rule + DIG).encode()) else "NO MATCH")
