#!/usr/bin/env python3
"""Clue 2, round 7: the two "geometric" routes the external review proposed.

(A) ANAGRAM PERMUTATION. The eight displayed strings are anagrams of eight
    instruction words, and their lengths partition the 41-cell ciphertext in
    display order (lengths 2,5,8,7,4,8,3,4 = 41). So each word is aligned with
    its own segment, cell for cell.  Route: take the permutation that
    unscrambles the displayed anagram into its canonical word and apply *that
    same permutation to the ciphertext segment*, then read the capitals.

    Repeated letters make the permutation non-unique; all distinct choices are
    enumerated (16 combinations in total for this string).

(B) ORDERING KEY. Same per-cell values (word letter, cipher letter, 1-based
    position; +/-), but the value is used to *sort* the 15 capitals instead of
    immediately becoming a letter.  (The repo's clue2_three_layer.py already
    covers a first version of this; here it is re-run over the aligned chunks
    and both orders.)
"""
import itertools
import sys

sys.path.insert(0, "tools")
from oracle import segment_oracle  # noqa: E402

S = "s-bcBPEFfJDfeFmksmPOkChDhrgBqjD-i---ffeNB"
assert len(S) == 41

# (displayed anagram, canonical word) in DISPLAY order
DISPLAY = [("ot", "TO"), ("rleow", "LOWER"), ("utbrctsa", "SUBTRACT"),
           ("aacpilt", "CAPITAL"), ("hwti", "WITH"), ("dioiatdn", "ADDITION"),
           ("het", "THE"), ("ryuo", "YOUR")]
# sentence order: WITH YOUR CAPITAL ADDITION TO THE LOWER SUBTRACT
SENTENCE_ORDER = ["WITH", "YOUR", "CAPITAL", "ADDITION", "TO", "THE", "LOWER", "SUBTRACT"]

CANON_BY_DISP = {d: c for d, c in DISPLAY}
SKIES = {"witness": "71520219618128920", "repo": "58112171456182114"}

segs, pos = [], 0
for d, c in DISPLAY:
    segs.append(S[pos:pos + len(d)])
    pos += len(d)
assert pos == 41


def perms_to_canon(disp, canon):
    """All position maps p with [disp[p[i]] for i] == list(canon), lower vs upper."""
    d = disp.lower()
    c = canon.lower()
    # for each canonical position i, the candidate positions j in disp with d[j]==c[i]
    cands = [[j for j, ch in enumerate(d) if ch == c[i]] for i in range(len(c))]
    out = []
    for choice in itertools.product(*cands):
        if len(set(choice)) == len(choice):
            out.append(choice)
    return out or [tuple(range(len(d)))]


PERMS = {d: perms_to_canon(d, c) for d, c in DISPLAY}
n = 1
for d in PERMS:
    n *= len(PERMS[d])
print("permutation combinations:", n)
for d in PERMS:
    if len(PERMS[d]) > 1:
        print("  %-9s %d ways" % (d, len(PERMS[d])))

cands = {}


def emit(s, tag):
    if len(s) == 15 and s.isalpha():
        cands.setdefault(s.lower(), tag)


# ---------------- (A) apply permutation to the segment ----------------
keys = list(PERMS.keys())
for combo in itertools.product(*[PERMS[d] for d in keys]):
    newsegs = {}
    for d, p in zip(keys, combo):
        newsegs[d] = "".join(segs[keys.index(d)][p[i]] for i in range(len(p)))
    # rebuild in display order and in sentence order
    disp_str = "".join(newsegs[d] for d, _ in DISPLAY)
    sent_str = "".join(newsegs[[d for d, c in DISPLAY if c == w][0]] for w in SENTENCE_ORDER)
    for X, tag in ((disp_str, "perm-disp"), (sent_str, "perm-sent")):
        caps = "".join(ch for ch in X if ch.isupper()).lower()
        if len(caps) == 15:
            emit(caps, tag + "|caps")
        letters = "".join(ch for ch in X if ch.isalpha()).lower()
        for start in range(0, 41 - 15 + 1):
            w = letters[start:start + 15]
            if w.isalpha():
                emit(w, tag + "|win%d" % start)
        # also: characters at the ORIGINAL capital positions
        orig_cap_pos = [i for i, ch in enumerate(S) if ch.isupper()]
        at = "".join(X[i] for i in orig_cap_pos).lower()
        if at.isalpha():
            emit(at, tag + "|atcap")
print("after permutation families:", len(cands))

# ---------------- (B) ordering key over aligned chunks ----------------
CV = lambda c: ord(c.upper()) - 64
LV = lambda c: ord(c) - 96


for ordname, order_words in (("display", [c for _, c in DISPLAY]), ("sentence", SENTENCE_ORDER)):
    chunks = []
    for w in order_words:
        i = [k for k, (dd, c) in enumerate(DISPLAY) if c == w][0]
        chunks.append((w, [dd for dd, c in DISPLAY if c == w][0], segs[i]))
    for tokA, tokB in itertools.product("wcp", repeat=2):
        for op in "+-":
            cells = []  # (key, capital-char)
            for w, d, seg in chunks:
                for k, ch in enumerate(seg, start=1):
                    if not ch.isalpha():
                        continue
                    wl = ord(w[k - 1].upper()) - 64
                    c = CV(ch)
                    a = {"w": wl, "c": c, "p": k}[tokA]
                    b = {"w": wl, "c": c, "p": k}[tokB]
                    key = a + b if op == "+" else a - b
                    if ch.isupper():
                        cells.append((key, ch))
            if len(cells) != 15:
                continue
            for rev in (False, True):
                for flip in (False, True):
                    order = sorted(range(15), key=lambda i: (-cells[i][0] if flip else cells[i][0]), reverse=rev)
                    w = "".join(cells[i][1] for i in order).lower()
                    emit(w, "ordkey|%s %s%s|%s|rev%d|flip%d" % (ordname, tokA, tokB, op, rev, flip))
print("after ordering-key families:", len(cands))

# ---------------- test ----------------
tested = hits = 0
for sc, tag in cands.items():
    for sky, kn in SKIES.items():
        tested += 1
        r = segment_oracle(4, (sc + sky).encode())
        if r:
            hits += 1
            print("MATCH!!! scramble=%s (%s) sky=%s (%s) -> %s" % (sc, tag, sky, kn, r.hex()))
print("tested %d pairs, hits %d" % (tested, hits))
