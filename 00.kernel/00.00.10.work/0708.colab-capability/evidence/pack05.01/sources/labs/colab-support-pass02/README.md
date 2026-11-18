# colab-support-pass02 — exchange layout v2 preparer

**batch:** `00.kernel/00.00.10.work/0510.colab-tools/05.03.md`
**contract:** `00.kernel/00.00.10.work/0510.colab-tools/evidence/exchange05.03/CONTRACT.md`
**design:** `00.kernel/00.00.10.work/0411.colab/evidence/exchange-layout-v2/CONTRACT.md` (read, not changed)
**state:** experimental lab code until Prime reviews it. Standard library only.

This lab prepares an N7NN Colab pass in the Director-agreed exchange layout:

| file | made by | in the package? |
|---|---|---|
| `05.NN.pack.md` | this preparer | yes, the one primary instruction source |
| `06.NN.notes.md` | this preparer, from supplied notes | yes, preparation notes, not a review |
| `05.NN.return.md` | the Colab's exact bytes, after capture | **no**; a TEMPLATE is included |
| `06.NN.review.md` | Prime, later | **no**; a TEMPLATE is included |

## Relationship to v1
Accepted v1 (`labs/colab-support-pass01`, 33bbe41c…) stays byte-identical. Grok-1's current workflow repair depends on it. This lab loads v1 read-only by pin and reuses its request and binding validation, section resolution, pinned assembler and checker loading, pinned tool launch, deterministic ZIP, output-path rules and inspector parsing. It does not copy them. Capture, verify and inspect stay with the accepted helper and inspector.

Versions are explicit and fail closed:
- request `colab-request/2` (v1 keys plus `preparation_notes`);
- config `colab-config/2` (adds `producer_v1`);
- digest `colab-package-digest/2`, OUT verification `colab-package-verification/2`, handoff `colab-handoff/2`.

A v1 request or OUT is refused, not migrated.

## Commands
```text
python -B colab_support.py preview --request ABS --config ABS --json
python -B colab_support.py prepare --request ABS --config ABS --output ABS --digest HEX --json
python -B colab_support.py verify  --output ABS --config ABS --json
python -B colab_support.py intake  --output ABS --config ABS --book ABS --member 01NN.slug \
    --return-file ABS --source-root ABS --artifact REL|LOGICAL [...] --json
python -B handoff_check.py check --output ABS --expected-digest HEX --json
python -B handoff_check.py copy  --output ABS --expected-digest HEX --to ABS --json
python -B -X dev tests/test_colab_support_v2.py -v
python -B -X dev tests/test_handoff_check.py -v
```
Examples: `examples/config.example.json` and `examples/request-exchange-layout.json` (the real-source request).

## Package
- `package/` contains:
  - `ENTRY.md`, `05.NN.pack.md` and `06.NN.notes.md`;
  - `templates/05.NN.return.TEMPLATE.md` and `templates/06.NN.review.TEMPLATE.md`;
  - `binding.json`, `colab-request.json`, `source-manifest.json` and `snapshots/`;
  - `support/SUPPORT.md` and `support/assembler/{05.NN.md, request.snapshot, completion-receipt.json}`.
- The legacy assembler draft lives only under `support/` and is labelled as transport support. Verify runs the pinned assembler verify on a temporary projection of those files plus the shared manifest and snapshots, and checks them byte-for-byte against the assembler's own `assembler-output/`.
- OUT also holds `prepared-colab.zip`, `evaluator/` (blind scoring only, never zipped), `assembler-request.json`, `assembler-run.json` (raw), `assembler-output/`, `handoff.json` and `verification.json` (written last).
- Verify demands this exact set. Any `*.return.md` or `*.review.md` in OUT is a `fabricated-exchange` defect.

## Handoff for a later consumer
`handoff.json` (`colab-handoff/2`) lists:
- the digest preimage;
- the binding;
- the exchange names, including the not-created return and review;
- every envelope file with its role and hash;
- the source-path to snapshot map;
- the support projection;
- the ZIP identity;
- the verify invocation and the config contract.

`handoff_check.py` imports no producer and no workflow code. Since batch 05.04 (contract `evidence/checker05.04/CONTRACT.md`), the expected launch digest is its only trust anchor.
- It **derives** every claim from digest-bound bytes by fixed v2 rules and recomputes both the assembler and package digests. The claims are: investigation, binding, exchange names and roles, the source to snapshot map, the support projection, ZIP membership, evaluator separation and the full preimage.
- It refuses any handoff field that differs from what it derived. Identity is output only under `trusted`, and only when the result is `valid`.
- It validates every path and refuses links, junctions, hard links, unknown extras, duplicate ZIP entries and pre-created return or review files.
- `copy` needs a fresh destination and writes exclusively. A replay is a read-only refusal (`already-copied` or `occupied`). A failed copy stays `partial`, with no deletion and no resume.
- It does NOT re-render the prose files or recompute section line ranges; it lists these under `not_verified`. Use the pinned producer `verify` when those matter.

Exit codes: 0 valid or copied; 1 mismatch or partial; 2 refused.

## Intake
Intake requires the reservation origin to equal the investigation book, page and pass. It runs the pinned capture, verify and inspect, and keeps the raw runs. It returns a separate `colab-placement-proposal/2`: the member, receipt and return hash mapped to `<page>/05.NN.return.md`, with `action: proposed; not written`. Returned bytes are never edited and nothing is written to a live book. No review is produced.

## Limits
- There is no reviewed workflow consumer of this layout; workflow naming integration is pending. No integration is claimed.
- Single repository and commit, exact headings or whole files, and pages 0701–0799 only: all inherited from v1.
- The ZIP does not contain its own digest. The launch must carry the expected digest.
- The hash of a pinned tool is checked immediately before each launch. No sandbox is claimed against a same-user race between that check and the launch.
