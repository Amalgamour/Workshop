# 10.10.10.0503 why-check

Read this file before touching the pack. The root `AGENTS.md` still governs the workshop. This file governs how this page runs its packs.

## Page

Jobs page for subject `why-check`. Design is `10.10.10.0403`. Build is `10.10.10.0303`. The pack is `10.10.10.0503.05.01`, tail `draft`.

MVP: a 01 or 02 card with no 04 twin, no why line, or no body is a hard gap. A copied 04 body is a finding.

## How a pack is run

1. Read the pack. Do the work card. Stop at `stop if`.
2. Stay inside the grant: `core/src/check.rs`, `core/src/bin/seqbook.rs`, `core/tests/next_pages.rs`, and appends to `cursor/temp.book`. Do not edit `director/`, the root `AGENTS.md`, `seqAddr.md`, or `decisions.md`.
3. Do not rewrite a face that already exists. Do not move the pack's tail. Do not write the return into the book. Report the return in your final message.
4. Evidence is a command you ran and the output you saw.
5. The work card has no `ask` line. That is a lint finding. Use the ask below.

## Ask

From `core/`, with `CARGO_TARGET_DIR` set to a directory of your own. Put the GNU gcc and cargo on `PATH` (`%LOCALAPPDATA%\winlibs\mingw64\bin` and `%USERPROFILE%\.cargo\bin`).

- w01: `cargo +stable-x86_64-pc-windows-gnu test --test next_pages -- missing_why_is_a_hard_gap copied_why_is_a_finding timer_fixture_passes_both_checks`

`stop if`: the work needs the compute, keyword branding, or an edit to `decisions.md`.

## Return

`result: done`, `blocked`, or `need`, then the command and what it printed. Then `notes`, `unprompted`, and `overflow`, each with a why.
