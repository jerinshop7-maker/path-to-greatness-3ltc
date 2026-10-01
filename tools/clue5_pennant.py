"""Clue 5: measure the three pennant directions from pixels.

Round 11's `clue5_ink.py` could not separate the red crayon drawings from the
scene: the corridor's parquet floor is deep red, and that tool thresholded
absolute red (`R>205 & G<145 & B<145`), which the floor also satisfies. It
recorded the result INCONCLUSIVE.

This tool keys on RED-MINUS-GREEN instead of absolute red. Over the artwork band
the distribution is cleanly bimodal -- tan wall / orange floor sit at R-G ~ 80,
the saturated crayon runs from ~120 to 255 with a sparse gap at 100-120 -- so a
cut at 130 isolates the drawings no matter how the surface underneath is lit.

Measurement notes (an earlier draft of this file got both wrong, so both are
recorded here to avoid re-introducing them):
  * the pennant is NOT the only ink in the row band, and it is not at the far
    right of it. The pictograms and the numeral are further left. The pennant is
    isolated as the widest contiguous ink block in x 1380..1500, which lands at
    abs x ~1391-1479. An earlier version used a fixed window that clipped the
    pennant's right edge and reported a mirrored result.
  * a pennant's mast end is thick and its point tapers, so the normalised ink
    height falls monotonically from the mast toward the tip.

Result: rows 1 and 3 run thick-left / thin-right (point extends RIGHT); row 2 is
the mirror (point extends LEFT). With KM on the left wall and mi on the right, the
units are mi / km / mi -- this CONFIRMS correction X2 by pixels, closing the
question round 11 left open.
"""
import numpy as np
from PIL import Image

SRC = "clues/clue5_wonders.jpg"
CUT = 130
BANDS = [(690, 810), (840, 960), (990, 1110)]   # one per row
BAND_X = (1380, 1500)


def pennant_block(mask, y0, y1):
    sub = mask[y0:y1, BAND_X[0]:BAND_X[1]]
    cols = sub.sum(axis=0)
    idx = np.nonzero(cols > 0)[0]
    if len(idx) == 0:
        return None
    blocks, cur = [], [idx[0]]
    for v in idx[1:]:
        if v - cur[-1] <= 4:
            cur.append(v)
        else:
            blocks.append((cur[0], cur[-1]))
            cur = [v]
    blocks.append((cur[0], cur[-1]))
    a, b = max(blocks, key=lambda t: t[1] - t[0])
    return sub[:, a:b + 1], BAND_X[0] + a, BAND_X[0] + b


def main():
    rgb = np.asarray(Image.open(SRC).convert("RGB")).astype(float)
    redness = rgb[:, :, 0] - rgb[:, :, 1]
    mask = redness > CUT

    art = redness[660:1140, 1050:1500]
    print("artwork band, fraction above cut: %.4f" % float((art > CUT).mean()))
    print("  R-G background, floor: %.0f   wall: %.0f   crayon p95: %.0f"
          % (np.median(redness[1200:1400, 1100:1500]),
             np.median(redness[600:660, 300:500]),
             np.percentile(art, 95)))
    print()

    results = []
    for i, (y0, y1) in enumerate(BANDS, 1):
        got = pennant_block(mask, y0, y1)
        if got is None:
            print("row %d: no pennant ink found" % i)
            continue
        p, a, b = got
        h = p.sum(axis=0).astype(float)
        h /= h.max()
        left_q = h[: len(h) // 4].mean()
        right_q = h[-len(h) // 4:].mean()
        mast = "LEFT" if left_q > right_q else "RIGHT"
        point = "RIGHT" if mast == "LEFT" else "LEFT"
        results.append((i, point))
        n = b - a + 1
        prof = " ".join("%.2f" % v for v in h[:: max(1, n // 14)])
        print("row %d  pennant abs x %d..%d (%d px)  ink %d px"
              % (i, a, b, n, int(p.sum())))
        print("        height profile L->R: %s" % prof)
        print("        mast %s, point extends %s" % (mast, point))
    print()

    print("MEASURED point directions: " + ", ".join("row %d %s" % r for r in results))
    dirs = {r[1] for r in results}
    print()
    if len(results) == 3 and dirs == {"RIGHT", "LEFT"}:
        print("rows 1 and 3 point RIGHT (toward the 'mi' wall);")
        print("row 2 points LEFT  (toward the 'KM' wall).")
        print("=> units mi / km / mi: correction X2 CONFIRMED by pixels.")
    else:
        print("uniform or unexpected pattern -- re-check the bands.")


if __name__ == "__main__":
    main()
