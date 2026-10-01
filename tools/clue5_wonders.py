#!/usr/bin/env python3
"""Clue 5, round 10: "Charting the eight wonders" as famous-site GREAT-CIRCLE
distances -- the first numeric fit of 12,772 / 5,210 / 12,061.

Method, stated so it cannot be mistaken for a rigged fit:

  1. Start from the canonical EIGHT wonders (New7Wonders + the Great Pyramid --
     the reason a list has eight).  All 28 pairwise great-circle distances are
     computed and compared to the three printed numerals under the two unit
     readings the image allows:
        all-km      12,772 / 5,210 / 12,061
        mi/km/mi    20,554 / 5,210 / 19,411   (the repo's X2 reading)
  2. Then widen to a fixed pool of famous sites (incl. Angkor Wat, Uluru, ...)
     and report the closest pair to row 2, whose value lies outside the
     canonical-eight range.

Honest caveats, printed with the result: row 1 and row 3 matches come from the
*canonical-eight* pool (small, so meaningful); the row-2 match needs a site
outside the canonical seven, so it is a weaker, partly-searched fit.  The route
is never oracle-testable (clue 5 has no independent half).
"""
import itertools
import math

# canonical eight wonders
W8 = {
    "Great Wall": (40.4319, 116.5704),
    "Petra": (30.3285, 35.4444),
    "Colosseum": (41.8902, 12.4922),
    "Chichen Itza": (20.6843, -88.5678),
    "Machu Picchu": (-13.1631, -72.5450),
    "Taj Mahal": (27.1751, 78.0421),
    "Christ the Redeemer": (-22.9519, -43.2105),
    "Great Pyramid of Giza": (29.9792, 31.1342),
}
# wider pool for row 2 (fixed, listed for reproducibility)
POOL = dict(W8)
POOL.update({
    "Angkor Wat": (13.4125, 103.8670),
    "Uluru": (-25.3444, 131.0369),
    "Stonehenge": (51.1789, -1.8262),
    "Easter Island": (-27.1127, -109.3497),
    "Mount Fuji": (35.3606, 138.7274),
    "Mount Everest": (27.9881, 86.9250),
    "Iceland": (64.9631, -19.0208),
    "K2": (35.8808, 76.5150),
    "Victoria Falls": (-17.9243, 25.8572),
    "Grand Canyon": (36.1069, -112.1129),
    "Amazon (Manaus)": (-3.1190, -60.0217),
    "Gobi (Ulaanbaatar)": (47.8864, 106.9057),
    "Sahara (Tamanrasset)": (22.7850, 5.5228),
    "Niagara Falls": (43.0962, -79.0377),
    "Yellowstone": (44.4280, -110.5885),
    "Lake Baikal": (53.5587, 108.1650),
    "Serengeti": (-2.3333, 34.8333),
    "Salar de Uyuni": (-20.1338, -67.4891),
    "Antarctica (Vostok)": (-78.4645, 106.8330),
    "Great Barrier Reef": (-18.2871, 147.6992),
})
KM_PER_MI = 1.609344


def hav(a, b):
    r = 6371.0088
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp, dl = p2 - p1, math.radians(b[1] - a[1])
    x = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(x))


def best(pool, target, k=3):
    ds = [(abs(hav(a, b) - target), na, nb, hav(a, b))
          for (na, a), (nb, b) in itertools.combinations(pool.items(), 2)]
    ds.sort()
    return ds[:k]


def main():
    print("EARTH MAX great-circle distance = %.1f km\n" % (math.pi * 6371.0088))

    for label, targets in (
        ("all-km   (12772 / 5210 / 12061 km)",
         [("row1", 12772.0), ("row2", 5210.0), ("row3", 12061.0)]),
        ("mi/km/mi (20554 / 5210 / 19411 km)",
         [("row1", 12772 * KM_PER_MI), ("row2", 5210.0), ("row3", 12061 * KM_PER_MI)]),
    ):
        print("=== reading: %s ===" % label)
        for name, t in targets:
            ds = best(W8, t)
            off, na, nb, d = ds[0]
            print("  %-5s %8.0f km -> %s <-> %s = %.1f km  (off %.1f, %.2f%%)"
                  % (name, t, na, nb, d, off, 100 * off / t))
        print()

    print("row 2 %d km: closest pairs in the WIDER pool" % 5210)
    for off, na, nb, d in best(POOL, 5210.0):
        print("   %-22s <-> %-22s %8.1f km  off %.1f" % (na, nb, d, off))

    print("\nPROPOSED TRIPLE (all-km):")
    rows = [("row1", 12772.0, "Great Wall", "Chichen Itza"),
            ("row2", 5210.0, "Angkor Wat", "Uluru"),
            ("row3", 12061.0, "Machu Picchu", "Great Pyramid of Giza")]
    for name, t, a, b in rows:
        d = hav(W8.get(a, POOL[a]), W8.get(b, POOL[b]))
        print("   %-5s %-20s <-> %-22s %8.1f km  vs printed %d  (off %+.1f, %.2f%%)"
              % (name, a, b, d, t, d - t, 100 * (d - t) / t))
    print("\nSIX sites used: Great Wall, Chichen Itza, Angkor Wat, Uluru,")
    print("Machu Picchu, Great Pyramid of Giza -- exactly the six pictograms' count.")
    print("Row 2 needs a site OUTSIDE the canonical seven (weaker fit).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
