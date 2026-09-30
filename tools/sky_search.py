#!/usr/bin/env python3
"""Systematic clue-8 decode search: the 17 digits x 13 real tracks.

Every scheme maps a number to a letter of a track title. Print readable output.
"""
import itertools

TRACKS = ["fewandfarbetween", "thesuffocatingcarrier", "thesurrogate",
          "exitlight", "ghostmarch", "nocturnalsugars", "allartmustdie",
          "daylightbrings", "hillsoflife", "asseenfromafar",
          "thegreatadventure", "sequels", "secondsofdream"]
DIGITS = "58112171456182114"
CELLS = "ehk-bqNEFRUn-"
LETTERS = [(i, c) for i, c in enumerate(CELLS) if c != "-"]
VALS = [(i, ord(c.upper()) - 64) for i, c in LETTERS]

VOWELS = set("aeiou")
def readable(s):
    return sum(c in VOWELS for c in s) >= len(s) * 0.15 and all(ch.isalpha() for ch in s)


def try_report(tag, s):
    if readable(s):
        print("%-42s %s" % (tag, s))


print("== scheme 1: digit i -> track i (cycle 13), letter = digit-th (1-based) ==")
for mode in ("1based", "0based"):
    out = []
    for i, d in enumerate(DIGITS):
        t = TRACKS[i % 13]
        idx = int(d) - 1 if mode == "1based" else int(d)
        out.append(t[idx] if 0 <= idx < len(t) else "?")
    try_report("cycle track, %s" % mode, "".join(out))

print("== scheme 2: digit i -> track i (no cycle: 1..17 -> 1..13 then ?) ==")
for mode in ("1based", "0based"):
    out = []
    for i, d in enumerate(DIGITS):
        if i >= 13:
            break
        t = TRACKS[i]
        idx = int(d) - 1 if mode == "1based" else int(d)
        out.append(t[idx] if 0 <= idx < len(t) else "?")
    try_report("track i<=13, %s" % mode, "".join(out))

print("== scheme 3: each cell's value indexes its own track (11 letters) ==")
for mode in ("1based", "0based", "end1", "end0"):
    out = []
    for cell_i, v in VALS:
        t = TRACKS[cell_i]
        if mode == "1based":
            idx = v - 1
        elif mode == "0based":
            idx = v
        elif mode == "end1":
            idx = len(t) - v
        else:
            idx = len(t) - v - 1
        out.append(t[idx] if 0 <= idx < len(t) else "?")
    try_report("own track %s" % mode, "".join(out))

print("== scheme 4: each cell's value indexes every track (11 letters) ==")
for mode in ("1based", "0based", "end1", "end0"):
    for shift in range(13):
        out = []
        for cell_i, v in VALS:
            t = TRACKS[(cell_i + shift) % 13]
            if mode == "1based":
                idx = v - 1
            elif mode == "0based":
                idx = v
            elif mode == "end1":
                idx = len(t) - v
            else:
                idx = len(t) - v - 1
            out.append(t[idx] if 0 <= idx < len(t) else "?")
        try_report("shift %+d %s" % (shift, mode), "".join(out))

print("== scheme 5: digits split into 13 two-part values (track,letter) ==")
# 17 = 13 + 4 two-digit values; each value v: track = v//10? or first digit track?
found = 0
for combo in itertools.combinations(range(1, 17), 4):
    vals, pos = [], 0
    ok = True
    for k in range(13):
        two = pos in combo
        chunk = DIGITS[pos:pos + (2 if two else 1)]
        pos += 2 if two else 1
        vals.append(int(chunk))
    if pos != 17:
        continue
    for mode in ("1based", "0based"):
        out = []
        for k, v in enumerate(vals):
            t = TRACKS[k]
            idx = v - 1 if mode == "1based" else v
            out.append(t[idx] if 0 <= idx < len(t) else "?")
        s = "".join(out)
        if "?" not in s and readable(s):
            print("split", vals, mode, s)
            found += 1
print("readable splits:", found)

print("== scheme 6: 11 cell values as (track,letter) pairs, tracks by cell pos ==")
for mode in ("1based", "0based"):
    out = []
    for cell_i, v in VALS:
        # try v as letter index within the track of the NEXT/PREV letter cell
        t = TRACKS[cell_i]
        for cand_idx in (v - 1, v, len(t) - v, len(t) - v - 1):
            if 0 <= cand_idx < len(t):
                out.append(t[cand_idx])
                break
        else:
            out.append("?")
    try_report("cell own %s" % mode, "".join(out))

print()
print("== scheme 7: raw 'note' check, print the full output ==")
out = "".join(TRACKS[i % 13][int(d) - 1] for i, d in enumerate(DIGITS))
print("digit-th letter of track i:", out)
out2 = "".join(TRACKS[i % 13][int(d) % len(TRACKS[i % 13])] for i, d in enumerate(DIGITS))
print("wrapped index            :", out2)
