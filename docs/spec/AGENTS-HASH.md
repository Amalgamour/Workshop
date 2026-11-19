# AGENTS-HASH: the release hash on a pass's AGENTS.md and PROMPT.md

Status: **build stage.** Built on branch agents-hash (from harden-dev 2b5a7ef). Not merged, not pushed.
The rule comes from the Director (t373u). The details below (field names, messages, what counts as
"old") are the builder's reading, not his words.

## His words (t373u, Nov 19 2026, 10:57 AM EST, verbatim)

"We need to run that bit check thing.  I can't remember the name so it's recorded once a released agents file is done.  So we can confirm it's correct otherwise it's invalid."

Our reading (not his words): the "bit check thing" is a hash (sha256). When wf releases a pass's
AGENTS.md (and PROMPT.md, which is released at the same moment), it records the hash in the page log.
Any copy whose hash does not match is invalid. This answers question C5 of the Codex ideas design
pass (docs/design/CODEX-IDEAS-design-pass.md on prima/build, lines 149-151 and 227-231).

## Why

- Before this, the pack entry pinned the templates only by a label, `templates: "2"` (cmd.rs pack;
  render.rs `packed_templates`). If someone edited templates/agents.txt without a new label,
  `wf verify --fix` would reprint every past AGENTS.md with the new words and call it "matches the log".
  The past would have been rewritten, and no one could say what a worker was really given.
- Axiom 1 (authority): the live record is the log. A copy does not outrank it. The hash lets the log
  say exactly which text was released, byte for byte.
- Axiom 6/8: a view is a pointer to the record; the hash is how anyone checks the pointer.

## What wf does now

1. **At pack.** wf prints AGENTS.md and PROMPT.md from the new pack entry itself, then stores
   `agents_hash` and `prompt_hash` (full sha256 hex of the exact bytes written) in that entry.
   The templates have no slot for these two fields, so storing them does not change the text.
2. **Every read that loads the page** (every command except `board`, which compares the same way
   without writing) recomputes:
   - the copy on disk against the recorded hash. A hand edit gives
     `AGENTS.md for pass 05.NN is invalid: hash mismatch (the copy on disk hashes to X, the log recorded Y)`.
   - the text this wf would print against the recorded hash. A template change after release gives
     `AGENTS.md for pass 05.NN is invalid: hash mismatch (pack entry N recorded Y, this wf would print X; the released text is not reprinted)`.
   The same for PROMPT.md. `verify` exits 1; write commands are refused and write nothing.
   Recorded values are escaped (a forged field may hold control characters) and a non-string field
   matches nothing.
3. **verify --fix.** A hand-edited copy is reprinted, because the reprint hashes to the recorded value
   (the released bytes come back). If the reprint would hash differently, `--fix` refuses with
   `refused to reprint: ...; nothing was changed` and writes no view at all, not even a missing one.
   wf never rewrites what a worker was given.
4. **Old pack entries** (no hash field, packed before t373u) are not failed. `verify` adds one line per
   pass, `05.NN: AGENTS.md no hash recorded (before t373u); PROMPT.md no hash recorded (before t373u)`,
   and the board card has a `released:` line saying the same. The real pages 90.10, 90.20 and 90.30
   verify ok this way.
5. `wf verify` on a page with hashes prints `05.NN: AGENTS.md hash <12 chars> holds; PROMPT.md hash <12 chars> holds`.

## Consequence for builders

A template text change is now a new template version (a new label and a new file, like templates/v1),
never an edit of the current one. Editing templates/agents.txt or prompt.txt in place would make every
hashed pass on every page invalid and lock those pages until the old text is back.

## Not covered (open)

- RETURN-TEMPLATE.md and PACK.md are not hashed by this rule. PACK.md already has `pack_hash`.
- The hash proves what wf printed. It does not prove what reached the worker (Codex idea 1 / C2: a
  delivery entry). It does not prove who claimed (the name is still `--as`).
- Whether an "invalid" file should also be raised to Prime or the person automatically is not decided.
