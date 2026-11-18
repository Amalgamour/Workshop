# Prime use — desk-core/2 repair
date: 2026-10-31
who: Grok Build (xAI)
state: repair instructions; not a release and not acceptance

## What this is
The same disposable CLI as pass 01, with portable byte writes, revision
history, source identity in the task binding, stale-return refusal, and a
pass-local trace. Intelligence still supplies the task, the release, the
claim, the return, the judgment, and any revision reason. Compute does not
decide that the work is correct and does not invent an authorizing reference.

Run from the repository root:

```text
python3.11 -B -m app.desk_core --help
python3.11 -B -m unittest app.desk_core.test_loop app.desk_core.test_repair -v
python3.11 -B -m app.desk_core.demo --transcript /absolute/path/demo.txt
```

Give `--book` an absolute directory outside this checkout. A path inside the
Librarian tree is refused. Do not point it at `00.kernel/00.00.10.work`.

Windows Python 3.12+ was not run here. Please rerun the unmodified tree there.
A Linux pass is not that result. `accepted` remains false.

## One pass
1. `init` the disposable book.
2. `record-task` with a synthetic spec. `0523.subject` uses face
   `05.01.md` and later returns on `0123.subject`. `1523.subject` returns on
   `1123.subject`. `1702.subject` stays on that page.
3. `register` the supplied release and claim.
4. `show` in a new process. State is `claimed` until a return is captured.
   `complete` is false. `accepted` is false.
5. `submit-return`. An identical retry is idempotent. Different bytes are
   refused and the receipt file stays.
6. `review` with a typed judgment. This is fresh only while the receipt's
   captured task binding, the release, and the claim all match the current
   task.
7. `revise-task` with `reason` and `authorizing_reference` in the input.
   Prior task and face bytes are under `05.PP.history/<revision>/`.
   `--interrupt` exits 3 and does not replace those bytes.
8. A later `review` of the revised task is `stale-return` until a new return
   is captured for the new binding. `recover` stays derived.

## What not to treat as acceptance
A selected revision is not Director approval. A trace is not a review.
A review is not seating, migration, or permission to launch a model.
Advisory locks are not OS isolation.
