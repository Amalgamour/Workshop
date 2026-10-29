# Workflow contract for one N7NN investigation

schema: colab-workflow-contract/1
status: builder contract for 0511.workflow-colab/05.01. Not shared-interface law. Not a release.

## Scope
The adapter in labs/colab-workflow-pass01 supports one caller-supplied book directory, workflow space 0, and one investigation identity at a time. Space 0 is pages 0701–0799. The door 0700.band.colabs is not a member. No other band is opened. Face 07 is not created. Filenames do not gain a .colab tail. Kernel pages 0000–0009 are not used.

The live work book D:\Git\lib-build\00.kernel\00.00.10.work is refused. Fixture books are elsewhere. The tool does not call Git, a model, or a network service. It does not reserve, capture, allocate, or repair a return. Fixture setup outside the tool may call the pinned capture helper.

## Canonical record
`<page>/investigation.json` is the only fact store. Schema `colab-investigation/1`. JSON is UTF-8, no BOM, sorted keys, separators `,` and `:`, one trailing LF. Duplicate keys refuse. Unknown keys refuse. Booleans are not integers. Non-finite numbers refuse.

Identity facts, stored once: `book`, `page`, `title`, `question`, `purpose`, `mode`, `scope`, `known_gaps`, `reasons`, `assumptions`, `reading_order`, `dependencies`, `capabilities`, `method`, `challenge`, `permissions`, `stop`, `return_shape`, `targets`.

Pass facts live under `passes` keyed by `05.NN`: `package`, `statements`, `return_pointer`, `findings`, `dispositions`, `closure`. `proposals` and `reconciliation` live on the investigation. There is no `status` field.

`<page>/seal.json` is the last file of a finished write. It stores the investigation hash and the projection hashes. It is not a second copy of the facts. A missing seal, `.write.lock`, or `partial.json` means the write did not finish. Later writes refuse with `resume refused`. The tool does not delete retained files and does not finish the partial.

## Projections
These files are regenerated from the canonical record and the retained artifact hashes. Hand edits are `projection diverges`. The tool does not repair them.

- `01.md` is the Colab brief: role and mode, purpose and question, built state and known gaps, reasons and assumptions, scope and sources, dependencies, capabilities, method, permissions and stop, return shape. Scoring is not declared. The projection says to state a qualitative result and not to manufacture a number. It does not use the law 0036 Ask line.
- `03.md` points at each target's book, page, file, section, commit label, and sha256. One file is not whole-page coverage.
- `08.md` points at each pass package digest and any return member. It does not copy the return body.
- `05.NN.md` points at the package route, recorded statements, and the return member.
- `06.md` and `06.NN.md` hold the supplied reasons and point at the package reason file by hash.

`show` prints `colab-index/1` and writes nothing, including `00.live`.

## Open request
Schema `colab-open/1`, additional properties refused. Required identity fields above, plus `schema` and `pass`. `schema` is `colab-open/1`. `book` and the text fields are non-empty and at most 4096 characters. `title` is at most 200 characters. `page` matches `^[0-9]{4}\.[a-z][a-z0-9-]*$` and the number is 0701–0799. `pass` matches `^05\.[0-9]{2}$`. `mode` is `open-design`, `hostile`, `diagnostic`, or `experiment`.

`known_gaps`, `reasons`, `assumptions`, and `reading_order` are arrays of 1 to 32 non-empty strings. `dependencies` is exactly `supplied`, `withheld`, and `unavailable`, each an array of at most 32 strings. `capabilities` is exactly `read`, `write`, `execute`, and `network`, each a string. `targets` has 1 to 32 items.

A second pass on the same page requires the same identity facts. A different identity is `occupied different content`. The same request and an existing pass is a readonly repeat. The same title on another investigation refuses. The caller selects the page. `propose` may print the lowest free number in 0701–0799 and creates nothing. Any existing file or directory whose name starts with that number occupies it. The door number 0700 is never proposed.

## Targets and the binding schema
Targets and `binding.json` follow `binding.schema.json` (`colab-binding/1`, sha256 690a0d56e590b7028dbcad8a57ffd6d6eaf20c341c016308506373d82e5c690b, 3195 bytes). The adapter implements those rules in the standard library. A schema pin mismatch refuses before use.

T ids are unique. Two targets with the same book, page, file, section, and source refuse. `section` null means the whole named file. A heading value is the exact line, including Markdown markers. Null occurrence is valid only when that line occurs once. Occurrence is 1-based. Kind `id` matches a whole line `section-id: VALUE` and no other syntax. A missing or extra match refuses. A nearby file is not a substitute.

Snapshot bytes are read from the caller `--sources` tree at `source.path` during open, and from `snapshots/<source.path>` during attach. The sha256 must match. The commit is a stored label. The repository string is a stored label. Local paths are not recipient access.

## Package digest
Algorithm `colab-package-digest/1`. The preimage is UTF-8:

```text
colab-package-digest/1
request <sha256> <bytes>
binding <sha256> <bytes>
file <relative-path> <sha256> <bytes>
```

`request` is the raw `request.json` bytes. `binding` is the raw `binding.json` bytes. Each other file except `verification.json` is one `file` line, sorted by relative path using `/`. The preimage ends in one LF. The digest is the sha256 of that preimage.

`verification.json` schema `colab-package-verification/1` repeats the digest, both hashes, and every package file except itself, including `request.json` and `binding.json`. It is retained and is not inside the preimage. The preimage still uses the `request` and `binding` lines for those two files and `file` lines for the rest. The caller's `--expect-digest` must equal the recomputed digest and the verification digest. A difference is `stale expected hash` or `conflicting bytes`.

Required package files: `request.json`, `binding.json`, `ENTRY.md`, `RETURN-TEMPLATE.md`, `source-manifest.json`, `verification.json`, `<pass>.md`, `06.NN.md`, and one snapshot per target. `ENTRY.md` carries the brief headings listed for `01.md`. `RETURN-TEMPLATE.md` carries Question, Evidence, Hostile, Factfind, Overflow, Unprompted, and Qualitative result, and the line `Do not manufacture a number.` The line `Scores first. Opinion second.` refuses in those two files and in projections. Package paths are relative, have no `..`, and are plain files. Links and junctions refuse. At most 64 files, each at most 262144 bytes.

Attach copies those bytes under `artifacts/<pass>/` and does not modify the supplied directory. The same digest and the same bytes are a readonly repeat. The same pass with other bytes refuses. Binding book, page, and pass must equal the investigation. Package targets must equal the stored targets. A draft in that folder is still a draft.

## Statements, findings, dispositions
A statement is `release`, `claim`, or `review`, with non-empty `by`, `on` (`YYYY-MM-DD`), and `text`. Any other kind is `claim/release unknown`. The record marks `authority` as `recorded-statement`.

A finding is caller-supplied: `id` (`^F[0-9]{2}$`), `topic`, `observation`, `affected_page`, `affected_file`, `target`, `consequential` boolean, `evidence_kind`. Ids are unique. `target` must exist. The same list is a readonly repeat. A different list refuses. The tool does not judge the observation.

A disposition is caller-supplied: `finding_id`, `reviewer`, `action`, `reason`, `director_reply`, `director_reply_ref`, `followup_ref`, `park`, `source_binding`. `action` is `accepted`, `rejected`, `held`, `deferred`, or `answered`. `held` requires `followup_ref` or `park`. `director_reply` is stored text and is not executed. Every id is one of the findings. The tool does not judge adequacy.

A proposal is caller-supplied text stored on the investigation and projected under `proposals/`. It names the finding, the affected page and file, and the target. It is not written to the subject page. A consequential finding needs a proposal before close.

Closure is a supplied object `explicit` true, plus `by`, `on`, and `text`. Close refuses unless every finding has one disposition, every consequential finding has a proposal, and no target is blocked for reconciliation. An accepted disposition without closure is not completion. A rejection remains in the record.

## Reconciliation
`check-subject` hashes a caller-supplied current file and writes nothing. A mismatch can be recorded with `flag-reconciliation`. The stored target hash stays. Dispositions and close for that target refuse while the flag is `blocked`. `retain-historical` records the caller's reason, keeps the old hash, and clears the block. `retarget` refuses.

## Return pointer
Pins, then launch, no timeout, shell false, `python -B`:

- `return_capture.py` sha256 8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac, 45767 bytes.
- `return_inspect.py` sha256 947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b, 11402 bytes.

A pin mismatch refuses and does not launch. Inspect must be `complete` and verify must exit 0 with the lines `result complete`, `not approved`, `not accepted`, `not published`. The receipt hashes must agree. Origin `book`, `page`, and `batch` must equal the investigation book, page, and pass. Any other origin refuses, including a subject page or an implementation page. Reserved, missing, incomplete, and refused inspections are partial custody and are not stored. Two non-retrospective complete matches require `--member`. A retrospective match is stored only with `--member` and `--secondary`, and only when no non-retrospective match exists. The same member and receipt are a readonly repeat.

## Derived flags
Computed by the reader. Not stored.

- `draft`: closure is null.
- `custody_complete`: the pointer is a complete non-conflicting observation.
- `review_pending`: no review statement, or the latest review text is `PENDING`.
- `held_followup`: a disposition action is `held`, or a followup or park is set.
- `accepted_without_terminal`: a disposition action is `accepted` and closure is null.
- `explicit_completion`: closure is present.

More than one flag may be true. None of them approves, accepts, or publishes the work.
