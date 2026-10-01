"""Clue 3: exploit that the four NON-STAR roots carry exactly the four WASD
directions.

Verified facts from tools/wasd_grid.py:
  * 100 cells, 4 numbered stars (isolated: no in-edge, no out-edge)
  * exactly 8 cells have no predecessor: the 4 stars + 4 arrow cells
  * those 4 arrow cells have directions D, W, A, S -- i.e. one of each WASD key

Since the clue is literally named "wasd" and the answer is 8 characters, test the
reading in which each non-star root starts a walk and the WASD key supplies a
letter, with the stars supplying the rest.
"""
import sys
sys.path.insert(0, "tools")
from wasd_grid import cell, rc, succ, build

KEY = {"W": "w", "A": "a", "S": "s", "D": "d"}

out, ind = build()
indeg = {i: 0 for i in range(100)}
for i in range(100):
    if out[i] is not None:
        indeg[out[i]] += 1

roots = [i for i in range(100) if indeg[i] == 0]
stars = sorted([i for i in roots if cell(i)[1] == "*"], key=lambda i: cell(i)[0])
walks = sorted([i for i in roots if cell(i)[1] != "*"], key=lambda i: KEY[cell(i)[1]])

print("roots (%d):" % len(roots))
for i in roots:
    r, c = rc(i)
    print("  r%-2dc%-2d value=%d dir=%s%s" % (r + 1, c + 1, cell(i)[0],
                                             cell(i)[1], "  <- star" if cell(i)[1] == "*" else ""))
print()
print("non-star roots in WASD key order:")
for i in walks:
    r, c = rc(i)
    print("  %s : r%-2dc%-2d value=%d" % (KEY[cell(i)[1]], r + 1, c + 1, cell(i)[0]))
print()


def walk_from(start, limit=8):
    seq, j = [], start
    while j is not None and len(seq) < limit:
        seq.append(cell(j)[0])
        j = out[j]
    return seq


print("walk from each non-star root (first 12 numbers):")
digits = []
for i in walks:
    s = walk_from(i, 12)
    print("  %s : %s" % (KEY[cell(i)[1]], " ".join(map(str, s))))
    digits.append(s)
print()

# star order gives the sequence; pair star n with the n-th WASD walk
print("star-number order of the four stars:")
for n, i in enumerate(stars, 1):
    r, c = rc(i)
    print("  star %d at r%dc%d" % (n, r + 1, c + 1))
print()

print("cross-products (one digit per root, various orderings):")
print("  wasd order, first digit of each walk :", "".join(str(s[0]) for s in digits))
print("  wasd order, last digit of each walk  :", "".join(str(s[-1]) for s in digits))

# full chains from each root, in WASD order, take the first N of each
for n in (1, 2, 3):
    cols = ["".join(str(s[k]) for s in digits) for k in range(n)]
    print("  first %d of each walk, joined by row: %s" % (n, " | ".join(cols)))
