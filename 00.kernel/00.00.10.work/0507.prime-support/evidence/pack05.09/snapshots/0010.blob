# Contract — return-capture-inspection/1

Date: 2026-10-27. Recorder: Grok Builder 2.

This file is the schema for `labs/return-capture-pass01/return_inspect.py`. The inspector reads one named member. It does not reserve, capture, repair, allocate, enumerate, or write. It does not call Git or the network.

The sibling `return_capture.py` is pinned at SHA-256 `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac` (45767 bytes). The inspector checks that plain file, refuses a reparse point or a link count other than one, and executes those pinned bytes only when the hash matches. The path is the sibling name. No caller path, no data file, and no version fallback selects it.

Package integrity is that helper's `verify_member`. The inspector does not copy a receipt validator and does not parse the human verify text. `receipt_sha256` is the helper's recomputation of `receipt.json`. It is not stored inside the receipt. Return hash and length are the values `verify_member` accepted by reading `return.md`. A missing or damaged receipt does not become a capture identity. Stored hash strings on a refused package are not reported as `capture`.

Review, acceptance, seating, and publication are outside this schema. A complete object does not claim those decisions are false or true. `includes_prime_review` is the stored caller flag that `verify_member` accepted.

## Command and exits

```text
python -B return_inspect.py inspect --book ABS --member 01NN.slug --json
```

`--book` is absolute. `--json` is required. A well-formed invocation writes one JSON object to stdout and no traceback.

| Status | Exit | Meaning |
| --- | --- | --- |
| `complete` | 0 | `verify_member` succeeded. Capture integrity holds. |
| `reserved` | 1 | A parsed reservation matches the folder. No capture files. Informational. |
| `missing` | 1 | The member is absent, or the directory is an empty slot. Informational. |
| `incomplete` | 2 | The directory is readable and the helper refused the package. |
| `refused` | 2 | The helper pin, the book guard, the member name, or the member directory failed. |

Argument syntax errors use argparse on stderr and exit 2. They are not this JSON object.

Stdout encoding, once the helper is imported, is that helper's canonical JSON: sorted keys, separators `,` and `:`, `ensure_ascii` false, finite numbers, one trailing LF. The pre-import pin refusal uses the same encoding locally because the helper was not executed.

`book` is the absolute path from the helper's reader guard when that guard succeeds. When the guard refuses, `book` is the absolute form of an absolute argument, otherwise the raw argument. `member` is the requested string.

## Object

Top-level keys, exactly:

| Key | Type |
| --- | --- |
| `schema` | string, always `return-capture-inspection/1` |
| `book` | string |
| `member` | string |
| `status` | string, one of the five statuses |
| `problems` | array of strings. Empty only for `complete`. |
| `reservation` | object or null |
| `capture` | object or null |

`reservation`, when present, has exactly: `submission_id` (string), `origin` (`book`, `page`, `batch` strings), `destination` (`member`, `name`, `path` strings), `expected_outputs` (array of strings), `submitter`, `reviewer`, `release` (strings), `supersedes` (string or null), `reserved_at` (string), `reservation_sha256` (64 lowercase hex). It is present only when `parse_reservation` accepts the file and the destination matches the folder. `reservation_sha256` is the helper's hash of those bytes.

`capture` is present only for `status` `complete`. Keys, exactly: `submission_id`, `origin`, `retrospective` (boolean), `source_commit` (40 lowercase hex or null), `captured_at` (string), `reservation_sha256`, `manifest_sha256`, `receipt_sha256`, `return`, `payloads`. `return` is `sha256`, `bytes` (integer), `includes_prime_review` (boolean). Each payload is `logical`, `payload`, `sha256`, `bytes`. Payload `sha256` is the digest `verify_member` recomputed, in manifest order.

`reserved` uses problem `reservation only`. `missing` uses `member is absent` or `empty member`. `incomplete` uses the helper's refusal text, such as `missing receipt.json`, `hash mismatch return`, `duplicate JSON key`, or `invalid JSON`. `refused` uses the pin or guard text, such as `helper hash mismatch: expected <pin> actual <actual>`, `book is link`, `member is link`, `member path is not a return member`, or `member path is outside the book`.

## Worked complete example

These bytes came from one disposable package the accepted helper wrote outside this archive. They illustrate the binding. They are not a live member and they are not `0110`.

Return bytes are `Did.\n` (5 bytes), SHA-256 `e1d4ac07dade356a40ea3da83f437c1ae36d3d89bd8718601600925bc842223b`. Payload `note.txt` bytes are `note\n` (5 bytes), SHA-256 `389ed6887e49a315f706f6c2b931b1dcf0d797c91437124f32eb98555c669758`. The helper's `verify` on that package returned exit 0. `verify_member` reported the hashes below.

```json
{
  "schema": "return-capture-inspection/1",
  "book": "<absolute book path>",
  "member": "0101.alpha",
  "status": "complete",
  "problems": [],
  "reservation": {
    "submission_id": "example-inspect",
    "origin": {"book": "0508.return-capture", "page": "05.04.md", "batch": "05.04"},
    "destination": {"member": "0101", "name": "alpha", "path": "0101.alpha"},
    "expected_outputs": ["note.txt"],
    "submitter": "Grok Builder 2",
    "reviewer": "Codex Prime",
    "release": "example only",
    "supersedes": null,
    "reserved_at": "2026-10-27T20:49:06.122099Z",
    "reservation_sha256": "236567a293e16569aa2ff32139bfebeec5fa44eccccc48a2ba4b3bc6ad6b5c7e"
  },
  "capture": {
    "submission_id": "example-inspect",
    "origin": {"book": "0508.return-capture", "page": "05.04.md", "batch": "05.04"},
    "retrospective": false,
    "source_commit": null,
    "captured_at": "2026-10-27T20:49:06.146239Z",
    "reservation_sha256": "236567a293e16569aa2ff32139bfebeec5fa44eccccc48a2ba4b3bc6ad6b5c7e",
    "manifest_sha256": "dba25acfde207cb689bf706ef7e148448b79a39d5bb1ddefc97986b10c73c12f",
    "receipt_sha256": "aa7435370d4641391c7a6f235d1c07fcea3f7d426c678102b8f103b98478d60e",
    "return": {
      "sha256": "e1d4ac07dade356a40ea3da83f437c1ae36d3d89bd8718601600925bc842223b",
      "bytes": 5,
      "includes_prime_review": false
    },
    "payloads": [
      {
        "logical": "note.txt",
        "payload": "0001.blob",
        "sha256": "389ed6887e49a315f706f6c2b931b1dcf0d797c91437124f32eb98555c669758",
        "bytes": 5
      }
    ]
  }
}
```

The same reservation projection with `"status": "reserved"`, `"problems": ["reservation only"]`, and `"capture": null` is the informational shape for that reservation file before capture files exist.

A missing member uses `"status": "missing"`, `"problems": ["member is absent"]`, `"reservation": null`, and `"capture": null`.

An incomplete package, such as a mutated return, uses `"status": "incomplete"`, `"problems": ["hash mismatch return"]`, `"capture": null`, and a `reservation` object only when the reservation file still parses and matches the folder.

A refused name uses `"status": "refused"`, `"problems": ["member path is not a return member"]`, `"reservation": null`, and `"capture": null`.
