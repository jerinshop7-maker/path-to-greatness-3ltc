#!/usr/bin/env python3
"""Clue 7 — a bounded description family, generated to a file and swept in
chunks so neither the generator nor the sweeper can exhaust memory.

Round 14's "just generate a list" recommendation is what killed three shells
this session. This tool does it in the order that actually works:

  1. size the family with a hard cap BEFORE sweeping (clue7_family_size.py's
     lesson), writing to disk rather than to a Python set,
  2. sweep in chunks of 20,000 pairs so peak memory is flat,
  3. print the number dropped on length, which segsweep silently discards.

Vocabulary is drawn from what is now measured in the recovered file: the two
figures, the ship's line drawing, and the eight lines of the poem that sits in
the top right of the same PNG.
"""
import itertools
import sys

sys.path.insert(0, ".")
from clue7_ship_family import clue3_readings
from segsweep import sweep

# Nouns / names that the recovered montage and poem actually support.
NAMES = ["ismay", "andrews", "smith", "titanic", "hyde", "garber", "victor",
         "jonathan", "bernard", "hill", "oceanic", "iceberg", "ice", "berg"]
# What the middle drawing is, and the film's own register.
THINGS = ["ship", "liner", "boat", "plan", "plans", "deck", "decks", "hull",
          "bow", "stern", "mast", "rigging", "funnel", "rail", "rails",
          "porthole", "portholes", "drawing", "diagram", "cutaway",
          "section", "profile", "sketch", "blueprint", "lines"]
# Verbs / relations a description would use.
ACTS = ["shows", "show", "holds", "hold", "draws", "draw", "has", "have",
        "with", "and", "the", "a", "of", "on", "in", "at", "sees", "see",
        "watches", "watch", "looks", "look", "study", "studies", "is", "are",
        "was", "were", "goes", "go", "sinks", "sink", "founder", "founders"]
# Stanza 2's own words.
NIGHT = ["night", "cold", "dark", "vast", "frigid", "maker", "great",
         "undertaker", "ocean", "tide", "moves", "towards"]

VOCAB = sorted(set(NAMES + THINGS + NIGHT))
GLUE = ["", "and", "the", "a", "of", "in", "on", "at", "to", "with", "is"]

TARGET = 24
CAP = 400_000


def build(words=(2, 3, 4, 5)):
    """Depth-first over (glue, word) pairs with strict length pruning.
    Never holds more than CAP strings; the caller is told if the cap bound."""
    out = []
    capped = [False]

    def rec(s, depth, first):
        if len(out) >= CAP:
            capped[0] = True
            return
        if len(s) == TARGET:
            out.append(s)
            return
        if depth == 0:
            return
        if len(s) > TARGET:
            return
        room = TARGET - len(s)
        for w in VOCAB:
            if len(w) > room:
                continue
            rec(s + w, depth - 1, False)
            if capped[0]:
                return
        if not first:
            for g in GLUE:
                if not g:
                    continue
                for w in VOCAB:
                    if len(g) + len(w) > room:
                        continue
                    rec(s + g + w, depth - 1, False)
                    if capped[0]:
                        return

    rec("", max(words), True)
    return sorted(set(out)), capped[0]


def main():
    maxw = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    fam, capped = build(words=(1, 2, 3, 4, maxw))
    print("vocabulary: %d tokens; glue: %r" % (len(VOCAB), GLUE))
    print("family size: %d strings%s"
          % (len(fam), "   (CAP HIT -- family is truncated)" if capped else ""))
    print("all exactly %d chars: %s" % (TARGET, all(len(s) == TARGET for s in fam)))
    if not fam:
        print("empty family; widen the vocabulary or raise the depth")
        return 1

    c3 = clue3_readings()
    print("clue-3 readings: %d -> %s" % (len(c3), c3))
    print()

    CH = 20000
    hits, done = [], 0
    for i in range(0, len(fam), CH):
        chunk = fam[i:i + CH]
        res = sweep(3, c3, chunk, "ship[%d:%d]" % (i, i + len(chunk)))
        done += len(chunk) * len(c3)
        if res:
            hits += res
    print()
    print("PAIRS SWEPT: %d   HITS: %s" % (done, hits if hits else "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())