#!/usr/bin/env python3
"""Stockfish driver.

Stockfish's UCI banner and NNUE load chatter must be consumed to the `uciok`
token, and the search must be driven by reading lines until `bestmove` rather
than by writing `quit` immediately after `go` -- sending `quit` straight after a
`go` makes the engine exit before it prints more than the first `info depth 1`
line, which silently turns a depth-22 search into a depth-1 one.
"""
import subprocess
import time

EXE = "/usr/games/stockfish"


class Engine:
    def __init__(self, exe=EXE):
        self.p = subprocess.Popen([exe], stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, text=True, bufsize=1)
        self._write("uci")
        while True:
            l = self._read()
            if l is None:
                raise RuntimeError("engine closed during uci")
            if l.startswith("uciok"):
                break
        self._write("isready")
        while True:
            l = self._read()
            if l is None:
                raise RuntimeError("engine closed during isready")
            if l.startswith("readyok"):
                break

    def _write(self, c):
        self.p.stdin.write(c + "\n")
        self.p.stdin.flush()

    def _read(self):
        l = self.p.stdout.readline()
        return None if not l else l.rstrip()

    def go(self, fen, movetime=4000):
        """Returns (search_lines, bestmove_line)."""
        self._write("position fen " + fen)
        self._write("go movetime %d" % movetime)
        lines, best = [], None
        while True:
            l = self._read()
            if l is None:
                break
            if l.startswith("info depth"):
                lines.append(l)
            elif l.startswith("bestmove"):
                best = l
                break
        return lines, best

    def close(self):
        try:
            self._write("quit")
        except Exception:
            pass
        self.p.kill()


def best_info(lines):
    """Deepest real search line.  Filters out `info string` noise, which carries
    neither a score nor a pv."""
    real = [l for l in lines if " pv " in l]
    return real[-1] if real else ""