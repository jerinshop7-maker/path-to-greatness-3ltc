#!/usr/bin/env python3
"""Surgical candidate tests for Path to Greatness, per segment.

Uses tools/oracle.py's certified L1 segment oracle directly. Every hypothesis
family below is a *free* test (microseconds per pair); the point is precision,
not volume. Any candidate of the wrong length is skipped by the oracle.
"""
import itertools
import sys

sys.path.insert(0, "tools")
from oracle import segment_oracle, SEGMENTS, ANSWER_LEN  # noqa: E402

hits = []


def test(seg, left, right, tag=""):
    la, lb = SEGMENTS[seg][3]
    ka = (left if la == 4 else left.lower())
    kb = (right if lb == 4 else right.lower())
    if len(ka) != ANSWER_LEN[la] or len(kb) != ANSWER_LEN[lb]:
        return False
    if segment_oracle(seg, (ka + kb).encode()) is not None:
        msg = "MATCH seg=%d %s | %s | %s" % (seg, tag, ka, kb)
        print(msg)
        hits.append(msg)
        return True
    return False


def batch(seg, lefts, rights, tag):
    n = 0
    for l in lefts:
        for r in rights:
            n += 1
            test(seg, l, r, tag)
    print("  [%s] %d pairs tested" % (tag, n))
    return n


# --------------------------------------------------------------- segment 1
# imagine = 8 digits (date/decoration), beach = melody variants.
def date8():
    out = set()
    for y in range(1900, 2051):
        for m in range(1, 13):
            for d in range(1, 32):
                out.add("%04d%02d%02d" % (y, m, d))
                out.add("%02d%02d%04d" % (m, d, y))
    return sorted(out)


def dates_in_words():
    """Two dates of the form MONTH DD YYYY etc., no spaces, concatenated twice."""
    months = ["january", "february", "march", "april", "may", "june", "july",
              "august", "september", "october", "november", "december"]
    out = []
    for m in months:
        for d in range(1, 32):
            for y in (1941, 1898, 1912, 2020, 2021):
                out.append("%s%02d%04d" % (m, d, y))
                out.append("%s%d%04d" % (m, d, y))
    return out


D8 = date8()
print("dates 8-digit:", len(D8))

# beach melody variants: base reading and common re-encodings
BASE = "536531276755365"          # 15 chars, degree of each note in D# minor
BASE_E = "536531#276755365"       # 16 chars, 6th note bent to E


def melody_variants():
    out = {BASE_E}
    # fill-with-0, fill-with-X, degrees >=8 as two chars
    for fill in "0x":
        out.add(BASE + fill)
        out.add(fill + BASE)
        out.add(BASE[:5] + fill + "1" + BASE[5:])
    # 6th note as E natural (degree 1 with #) already in BASE_E; also as plain 1
    out.add(BASE[:5] + "1" + BASE[5:])
    # everything as absolute semitone numbers from A (0) to G# (10)
    semis = "3 11 2 3 11 8 9 6 1 6 3 3 11 2 3".split()
    for j in ("", "-"):
        cand = ""
        for s in semis:
            v = int(s) + (0 if s == "" else 0)
            cand += str(v) if len(str(v)) == 2 else j + str(v)
        out.add(cand)
    return out


MELODY = sorted(melody_variants())
print("melody variants:", len(MELODY))

batch(1, D8, MELODY, "dates x melody")
batch(1, ["19410712"], MELODY, "anchor x melody")
batch(1, ["imagineall", "imagine", "johnlennon", "imagine1971",
          "imagine1941", "peace", "livinglifeinpeace", "livinglife",
          "apostleofpeace", "gimmeSomeTruth".lower()], MELODY, "words x melody")

# --------------------------------------------------------------- segment 1
# beach = digit holes: all 8-digit strings over {0-9} with every number
# 0-99 appearing at least once is impossible in 8 chars; instead test all
# 8-digit strings containing '00' or '99' (the hole) -- 10^8 is too big on
# CPU, so take the melody digits as the fixed part.
hole = set()
for base in [BASE_E, BASE, BASE[:5] + "1" + BASE[5:]]:
    digits = "".join(ch if ch != "#" else "" for ch in base)
    digits = digits.replace("11", "1").replace("21", "1").replace("31", "1") \
        .replace("41", "1").replace("51", "1").replace("61", "1").replace("71", "1")
    if len(digits) < 8:
        digits = digits + "0" * (8 - len(digits))
    for pos in range(7):
        for ins in ("00", "99", "0", "9"):
            cand = digits[:pos] + ins + digits[pos + 1:]
            if len(cand) == 8:
                hole.add(cand)
print("digit-hole candidates:", len(hole))
for l in sorted(hole):
    test(1, l, l, "digit-hole")

# --------------------------------------------------------------- segment 4
# sky = digits from album-track initials (certified rule 4->Exit Light->T)
# track list of Seconds of Dream (13 tracks, iTunes order):
TRACKS = ["fewandfarbetween", "nocturnalsugars", "somethingnew", "ghostmarch",
          "exitlight", "allartmustdie", "secondsofdream", "colorsandlight",
          "thepath", "remembrance", "wintersun", "apogee", "burningbridges"]
# NOTE: the exact tracklist needs verification; the certified facts are:
# 13 tracks, IVs few_n_far_btween (t1), nocturnal_sugars, seconds_of_dream,
# exit light (example), ghost march (example). Initials families are swept
# structurally instead of relying on the full list.
initials = set()
for combo in itertools.product("0123456789", repeat=2):
    initials.add(combo[0] + combo[1])
# 4 -> T means: n=4 picks letter T, position of T in "exitlight" is 2 (1-based).
# lowercase n = len - v gives T = exitlight[2-1]=x?? -- no. v = len - n:
# len=9, n=4 -> v=5 -> char 'exitlight'[4] = 'l'. Not T. So try other rules.
# certified: 4->ExitLight->T: E x i t L i g h t -> T is index 4 (0-based)!
# GhostMarch -> R is index 4 too (G h o s t M a r c h, 0-based index 4 = 'M'... no).
# 1-based index 4: ExitLight -> 't'; GhostMarch -> 't'. Hmm 'T' vs 't'.
# so rule: 1-based 4th letter? ExitLight[3]='t' -> T (capitalized in example).
print("rule probe: ExitLight 1-based4 = 't'; GhostMarch 1-based4='t'")
# so the example letter is the 1-based 4th letter, capitalised as printed.
# then 8 -> GhostMarch -> R must come from elsewhere: 0-based 4 = 'M'? no.
# possibilities: 8 -> 8th letter 1-based: GhostMarch[7]='r' -> R!
# 4 -> 4th letter 1-based: ExitLight[3] = 't' -> T. Consistent!!
print("rule probe: 4->ExitLight[3]='t' (T); 8->GhostMarch[7]='r' (R). CONSISTENT")
# digit rule: the two digits of each number pick (track#, letter index)?
# or (letter index, track#)? test both against 13x13 letter picking later.
for a in ("12345678", "00990099", "19410712", "20262026"):
    test(4, a, a, "digit-echo")

# --------------------------------------------------------------- segment 4
# scramble from the 41-char string: mechanical reads already refuted; try
# the 15 capitals in order (16 chars? count them) as the other half.
CAPS = "BPEFJDPCBDNF"  # placeholder; exact caps need the image -- skipped
print("(segment 2 untouched: needs the clue images)")

print()
if hits:
    print("HITS:", len(hits))
    for h in hits:
        print(h)
else:
    print("no hits in any family tested")
