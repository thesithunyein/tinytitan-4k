# TinyTitan 4K

A deterministic Python chess engine for the [make.fun Tiny Chess bounty](https://make.fun/bounty/tiny-chess-01).

## Engine

The single-file `main.py` uses a 10x12 mailbox representation, legal-king filtering, alpha-beta negamax, capture quiescence, material and positional evaluation, move ordering, and a fixed 9,000-node search budget per iteration. It supports castling, en passant, and promotions. The game server supplies the root legal moves.

## Run

Python 3.13, standard library only. The official make.fun starter kit provides `MAKEFUN_ENV_URL` and the match environment.

```sh
python main.py
```

## Checks

`main.py` must be no more than 4,096 bytes. Validate with the official starter kit before submission. No official Elo score is claimed. This code is an initial tested implementation, not a verified winning engine.

## Author

Sithu Nyein (@thesithunyein). MIT licensed.
