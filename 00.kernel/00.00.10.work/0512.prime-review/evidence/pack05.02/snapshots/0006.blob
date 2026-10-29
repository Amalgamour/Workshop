# Adoption — not wired

0512.prime-review/05.01 #03 and #04. This slice does not gate releases. A caller that has not been changed does not consult `labs/prime-review-pass01/prime_review.py`.

Checked on workshop at the build: `python -B app/librarian.py prime-review` exited 2 with `stop: normal run is not activated`.

## Callers today

| Caller | Entry | What it does now | This module |
| --- | --- | --- | --- |
| Prime support | `app/librarian.py prime-status` through `app/prime_intake.py` to `labs/prime-support-pass01/prime_support.py` | Read-only status. Pin `700d60d2e49c186d49e56a9a38058e21a722b4a5dd79d461453a305e8d904f70`. | Not called. |
| Prime brief | `labs/prime-brief-pass01/prime_brief.py brief` | Direct lab command. Pin `302ed832d2fa955a591420f13d3b22ce91e4a7669c69a778d443fc82627580d7`. Not a librarian command. | Not called. |
| Pack check | `app/librarian.py pack-check` through `app/prime_tools.py` to `labs/pack-custody-pass01/pack_check.py` | Checks a pack manifest. A clean check is not release readiness. | Not called. |
| State projection | `labs/state-projection-pass01/state_projection.py project` | Lifecycle projection. Pin `b349da5cef5178296a069c354002a600ba4e168c2710aa5d87789724d4951ecb`. | Not called. This module does not reuse its closure rule. |
| Return capture | `labs/return-capture-pass01/return_capture.py` and `return_inspect.py` | Custody. Pins `8f3da5c6…` and `947915fe…`. | Not called. A capture binding only cites `return-capture/1` fields. |

`app/librarian.py` also has `batch-observe`, `capture-return`, `boot-prepare`, `boot-check`, `boot-judge`, and `boot-show`. None of them call this module.

## Later integration tests

Run these only after Prime reviews this return and a later batch names the wiring. They are not this slice.

1. Prime support: copy one `revision_id` from a status fixture into a `prime-support-return/1` source with `bytes_are_revision` true. The review tool refuses when that id is not the content sha256. `prime_support.py` stays unmodified.
2. Prime brief: copy one brief document's sha256 into a `prime-brief-input/1` source. The review tool refuses when `brief_sha256` is not the content sha256. `prime_brief.py` stays unmodified.
3. Pack check: `librarian.py pack-check` still has no prime-review flag, and a clean pack check still does not release the pack.
4. App: the librarian command list still rejects `prime-review` until a reviewed batch adds a pinned front door. That door, if added, must keep `releases_action` false and must not treat exit 0 as a release.

## Unsupported until that wiring

- `prime_support.py` status, scan, and ack
- `prime_brief.py brief`
- `state_projection.py project`
- `return_capture.py` capture and verify
- librarian `prime-status`, `pack-check`, `pack-preview`, `pack-assemble`, `pack-verify`, `batch-observe`, `capture-return`, and the boot commands
- Clerk
- any dispatcher, poll, or session launcher

## Colab seam

`labs/colab-workflow-pass01` is not imported. Its return is not a dependency. After Prime accepts that lab, a later caller may place its output digest in a `supplied-text/1` or `batch-observation/1` source of this tool. This batch does not do that.

## What a wired caller must still not claim

Exit 0 means the named action was outside the declared holds, or the report was a clean continue, develop, or complete-as-supplied draft. It does not release work. A bound Director reply does not expand the grant. Dev dialogue does not become a #NN job.
