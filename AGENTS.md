# AGENTS.md

Guidance for AI coding/reasoning agents working in this repository
(*Path to Greatness* — 3 LTC cryptanalysis).

## What this repo is

An independent cryptanalysis of Justin Patterson's (`jpatt94`) Litecoin treasure
hunt. There is **no application** to build — the work is reasoning + one small
Python/C toolchain. Findings live in `analysis/`; hypothesis generators and the
oracle live in `tools/`. `analysis/IMAGE-TRANSCRIPTION.md` is the authoritative
reading of the clue images and **wins over any other file** where they disagree.

Conventions that matter:

- Every claim is marked CONFIRMED / UNCONFIRMED / REFUTED with its evidence.
  Do not upgrade a hypothesis to a fact without a run that shows the output.
- Negatives are results. Record the family, its size, and the tool that produced
  it, so the next agent does not re-sweep it.
- Prefer editing existing files; keep new tools self-describing (they print
  their own scope and result).

## Setup and checks

```bash
pip install pycryptodome ecdsa      # oracle deps (falls back to pure Python)
python3 tools/oracle.py --selftest                 # must print: SELFTEST OK
python3 tools/clue5_music.py                        # round-7 music-layer test
python3 tools/clue2_permutation.py                  # clue-2 permutation families
gcc -O3 -march=native -o tools/sweep tools/sweep.c  # only if you need the engine
```

Run `tools/oracle.py --selftest` before trusting any match/no-match verdict, and
always report the tested space size alongside a zero-hit result.

## Pushing (important — a plain `git push` fails here)

This environment has **two** GitHub credentials for the account
`jerinshop7-maker`, and the one git picks first cannot push:

| # | Where | Token | Scopes | Works? |
|---|---|---|---|---|
| 1 (active) | `GH_TOKEN` env var | `ghu_…` | limited | **no — 403** |
| 2 (fallback) | `gh`'s `~/.config/gh/hosts.yml` | `gho_…` | `gist, read:org, repo` | yes |

A bare `git push origin main` uses #1 and returns
`403 Permission ... denied`. Push with #1 unset so the `gh` credential helper
falls through to #2:

```bash
env -u GH_TOKEN GITHUB_TOKEN= git -c credential.helper='!gh auth git-credential' push origin main
```

Check which credential is in play with `gh auth status` (look for the token with
`repo` scope), and confirm the remote with `git remote -v` (must be
`https://github.com/jerinshop7-maker/path-to-greatness-3ltc.git`).

Rules:

- Never rewrite history or force-push; history here is append-only.
- Do not run `git config` to change identity or credential settings globally.
- Commit only files relevant to the change; commit messages are imperative and
  explain the *why* (see `git log` for the house style).
