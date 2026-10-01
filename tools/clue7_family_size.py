#!/usr/bin/env python3
"""Build the clue-7 description family and report its size only.

Deliberately capped: a recursive concatenation walk with a 50-word vocabulary
and nine connectives explodes. This measures the size at each depth so the
cost of a real sweep is known before it is launched.
"""
import itertools
import sys

VOCAB = [
    "ismay", "andrews", "john", "sir", "smith", "the", "two", "men",
    "deck", "naval", "titanic", "ship", "boat", "plans", "plan",
    "blueprint", "drawings", "diagram", "draft", "paper", "roll",
    "and", "with", "for", "left", "right", "middle", "centre", "center",
    "holds", "study", "looks", "over", "studies", "on", "of", "at", "in",
    "willfounder", "sinking", "founder", "sunk", "sink", "final", "scene",
    "montage", "lifeboats", "a", "an", "to",
]
CONNECT = ["", "and", "with", "on", "of", "the", "to", "in", "a"]
TARGET = 24
CAP = 400_000


def build(max_words):
    out = set()

    def emit(s):
        out.add(s)
        return len(out) < CAP

    def bare(s, left):
        if len(s) == TARGET:
            return emit(s)
        if left == 0 or len(s) > TARGET or len(out) >= CAP:
            return
        for w in VOCAB:
            if len(s) + len(w) <= TARGET:
                bare(s + w, left - 1)

    def joined(s, left):
        # s ends with a connective; append one word
        if len(s) == TARGET:
            return emit(s)
        if left == 0 or len(s) > TARGET or len(out) >= CAP:
            return
        for w in VOCAB:
            if len(s) + len(w) == TARGET:
                emit(s + w)
            elif len(s) + len(w) < TARGET:
                joined(s + w, left - 1)

    for w in VOCAB:
        if len(out) >= CAP:
            break
        bare(w, max_words - 1)
    for w in VOCAB:
        if len(out) >= CAP:
            break
        for m in CONNECT:
            if len(w) + len(m) < TARGET:
                joined(w + m, max_words - 1)
    return out


if __name__ == "__main__":
    for k in range(2, 6):
        s = build(k)
        print("words<=%d -> %d strings%s" % (k, len(s),
              "  (CAPPED)" if len(s) >= CAP else ""))
        sys.stdout.flush()