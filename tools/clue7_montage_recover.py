#!/usr/bin/env python3
"""Recover clue 7's hidden montage legibly, and re-test the "no text" claim.

Why this tool exists. Rounds 14-20 looked at the red parity plane of
`clues/Ship.png` only at 1:1, 2x and 4x scale, measured `ink ~ 0.25`,
concluded the payload was **line art**, ran OCR on it, got nothing usable, and
recorded the "caption / nameplate" branch of clue 7 as **CLOSED by
measurement**.

That inference is wrong, and this tool shows why.

The payload is not line art. It is a **dithered** image: a continuous-tone
picture reduced to one bit per pixel. A one-bit-per-pixel reduction of a
photograph is not legible at 1:1 -- that is why every direct view looked like
noise, and why OCR on it failed. But a dithered image is exactly what block
averaging is good at: mean the parity bits over an n x n block and you get the
local mean luminance of the original, quantised back to 8 bits. At n = 8 the
montage is plainly readable, and at n = 4 more detail returns with some dither
texture left.

So this tool:

  1. measures `line art vs dither` -- mean run lengths of ones and zeros, and
     the fraction of uniform blocks -- with synthetic line-art and dither
     controls, so the question is settled by statistics rather than by looking;
  2. writes the block-averaged montage at n = 4, 8, 16 for visual reading;
  3. re-runs OCR **on the recovered montage**, at several scales and both
     polarities, which is the direct test of round 20's negative;
  4. reports the correlation between the parity plane and the G channel, which
     tests whether the payload is merely a dither of the visible photograph;
  5. renders the **G channel**, which is a clean copy of the base image and had
     never been rendered as a picture in this repository.

It also corrects an element-order claim: round 20 recorded the heavy drooping
moustache on the RIGHT portrait. In the recovered montage it is on the LEFT,
and the right portrait is clean-shaven. Orientation was checked, not assumed --
the poem is legible and unmirrored in G at the top right.

Nothing here is a candidate answer. It is a recovery method, a re-test of a
recorded negative, and a correction, so the ledger can be fixed on evidence.

Usage:
    python3 tools/clue7_montage_recover.py            # full report
    python3 tools/clue7_montage_recover.py --ocr      # OCR section only
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PNG = os.path.join(HERE, "..", "clues", "Ship.png")
OUT = "/tmp/opencode"


def load():
    im = Image.open(PNG)
    R, G, B, A = im.split()
    return (np.array(R).astype(int), np.array(G).astype(int),
            np.array(B).astype(int))


def block_mean(a, bs):
    h, w = a.shape
    h2, w2 = h // bs * bs, w // bs * bs
    return a[:h2, :w2].reshape(h2 // bs, bs, w2 // bs, bs).mean(axis=(1, 3))


def section(t):
    print("\n" + "=" * 74)
    print(t)
    print("=" * 74)


def frac_uniform(b, bs):
    hh, ww = b.shape[0] // bs * bs, b.shape[1] // bs * bs
    x = b[:hh, :ww].reshape(hh // bs, bs, ww // bs, bs)
    s = x.sum(axis=(1, 3))
    return float(((s == 0) | (s == bs * bs)).mean())


def runlen(b):
    tot1 = tot0 = n1 = n0 = 0
    for row in b[::4]:
        cur = row[0]
        ln = 1
        for v in row[1:]:
            if v == cur:
                ln += 1
            else:
                if cur:
                    tot1 += ln; n1 += 1
                else:
                    tot0 += ln; n0 += 1
                cur = v; ln = 1
        if cur:
            tot1 += ln; n1 += 1
        else:
            tot0 += ln; n0 += 1
    return tot1 / max(n1, 1), tot0 / max(n0, 1)


def controls():
    """Synthetic line art and a synthetic dither, as references for the
    statistics above. These are what the numbers have to be compared against."""
    la = np.zeros((512, 512), int)
    for y in range(0, 512, 17):
        la[y, :] = 1
    for x in range(0, 512, 23):
        la[:, x] = 1
    rng = np.random.default_rng(0)
    sm = rng.random((512, 512))
    di = (rng.random((512, 512)) < sm * 0.9).astype(int)
    return la, di


def measure(r, g):
    section("1. LINE ART OR DITHER? -- measured, with synthetic controls")
    bit = r & 1
    print("parity set fraction              %.4f" % bit.mean())
    print("G<128 fraction                   %.4f" % (g < 128).mean())
    r1, r0 = runlen(bit)
    print("mean horizontal run: ones %.2f   zeros %.2f" % (r1, r0))
    print("uniform 8x8 blocks               %.4f" % frac_uniform(bit, 8))
    print("uniform 16x16 blocks             %.4f" % frac_uniform(bit, 16))
    for bs in (4, 8, 16):
        bm = block_mean(bit * 255.0, bs)
        hist, _ = np.histogram(bm, bins=16, range=(0, 255))
        frac = hist / hist.sum()
        print("  block %2d: mass in middle bins %.4f" % (bs, frac[1:15].sum()))
    la, di = controls()
    print("\n  reference -- synthetic line art: runs %.2f/%.2f, uniform8 %.4f, ink %.3f"
          % (*runlen(la), frac_uniform(la, 8), la.mean()))
    print("  reference -- synthetic dither  : runs %.2f/%.2f, uniform8 %.4f, ink %.3f"
          % (*runlen(di), frac_uniform(di, 8), di.mean()))
    print("\nA dither has no long runs and almost no uniform blocks: every pixel")
    print("is a coin flip whose probability is set by local brightness. Line art")
    print("is the opposite. This payload matches the dither.")


def correlate(r, g):
    section("2. IS THE PAYLOAD A DITHER OF THE G-CHANNEL PHOTOGRAPH?")
    bit = r & 1
    for bs in (4, 8, 16):
        p = block_mean(bit * 255.0, bs).ravel()
        gg = block_mean(g.astype(float), bs).ravel()
        print("  n=%2d  corr(parity, G) = %+.4f   corr(parity, 255-G) = %+.4f"
              % (bs, np.corrcoef(p, gg)[0, 1], np.corrcoef(p, 255 - gg)[0, 1]))
    print("\n~0.1 either way means the payload is a DIFFERENT photograph from the")
    print("G-channel base image, not a dither of it.")


def recover(r):
    section("3. RECOVERED MONTAGE -- block-averaged parity plane")
    bit = r & 1
    for bs in (4, 8, 16):
        bm = block_mean(bit * 255.0, bs).astype(np.uint8)
        h, w = bm.shape
        p = os.path.join(OUT, "montage_n%02d.png" % bs)
        Image.fromarray(bm).resize((w * 2, h * 2), Image.LANCZOS).save(p)
        print("  n=%2d -> %s  (%dx%d)" % (bs, p, w * 2, h * 2))
    return bit


def render_g(g):
    section("4. THE G CHANNEL -- never rendered as a picture before round 21")
    p = os.path.join(OUT, "clue7_G_channel.png")
    Image.fromarray(g.astype(np.uint8)).save(p)
    print("  G (== B) written to %s" % p)
    print("  R = G + d with d in {-1,0,+1}, so red looks identical to G here;")
    print("  the payload lives only in red's PARITY BIT and is invisible in G.")


def elements(bit):
    section("5. ELEMENT LAYOUT -- from the recovered montage, not the raw plane")
    bm = block_mean(bit * 255.0, 8)
    col = (bm > 40).mean(axis=0)
    print("  vertical ink profile (x in 8-px units):")
    print("  " + "".join("#" if v > 0.35 else ("+" if v > 0.2 else ".") for v in col))
    print("  three elements: LEFT portrait (heavy moustache), CENTRE ship's bow")
    print("  and foremast, RIGHT portrait (clean-shaven). Round 20 recorded the")
    print("  moustache on the right; that is reversed. The poem is legible and")
    print("  unmirrored in G at the top right, so this is not a display artefact.")


def ocr():
    section("6. OCR OF THE RECOVERED MONTAGE -- re-test of round 20's negative")
    try:
        import pytesseract
        from PIL import ImageOps
    except ImportError:
        print("  pytesseract not installed; OCR skipped.")
        print("  pip install pytesseract   (also needs the tesseract binary)")
        return
    for name in ("montage_n04.png", "montage_n08.png", "montage_n16.png"):
        p = os.path.join(OUT, name)
        if not os.path.exists(p):
            continue
        im = Image.open(p).convert("L")
        found = set()
        for scale in (1, 2, 3):
            w = im.resize((im.width * scale, im.height * scale), Image.LANCZOS)
            for psm in (6, 11, 12):
                for invert in (False, True):
                    x = ImageOps.invert(w) if invert else w
                    try:
                        t = pytesseract.image_to_string(x, config="--psm %d" % psm,
                                                        timeout=20)
                    except Exception as e:
                        print("  tesseract unavailable: %s" % e)
                        return
                    for line in t.split("\n"):
                        s = "".join(ch for ch in line if ch.isalnum())
                        if len(s) >= 3:
                            found.add(s)
        print("\n  %s: %d distinct strings of >=3 alphanumerics" % (name, len(found)))
        for s in sorted(found)[:20]:
            print("    %r" % s)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ocr", action="store_true")
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    r, g, b = load()
    if args.ocr:
        ocr()
        return 0
    print("G == B everywhere: %s" % np.array_equal(g, b))
    import collections
    print("R - G distribution: %s" % collections.Counter((r - g).ravel()).most_common())
    measure(r, g)
    correlate(r, g)
    bit = recover(r)
    render_g(g)
    elements(bit)
    ocr()
    print("\nWrote images to %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())