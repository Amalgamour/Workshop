# Task-agreement reference contract — specification v3 (0707/05.15)
who: claude-opus-5-5 · state: **PROPOSAL.** It supersedes `design05.14/SPEC.md` (preserved). Reference lab: `labs/task-agreement-reference-pass02/ta2.py`. **Everything in design05.14 §1–§9 still holds unless changed below** (passive resolver; references-only block; immutable bindings; semantic findings attributed; whole-record plus cut context).

## Changes in v3
### J1 — a bounded Markdown grammar (applies to heading cuts, block extraction and the pack cut)
- **A fence opens** with 0–3 spaces of indent, then 3 or more backticks or 3 or more tildes. A backtick fence's info string may not contain a backtick.
- **It closes** with 0–3 spaces of indent, the **same** character, a length **≥** the opener, and nothing but spaces or tabs after. A shorter run inside is content (a four-backtick fence encloses triple-backtick lines).
- **An unclosed fence is refused** before any heading or cut is selected. It is never silently run to the end of the file.
- **A heading target** is exactly `## <text>` at column 0, outside every fence. A line with 1–3 spaces of indent whose text equals a cited heading is **refused as ambiguous**, never selected. Setext headings and HTML blocks are not targets.
- **The task block** is the fence whose info string is exactly `task-agreement`; there must be exactly one.
- **The pack cut** ends at the first **real** `## Return pointer` (outside fences).
- **Raw bytes are kept.** Line endings are detected per line (LF and CRLF); nothing is normalized.

### J2 — revalidate bindings on every entry
- `inspect`, `compare` and `reconcile-request` validate before reading any source:
  - the schema `task-agreement-binding/2` (other versions are refused, with a "re-bind" hint);
  - the required keys and types;
  - the page and pass formats;
  - `pack.path ∈ {page/pass.md, page/pass.pack.md}`;
  - a `self` ref names the pack path with `record_basis: pack-cut`; `record_basis` on any other ref is refused; a non-self path must match its source;
  - `kind ∈ {whole, heading}` (a heading needs text);
  - the hash formats;
  - the book instance (compare and reconcile).
- **One checked resolver** handles every path: book-relative `/` paths only, with absolute paths, drive paths, `..`, backslashes and link or reparse ancestors refused, then a containment check. **It runs before any read.**
- **`raw_cut_b64` is history only;** it is never treated as current bytes. A path-instance hash match is **not authentication.**

### J3 — the lab output room
- `construct`, `assemble`, `bind` and `reconcile-request` require `--lab-root`. The room must:
  - exist as an ordinary directory;
  - have no link or reparse point in its ancestors;
  - have **no `.git` or `00.kernel` marker** in any ancestor, so it is never inside a checkout or book tree.
- **The output must:**
  - resolve strictly inside the room (a sibling-prefix such as `lab2` is refused);
  - not lie inside the source book;
  - have no link ancestor;
  - **not exist.**
- **All of this is checked before any directory or file is created.** `inspect` and `compare` need no room and write nothing.
- **This is a lab guard, not OS confinement.** A production host must enforce its own write scope.

### Compatibility — profile `core-measured-agreement-v1`
- **Opt-in** (`--profile core-measured-agreement-v1`) and only when the block is absent.
- It records the **exact** observation of the frozen core helper (`labs/workbook-review-pass01/workbook.py`, sha256 60e040fa…, 79131 bytes) as `legacy_observation`, with the helper identity.
- **How it observes:** the helper's six definitions are extracted by AST and executed in a clean namespace; **no module import.** The page is decoded exactly as the core does (`decode("utf-8", "replace")`).
- **Field states** become `observed-legacy` with provenance `profile:core-measured-agreement-v1`. **No decision pairing is created** from a Director-verbatim section, and nothing becomes a new grant.
- **Observed helper behavior** (`COMPAT.md`) is reported, not changed.
- The pass01 exact-heading profile is kept for compatibility, but **superseded by this one for core parity.**

## Unchanged guarantees (do not regress)
- the passive policy (`policy: "passive"`) and no holds table;
- semantic conflicts only as attributed findings;
- immutable bindings, with new evidence giving a new binding;
- no hash in the block;
- whole-record plus cut context (`context-changed`);
- self references measured on the pack cut;
- distinct verbatim and interpretation cuts;
- `none-recorded` with its "not proof" limit;
- instance separation;
- the exit codes 0, 1 and 2.
