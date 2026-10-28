# CONTRACT — batch-observation-pass01 (0508.return-capture 05.13)

Recorder: Grok Builder 2. Date: 2026-10-27.
This contract is written before the lab code. It is a read-only observation contract. It is not a seated schema, a workflow, a parser change, or a closure rule. SP-01 through SP-04 from prime-review05.11 override the provisional `batch-observation/1` sketch in the 05.11 state proposal wherever they differ. The field families stay compatible with that sketch: source identity and kind, the exact legacy observation, sections and raw fields, pointer candidates, custody observations and roles, review text, and ambiguities.

Standard library only. The lab does not import the state-projection lab and does not write a projection.

## 1. Command and exits

```text
python -B batch_observe.py observe --json
    (--repo REPO --commit HEX40 --path REL |
     --repo REPO --live --path REL |
     --supplied FILE [--path REL])
    [--members-book ABS] [--declaration FILE]
```

| exit | meaning |
|---|---|
| 0 | one observation, with empty `ambiguities` and empty `attention` |
| 1 | one observation, with one or more ambiguities or attention items |
| 2 | refused before an observation is emitted |

- UTF-8 JSON on stdout, one document, trailing newline. Refusals leave stdout empty and write the reason on stderr.
- The tool writes no file, store, registry, book, or Git object.
- `--json` is required. There is no Git executable override, no parser path override, no schema switch, and no version scan.
- `--commit` is 40 lowercase hex. An abbreviation is refused.
- `--path` is a relative path with no `..`, no backslash, and no colon. It is contained. It is not a command.
- `--repo` with `--commit` reads a Git blob. `--live` reads the worktree file at `--path` and does not call Git. `--supplied` reads the named file. The three modes are mutually exclusive. Supplied and live bytes are never labelled as a Git blob.
- `--path` on a supplied file is an identity label for page parsing. It does not cause a Git read.
- `--members-book`, when present, is the only book passed to the inspector. The tool does not crawl a band.

## 2. Pins, checked before use

| file | SHA-256 | bytes |
|---|---|---|
| `labs/prime-support-pass01/prime_support.py` | `700d60d2e49c186d49e56a9a38058e21a722b4a5dd79d461453a305e8d904f70` | 59791 |
| `labs/prime-support-pass01/clerk_adapter.py` | `2f30ba751f78ec9f7d2995739bebde0e3b6509eeab35ae29a9078385ff33f8d4` | 11774 |
| `labs/return-capture-pass01/return_inspect.py` | `947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b` | 11402 |
| `labs/return-capture-pass01/return_capture.py` | `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac` | 45767 |

The parser and its sibling are checked before `parse_source` is imported and before Git runs. The inspector and helper are checked before any inspect launch, and only when `--members-book` is set. A mismatch exits 2 and launches nothing.

Git, when used, is only `git -C REPO rev-parse --verify --end-of-options COMMIT^{commit}` and `git -C REPO cat-file -t|-blob --end-of-options OBJECT`. No shell. No network command. No write command.

## 3. Output `batch-observation/1`

```text
{schema, tool: {name, path, sha256}, authority,
 source: {kind, repository, path, commit, sha256, bytes, label},
 page: null | {book, page, batch},
 document: {header_state_raw},
 assignment: {executor_raw, release_raw, claim_raw},
 legacy: {tool, sha256, sibling, sibling_sha256, kind, status, reason,
          revision_id, execution, whole, review},
 channels: {legacy, inventory, revision_repaired},
 sections: [{line, level, title, form, fenced, text}],
 fenced_headings: [{line, title, text}],
 pointers: [{line, form, title, execution_raw,
             members: [{name, line, receipts: [{sha256, line}]}]}],
 assignment_mentions: [{member, line, form}],
 custody: {basis, members_book, package_at_commit, primary, primary_rule,
           observations: [{member, how_named, stated_receipts, inspection, exit,
                           role, commit_receipt_sha256, commit_receipt_present,
                           receipt_bytes_match, attention}]},
 review: {parser_object, sections: [{line, title, text_raw}], text_raw,
          legacy_hashes: [{hash, equals_whole, equals_revision}],
          binding, typed_declaration},
 ambiguities: [CODE], attention: [CODE]}
```

- `authority` is `none`.
- `channels.revision_repaired` is false. A refused legacy parse keeps `revision_id` null. This tool does not invent a repaired revision.
- `legacy.review` is the `parse_source` review object or null. It is not rebuilt when the parser returns before a review object.
- `package_at_commit` is `not-established`. A matching committed `receipt.json` blob is recorded as `receipt_bytes_match` and does not prove the rest of the package.
- There is no `lifecycle`, `accepted`, `closed`, `ready`, or `completed` field. Review prose and a typed disposition stay inside their source fields.
- `binding` is `unbound`.
- `page` is parsed only from a relative path `…/{book}/{page}/05.NN.md`. The book label is the directory named immediately above the page directory.

Heading forms, outside fences, level 2, using the same fence rule as `parse_source`:

| title | form | members collected |
|---|---|---|
| `Return` | `return` | yes |
| `Return — …` | `return-em` | yes |
| `Return pointer` | `return-pointer` | yes |
| `Return pointers` | `return-pointers` | yes |
| `Return archive pointer — …` | `return-archive-pointer` | yes |
| `Review` / `Review — …` | `review` / `review-em` | no; raw text is kept |
| any other title whose casefold starts with `return` or `review` | `other-return-family` or `other-review-family` | no |

Fenced return and review headings are listed in `fenced_headings` and are not pointers. A line `NNNN.name captures` outside a fence is an assignment mention. It is not inspected and it is not a primary. Names in other prose, including inventory faces, are not members.

Pointer members are read only from the pointer body, and never from a `Release:` line. The observed spellings are `Member: NAME` with a later `Receipt` hash, `Member NAME` on an execution line with `Receipt sha256 HASH`, and, in an archive-pointer body only, a backticked member id. The receipt is the first 64-hex value after the word `Receipt` on that line. An archive id with no receipt is recorded with an empty receipt list. A quoted release instruction is not a pointer.

`how_named` is `pointer`, `archive-pointer`, `recognized-return`, or `assignment-sentence`.

## 4. Custody roles

Inspection runs only for members named by a collected pointer. The launch is `[sys.executable, "-B", return_inspect.py, "inspect", "--book", members_book, "--member", NAME, "--json"]`. The stored `inspection` is that JSON object when it is schema `return-capture-inspection/1`, the member matches, and the exit matches the status. Otherwise the role is `observation-failed` and no origin is invented.

| condition | role |
|---|---|
| no members book, pointer member | `not-observed` |
| assignment sentence only | `assignment-mention` |
| status `missing`, `incomplete`, `reserved`, or `refused` | that status |
| origin book differs | `cross-book-origin` |
| origin book, page, and batch match, retrospective true | `same-page-retrospective` |
| origin matches, retrospective false, exactly one such complete member | `primary-current-candidate` |
| origin matches, retrospective false, more than one such complete member | `ambiguous-primary-candidate` |
| origin differs, retrospective true, book matches | `secondary-historical` |
| origin differs, retrospective false, book matches | `origin-mismatch` |
| page path has no book/page/batch | `page-unidentified` |

`primary` is the single `primary-current-candidate`, or null. Pointer order does not choose it. A same-page retrospective member is not a primary. A stated receipt that differs from the live receipt stays in `stated_receipts`; the live hash stays in the inspection. The difference is attention `stated-receipt-differs`.

Live inspection is `custody.basis: live`. It does not change `source.kind` or the legacy parse of the commit blob.

## 5. Review text

- Copy the parser review object when `parse_source` produced one.
- Keep the raw body of each unfenced review section even when the parser refused the file.
- A `Reviewed return SHA-256` value is compared with the current whole and the current `revision_id` only. A mismatch is `legacy-hash-not-current`. No history search is done. Equality still leaves `binding` unbound.
- The word `Accepted` in review text is source text. It does not set a judgement.
- `--declaration` accepts only schema `batch-review-declaration/1` with keys `schema`, `reviewed_member`, `reviewed_receipt_sha256`, `reviewed_disposition` (`accepted`, `held`, or `returned-for-correction`), and `reviewer`. Any other schema is an unknown version and exits 2 before Git or inspect. A valid declaration is stored with `authority: not authenticated` and does not change `binding`.

## 6. What this lab does not do

It does not edit the parser, the sixteen pages, the corpus, or the projection lab. It does not reserve, capture, repair, ack, or publish. It does not infer completion. It does not treat a fixture or a typed label as Director release.
