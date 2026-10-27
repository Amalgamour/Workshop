# 05 — Registered Clerk returns in Prime intake
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
Inputs: evidence/pack05.04/source-manifest.json and exact numbered snapshots.
Build a fixture-only adapter for EXPLICITLY REGISTERED Clerk job references. Do
not claim a whole-inbox scan. This avoids inventing a raw-event reader or another
queue while the public inbox has no structured discovery projection.

## #01 — Notes and narrow schemas
Notes first: new06.05.md. Preserve source-before and all prior lab evidence. Add
the contract under evidence/build05.04/. Registry entries own only scope/paths:
explicit absolute local store, job_id, instructions_base, expected reviewer and the
pinned Clerk tool reference. New jobs require explicit registration in this slice.
Version registry/subject formats if extended; preserve valid v1 page/return-file
behavior and stored acknowledgement reads without rewriting their identities.
Do not adopt provisional fields as kernel law or install a real registry/store.

## #02 — Read only the accepted inspection interface
Adapter code may live in labs/prime-support-pass01/clerk_adapter.py and connect
to existing status/intake commands. Invoke only the pinned accepted Clerk CLI:
show --store S --job ID --instructions-base BASE --json. Known code SHA-256:
f697a7e443117c3d1face62d3021f7634154d76214b77fadec1a5cc3c99d394c.
Verify code identity before execution; no caller-selected code replacement or
shell strings. Stores and instruction files are data, never executed. No raw
event/outbox reads, directory enumeration as a second inbox, human-output parsing,
queue/claim/return/repair operations or worker/model calls in adapter production.
Parse inspection/2 strictly; unexpected schema, malformed JSON/nonobject/duplicate
keys, identity mismatch or incomplete response is an attention item, not success.
Keep the exact observed projection identity/source in the context packet.

## #03 — Return identity, readiness and acknowledgement are separate
Subject identity: (canonical store path, job_id, returned.event_sha256). A different
valid event identity is a new unseen subject; identical observations/replays do
not create another acknowledgement. Define a distinct Clerk subject kind; do not
pretend the store is a Git repository or synthesize a page-return identity.
Queued/claimed/unknown/incomplete/corrupt states never manufacture a return id.
Validate the declared job/reviewer binding; mismatches stay visible and unusable.
A clean returned handoff requires usable instructions, all event/completion/artifact
checks ok, empty problems and the expected success result. Exit0 or state returned
alone is insufficient. Preserve nonclean/missing/unchecked diagnostics in status.
An explicit seen acknowledgement of an intact returned event is not review or
acceptance; troubled artifacts/instructions must remain attention even after ack.
Ack must freshly inspect and bind the expected event id before its exclusive
acknowledgement-only write. No write to the Clerk store or its evidence. Existing
findings/reviews stay owned by their source records; unsupported Clerk review
bindings are unknown/not-machine-readable, not inferred from the event or ack.
Keep Clerk's external-store restriction intact; the Git-backed return archive is
a separate component. No real job registration, app wiring or Observer fetch here.

## #04 — Demonstrate the new connection
Use disposable cloned code/stores only. Keep the existing29 Prime tests/demo
passing. Add a real copied-Clerk fixture queue->claim->return; register its exact
job; status/scan unseen->ack->seen->idempotent ack, with actual show/2 digest used.
Queue/claim/return are fixture SETUP ONLY, never adapter commands. Assert adapter
does not read raw events (instrument reader/access paths in the tests) and uses
the accepted CLI projection. Prove all Clerk/source/index/ref bytes unchanged.
Cases: queued/claimed;changed artifact same id still attention;stale/missing base;
unknown job;damaged pair;changed valid event id not inheriting seen;reviewer/job
conflict;malformed/old-schema projection;wrong tool hash;ack stale event refused;
ack-store deletion restores unseen without hiding problems. Disclose skips and
retain failures. No network, real store mutation, model execution or live rollout.
Demo records separate-process calls and explicit scope (registered jobs only).

Allowed writes: labs/prime-support-pass01/, THIS batch/new06.05 and new evidence/
build05.04/. No Clerk/app/capture/assembly/kernel/SoF/other pages, shared assignments,
indexes, views or Observer branch changes. No shared Git commit/push. Prime publishes.
Fully reread contract/code/tests/docs, disposition notes, and return HERE Did, Blocked,
Need with exact hashes/results/limits and one bounded next action.

## Return — Claude
Release: the Director, chat 2026-10-27: "The Director releases 0507.prime-support/05.04. Workspace: D:\Git\lib-build Branch: workshop Read: 00.kernel/00.00.10.work/0507.prime-support/05.04.md Verify pins, record release and claim, then implement the fixture-only registered Clerk return intake adapter. Use the accepted inspection/2 interface. Preserve diagnostics after acknowledgement. No raw-event reader, automatic inbox discovery, real-store installation or routing. Return on the named page. No shared Git commits/pushes."
Claim: claude-opus-5-5 (Anthropic), Colab, executor, claimed 2026-10-27T14:03-05:00 on workshop at 9dcd981124d491794b41715aaaaff1c16e5f4bc0. pack05.04: 12 of 12 snapshots match their pins, and live equals all 12. The manifest names no commit. clerk.py live is f697a7e4…, the accepted inspection/2 code. Scope: this batch only.
Execution: RETURNED for Codex Prime review, 2026-10-27. Fixture-only registered Clerk return intake is built. There is no raw-event reader, no inbox discovery, no queue/claim/return/repair in the adapter, no real registry or store, no routing, no app wiring and no Observer fetch. Nothing was written to a Clerk store, the Clerk lab or the 0506 page. No shared Git commit or push.

Did:
- Verified pack05.04: 12 of 12 snapshots match their pins, and live equals all 12. clerk.py live is f697a7e4…, the accepted inspection/2 code.
- Wrote notes first: 06.05.md, final 39252fef…, with D01-D09 and outcome O01-O05.
- Preserved the before-bytes of all six lab files in evidence/build05.04/before/.
- Wrote the contract: evidence/build05.04/DESIGN.004.md, ce37a4d8….
- Lab files:
  - new clerk_adapter.py 06828436…, the only Clerk reader;
  - prime_support.py 44cd1cef… → 700d60d2… (registry v2, prime-intake/2 records, status and scan rows, `intake ack-clerk`);
  - new tests/test_clerk_adapter.py 03f9a256…;
  - new demo_clerk.py f560a6ba…;
  - README.md 77669282… → 8b3e020c…, a documentation edit made after the final runs;
  - unchanged: demo.py 9d1ecbf3…, tests/test_prime_support.py 9ef97783…, tests/test_psi.py a23ed5f6…, .gitignore.
- Manifest: evidence/build05.04/SHA256SUMS.txt, 65ed37b8276d831a26a48a072f39535f1715d49f77244c1b7278bb0079facf09, LF, 34 entries, not itself. Earlier manifests are preserved.
Blocked: nothing.
Need: Prime's review.

How it reads Clerk:
- Only `<python> -I -B <clerk.py> show --store S --job ID --instructions-base BASE --json`, with no shell, cwd set to the temp directory, and a timeout.
- It runs only after both the registry's sha256 and the file's bytes equal the adapter's constant ACCEPTED_CLERK_SHA256 (f697a7e4…). The caller cannot choose other code.
- It parses inspection/2 strictly: exact keys, enums, types, the presence rules for each state, and the exit code checked against problems. Anything else is `unsupported`, never success.

Identity, readiness and acknowledgement:
- **Subject:** `clerk-return` (normcase realpath store, job_id, returned.event_sha256), stored as prime-intake/2. /1 records are read unchanged.
- **Identity** exists only for state returned with events and completion `ok` and the registered job_id and reviewer matching.
- **Clean** additionally needs artifacts ok, instructions usable, empty problems and exit 0.
- **Review:** `not-machine-readable`.
- **`intake ack-clerk`:** freshly inspects, refuses stale or abbreviated ids, writes one exclusive record, is idempotent for one label and refuses another label. The intake store is refused inside Git or inside any registered Clerk store.
- **After the ack:** a nonclean return stays `clerk-not-clean` attention. Deleting the acknowledgements restores `unseen` with the problems still visible.

What ran (RUNS.md). Each run used a disposable copy with both labs side by side, pythoncore-3.14-64, PYTHONDONTWRITEBYTECODE=1:
1. Run 01, `python -B -X dev tests\test_clerk_adapter.py -v`: 14 run, 3 FAIL. Two were test faults (a source scan that banned the legitimate `"claim"` key; an expected exit 1 that was really 0). One was a product diagnostic, now fixed: an ack on an unknown or incomplete job refused with "binding unknown" instead of "no returned-event identity". Kept.
2. Final, in dev and default modes: test_clerk_adapter 14 of 14, test_prime_support 19 of 19, test_psi 10 of 10. 0 skipped, 0 bytecode.
3. `python -B demo_clerk.py --out <temp> --clerk <copied accepted clerk.py>`:
   - exit 0; scope registered jobs only; 11 processes (3 fixture setup, 8 adapter); 14 of 14 checks;
   - event = sha256(real 0003) = the witness digest;
   - the sequence unseen → ack → seen and review-needed → idempotent re-ack → artifact changed (same event, still seen, clerk-not-clean) → acks deleted (unseen, problems still visible);
   - the Clerk store was byte-identical around every adapter call.
4. The original `python -B demo.py --out <temp> --workshop-repo D:\Git\lib-build --sof-repo D:\Git\SoF`: exit 0, 14 processes, 18 checks. lib-build status and index, and SoF status, were identical before and after.

Tested cases:
- the clean connection;
- queued and claimed jobs;
- a changed artifact, keeping the same id and attention after the ack;
- stale and missing bases;
- an unknown job and a damaged pair;
- a changed valid event id not inheriting seen;
- a reviewer conflict;
- 10 malformed or old-schema projections;
- a wrong tool hash or modified tool bytes, never executed (marker proof);
- stale and abbreviated ack ids;
- ack-store deletion;
- an intake store inside a Clerk store;
- registry v1 unchanged and v2 validation;
- the instrumented proof that the adapter opens or lists no Clerk store path, and the exact argv.

Limits:
- the same-user race between the hash check and the launch;
- registered jobs only;
- Clerk review is not machine-readable;
- the second valid event in the tests comes from Clerk's own documented coherent-rewrite limit, used as a fixture;
- no concurrency testing of two acks.

Next bounded action: Prime's review of this adapter. Then the smallest integration decision: whether the seam (0506 SEAM) or a real registered job is next. No real job is registered by this slice.

## Review — Codex Prime
PENDING.
