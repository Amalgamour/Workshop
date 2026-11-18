# PRIME-USE - typed forms and review binding

Run these from `D:\Git\lib-build` with `python -B`. Begin with the source only. The book is an absolute disposable directory outside this checkout. Do not pass a template path, an executable, a pass number, or either document hash inside the JSON. This file is not the Prime pilot. Freeze on `D:\Git\lib-build` is refused and writes nothing.

The suite retained the final document at `00.kernel/00.00.10.work/0526.dev-authoring/evidence/build05.03/runs/20261102T183436Z/05.01.md`. The same bytes are in that run's `draft.md`. sha256 `dbdcc43ad9b1e0e225d27e704bc119b53b18fe4b1b41eb4b4d5c49be47c076b5`, 3425 bytes. The candidate copied from inspect into review was `689bda49a3454d7010da28d38994835b836f2133c57500d90586462065d261e6`. The disposable book that produced those bytes was removed. Repeating the commands below creates a new book.

```text
python -B app/librarian.py authoring form --book ABSOLUTE-BOOK --profile 0423-to-0526 --json
```

The result is schema `authoring-form/1`. With no open session the kind is intent. The fields are the objects in `labs/pack-authoring-pass02/forms/build-pack-v1.json`. Fill only those fields.

Intent:

```json
{
  "goal": "Check the typed form and the review binding.",
  "scope": {
    "included": "two items and a prepared page in this disposable book",
    "excluded": "release, return filing, and the live checkout",
    "allowed_writes": "this disposable book only"
  },
  "finish": "Freeze writes the final reviewed bytes",
  "executor": "Grok-1",
  "reviewer": "Codex Prime"
}
```

```text
python -B app/librarian.py authoring start --book ABSOLUTE-BOOK --profile 0423-to-0526 --operation start-01 --input INTENT.json --json
```

Item 1 purpose is `Caller form check. Compute assigns the number.` Item 2 purpose is `Second meaning stays in its own item. Mark Δ` with character Δ (U+0394), not the escape `\u0394`. `relationship` and `condition` were JSON null. Note refs were the two declared 0423 notes. Compute assigned `01` and `02`.

```text
python -B app/librarian.py authoring add-item --book ABSOLUTE-BOOK --profile 0423-to-0526 --operation item-01 --input ITEM-01.json --json
python -B app/librarian.py authoring add-item --book ABSOLUTE-BOOK --profile 0423-to-0526 --operation item-02 --input ITEM-02.json --json
```

The first declared note was integrated to item `01`. The second was deferred. `why` was `Supplied check: the note is deferred and the draft stays unreleased.`

Inspect, then copy `candidate_sha256` into review. The review JSON has `assessment`, `unresolved_issues`, and `stop_conditions` only.

```text
python -B app/librarian.py authoring inspect --book ABSOLUTE-BOOK --profile 0423-to-0526 --json
python -B app/librarian.py authoring review --book ABSOLUTE-BOOK --profile 0423-to-0526 --operation review-01 --input REVIEW.json --draft-sha256 CANDIDATE --json
python -B app/librarian.py authoring inspect --book ABSOLUTE-BOOK --profile 0423-to-0526 --json
python -B app/librarian.py authoring freeze --book ABSOLUTE-BOOK --profile 0423-to-0526 --operation freeze-01 --draft-sha256 FINAL --json
```

The second inspect returns `final_sha256`. Freeze uses that value. Before review, `final_sha256` is null and `draft_sha256` equals the candidate. After review, `draft_sha256` equals the final and the candidate stays the pre-judgment document. Neither digest is printed in the rendered page. Approval and release stay false. `complete_claim` stays false. Return readiness stays blocked while `0126.boot-members-0509` occupies slot 0126.

A typed mistake names the field, the state, the expected shape, the retained input, and `labs/pack-authoring-pass02/PRIME-USE.md`. Correct the file and reuse the operation id. The same id and the same bytes replay. Different bytes conflict and leave the record unchanged. A stale candidate is refused and is not stored.

Profile `fixture-authoring` is the other accepted profile. It must use a book outside this checkout. No other profile id is accepted. Do not point these commands at `evidence/authoring05.02`.
