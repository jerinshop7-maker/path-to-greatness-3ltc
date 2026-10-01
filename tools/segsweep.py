#!/usr/bin/env python3
"""segsweep -- the small CPU cross-product driver the round-13/14 tools import.

Status: RESTORED.  `tools/clue3_ship_cross.py`, `tools/clue7_ship_family.py` and
`tools/clue7_desc_sweep.py` all do `from segsweep import sweep`, but the module
itself was a round-14 working file that never got committed, so those three
tools could not be re-run from a clean checkout.  This is a re-implementation
against `tools/oracle.py`, with the two properties round 14's write-up says the
sweeper must have:

  1. normalise both halves exactly as the author's `fix_clues.script` does
     (spaces removed, lowercased except clue 4), then drop wrong-length
     candidates -- and REPORT how many were dropped.  A silent drop is what
     made round 14 read a 19-string list as a clean negative while testing 6.
  2. re-certify the AES path once per call with a planted witness, so a run
     that reports "0 hits" is a run that could have found a planted one.

It is deliberately small: these are families of tens to a few hundred thousand
pairs, where the CPU path is already seconds.  The GPU engine (`tools/sweep.c`)
is for the 10^9+ spaces.
"""

from __future__ import annotations

import oracle


def _witness_ok(seg_id: int) -> bool:
    """Encrypt a known 8-byte block under a known key with this segment's IV,
    swap it in, and check the oracle re-finds it.  Restores the real ciphertext
    whatever happens, so a failed witness cannot corrupt a later run."""
    key = bytes(range(32))
    eight = b"WITNESS!"
    ct = oracle.AES.new(key, oracle.AES.MODE_CBC,
                        oracle.SEGMENTS[seg_id][2]).encrypt(eight + b"\x08" * 8)
    saved = oracle._SEG_CT[seg_id]
    try:
        oracle._SEG_CT[seg_id] = ct
        return oracle.segment_oracle(seg_id, key) == eight
    finally:
        oracle._SEG_CT[seg_id] = saved


def sweep(seg_id: int, lefts, rights, label: str = ""):
    """Cross every (left, right) pair for segment `seg_id` and return the hits.

    `lefts` feeds the lower-numbered clue of the segment, `rights` the higher
    one (oracle.SEGMENTS).  Prints one scope line per call: pair count, the
    number of candidates dropped on length, the witness verdict, and the hit
    count.  A hit is the 16 hex digits of the recovered 8 super_key bytes -- it
    is a filter, not a solution; `oracle.py --answers` still has to be run to
    reach L3.
    """
    clue_a, clue_b = oracle.SEGMENTS[seg_id][3]
    len_a, len_b = oracle.ANSWER_LEN[clue_a], oracle.ANSWER_LEN[clue_b]

    L, drop_l = [], 0
    for raw in lefts:
        s = oracle.normalise_answer(clue_a, raw)
        if len(s) == len_a:
            L.append(s)
        else:
            drop_l += 1
    R, drop_r = [], 0
    for raw in rights:
        s = oracle.normalise_answer(clue_b, raw)
        if len(s) == len_b:
            R.append(s)
        else:
            drop_r += 1
    L, R = sorted(set(L)), sorted(set(R))

    witness = _witness_ok(seg_id)
    hits, tested = [], 0
    for a in L:
        for b in R:
            tested += 1
            eight = oracle.segment_oracle(seg_id, (a + b).encode())
            if eight:
                hits.append((a, b, eight.hex()))

    print("[%-22s] seg %d  clue %d (%d) x clue %d (%d) = %d pairs"
          % (label or "-", seg_id, clue_a, len_a, clue_b, len_b, tested))
    print("     dropped on length: %d left, %d right | distinct: %d x %d"
          " | witness: %s | hits: %d"
          % (drop_l, drop_r, len(L), len(R),
             "re-found" if witness else "*** FAILED ***", len(hits)))
    if not witness:
        raise RuntimeError("witness not re-found: conclude nothing from this run")
    for a, b, h in hits:
        print("     MATCH %s + %s -> %s" % (a, b, h))
    return hits
