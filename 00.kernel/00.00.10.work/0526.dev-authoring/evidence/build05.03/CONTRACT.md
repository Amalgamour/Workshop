# CONTRACT - typed forms and review binding
date: 2026-11-02
pack: 0526.dev-authoring/05.03
schema: authoring-delta-contract/1
status: written before code; do not revise after tests

This is the delta from labs/pack-authoring-pass01 and app/authoring_tools.py. Pass01 remains the prototype. This contract is not approval, release, seating, or a Prime authoring pilot. accepted is false. This builder does not commit.

## Preserved
labs/pack-authoring-pass01, app/authoring_tools.py, app/authoring.json, and app/tests/test_authoring_entry.py stay byte-stable. Review-loop v4 and its nine pins stay. The synthetic preview evidence/authoring05.02 stays, including its five draft.md.conflict-prime-* faces. No 05.02.md page is created. Freeze on D:\Git\lib-build is refused and writes nothing. Profiles stay the two pass01 files, 0423-to-0526 and fixture-authoring. No new profile and no new kernel address. The dependency reader, code-root set, and pack checker stay the accepted pins. The assembler is not called. complete_claim stays false. 0126.dev-authoring stays unfiled. 0126.boot-members-0509 stays the occupant. Readiness stays blocked.

0710/06.02.decisions is unseated direction. This slice does not edit it and does not treat it as seated law. No conflict between the build-pack template and a seated law page is present in the allowed inputs. This build does not choose an authority. An action that required that choice would preserve the submitted input and stop with `held: template-law conflict`. No such action is defined here.

## Forms
The governing declaration is labs/pack-authoring-pass02/forms/build-pack-v1.json, schema authoring-forms/1, form id build-pack-v1. It is the only field list. The returned form and the validator both read that file. There is no second hard-coded field list. The readable source template remains 0423.dev-authoring/templates/build-pack-v1.draft.md and is still a measured source. The pass01 machine template remains pinned and is not the validator.

Named forms: intent, item, note, disposition, review. No other kind is accepted. Each returned form is schema authoring-form/1 and carries the declaration identity, the kind, the field objects from that declaration, the example input, the correction help, the not-submitted compute facts, the selected profile and measured sources, and the draft status. Draft status is absent when no session is open. It names the pass and state when a session is open.

The source-only request is:

```text
authoring form --book ABS --profile ID [--kind intent|item|note|disposition|review] [--json]
```

It has no operation id and writes nothing. An omitted kind returns the form needed now: intent when intent is incomplete or no session exists, otherwise item when the draft has no item, otherwise disposition when a note is unresolved, otherwise review when review is absent, otherwise no meaning form. The command `start` without input still reserves the next pass and returns that same next form inside the authoring result. A filled start validates intent through the declaration.

Field states are distinct. A required string refuses absent, null, empty, and a wrong JSON type. An optional object refuses a wrong type and accepts null as not-applicable. A required list refuses absent, null, and a short list; an empty list is allowed only where the declaration minimum is 0. An extra key is state extra. Help names the field, the state, the expected shape, the retained input path, and labs/pack-authoring-pass02/PRIME-USE.md. The caller does not submit pass numbers, item numbers, or hashes inside the JSON.

## Review binding
Inspect of an open draft returns schema authoring-result/2. Before a review, candidate_sha256 is the rendered document and final_sha256 is null. draft_sha256 equals the candidate. After a review, candidate_sha256 remains the document inspected before that judgment, final_sha256 is the render that includes the judgment, and draft_sha256 equals the final. Inspect also returns the selected review assessment, unresolved issues, and stop conditions. The render text does not contain either digest.

Review requires --draft-sha256. That value is compared to the current render before the judgment is stored. A match stores one review bound to that candidate, then computes final_sha256. A mismatch refuses with `stale candidate`, writes nothing, and does not store the operation. Omitting the flag refuses with `candidate identity is required`. The caller does not predict final_sha256.

Freeze requires --draft-sha256 of the final document returned by inspect. It recomputes the candidate from the record with the pre-judgment review restored, and recomputes the final from the current render. It also checks the form declaration digest, the readable template digest, the source digest, and the dependency-set digest. A miss refuses and does not write the page. Changed item meaning, intent, disposition, source bytes, template bytes, set bytes, or form-declaration bytes invalidate the stored review. Freeze does not silently approve the new bytes. The prepared page, when written on an outside book, is the final rendered bytes. approval and release stay false.

Exact retry of the same operation id and the same raw bytes returns the stored result and does not add a second judgment. A different request under that id exits 2, leaves the record unchanged, and says the conflict. Typed refusals are not stored.

## Derived face
The record remains authoritative. draft.md is a derived face. When a successful mutation replaces a face that still matches the previous canonical render, the previous bytes are kept as draft.md.history-<operation>. That is ordinary history. derived_history is true and derived_conflict is false. When the face differs from the previous canonical render, the divergent bytes are kept as draft.md.divergence-<operation>, derived_divergence is true, and derived_conflict is true. The canonical face is then rewritten from the record. Existing draft.md.conflict-* files are not deleted and are not relabeled. Inspect does not write. A face that matches the current record is matches-record.

## Failures
Exit 0 is success or an idempotent replay. Exit 2 is `stop:` on stderr and empty stdout. Exit 4 is `partial:` after a failed record replace; the previous record stays. A linked book ancestor is refused by the v2 door before the module starts: `book root ancestor is linked and was not followed`. A linked book root is `book root is not a directory`. Freeze on the checkout is `freeze on the live checkout is outside this slice`. Source drift remains `source-drift`. A stale set remains `stale dependency set`. A missing dependency remains `dependency <id> is missing`. A changed form binding is `changed form`. A freeze hash that is not the final document is `final document identity does not match`.

## App
app/authoring-v2.json and app/authoring_tools_v2.py are the pinned successor door. librarian.py changes only the authoring branch, which loads authoring_tools_v2.py. app/README.md changes only the authoring section. The caller cannot pass an executable, a template path, or a dependency-set path. The door pins the pass02 module, the form declaration, the two existing profiles, the pass01 module as predecessor, the reader, the set, and the checker. No N3NN address is created.

## Limits
No worker loop, no migration, no kernel or law or 00.live or current-assignment edit, no N1NN receipt, no 0184, no Git publish, no current-book authoring write, and no Prime pilot. A rendered page is not release.
