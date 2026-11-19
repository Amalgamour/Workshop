# WF over GitHub: the minimum loop (build stage)

Status: **build stage**, MVP. Branch wf-functional (from agents-hash c224329). Not merged, not pushed.

## His words (verbatim)
- t400u: "You push work onto github.  Then you hand me the prompt for the cursor to do.  That or I launch grok builders in powershell.  Either one works.  Then once they commit it they push it for you to review. ... you can make a returns branch and a packs branch if that works.  Then the builders run the compute to create the return, the compute pushes it ..."
- t401u: "Yes you are correct one shared returns branch and one packs branch. ... So lets get WF into a functional state.  It doesn't have to be perfect, it can be glitchy, we just need I can give you work."
- t402u (relayed by Prima): the first goal is the minimum pieces to close one loop; manual steps first, automation next, polish and security last ("We can't secure until it's finished").

## The layout
- GitHub repo, two working branches: `packs` (only `pages/`, plus a `.gitignore` with `work/`), written only by Prima;
  `returns` (the code the passes change, plus `.workshop/returns/<pass>.md` and `.workshop/logs/<page>/log.jsonl`), shared by every builder.
- A run folder (Prima on the box, each builder on Windows) = a clone of `packs`, with `work/` inside it = a clone of `returns`.
  The draft's `repo:` field is `work`; its `start:` is `origin/returns` (resolved to a SHA at pack).

## The commands
1. `wf pack <page> <NN> --branch returns`: as before, plus the pack records `branch: returns`, the `remote`
   (origin URL of work/) and `kit_branch` (env `WF_KIT_BRANCH`, where builders install wf from).
   For v3 packs wf also prints `05.NN/BUILDER-PROMPT.md`: the one paste for a Cursor or Grok builder in PowerShell
   (templates/v3/builder.txt). It is a view (reprinted from the log), not hashed.
2. `wf publish-pack <page> [<NN>]` (Prima): refuses unless the run folder is on `packs`; `git add -- pages/<page>`;
   commit "wf: publish <pass>"; `git push origin HEAD:refs/heads/packs`. Never forced. Takes no page lock (a lock
   file would be staged). Also used after close, to publish the closed log.
3. `wf return ... --push` (builder): fetch `returns`, check out `returns` at origin's tip, **merge** the builder's
   commit (a merge keeps its SHA, which the return records; a rebase would change it), then the usual return check
   and log lines. Then copy the page log to `.workshop/logs/<page>/log.jsonl`, commit it by path, and push.
   A rejected push does `git pull --no-rebase` and tries again, 3 times; never forced. A merge conflict stops before
   anything is recorded or pushed.
4. `wf intake [--repo work] [--branch returns]` (Prima): fetch `returns`; for each `.workshop/logs/<page>/log.jsonl`,
   if this run folder's log is an exact prefix of it, append the new entries, reload (the chain and the order rules
   must hold, or the old log is put back), reprint the views, and list passes ready to check. Anything else is
   refused with a plain line; other pages still go in.

## Why these choices
- One `returns` and one `packs` branch: t401u. Per-page paths keep collisions rare.
- Merge, not rebase, on the shared branch: the return records the commit SHA; rebase would orphan it (t402u: simplest thing that works).
- Builder work starts at the pack's start commit (a local branch), so the frame check (start..commit) sees only that pass's changes even when other returns landed since.
- The builder's claim travels with its return; Prima learns of it at intake (manual first, t402u).

## Later (TODO, not built)
- Intake check that the returned log continues from the **packs head** for that page (an outside record; closes most of Tester's full-rewrite hole). t402u moved it later.
- The 4-hour cheap check routine (LOCAL-BUILDER-FLOW-t400u.md, choice 3).
- Windows: 60+ e2e tests use `true` as a check command (not a Windows command); tests also use `grep`, `test`, shell redirection. Make checks portable or skip on Windows with a reason. Not done.
- Claims are only local until intake: two builders could claim the same pass on two machines. Prima must hand each prompt to one builder.
- `.gitattributes` with `* -text` is in the kit; the `packs` and `returns` branches need the same file.
