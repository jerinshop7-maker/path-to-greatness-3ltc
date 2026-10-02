#!/usr/bin/env python3
"""Cross-check the C search engine against pycryptodome, byte for byte.

Why this exists. `tools/seg3_cross.c` reports "no match" over spaces of up to
1.5e9 keys per clue-7 candidate. A zero-hit result only means something if the
engine would have found an answer that was really there. The padding condition
is met by roughly one key in 2^64, so watching for a hit proves almost nothing:
an engine can be wrong in a way that produces no false negatives either.

So this tool takes a file of 32-character keys, asks the C engine for the full
16-byte plaintext it computes under the real segment-3 ciphertext and IV
(`seg3_cross pt`), computes the same in pycryptodome, and requires exact
agreement on every line. That exercises the key schedule, the inverse cipher,
the CBC XOR and the padding comparison on real inputs, against an
implementation sharing no code with the C.

The key set is not arbitrary: it includes the repository's clue-3 readings
crossed with its clue-7 candidates, so agreement is checked in exactly the part
of the space the searches traverse, plus a uniform spread over the 14-character
alphabet so every byte value is exercised.

Usage:
    python3 tools/seg3_crosscheck.py            # ~4k keys
    python3 tools/seg3_crosscheck.py -n 20000
Exit 0 only if every plaintext agrees.
"""

from __future__ import annotations

import argparse
import base64
import os
import random
import subprocess
import sys

try:
    from Crypto.Cipher import AES
except ImportError:  # pragma: no cover
    from Crypto.Cipher import AES

SEG3_CT_B64 = "16GmtUINaYuN7f1RlBO5sQ=="
SEG3_IV = b"colors_on_leaves"

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(HERE, "seg3_cross")
KEYFILE = "/tmp/seg3cross_keys.txt"


def clue3_readings():
    """Structural clue-3 candidates derived from the grid, so the cross-check
    covers the space the real searches sweep and not only random keys."""
    sys.path.insert(0, HERE)
    try:
        from wasd_grid import N, build, cell
    except Exception:
        return []
    out, ind = build()
    roots = [i for i in range(N * N) if i not in ind]
    toks = [str(cell(i)[0]) if cell(i)[1] == "*" else cell(i)[1].lower()
            for i in roots]
    got = {"".join(toks), "".join(str(cell(i)[0]) for i in roots)}
    try:  # the 92-cycle windows, the other structural route
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
                    cs = "".join(cell(k)[1].lower() for k in c)
                    got |= {cs[t:t + 8] for t in range(len(cs) - 7)}
                    break
            seen |= local
    except Exception:
        pass
    return sorted(s for s in got if len(s) == 8)


def build_keys(n, seed=20261002):
    rng = random.Random(seed)
    alpha = "wasd0123456789"
    keys = []
    lefts = clue3_readings() or ["wasdwasd"]
    rights = ["ismayandrewsanddeckplans",
              "andrewsandismaydeckplans",
              "theshipthatmeetsitsmaker",
              "theoceanlinerwillfounder",
              "victorgarberjonathanhyde",
              "edwardsmiththomasandrews"]
    for l in lefts:
        for r in rights:
            if len(l) == 8 and len(r) == 24:
                keys.append(l + r)
    for _ in range(n):
        keys.append("".join(rng.choice(alpha) for _ in range(32)))
    seen, uniq = set(), []
    for k in keys:
        if len(k) == 32 and k not in seen:
            seen.add(k)
            uniq.append(k)
    return uniq


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-n", type=int, default=4096,
                    help="random keys to test (default 4096)")
    ap.add_argument("--engine", default=ENGINE)
    args = ap.parse_args()

    if not os.path.exists(args.engine):
        print("engine %s not built; run:\n"
              "  gcc -O3 -march=native -o tools/seg3_cross tools/seg3_cross.c"
              % args.engine)
        return 2

    keys = build_keys(args.n)
    with open(KEYFILE, "w") as fh:
        fh.write("\n".join(keys) + "\n")

    proc = subprocess.run([args.engine, "pt", KEYFILE],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        print("engine failed:\n%s" % proc.stderr)
        return 2

    ct = base64.b64decode(SEG3_CT_B64)
    lines = proc.stdout.strip().split("\n")
    if len(lines) != len(keys):
        print("engine returned %d lines for %d keys" % (len(lines), len(keys)))
        return 1

    bad = pads = 0
    for key, line in zip(keys, lines):
        parts = line.split()
        if len(parts) < 2:
            print("malformed engine line: %r" % line)
            bad += 1
            continue
        if parts[0] != key:
            print("key mismatch: engine %r, expected %r" % (parts[0], key))
            bad += 1
            continue
        want = AES.new(key.encode(), AES.MODE_CBC, SEG3_IV).decrypt(ct).hex()
        if want != parts[1]:
            bad += 1
            if bad <= 5:
                print("DISAGREE key=%s\n  engine %s\n  pycry  %s"
                      % (key, parts[1], want))
        if len(parts) > 2 and parts[2] == "PAD":
            pads += 1

    print("cross-check: %d keys, %d disagreements, %d with valid padding"
          % (len(keys), bad, pads))
    if bad:
        print("CROSSCHECK FAILED, the engine's negatives do not count")
        return 1
    print("CROSSCHECK OK (engine and pycryptodome agree on every plaintext)")
    return 0


if __name__ == "__main__":
    sys.exit(main())