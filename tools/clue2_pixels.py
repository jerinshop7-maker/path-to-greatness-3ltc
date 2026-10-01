#!/usr/bin/env python3
"""Clue 2, round 6: pixel-level read of the clue-2 panel.

All previous work OCR'd or measured geometry of clue2_scramble.jpg. Nobody has
measured the *ink*: whether some characters are drawn in a different shade,
weight or colour (a classic way to hide "which letters to take").

This tool:
  1. rotates the panel upright,
  2. locates the three text lines,
  3. segments the 41-character line into cells using tesseract word boxes,
  4. reports per-cell ink statistics and flags outliers.
"""
import subprocess
import sys

import numpy as np
from PIL import Image

SRC = "clues/clue2_scramble.jpg"


def rotate_upright(im):
    """The text runs bottom-to-top in the source (rotated 90 CCW), so rotate CW."""
    return im.rotate(-90, expand=True)


def main():
    im = Image.open(SRC).convert("RGB")
    print("source size", im.size)
    up = rotate_upright(im)
    print("upright size", up.size)
    up.save("/tmp/clue2_upright.png")

    # tesseract word boxes on the upright panel
    up.save("/tmp/clue2_tsv.png")
    r = subprocess.run(["tesseract", "/tmp/clue2_tsv.png", "stdout", "--psm", "6", "tsv"],
                       capture_output=True, text=True)
    lines = r.stdout.splitlines()
    hdr = lines[0].split("\t")
    rows = [dict(zip(hdr, l.split("\t"))) for l in lines[1:] if l.strip()]
    words = [w for w in rows if w.get("text", "").strip()]
    for w in words:
        print("%5s %5s %5s %5s  conf=%-4s %r" % (w["left"], w["top"], w["width"],
              w["height"], w["conf"], w["text"]))

    # line 3 is the longest / bottom-most group
    if words:
        ym = max(int(w["top"]) + int(w["height"]) for w in words)
        # group by rounded top
        groups = {}
        for w in words:
            key = round(int(w["top"]) / 10)
            groups.setdefault(key, []).append(w)
        print("\nline groups:")
        for k in sorted(groups):
            ws = sorted(groups[k], key=lambda w: int(w["left"]))
            print("  top~%s: %s" % (k * 10, " ".join(w["text"] for w in ws)))

    a = np.asarray(up.convert("L")).astype(float)
    print("\nglobal mean %.1f  p1 %.1f  p99 %.1f" % (a.mean(), np.percentile(a, 1),
          np.percentile(a, 99)))


if __name__ == "__main__":
    sys.exit(main())
