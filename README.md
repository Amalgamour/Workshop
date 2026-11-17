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
3. Build it: `cd workflow` then `cargo build --release`
4. The tool is now at `target/release/wf` (on Windows, `target\release\wf.exe`).
5. Test it: `cargo test`

## Start a page (one command)
```
wf init-page 10.20.30.1201 --title steering --person matthew --prime prima --grant "src/,tests/" --grant-ref t300u --as matthew
```

## Every command
Add `--as <your name>` to every command that writes.

| Step | Command |
|---|---|
| Start a page | `wf init-page <page> --title T --person P --prime L --grant "a,b" --grant-ref tNNNu` |
| Change Prime | `wf set-prime <page> <name>` |
| Widen the grant | `wf grant <page> --paths "a,b" --ref tNNNu [--answers <entry>]` |
| Write a face | `wf face-write <page> 01\|02\|04\|06\|08 --text "..."` (04 needs `--section goals`, `decisions` or `responses`) |
| Draft a pass | `wf draft <page> --file plan.txt` |
| Release it | `wf pack <page> <NN>` |
| Claim it | `wf claim <page> <NN>` |
| Hand it back | `wf return <page> <NN> --branch B --commit SHA --file PATH` |
| Check it | `wf check <page> <NN>` |
| Sign off | `wf signoff <page> <NN> --outcome passed\|failed\|blocked\|needs-authority` |
| Close it | `wf close <page> <NN>` |
| Send it up | `wf elevate <page> <NN> --to prime\|person --item "..."` |
| Answer | `wf answer <page> <entry> --text "..."` |
| See where things stand | `wf status <page>` |
| Observer check | `wf observe <page> [--record "finding"]` |
| Check nothing was tampered | `wf verify <page>` (`--fix` reprints page files from the log) |

`wf status` is the "where are we" view. It is always built fresh from the log.

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
- `docs/AXIOMS.md`, `docs/DESIGN.md`: the rules and the design, inside the kit.
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
