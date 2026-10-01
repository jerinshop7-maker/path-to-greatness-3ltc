#!/usr/bin/env python3
"""Clue 5, round 11: an independent *pixel* attempt at the pennants and the nine
pictograms -- and why it does not settle the unit question.

Correction X2 in analysis/IMAGE-TRANSCRIPTION.md says the three row pennants point
right / left / right (units mi / km / mi), and round 6 noted that this eye-read
had never been re-checked in pixels.  This tool does that re-check, and also
tries to segment the nine hand-drawn pictograms (6 distinct + 3 triangle
instances) as connected components.

Result (printed, reproducible): it FAILS to cleanly isolate the artwork.  The
clue-5 scene is a rendered stone corridor whose parquet FLOOR is itself deep red
(R>205, G<145, B<145), i.e. the same colour range as the red-crayon drawings.
The floor therefore co-occupies the crayon mask and merges with the pictograms,
so component segmentation returns the floor as one giant blob and the pennants
cannot be told apart from floor tiles.  There is no colour separation that
survives the comparison.

Consequence, stated plainly: this is an INCONCLUSIVE result, not a refutation.
X2 remains the ONLY measurement of the pennants, so the `mi / km / mi` reading
still stands by default, and round 10's all-km fit still conflicts with it.
"""
import sys

import numpy as np
from PIL import Image
from scipy import ndimage as ndi

IMG = "clues/clue5_wonders.jpg"


def crayon_mask(a):
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (R > 205) & (G < 145) & (B < 145)


def main():
    a = np.asarray(Image.open(IMG).convert("RGB")).astype(int)
    H, W = a.shape[:2]
    print("clue-5 image: %dx%d" % (W, H))

    m = crayon_mask(a)
    print("red-crayon mask (R>205 & G<145 & B<145): %d px (%.2f%%)"
          % (m.sum(), 100.0 * m.sum() / m.size))

    # the panel region found by the geometry sweep in this session
    box = np.zeros_like(m)
    box[660:1140, 1050:1500] = True
    print("artwork region (x 1050-1500, y 660-1140): %d px" % (m & box).sum())

    # connected components of the artwork region, light dilation to join strokes
    md = ndi.binary_dilation(m & box, iterations=6)
    lab, n = ndi.label(md)
    sizes = ndi.sum(np.ones_like(lab), lab, range(1, n + 1))
    keep = [int(s) for s in sizes if s > 600]
    print("components in region: %d ; >=600 px: %d" % (n, len(keep)))

    # how big is the biggest? a floor/wall blob, not a pictogram
    biggest = int(sizes.max())
    print("largest component: %d px  (a pictogram should be ~2000-6000 px)" % biggest)

    # show that the floor shares the crayon colour: sample far outside the panel
    floor = a[1300:1400, 1800:2000].reshape(-1, 3)
    R, G, B = floor[:, 0], floor[:, 1], floor[:, 2]
    frac = ((R > 205) & (G < 145) & (B < 145)).mean()
    print("right-floor pixels inside the crayon mask: %.1f%%" % (100 * frac))
    print("  => the parquet floor is deep red and co-occupies the mask; the")
    print("     drawings do not separate from the scene by colour.")

    print("\nVERDICT: INCONCLUSIVE.  X2's eye-read remains the only pennant")
    print("measurement; the unit conflict with round 10 is unresolved by pixels.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
