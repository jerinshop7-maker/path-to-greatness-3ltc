#!/usr/bin/env python3
"""Generate the witness file that tools/seg3_cross.c requires.

Why this is a separate program. `seg3_cross.c` needs proof, before it may
report any negative, that its padding test can find an answer that is really
there. Planting a witness requires AES *encryption*. An earlier version of the
C file carried its own forward cipher; its decrypt agreed with pycryptodome
while its encrypt did not, so the forward cipher was removed rather than
trusted, and witness generation moved here, in a library that shares no code
with the C engine.

A witness is a pair
    key32 = clue3 (8 chars) || clue7 (24 chars)
    ct    = AES-256-CBC(key32, iv, "WITNESS!" + 8 x 0x08)
such that `seg3_cross.c`'s test decrypts `ct` to a plaintext whose last eight
bytes are 0x08. It is the *witness* ciphertext, not the real segment-3
ciphertext, that is checked; the real ciphertext is what the engine sweeps.

Witness keys are drawn from the streams actually being swept, so a hit inside
a real family is guaranteed re-findable by that same run. A witness whose key
is not in a given family simply does not participate in it, and the engine
reports which ones it used.

Usage:
    python3 tools/seg3_witnesses.py --selftest
        prints and checks the pycryptodome AES-256 ECB vector that the C
        selftest is hard-coded against

    python3 tools/seg3_witnesses.py list  <lefts> <rights> -o wit.txt
        three witnesses: head, middle and tail of the cross product

    python3 tools/seg3_witnesses.py alpha <rights> -o wit.txt
        one witness whose clue-3 half is "wasdwasd" (inside "wasd0123456789")
        and whose clue-7 half is the middle entry of the list
"""

from __future__ import annotations

import argparse
import sys

try:
    from Crypto.Cipher import AES
except ImportError:  # pragma: no cover
    from Crypto.Cipher import AES

SEG3_CT_B64 = "16GmtUINaYuN7f1RlBO5sQ=="
SEG3_IV = b"colors_on_leaves"
PAYLOAD = b"WITNESS!" + b"\x08" * 8

SELFTEST_KEY = bytes.fromhex(
    "1bad420c0aa898aa5485483e92cd5d3a0af14dd7516d148eb6602ad6434bf064")
SELFTEST_PT = bytes.fromhex("502414db284e8198f5bf7af67344af2a")
SELFTEST_CT = bytes.fromhex("ff741e83ed1f12662dbebacb7cb56483")


def selftest() -> int:
    import base64
    ok = True
    got = AES.new(SELFTEST_KEY, AES.MODE_ECB).encrypt(SELFTEST_PT)
    t1 = got == SELFTEST_CT
    print("pycryptodome AES-256 ECB         -> %s" % ("OK" if t1 else "FAIL"))
    ok &= t1

    t2 = AES.new(SELFTEST_KEY, AES.MODE_ECB).decrypt(SELFTEST_CT) == SELFTEST_PT
    print("pycryptodome AES-256 ECB inverse -> %s" % ("OK" if t2 else "FAIL"))
    ok &= t2

    ct = base64.b64decode(SEG3_CT_B64)
    t3 = (len(ct) == 16 and len(SEG3_IV) == 16 and SEG3_CT_B64.endswith("==")
          and SEG3_CT_B64[21] in "AQgw")
    print("segment 3 parameters (%d bytes, %d-char IV, base64[21]=%r) -> %s"
          % (len(ct), len(SEG3_IV), SEG3_CT_B64[21], "OK" if t3 else "FAIL"))
    ok &= t3

    key = b"wasdwasd" + b"a" * 24
    w = AES.new(key, AES.MODE_CBC, SEG3_IV).encrypt(PAYLOAD)
    t4 = AES.new(key, AES.MODE_CBC, SEG3_IV).decrypt(w)[8:] == b"\x08" * 8
    print("planted witness round trip        -> %s" % ("OK" if t4 else "FAIL"))
    ok &= t4

    t5 = AES.new(b"x" * 32, AES.MODE_CBC, SEG3_IV).decrypt(w)[8:] != b"\x08" * 8
    print("wrong key rejected                -> %s" % ("OK" if t5 else "FAIL"))
    ok &= t5

    print("SELFTEST OK" if ok else "SELFTEST FAILED")
    return 0 if ok else 1


def read_list(path, want):
    out, dropped = [], 0
    with open(path) as fh:
        for line in fh:
            s = line.rstrip("\n").rstrip("\r")
            if not s:
                continue
            if len(s) != want:
                dropped += 1
                continue
            out.append(s.lower())
    if dropped:
        print("  %s: dropped %d line(s) not exactly %d chars"
              % (path, dropped, want), file=sys.stderr)
    return out


def emit(name, left, right, lines, summary):
    key = (left + right).encode()
    if len(key) != 32:
        raise SystemExit("witness key is %d bytes, need 32" % len(key))
    ct = AES.new(key, AES.MODE_CBC, SEG3_IV).encrypt(PAYLOAD)
    lines.append("%-10s %s %s" % (name, key.decode(), ct.hex()))
    summary.append("  %-10s clue3=%-8s clue7=%s" % (name, left, right))


def mode_list(lefts_path, rights_path):
    lefts = read_list(lefts_path, 8)
    rights = read_list(rights_path, 24)
    if not lefts or not rights:
        raise SystemExit("nothing to plant: empty side")
    picks = [("head", 0, 0),
             ("mid", len(lefts) // 2, len(rights) // 2),
             ("tail", len(lefts) - 1, len(rights) - 1)]
    lines, summary = [], []
    for name, li, ri in picks:
        emit(name, lefts[li], rights[ri], lines, summary)
    return lines, summary


def mode_alpha(rights_path):
    rights = read_list(rights_path, 24)
    if not rights:
        raise SystemExit("nothing to plant: empty right list")
    lines, summary = [], []
    emit("alpha", "wasdwasd", rights[len(rights) // 2], lines, summary)
    return lines, summary


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("mode", nargs="?", choices=("list", "alpha"))
    ap.add_argument("paths", nargs="*")
    ap.add_argument("-o", "--out")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if args.mode == "list" and len(args.paths) == 2:
        lines, summary = mode_list(*args.paths)
    elif args.mode == "alpha" and len(args.paths) == 1:
        lines, summary = mode_alpha(args.paths[0])
    else:
        ap.print_help()
        return 2

    text = "\n".join(lines) + "\n"
    if args.out:
        with open(args.out, "w") as fh:
            fh.write(text)
        print("wrote %d witness(es) to %s" % (len(lines), args.out))
    else:
        sys.stdout.write(text)
    print("planted keys (each lies inside the stream the matching mode sweeps):")
    for line in summary:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())