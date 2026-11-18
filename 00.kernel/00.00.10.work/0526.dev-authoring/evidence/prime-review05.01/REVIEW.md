# Review - Codex Prime: 0526/05.01
date: 2026-11-02
outcome: useful incremental authoring prototype; targeted repair required before Prime operational use
custody: pending matching 0126; no receipt or acceptance invented

## Evidence
Read the full submission, contract, PRIME-USE, app facade/profile/template, relevant command implementations and test coverage. All 39 artifact rows and 53 frozen input snapshots match. Input live differences are the authorized app/librarian.py and README changes. Review-loop v4 pins remain as declared. Builder reports 60 cases green after three first-run failures, preserved; Prime did not rerun the old main because it assumes the live preview is absent, contrary to the builder's completed preview.

Prime independently exercised the actual app in a retained external book: typed intent, two small semantic item inputs, computed numbering, two note dispositions and fresh-process full inspection succeeded. Exact commands, stdout/stderr and rendered document are in evidence/prime-review05.01. This is an operator/caller exercise with supplied demonstration meaning, not a real production pack or a fresh-model boot.

## Findings
A1 - Confirmed review target mismatch. After inspect, review with that returned draft_sha256 exits 2: draft sha256 does not match the rendered draft. Code adds the review to the render before comparing the supplied candidate digest. Omitting that digest lets review succeed and then freeze exit 0 on the disposable book. Therefore the intended inspected-candidate binding is not operationally correct. Bind the judgment to the pre-review candidate; separately identify the complete final rendered artifact containing that judgment. Never require Prime to predict the latter hash. Preserve both identities and changed-target refusals.

A2 - The first form is not yet handed to the caller. Start emits gaps and the whole draft but not a typed fillable input contract. The machine template lists field names/ownership and is pinned; implementation hard-codes parsing/rendering and does not load its field declarations as the usable form. A narrow pinned machine form must supply field types, presence, constraints, ownership and sample shape through a command/result, and the same declaration must actually govern validation. Do not claim a generic face engine is finished.

A3 - The current-book preview is synthetic, pass 05.02, without semantic review. It is preserved and NOT the next released builder pack. Its reservation means the next new assignment here is 05.03; do not overwrite 05.02 or copy synthetic meaning into the real repair. Live freeze remains outside this slice. Current matching return route is still occupied.

A4 - Normal computed render revisions are saved as draft.md.conflict-* by write_face, so those names alone do not prove human tampering. Distinguish ordinary derived-history replacement from a divergence relative to the previously rendered record. Do not erase existing evidence. This is diagnostic clarity, not a new authority rule.

## Decision / next
Retain pass01 unchanged as prototype evidence. Build a bounded successor fixing A1/A2 and diagnostic A4, with a first source-only request and exact returned forms. Keep the current-book freeze restriction and pending return custody explicit. The Director's 0710/06.02 decisions govern design direction; proposed law drafts are not seated law. Template/law conflicts require Director review, not builder preference. No kernel edits, migration, release or Git publication by this review.
