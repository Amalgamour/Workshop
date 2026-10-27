# return-capture-pass01

Schema `return-capture/1`. Local capture of one submitted return. Python standard library only.

A receipt says the copy finished and the hashes match. It does not approve, accept, seat, publish, or finish the work. Prime review and Git publication are later, separate facts. Publication copies sealed bytes. It does not rewrite `receipt.json` and it does not store its own commit hash there.

`return_capture.py` reserves, captures, and verifies. It does not dispatch the app, launch a worker, call a model, or choose a route. Labels and the recorded release string are stored text. They grant no authority.

`demo.py` and `inventory.py` are separate. They may read Git. The capture tool does not import a process runner, a shell copy helper, or a database.

## Commands

```text
python -B return_capture.py reserve --book BOOK --submission ID --name SLUG \
  --origin-book BOOK --origin-page PAGE --origin-batch 05.NN \
  --expected-output LOGICAL --submitter LABEL --reviewer LABEL --release TEXT \
  [--supersedes 01NN.slug]
python -B return_capture.py capture --book BOOK --submission ID \
  --return-file ABS --source-root ABS --artifact REL|LOGICAL \
  [--retrospective] [--source-commit HEX] [--return-includes-prime-review]
python -B return_capture.py verify --book BOOK --member 01NN.slug
```

`--book`, `--return-file`, and `--source-root` are absolute. Reserve and capture require a plain book directory. The book may be an ordinary directory inside a local Git checkout, including the checkout root and a linked worktree whose `.git` entry is a file. There is no flag that treats that path as an exception. The book may not be a filesystem root, a path with a `.git` component, or anything inside a Git control directory. The helper does not invoke Git and does not write Git metadata. Verify only reads. It may read a sealed package that already sits in a checkout. It still does not write.

Exit 0 is a completed reserve, an idempotent reserve, a completed capture, an idempotent capture, or a verified receipt. Exit 2 is a refusal, a conflict, a partial package, a missing input, a full band, or a failed verify. Argument syntax errors use the process exit 2 and standard error.

## Member

Members are siblings of `0100.band.returns`, numbered `0101` through `0199`, folder `01NN.slug`. The door is not a member. Any existing directory or file whose name begins with one of those numbers is taken, including drafts and temporary names. The lowest free number is used. A full band stops. The tool does not create `0200`.

```text
01NN.slug/
  01.md
  reservation.json
  return.md
  manifest.json
  payload/0001.blob
  receipt.json
```

`01.md` is an index written once at reserve. It tells a reader to verify `receipt.json`. It is not a completion status. Later prose edits do not complete a package. Capture does not rewrite it.

`reservation.json` keys, exactly: `schema`, `kind`, `submission_id`, `origin`, `destination`, `expected_outputs`, `submitter`, `reviewer`, `release`, `supersedes`, `reserved_at`. `kind` is `reservation`. `origin` is `book`, `page`, `batch`. `destination` is `member`, `name`, `path`. `path` is the folder name. `supersedes` is null or an existing member folder. The old member is not edited.

The same submission id and the same reserve fields return the existing reservation and write nothing. The same id with different fields is a conflict and writes nothing. Overlapping reserves of one id produce one member.

The allocation lock is `0100.band.returns/.allocation.lock`. The reserve call creates it exclusively and removes that same lock. It is not a member and not a receipt. A lock this call did not create is left in place. After five seconds the call reports `allocation lock held: <path>`. Removing a leftover lock is a person's recovery. The tool does not delete captured files.

A crash after the member directory is created and before `reservation.json` is written leaves that number occupied and unnamed. A later retry of the same submission can receive a new number. The tool does not guess its way across that gap.

## Capture

Capture reads one return file and an explicit artifact list. It does not search for a Review heading and does not split the return file. The whole return file is `return.md`.

Each input is read twice before any capture write. A change between those reads writes nothing. After the copy, the tool reads the destination and the source again. `receipt.json` is written last.

Artifact text is `relative|logical`, split on the first `|`. Relative paths use forward slashes and stay under the source root. Logical names are manifest labels. Payload files are flat: `payload/0001.blob` in list order. The logical name is not a nested path.

Source and destination files must be plain files with link count one. Symlinks, junctions, and hard links are refused. Reads stay under the source root, plus the one return file. The source root may contain the book, and it may be the book. The return file may sit outside the source root, and it may sit on the originating work page inside the book. A source root, return file, or selected artifact inside the destination member is refused, including a case-alias of that member. That refusal writes no capture files. Writes stay under the reserved member. Only the explicit artifact list is read. The tool does not crawl the checkout or choose files.

A required logical name that is missing is reported as `missing <logical>` and creates no capture files. The reservation stays. `omitted` on a successful capture is an empty list. Verify accepts a package only when `omitted` is empty and every required logical name is present.

An identical second capture prints `already-captured` and writes nothing. Changed return bytes, payload bytes, or the flags below are a conflict and write nothing. An amended submission is a new submission id on a new member, with `supersedes` pointing at the prior folder.

If `return.md`, `payload/`, `manifest.json`, or `receipt.json` already exists and verification is not complete, capture writes nothing and reports the retained paths.

`interrupt` is a keyword of the Python function, not a command flag. `before-write` writes nothing. `after-return` leaves `return.md` and stops. `before-receipt` writes the manifest and stops. A retry does not finish a partial package.

## Manifest and receipt

`manifest.json` keys, exactly: `schema`, `kind`, `submission_id`, `reservation_sha256`, `return`, `retrospective`, `source_commit`, `captured_at`, `sources`, `omitted`, `required`. `kind` is `manifest`. `return` is `sha256`, `bytes`, `includes_prime_review`. Each source is `logical`, `payload`, `sha256`, `bytes`. The manifest does not contain its own hash.

`retrospective` is the caller's flag. `source_commit` is 40 lowercase hex when that flag is true, and null otherwise. Passing a source commit on a current capture is a refusal. `captured_at` is the time of this capture, UTC `YYYY-MM-DDTHH:MM:SS.ffffffZ`. The tool does not invent a historic timestamp. `includes_prime_review` is the caller's flag. It is recorded and not inferred.

`receipt.json` keys, exactly: `schema`, `kind`, `submission_id`, `reservation_sha256`, `manifest_sha256`, `captured_at`. `kind` is `receipt`. Verify recomputes the reservation hash, the manifest hash, the return bytes, and every payload hash. Extra files fail. `01.md` is ignored as evidence of completion. A verified receipt is not approval, acceptance, or publication. Stdout of a complete verify says `result complete`, `not approved`, `not accepted`, and `not published`.

JSON is canonical UTF-8: sorted keys, separators `(`,`,`,`:`,`)`, `ensure_ascii` false, one trailing LF, finite numbers, duplicate keys refused. Copies are exact bytes. CRLF stays CRLF.

## Future pack section

```text
## Return
Destination: `<reserved 01NN.name>`
Submission: `<id>`
The submission bytes are the captured package. This section points at that package. It is not a second copy of the return body.

## Prime intake
1. Verify the member in a fresh process: `python -B return_capture.py verify --book BOOK --member 01NN.name`
2. A complete receipt means the hashes matched. It does not approve or accept.
3. Review the captured return.md and payload bytes.
4. Publication copies the sealed package and commits those bytes. It does not rewrite receipt.json. Record the commit in a separate acknowledgement.
5. If publication fails, leave the local package complete and unpublished. Do not allocate a new id to retry the push.
```

Prime-support source discovery needs an explicit adapter before it reads these members. This lab does not change that pack.

## Limits

The helper does not claim it can confine a same-user process that can already write the book. A leftover allocation lock blocks new reserves until a person removes that lock. A crash between creating the member directory and writing `reservation.json` does not repair itself. Partial capture files stay on disk and are not completed by a retry. Heading text inside a return file is data. Inventory classification is a separate reader and is not used to extract return bytes.
