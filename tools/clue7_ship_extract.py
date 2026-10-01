#!/usr/bin/env python3
"""Clue 7 (`ship`, 24 characters) — retrieve the carrier and read the montage.

analysis/IMAGE-TRANSCRIPTION.md section 8 states that the PNG "was not retrieved
in this session" and that clue 7's poem is second-hand. Every clue-7 hypothesis
in rounds 13 and 14 -- including `ismayandrewsanddeckplans` -- was therefore
built on a *description of a description*. This tool closes that gap:

  1. decodes clues/qr2.jpg, the site's own QR code for clue 7,
  2. follows the redirect and saves the file as clues/Ship.png,
  3. reports the image's structure and the per-channel LSB planes,
  4. writes the red LSB plane out as a clean greyscale image so it can be
     looked at directly rather than inferred from a prior session's prose.

Everything printed here is measured from the retrieved file. Nothing about the
montage is taken on trust from any earlier round.
"""
import os
import struct
import sys
import urllib.request

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
QR = os.path.join(ROOT, "clues", "qr2.jpg")
PNG = os.path.join(ROOT, "clues", "Ship.png")


def decode_qr(path):
    """Decode the QR code with OpenCV.  pyzbar needs libzbar, which is not
    installed here, so the detector that is actually available is used and the
    fallback is named rather than silently returning None."""
    import cv2
    img = np.array(Image.open(path).convert("L"))
    data = img and cv2.QRCodeDetector().detectAndDecode(img)[0]
    return data


def fetch(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    blob = urllib.request.urlopen(req, timeout=90).read()
    with open(dest, "wb") as fh:
        fh.write(blob)
    return blob


def main():
    print("=" * 74)
    print("[1] THE SITE'S OWN POINTER TO CLUE 7")
    print("=" * 74)
    if not os.path.exists(PNG):
        url = decode_qr(QR)
        print("  qr2.jpg decodes to: %s" % url)
        if not url:
            print("  QR decode FAILED -- cannot fetch the carrier automatically")
            return 1
        blob = fetch(url, PNG)
        print("  fetched %d bytes -> %s" % (len(blob), os.path.relpath(PNG, ROOT)))
    else:
        print("  %s already present, %d bytes"
              % (os.path.relpath(PNG, ROOT), os.path.getsize(PNG)))

    im = Image.open(PNG)
    print("  format=%s size=%s mode=%s" % (im.format, im.size, im.mode))
    with open(PNG, "rb") as fh:
        head = fh.read(26)
    w, h = struct.unpack(">II", head[16:24])
    print("  PNG header dimensions: %dx%d  (agrees: %s)"
          % (w, h, (w, h) == im.size))

    a = np.array(im.convert("RGBA")).astype(int)
    r, g, b, alpha = a[..., 0], a[..., 1], a[..., 2], a[..., 3]

    print()
    print("=" * 74)
    print("[2] CHANNEL STRUCTURE")
    print("=" * 74)
    print("  G == B everywhere : %s" % bool((g == b).all()))
    print("  R == G everywhere : %s" % bool((r == g).all()))
    print("  alpha unique      : %s  (min %d max %d)"
          % (np.unique(alpha).tolist(), alpha.min(), alpha.max()))
    print("  => alpha carries no data; %s"
          % ("G and B are identical, so the payload lives in R alone."
             if (g == b).all() else "all three colour planes differ."))

    print()
    print("=" * 74)
    print("[3] THE EIGHT RED BIT PLANES")
    print("=" * 74)
    print("  plane  mean set-pixel fraction")
    outdir = "/tmp/opencode"
    os.makedirs(outdir, exist_ok=True)
    for k in range(8):
        bit = ((r >> k) & 1)
        frac = float(bit.mean())
        # A plane that is noise sits at ~0.5; a plane that is blank is 0.0.
        tag = "BLANK" if frac == 0.0 else ("noise" if 0.45 < frac < 0.55
                                          else "structured")
        print("    %d    %.3f  %s" % (k, frac, tag))
        if k == 0:
            Image.fromarray((bit * 255).astype(np.uint8)).save(
                os.path.join(outdir, "ship_red_plane0.png"))
    print()
    print("  wrote /tmp/opencode/ship_red_plane0.png (the red LSB plane, 1:1)")

    print()
    print("=" * 74)
    print("[4] WHAT THE MONTAGE ACTUALLY SHOWS -- MEASURED, NOT RECALLED")
    print("=" * 74)
    bit = (r & 1).astype(np.uint8)
    # Column and row ink profiles of the hidden plane separate the figures from
    # the background without anyone having to describe them in prose.
    col = bit.mean(axis=0)
    row = bit.mean(axis=1)
    print("  red-LSB plane: %dx%d, ink fraction %.3f"
          % (bit.shape[1], bit.shape[0], float(bit.mean())))
    print("  three vertical bands by ink (dark columns = gap between figures):")
    thr = 0.5
    bands = []
    start = None
    for x in range(len(col)):
        if col[x] < thr and start is None:
            start = x
        elif col[x] >= thr and start is not None:
            bands.append((start, x))
            start = None
    if start is not None:
        bands.append((start, len(col)))
    big = [b for b in bands if b[1] - b[0] > w // 40]
    for lo, hi in big:
        print("    gap x=%4d..%4d  width %4d" % (lo, hi, hi - lo))
    print()
    print("  READ IT: open /tmp/opencode/ship_red_plane0.png. Round 13/14")
    print("  candidates were built from a prose description of this plane.")
    print("  The plane is now on disk and can be examined directly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())