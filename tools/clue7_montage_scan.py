#!/usr/bin/env python3
"""Clue 7 -- scan the recovered red-LSB montage for structure the round-14
inspection did not measure: where the payload actually sits, how many ink
elements there are, whether any element carries TEXT (OCR), and whether the two
portraits are the same image.

Everything here is measured from clues/Ship.png.  The previous rounds read the
montage twice -- once from prose (wrong: "deck plans") and once from a render
("ship's line drawing", "moustache").  Neither pass asked the cheap questions
below, and clue 7 is the segment-3 bottleneck, so a text or caption found in the
plane would be the first 24-character candidate that is *read* rather than
guessed.
"""
from __future__ import annotations

import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PNG = os.path.join(ROOT, "clues", "Ship.png")
OUT = "/tmp/opencode"


def load_plane():
    a = np.array(Image.open(PNG).convert("RGBA")).astype(int)
    r = a[..., 0]
    return (r & 1).astype(np.uint8), r


def block_map(bit, B=16):
    h, w = bit.shape
    hb, wb = h // B, w // B
    m = bit[:hb * B, :wb * B].reshape(hb, B, wb, B).mean(axis=(1, 3))
    return m


def bands(profile, thr, minlen):
    out, start = [], None
    for i, v in enumerate(profile):
        if v >= thr and start is None:
            start = i
        elif v < thr and start is not None:
            if i - start >= minlen:
                out.append((start, i))
            start = None
    if start is not None and len(profile) - start >= minlen:
        out.append((start, len(profile)))
    return out


def main():
    bit, r = load_plane()
    h, w = bit.shape
    print("=" * 78)
    print("CLUE 7 -- red-LSB montage scan (%s)" % os.path.relpath(PNG, ROOT))
    print("=" * 78)
    print("size %dx%d   ink fraction %.4f" % (w, h, bit.mean()))

    os.makedirs(OUT, exist_ok=True)
    Image.fromarray(bit * 255).save(os.path.join(OUT, "ship_plane0.png"))

    # ---- 1. where is the payload? -------------------------------------------
    print("\n[1] WHERE THE PAYLOAD SITS (16x16 block ink map)")
    m = block_map(bit)
    print("    block map %dx%d; global mean %.4f" % (m.shape[1], m.shape[0],
                                                      m.mean()))
    for name, thr in (("ink blocks  (mean>0.05)", 0.05),
                      ("dense blocks(mean>0.30)", 0.30),
                      ("empty blocks(mean<0.01)", -0.01)):
        if name.startswith("empty"):
            idx = m < 0.01
        else:
            idx = m > thr
        if idx.any():
            ys, xs = np.where(idx)
            print("    %-24s %6d blocks  x %4d..%4d  y %4d..%4d"
                  % (name, idx.sum(), xs.min() * 16, (xs.max() + 1) * 16,
                     ys.min() * 16, (ys.max() + 1) * 16))

    # ---- 2. elements by projection ------------------------------------------
    print("\n[2] ELEMENTS (row/column ink profiles)")
    colp = bit.mean(axis=0)
    rowp = bit.mean(axis=1)
    cb = bands(colp, 0.30, w // 40)
    rb = bands(rowp, 0.20, h // 40)
    print("    vertical bands (x):   %s" % cb)
    print("    horizontal bands (y): %s" % rb)
    boxes = []
    for (x0, x1) in (cb if cb else [(0, w)]):
        for (y0, y1) in (rb if rb else [(0, h)]):
            boxes.append((x0, y0, x1, y1))
    boxes.sort(key=lambda b: -(b[2] - b[0]) * (b[3] - b[1]))
    for i, (x0, y0, x1, y1) in enumerate(boxes[:12]):
        sub = bit[y0:y1, x0:x1]
        print("    box %2d  x %4d..%4d y %4d..%4d  %4dx%4d  ink %.3f"
              % (i, x0, x1, y0, y1, x1 - x0, y1 - y0, sub.mean()))
        Image.fromarray(sub * 255).save(os.path.join(OUT, "ship_box%d.png" % i))

    # ---- 3. text-like components --------------------------------------------
    print("\n[3] TEXT-LIKE COMPONENTS (connected-component heuristic)")
    try:
        import cv2
    except ImportError:
        print("    cv2 unavailable; skipping")
        cv2 = None
    text_lines = []
    if cv2 is not None:
        n, lab, stats, cent = cv2.connectedComponentsWithStats(
            bit.astype(np.uint8), connectivity=8)
        comp = []
        for k in range(1, n):
            x, y, ww, hh, area = stats[k]
            if not (3 <= hh <= 26 and 1 <= ww <= 60 and 4 <= area <= 600):
                continue
            ar = ww / float(hh)
            if 0.06 <= ar <= 2.2:
                comp.append((x, y, ww, hh, area))
        print("    components: %d total, %d text-like" % (n - 1, len(comp)))
        comp.sort(key=lambda c: (c[1] // 12, c[0]))
        # group into lines by vertical overlap
        lines = []
        for c in comp:
            placed = False
            for ln in lines:
                if abs(ln[0][1] - c[1]) <= 5:
                    ln.append(c)
                    placed = True
                    break
            if not placed:
                lines.append([c])
        lines = [ln for ln in lines if len(ln) >= 4]
        lines.sort(key=len, reverse=True)
        print("    candidate text lines (>=4 glyphs): %d" % len(lines))
        for ln in lines[:8]:
            xs0 = min(c[0] for c in ln)
            xs1 = max(c[0] + c[2] for c in ln)
            ys0 = min(c[1] for c in ln)
            ys1 = max(c[1] + c[3] for c in ln)
            text_lines.append((xs0, ys0, xs1, ys1))
            print("      line: %2d glyphs  x %4d..%4d y %4d..%4d  h~%d"
                  % (len(ln), xs0, xs1, ys0, ys1,
                     int(np.median([c[3] for c in ln]))))

    # ---- 4. OCR --------------------------------------------------------------
    print("\n[4] OCR OF THE MONTAGE (tesseract, several scales/preprocessings)")
    try:
        import pytesseract
    except ImportError:
        print("    pytesseract unavailable")
        pytesseract = None
    if pytesseract is not None:
        targets = [("whole plane 1:1", bit, 1), ]
        for i, (x0, y0, x1, y1) in enumerate(boxes[:4]):
            targets.append(("box%d" % i, bit[y0:y1, x0:x1], 2))
        for i, (x0, y0, x1, y1) in enumerate(text_lines[:6]):
            pad = 4
            targets.append(("line%d" % i,
                            bit[max(0, y0 - pad):y1 + pad,
                                max(0, x0 - pad):x1 + pad], 4))
        seen = {}
        for name, sub, scale in targets:
            if sub.size == 0:
                continue
            im = Image.fromarray(sub * 255)
            if scale > 1:
                im = im.resize((im.width * scale, im.height * scale),
                               Image.NEAREST)
            for inv in (False, True):
                use = Image.fromarray(255 - np.array(im)) if inv else im
                for psm in (6, 7, 11):
                    try:
                        txt = pytesseract.image_to_string(use, config=(
                            "--psm %d -c tessedit_char_whitelist="
                            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
                            "0123456789" % psm)).strip()
                    except Exception as exc:
                        txt = ""
                        print("      (%s psm%d inv=%s error %s)"
                              % (name, psm, inv, exc))
                    clean = "".join(c for c in txt if c.isalnum())
                    if len(clean) >= 3 and clean not in seen:
                        seen[clean] = (name, psm, inv)
                        print("      %-14s psm%2d inv=%-5s -> %r"
                              % (name, psm, inv, clean))
        print("    distinct OCR strings with >=3 alphanumerics: %d" % len(seen))

    # ---- 5. are the two portraits the same image? ---------------------------
    print("\n[5] PORTRAIT COMPARISON (are the two faces one image?)")
    if len(boxes) >= 2:
        def prep(b):
            x0, y0, x1, y1 = b
            sub = bit[y0:y1, x0:x1]
            if sub.size == 0:
                return None
            return np.array(Image.fromarray(sub * 255).resize((128, 128),
                                                            Image.NEAREST))
        a = prep(boxes[0])
        b2 = prep(boxes[1])
        if a is not None and b2 is not None:
            def corr(u, v):
                u = u.astype(float) - u.mean()
                v = v.astype(float) - v.mean()
                d = (np.sqrt((u * u).sum()) * np.sqrt((v * v).sum()))
                return float((u * v).sum() / d) if d else 0.0
            print("    corr(box0, box1)          = %+.3f" % corr(a, b2))
            print("    corr(box0, mirror(box1))  = %+.3f"
                  % corr(a, np.fliplr(b2)))
            print("    corr(box0, rot180(box1))  = %+.3f"
                  % corr(a, np.rot90(b2, 2)))

    print("\nwrote crops to %s (ship_plane0.png, ship_box*.png)" % OUT)
    print("A found caption/nameplate would be the first clue-7 candidate that")
    print("is read from the image rather than guessed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
