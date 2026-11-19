# TinyTitan 4K

Deterministic Python chess engine for the [make.fun Tiny Chess bounty](https://make.fun/bounty/tiny-chess-01), by [@thesithunyein](https://github.com/thesithunyein).

## Implementation

`main.py` is a 3,663-byte LZMA-packed Python entry. Its readable source (`engine.py`) includes a 10x12 mailbox board, iterative-deepening negamax/alpha-beta, check evasions, quiescence, a transposition cache, null-move pruning, late-move reductions, killer/history move ordering, basic pawn structure and rook open-file evaluation. The node budget is deterministic (22,000 nodes per search iteration). Uses Python 3.13 standard library only and the official game's `MAKEFUN_ENV_URL`.

## Run and validate

Download the official starter kit from https://make.fun/c/tiny-chess-01/kit, read `RULES.txt`, and run its local validation and practice opponents. The file launches using `python main.py` when `MAKEFUN_ENV_URL` points to the official game server.

## Tests and limitations

Local compilation and gameplay checks passed for starting moves, castling, en passant, promotions, check evasions and mock protocol. Initial-position depth-three perft matched 8,902. Additional local runtime checks were below ten seconds. The head-to-head comparison was **incomplete**; no official gauntlet result or Elo has been obtained. This is **not** a verified 9+/10 engine or guaranteed winner.

Submission also requires genuine coding-agent build transcripts and the full Git commit SHA. No transcripts are included or claimed from this repository. License: MIT.
