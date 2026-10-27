# DESIGN.003 — PSI-01 and PSI-02 corrections (0507.prime-support 05.03)

Author: claude-opus-5-5. Date: 2026-10-27.
Additive to `../build05.02/DESIGN.002.md`, which stays unchanged. This file replaces only the parts of DESIGN.002 §4 it names. Every field is still a provisional fixture contract.

## 1. Binding before use (PSI-01; replaces "Binding" in DESIGN.002 §4)

Each review item is collected raw, with:
- its source: `path@commit`, or `path@worktree (uncommitted draft)`;
- its declared target;
- its fields.

Its status is decided afterwards, against the target's **known revisions**: the revision ids of the target path seen in bounded history or among the observations.

| Item | Target | Valid when | Otherwise |
|---|---|---|---|
| page Review section | its own page | `reviewed_return_prefix` ∈ known revisions; or the legacy `Reviewed return SHA-256` equals the whole-file hash of an observed version of that page | `unknown-hash` or `invalid-legacy` |
| review source | the `reviewed_return_path:` line, which must be a registered page or return file of the same lane | the same rules, applied to that target | `invalid-target`, or the above |
| anything with no binding line | — | never | `unbound` |

Effects:
- Only **valid** items change a finding, count a pass, give a revision the state `reviewed`, or supply a disposition.
- An `unknown-hash`, `invalid-legacy` or `invalid-target` item, or an `unbound` item that carries findings or a disposition, becomes an `invalid-review` attention line. That line keeps the source, the hash it named, and its finding text.
- The last valid finding state is unchanged by it.
- A target is never inferred, and nothing is read from disposition prose.

**Finding identity** is `(target path, ID)`, and the report key is `<target path>#<ID>`. The same ID on two returns is two findings.

## 2. Causal order (PSI-02; replaces "latest record wins")

- **Committed records.** For one finding, the records are `(commit, resolution, source, bound revision)` taken from every valid committed item. The **frontier** is the set of records whose commit is not an ancestor of another record's commit, tested with `git merge-base --is-ancestor`.
  - Commit and author dates are never consulted.
  - `git log --topo-order` orders history for `supersedes`.
- **The finding's state:**
  - **One resolution on the frontier** gives that resolution's state: `open`, `closed` or `unrecognized`.
  - **More than one** gives the state `conflict`. Every frontier record is listed, and a `conflict` attention item is raised. There is no timestamp, registry-order or lexical winner. Two sources at one commit that disagree are also a conflict.
- **Uncommitted drafts.**
  - A worktree file whose bytes equal HEAD's is the same observation and is not read again.
  - A differing worktree file is a draft. Its resolutions go in `draft` and never replace the committed state.
  - A draft that differs from the committed resolution is a `conflict` attention item, "draft differs from committed".
  - A finding seen only in a draft has state `draft-only`.
- **Passes** = the distinct bound revisions among the committed valid records. Repeated copies of one review across commits, or an identical worktree, add nothing.
- **Review dispositions** for a reviewed revision come from the frontier of its valid committed reviews. Incomparable different dispositions are shown joined and raised as a conflict.

## 3. Unchanged

- Read-only operation and the git allowlist.
- History `incomplete` and `none` reporting.
- The intake store as acknowledgements only.
- The PS-01 boundary and the PS-02 return files.
- Exit codes.
- Attention order, with one new kind `invalid-review`, placed after `bad-intake` by default.
