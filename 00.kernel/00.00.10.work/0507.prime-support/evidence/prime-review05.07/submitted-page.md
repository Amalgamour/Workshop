# 05 — First recorded Prime boot prototype
version: 001
Authorization: draft — 2026-10-27
who: Codex Prime
state: draft; awaiting Director release
Face: 05
PPPP: 0507
book: 00.00.10.work

## Assignment
Executor: Claude. Reviewer: Codex Prime.
Release: PENDING. Claim: PENDING.
Workspace D:/Git/lib-build, branch workshop. Verify evidence/pack05.07/source-manifest.json
and exact snapshots. Implement a new fixture lab; do not edit active builders' code.

## #01 — Notes, contract and pin gates
Notes FIRST on new06.08.md. Write evidence/build05.07/CONTRACT.md before code,
carrying all PB-01–PB-05 requirements and fixture choices from prime-review05.06.
Only new labs/prime-boot-pass01/ code/docs/tests/demo plus THIS batch/new notes/
build05.07 evidence. Standard library only. Reuse accepted read-only tools, with
fixed full code hashes checked before import/subprocess (including required sibling
dependencies). No shell strings, data-as-code, highest-version scan or guessed pin.
Contents checker SHA-256: fc16d2f68a3645050b6766ce18ce55f8169a0e2bad52d3392b4d059c629073a4.
Prime support, Clerk adapter and capture helper full pins are supplied in the manifest.
The return_inspect.py dependency is STILL UNACCEPTED. Do not read/import its changing
code. Missing structured identity is explicit, not guessed from human verify text.

## #02 — A bounded prepare/check/judge/show prototype
Implement prime_boot.py, README.md, meaningful tests/test_prime_boot.py and demo.py.
CLI may follow the draft prepare/check/judge/show, with an explicit attempt id
allocated before any fallible preparation. Keep requests/inputs/packet/answers/
checks/judgement/outcome in one externally designated attempt directory, each
file exclusive-create. Link later attempts without editing earlier ones. Preserve
request/intent and stage failures; a failed/partial attempt must not look ready.
Invalid or unwritable record roots honestly refuse; never falsely claim a log.
No live book/store installation, source edits, acknowledgements, model calls,
dispatch, acceptance, role seating or normal-run activation. A judgement is an
explicit supplied record from a named reviewer label, not authentication or an
authority grant. No automated free-text semantic grading.

First slice: disposable Git workspace/registry/records fixtures. Use explicit
registered Git lanes, with committed reads; preserve dirty-path observations
separately. Clerk-job runtime boot integration is deferred; it must be reported
unsupported if requested here, not silently dropped. Read fixed Git blobs at the
requested commit, validate the explicit contents pointer with the pinned checker,
record role/assignment text and conflicts, and call accepted status/scan instead
of inventing a queue. Record actual branch/HEAD identities and source kinds;
changed required identities during prepare produce an unstable/partial result.
Keep every input/observed identity in the attempt, never stamp live bytes as old
commit blobs. No network or Git writes; allow only bounded read commands.

An explicit member list may use pinned capture verify on disposable member copies
and record integrity evidence, but without an accepted inspector structured fields
stay unavailable. No prose parser or parallel receipt validator. That dependency
does not block the Git-lane prototype; steps requiring it stay clearly unverified.

## #03 — Packet, answers and readiness
Packet defaults: at most12 references and128 KiB RAW source material. Validate
positive bounded caller limits; record exact source hashes plus retrievable text
for the allowed material. No recursive repo read, truncation presented as full
content, or silent overflow. Omitted required context remains a remediation.
Carry the small O1–O6 exercise with PB-02/PB-03 corrections: any valid cited target
inside declared scope may be selected with an explanation; attention order grants
nothing. 'No unknown found in this bounded packet' is allowed. An absent source
uses recorded absence evidence, not a fake citation. Compute checks identities,
scope and explicit fields; the named judgement grades explanations. Without all
required checks and supplied grades, outcome cannot be oriented. Oriented grants
no new work authority. Follow-up investigation/remediation is recorded separately.

## #04 — Demonstrate failed and successful attempts
Disposable fixtures only. Demo: prepare -> explicit fixture answers -> check ->
explicit fixture judgement -> show -> remedied second attempt linking the first.
Do not claim an actual model has cold-booted. Tests cover content and citation
checks, known conflicts, non-first valid target, no-missing-dependency case,
missing source/absence evidence, wrong/missing tool pin, dirty vs committed bytes,
HEAD/ref change, packet overflow, malformed/duplicate inputs, invalid linked or
occupied destinations, failed preparation kept, stage interruption retained,
immutable retry/conflict behavior and no orientation without judgement.
Assert source/Git metadata unchanged and no writes outside the explicit records
fixture. Retain first failures/skips. Store commands/logs in tests.txt; exact
hashes, cases, actual demo results and remaining limits in verification.json.
No unrelated regression suites for untouched tools. Fully reread and disposition
notes. If a proposed requirement needs more scope, report it instead of expanding.

## #05 — Capture the submission locally
Verify capture helper SHA-256 8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac. Write dedicated
evidence/build05.07/submission.md beginning Did, Blocked, Need. Complete every
declared output in reserved 0113.prime-boot-0507/reservation.json, then run:

```text
python -B labs/return-capture-pass01/return_capture.py capture --book "D:/Git/lib-build/00.kernel/00.00.10.work" --submission claude-0507-0507 --return-file "D:/Git/lib-build/00.kernel/00.00.10.work/0507.prime-support/evidence/build05.07/submission.md" --source-root "D:/Git/lib-build" --artifact "labs/prime-boot-pass01/prime_boot.py|labs/prime-boot-pass01/prime_boot.py" --artifact "labs/prime-boot-pass01/README.md|labs/prime-boot-pass01/README.md" --artifact "labs/prime-boot-pass01/tests/test_prime_boot.py|labs/prime-boot-pass01/tests/test_prime_boot.py" --artifact "labs/prime-boot-pass01/demo.py|labs/prime-boot-pass01/demo.py" --artifact "00.kernel/00.00.10.work/0507.prime-support/06.08.md|00.kernel/00.00.10.work/0507.prime-support/06.08.md" --artifact "00.kernel/00.00.10.work/0507.prime-support/evidence/build05.07/CONTRACT.md|00.kernel/00.00.10.work/0507.prime-support/evidence/build05.07/CONTRACT.md" --artifact "00.kernel/00.00.10.work/0507.prime-support/evidence/build05.07/tests.txt|00.kernel/00.00.10.work/0507.prime-support/evidence/build05.07/tests.txt" --artifact "00.kernel/00.00.10.work/0507.prime-support/evidence/build05.07/verification.json|00.kernel/00.00.10.work/0507.prime-support/evidence/build05.07/verification.json"
python -B labs/return-capture-pass01/return_capture.py verify --book "D:/Git/lib-build/00.kernel/00.00.10.work" --member 0113.prime-boot-0507
```

Keep original source/submission/evidence. Append only member/receipt hash/fresh
verification below. A partial/refused capture stays explicit; never remove it or
allocate around failure. No shared Git commits/pushes, app/kernel/current-law/
assignment changes, other active lanes or SoF. Prime reviews and publishes.

## Return pointer
Release: the Director, chat 2026-10-27: "The Director releases 0507.prime-support/05.07. Workspace: D:\Git\lib-build Branch: workshop Read 00.kernel/00.00.10.work/0507.prime-support/05.07.md. Verify pins, record release and claim, then build the fixture-only recorded Prime boot prototype. Carry the PB-01–PB-05 review requirements. Preserve failed attempts, keep committed and live observations distinct, and separate orientation from authority. Do not integrate the unaccepted return inspector, install a live registry, invoke models or change assignment records. Capture into reserved 0113.prime-boot-0507 and fresh-verify it. No shared Git commits or pushes."
Claim: claude-opus-5-5 (Anthropic), Colab, executor, claimed 2026-10-27T15:59-05:00 on workshop at db4629e48217a79d6f9839afd7ea105ec5ec8fb8. pack05.07: 16 of 16 snapshots match their pins, and live equals all 16. Capture helper 8f3da5c6… and contents checker fc16d2f6… verified. Scope: this batch only.
Execution: returned. Member 0113.prime-boot-0507. Receipt sha256 e23fd57ccecc7db8a32b93d0315bffb01d7a9167da4b90506015455f48247db4. Fresh verify: result complete (not approved, not accepted, not published).

## Review — Codex Prime
PENDING.
