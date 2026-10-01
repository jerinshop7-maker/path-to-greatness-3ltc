#!/usr/bin/env python3
"""Clue 5, round 8: sanity-check the "song-pair geography" revival.

The pasted round-8 analysis revives the landmark-distance reading, now with the
*songs'* origins as endpoints, and cites New York <-> Perth ~= 5,219 km against
the printed 5,210 km.  This tool does the arithmetic honestly:

  (1) the printed values as distances, under the repo's units mi/km/mi;
  (2) the Earth's maximum great-circle distance, so the impossible ones are
      labelled impossible rather than "close";
  (3) every pairwise great-circle distance between the six bands' origin
      cities, in km and miles, checked against the three printed values.

It prints the matches (if any) and the closest near-misses, so the route is
either opened or closed with a number instead of an impression.
"""
import itertools
import math

# the three printed values (Roman numerals) and the repo's unit reading (X2)
PRINTED = [("row1", 12772, "mi"), ("row2", 5210, "km"), ("row3", 12061, "mi")]
KM_PER_MI = 1.609344

# origin cities of the six confirmed clue-5 artists (approx. city centres)
BANDS = {
    "Vintersorg": ("Skelleftea, SE", 64.7507, 20.9500),
    "Falkenbach": ("Germany (project origin)", 51.1657, 10.4515),
    "Nightwish": ("Kitee, FI", 62.1000, 30.1400),
    "Pink Floyd": ("London, UK", 51.5074, -0.1278),
    "Coheed and Cambria": ("Nyack, NY, US", 41.0907, -73.9179),
    "Alestorm": ("Perth, UK", 56.3950, -3.4308),
}


def hav_km(lat1, lon1, lat2, lon2):
    r = 6371.0088
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def main():
    print("(1) the printed values under the mi / km / mi reading:")
    targets_km = {}
    for name, v, unit in PRINTED:
        km = v * KM_PER_MI if unit == "mi" else v
        targets_km[name] = km
        print("    %-5s %6d %-2s = %9.1f km" % (name, v, unit, km))

    rmax = math.pi * 6371.0088
    print("\n(2) Earth's maximum great-circle distance = %.1f km (%.0f mi)"
          % (rmax, rmax / KM_PER_MI))
    for name, v, unit in PRINTED:
        km = targets_km[name]
        print("    %-5s %9.1f km  -> %s" %
              (name, km, "IMPOSSIBLE as a surface distance" if km > rmax else "possible"))

    print("\nthe same three values read as ALL km (the pre-X2 reading):")
    for name, v, unit in PRINTED:
        print("    %-5s %9.1f km  -> %s" %
              (name, v, "IMPOSSIBLE" if v > rmax else "possible"))

    print("\n(3) pairwise band-origin distances vs the printed values:")
    nearest = []
    for (a, (ca, la, loa)), (b, (cb, lb, lob)) in itertools.combinations(BANDS.items(), 2):
        d_km = hav_km(la, loa, lb, lob)
        d_mi = d_km / KM_PER_MI
        best = min((abs(d_km - k), n, "km") for n, k in targets_km.items())
        best_mi = min((abs(d_mi - v) for name, v, unit in PRINTED if unit == "mi"), default=9e9)
        nearest.append((best[0], "%s <-> %s: %.0f km / %.0f mi" % (ca, cb, d_km, d_mi), best[1]))
    nearest.sort()
    for _, line, tgt in nearest[:12]:
        print("    %-52s (closest target: %s)" % (line, tgt))

    print("\nNYC <-> Perth, UK (the quoted hit): %.0f km  [printed row2 = 5210 km]"
          % hav_km(40.7128, -74.0060, *BANDS["Alestorm"][1:]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
