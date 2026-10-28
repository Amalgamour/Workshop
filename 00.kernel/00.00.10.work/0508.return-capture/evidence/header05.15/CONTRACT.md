# CONTRACT — initial header boundary (0508.return-capture 05.15)

Recorder: Grok Builder 2. Date: 2026-10-28.
This contract is written before the repair code. It corrects BO-05. It does not replace the captured bytes in `0138.batch-reader-0513` or `0140.batch-reader-repair-0514`. The reader remains `batch-observation/1`. It still grants no release, acceptance, closure, or seat. `parse_source` stays the pinned file and its object is copied unchanged.

## 1. Initial header

`document.header_state_raw` is filled only from eligible `state:` lines. An eligible line is outside fences, outside blockquotes, and inside the initial header.

The initial header is:

- every unfenced, unquoted line before the first unfenced, unquoted heading
- and, when that first heading is a level-1 title, the unfenced, unquoted lines after that title until the next unfenced, unquoted heading

That next heading is the body boundary. A level-2 title that starts with `Assignment` opens Assignment. A level-2 return-family title opens the return scope. Any other heading, including a later level-1 title, opens other. Header mode does not resume after the boundary.

A heading inside a fence is not a title and is not a boundary. A blockquote is a line whose text after leading spaces or tabs starts with `>`. A quoted title and a quoted `state:` line do not enter the header fields and do not move the boundary.

The fence rule is unchanged, including a longer outer fence around a shorter inner fence.

## 2. What stays

Assignment and return scopes are unchanged. One eligible line is the raw value. Zero lines leave the raw value null. Two or more leave the raw value null, keep every line with its original line number, and mark the field ambiguous. The first line is not selected.

No state is invented when the header has no `state:` line. The raw text is not rewritten into a closed vocabulary. `Release:` and `Release and claim:` are not merged. A page that carries both stays `duplicate-release`.

Declaration refusal, the pinned legacy channel, live UTC timestamps, git-blob times left null, and custody roles stay as they are. `package_at_commit` stays `not-established`. A typed declaration stays unauthenticated. Review binding stays unbound.

## 3. Regressions

The suite keeps the prior declaration, fence, source, and custody cases. It adds a normally shaped title, stamp, Assignment, and Return page; a leading fence with a false header; a title-free page; duplicate header state; a quoted title; a later body title; and a nested fence. The sixteen corpus pages each assert the one eligible `state:` line and its line number against the blob at `4cca1d2e9ac845e82a2d44df432f8f7f6584f1e5`. The live `05.14` page is read as a worktree file. Its `state: draft` on line 5 stays, and its assignment and return-pointer lines stay. That read is not reported as a git blob.

## 4. Limits

This repair writes the reader lab, `06.16.md`, `evidence/header05.15/`, and the `05.15` return pointer only. It does not edit captured members, the corpus, historical pages, the parser, the adapter, the inspector, the helper, or the state-projection lab.
