"""Clue 3 (`wasd`) grid, transcribed by eye from clues/clue3_wasd.jpg.

Transcription method: the served JPEG was cropped to the grid and upscaled 3x
with LANCZOS, then read twice (whole-image pass and crop pass). Both passes
agree cell for cell, so the table below is a faithful transcription.

WASD key mapping, from the clue's own title "wasd":
    up arrow = W, left arrow = A, down arrow = S, right arrow = D
"""

# (number, direction) per cell, row-major, 10x10. '*' = numbered star.
GRID = [
    [(7, "S"), (5, "D"), (2, "D"), (8, "S"), (3, "S"), (1, "D"), (5, "S"), (7, "A"), (4, "S"), (1, "A")],
    [(2, "D"), (4, "D"), (1, "W"), (3, "*"), (5, "D"), (5, "S"), (6, "S"), (6, "S"), (2, "A"), (1, "S")],
    [(3, "S"), (6, "D"), (3, "D"), (1, "D"), (4, "S"), (7, "S"), (6, "S"), (1, "W"), (8, "A"), (3, "A")],
    [(3, "D"), (5, "D"), (5, "D"), (3, "W"), (5, "D"), (2, "S"), (1, "A"), (3, "S"), (2, "W"), (1, "S")],
    [(1, "W"), (6, "D"), (3, "D"), (3, "S"), (1, "A"), (4, "W"), (1, "*"), (4, "W"), (2, "S"), (9, "A")],
    [(2, "D"), (3, "W"), (3, "W"), (3, "W"), (4, "W"), (3, "S"), (2, "D"), (4, "S"), (4, "W"), (6, "A")],
    [(5, "W"), (5, "W"), (4, "D"), (3, "S"), (3, "A"), (5, "A"), (3, "A"), (2, "D"), (6, "A"), (6, "W")],
    [(2, "D"), (4, "W"), (3, "W"), (5, "D"), (2, "W"), (4, "A"), (2, "S"), (2, "A"), (5, "W"), (4, "A")],
    [(1, "S"), (4, "W"), (2, "*"), (4, "D"), (4, "W"), (4, "D"), (2, "A"), (3, "W"), (4, "*"), (8, "A")],
    [(9, "D"), (4, "W"), (6, "W"), (2, "A"), (2, "W"), (3, "A"), (6, "A"), (1, "D"), (4, "A"), (4, "W")],
]

N = 10
STEP = {"W": (-1, 0), "A": (0, -1), "S": (1, 0), "D": (0, 1)}
KEYNAME = {"W": "W", "A": "A", "S": "S", "D": "D"}


def cell(i):
    """The (number, direction) pair at flat index i."""
    r, c = divmod(i, N)
    return GRID[r][c]


def rc(i):
    return divmod(i, N)


def idx(r, c):
    return r * N + c


def succ(i):
    """Cell that cell i points at, or None if it leaves the grid / is a star."""
    n, d = cell(i)
    r, c = rc(i)
    if d == "*":
        return None
    dr, dc = STEP[d]
    r, c = r + dr * n, c + dc * n
    if not (0 <= r < N and 0 <= c < N):
        return None
    return idx(r, c)


def build():
    out = {}
    ind = {}
    for i in range(N * N):
        s = succ(i)
        out[i] = s
        if s is not None:
            ind.setdefault(s, []).append(i)
    return out, ind


def cycles(out, ind):
    """Walk successor chains from every cell lacking a predecessor."""
    seen = set()
    comps = []
    for i in range(N * N):
        if i in seen or i in ind:
            continue
        chain = []
        j = i
        while j is not None and j not in seen:
            seen.add(j)
            chain.append(j)
            j = out[j]
        comps.append(chain)
    # anything left over sits in a cycle with no entry point
    for i in range(N * N):
        if i in seen:
            continue
        chain = []
        j = i
        while j not in seen:
            seen.add(j)
            chain.append(j)
            j = out[j]
        comps.append(chain)
    return comps


def main():
    out, ind = build()
    comps = cycles(out, ind)
    comps.sort(key=len, reverse=True)

    print("cells:            %d" % (N * N))
    print("off-grid/star successors (no successor): %d"
          % sum(1 for i in range(100) if out[i] is None))
    print("components:       %d" % len(comps))
    print("component sizes:  %s" % sorted((len(c) for c in comps), reverse=True))
    print()
    for c in comps:
        if len(c) < 6:
            desc = ", ".join("r%dc%d=%d%s" % (rc(i)[0] + 1, rc(i)[1] + 1,
                                              cell(i)[0], cell(i)[1])
                             for i in c)
            print("small chain (len %d): %s" % (len(c), desc))
    print()

    nopred = [i for i in range(100) if i not in ind]
    print("cells with NO predecessor: %d" % len(nopred))
    for i in nopred:
        r, c = rc(i)
        print("  r%dc%d  value=%-2d dir=%-2s" % (r + 1, c + 1, cell(i)[0], cell(i)[1]))
    print()

    dup = {k: v for k, v in ind.items() if len(v) > 1}
    print("cells with >1 predecessor: %d" % len(dup))
    for k, v in sorted(dup.items()):
        r, c = rc(k)
        print("  r%dc%d <- %s" % (r + 1, c + 1,
                                  ", ".join("r%dc%d" % (rc(j)[0] + 1, rc(j)[1] + 1)
                                            for j in v)))


if __name__ == "__main__":
    main()