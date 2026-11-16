# 10.10.10.0502 read

Read this file before touching the pack. The root `AGENTS.md` still governs the workshop. This file governs how this page runs its packs.

## Page

Jobs page for subject `read`. Design is `10.10.10.0402`. Build is `10.10.10.0302`. `10.10.10.0502.05.01` is at return. The next pack is `10.10.10.0502.05.02`.

MVP of 05.02: a person opens a local page and reads one face's why. The page calls the compute. It does not read the book file.

## How a pack is run

1. Read the pack. Do the work cards in order. Stop at `stop if`.
2. `05.01` stayed inside the core. `05.02` stays inside `app/` and `compute/`. The page calls the compute. It does not read the book file. Do not edit `director/`, the root `AGENTS.md`, `seqAddr.md`, or `decisions.md`.
3. Do not rewrite a face that already exists. Do not move the pack's tail. Do not write the return into the book. Report the return in your final message.
4. Evidence is a command you ran and the output you saw.
5. The work cards have no `ask` line. That is a lint finding. Use the ask below.

## Asks

From `core/`, with `CARGO_TARGET_DIR` set to a directory of your own. Put the GNU gcc and cargo on `PATH` (`%LOCALAPPDATA%\winlibs\mingw64\bin` and `%USERPROFILE%\.cargo\bin`).

- w01: `cargo +stable-x86_64-pc-windows-gnu test --test next_pages open_appends_to_an_existing_book`
- w02: `cargo +stable-x86_64-pc-windows-gnu run --quiet -- read fixtures\10.11.21.book 10.11.21.1001.04` and the missing-address case `10.11.21.1001.09`.

`05.01` stops if the work needs the compute or the Next.js app. `05.02` is that work. Both stop if they would edit `seqAddr.md` or `decisions.md`.

- 05.02 ask: open the app, ask for `10.11.21.1001.04`, and read the why on the screen. The compute serves `core/fixtures/10.11.21.book` on port 7040. The app is on port 3210.

## Return

For each card, `result: done`, `blocked`, or `need`, then the command and what it printed. Then `notes`, `unprompted`, and `overflow`, each with a why.
