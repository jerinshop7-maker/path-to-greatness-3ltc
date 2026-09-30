#!/usr/bin/env python3
"""Generate 16-char clue-6 (beach) readings from the measured melody.

Melody (measured by FFT, ledger): A#5 F#5 B5 A#5 F#5 D#5 F5 C#5 B4 C#5 A#4 A#5 F#5 B5 A#5
Key D# minor; degrees 1=D# 2=F 3=F# 4=G# 5=A# 6=B 7=C#  -> 5 3 6 5 3 1 2 7 6 7 5 5 3 6 5
Real album tracks (iTunes): 1 fewandfarbetween 2 thesuffocatingcarrier
3 thesurrogate 4 exitlight 5 ghostmarch 6 nocturnalsugars 7 allartmustdie
8 daylightbrings 9 hillsoflife 10 asseenfromafar 11 thegreatadventure
12 sequels 13 secondsofdream
"""
TRACKS = ["fewandfarbetween", "thesuffocatingcarrier", "thesurrogate",
          "exitlight", "ghostmarch", "nocturnalsugars", "allartmustdie",
          "daylightbrings", "hillsoflife", "asseenfromafar",
          "thegreatadventure", "sequels", "secondsofdream"]
DEG = [5, 3, 6, 5, 3, 1, 2, 7, 6, 7, 5, 5, 3, 6, 5]   # 15 notes
NOTES = ["A#5", "F#5", "B5", "A#5", "F#5", "D#5", "F5", "C#5", "B4", "C#5",
         "A#4", "A#5", "F#5", "B5", "A#5"]

cands = {}

# A. degrees -> track number, take the d-th letter of that track title
cands["deg2track_1based"] = "".join(
    TRACKS[d - 1][d - 1] if d - 1 < len(TRACKS) and d - 1 < len(TRACKS[d - 1]) else "?"
    for d in DEG)
cands["deg2track_0based"] = "".join(
    TRACKS[d][d] if d < len(TRACKS) and d < len(TRACKS[d]) else "?"
    for d in DEG)

# B. degrees -> track number, take the note index-th letter of the track
cands["noteidx_in_track"] = "".join(
    TRACKS[d - 1][i] if i < len(TRACKS[d - 1]) else "?"
    for i, d in enumerate(DEG))
cands["noteidx_in_track_end"] = "".join(
    TRACKS[d - 1][-(i + 1)] if -(i + 1) >= -len(TRACKS[d - 1]) else "?"
    for i, d in enumerate(DEG))

# C. cumulative degree positions into the joined album string
album = "".join(TRACKS)
cum, tot = [], 0
for d in DEG:
    tot += d
    cum.append(tot)
cands["album_cumsum_1based"] = "".join(
    album[p - 1] if 0 <= p - 1 < len(album) else "?" for p in cum)
# with 16th char: append the last again
cands["album_cumsum16"] = cands["album_cumsum_1based"] + cands["album_cumsum_1based"][-1]

# D. degrees -> first letters of tracks 1..7 in order (a 7-letter alphabet)
init7 = "".join(TRACKS[d - 1][0] for d in range(1, 8))
print("first-letter table:", init7)
cands["deg_letters"] = "".join(init7[d - 1] for d in DEG)
cands["deg_letters_16"] = cands["deg_letters"] + "t"

# E. conventional digit readings (for completeness / cross-check)
base = "".join(str(d) for d in DEG)
cands["digits15"] = base
cands["digits16_prepend5"] = "5" + base[0:15]
cands["digits16_append5"] = base + "5"
cands["digits16_6th_is_1sharp"] = base[:5] + "1#" + base[6:]
cands["digits16_6th_is_e"] = base[:5] + "2" + base[6:] + "?"
cands["digits16_sharp_first"] = base[:5] + "#1" + base[6:]
# semitone spelling of the 6th note relative to D# minor (D# = 1, chromatic)
chrom = {0: "1", 1: "1#", 2: "2", 3: "3", 4: "3#", 5: "4", 6: "4#", 7: "5",
         8: "5#", 9: "6", 10: "6#", 11: "7"}
semis = [3, 6, 11, 3, 6, 10, 8, 1, 6, 1, 3, 3, 6, 11, 3]  # from D#
cands["chromatic_06"] = "".join(chrom.get(s, "?") for s in semis)
cands["chromatic_16"] = "".join(chrom.get(s, "?") for s in semis) + "?"
# note names, accidentals only
cands["letters_only"] = "".join(n[0] for n in NOTES) + "?"
cands["solfege_initials"] = "".join(
    {1: "d", 2: "r", 3: "m", 4: "f", 5: "s", 6: "l", 7: "t"}[d] for d in DEG) + "?"

for k, v in list(cands.items()):
    if len(v) != 16 or "?" in v:
        print("DROP %-22s %r (%d)" % (k, v, len(v)))
        del cands[k]

print("\nvalid 16-char beach candidates: %d" % len(cands))
for k, v in sorted(cands.items()):
    print("%-24s %s" % (k, v))
