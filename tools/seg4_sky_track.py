#!/usr/bin/env python3
"""Segment 4, round 3: clue-8 track-pairing search, with CORRECTED track lengths.

Two things this establishes:

(A) The "cell value indexes its assigned track" reading (the pasted analysis's
    starred next target, and the repo's own "non-positional pairing" hope) is
    impossible for *every* assignment of the 11 letter-cells to distinct tracks,
    because the clue needs two values >= 18 (cells 10 and 11: R=18, U=21) but the
    album has exactly ONE title of length >= 18 ("thesuffocatingcarrier", 21).
    The previous session's findings claimed three titles were >= 18 (18/22/18);
    the real lengths are 16/21/17, so the original repo's counting argument was
    correct after all.

(B) A systematic family of alternative clue-8 decoders (track selector x letter
    position), each producing an 11-letter string whose alphabet positions are
    concatenated; the length-17 results are crossed with the clue-2 scramble
    candidates against segment 4.
"""
import itertools
import sys

sys.path.insert(0, "tools")
from oracle import segment_oracle  # noqa: E402

TRACKS = ["fewandfarbetween", "thesuffocatingcarrier", "thesurrogate",
          "exitlight", "ghostmarch", "nocturnalsugars", "allartmustdie",
          "daylightbrings", "hillsoflife", "asseenfromafar",
          "thegreatadventure", "sequels", "secondsofdream"]
LEN = [len(t) for t in TRACKS]
CELLS = "ehk-bqNEFRUn-"
LETTERS = [(i + 1, c) for i, c in enumerate(CELLS) if c != "-"]  # 1-based cell
VAL = {i: ord(c.upper()) - 64 for i, c in LETTERS}
ORD = {i: k for k, (i, c) in enumerate(LETTERS, 1)}              # 1-based ordinal

print("track lengths (real, spaces removed):")
for n, t in enumerate(TRACKS, 1):
    print("  %2d %-21s %2d" % (n, t, LEN[n - 1]))
print("letter cells (1-based idx, char, value, ordinal):")
for i, c in LETTERS:
    print("  %2d %s v=%d ord=%d" % (i, c, VAL[i], ORD[i]))


# ---------- (A) impossibility of value-as-index into a distinct track ----------
def can_assign_index():
    """Can we give every letter-cell a DISTINCT track whose length >= its value?"""
    need = sorted(((VAL[i], i) for i, c in LETTERS), reverse=True)
    avail = sorted(LEN, reverse=True)
    # greedy: biggest need gets biggest track; both lists sorted desc, need[k] <= avail[k]
    return all(v <= a for (v, _), a in zip(need, avail)), need, avail


ok, need, avail = can_assign_index()
print("\n(A) value-as-index, distinct tracks: feasible =", ok)
print("    needs (desc):", [v for v, _ in need][:6], "...")
print("    avail (desc):", avail[:6], "...")
big = [(i, VAL[i]) for i, c in LETTERS if VAL[i] >= 18]
print("    cells needing a title of length >= 18:", big,
      "| titles that long:", [t for t in TRACKS if len(t) >= 18])
print("    -> impossible: two cells need the only one such title.")


# ---------- (B) decoder families -> 11-letter strings -> digit concat ----------
def decode(sel, pos):
    out = []
    for i, c in LETTERS:
        v = VAL[i]
        if sel == "v":
            ti = v - 1
        elif sel == "i":
            ti = i - 1
        elif sel == "ord":
            ti = ORD[i] - 1
        elif sel == "vmod13":
            ti = (v - 1) % 13
        elif sel == "vmod13b":
            ti = v % 13
        elif sel == "rev":
            ti = 13 - v
        elif sel == "revmod":
            ti = (13 - v) % 13
        else:
            return None
        if not (0 <= ti < 13):
            out.append("?")
            continue
        t = TRACKS[ti]
        if pos == "v":
            p = v - 1
        elif pos == "i":
            p = i - 1
        elif pos == "ord":
            p = ORD[i] - 1
        elif pos == "len-v":
            p = len(t) - v
        elif pos == "len-ord":
            p = len(t) - ORD[i]
        elif pos == "vmodlen":
            p = v % len(t)
        else:
            return None
        out.append(t[p] if 0 <= p < len(t) else "?")
    return "".join(out)


def digitize(s):
    return "".join(str(ord(ch.upper()) - 64) for ch in s if ch.isalpha())


sels = ["v", "i", "ord", "vmod13", "vmod13b", "rev", "revmod"]
poss = ["v", "i", "ord", "len-v", "len-ord", "vmodlen"]
skies = {}
for sel in sels:
    for pos in poss:
        s = decode(sel, pos)
        if s is None:
            continue
        d = digitize(s)
        tag = "%s|%s" % (sel, pos)
        print("  %-14s letters=%-12s digits=%-20s len=%d" % (tag, s, d, len(d)))
        if len(d) == 17:
            skies.setdefault(d, tag)
print("\n=> distinct 17-digit skies from these families:", len(skies))
for d, tag in skies.items():
    print("   ", d, "<-", tag)


# ---------- clue-2 scramble candidate generator (compact) ----------
S = "s-bcBPEFfJDfeFmksmPOkChDhrgBqjD-i---ffeNB"
CAP_IDX = [i for i, c in enumerate(S) if c.isupper()]
DASH_IDX = [i for i, c in enumerate(S) if c == "-"]
VALc = lambda ch: ord(ch.upper()) - 64
LOVc = lambda ch: ord(ch) - 96


def feat(i):
    prev_low = next((j for j in range(i - 1, -1, -1) if S[j].islower()), None)
    runB = []
    j = i - 1
    while j >= 0 and S[j].islower():
        runB.append(LOVc(S[j]))
        j -= 1
    runB.reverse()
    runA = []
    j = i + 1
    while j < len(S) and S[j].islower():
        runA.append(LOVc(S[j]))
        j += 1
    next_low = next((j for j in range(i + 1, len(S)) if S[j].islower()), None)
    d = {
        "prev_low": LOVc(S[prev_low]) if prev_low is not None else 0,
        "next_low": LOVc(S[next_low]) if next_low is not None else 0,
        "dist_prev": i - prev_low if prev_low is not None else 0,
        "dist_next": next_low - i if next_low is not None else 0,
        "runb_sum": sum(runB), "runa_sum": sum(runA),
        "runb_cnt": len(runB), "runa_cnt": len(runA),
        "runb_first": runB[0] if runB else 0, "runb_last": runB[-1] if runB else 0,
        "runb_max": max(runB) if runB else 0, "runb_min": min(runB) if runB else 0,
        "runa_first": runA[0] if runA else 0, "runa_last": runA[-1] if runA else 0,
        "runa_max": max(runA) if runA else 0, "runa_min": min(runA) if runA else 0,
        "ordinal": CAP_IDX.index(i) + 1, "idx": i,
        "chunk": sum(1 for x in DASH_IDX if x < i),
    }
    lo = max([x for x in DASH_IDX if x < i], default=-1)
    hi = min([x for x in DASH_IDX if x > i], default=len(S))
    inb = [LOVc(S[j]) for j in range(lo + 1, i) if S[j].islower()]
    ina = [LOVc(S[j]) for j in range(i + 1, hi) if S[j].islower()]
    d["chunk_before_sum"] = sum(inb)
    d["chunk_after_sum"] = sum(ina)
    d["chunk_before_cnt"] = len(inb)
    d["chunk_after_cnt"] = len(ina)
    return d


MF = {i: feat(i) for i in CAP_IDX}


def scramble_cands():
    out = {}
    for f in ("prev_low", "next_low", "dist_prev", "dist_next", "runb_sum",
              "runa_sum", "runb_cnt", "runa_cnt", "runb_first", "runb_last",
              "runb_max", "runb_min", "runa_first", "runa_last", "runa_max",
              "runa_min", "ordinal", "idx", "chunk", "chunk_before_sum",
              "chunk_after_sum", "chunk_before_cnt", "chunk_after_cnt"):
        for op in ("+", "-"):
            for k in range(26):
                for mp in ("a1", "a0", "A1"):
                    w = []
                    for i in CAP_IDX:
                        n = VALc(S[i]) + MF[i][f] + k if op == "+" else VALc(S[i]) - MF[i][f] + k
                        if mp == "a1":
                            w.append(chr((n - 1) % 26 + 97))
                        elif mp == "a0":
                            w.append(chr(n % 26 + 97))
                        else:
                            w.append(chr((n - 1) % 26 + 65))
                    s = "".join(w)
                    if s.isalpha():
                        out.setdefault(s.lower(), "A|%s%s+%d|%s" % (f, op, k, mp))
    # family B: position walks mod m
    for f in ("prev_low", "next_low", "dist_prev", "dist_next", "idx", "runb_sum", "runa_sum"):
        for op in ("+", "-"):
            for mod in (41, 40, 39, 33, 26, 15):
                for k in range(mod):
                    w = []
                    for i in CAP_IDX:
                        x = MF[i][f]
                        p = (i + x + k) % mod if op == "+" else (i - x + k) % mod
                        ch = S[p]
                        w.append(ch.lower() if ch.isalpha() else "")
                    s = "".join(w)
                    if s.isalpha():
                        out.setdefault(s, "B|%s%s mod%d +%d" % (f, op, mod, k))
    # running arithmetic
    for res in (True, False):
        for k in range(26):
            w = []
            tot = 0
            for ch in S:
                if ch == "-":
                    if res:
                        tot = 0
                    continue
                tot += VALc(ch) if ch.isupper() else -LOVc(ch)
                if ch.isupper():
                    w.append(chr((tot + k - 1) % 26 + 97))
            s = "".join(w)
            if s.isalpha():
                out.setdefault(s.lower(), "C|running res=%s +%d" % (res, k))
    return out


sc = scramble_cands()
print("\nscramble candidates:", len(sc))

# ---------- cross ----------
DIG = "58112171456182114"

# WITNESS-CONSISTENT SCHEME (new): each cell selects a track -- a letter cell by
# its alphabet value wrapped into 1..13, a dash by its own position -- and the
# output letter is that track's (cell-index)-th character.  Both author examples
# fall out exactly: cell 4 (dash -> track 4 = exitlight -> exitlight[4] = T) and
# cell 8 ('E' value 5 -> track 5 = ghostmarch -> ghostmarch[8] = R).
def witness_decode(cells):
    out = []
    for i, ch in enumerate(cells, 1):
        n = i if ch == "-" else ((ord(ch.upper()) - 64 - 1) % 13) + 1
        t = TRACKS[n - 1]
        out.append(t[i - 1] if 1 <= i <= len(t) else "?")
    return "".join(out)


w13 = witness_decode(CELLS)
w12 = witness_decode(CELLS[:-1])
w11 = witness_decode(CELLS.replace("-", ""))
for tag, w in (("witness13", w13), ("witness12", w12), ("witness11", w11)):
    wd = digitize(w)
    print("  %-10s letters=%-12s digits=%s len=%d" % (tag, w, wd, len(wd)))

allskies = dict(skies)
allskies[DIG] = "repo|digits"
if len(digitize(w13)) == 17:
    allskies[digitize(w13)] = "witness13"
if len(digitize(w12)) == 17:
    allskies[digitize(w12)] = "witness12"
if len(digitize(w11)) == 17:
    allskies[digitize(w11)] = "witness11"
print("sky candidates:", len(allskies))

hits = 0
tested = 0
for s, sn in sc.items():
    for sky, kn in allskies.items():
        tested += 1
        r = segment_oracle(4, (s + sky).encode())
        if r:
            hits += 1
            print("MATCH!!! scramble=%s (%s) sky=%s (%s) -> %s" % (s, sn, sky, kn, r.hex()))
print("tested %d pairs, hits %d" % (tested, hits))

# ---------- pasted-claim checks ----------
print("\n-- pasted claim checks --")
rule = "".join(chr((VALc(S[i]) + MF[i]["prev_low"] - 1) % 26 + 97) for i in CAP_IDX)
print("capital + nearest preceding lowercase  ->", rule.upper(),
      "(in candidate set:", rule in sc, ")")
print("  its seg4 verdict with sky=digits    ->",
      "MATCH" if segment_oracle(4, (rule + DIG).encode()) else "NO MATCH")
