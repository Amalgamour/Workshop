# PRIME-USE - pack authoring preview

Run these from `D:\Git\lib-build` with Python 3.14 and `python -B`. The recorded preview used `C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe -B` and `PYTHONDONTWRITEBYTECODE=1`.

The session is already open. Profile `0423-to-0526` is the source reference. It loads `0423.dev-authoring` and the linked work page `0526.dev-authoring`. Do not pass a template path, a pass number, or a hash. Repeating a command below with the same operation id and the same input bytes returns the stored result and writes nothing. A different file under the same operation id exits 2 and preserves the record. A new start operation exits 2. Freeze on this checkout exits 2 and writes nothing. This is not the Prime pilot.

## Source reference

```text
python -B app/librarian.py authoring start --book D:\Git\lib-build --profile 0423-to-0526 --operation prime-start-01 --json
```

There is no `--input`. The recorded exit was 0. Compute reserved pass `05.02`.

## Two semantic items

The bytes that count are the files. Item 2 contains the character Δ (U+0394), not the escape `\u0394`.

```text
python -B app/librarian.py authoring add-item --book D:\Git\lib-build --profile 0423-to-0526 --operation prime-item-01 --input D:\Git\lib-build\00.kernel\00.00.10.work\0526.dev-authoring\evidence\build05.01\preview-inputs\item-01.json --json
python -B app/librarian.py authoring add-item --book D:\Git\lib-build --profile 0423-to-0526 --operation prime-item-02 --input D:\Git\lib-build\00.kernel\00.00.10.work\0526.dev-authoring\evidence\build05.01\preview-inputs\item-02.json --json
```

`item-01.json` supplies this meaning. Compute assigned `#01`.

```json
{
  "title": "Show the source form",
  "purpose": "Supplied synthetic demonstration. Load the registered 0423 source and reserve the next pass.",
  "requirements": ["The model does not choose the pass or the item number."],
  "interfaces": ["authoring start"],
  "acceptance": ["Inspect shows this meaning under the computed item number."],
  "note_refs": ["00.kernel/00.00.10.work/0423.dev-authoring/06.01.md"],
  "open_choices": ["Prime replaces this synthetic item in a later pilot."],
  "dependency_refs": []
}
```

`item-02.json` supplies this meaning. Compute assigned `#02`.

```json
{
  "title": "Keep the second meaning separate",
  "purpose": "Supplied synthetic demonstration. A second item is meaning only, including the mark Δ.",
  "requirements": ["UTF-8 text is stored as text."],
  "interfaces": ["authoring add-item"],
  "acceptance": ["Inspect shows both items in one draft."],
  "note_refs": ["00.kernel/00.00.10.work/0423.dev-authoring/06.02.md"],
  "open_choices": [],
  "dependency_refs": []
}
```

Both recorded exits were 0.

## Intent and dispositions already applied

These three calls are why inspect shows intent and note coverage. They are supplied synthetic. They are not a Prime review.

```text
python -B app/librarian.py authoring revise --book D:\Git\lib-build --profile 0423-to-0526 --operation prime-intent-01 --target intent --input D:\Git\lib-build\00.kernel\00.00.10.work\0526.dev-authoring\evidence\build05.01\preview-inputs\intent.json --json
python -B app/librarian.py authoring revise --book D:\Git\lib-build --profile 0423-to-0526 --operation prime-disp-01 --target disposition --note 00.kernel/00.00.10.work/0423.dev-authoring/06.01.md --input D:\Git\lib-build\00.kernel\00.00.10.work\0526.dev-authoring\evidence\build05.01\preview-inputs\disp-01.json --json
python -B app/librarian.py authoring revise --book D:\Git\lib-build --profile 0423-to-0526 --operation prime-disp-02 --target disposition --note 00.kernel/00.00.10.work/0423.dev-authoring/06.02.md --input D:\Git\lib-build\00.kernel\00.00.10.work\0526.dev-authoring\evidence\build05.01\preview-inputs\disp-02.json --json
```

`disp-01.json` is `{"disposition": "integrated", "item": "01"}`. `disp-02.json` is deferred, with why `Supplied synthetic: this preview does not decide the draft review.` The recorded exits were 0. The command line does not pass `--item`.

## Inspect

```text
python -B app/librarian.py authoring inspect --book D:\Git\lib-build --profile 0423-to-0526 --json
```

The recorded exit was 0.

- pass: `05.02`
- state: drafting
- approval: false
- release: false
- review: absent
- missing: review, return readiness
- next: Prime can inspect this draft. Freeze on the live checkout is refused. This is not the Prime pilot.
- record: `D:\Git\lib-build\00.kernel\00.00.10.work\0526.dev-authoring\evidence\authoring05.02\record.json`
- draft: `D:\Git\lib-build\00.kernel\00.00.10.work\0526.dev-authoring\evidence\authoring05.02\draft.md`
- draft sha256: `547c3ae566323d6f821abed79a004a08a143f0246f14d110476560e1eee98cf3`
- draft bytes: 3431
- return: intended `0126.dev-authoring`, status occupied, occupant `0126.boot-members-0509`, readiness blocked
- `complete_claim`: false

`05.01.md` was not changed by these calls. No `05.02.md` page was written. Do not freeze this draft. Do not start a new operation on this profile while it is open.
