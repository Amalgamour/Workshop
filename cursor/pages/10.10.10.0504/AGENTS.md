# 10.10.10.0504 page-shape

Read this file before touching the pack. The root `AGENTS.md` still governs the workshop. This file governs how this page runs its packs.

## Page

Jobs page for subject `page-shape`. Design is `10.10.10.0404`. Build is `10.10.10.0304`. The pack is `10.10.10.0504.05.01`, tail `draft`.

MVP: a page with faces needs face 00 and a content face in 01-06 or 08. Face 07 does not count.

## How a pack is run

1. Read the pack. Do the work card. Stop at `stop if`.
2. Stay inside the grant: `core/src/check.rs`, `core/src/bin/seqbook.rs`, `core/tests/next_pages.rs`, and appends to `cursor/temp.book`. Do not edit `director/`, the root `AGENTS.md`, `seqAddr.md`, or `decisions.md`.
3. Do not rewrite a face that already exists. Do not move the pack's tail. Do not write the return into the book. Report the return in your final message.
4. Evidence is a command you ran and the output you saw.
5. The work card has no `ask` line. That is a lint finding. Use the ask below.

## Ask

From `core/`, with `CARGO_TARGET_DIR` set to a directory of your own. Put the GNU gcc and cargo on `PATH` (`%LOCALAPPDATA%\winlibs\mingw64\bin` and `%USERPROFILE%\.cargo\bin`).

- w01: `cargo +stable-x86_64-pc-windows-gnu test --test next_pages -- page_shape_rejects_a_stamp_with_only_face_07 timer_fixture_passes_both_checks`

`stop if`: the work needs the compute, or a change to which faces count.

## Return

`result: done`, `blocked`, or `need`, then the command and what it printed. Then `notes`, `unprompted`, and `overflow`, each with a why.
