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
   - The `## Other books` paths, resolved relative to the book root, lexically, inside the repository; each must be a blob at the commit.
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

## Run

```text
python -B check_book.py --root D:\Git\lib-build --revision a5853b7 --book 00.kernel/00.00.10.work
python -B check_book.py --root D:\Git\lib-build --revision a5853b7 --book 00.kernel/00.00.10.work --contents 0011.contents/01.002.md
python -B check_book.py --root D:\Git\lib-build --revision 15b9cceb3438b8a91acfd8d3155b9b0d5fce29ae --book 00.kernel/00.00.10.work --json
python -B -X dev tests/test_check_book.py -v
```

The tests build disposable Git repositories under `scratch/tests/` (ignored by this lab's `.gitignore`), with per-command identity variables only.

## Limits

- **A clean result** means only that "the selected contents describe the published tree at this commit".
- **The pointer form** is this book's provisional local format, not kernel grammar.
- **Other-books paths** are resolved relative to the book root, which is write_contents.py's convention. Read relative to the contents face itself, they would not resolve.
- **Tree layout:** a tree with two folders sharing a page number is reported (`duplicate-page-number-in-tree`). Pages nested deeper than one level are not modelled.
