#!/usr/bin/env python3
"""Round 14: run the four proposed clue-3 routes (and the existing ones) as
*segment-3 key halves*, crossed with the proposed clue-7 candidates.

Segment 3's key is clue3 (8 chars) || clue7 (24 chars), so every candidate here
is a PAIR. Nothing about a clue-3 reading can be confirmed on its own; the best
this tool can do is enlarge the set of pairs that are REFUTED, which is why it
reports the scope of every family it runs.

Families:
  A  the eight-root readings (round 13's d3w1as24 and friends)
  B  route 1 -- sources interleaved with stars, both orders, all 70 slot choices
  C  route 2 -- source directions/values, 6 orderings x 2 pairings
  D  route 3 -- all 85 length-8 substrings of the 92-cycle
  E  route 4 -- all distinct permutations of the coordinate-index letters
  F  the eight-coordinate index read three ways
"""
import itertools
import sys

sys.path.insert(0, ".")
from segsweep import sweep
from wasd_grid import N, build, cell, rc

# ---------------------------------------------------------------- clue 3 ----
out, ind = build()


def the_cycle():
    seen = set()
    for i in range(N * N):
        if i in seen:
            continue
        j, path, local = i, [], set()
        while j is not None and j not in local:
            local.add(j)
            path.append(j)
            j = out[j]
        if j is not None:
            c = path[path.index(j):]
            if len(c) > 50:
                return c
        seen |= local
    raise RuntimeError


CYC = the_cycle()
CYCSTR = "".join(cell(i)[1].lower() for i in CYC)
ROOTS = [i for i in range(N * N) if i not in ind]           # row-major, 8 cells
STAR = [(i, cell(i)[0]) for i in ROOTS if cell(i)[1] == "*"]   # (idx, label)
SRC = [i for i in ROOTS if cell(i)[1] != "*"]
ENTRY = {i: CYC.index(out[i]) for i in SRC}


def root_token(i):
    n, d = cell(i)
    return str(n) if d == "*" else d.lower()


# ---------------------------------------------------------------- clue 7 ----
# Hand-picked, each verified to be exactly 24 characters.
SHIP = [
    # the two proposed in this round
    "ismayandrewsanddeckplans",
    "andrewsandismaydeckplans",
    # round 13's four, kept so the negatives stay attributable
    "andrewsandismayviewplans",
    "andrewsandismayontitanic",
    "andrewsdrawstheshipplans",
    "theoceanlinerwillfounder",
]

# A systematic description family.  Clue 7 is 24 characters of *plain
# description of the montage* (Ismay left, Andrews right, deck plans middle),
# so the honest family is: concatenations of a small vocabulary, with and
# without the connective "and", that come out at exactly 24 characters.
VOCAB = [
    "ismay", "andrews", "john", "sir", "smith", "the", "two", "men",
    "deck", "naval", "titanic", "ship", "boat", "plans", "plan", "blueprint",
    "drawings", "diagram", "draft", "paper", "roll", "on", "of", "at",
    "a", "an", "in", "and", "with", "for", "left", "right", "middle",
    "centre", "center", "holds", "hold", "holds2", "study", "looks",
    "look", "over", "studies", "the", "a", "willfounder", "sinking",
    "founder", "sunk", "sink", "lifeboats", "final", "scene", "montage",
]
CONNECT = ["", "and", "with", "on", "of", "the", "to", "in", "a"]


def gen_ship_family(max_words=5):
    """Every 24-character concatenation of 2..max_words vocabulary words,
    optionally joined by single connectives.

    Built by recursive extension with length pruning, not by a full product:
    a partial string longer than 24 is abandoned immediately, which keeps the
    walk linear in the number of *surviving* prefixes rather than |V|^k."""
    out = set()
    target = 24

    def walk(s, remaining):
        if len(s) == target:
            out.add(s)
            return
        if remaining == 0 or len(s) > target:
            return
        for w in VOCAB:
            walk(s + w, remaining - 1)
        for m in CONNECT:
            walk(s + m + VOCAB[0], remaining)   # connective + any word below

    # bare concatenation pass
    def walk_bare(s, remaining):
        if len(s) == target:
            out.add(s)
            return
        if remaining == 0 or len(s) > target:
            return
        for w in VOCAB:
            walk_bare(s + w, remaining - 1)

    # joined pass: first word, then (connective + word) repeatedly
    def walk_joined(s, remaining):
        if len(s) == target:
            out.add(s)
            return
        if remaining == 0:
            return
        for m in CONNECT:
            if len(s) + len(m) >= target:
                continue
            for w in VOCAB:
                if len(s) + len(m) + len(w) <= target:
                    walk_joined(s + m + w, remaining - 1)

    for w in VOCAB:
        walk_bare(w, max_words - 1)
    for w in VOCAB:
        for m in CONNECT:
            if len(w) + len(m) < target:
                walk_joined(w + m, max_words - 1)
    return sorted(out)


def fam_a():
    f = {}
    f["d3w1as24"] = "".join(root_token(i) for i in ROOTS)
    f["nums53214124"] = "".join(str(cell(i)[0]) for i in ROOTS)
    f["src_then_star"] = ("".join(cell(i)[1].lower() for i in SRC)
                          + "".join(str(n) for _, n in STAR))
    f["star_then_src"] = ("".join(str(n) for _, n in STAR)
                          + "".join(cell(i)[1].lower() for i in SRC))
    # round 12's nearest-entry-cell pairing, recomputed (not hard-coded)
    f["w2s1d5a4"] = "".join(
        cell(e)[1].lower() for _, n in sorted(STAR)
        for e in [min(SRC, key=lambda x: abs(rc(x)[0] - rc(st)[0])
                     + abs(rc(x)[1] - rc(st)[1]))
                  for st in [i for i in ROOTS if cell(i)[1] == "*"
                             and cell(i)[0] == n]])
    return f


def fam_b():
    """Route 1: 4 source entry letters x 4 star values, all slot choices."""
    sl = [CYCSTR[ENTRY[i]] for i in SRC]              # s a d a
    sv = [str(n) for _, n in STAR]                     # 3 1 2 4
    f = {}
    for k in range(5):
        for combo in itertools.combinations(range(8), 4):
            s = [None] * 8
            for c, sl_ in zip(combo, sl):
                s[c] = sl_
            j = 0
            for idx in range(8):
                if s[idx] is None:
                    s[idx] = sv[j]
                    j += 1
            f["route1_%s" % "".join(s)] = "".join(s)
    return f


def fam_c():
    """Route 2: source directions and/or values, six orders, two pairings."""
    dl = [cell(i)[1].lower() for i in SRC]            # d w a s
    dv = [str(cell(i)[0]) for i in SRC]                # 5 2 4 1
    sv = [str(n) for _, n in STAR]                     # 3 1 2 4
    orders = {
        "rowmajor": list(range(4)),
        "bycol": sorted(range(4), key=lambda k: rc(SRC[k])[1]),
        "byrow": sorted(range(4), key=lambda k: rc(SRC[k])[0]),
        "byval": sorted(range(4), key=lambda k: int(dv[k])),
        "rev_row": list(reversed(range(4))),
        "byentry": sorted(range(4), key=lambda k: ENTRY[SRC[k]]),
    }
    f = {}
    for on, o in orders.items():
        f["route2_%s_d%s" % (on, "".join(dl[k] for k in o))] = \
            "".join(dl[k] for k in o) + "".join(sv)
        f["route2_%s_dv" % on] = "".join(dl[k] for k in o) + "".join(dv[k] for k in o)
        f["route2_%s_vd" % on] = "".join(dv[k] for k in o) + "".join(dl[k] for k in o)
        f["route2_%s_i%s" % (on, "".join(dl[k] for k in o))] = \
            "".join(str(int(dv[k])) for k in o) + "".join(dl[k] for k in o)
    return f


def fam_d():
    """Route 3: every length-8 window of the 92-cycle."""
    return {"route3_%d" % k: CYCSTR[k:k + 8] for k in range(len(CYCSTR) - 7)}


def fam_e():
    """Route 4: all distinct permutations of the coordinate-index letters."""
    s = "".join(CYCSTR[i] for i in [1, 13, 38, 46, 79, 80, 82, 88])
    f = {}
    for p in set(itertools.permutations(s)):
        f["route4_" + "".join(p)] = "".join(p)
    return f


def fam_f():
    f = {}
    idxs = sorted(ROOTS)
    f["coord_asc"] = "".join(CYCSTR[i] for i in idxs)
    f["coord_desc"] = "".join(CYCSTR[i] for i in reversed(idxs))
    f["coord_cyc0"] = CYCSTR[idxs[0]] + "".join(CYCSTR[i] for i in idxs[1:])
    return f


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--words", type=int, default=5)
    ap.add_argument("--list-only", action="store_true")
    ap.add_argument("--show", type=int, default=40)
    ap.add_argument("--ship-words", type=int, default=4,
                    help="depth of the generated 24-char description family; "
                         "0 = the 6 hand-picked strings only")
    args = ap.parse_args()

    fam7 = gen_ship_family(args.ship_words) if args.ship_words else []
    fam7 = sorted(set(fam7) | set(SHIP))
    print("clue-7 family: %d distinct strings, all exactly 24 chars: %s"
          % (len(fam7), all(len(s) == 24 for s in fam7)))
    if args.ship_words:
        print("  (generated to depth %d; raises fast -- measure with"
              " clue7_family_size.py first)" % args.ship_words)
    if args.list_only:
        for s in fam7[:args.show]:
            print("  ", s)
        return 0

    fams = [("A root", fam_a), ("B route1", fam_b), ("C route2", fam_c),
            ("D route3", fam_d), ("E route4", fam_e), ("F coord", fam_f)]
    if args.ship_words == 0:
        fam7 = sorted(set(SHIP))
    total_pairs = 0
    any_hit = False
    union3 = set()
    for label, fn in fams:
        f = fn()
        f = {k: v for k, v in f.items() if len(v) == 8}
        n3 = len(set(f.values()))
        union3 |= set(f.values())
        print("\n[%s] %d distinct 8-char readings" % (label, n3))
        for k, v in sorted(f.items())[:args.show]:
            print("   %-28s %s" % (k, v))
        if len(f) > args.show:
            print("   ... and %d more" % (len(f) - args.show))
        hits = sweep(3, list(f.values()), fam7, label)
        total_pairs += n3 * len(fam7)
        if hits:
            any_hit = True
            print("   *** HIT ***", hits)
    print("\ntotal pairs tested: %d" % total_pairs)
    print("distinct clue-3 readings across all families: %d" % len(union3))
    print("HITS: %s" % ("YES" if any_hit else "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())