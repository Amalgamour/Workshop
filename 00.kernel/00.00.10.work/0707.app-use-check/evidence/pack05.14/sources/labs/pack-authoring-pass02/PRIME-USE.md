# PRIME-USE - typed forms and review binding

Begin with the source only. Ask for the form before supplying meaning. Do not send a template path, an executable, a pass number, or either document hash inside the JSON. This file is not the Prime pilot. Freeze on `D:\Git\lib-build` is refused and writes nothing.

```text
python -B app/librarian.py authoring form --book ABSOLUTE-BOOK --profile 0423-to-0526 --json
```

The result is schema `authoring-form/1`. It names the form needed now, the field objects, the example input, and this help route. An omitted kind returns intent when no session is open or intent is incomplete, then item, then disposition, then review. `--kind intent|item|note|disposition|review` asks for that form and still writes nothing.

Fill only the returned fields. Compute assigns the pass and the item numbers. After the draft is complete, inspect it. Copy `candidate_sha256` from that inspect into the review command. Do not predict the final document hash.

```text
python -B app/librarian.py authoring inspect --book ABSOLUTE-BOOK --profile 0423-to-0526 --json
python -B app/librarian.py authoring review --book ABSOLUTE-BOOK --profile 0423-to-0526 --operation LABEL --input REVIEW.json --draft-sha256 CANDIDATE --json
python -B app/librarian.py authoring inspect --book ABSOLUTE-BOOK --profile 0423-to-0526 --json
python -B app/librarian.py authoring freeze --book ABSOLUTE-BOOK --profile 0423-to-0526 --operation LABEL --draft-sha256 FINAL --json
```

`REVIEW.json` contains `assessment`, `unresolved_issues`, and `stop_conditions` only. The second inspect returns `final_sha256`. Freeze uses that value. Approval and release stay false. A rendered page is not a return and not release.

A typed mistake names the field, the state, the expected shape, the retained input, and this file. Correct the file and reuse the operation id. The same id with the same bytes replays the stored result. The same id with different bytes conflicts and leaves the record unchanged. A stale candidate is refused and is not stored.

Profile `fixture-authoring` is the other accepted profile. It must use a book outside this checkout. No other profile id is accepted.
