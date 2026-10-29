# CONTRACT — review-packet-pass01

Builder spec for one mechanical packet. This file does not accept the lab.

## Tool

labs/review-packet-pass01/review_packet.py uses the Python standard library.
Command:

```text
python -B labs/review-packet-pass01/review_packet.py assemble --request REQUEST.json
```

Exit 0 means the output directory holds a finished packet.
Exit 2 means the request was refused before that directory existed, or the assembly stopped partial after creating it.
A finished packet may still record custody as complete, reserved, missing, incomplete, or refused.

The interpreter named in the request runs the pinned inspector and helper.
The assembler does not import those modules. It hashes them and then uses a subprocess argument array, python -B, shell false.
Helper sha256 8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac, 45767 bytes.
Inspector sha256 947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b, 11402 bytes.
A pin mismatch refuses the request and does not start the process.
The assembler never calls capture, reserve, or any other helper command.

## Request

Schema review-packet-request/1. JSON object, no duplicate keys, no nonfinite numbers.
Exact keys: schema, book, member, origin, repo, python, inspector, helper, output, bounds, sources.

book, repo, python, inspector, helper, and output are absolute paths.
A path part `..` is refused. An ancestor that is a link or junction is refused.
output must not already exist, must not lie inside the named member, and must not lie inside a `.git` directory.
The parent of output must exist and be a regular directory.

member matches `^(\d{4})\.([A-Za-z0-9][A-Za-z0-9._-]{0,63})$`.
origin has exact keys book, page, pass. pass matches `^05\.\d{2}$`.

bounds has exact keys max_sources, max_source_bytes, max_total_bytes, max_output_bytes.
They are integers, not booleans.
max_sources is 0 through 64.
max_source_bytes is 1 through 2000000.
max_total_bytes is 1 through 8000000 and is at least max_source_bytes.
max_output_bytes is 1 through 12000000.
sources is an array no longer than max_sources.

Each source has a unique id matching `^[a-z][a-z0-9-]{0,31}$` and a role:
builder-claim, custody, director-quotation, or supporting.
kind is git-blob, live, or member-file.

A git-blob source has commit (40 lowercase hex) and path (repo-relative, no backslash, no colon, no `..`).
expect_sha256 is optional. artifact_manifest is optional.
The bytes come from `git cat-file blob`. A missing commit or blob stays absent.
The live work tree is not opened for that source.

A live source has path and embed (boolean). expect_sha256 and artifact_manifest are optional.
embed true copies the file into the packet. embed false records sha256 and length only.
A link is refused before the output directory is created.

A member-file source has name. Allowed names are return.md, receipt.json, manifest.json, reservation.json, and payload/NNNN.blob with four digits.
The file is read only under the named member. An absent file stays absent.
A work-page file is not substituted. expect_sha256 and artifact_manifest are optional.

Unknown keys are refused. Malformed JSON and duplicate keys are refused.
No declared source is executed.

## Custody

The inspector command is:

```text
python -B INSPECTOR inspect --book BOOK --member MEMBER --json
```

The helper command is:

```text
python -B HELPER verify --book BOOK --member MEMBER
```

Stdout is stored exact. The verify text is evidence. It is not parsed into an acceptance decision.
When the inspector JSON has a reservation origin, book, page, and batch are compared with the requested book, page, and pass.
A mismatch is an origin conflict. The assembler does not rewrite the request or the member.
Timeout is 60 seconds. There is no retry.

The packet always records acceptance, approved, published, seated, and authority_inferred as false, semantic_review as false, and next_task as null.
The fixed statement is: "A verified receipt is custody, not acceptance. Return claims remain claims even when a hash matches. These checks are not an OS sandbox or a same-user race guarantee."

## Artifact checks

artifact_manifest has exact keys compare_commit and compare_live.
compare_commit is a 40-hex commit or null. compare_live is boolean.
The source bytes are parsed as JSON. The check runs only when schema is exactly artifact-manifest/1 and artifacts is an array.
Any other schema, including prime-entry-pin-artifact-manifest/1, is unsupported-schema. Rows are not interpreted.
Top-level keys other than schema and artifacts are named and not interpreted.

Each row needs path, sha256, and bytes. Optional commit overrides compare_commit for that row.
Other row keys are named and not interpreted. A row that lacks the required fields is row-rejected.
Historical bytes are the git blob at the row commit. Live bytes are a separate hash of the work-tree file.
Classifications:

- historical-match: the git blob matches the declared sha256 and length, and live was not requested or live matches too
- changed-live-working-copy: the git blob matches and the live file exists with different bytes
- live-absent: the git blob matches and the live path is absent
- historical-mismatch: the git blob is present and does not match the declaration
- historical-absent: the git blob is absent; a live file is not used in its place
- live-match: no commit was requested and the live file matches the declaration
- live-mismatch: no commit was requested and the live file differs
- row-rejected: the row or its path is unsafe or incomplete

The output does not use the word corruption. Row file contents are not written into the packet.
A live or historical file larger than max_source_bytes is oversize and is not copied.

## Output

Inside the new directory:

- custody.json, the inspector stdout, and custody-stderr.txt
- helper-verify.txt and helper-verify-stderr.txt
- sources/NNNN-ID.blob for each embedded source, in request order
- packet.json, schema review-packet/1
- PACKET.md
- manifest.json, schema review-packet-manifest/1, binding those files by sha256
- assembly-status.json, schema review-packet-assembly/1, written last

PACKET.md has these headings, in order: Custody observation; Builder-reported claims; Artifact checks; Absent, conflicting, and unverified; Director quotations; Limits.
It identifies snapshots and checks. It does not replace them with a semantic summary.
Builder-reported claims, custody observations, artifact checks, and absent or conflicting material stay in those sections.
A director-quotation source is named there, and the section says the bytes do not confer authority.

Gathered source bytes count against max_source_bytes and max_total_bytes.
Written file bytes count against max_output_bytes. Nothing is shortened to fit.
If a bound is crossed after the directory exists, existing files stay, a partial status is written when it fits, and the process exits 2.
A second run sees an occupied destination and does not modify it.
These checks are not an OS sandbox or a same-user race guarantee.

## Specimens

The 0164 request names member 0164.prime-entry-pin-repair-0503, page 0512.prime-review, pass 05.03.
It allowlists the sealed return, receipt, manifest, and reservation, the pinned prime-entry-pin artifact manifest as a live file, and the director-agreement file as a director quotation.
The artifact check on that manifest must come back unsupported-schema.

The 0163 request names member 0163.prime-bench-harness-0501, page 0513.bench-build, pass 05.01.
It allowlists the sealed return, receipt, manifest, and reservation.
It requests the artifact manifest as a git blob at 749cfd9c670fe77fbedd232c2630f98b0529025d and checks artifact-manifest/1 rows there, with live hashes and without embedding those row files.
It also requests the same path at 80f7025425d7bb3fdcf3b0ee56057cd6d8b6b9fe, which is absent, and does not replace it with the live file.
The 0164 packet.json and PACKET.md are the copies nominated for capture.
Both specimen directories remain under evidence/build05.01/.

## Non-goals

No model, API, credentials, install, worker, routing, or acceptance decision.
No Git stage, commit, or push of this workspace.
No edit of the pinned helper, the pinned inspector, or another lane.
