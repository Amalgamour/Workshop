# DESIGN.002 — implementation decisions for the status/intake fixture lab

Batch: 0507.prime-support/05.02.
Author: claude-opus-5-5.
Date: 2026-10-27.

This is additive to `../design05.01/DESIGN.md`, which stays unchanged. Where they differ, this file wins, and only inside this fixture lab. The PS items come from Prime's 05.01 review. Every field named here is a **provisional fixture contract**. None of them is workshop law.

## 1. Registry (`prime-support-registry`, version 1): exact keys, strict JSON

```json
{"schema": "prime-support-registry", "version": 1,
 "repositories": {"<name>": {"local": "<abs path>", "branch": "<branch>", "remote_ref": "refs/remotes/<...>",
                             "worktree": "registered-paths" | "off", "history_limit": 50}},
 "canonical_assignment": {"repository": "<name>", "path": "<rel>", "lane": "<lane>"} | null,
 "lanes": [{"lane": "<id>", "project": "<text>", "owner_label": "<text>", "repository": "<name>",
            "pages": ["<rel page folder>"], "return_files": ["<rel file>"], "review_sources": ["<rel file>"]}],
 "attention_order": ["conflict", "missing", "unsupported", "review-needed", "unseen", "history-unknown", "open-finding"]}
```

Validation:
- Every key is required, except `canonical_assignment` and `attention_order`, which may be omitted.
- Unknown keys, duplicate keys, NaN and Infinity are refused.
- Paths are relative POSIX paths: no `..`, no leading `/`, no backslash, no drive.
- `local` must be absolute.
- `owner_label` and `project` are display text.
- The registry owns paths and scope only. It holds no state.

## 2. What is read (bounded)

- **A page folder:** only root files named `05.NN.md`. The listing comes from `git ls-tree` at each observed commit, plus the folder itself in the worktree when `worktree: registered-paths`. Nothing below the page folder is read.
- **A return file:** that exact path.
- **A review source:** that exact path.
- **Revisions observed per file:**
  - `published` is the file at `remote_ref`. It is the last-observed ref and is never fetched.
  - `local` is the file at HEAD.
  - `worktree` is the file on disk, read only when `worktree` is `registered-paths`.
- **History:** `git log --format=%H -n <limit> <HEAD> <remote_ref> -- <path>`. History is `complete` only when the repository is not shallow and fewer than `limit` commits were returned. Otherwise it is `incomplete`. An untracked file has history `none`.
- **Git subcommands allowed:** rev-parse, show, ls-tree, log, status, merge-base, for-each-ref, cat-file. They run with `GIT_OPTIONAL_LOCKS=0`. Any other subcommand raises before it runs.

## 3. Structure and identity (PS-01, PS-02)

**Parsing:**
- Bytes are decoded as UTF-8. Invalid bytes mean the source is `unsupported`.
- Lines are split on LF. A trailing CR is ignored for structure, and the hash is always taken over the raw bytes.
- **Fences:** a line indented at most 3 spaces that starts with 3 or more backticks, or 3 or more tildes, opens a fence. A line of the same character, at least as long, with nothing else after it, closes it. An unclosed fence makes the source `unsupported: unclosed fence`.
- **Recognized top-level headings**, outside fences only:
  - `## Return` or `## Return — <label>`;
  - `## Review` or `## Review — <label>`;
  - for return files only, line 1 must be `# Return` or `# Return — <label>`.
  - The separator is ` — ` (U+2014 with spaces).
- **Ambiguous:** any other line outside a fence, `#` to `######` then a space, whose text case-folded begins with `return` or `review`. The source is `unsupported: ambiguous heading line N`.
- **Page structure:**
  - exactly one Return is required;
  - zero Review headings, or one after the Return;
  - more than one Return or Review is `unsupported: duplicate heading`;
  - a Review before the Return is `unsupported: misordered`;
  - a page with no Return is `no-return`. It is a batch and is not intake-eligible.
- **Return-file structure:** line 1 is the return heading. At most one `## Review` may follow, with the same rules.

**Reviewable bytes:** every byte before the Review heading line, or the whole file when there is no Review heading. Trailing whitespace-only content is then removed (spaces, tabs, CR, LF at the end), and exactly one LF is appended.

This normalization is a deliberate deviation from the 05.01 design's exact-prefix example. Without it, appending a Review section and its separating blank line to a file that had none (the SoF return-file case) would change the identity of an unchanged return. As a result, the 05.01 example numbers (5e4439fc…, 8c1dfe6f…) are not this lab's ids. The rule itself, "bytes before the review boundary", is unchanged.
- `revision_id` = sha256 of the reviewable bytes, written as full hex in every record and JSON output.
- A change to any reviewable byte, including instructions or metadata before the Return, is a new revision.
- A review binds by hash only. A later revision never inherits a review.

**Execution:**
- In a page, the first nonblank line of the Return section is examined. In a return file, the first nonblank line after line 1 is examined.
- `execution: claimed|running|returned|stopped` gives that state.
- A Return body of exactly `PENDING.` is `pending`.
- Anything else is `unknown (legacy)`, and is still intake-eligible.
- Eligible means `returned` or `unknown`. `pending`, `claimed`, `running` and `stopped` are not eligible.

## 4. Review binding and findings (PS-01, PS-03)

**Fields read in a Review section:**
- `reviewed_return_prefix: <64 hex>`;
- legacy `Reviewed return SHA-256: <64 hex>`, which is a whole-file hash;
- `Disposition: <text>`;
- `findings: <ID>=<resolution>; …`, with IDs matching `[A-Za-z][A-Za-z0-9-]*`.

A review source file may carry `reviewed_return_prefix:` and `findings:` lines in the same form.

**Binding:**
- A review binds to revision R when its prefix field equals R.
- A legacy whole-file hash binds to R when some file revision seen in history or among the observations has that whole-file hash and reviewable hash R.
- Otherwise the review is `unbound` and binds to nothing.

**Review state of the current revision C:**
- `reviewed`: some observed review binds to C;
- `stale-review`: there are bound reviews, but none binds to C;
- `review-needed`: no review at all.

**Findings:**
- Every `findings:` line is collected from every commit in bounded history and every observation, in page Reviews and in review_sources.
- Each is keyed by (source path, commit time order, ID).
- The latest record per ID gives the current resolution. An ID once seen is always listed.
- Open set: `unresolved`, `fix-planned`, `director-pending`.
- Closed set: `verified-fixed`, `answered-with-reason`, `decided`.
- Any other word is `unrecognized`, which needs attention.
- Passes per ID = the distinct revisions bound by the reviews that mention it.
- If history is `incomplete` or `none` for a source that has any revision, the lane reports `findings history unknown` as an attention item. The intake store is never read for findings.

**Acceptance is never computed.** `disposition` is printed verbatim, with the commit of the review it came from.

## 5. Status (read-only)

Status prints:
- the scope line: registry sha256, the lanes, and "only registered sources; no fetch";
- per repository: HEAD, the remote ref sha, `remote: last observed, not fetched`, and the ahead/behind relation (merge-base);
- the canonical record, parsed against the 0410 key set when declared.

**Conflicts**, shown with both sources and never resolved:
- canonical `waiting` or `released`, while the page for `current_work` has a return (execution `returned` or `unknown`);
- canonical `returned`, while the page's execution is not `returned` or `unknown`;
- canonical `current_work` not inside any registered page, or inside one but absent at every observed revision (two distinct messages);
- uncommitted changes under the canonical lane's registered paths while the canonical state is `waiting`;
- `published` ≠ `local` ≠ `worktree` revision of one file. Shown as `divergent` with every id; not a conflict by itself.

**Per source:** revisions; execution; review state, with the binding commit; disposition; findings (open and closed IDs, passes); intake seen or unseen per eligible revision; and a context packet `path@commit|worktree#revision_id`.

**Compact text:** observations with an identical revision are printed as one row (`published=local=worktree`). JSON keeps every observation. A bound review is cited at its latest commit; `@worktree` appears only when no committed copy exists.

**Attention:** the first item by `attention_order` (configurable), labelled `recommendation, not authority`.

**Exit codes:** 0 nothing to attend, 1 items, 2 invalid registry or tool failure.

## 6. Intake store (M01 temporary)

- `--intake <abs dir>`, supplied explicitly. It is refused when it resolves inside a Git working tree (any `.git` dir or file among its ancestors). It is created only by `ack`.
- Layout: `<store>/subjects/<id12>/0001.seen.json`.
- `subject_id` = sha256 of canonical JSON of `{"kind": "page-return" | "return-file", "repository": <name>, "path": <rel>, "revision_id": <full>}`.
- The record holds `schema: prime-intake/1`, `subject_id` (full), `subject`, `observed` (source, commit or worktree, whole sha, execution), `supersedes` (the previous eligible revision id on that path in history, or null), `by`, `at`, and `note: acknowledged as seen; not reviewed, not accepted`.
- Written with exclusive create. No other file is ever written.

**ack** requires:
- `--revision` as full 64 hex;
- the subject currently observed and eligible;
- an id12 directory that is absent, or that holds the same `subject_id`. A different id there is `refused: abbreviated id collision`.

If the same subject already holds a record by the same `by`, the result is `already-recorded`, with no write. A different `by` is `refused: conflicting acknowledgement`.

**show and status** verify every stored record: exact keys; `subject_id` recomputed from `subject`; and the directory name equal to `subject_id[:12]`. Anything else is `bad intake record`, an attention item. It is never silently dropped.

## 7. CLI

```text
python -B prime_support.py status --registry R [--intake S] [--json]
python -B prime_support.py intake scan --registry R [--intake S] [--json]
python -B prime_support.py intake ack --registry R --intake S --lane L --path P --revision <64hex> --as LABEL
python -B prime_support.py intake show --intake S [--json]
```

## 8. Limits

- A fixture lab only.
- `--as` is a label, not authentication.
- The hash binds bytes. It does not authenticate the reviewer.
- The provisional fields are not law.
- Remote state is only as fresh as the last fetch someone else made.
- No Observer fetch, no Clerk adapter, and no real store.
