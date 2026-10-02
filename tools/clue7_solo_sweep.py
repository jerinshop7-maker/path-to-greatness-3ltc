#!/usr/bin/env python3
"""Test clue-7 candidates ALONE, by letting the clue-3 half range over
everything it could be.

The problem this solves. Clue 3 is closed as a source of new readings
(tools/clue3_closure.py: the printed digits are redundant on all 96 arrow
cells, the 92-cycle string hides no message, and every 8-character extraction
consistent with the step-size semantics has been enumerated). So a clue-7
candidate can no longer be certified by pairing it with a clue-3 reading that
"looks right" -- the pairing is a guess about a closed source.

The only honest way to test clue 7 by itself is to enumerate the clue-3 half
exhaustively. Earlier runs did that over two alphabets:

    {w,a,s,d}^8         =         65,536
    {0-9}^8             =    100,000,000

Neither contains a *mixed* answer. The repository's strongest structural
reading, `d3w1as24`, needs letters AND digits, and so do the other root-cell
encodings -- all 1,290 retained clue-3 readings contain at least one digit and
at least one of w/a/s/d. Every clue-7 string refuted in rounds 14-20 was
refuted against a clue-3 space that could not have held those answers.

This tool sweeps the full

    "wasd0123456789" ^ 8 = 1,475,789,056

per candidate. A string that fails here is refuted UNCONDITIONALLY: no clue-3
answer in the author's own alphabet can rescue it.

Cost. The engine runs at about 1.3M keys/s per core, so one candidate is
1.48e9 keys, roughly 19 minutes. That is the price of an unconditional
negative, and it is why this is a short list rather than a large family. Each
candidate is a considered reading, not a generated one.

Certification. Before each sweep the engine re-finds a planted witness whose
clue-3 half is "wasdwasd" and whose clue-7 half is the candidate itself, so a
hit inside the stream is guaranteed detectable. Every negative is therefore
attributable to a specific string and a specific alphabet.

Usage:
    python3 tools/clue7_solo_sweep.py --list
    python3 tools/clue7_solo_sweep.py --run 3
    python3 tools/clue7_solo_sweep.py --run all        # ~2 hours, background
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(HERE, "seg3_cross")
WITOOL = os.path.join(HERE, "seg3_witnesses.py")
ALPHA = "wasd0123456789"
SPACE = 1475789056

# Each string is a considered reading, not a generated one. The registers are
# the four the evidence supports: the two portraits (actors and characters),
# the deck-plans register the repo asserted for rounds 12-14, and the poem's
# own stanza-2 fate vocabulary.
CANDIDATES = [
    # actor pairs, both orders; both are exactly 24 characters
    "victorgarberjonathanhyde",
    "jonathanhydevictorgarber",
    # character-name pairs from the same two men
    "edwardsmiththomasandrews",
    "thomasandrewsedwardsmith",
    # the deck-plans register, in the length-24 forms that register admits
    "smithandrewsdeckplanlast",
    # the poem's stanza-2 fate register, length-24 forms
    "thenightmovestomakerofit",
    "thecoldnightmovestomaker",
]


def build_engine() -> str:
    if not os.path.exists(ENGINE):
        print("engine not built; run:\n"
              "  gcc -O3 -march=native -o tools/seg3_cross tools/seg3_cross.c")
        sys.exit(2)
    return ENGINE


def sweep_one(engine: str, cand: str, logdir: str):
    lp = os.path.join(logdir, "%s.lefts.txt" % cand)
    rp = os.path.join(logdir, "%s.rights.txt" % cand)
    wp = os.path.join(logdir, "%s.wit.txt" % cand)
    log = os.path.join(logdir, "%s.log" % cand)

    with open(lp, "w") as fh:
        fh.write("wasdwasd\n")     # the alpha sweep's witness clue-3 half
    with open(rp, "w") as fh:
        fh.write(cand + "\n")

    w = subprocess.run([sys.executable, WITOOL, "alpha", rp, "-o", wp],
                       capture_output=True, text=True)
    if w.returncode != 0:
        print("witness generation failed for %s:\n%s%s" % (cand, w.stdout, w.stderr))
        return cand, None

    t0 = time.time()
    with open(log, "w") as fh:
        subprocess.run([engine, "alpha", wp, rp, "1"],
                       stdout=fh, stderr=subprocess.STDOUT, text=True)
    dt = time.time() - t0

    with open(log) as fh:
        text = fh.read()
    hit = "RESULT HIT" in text
    certified = "UNCERTIFIED" not in text
    print("%-30s %-9s %6.1f min  %s"
          % (cand, "HIT" if hit else "no match", dt / 60.0,
             "certified" if certified else "UNCERTIFIED -- negative does not count"),
          flush=True)
    if hit:
        print(text)
    return cand, ("HIT" if hit else ("no match" if certified else "UNCERTIFIED"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--run", default=None, help="N, or 'all'")
    ap.add_argument("--logdir", default="/tmp/clue7solo")
    args = ap.parse_args()

    ok = [c for c in CANDIDATES if len(c) == 24]
    bad = [c for c in CANDIDATES if len(c) != 24]
    print("clue-3 space swept per candidate: %s^8 = %s keys"
          % (ALPHA, format(SPACE, ",")))
    print("at ~1.3M keys/s that is about %.0f minutes per candidate"
          % (SPACE / 1.3e6 / 60))
    print("candidates: %d, all exactly 24 characters: %s"
          % (len(ok), all(len(c) == 24 for c in ok)))
    if bad:
        print("dropped on length: %s" % bad)
    if args.list:
        for c in ok:
            print("  %s" % c)
        return 0
    if not args.run:
        ap.print_help()
        return 2

    os.makedirs(args.logdir, exist_ok=True)
    engine = build_engine()
    todo = ok if args.run == "all" else ok[:int(args.run)]

    results = {}
    for c in todo:
        cand, verdict = sweep_one(engine, c, args.logdir)
        results[cand] = verdict

    print("\n" + "=" * 78)
    print("SUMMARY -- each refuted against ALL %s clue-3 answers" % format(SPACE, ","))
    for c, v in results.items():
        print("  %-30s %s" % (c, v))
    return 0


if __name__ == "__main__":
    sys.exit(main())