# TinyTitan 4K

A deterministic Python chess engine for the [make.fun Tiny Chess bounty](https://make.fun/bounty/tiny-chess-01).

## Engine

The 3,478-byte `main.py` contains an LZMA-packed Python engine using a 10x12 mailbox board, alpha-beta negamax with iterative deepening, capture quiescence and check evasions, transposition table, null-move pruning, killer/history ordering, late-move reductions, and positional/pawn/endgame evaluation. It searches to a deterministic node budget and does not consult a clock when choosing moves.

## Run

Python 3.13 standard library only. The official starter kit supplies the match environment through `MAKEFUN_ENV_URL`:

```sh
python main.py
```

The program communicates with the kit's `/game` and `/move` endpoints.

## Status

Local checks covered initial moves, castling, en passant, promotion, check evasion, compilation and a mock make.fun API game. **Official make.fun Elo has not been measured.** Validate with the official kit before submitting. Genuine coding-agent transcripts are required for prize eligibility. No competition result is claimed.

Author: Sithu Nyein (@thesithunyein). MIT licensed.
