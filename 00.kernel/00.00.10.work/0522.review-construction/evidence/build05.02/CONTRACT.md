# Contract — review-construction address repair

Date: 2026-10-31. Author: Grok-2. This contract is written before the 05.02 code change. It repairs the interface in `labs/review-construction-pass01`. The sealed `evidence/build05.01/CONTRACT.md` remains the record of the first lab. A rendered review is not approval, acceptance, release, closure, or custody.

## Commands

From `D:\Git\lib-build`, the commands stay:

```text
python -B labs/review-construction-pass01/construct.py preview --fixture-root ABS --input REL
python -B labs/review-construction-pass01/construct.py apply --fixture-root ABS --input REL
python -B labs/review-construction-pass01/construct.py bind --fixture-root ABS --input REL
python -B labs/review-construction-pass01/construct.py show --fixture-root ABS --target REL
```

The fixture root is an absolute directory outside `D:\Git\lib-build`. `preview`, `bind`, and `show` write nothing. `apply` writes only inside that root. Exit 0 completes. Exit 2 refuses, with stderr starting `refused:`. A held or incomplete judgment can still render. `prime_review_exit` is a result field. The envelope schema stays `review-construction/1` with the same keys. Unknown envelope keys are refused. There is no `verified` or `custody_ok` field.

## RC-01 destination

The source page is a logical path under `00.kernel/00.00.10.work/`.

- N5NN page matches `00.kernel/00.00.10.work/{N}5{NN}.{subject}/{pass}.md`.
- N7NN page matches `00.kernel/00.00.10.work/{N}7{NN}.{subject}/{pass}.pack.md`.
- `{N}` is one digit `0-9`. `{NN}` is two digits. `{subject}` is `[a-z0-9][a-z0-9-]*`. `{pass}` is `05.` plus two digits, and it equals the envelope `pass`.

The derived destination, relative to the fixture root, is:

- N5NN: `{N}5{NN}.{subject}/{pass}.md`
- N7NN: `{N}7{NN}.{subject}/06.{tail}.review.md`, where `{tail}` is the two digits of `{pass}`

`target` is a fixture-relative logical path. It must equal that destination as a string. The same filename under another page id is a different target and is refused with `target is not the derived review destination`. The check runs in envelope parsing, before the target is read, before support files are created, and before any target write. The tool does not search for a newer pass or another copy of the basename. Bytes outside the declared review section stay byte-for-byte.

## RC-02 line and origin

From an N5NN page id `{N}5{NN}.{subject}` the matching line is `{N}1{NN}.{subject}`. The receipt `member` must equal that line or the envelope is refused with `member is not the derived matching line`. The typed return source is `kind: capture`, schema `return-capture/1`, and its `identity.member` must equal the same derived line. Agreement between the receipt string and the identity string is not sufficient when both differ from the derived line.

The pinned capture origin has keys `book`, `page`, and `batch`. This pack does not add a `pass` key to that object. `batch` carries the declared pass. Where those fields are present they must equal:

- `book`: `00.00.10.work`
- `page`: the source page id, such as `0599.synth-lab`
- `batch`: the envelope pass, such as `05.01`

A mismatch is refused with `origin does not match the source` before any support file or target write. A missing origin on an N5NN capture is the same refusal. The positive fixture identity is `0199.synth-lab` for source page `0599.synth-lab` and pass `05.01`. The subject is the page subject.

N7NN `member` is null. `page_local` remains `05.{tail}.return.md`. The record must not contain a `capture` source. No N1NN path is allocated. Receipt file hashes are still compared with the supplied bytes. The result field `custody` remains `not-established`. `allocated` remains false. A boolean in the caller input is not custody.

## RC-03 binding

Schema of the hashed preimage is `review-task-binding/2`. Canonical JSON is UTF-8, sorted keys, separators `(`,`,`, `:`,`)`. The sha256 covers:

- `source.book`, `source.page`, `source.pass`
- `task_id`
- `assignment_path`, `assignment_sha256`, `assignment_bytes`
- evidence rows sorted by `logical_path`, each with `bytes`, `label`, `logical_path`, `sha256`
- `agreement_sha256`
- receipt placement, member, page-local name, submission id, status, label, and receipt, return, and manifest hashes and lengths

The preimage does not cover review text, record bytes, or the target file hash. Rendering a review leaves the digest unchanged. A judgment-only change leaves it unchanged. A coherent change of source page or pass, of `assignment_path`, of assignment bytes, of an evidence file, of the agreement, or of a receipt file changes the digest. An origin that disagrees with the source does not produce an alternate binding; parsing refuses it.

`bind` returns the wrapper schema `review-task-binding/2` with `binding_sha256`, `binding`, and `target_read` false. It uses the same address and origin checks. It does not read the target and does not call `prime_review.py`.

### Old inputs

`review-task-binding/1` is not emitted. The tool has no upgrader and does not reinterpret a `/1` preimage as `/2`. `evidence/build05.01/` is not an input. When `support/<review_identity>/record.json` or `binding.json` already exists, apply compares bytes first. A difference refuses with `support record conflicts <name>` before any support byte is replaced and before the target write. Matching bytes are left in place.

## Pinned member boundary

`labs/prime-review-pass01/prime_review.py` stays the pinned report tool. Its capture member pattern is `^01[0-9]{2}\.[a-z0-9][a-z0-9.-]*$`. This lab accepts every leading digit in its own address rule. For `{N}` other than `0`, the derived member is outside that pin. `bind` still returns `review-task-binding/2` for a coherent envelope. `preview` and `apply` call the pin and refuse with `bad member` before creating support files or writing the target. N7NN has no capture member, so a nonzero N7NN page can render under the same page-local rule. This pack does not edit the pin. Widening it is a later change to an existing module.

## Writes that stay

Exactly one review heading is accepted: `## Review — Codex Prime` or `## Review - Codex Prime`. The heading line and the bytes outside the section stay. The body is replaced when it strips to `PENDING` or `PENDING.`, or when it already equals the new render. Idempotent replay exits 0 with `written` false and the same target bytes. A different substantive section is not overwritten; apply saves the unused body under `partial/<review_identity>-<reviewsha12>.md` and refuses with `existing review conflicts; a successor process is required and this review was not overwritten` and `partial evidence:`. Preview of that conflict writes no second partial.

`expect_sha256` is 64 lowercase hex or `absent`. A stale hash refuses and leaves the target. `permit_create` true creates an absent destination file: the U+2014 heading, the assessment, and LF, without inventing assignment text. UTF-8 is required. BOM, NUL, invalid UTF-8, and mixed CR/LF refuse with no write. An all-LF or all-CRLF file keeps that newline for the new section only.

Apply writes `name.review-construct.tmp` beside the target, fsyncs, rereads, and uses `os.replace` for an update or `os.rename` for a create. If the target changed after the first read, the temporary file stays and the target stays. Compare-then-rename narrows a stale write. It is not proof of race freedom.

Support files on a successful apply are `support/<review_identity>/record.json` and `binding.json`. The record file is the record bytes sent to the report tool. Identity, origin, destination, and stale-hash refusals leave both the target and the support files untouched.

## Result

Success stdout is one JSON object. `preview`, `apply`, and idempotent replay use schema `review-construction-result/1` with the same keys as the 05.01 result, including `custody: not-established` and `allocated: false`. `result` is `preview`, `applied`, or `idempotent`. `show` returns `review-construction-show/1`. The rendered body still quotes authority none, the three false flags, the task binding, the receipt hashes, and `custody: not-established`. Compute headings stay at level 3. Stock report headings are nested two levels. A rendered level-2 page heading is refused with nothing written.

## Evidence and scope

The suite writes `evidence/build05.02/transcript.json` and `evidence/build05.02/sample-review.md`. It does not write `evidence/build05.01/`. The constructor does not import or edit `app/`, `prime_cycle.py`, `return_capture.py`, `return_inspect.py`, `desk_lab.py`, or `labs/return-placement-pass01`. It does not reserve, capture, migrate, or scan. The future adapter that fills a descriptor from `0122.review-construction` remains unwritten. AR-01 stays held.
