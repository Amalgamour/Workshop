# PRIME-USE - pack authoring

Run these from `D:\Git\lib-build`. The profile id is the source reference. It loads `0423.dev-authoring` and the linked work page `0526.dev-authoring`. Do not pass a template path, a pass number, or a hash.

```text
python -B app/librarian.py authoring start --book D:\Git\lib-build --profile 0423-to-0526 --operation prime-start-01 --json
```

Supply one item at a time. The file is meaning only.

```text
python -B app/librarian.py authoring add-item --book D:\Git\lib-build --profile 0423-to-0526 --operation prime-item-01 --input ITEM-01.json --json
python -B app/librarian.py authoring add-item --book D:\Git\lib-build --profile 0423-to-0526 --operation prime-item-02 --input ITEM-02.json --json
```

ITEM-01.json:

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

ITEM-02.json:

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

Then inspect:

```text
python -B app/librarian.py authoring inspect --book D:\Git\lib-build --profile 0423-to-0526 --json
```

The same operation id and the same input bytes are idempotent. A new start operation while this draft is open is refused. Freeze on this checkout is refused. This file is not the Prime pilot.

This build already ran that start and those two items on `D:\Git\lib-build`, then one intent and two note dispositions. The reserved draft is `00.kernel/00.00.10.work/0526.dev-authoring/evidence/authoring05.02/draft.md`. Exact replay bytes and the later commands are in `00.kernel/00.00.10.work/0526.dev-authoring/evidence/build05.01/PRIME-USE.md`. Item 2 contains the character Δ (U+0394). Saving the escape `\u0394` is different raw bytes and conflicts with operation `prime-item-02`.
