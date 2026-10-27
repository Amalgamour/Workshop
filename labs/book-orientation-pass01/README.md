# Book orientation checker, pass 01

**batch:** `00.kernel/00.00.10.work/0502.workflow-start/05.02.md` (released by the Director, 2026-10-26)
**who:** claude-opus-5-5, Colab · **state:** read-only development tool. Not a contents writer, not an authority; findings are advisory.

## What it checks

`check_book.py` compares a book's declared contents face with that book's **published Git tree at one commit**.

1. **The commit:** `--revision` is resolved once to a SHA. All reads use `git ls-tree` and `git cat-file` at that SHA, with `GIT_OPTIONAL_LOCKS=0`. The working directory, the index and untracked files are never read.
2. **The contents face:**
   - **By default:** the one named by the book's `00.md` in this book's documented local sentence form, `contents in <path>.` There must be exactly one; the path is book-relative, under `0011.contents/`, and ends in `.md`.
   - **With `--contents <path>`:** a named candidate instead, reported as chosen on the command line.
   - There is no fallback and no highest-version rule.
3. **Covered:**
   - Pages table rows: page folders; direct files; direct subdirectories with their recursive tracked-file counts.
   - The `Book files:` list.
   - The `## Other books` paths: every one in the section, resolved relative to the book root, lexically, inside the repository; each must be a blob at the commit.
4. **Not covered:** other prose and links, face contents, whether a page should be published, and anything local.

**Exit codes:**
- **0:** clean;
- **1:** findings;
- **2:** invalid input, unsupported structure, or tool failure, with a reason.

## Supported contents structure

The one that `labs/bootstrap-establish-pass01/write_contents.py` writes:

```text
## Pages

| Page | Faces and files |
|---|---|
| `PPPP.title` | `file`, `dir/` (N files), ... |

Book files: `00.md`.

## Other books
Label: `relative/path`. Label: `relative/path`. ...
```

Any other shape inside these sections is refused as unsupported, never passed.

**Other books, the complete section** (pass 02, batch `0502.workflow-start/05.03`, finding OR-01):
- **Bounds:** from the heading to the next Markdown heading line (`#` to `######`, then a space) or the end of the face. Nothing after that next heading is read.
- **Heading:** exactly `## Other books`, at most once. A second one, or a variant in case or spacing such as `## Other Books`, refuses.
- **Lines:** each nonblank line holds one or more items ``Label: `path`.``, joined by single spaces. Label is a capital letter, then letters, with single spaces between words. Blank lines are allowed. More than one line is allowed.
- **The one sentence:** `Each lists what it holds.` is accepted once, after a single space, at the end of the section's last nonblank line. It is the sentence `write_contents.py` emits, so it is the only non-item text the section may hold.
- **Everything else refuses** with exit 2 and names the line: same-line text that is not an item, a comma separator, a missing period, trailing whitespace, a bare path, a prose line, or the sentence anywhere else. Pass 01 read only the first line and dropped text between items, so such faces could pass as clean.

## Run

```text
python -B check_book.py --root D:\Git\lib-build --revision a5853b7 --book 00.kernel/00.00.10.work
python -B check_book.py --root D:\Git\lib-build --revision a5853b7 --book 00.kernel/00.00.10.work --contents 0011.contents/01.002.md
python -B check_book.py --root D:\Git\lib-build --revision 15b9cceb3438b8a91acfd8d3155b9b0d5fce29ae --book 00.kernel/00.00.10.work --json
python -B -X dev tests/test_check_book.py -v
```

The tests (17 since pass 02) build disposable Git repositories under `scratch/tests/` (ignored by this lab's `.gitignore`), with per-command identity variables only.

## Limits

- **A clean result** means only that "the selected contents describe the published tree at this commit".
- **The pointer form** is this book's provisional local format, not kernel grammar.
- **Other-books paths** are resolved relative to the book root, which is write_contents.py's convention. Read relative to the contents face itself, they would not resolve.
- **Tree layout:** a tree with two folders sharing a page number is reported (`duplicate-page-number-in-tree`). Pages nested deeper than one level are not modelled.
