# Draft: 90.50.10.0424 book-board

Pack text for pass 05.01. Title: book-board. Builder: Grok-3 (Matthew's PC, D:\Git\grok3).

## Scope

Matthew's G5 answer (t541u): "wf board with holder, step and next". Each line of the book-level board (`wf board` with no page) shows the page's holder, current step, and next step. The data already exists on the page board at `src/board.rs:272` (claim, tail, `pass_next`). `book()` already prints one line per page; this pass adds the three fields there.

Grant: `src/board.rs`, `tests/page_0424.rs` only. No `src/lib.rs`. `wf board` already dispatches to `book()`, so help text and dispatch do not need to change. If that stopped being true, the pack says to stop and raise it.

## Current pass, holder, step, next

The current pass is the highest-numbered pass whose tail is not `closed`, the same rule as `status.rs:17`. Holder is that pass's claim, or `none` when the claim is empty or there is no such pass. Step is that pass's tail, or `none`. Next is `pass_next` for that pass, or the no-open-pass / halt sentences already used by status, copied into `board.rs`. `status.rs` is not granted.

## Q1

WF-BOARD Q1 (column names) is still open for Matthew. Prima's default, already in `src/board.rs:23-31`, is used and must not change: tool words are the columns, body-shop words are side labels only.

## Line shape

Keep the existing prefix so `tests/wf.rs` still passes:

`  {addr}  {title}  entries {n}, last {when} | holder {h} | step {s} | next: {next} | draft ...`

Unreadable lines stay as they are.

## Files

- FINAL-0424-face01.txt
- FINAL-0424-face04-goals.txt
- FINAL-0424-face06-note.txt
- FINAL-0424-face08.txt
- FINAL-PACK-0424-05.01.txt
