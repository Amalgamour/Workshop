# Final release check: labs 0702 (seq grammar) and 0703 (seq storage), base c09fa60c

made: 2026-11-19, 2:59 PM EST, by Designer. For Prima's review. Not published; nothing
written under wf-run-gh/pages. wf cites at returns c09fa60c (code d9110934); design
sources at origin/prima/build 8e96151d; build repo bdf3a35. Checklist RELEASE-CHECK.md
@ c0e5b22. Commands: COMMANDS-FOR-PRIMA.md, section "Labs 0702 and 0703".

Files (this folder):
- FINAL-0702-face01.txt, FINAL-0702-face08.txt, FINAL-0702-face06-note.txt
- FINAL-PACK-0702-05.01.txt (sha256 6b603b77f343ad057ce22855966bc696a0a5b40451c1a8589daebc789ef5ada9)
- FINAL-0703-face01.txt, FINAL-0703-face08.txt, FINAL-0703-face06-note.txt
- FINAL-PACK-0703-05.01.txt (sha256 d104fac2cde0f70df1b0e5431cacef1f8654191f31c344cbfaeef7322a5c779d)
- FINAL-0700-face01-v2.txt, FINAL-0700-face08-v2.txt (the door lists both labs: two-way links)

Dry run: the whole block ran with wf-bin/wf-d9110934 on a throwaway copy of wf-run-gh
in /tmp (push URLs disabled; no publish), with WF_KIT_BRANCH=returns. Every step passed;
wf verify passed on 0700 (6 entries), 0702 and 0703 (6 entries each). BUILDER-PROMPT.md
line 13 then reads "cargo install --git https://github.com/Amalgamour/Workshop.git
--branch returns --locked wf" instead of "<kit branch>". The check commands were run with
sh -c in a scratch git repo: each passes with the sections present and fails when one is
missing. The 0703 check (cargo test --manifest-path labs/0703/Cargo.toml) was tried on a
scratch nested crate with an empty [workspace]; it builds apart from the wf crate. Copy
and scratch repos deleted.

## 1. Authority

| Item | Source | Result |
|---|---|---|
| Words file exists and quoted | docs/review/DIRECTOR-WORDS-t450-t453u.md:6, :9, :12, :15 (bdf3a35) | PASS |
| Lab topics | t451u (:9) "axioms, designing and building our grammar out of seqaddr.  How a .seq file should work.  What should be the design for the storage of it." | PASS |
| Prima sets up the pages | t452u (:12) "Your job is to setup the pages where they drop their findings." | PASS |
| Own space, wf design | t453u (:15) "they should still setup a workshop space with it.  Then pull the pages same as cursor and use the wf design." | PASS |
| Grant paths labs/0702/, labs/0703/ | t452u gives the pages, not the paths | TENSION (paths are Prima's choice, H1 traced below) |
| Prima types init-page for 0702/0703 | t437s1659 covered 0700 and 0701 only (DIRECTOR-WORDS-t437-t438u.md:3-4) | TENSION: Q17; face 06 notes carry "[Q17 answer file]" to fill |
| Page numbers, titles, which builder | the file's "Effect" line (:17) is Prima's, not his words | TENSION (relay) |
| Cross-check rule | not in his words; Prima's | TENSION (Prima's rule) |

## 2. Addresses (A1-A9) and H1

| Item | Source | Result |
|---|---|---|
| A1-A4, A7 | t413u.md:7, :9; seqAddr.md:14 | 90.50.10.0702 and 0703 | PASS |
| A5 | t432u; t434.md:24; seqAddr.md section 11 | lab band 0700-0799 | PASS |
| A6, A9 | seqAddr.md:241-242 | on 0701-0798, not 0700 or 0799 | PASS |
| A8 | seqAddr.md:228 | not 0001-0099 | PASS |
| H1 next free slots | 0700 face 01 (labs list) | 0702, 0703 follow 0701 | PASS |
| H1 output path | brief said docs/research/; traced | labs/07NN/ chosen: see 4 | PASS (changed from the brief, said so) |

## 3. Lab band fit

| Item | Source | Result |
|---|---|---|
| Titled by subject | 0700 face 01 v1; seqAddr.md section 11 rule 2 | "seq grammar lab", "seq storage lab" | PASS |
| Reusable across stages | seqAddr.md section 11 rule 2; t432u | serve later .seq stages (roadmap :82, :87) | PASS |
| What a lab does | workflow-loop.003.md:48 "labs: cold-model trials of the page's work"; DEV-WORK-LAB-PAGES.md:45 "tries to break the work"; 0700 face 01 v1 | these learn a subject before any page exists; by the files that is dev (N4: "what we are trying to prove", workflow-loop.003.md:45) | TENSION: Q16. t451u calls them labs ("We can think about labs.  What should we be learning."); 0700 face 01 v2 adds "or it learns its subject by trial" |
| Two-way links | seqAddr.md:251 | door face 08 v2 lists 0702, 0703; each lab face 08 names the door; 0702 and 0703 name each other | PASS |
| Serves | 0700 face 01 | none yet in stage 1; said on faces 01 and 08 | PASS |

## 4. Repo, branch, grant

| Item | Source | Result |
|---|---|---|
| Lands in | pack repo: work, branch returns (cmd.rs:380, :403); return must descend from start and sit on returns (cmd.rs:500-503) | wf repo Amalgamour/Workshop, branch returns | PASS |
| Paths in the return | may touch inside grant (cmd.rs:369-371); return frame (cmd.rs:506-509); check frame (cmd.rs:750-751) | labs/0702/LAB-0702-SEQ-GRAMMAR.md in grant labs/0702/; labs/0703/ in grant labs/0703/ | PASS (dry run packed) |
| Tree at c09fa60c | git ls-tree c09fa60c | no labs/, no docs/research/; docs/ holds the kit docs AXIOMS.md and DESIGN.md that every AGENTS.md pins | PASS: labs/ conflicts with nothing; docs/research/ would sit beside pinned rule files |
| Overlap | cmd.rs:339-355 is per page only; t422.md:7-8 | labs/0702/, labs/0703/ share no file with 0701 (tests/) or stage pages (src/, templates/) | PASS: both may run now, beside the waves |
| Sources | in the build design, not in the wf tree | read only from origin/prima/build 8e96151d via git show; all 15 paths exist there | PASS |
| Findings split from the design | design docs live on prima/build, findings on returns | TENSION: Q15 |

## 5. Packs

| Item | Source | Result |
|---|---|---|
| Start | c09fa60c | both | PASS |
| REQUIRED fields | cmd.rs:16, :365-367 | dry run packed | PASS |
| Checks under cmd /C | git.rs:111 (Windows cmd /C, else sh -c); split on ";" (cmd.rs:748); run in a worktree at the return commit (git.rs:101-107) | git ls-files, git grep -F with double quotes, cargo; no pipes, redirects, && or bash-only tools; no "--" (PowerShell may eat it when Prima's prompt says run the checks) | PASS |
| Builder line (t439u) | DIRECTOR-WORDS-t439u.md:5 | "builder:" field (stored, not printed until 0414) and "Builder: <name>" first in overview | PASS (by hand until 0414) |
| Design review line (t416u) | DIRECTOR-WORDS-t416u.md:7 | overview tells the builder to add it in noticed: (template v3 has none) | PASS (by hand until 0404) |
| Kit branch placeholder | templates/v3/builder.txt:13; render.rs:107; cmd.rs:407 | WF_KIT_BRANCH=returns at pack | PASS; TENSION: --branch follows the returns tip, so the overview also gives the pinned --rev line |
| Install | cargo install --git https://github.com/Amalgamour/Workshop.git --rev c09fa60c92ac2e4cde39c73a061166ebc2fac0e0 --root <folder> --locked wf | installed on the box in 7 s: package wf v0.1.0, bin wf | PASS |
| ASCII, plain words | DIRECTOR-RULINGS.md:16 | all files | PASS |

## 6. Checker

| Item | Source | Result |
|---|---|---|
| How wf records the checker | check entry actor, role checker (cmd.rs:782); refuses only the claim holder (cmd.rs:730, :778) | PASS |
| Named checker | nothing in the pack names one; 0414 adds the builder only | hand-written on faces 01, 08, 06 and the overview, even after 0414 | TENSION |
| Where the check entry is written | the run folder where wf check runs; only return --push pushes a log (cmd.rs:554-575) | a check run in Codex's own wf-run never reaches Prima's log | TENSION, handled: the cross-checker runs wf check --dry-run (writes nothing) and gives Prima the report; Prima records the real check on the box as prima-check with --note naming the cross-checker |

## 7. Axioms

- 1 Authority (Axioms.md:13): TENSION, Q17 and the grant paths.
- 2 Fractal (:15): PASS, sources read, not copied; one folder per lab.
- 6 Lineage (:23): PASS, 0700 face 01 v2 is a new version, v1 stays.
- 7 Missing (:25): PASS, missing sources written as missing; "serves none yet".
- 8 Connection (:27): PASS, two-way links on faces 08.
- 9 Trial (:29): PASS for the labs' purpose; TENSION, no hostile pass on these drafts.

Verdict: no FAIL. 0702: PASS for review. 0703: PASS for review. 0700 face 01 v2 and face
08 v2: PASS for review. Prima should not type the two init-page commands until Q17 is
answered; Q15 and Q16 have defaults that need no change to these drafts.

## 8. Questions for Matthew

Q15. Where do the labs' findings live?
- Proposed: (default) on the returns branch of the wf repo, each lab in its own folder
  (labs/0702/, labs/0703/), and design docs link to them by commit and path. wf needs no
  change. Other option: in the build design (prima/build, docs/research/), which wf v0
  cannot return to (one repo and branch per pack: cmd.rs:380, :500-503; intake reads one
  repo, cmd.rs:601-605).
- Why: the builders work in wf-run spaces (t453u), so wf's checks only cover what lands
  on returns; the design they study lives on prima/build.
- Axioms: 2 Fractal (Axioms.md:15) PASS, one home, linked not copied; 8 Connection (:27)
  PASS; 1 Authority (:13) PASS, wf enforces the grant.

Q16. Are "seq grammar" and "seq storage" labs, in the lab band?
- Proposed: (default) yes: labs 0702 and 0703, and the door's card says a lab may also
  learn its subject by trial before any page needs it. Other option: research pages in
  the dev band of the stage that builds .seq (roadmap stage 3 :82 or stage 4 :87; band
  not set yet).
- Why: t451u says "We can think about labs.  What should we be learning."; the design
  files say a lab tries to break a page's work (workflow-loop.003.md:48;
  DEV-WORK-LAB-PAGES.md:45), and learning is dev work (workflow-loop.003.md:45).
- Axioms: 2 Fractal PASS, labs stay one kind, reusable across stages (t432u); 6 Lineage
  PASS, the door card gets a new version, v1 stays; 9 Trial PASS, they learn by trial.

Q17. May Prima type init-page for 0702 and 0703 for you?
- Proposed: (default) yes, the same as t437s1659 for 0700 and 0701: Prima types it with
  --as matthew, cites your OK, and face 06 says she typed it for you. Other option: you
  type both on your PC.
- Why: wf v0 lets only the person start a page (src/cmd.rs:190) until 0411 and 0412
  land; t437s1659 covered two pages only.
- Axioms: 1 Authority (Axioms.md:13) PASS, your recorded OK; 6 Lineage PASS, face 06
  says who typed.
