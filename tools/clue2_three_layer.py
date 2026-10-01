"""Clue 2: the three-layer rule (anagram word + case mask + ciphertext char).

The clue's own words, in sentence order, are the instruction
"WITH YOUR CAPITAL, ADDITION. TO THE LOWER, SUBTRACT."
So uppercase cells are ADDED and lowercase cells are SUBTRACTED. The question is
*added to / subtracted from what*. This tool sweeps that choice systematically:

  operand A in {word letter, ciphertext letter, 1-based position}
  operand B in {word letter, ciphertext letter, 1-based position}
  op        in {+, -}
  word form in {canonical (unscrambled), as displayed}
  ordering  in {display, sentence}
  emit      in {capital cells only, every letter cell}

and additionally the user's proposed "operation result is an ordering key"
variant, where the per-cell numbers sort the capitals instead of forming letters.

Every candidate produced is exactly 15 characters and is tested against both
pinned clue-8 skies through the segment-4 oracle.
"""
import itertools
import subprocess
import sys

S = "s-bcBPEFfJDfeFmksmPOkChDhrgBqjD-i---ffeNB"

# (word, length) in DISPLAY order, and the scrambled spelling as printed
DISPLAY = [
    ("TO", "ot"), ("LOWER", "rleow"), ("SUBTRACT", "utbrctsa"), ("CAPITAL", "aacpilt"),
    ("WITH", "hwti"), ("ADDITION", "dioiatdn"), ("THE", "het"), ("YOUR", "ryuo"),
]
SENTENCE = [
    ("WITH", "hwti"), ("YOUR", "ryuo"), ("CAPITAL", "aacpilt"), ("ADDITION", "dioiatdn"),
    ("TO", "ot"), ("THE", "het"), ("LOWER", "rleow"), ("SUBTRACT", "utbrctsa"),
]

SKIES = ["58112171456182114", "71520219618128920"]

SKIP, CAP, LOW, DASH = 0, 1, 2, 3


def kind(ch):
    if ch.isupper():
        return CAP
    if ch.islower():
        return LOW
    return DASH


def partition(order):
    """[(word, scrambled, segment)] cutting S by word length in the given order."""
    out, i = [], 0
    for canon, scrambled in order:
        n = len(canon)
        out.append((canon, scrambled, S[i:i + n]))
        i += n
    assert i == len(S)
    return out


def val(tok, kindtag, wletter, cletter, pos):
    if tok == "w":
        return wletter
    if tok == "c":
        return cletter
    return pos


def build(order, wordform, tokA, tokB, op, emit):
    """Return (letters, keys). letters = 15 chars when emit == 'cap'."""
    segs = partition(order)
    letters, keys = [], []
    for canon, scrambled, seg in segs:
        word = canon if wordform == "canon" else scrambled
        for k, ch in enumerate(seg, start=1):
            kd = kind(ch)
            if kd == DASH:
                continue
            w = ord(word[k - 1].upper()) - 64
            c = ord(ch.upper()) - 64
            a = val(tokA, kd, w, c, k)
            b = val(tokB, kd, w, c, k)
            r = (a + b) if op == "+" else (a - b)
            if emit == "cap" and kd != CAP:
                continue
            letters.append(((r - 1) % 26) + 1)
            keys.append(r)
    return letters, keys


def order_by_keys(keys, letters, mode):
    idx = sorted(range(len(keys)), key=lambda i: keys[i])
    if mode == "asc":
        pick = idx
    elif mode == "desc":
        pick = idx[::-1]
    else:
        return None
    return [letters[i] for i in pick]


def to_text(nums):
    return "".join(chr((n - 1) % 26 + 97) for n in nums)


def main():
    cands = {}

    def add(s):
        if s and len(s) == 15 and s.isalpha():
            cands[s] = cands.get(s, 0) + 1

    for order, ordername in ((DISPLAY, "display"), (SENTENCE, "sentence")):
        for wordform in ("canon", "as-is"):
            for tokA, tokB in itertools.product("wcp", repeat=2):
                for op in "+-":
                    for emit in ("cap", "all"):
                        letters, keys = build(order, wordform, tokA, tokB, op, emit)
                        if len(letters) == 15:
                            add(to_text(letters))
                        if emit == "cap":
                            for mode in ("asc", "desc"):
                                seq = order_by_keys(keys, letters, mode)
                                if seq and len(seq) == 15:
                                    add(to_text(seq))

    cand_list = sorted(cands)
    print("candidates generated: %d" % len(cand_list))
    if not cand_list:
        return 1

    for sky in SKIES:
        payload = "".join("%s %s\n" % (c, sky) for c in cand_list)
        r = subprocess.run(
            [sys.executable, "tools/oracle.py", "--stdin-segment", "4"],
            input=payload, capture_output=True, text=True)
        out = (r.stdout + r.stderr).strip()
        print("sky %s -> %s" % (sky, out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
