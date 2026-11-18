# Workshop workflow kit (v0)

## What it is
- A small tool called `wf`.
- It runs one page per piece of work.
- It keeps the record. It checks the rules. People and models just ask it.

## The picture
- The page is a box. The tool sits inside it.
- You and the models stay outside the box.
- Nobody writes on the page by hand. Everyone asks `wf`.
- `wf` writes every change into one file: `pages/<page>/log.jsonl`.
- That log is the truth. The page files are copies printed from it.
- If someone edits a page file by hand, `wf` refuses to go on.

## Who does what
- **You (person)**: start the page. Give the grant (which files the work may touch). Answer big questions.
- **Prime**: the team lead. Plans each pass. Signs off at the end.
- **Builder**: a model that does one pass of work.
- **Checker**: Prime's helper. Tests each finished pass. Never the builder.
- **Observer**: watches Prime. Looks for drift from the goals, loops, and stalls.

Checker and observer are working paths (T7, T8), not rulings yet.

## One pass, step by step
1. Prime reads faces 04 and 06 and the last pass. Writes a note on 06.
2. **draft**: Prime writes the plan. `wf` pins what Prime read.
3. **pack**: `wf` checks the plan, then prints the job for the builder.
4. **open**: a builder claims the job.
5. **return**: the builder pushes the work and pings `wf`. `wf` checks the files.
6. **review**: the checker runs the tests. `wf` writes a short report.
7. **closed**: Prime signs off. `wf` writes the close record.

If a builder is stuck, it goes up to Prime. If Prime is stuck, it goes up to you.

## Set it up (once)
1. Install Rust: https://rustup.rs (one installer, any computer).
2. Get the kit: `git clone -b workflow https://github.com/Amalgamour/Workshop.git workflow`
3. Build the tool once, from that last merged commit: `cd workflow` then `cargo build --release`
4. Copy the binary out, so later builds cannot overwrite the tool you run:
   `mkdir -p ../wf-bin && cp target/release/wf ../wf-bin/wf`
   (on Windows, copy `target\release\wf.exe` to `..\wf-bin\wf.exe`).
5. Run that pinned copy: `../wf-bin/wf` (or add `wf-bin` to your PATH).
6. When you build or test as a builder, set your own `CARGO_TARGET_DIR` so you never
   write into the pinned copy: `CARGO_TARGET_DIR=target-builder cargo test`
   When an old and a new build share a `CARGO_TARGET_DIR`, run `cargo clean -p wf`
   and touch the sources between them, or the new tests may run against the old binary.

## Start a page (one command)
```
wf init-page 10.20.30.1201 --title steering --person matthew --prime prima --grant "src/,tests/" --grant-ref t300u --as matthew
```

## Every command
Add `--as <your name>` to every command that writes.

| Step | Command |
|---|---|
| Start a page | `wf init-page <page> --title T --person P --prime L --grant "a,b" --grant-ref tNNNu` |
| Change Prime | `wf set-prime <page> <name> --ref tNNNu` |
| Widen the grant | `wf grant <page> --paths "a,b" --ref tNNNu [--answers <entry>]` |
| Write a face | `wf face-write <page> 01\|02\|04\|06\|08 --text "..."` (04 needs `--section goals`, `decisions` or `responses`) |
| Draft a pass | `wf draft <page> --file plan.txt [--overlap-ok NN --why "... (ref)"]` |
| Release it | `wf pack <page> <NN> [--overlap-ok NN --why "... (ref)"]` |
| Claim it | `wf claim <page> <NN>` |
| Hand it back | `wf return <page> <NN> --branch B --commit SHA --file PATH` |
| Check it | `wf check <page> <NN> [--note T] [--fail T] [--dry-run]` |
| Sign off | `wf signoff <page> <NN> --outcome passed\|failed\|blocked\|needs-authority [--cards w01=accepted,...] [--note "... (ref)"]` |
| Close it | `wf close <page> <NN>` |
| Send it up | `wf elevate <page> <NN> --to prime\|person --item "..."` |
| Answer | `wf answer <page> <entry> --text "..."` |
| Stop the page | `wf halt <page> --note "why (ref)"` (Prime or person; refused while a pass is open; draft, pack and claim then refuse) |
| Go on again | `wf resume <page> --note "why (ref)"` (Prime or person) |
| See where things stand | `wf status <page>` |
| Observer check | `wf observe <page> [--record "finding"]` |
| Check the log chain and views | `wf verify <page>` (`--fix` reprints missing and changed views from the log) |

`wf status` is the "where are we" view. It is always built fresh from the log.

Pass numbers may be written `1` or `01`. Hashes are sha256; views show a 12-character prefix.

A pass holds its files while its tail is pack, open (claimed), return, or review. `wf pack` refuses a second pass that would touch the same files, unless Prime names the other pass with `--overlap-ok` and gives `--why` with a reason and a (ref). That flag is refused if the named pass is not open.

`wf draft` is refused while another pass on the page is not closed (draft, pack, open, return or review), unless Prime names an already-packed open pass with `--overlap-ok NN` and `--why` with a reason and a (ref). A pass that still sits at draft (not packed) cannot be overlapped. Without the flag the refusal stands. The message names that pass and its next step. A draft that is not packed yet can be redrafted with `--pass NN`.

`wf signoff --outcome passed` is refused while a job is need or blocked and `--cards` does not name it, a question to the person on this pass has no answer, or face 01 changed since the pack. Naming a not-done job, signing off over drift, or changing a default card needs `--note` with a reason and a (ref). Both the reason and the ref must be non-blank. `wf close` re-runs those same refusals when the outcome is passed, and a passed close is refused if face 01 changed after the signoff entry (a note stored for something else does not cover it). `wf set-prime --ref`, `wf grant --ref` and `wf answer --text` refuse blank or spaces.


## A plan file (for `wf draft`)
```
repo: driving-game
start: main
outcome: arrow keys turn the car; max 30 degrees
w01: steer left and right at rate 2
w02: clamp the angle at 30 degrees
may touch: src/steer.rs, tests/steer.rs
checks: cargo test steer
stop if: the turn needs a physics change
```
`repo` is the work repo's folder, next to `pages/`. `checks` are commands, split by `;`.

## The example
- `examples/car-steering.sh` runs the car steering sample through `wf`.
- Its output is in `examples/pages/`. Nothing there was written by hand.
- Page 10.20.30.1201: pass 1 passed, pass 2 blocked then widened, pass 3 in progress.
- Page 10.20.30.1211: the hard paths. A failed check. A refused return. A question sent up to you.

## Files
- `AGENTS.md`: what any model must do.
- `docs/AXIOMS.md`, `docs/DESIGN.md`: the rules and the design, inside the kit folder
  (the folder with `src/` and `AGENTS.md`). From a run folder that only holds `pages/`,
  open them from the kit, not from the run folder.
- `src/`: the tool. `templates/`: the fixed text it prints. `tests/`: the tests.

## Design sources
- [WORKFLOW-TOOLS.md](https://github.com/Amalgamour/Workshop/blob/ef67287ee0cb101e237fdf0e87eb4828596afff3/docs/design/WORKFLOW-TOOLS.md),
  [ONE-PAGE-WORK.md](https://github.com/Amalgamour/Workshop/blob/ef67287ee0cb101e237fdf0e87eb4828596afff3/docs/design/ONE-PAGE-WORK.md),
  [SAMPLE-PAGE.md](https://github.com/Amalgamour/Workshop/blob/ef67287ee0cb101e237fdf0e87eb4828596afff3/docs/design/SAMPLE-PAGE.md),
  [SAMPLE-PAGE-PATHS.md](https://github.com/Amalgamour/Workshop/blob/ef67287ee0cb101e237fdf0e87eb4828596afff3/docs/design/SAMPLE-PAGE-PATHS.md)
  on prima/build at ef67287.
- The checker and observer update (step 7, T7, T8) is build commit 9ac8d58. It is not on GitHub yet.

## Not in v0 (known gaps)
- Names are not proven. `--as` is trusted. Keys come later.
- `wf` does not merge accepted work. Merging waits on question T1.
- No labs (face 07) and no face 09 history view.
- The observer reads signals. Judging drift in meaning is still the observer's job.
- The log chain shows the log is consistent, not that it was never rewritten. Anyone who can write `log.jsonl` can rewrite and rehash it.
- wf v0 page ids are temporary labels, not checked as SeqAddr. A SeqAddr check comes later through seqaddr-core.
