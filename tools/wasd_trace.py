"""Trace clue 3's pointer chains and harvest readings from the 8 roots."""
import sys
sys.path.insert(0, "tools")
from wasd_grid import GRID, N, cell, rc, succ, build, STEP

out, ind = build()

# the long chain (all cells reachable from a root, largest component)
best = []
seen = set()
for i in range(100):
    if i in seen or i in ind:
        continue
    chain = []
    j = i
    while j is not None and j not in seen:
        seen.add(j)
        chain.append(j)
        j = out[j]
    if len(chain) > len(best):
        best = chain

print("long chain length:", len(best))
print()
vals = [cell(i)[0] for i in best]
print("values along the chain, first 40:", vals[:40])
print("values along the chain, all      :", "".join(str(v) for v in vals))
print()

roots = [i for i in range(100) if i not in ind]
print("8 roots, and the first 8 numbers reached from each:")
rows = []
for r in roots:
    rr, cc = rc(r)
    seq = []
    j = r
    for _ in range(8):
        if j is None:
            break
        seq.append(cell(j)[0])
        j = out[j]
    rows.append((r, rr + 1, cc + 1, cell(r)[1], seq))
    print("  r%2dc%-2d dir=%-2s -> %s" % (rr + 1, cc + 1, cell(r)[1],
                                         "".join(map(str, seq))))

print()
print("as columns (one digit per root):", "".join(str(s[0]) for _, _, _, _, s in rows))
print("as 8-digit blocks per root      :",
      " ".join("".join(map(str, s)) for _, _, _, _, s in rows))

# star order 1..4 and what each star's chain gives
print()
stars = sorted([i for i in range(100) if cell(i)[1] == "*"], key=lambda i: cell(i)[0])
print("stars in numeric order:", [(cell(i)[0], "r%dc%d" % (rc(i)[0] + 1, rc(i)[1] + 1)) for i in stars])
print()
print("successor of each star:", [(cell(i)[0], out[i], "r%dc%d" % (rc(out[i])[0] + 1, rc(out[i])[1] + 1)) for i in stars if out[i] is not None])
