# Contract — corrected worked example for return-capture-inspection/1

Date: 2026-10-27. Recorder: Grok Builder 2.

This file corrects the illustrative origin. The original contract at `evidence/inspection05.04/CONTRACT.md` stays as submitted, SHA-256 `2a37dc0720067f1380f00a63a8501fa9ac36f52e9bda6a63356ee6654fd4734c`, 7305 bytes. Schema `return-capture-inspection/1` is unchanged. The seven top-level keys stay `schema`, `book`, `member`, `status`, `problems`, `reservation`, and `capture`. Statuses stay `complete`, `reserved`, `missing`, `incomplete`, and `refused`.

The sibling `return_capture.py` stays SHA-256 `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac` (45767 bytes). The inspector still executes those pinned bytes only after the hash matches. Package integrity is still that helper's `verify_member`. This correction adds no validator, no origin-normalization code, and no live-member edit.

## Range

`MEMBER_MIN` is 101 and `MEMBER_MAX` is 199. The inspector applies that test before it classifies the path as absent or present. A name outside 0101–0199 is `refused`, exit 2, problem `member is outside the return band`, with `reservation` null and `capture` null. That refusal is the same whether the directory exists. An in-band path that is absent stays `missing`, exit 1, problem `member is absent`. An in-band directory with neither a reservation nor capture files stays `missing`, problem `empty member`. `reserved` and `complete` for 0101 and 0199 are unchanged.

## Command and exits

```text
python -B return_inspect.py inspect --book ABS --member 01NN.slug --json
```

`--book` is absolute. `--json` is required. A well-formed invocation writes one JSON object to stdout and no traceback.

| Status | Exit | Meaning |
| --- | --- | --- |
| `complete` | 0 | `verify_member` succeeded. Capture integrity holds. |
| `reserved` | 1 | A parsed reservation matches the folder. No capture files. Informational. |
| `missing` | 1 | An in-band member is absent, or the directory is an empty slot. Informational. |
| `incomplete` | 2 | The directory is readable and the helper refused the package. |
| `refused` | 2 | The helper pin, the book guard, the member name, the band, or the member directory failed. |

Argument syntax errors use argparse on stderr and exit 2. They are not this JSON object.

`book` is the absolute path from the helper's reader guard when that guard succeeds. `member` is the requested string. Review, acceptance, seating, and publication stay outside this schema. The object does not claim those decisions are false. `includes_prime_review` is the stored caller flag that `verify_member` accepted.

## Object

`reservation`, when present, has the same keys as the original contract: `submission_id`, `origin`, `destination`, `expected_outputs`, `submitter`, `reviewer`, `release`, `supersedes`, `reserved_at`, and `reservation_sha256`. It is present only when `parse_reservation` accepts the file and the destination matches the folder.

`capture` is present only for `status` `complete`, and only from a successful `verify_member` result. Its keys are unchanged: `submission_id`, `origin`, `retrospective`, `source_commit`, `captured_at`, `reservation_sha256`, `manifest_sha256`, `receipt_sha256`, `return`, and `payloads`.

## Caller labels are shape

`origin.book`, `origin.page`, and `origin.batch` are strings the helper stored. The reader checks that they are non-empty strings and that the batch matches `05.NN`. It does not check that a book of that name exists, that the page was released, or that the batch label is historically true. `submitter`, `reviewer`, and `release` are the same kind of caller text. A well-formed origin is not proof of its semantic truth. Caller labels and release text confer no authority.

## Worked complete example

These bytes came from one disposable package the pinned helper wrote outside this archive. The reserve command used `--origin-book 00.00.10.work --origin-page 0508.return-capture --origin-batch 05.04`. The package is not a live member and it is not `0114`.

Return bytes are `Did.\n` (5 bytes), SHA-256 `e1d4ac07dade356a40ea3da83f437c1ae36d3d89bd8718601600925bc842223b`. Payload `note.txt` bytes are `note\n` (5 bytes), SHA-256 `389ed6887e49a315f706f6c2b931b1dcf0d797c91437124f32eb98555c669758`. Both digests were recomputed from the captured files. The helper's `verify` on that package returned exit 0. `verify_member` reported the hashes below. The absolute book path in the inspect object was `C:\Users\misg\AppData\Local\Temp\rc0505-example-mkli0198\book`. The example replaces that path with `<absolute book path>` and pretty-prints the same object. No hash, timestamp, length, or origin field was edited.

```json
{
  "book": "<absolute book path>",
  "capture": {
    "captured_at": "2026-10-27T21:12:02.637419Z",
    "manifest_sha256": "a86053d3c94bf6a384b12e37b9483448d792738b61ddb23fd434de78cba14057",
    "origin": {
      "batch": "05.04",
      "book": "00.00.10.work",
      "page": "0508.return-capture"
    },
    "payloads": [
      {
        "bytes": 5,
        "logical": "note.txt",
        "payload": "0001.blob",
        "sha256": "389ed6887e49a315f706f6c2b931b1dcf0d797c91437124f32eb98555c669758"
      }
    ],
    "receipt_sha256": "fd822d4260c7329f3171d26dafbfb8a6ca19e4373d24bfa70b430778a7668d9c",
    "reservation_sha256": "ed5fafc4a4f4597dc241996794c6043eb6787d35f61a8a2037b8453220050669",
    "retrospective": false,
    "return": {
      "bytes": 5,
      "includes_prime_review": false,
      "sha256": "e1d4ac07dade356a40ea3da83f437c1ae36d3d89bd8718601600925bc842223b"
    },
    "source_commit": null,
    "submission_id": "example-inspect"
  },
  "member": "0101.alpha",
  "problems": [],
  "reservation": {
    "destination": {
      "member": "0101",
      "name": "alpha",
      "path": "0101.alpha"
    },
    "expected_outputs": [
      "note.txt"
    ],
    "origin": {
      "batch": "05.04",
      "book": "00.00.10.work",
      "page": "0508.return-capture"
    },
    "release": "example only",
    "reservation_sha256": "ed5fafc4a4f4597dc241996794c6043eb6787d35f61a8a2037b8453220050669",
    "reserved_at": "2026-10-27T21:12:00.440248Z",
    "reviewer": "Codex Prime",
    "submission_id": "example-inspect",
    "submitter": "Grok Builder 2",
    "supersedes": null
  },
  "schema": "return-capture-inspection/1",
  "status": "complete"
}
```

Before those capture files existed, the same reservation read as `status` `reserved`, `problems` `["reservation only"]`, `capture` null, exit 1. Its `reservation_sha256` was `ed5fafc4a4f4597dc241996794c6043eb6787d35f61a8a2037b8453220050669`.

An in-band missing member uses `status` `missing`, `problems` `["member is absent"]`, `reservation` null, and `capture` null.

An out-of-band name, present or absent, uses `status` `refused`, `problems` `["member is outside the return band"]`, `reservation` null, and `capture` null.

An incomplete package, such as a mutated receipt, uses `status` `incomplete` and `capture` null. A reservation object is included only when the reservation file still parses and matches the folder.

A name the member pattern rejects uses `status` `refused`, `problems` `["member path is not a return member"]`, `reservation` null, and `capture` null.
