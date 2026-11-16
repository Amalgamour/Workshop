# Work-book research: AGENTS.md in Cursor and Grok Build

WORKING PATH. Research by Tester (Grok Bot). Not a ruling.
Only Matthew rules. Prima coordinates. Feeds Designer's
WORK-BOOK-SPEC.md (no draft existed when this was written).
All web sources read 2026-11-16. Prices and plans change fast:
treat every number here as a dated snapshot (may go stale).

## The short version

- Both builders read a plain file called AGENTS.md. [S1][S5]
- Both read nested ones: a deeper folder's file wins. [S1][S5]
- Neither has a hard size limit we found. Both say: keep it
  short. Cursor says keep a rule under 500 lines. [S1][S5]
- Name it AGENTS.md in capitals. Grok Build's list of names
  has no all-lowercase "agents.md". [S6]
- Best option: the compute makes AGENTS.md from the page's
  faces 01 and 05, as an export, one per job. The page stays
  the source. The builder never edits the book.
- Cursor cloud agents need the repo on a host (GitHub and
  similar). [S3] We have one: Amalgamour/Workshop, branch
  prima/build (per Prima, pushed 2026-11-16). Only the local
  copy has no remote, so cloud sees only what was pushed.

## 1. Cursor

What it reads (editor and agent):
- `.cursor/rules/*.mdc` files with a small header. A plain
  .md file in that folder is ignored. [S1]
- AGENTS.md at the project root and in subfolders. A nested
  file applies when working on files in its folder. It is
  combined with the parent; the more specific one wins. [S1]
- Rules go at the start of the model's context. [S1]
- A file named inside a rule is NOT pasted in. The agent opens
  it with its tools when it needs it. Same in editor, CLI and
  cloud. Anything that must always be seen goes in the body. [S1]

Cursor CLI (local, terminal):
- Same rules system. Also reads AGENTS.md and CLAUDE.md at the
  project root. [S2] The CLI page does not mention nested
  files (see "no source found").

Cursor cloud agents (old name: background agents):
- Clone the repo from GitHub, GitLab, Azure DevOps or Bitbucket,
  work on a branch, push back. [S3]
- Read AGENTS.md files; Cursor suggests a "Cursor Cloud specific
  instructions" section, with links out if it grows. [S4]
- Follow committed `.cursor/rules/*.mdc`. [S4b]

Size guidance: "Keep rules under 500 lines", split big rules,
link files instead of copying them. [S1] No hard cap found.

Cost (Cursor pricing page, 2026-11-16): [S9]
- Plus $8/month: Grok models only, no cloud agents.
- Premium $30/month: cloud agents, third-party models at API
  list price. Super $100, Ultra $200.

Cheap at / weak at (sourced only):
- Strong: many cloud agents in parallel, each with its own VM,
  tests, browser, screenshots as proof. [S3]
- Weak for us: needs Premium, and sees only pushed commits,
  so it can lag the local build branch. [S3][S9]

## 2. Grok Build

What it is: xAI's coding agent, the `grok` command. Runs as a
terminal app, headless (`grok -p`), or in other apps. [S7][S8]

What it reads: [S5][S6]
- In each folder: AGENTS.md, Agents.md, AGENT.md, CLAUDE.md,
  Claude.md, CLAUDE.local.md. ALL matching files load, so a
  folder with AGENTS.md and CLAUDE.md gives both.
- Every *.md in `.grok/rules/`; also `.claude/rules/` and
  `.cursor/rules/` for compatibility. (It says *.md; Cursor's
  rules are .mdc. Untested whether Grok loads .mdc.)
- Files in .gitignore are skipped.
- Startup loading needs folder trust (`--trust`). [S6]

Nesting: [S6]
- At start it loads every folder from the repo root DOWN TO the
  working folder. Deeper files come later and win.
- Files in other folders are noted when Grok touches that
  folder, and read "when they apply to the task".
- So: where you start Grok decides what it reads first.

Size: "no character cap and no truncation". Short, specific
rules are followed better; every file costs context. [S5][S6]
`grok inspect` lists each file with its token count. [S5]

Cost (xAI API list prices per 1M tokens, 2026-11-16): [S10]
- grok-build-0.1: $1 in, $0.20 cached, $2 out. 256k window.
- grok-4.7: $2 in, $0.50 cached, $6 out. 500k window.
- At 200k prompt tokens or more, the WHOLE request bills at
  double rate. [S10]

Cheap at / weak at (sourced only):
- Cheap: grok-build-0.1 is xAI's lowest rate listed here. [S10]
- Has `--max-turns` for headless runs. [S11]
- Weak: "grok has no budget feature" (no dollar cap). [S11]
- Weak: loads every name variant, so copies double-load. [S6]
- Which model it uses by default: sources disagree (see end).

## 3. The agents.md open standard

- Plain Markdown. No required fields. [S12]
- The nearest AGENTS.md to the edited file wins. A chat prompt
  overrides all files. [S12]
- Suggested parts: overview, build and test, style, security.

## 4. Best option: layout of a work page's AGENTS.md

Plain idea: the page is the source. AGENTS.md is a printout of
it, made by the compute, for one job. Nobody edits it.

Where things live:
- Face 01: the page's meaning, in model cards (seqAddr.md:150).
- Face 05: the pack, one counter per job (workflow-loop.md:96).
- AGENTS.md: an export. Compute fills it from 01 + one 05 pack
  (R26 export, R33 item 1: books change only through compute).

Sections, fixed order, about 100 lines, hard stop 150:
1. Header, compute-filled: page address.title (R30), pack
   05.NN, approval id, base hash, lead, axioms
   (pack header, workflow-loop.md:98-112).
2. Done looks like: 3-5 lines (axiom 5).
3. Why: 2-3 lines, then a link to face 04 (axiom 4).
4. Frame: may touch (paths), must not touch, stop if (axiom 5).
5. Work cards w01, w02 ... (workflow-loop.md:114-130).
6. Checks: exact test commands to run.
7. Hand back: what to return, through the gate as a proposal;
   what was gathered and what was not (R37 items 6, 10).
8. Links: rulings and axioms by address.title, to open when
   needed, not pasted in. Both builders support this. [S1][S6]

Size budget for the whole chain a builder loads:
- Root AGENTS.md: under 40 lines (cold set 1.7.8, the gate,
  never write books/). Grok always loads it. [S6]
- Job AGENTS.md: under 150 lines. Check with `grok inspect`.
- Whole chain: under 300 lines; Cursor's 500 is a ceiling. [S1]

Nesting: do not mirror book folders. Builders nest by where the
CODE is, not where the TASK is. A page in books/ is not near the
code it changes. So compute writes the job AGENTS.md at the root
of a fresh worktree, one job per worktree. Both builders load a
root file every time. [S1][S6]

Axioms check:
- 1 (Axioms.md:13) pass: the printout never outranks the page.
- 2 (:15) pass: inherit the root file, write only the difference.
- 3 (:17) pass: lead letters ride in the header.
- 4 (:19) pass: why is in, short, linked to 04.
- 5 (:21) pass: frame and stop-if are required sections.
- 6 (:23) pass: base hash ties the job to one page version.
- 7 (:25) pass: hand back keeps "not gathered" apart.
- 8 (:27) pass: a copy is not the source; links by address.
- 9 (:29) tension: untested. Needs a trial run on both builders.

## 5. Other options Matthew may not have thought of

A. Hash the printout. Store the AGENTS.md hash in the hand back
   and face 09. Why: R37 item 4, a review ties to an exact
   version. Who is hurt without it: the reviewer. 6 pass, 8 pass.
B. One name only. Forbid CLAUDE.md and AGENT.md copies. Why:
   Grok loads every variant [S6], so copies double-load and
   drift. 2 pass ("do not copy the parent").
C. No file at all: pass the pack as the prompt (`grok --rules`,
   `agent -p`). [S6][S2] Why: nothing to go stale. Cost: harder
   to audit. 6 tension unless the prompt text is logged.
D. Route by cost. Small bounded cards to Grok Build
   (build-0.1). Jobs that need a VM, browser or many in parallel
   to Cursor cloud. [S3][S10] 3 pass (compute picks the lead).
E. Stay under 200k tokens per request. xAI doubles the whole
   bill past it. [S10] Use the face 03 menu first (R35 note).
   5 pass.
F. Compute lint: refuse a job AGENTS.md over budget, with
   pasted rulings, or missing a stop-if. 1 pass, 9 pass.
G. A cap from outside: set `--max-turns` on Grok, since it has
   no dollar cap. [S11] 1 pass (person sets the limit).

## 6. Questions for Matthew (t189u form)

Q1. (1) Is a work page's AGENTS.md stored in the book, or is it
a printout the compute makes for each job?
(2) Proposed: a printout (export), made from faces 01 and 05.
(3) Why: R33 says books change only through compute. Two
builders read it; one source stops drift.
(4) Axioms: 1 pass, 2 pass, 6 pass, 8 pass, 9 tension (untried).

Q2. (1) Should Cursor cloud agents work from prima/build on
GitHub? Pushes there need your OK, and cloud needs the paid
plan.
(2) Proposed: yes, once you OK the plan. Each job starts from a
pushed prima/build commit named in its AGENTS.md header. The
agent works on its own branch and hands back as a pull request.
It never pushes to prima/build. Nothing merges without you.
Until then, use local Cursor and Grok Build.
(3) Why: the code is already hosted, so nothing new is exposed.
Naming the start commit keeps the line traceable. Pushes and
spending stay your call. [S3][S9]
(4) Axioms: 1 pass (push, merge, and plan stay with you);
6 pass (start commit recorded); 8 pass (hand-back links to its
job); 7 tension (local build can be ahead of prima/build, so a
job sees old code until a push).

## 7. No source found

- A hard line or token limit for AGENTS.md in Cursor.
- Whether Cursor finds an all-lowercase "agents.md".
- Whether the Cursor CLI reads nested AGENTS.md (page says root).
- Whether the Cursor editor reads CLAUDE.md (CLI page says yes).
- Grok Build's default model: config sample says grok-4.5 [S13];
  third-party pages say Grok 4.7. Unverified.
- Whether Grok loads .mdc files from .cursor/rules (docs: *.md).
- How much token use each plan buys. Not published.
- Which builder writes better code for which task. None found.

## Sources (all read 2026-11-16)

S1  https://cursor.com/docs/context/rules
S2  https://cursor.com/docs/cli/using
S3  https://cursor.com/docs/cloud-agent
S4  https://cursor.com/docs/cloud-agent/setup
S4b https://cursor.com/docs/cloud-agent/best-practices
S5  https://docs.x.ai/build/features/project-rules
    (page says last updated July 4, 2026)
S6  https://github.com/xai-org/grok-build/blob/main/crates/
    codegen/xai-grok-pager/docs/user-guide/12-project-rules.md
S7  https://docs.x.ai/build/overview
S8  https://github.com/xai-org/grok-build
S9  https://cursor.com/pricing
S10 https://docs.x.ai/developers/pricing
S11 https://github.com/xai-org/grok-build/blob/main/crates/
    codegen/xai-grok-pager/docs/user-guide/14-headless-mode.md
S12 https://agents.md/
S13 https://github.com/xai-org/grok-build/blob/main/crates/
    codegen/xai-grok-pager/docs/user-guide/05-configuration.md
