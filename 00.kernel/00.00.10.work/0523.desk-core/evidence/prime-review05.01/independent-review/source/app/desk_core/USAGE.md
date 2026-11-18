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
python3.11 -B -m app.desk_core show --book /absolute/disposable --page 0523 --subject sample --pass 01
python3.11 -B -m app.desk_core submit-return --book /absolute/disposable --input return.json
python3.11 -B -m app.desk_core retrieve --book /absolute/disposable --page 0523 --subject sample --pass 01
python3.11 -B -m app.desk_core review --book /absolute/disposable --input review.json
python3.11 -B -m app.desk_core recover --book /absolute/disposable --page 0523 --subject sample --pass 01
python3.11 -B -m app.desk_core pending --book /absolute/disposable
python3.11 -B -m app.desk_core pins
```

N5NN pass files stay on the matching `01NN.subject` line. N7NN pack, return, and
review stay on that page. Other bands are refused. See `evidence/build05.01/CONTRACT.md`.
This is not production-ready and it does not call pinned custody tools.
