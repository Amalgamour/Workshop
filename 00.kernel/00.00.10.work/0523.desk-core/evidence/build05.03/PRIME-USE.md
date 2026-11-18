# Prime use — desk-core reliability lab
date: 2026-11-01
who: Grok Build (xAI)
state: exploratory instructions; not a release and not acceptance

## What this is
The same disposable CLI as the 05.02 repair, plus LF/CRLF face reads and a
revision crash lab. It does not replace the local app. Do not point `--book`
at `00.kernel/00.00.10.work`.

From the repository root:

```text
python3.11 -B -m unittest app.desk_core.test_loop app.desk_core.test_repair app.desk_core.test_fault -v
python3.11 -B -m app.desk_core.demo --transcript /absolute/path/demo.txt
```

## Fault injection
`DESK_CORE_FAULT` is an environment variable, not a JSON field and not a CLI
flag. A non-empty unknown value refuses `fault`. A known value writes a trace
and exits 91 at that revision boundary. Unset it before `show` and `recover`.

```text
DESK_CORE_FAULT=after-task-replacement python3.11 -B -m app.desk_core revise-task --book /absolute/book --input revise.json
python3.11 -B -m app.desk_core recover --book /absolute/book --page 0523 --subject sample --pass 01
```

`show` does not mutate. `recover` keeps A, restores A, or commits B only when
both live files match a sealed proposal. It does not pick the highest
revision directory. `revise-task` of the same request may finish that
proposal. A different request is refused while one is open.

## Windows
Please rerun this tree on Windows Python 3.12+ without edits. The lock child
should take the `msvcrt.LK_NBLCK` branch. The CRLF and tamper tests should
pass without a text-mode rewrite. This sandbox did not run that platform.
An exit of 91 inside the fault test is expected. It is not a STOP.

## Not claimed
No live custody, no model launch, and no proof of race freedom or power loss.
`accepted` stays false.
