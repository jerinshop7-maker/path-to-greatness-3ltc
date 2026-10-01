#!/usr/bin/env python3
"""Clue 2, round 6: per-character ink analysis of the 41-cell line.

Segments the line-3 text box into its 41 character cells, then for each cell
reports the mean luminance, mean RGB and ink coverage of the glyph pixels. If
the author marked the answer by drawing some glyphs a different shade/tint, this
is where it shows.
"""
import sys

import numpy as np
from PIL import Image

SRC = "clues/clue2_scramble.jpg"


def main():
    im = Image.open(SRC).convert("RGB").rotate(-90, expand=True)
    rgb = np.asarray(im).astype(float)
    L = rgb.mean(axis=2)

    # line-3 tesseract banner: left=347 top=1352 width=823 height=34
    x0, y0, w, h = 347, 1352, 823, 34
    pad = 6
    crop = L[y0 - pad:y0 + h + pad, x0 - pad:x0 + w + pad]
    crop_rgb = rgb[y0 - pad:y0 + h + pad, x0 - pad:x0 + w + pad]
    print("crop", crop.shape, "mean", crop.mean())

    # background = brightest part of panel? print histogram
    print("lum percentiles", [round(float(np.percentile(crop, p)), 1) for p in (1, 5, 25, 50, 75, 95, 99)])

    n = 41
    pitch = (w + 2 * pad) / n
    print("pitch", pitch)
    cells = []
    for k in range(n):
        a = int(round(k * pitch))
        b = int(round((k + 1) * pitch))
        sub = crop[:, a:b]
        sur = crop_rgb[:, a:b]
        cells.append((k + 1, sub, sur))

    # ink = darker or lighter than background? show both polarities relative to median
    med = np.median(crop)
    print("median lum of crop", med)
    print("\ncell  meanL   stdL   dark%  light%   meanR  meanG  meanB   inkmean")
    stats = []
    for k, sub, sur in cells:
        m = sub.mean()
        s = sub.std()
        dark = float((sub < med - 25).mean())
        light = float((sub > med + 25).mean())
        sr, sg, sb = sur.reshape(-1, 3).mean(axis=0)
        # ink mask = pixels far from background in either direction
        mask = np.abs(sub - med) > 30
        inkmean = float(sub[mask].mean()) if mask.any() else 0.0
        stats.append((k, m, s, dark, light, inkmean, sr, sg, sb, mask.sum()))
        print("%3d  %6.1f %6.1f %6.3f %6.3f  %6.1f %6.1f %6.1f  %7.1f  n=%d"
              % (k, m, s, dark, light, sr, sg, sb, inkmean, mask.sum()))

    # flag outliers in ink columns
    ink = np.array([s[5] for s in stats])
    cov = np.array([s[9] for s in stats])
    for name, v in (("mean", np.array([s[1] for s in stats])), ("ink", ink), ("cov", cov)):
        z = (v - v.mean()) / (v.std() + 1e-9)
        out = [(i + 1, round(float(v[i]), 1), round(float(z[i]), 2)) for i in range(n) if abs(z[i]) > 2]
        print("\n%s outliers |z|>2:" % name, out)

    # render each cell as coarse ascii for the first 12 cells to compare glyphs
    print("\nASCII of cells 5-15 (max downsampled):")
    for k, sub, sur in cells[4:15]:
        small = np.asarray(Image.fromarray(sub.astype(np.uint8)).resize((10, 8)))
        rows = []
        for r in small:
            rows.append("".join("#" if x < med - 30 else ("." if x > med + 30 else " ") for x in r))
        print("cell %d:" % k)
        print("\n".join(rows))


if __name__ == "__main__":
    sys.exit(main())
