# Builders on your own machine: a walkthrough

Written by Prima on Thu Nov 19, 2026, about 12:00 PM EST, because you asked (t391u): "So we can start to get builders on my local environment setup. I'll need you to walk me how it should work."

Your machine: Windows. Repos live under `D:\Git\`. All commands are PowerShell.
The tool is `wf`. The rules come from the kit's README.md, AGENTS.md and docs/DESIGN.md, and from its code (`src/`), at commit a00bc53.

**I can't test on Windows.** I ran every step below on the Linux box with the same tool. I list the Windows risks I found in the code in section 7.

---

## 1. Who does what

| Role | Who | What they run |
|---|---|---|
| **Person** | You (Matthew) | Start the page and give the grant (`init-page`, `grant`). Answer questions (`answer`). Stop the page if needed (`halt`). |
| **Prime** | Prima (the lead) | Write the faces (`face-write`), plan a pass (`draft`), release it (`pack`), sign off (`signoff`), close it (`close`). |
| **Builder** | A Cursor agent | `claim` the pass, do the work on its pass branch, `return` it. |
| **Checker** | A Codex agent (never the builder of that pass) | `check` the return. |
| Observer (optional) | A third agent (never Prime) | `observe`. |

[source: kit AGENTS.md, "Your role, and what you may run"]

Signing off: in wf, `signoff` and `close` are Prime's commands. The tool checks that the signer is the Prime named on face 00.
Your yes comes after the close. You read the close record and decide whether the pass branch gets merged. wf never merges anything. [kit README, "Not in v0": "wf does not merge accepted work"]

---

## 2. Install (once)

1. **Git for Windows**: https://git-scm.com. `wf` runs `git` itself, so `git` must work in PowerShell.
2. **Rust**: https://rustup.rs. Run `rustup-init.exe` and take the defaults. If it asks for the Visual Studio C++ Build Tools, install them too.
3. Check that both work:
   ```powershell
   git --version
   cargo --version
   ```
That is all wf needs. It uses only two code libraries, `serde_json` and `sha2`, and cargo downloads them on the first build. [Cargo.toml]
The box built and tested it with Rust 1.85.1. [tester-ahash/CHECK-RESULTS.md]

---

## 3. Which commit to build, and why

- **Build a00bc53 (the `workflow` branch on GitHub).** It is the last merged commit. The pinned tool on the box is built from it. The three real pages were made with it, and they verify with it today. Its tests pass: 29 unit + 78 end-to-end.
- **Not agents-hash yet.** The newest work (agents-hash c224329, and the other branches) passed Tester, but it is not merged. Merges wait on you. It is also not on GitHub yet.
- a00bc53 is missing one fix that matters: a failing check could repaint the checker's screen to look like a pass. With a00bc53, always confirm a check with `wf status` (see step 9).

---

## 4. Get the kit and build wf

```powershell
cd D:\Git
git clone -c core.autocrlf=false -b workflow https://github.com/Amalgamour/Workshop.git wf-kit
cd D:\Git\wf-kit
git checkout a00bc53
cargo build --release
New-Item -ItemType Directory -Force D:\Git\wf-bin
Copy-Item target\release\wf.exe D:\Git\wf-bin\wf.exe
D:\Git\wf-bin\wf.exe help
```

- **`core.autocrlf=false` matters.** wf builds its templates and the axioms file into the program. If Git turns their line endings into Windows ones, every page the tool prints will be different from the box's pages. [src/render.rs lines 13-25, `include_str!`]
- Run the **copy** in `wf-bin`, never the build folder. A builder's build must never overwrite the tool that judges the work. [kit AGENTS.md, "The tool you run"]
- Add `D:\Git\wf-bin` to your PATH, or type the full path each time. Below I write `wf` for short.

---

## 5. Make a run folder

A run folder holds `pages\` (wf makes it) and the work repo next to it. In a plan, the `repo:` line names the work repo's folder. [kit README, "A plan file"]

```powershell
New-Item -ItemType Directory -Force D:\Git\wf-run
cd D:\Git\wf-run
git clone -c core.autocrlf=false https://github.com/Amalgamour/Workshop.git workshop
$env:WF_ROOT = "D:\Git\wf-run"
```

`wf` finds pages in the current folder, or in `WF_ROOT`. [src/lib.rs, help text]
For a first trial, a tiny practice repo is safer than Workshop itself (see the decisions at the end).

---

## 6. One pass, step by step

The example page is `90.40.00.0001`. Page ids are only labels in wf v0.
Every command that writes needs `--as <name>`. Each agent can set its own name once per terminal instead: `$env:WF_AS = "cursor-b1"`.

**Step 1. You start the page and give the grant.**
```powershell
wf init-page 90.40.00.0001 --title "first local trial" --person matthew --prime prima --grant "src/,tests/" --grant-ref t391u --as matthew
```

**Step 2. Prime writes the goal (face 01), the dev goals (face 04) and a note (face 06).**
```powershell
wf face-write 90.40.00.0001 01 --file face01.txt --as prima
wf face-write 90.40.00.0001 04 --section goals --text "..." --as prima
wf face-write 90.40.00.0001 06 --text "first pass: why and what I read" --as prima
```
Face 01 holds the `Done when:` lines the checker judges.

**Step 3. Prime drafts and packs the pass.** A plan file looks like this:
```
repo: workshop
start: prima/build
outcome: one plain sentence
w01: the first job
may touch: src/x.rs, tests/x.rs
checks: cargo test x
stop if: the job needs a file outside may touch
```
```powershell
wf draft 90.40.00.0001 --file plan.txt --as prima
wf pack 90.40.00.0001 01 --as prima
```
The pack prints the job into `pages\90.40.00.0001\05.01\`: `PROMPT.md`, `AGENTS.md`, `PACK.md` and `RETURN-TEMPLATE.md`.

**Step 4. The builder (Cursor) claims it.** Tell it: "Read `D:\Git\wf-kit\AGENTS.md`, then `D:\Git\wf-run\pages\90.40.00.0001\05.01\PROMPT.md` and `AGENTS.md`, and follow them."
```powershell
wf claim 90.40.00.0001 01 --as cursor-b1
```
The first claim wins.

**Step 5. The builder works on its own pass branch.** It starts from the start commit named in PROMPT.md:
```powershell
git -C D:\Git\wf-run\workshop worktree add D:\Git\wf-run\b-05.01 -b pass/90.40.00.0001.05.01 <start sha>
```
It changes only the "may touch" files. Then it copies `RETURN-TEMPLATE.md` to `.workshop/returns/90.40.00.0001.05.01.md`, fills every line, stages by path, and commits.

**Step 6. The builder returns.**
```powershell
wf return 90.40.00.0001 01 --branch pass/90.40.00.0001.05.01 --commit <full sha> --file .workshop/returns/90.40.00.0001.05.01.md --as cursor-b1
```
- wf reads the branch from the work repo. A worktree branch is already there, so no push is needed.
- Type `--file` with forward slashes, exactly as PROMPT.md shows it.
- Any changed file outside "may touch" gets the return refused, and the refusal is recorded.

**Step 7. The checker (Codex) checks.**
```powershell
wf check 90.40.00.0001 01 --dry-run --as codex-c1
wf check 90.40.00.0001 01 --as codex-c1
```
- Before filing, the checker reads the return file and the diff.
- It adds `--fail "why"` if a `Done when` line is not met, even when the commands pass.
- wf refuses a check by the builder of that pass. [src/cmd.rs line 538]

**Step 8. Prime signs off and closes.**
```powershell
wf signoff 90.40.00.0001 01 --outcome passed --as prima
wf close 90.40.00.0001 01 --as prima
```
The outcome is one of passed, failed, blocked or needs-authority. A `passed` signoff is refused if the check failed.

**Step 9. Anyone can look at the page. These only read.**
```powershell
wf status 90.40.00.0001
wf verify 90.40.00.0001
wf observe 90.40.00.0001
```
`status` shows the true check verdict from the log. Use it after every check (see section 3).
Use `wf halt` / `wf resume` with `--note "why (ref)"` to stop or restart a page.
If a builder is stuck, it ends the job `need` or `blocked`, and wf sends it to Prime.

I ran this whole loop with a00bc53 on the box today (one pass, closed `passed`; verify ok).

---

## 7. Windows risks I found in the code (untested)

1. **Line endings.** Without `core.autocrlf=false`, the templates and axioms built into wf change. Printed pages then differ from the box's pages, and the pinned hashes differ. The kit has no `.gitattributes` to stop this.
2. **CRLF and BOM in files you give wf.** I tested Windows-style bytes on the box:
   - `face-write --file` with CRLF endings is refused.
   - `draft --file` with a BOM at the start is refused.
   - CRLF in a plan file and in a return file was accepted.
   - Fix: save files as UTF-8 with no BOM and LF endings (in Cursor: bottom bar, "LF"). In Windows PowerShell 5.1, `Out-File` writes UTF-16 and `Set-Content -Encoding utf8` adds a BOM. Use an editor instead, or PowerShell 7 (`Set-Content -Encoding utf8NoBOM`).
3. **Checks run in `cmd /C` on Windows, not `sh`.** So a check line like `FOO=1 cargo test` or `true` will not work. Write checks that cmd understands. [src/git.rs `run`]
4. **The tool's own tests will likely fail on Windows.** 43 test lines use `true` as the check, and cmd has no `true` command. A red `cargo test` on Windows is expected. It does not mean the tool is broken. [tests/wf.rs]
5. **Paths use forward slashes.** "may touch", the grant and `--file` are compared as text against git's paths. Use `src/`, never `src\`. [src/page.rs `inside`; src/cmd.rs `ret`]
6. **Untested:** the check's temporary worktree under `%TEMP%` (long paths), Windows junctions vs wf's linked-folder check, and antivirus or OneDrive holding `.wf-lock`.

---

## 8. Safety rules every builder must follow

You approved these (t335s1296):
1. **Stage by path only.** `git add -- <path>`. Never `git add -A`, `git add .` or `git commit -a`.
2. **Push only to your granted branch** (your `pass/...` branch). Never merge into main. Never force push.
3. **Never commit secrets.** Never print, copy or commit a token, password or key. If you find one, stop and say where, without its value.

And from the kit:

4. **Never edit anything under `pages\` by hand.** Only wf writes there.
5. **Use your own name in `--as`.** Never use someone else's. wf can't prove names yet, so this rule is on trust.
6. **Build into your own folder**, for example `$env:CARGO_TARGET_DIR = "D:\Git\target-builder"`. Never build into `wf-bin`.
