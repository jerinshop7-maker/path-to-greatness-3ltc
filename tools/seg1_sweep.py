#!/usr/bin/env python3
"""Targeted segment sweeps with a CORRECT mask.

sweep.c mask classes: '.' printable, '0' digit, '?' all bytes, 'r' mirror 8 back.
Every other character means FIXED (take the template byte). So a fixed mask
position must use a char that is not '.', '0', '?', or 'r' -- 'x' is used here.
Passing the template as its own mask is a bug: every literal '0' in the template
silently becomes a free digit position.
"""
import subprocess
import sys

FIX = "x"


def mask_for(template, free_idx):
    return "".join("." if i in free_idx else FIX for i in range(32))


def run(seg, template, free_idx, timeout=None):
    m = mask_for(template, free_idx)
    cmd = ["./tools/sweep", str(seg), template, m]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return r.stderr.strip(), r.stdout.strip()


if __name__ == "__main__":
    IMAGINE = "1941071219410712"          # 19410712 written twice, per the clue
    BASE = "536531276755365"              # 15 scale degrees from Beach.png
    seg = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    for n in (1, 2, 3, 4):
        prefix = BASE[: len(BASE) - (n - 1)] if n > 1 else BASE[:15]
        tpl = (IMAGINE + prefix)[:32]
        tpl = tpl + "." * n
        assert len(tpl) == 32, (tpl, len(tpl))
        free = set(range(len(tpl) - n, 32))
        try:
            err, out = run(seg, tpl, free, timeout=1800)
        except subprocess.TimeoutExpired:
            print(f"n={n} prefix={prefix!r} TIMEOUT")
            continue
        hit = "HIT" if "hit" in out.lower() and "no hit" not in out.lower() else "no hit"
        print(f"n={n} beach={prefix!r} + {n} free -> {out.splitlines()[-1] if out else err.splitlines()[-1]}")
