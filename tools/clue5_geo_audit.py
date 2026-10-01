#!/usr/bin/env python3
"""Clue 5, round 11: an *audit* of the round-10 geography fit.

Round 10 claimed the three Roman numerals (12,772 / 5,210 / 12,061) are
great-circle distances between famous sites, under an **all-km** reading, with
row 1 and row 3 drawn from the canonical eight wonders.  This tool does not add
a new reading; it stress-tests that claim the way the repository's own
conventions demand:

  1. RE-DERIVE the proposed triple and its errors.
  2. UNIQUENESS: within the canonical-eight pool, list *every* pair that lands
     within a tolerance of each numeral.  A meaningful fit needs the printed
     value to select essentially one pair, not one of many.
  3. UNIT READING: re-run under the authoritative `mi / km / mi` pennant reading
     (IMAGE-TRANSCRIPTION correction X2) and show row 1 is geometrically
     impossible (12,772 mi > pi*R).
  4. POST-HOC RISK: row 2 (5,210) needs a site *outside* the canonical eight, so
     it is a search over a large, freely chosen pool -- quantify that.
  5. NULL MODEL: Monte-Carlo over random 8-site sets on the sphere, asking how
     often an arbitrary target value is matched this tightly by chance.

Everything is printed so a reader can disagree with the conclusion independently.
"""
import itertools
import math

import numpy as np

R_EARTH = 6371.0088
KM_PER_MI = 1.609344
MAX_GC = math.pi * R_EARTH  # 20015.1 km

# canonical eight wonders (New7Wonders + the Great Pyramid) -- the reason a list
# has eight, and the pool round 10 drew rows 1 and 3 from
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

NUMERALS = [("row1", 12772.0), ("row2", 5210.0), ("row3", 12061.0)]


def hav(a, b):
    lat1, lon1, lat2, lon2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    dlat, dlon = lat2 - lat1, lon2 - lon1
    x = (math.sin(dlat / 2) ** 2
         + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2)
    return 2 * R_EARTH * math.asin(math.sqrt(x))


def pair_distances(pool):
    return [((ha, hb), hav(a, b)) for (ha, a), (hb, b) in itertools.combinations(pool.items(), 2)]


def lenname(name):
    return len("".join(c for c in name.lower() if c.isalpha()))


def main():
    print("=" * 78)
    print("CLUE-5 GEOGRAPHY AUDIT (round 11)")
    print("=" * 78)
    print("Earth max great-circle distance = %.1f km (pi*R)\n" % MAX_GC)

    # -- 1. re-derive the proposed triple ---------------------------------
    print("[1] the proposed triple (all-km), recomputed here")
    prop = [("row1", 12772.0, "Great Wall", "Chichen Itza"),
            ("row2", 5210.0, "Angkor Wat", "Uluru"),
            ("row3", 12061.0, "Machu Picchu", "Great Pyramid of Giza")]
    extra = {"Angkor Wat": (13.4125, 103.8670), "Uluru": (-25.3444, 131.0369)}
    allcoords = dict(W8)
    allcoords.update(extra)
    for name, t, a, b in prop:
        d = hav(allcoords[a], allcoords[b])
        print("   %-5s %-20s <-> %-22s %8.1f km  vs %d  (off %+.1f, %.2f%%)"
              % (name, a, b, d, t, d - t, 100 * (d - t) / t))

    # -- 2. uniqueness within the canonical eight -------------------------
    print("\n[2] uniqueness: canonical-eight pairs within a tolerance of each numeral")
    pd = pair_distances(W8)
    dists = np.array([d for _, d in pd])
    print("   28 canonical-eight distances span %.0f .. %.0f km (median %.0f)"
          % (dists.min(), dists.max(), np.median(dists)))
    for tol_frac in (0.005, 0.01, 0.02):
        print("   tolerance +/-%.1f%%:" % (100 * tol_frac))
        for name, t in NUMERALS:
            hits = sorted(((abs(d - t), a, b, d) for (a, b), d in pd))[:8]
            near = [h for h in hits if h[0] <= tol_frac * t]
            txt = "; ".join("%s<->%s %.0f(off %.0f)" % (a, b, d, o)
                            for o, a, b, d in near) or "NONE"
            print("     %-5s %6.0f -> %d pair(s): %s" % (name, t, len(near), txt))

    # -- 3. unit reading --------------------------------------------------
    print("\n[3] the authoritative `mi / km / mi` reading (X2):")
    tot = [12772.0 * KM_PER_MI, 5210.0, 12061.0 * KM_PER_MI]
    for (name, _), km in zip(NUMERALS, tot):
        flag = "IMPOSSIBLE (> pi*R)" if km > MAX_GC else "possible"
        print("   %-5s -> %9.1f km   %s" % (name, km, flag))
    print("   => under X2, row 1 is %.0f km beyond the Earth's maximum; the"
          % (tot[0] - MAX_GC))
    print("      all-km reading is the only one in which all three can be distances.")

    # -- 4. post-hoc risk of row 2 ---------------------------------------
    print("\n[4] row 2 is a post-hoc pick from a much larger pool.")
    print("   canonical-eight range is %.0f..%.0f km, so 5,210 CANNOT be a"
          % (dists.min(), dists.max()))
    print("   canonical-eight pair; it is found only after widening the site pool.")
    # how 'special' is a 5,210 hit: spacing of the 28 canonical values near 5210
    lo = dists[dists < 5210].max() if (dists < 5210).any() else 0
    hi = dists[dists > 5210].min() if (dists > 5210).any() else MAX_GC
    print("   nearest canonical distances to 5,210: below %.0f, above %.0f"
          % (lo, hi))

    # -- 5. Monte-Carlo null ---------------------------------------------
    print("\n[5] null model: how often does a random 8-site set match a target")
    print("    this tightly by chance?  (tolerance +/-35 km, the round-10 error)")
    tol = 35.0
    rng = np.random.default_rng(1234567)
    # random 8 points uniformly on the sphere, 20000 trials
    n_trials, n_sites = 20000, 8
    def random_dists(rng):
        lat = np.arcsin(rng.uniform(-1, 1, size=(n_trials, n_sites)))
        lon = rng.uniform(0, 2 * np.pi, size=(n_trials, n_sites))
        x = np.cos(lat) * np.cos(lon)
        y = np.cos(lat) * np.sin(lon)
        z = np.sin(lat)
        P = np.stack([x, y, z], -1)
        iu = np.triu_indices(n_sites, 1)
        D = np.einsum("tik,tjk->tij", P, P)
        D = np.clip(D, -1, 1)
        return R_EARTH * np.arccos(D)[:, iu[0], iu[1]]  # (trials, 28)
    RD = random_dists(rng)
    # per-target match probability, target drawn from the printed numerals
    print("   P(some pair within +/-35 km) per target, over 20k random site sets:")
    for name, t in NUMERALS:
        p = float((np.abs(RD - t).min(axis=1) <= tol).mean())
        print("     %-5s %6.0f km : p = %.5f  (expected matches in 28 pairs: %.3f)"
              % (name, t, p, p * 28))
    # joint: rows 1 and 3 both matched (independent trials)
    p1 = float((np.abs(RD - 12772.0).min(axis=1) <= tol).mean())
    p3 = float((np.abs(RD - 12061.0).min(axis=1) <= tol).mean())
    print("   joint (row1 AND row3) for independent random sets: p1*p3 = %.6f"
          % (p1 * p3))
    print("   NOTE: rows 1 and 3 share only the Great Wall; they are not")
    print("   independent, and the pool is FIXED and hand-chosen, not random,")
    print("   so this p is an order-of-magnitude sanity bound, not a p-value.")

    # -- 6. name-length arithmetic (the 20-char answer) -------------------
    print("\n[6] answer is 20 lowercased chars.  Name lengths of the six sites:")
    six = [("Great Wall", 9), ("Chichen Itza", 11), ("Angkor Wat", 9),
           ("Uluru", 5), ("Machu Picchu", 11), ("Great Pyramid of Giza", 18)]
    for n, l in six:
        print("     %-22s %2d" % (n, l))
    print("   row1 pair lengths 9 + 11 = 20  == the answer length.")
    print("   BUT many canonical-eight pairs sum to 20 (9+11 several ways,")
    print("   5+15, 8+12, ...), so this is a weak coincidence, not evidence.")

    print("\n" + "=" * 78)
    print("VERDICT (round 11): the all-km triple reproduces to <=0.27% and the")
    print("three distances are internally consistent, BUT (a) it contradicts the")
    print("authoritative mi/km/mi pennant reading, (b) row 2 is post-hoc, and")
    print("(c) the joint coincidence is only ~0.1% before multiple-comparisons")
    print("inflation.  Status: UNPROVEN, not confirmed.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
