# desk-core usage

Prototype command, from the repository root:

```text
python3.11 -B -m app.desk_core <command>
```

`--book` is an absolute disposable directory outside this checkout. The tool
refuses a book inside the Librarian tree. Inputs are JSON files. Stdout is one
JSON object. `accepted` is always false.

```text
python3.11 -B -m app.desk_core init --book /absolute/disposable --label synthetic
python3.11 -B -m app.desk_core record-task --book /absolute/disposable --input task.json
python3.11 -B -m app.desk_core register --book /absolute/disposable --input register.json
python3.11 -B -m app.desk_core revise-task --book /absolute/disposable --input revise.json
python3.11 -B -m app.desk_core revise-task --book /absolute/disposable --input revise.json --interrupt
python3.11 -B -m app.desk_core show --book /absolute/disposable --page 0523 --subject sample --pass 01
python3.11 -B -m app.desk_core submit-return --book /absolute/disposable --input return.json
python3.11 -B -m app.desk_core retrieve --book /absolute/disposable --page 0523 --subject sample --pass 01
python3.11 -B -m app.desk_core review --book /absolute/disposable --input review.json
python3.11 -B -m app.desk_core recover --book /absolute/disposable --page 0523 --subject sample --pass 01
python3.11 -B -m app.desk_core pending --book /absolute/disposable
python3.11 -B -m app.desk_core pins
```

N5NN keeps the leading workflow digit: `0523.subject` returns on `0123.subject`,
and `1523.subject` returns on `1123.subject`. N7NN pack, return, and review stay
on that page, including a nonzero prefix such as `1702`. Other bands are refused.
`revise-task` requires a supplied `reason` and `authorizing_reference`. It keeps
the previous task and face bytes under `05.PP.history/`. `--interrupt` does not
replace the selected wording. A return captured for one task is not a fresh
review of a later task. A face heading may end in LF or CRLF. The stored bytes
are not rewritten just to normalize newlines. `DESK_CORE_FAULT` is a test-only
process exit for the revision lab. It is not a request field. See
`evidence/build05.03/CONTRACT.md`.
This is not production-ready and it does not call pinned custody tools.
