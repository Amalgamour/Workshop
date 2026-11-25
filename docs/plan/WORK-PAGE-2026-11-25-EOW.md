# Work page, end of week, Wed Nov 25 2026

One run each for Claude and Codex tonight. About 30 minutes each.

Matthew picked Ideas 1 and 2 (card t593s2418, from t593u).

Written by Prima on Wed Nov 25, about 5:00 PM EST. All times are EST.

This is a plan page. It is not a wf page. It opens no pass by itself.

## Why this work

- We want a scaffold for the interface: a kanban "workshop front" in Next.js over the Rust compute core.
- The boards should join up the kernel, pages, desk, faces and seqaddr (axiom 8, connection).
- A book board and a page board should be the same shape at every level (axiom 2, fractal).
- Every card should carry its why and its ruling id (axiom 4, why).
- The design must rest on what really exists (axiom 9, trial).

## Issues found in the skim

1. **The reader app is old.** app/ was last changed Nov 11. That is before wf, packs, returns and boards.
2. **README.md is old.** Last changed Nov 11.
3. **DESIGN.md line 14 is wrong now.** It says several models may work one page at once. The live rule is one holder (0423).
4. **The board design is old.** docs/design/WF-BOARD.md was last changed Nov 18.

This page does not fix these. Claude designs. Codex gathers evidence.

## Rules for both

- Write only in your own folder, and your report under `reports/lab/<folder>/`.
- Never touch `src/`, `tests/`, `.workshop/`, `pages/`, `app/`, or the other agent's folder.
- Run no wf command. Not even read-only ones.
- You have no signoff, close or pack authority.
- Read anything. Cite every claim with a file and line, a commit, or a web link.
- Plain words. Short lines. One idea per line. Matthew is dyslexic.
- Stage files by path only. Never `add -A`. Never `commit -a`.
- Commit with the trailer `Builder: <name>`. Push to returns only. Never force push. Never merge into main.
- Never print, copy or commit a token, password or key.
- Report path: `reports/lab/<folder>/<Agent>-<YYYYMMDD-HHMM>.md`, local time.

## Extra rules for Claude (t580u)

- Narrow fenced lane: only `labs/ui-scaffold/` and `reports/lab/ui-scaffold/`.
- Design only. Touch no data, logs or datasets.
- No wf commands at all.
- Your design is checked by another view before anyone uses it.

## Stop rules (both)

Stop, push what you have, and report if:

- the work would need a file outside your folder;
- you find a rule conflict for Matthew (write it as a question; do not decide it);
- a push is refused twice;
- the job is not done in about 30 minutes (push progress, say what is left).

## Lanes

| Agent | Folders it may write (on returns) |
|---|---|
| Claude | labs/ui-scaffold/, reports/lab/ui-scaffold/ |
| Codex | labs/ui-evidence/, reports/lab/ui-evidence/ |

No folder is shared. Each may read the other's folder. Neither writes it.

## Claude: UI-1, kanban front design

Folder: `labs/ui-scaffold/`

Job:

- Design the workshop front: a Next.js kanban that reads only. The Rust compute core owns every write.
- Screens: a book board, a page board (faces 00-08 and the 05 passes), and a desk (who holds what).
- A card shape: address, holder, step, next, why, ruling id.
- Show how one board shape repeats at book, page and pass level.

Done when:

- `README.md` gives 2 or 3 options, each with its cost. The option that best fits axiom 2 is marked ★ and is the default.
- `CONTRACT.md` lists every field the screens show. Each field cites its source: wf board output, the compute crate, a face file, or the page log. A field with no source is marked missing.
- `QUESTIONS.md` has the open questions for Matthew, each with a default.
- No file in `app/` is edited.

Size: one run, about 30 minutes.

## Codex: UI-2, interface evidence

Folder: `labs/ui-evidence/`

Job:

- List what exists today, with file and line: app/ (lib/compute.ts, lib/rules.ts, lib/seq.ts, mock/), the crates/compute endpoints, src/board.rs output, and the face formats.
- A gap table: what a board scaffold needs, what exists, what is missing.
- Pattern notes on 3 public board tools, for example GitHub Projects, Linear and Trello.

Done when:

- `EXISTS.md`: every item has a file and line, or a commit.
- `GAPS.md`: every row is marked exists, partial or missing, with a cite.
- `PATTERNS.md`: 3 tools. Each has a link, the pattern in 2 or 3 lines, and one line on whether it fits our boards.

Size: one run, about 30 minutes.

## Prompt: Claude

```
Builder: Claude (Matthew's PC, D:\Git\claude\wf-run\work)

Lab job UI-1 from docs/plan/WORK-PAGE-2026-11-25-EOW.md on prima/build. That page is your brief. Do only UI-1.
0. cd D:\Git\claude\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, and git branch --show-current says returns. If not, stop and report.
1. git fetch origin; git pull --ff-only origin returns. Also read origin/prima/build.
2. Read the "Why this work", "Rules for both", "Extra rules for Claude", "Stop rules" and "Lanes" sections, then the UI-1 section.
3. Write only in labs/ui-scaffold/, plus your report at reports/lab/ui-scaffold/Claude-<YYYYMMDD-HHMM>.md (use the real local time).
4. Write README.md, CONTRACT.md and QUESTIONS.md. Meet every UI-1 "Done when" line. Cite a file and line, or a commit, for every claim.
5. Design only. Do not edit app/, src/, tests/, .workshop/, pages/, any log or any data file.
6. Put any rule conflict as a question for Matthew. Do not decide it. Do not weaken any rule.
7. Run no wf command. You have no signoff, close or pack authority.
8. Commit by path only (git add -- <path>), with the trailer "Builder: Claude". Push to returns. Never force push. Never merge into main.
9. Stop after about 30 minutes, or when done. Stop early on any stop rule.
10. Tell Matthew "UI-1 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). If wf fails:
1. Stop. Retry the same wf command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, the wf commit it was built from, and the OS.
4. Keep all work inside the grant. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: <name>" to returns. Do not write under .workshop/.
5. Write reports/<page>/05.NN/<Builder>-MANUAL-RETURN-<stamp>.md with: page, pass, builder, pack hash, start commit, failing step, error, what was done, files touched, test results, and the code commit. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). You still hold the page. The report releases the face lock. This is not a handover. The pass never closes until the report is committed to returns and the checker reviews it.
```

## Prompt: Codex

```
Builder: Codex (Matthew's PC, D:\Git\codex\wf-run\work)

Lab job UI-2 from docs/plan/WORK-PAGE-2026-11-25-EOW.md on prima/build. That page is your brief. Do only UI-2.
0. cd D:\Git\codex\wf-run\work. Check first: git remote -v shows Amalgamour/Workshop, and git branch --show-current says returns. If not, stop and report.
1. git fetch origin; git pull --ff-only origin returns. Also read origin/prima/build.
2. Read the "Why this work", "Rules for both", "Stop rules" and "Lanes" sections, then the UI-2 section.
3. Write only in labs/ui-evidence/, plus your report at reports/lab/ui-evidence/Codex-<YYYYMMDD-HHMM>.md (use the real local time).
4. Write EXISTS.md, GAPS.md and PATTERNS.md. Meet every UI-2 "Done when" line. Cite a file and line, a commit, or a web link for every claim.
5. Read only. Do not edit app/, src/, tests/, .workshop/, pages/, any log or any data file.
6. Put any scope or rule conflict as a question for Matthew. Do not decide it.
7. Run no wf command. Do not pack, sign off or close.
8. Commit by path only (git add -- <path>), with the trailer "Builder: Codex". Push to returns. Never force push. Never merge into main.
9. Stop after about 30 minutes, or when done. Stop early on any stop rule.
10. Tell Matthew "UI-2 pushed" with the commit id and 3 lines on what you found.

MANUAL RETURN (docs/plan/MANUAL-RETURN.md). If wf fails:
1. Stop. Retry the same wf command at most once. If it fails again, do not keep trying.
2. Never hand-edit .workshop logs or log.jsonl. Never fake a claim, return, check, or close. Never bypass wf by hand.
3. Record the exact command, exit code, full error text, the wf commit it was built from, and the OS.
4. Keep all work inside the grant. Stage files by path only (never add -A, never commit -a). Commit with trailer "Builder: <name>" to returns. Do not write under .workshop/.
5. Write reports/<page>/05.NN/<Builder>-MANUAL-RETURN-<stamp>.md with: page, pass, builder, pack hash, start commit, failing step, error, what was done, files touched, test results, and the code commit. Push to returns. Never force push.
6. If the push fails too, paste that same report to Matthew in one block (last resort only). You still hold the page. The report releases the face lock. This is not a handover. The pass never closes until the report is committed to returns and the checker reviews it.
```

## What Matthew decides

1. Approve this page, or change it.
2. Nothing goes to Claude or Codex until you say so.
