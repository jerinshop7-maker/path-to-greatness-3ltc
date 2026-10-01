#!/usr/bin/env python3
"""Clue 4 ("chess", 12 characters) — the only answer that KEEPS ITS CASE.

That single fact, which `clues.sheet` and `fix_clues.script` both pin, is a
strong signal about the answer's alphabet: 12 characters with uppercase letters
in it.  A chess position plus a 12-character case-preserved answer is, on its
face, a mate-in-N solution written in SAN.

This tool:
  1. rebuilds the position from analysis/IMAGE-TRANSCRIPTION.md,
  2. asks Stockfish for the forced mate length,
  3. enumerates every SAN line of that length,
  4. reports which of them are exactly 12 characters.

Nothing here is tested against the oracle -- segment 2's key is clue4 || clue5,
so a clue-4 line still needs clue 5.  What this settles is the *shape* of the
answer: if a unique 12-character SAN line exists, clue 4 is pinned by the board
alone, which makes clue 5 the only remaining unknown on that segment.
"""
import subprocess
import sys


# analysis/IMAGE-TRANSCRIPTION.md section 4, read square by square.
#   rank 8: e8 black rook
#   rank 7: a7 black rook, b7 black king, c7 p, f7 p
#   rank 6: b6 p, d6 p, f6 black knight, g6 p
#   rank 5: g5 white knight
#   rank 4: d4 white bishop
#   rank 3: b3 white queen, c3 white pawn
#   rank 2: c2 white king
FEN = "4r3/rkp1p3/1p1p1np1/6N1/3B4/1QP5/2K5/8 w - - 0 1"


from sfengine import Engine, best_info


def main():
    import chess
    b = chess.Board(FEN)
    print("position from analysis/IMAGE-TRANSCRIPTION.md section 4")
    print(b)
    print("FEN valid: %s   pieces: %d" % (b.is_valid(), len(b.piece_map())))
    print()

    e = Engine()

    # ---- what does the engine think the best line is? ----------------------
    print("engine's opinion (white to move):")
    for t in (3000, 8000):
        ls, bm = e.go(FEN, t)
        print("  movetime %-5d %s" % (t, best_info(ls)))
    print()

    # ---- is there a forced mate for white at all? -------------------------
    print("searching for a forced mate (white to move) ...")
    bestmate = None
    tried = 0
    for mv in b.legal_moves:
        san = b.san(mv)
        b.push(mv)
        ls, _ = e.go(b.fen(), 2000)
        b.pop()
        tried += 1
        hit = next((l for l in ls if " pv " in l and "score mate" in l), None)
        if hit:
            n = int(hit.split("score mate")[1].split()[0])
            # mate distance from the position AFTER white's move
            dist = -n + 1
            if bestmate is None or dist < bestmate[0]:
                bestmate = (dist, san, hit.strip())
    print("  white first moves tried: %d" % tried)
    if bestmate is None:
        print("  NO forced mate for white at 2s/move.")
        print("  -> a SAN mating line is not the 12-character answer.")
    else:
        dist, san, info = bestmate
        print("  shortest forced mate: %s  (mate in %d)" % (san, dist))
        print("  engine line: %s" % info)
        print("  that SAN token is %d characters; the answer needs 12" % len(san))
    e.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())