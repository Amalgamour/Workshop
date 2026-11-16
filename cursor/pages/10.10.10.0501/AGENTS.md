# 10.10.10.0501 first-build

Read this file before touching the pack. The root `AGENTS.md` still governs the workshop. This file governs how this page runs its packs.

## Page

Jobs page for subject `first-build`. Design is `10.10.10.0401`. Build is `10.10.10.0301`. The pack is `10.10.10.0501.05.01`, tail `draft`.

## How a pack is run

1. Read the pack. Do the work cards in order. Stop at `stop if`.
2. Stay inside the grant: `core/`, and appends to `cursor/temp.book`. Do not edit `director/`, the root `AGENTS.md`, `seqAddr.md`, or `decisions.md`.
3. Do not rewrite a face that already exists. Do not move the pack's tail. Do not write the return into the book. Report the return in your final message. The parent records it.
4. Evidence is a command you ran and the output you saw. A summary is not evidence.
5. The work cards have no `ask` line. That is a lint finding. Use the ask below. Do not invent a second pack to hide it.

## Asks

From `core/`, with `CARGO_TARGET_DIR` set to a directory of your own:

- w01: `cargo +stable-x86_64-pc-windows-gnu test --test first_build -- full_address_parses_and_short_form_expands bad_width_is_rejected_not_padded leading_dot_needs_exactly_one_active_page`
- w02: `cargo +stable-x86_64-pc-windows-gnu test --test first_build put_creates_tail_moves_from_current_and_torn_line_drops`
- w03: Read `core/src/lib.rs` and `core/src/book.rs`. Confirm append is only `Writer::create`, `Writer::open`, `Writer::put`, and `Writer::tail`.
- w04 and w05: Open `core/fixtures/10.11.21.book` and find `title: timer` and the `why:` on card `purpose`.

`stop if`: the fix needs the compute, the app, a language change, or an edit to `seqAddr.md` or `decisions.md`.

## Return

For each card, `result: done`, `blocked`, or `need`, then the command and what it printed. Then `notes`, `unprompted`, and `overflow`, each with a why. Empty is allowed only with a why.
