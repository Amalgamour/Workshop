# colab-support-pass01

**batch:** `00.kernel/00.00.10.work/0510.colab-tools/05.02.md`
**contract:** `00.kernel/00.00.10.work/0510.colab-tools/evidence/n7nn05.02/CONTRACT.md`
**interface:** `00.kernel/00.00.10.work/0411.colab/evidence/n7nn-interface-v1/CONTRACT.md` (read, not changed)
**state:** experimental lab code until Prime reviews it. Standard library only.

`colab_support.py` prepares, verifies and takes in one N7NN Colab investigation package. It formats Prime's supplied question, reasons, cases and permissions consistently and checks custody facts. It does not judge meaning, call a model, schedule work, review, accept, release or publish.

## Commands

```text
python -B colab_support.py preview --request ABS --config ABS --json
python -B colab_support.py prepare --request ABS --config ABS --output ABS --digest HEX --json
python -B colab_support.py verify  --output ABS --config ABS --json
python -B colab_support.py intake  --output ABS --config ABS --book ABS --member 01NN.slug \
    --return-file ABS --source-root ABS --artifact REL|LOGICAL [--artifact ...] --json
python -B -X dev tests/test_colab_support.py -v
```

Exit 0 means a completed preview, prepare, `already-prepared`, intact verify, `captured` or `already-captured`. Exit 1 means a recorded negative: a partial or mismatched package, or intake `attention`. Exit 2 means a refusal.

## Inputs

- **`colab-request/1`** is Prime's structured request. It holds the exact shared `colab-binding/1` object, plus the question, why, context, built state, known gaps, method, cases, mode, scoring intention, environment, permissions, stop points, prior involvement, required sources, withholds, unavailable items, Director replies and the return route. The full key table is in the contract. A worked real example is `evidence/n7nn05.02/request-example.json`.
- **`colab-config/1`** is local only: repository label to absolute root, the interpreter, and the four pinned tools. It never enters the package or the digest.

## What it checks

- **Investigation origin.** It must be an N7NN member (0701–0799). The door 0700, N5NN implementation batches and other bands refuse. A target that names the investigation page refuses.
- **Targets.**
  - Each target is read as the Git blob at its commit, and must match its sha256; otherwise it is stale and refuses.
  - `source.path` must end in `book/page/file`.
  - A heading section is the exact line outside fences, with a 1-based occurrence required when it repeats. There is no fuzzy match and no HEAD or worktree fallback.
  - `kind: id` refuses: interface v1 declares no id syntax.
- **One commit.** All targets, required sources and evaluator sources share one repository and commit, because the pinned assembler reads one revision.
- **ZIP-only recipients.** Recipient-facing text may not name a local absolute path. Director replies are quoted data and are exempt.
- **Blind scoring.** Evaluator sources may not overlap candidate inputs, by path or by bytes. Evaluator material is written to `OUT/evaluator/` and is never zipped.

## Reuse

- **Accepted pack assembler** (`75d49679…`). It is loaded in-process for planning and run by its own CLI to assemble. An adapter maps the colab request onto `pack-assembly-request/1`:
  - origin and identity are the investigation page and pass;
  - the executor is the recipient label;
  - the goal is the question and why;
  - instructions are entry, method, one per case, then return;
  - dependencies list withholds and unavailable items.

  The assembler's refusal of `#` in single-line fields carries over to the title, author, recipient, reviewer, `environment.write` and the return destination.
- **Pinned custody checker** (`9bbd9d57…`), through the assembler.
- **Capture helper** `return_capture.py` (`8f3da5c6…`) and **inspector** `return_inspect.py` (`947915fe…`) for intake.

Every tool is hash-checked before it is loaded or launched. Subprocesses use an argument array and no shell. Raw stdout, stderr and exit are retained.

## Output

```text
OUT/package/            assembler files + binding.json, colab-request.json, ENTRY.md, 06.NN.md, RETURN-TEMPLATE.md
OUT/prepared-colab.zip  deterministic ZIP of package/
OUT/evaluator/          blind scored method only
OUT/assembler-request.json, OUT/assembler-run.json
OUT/verification.json   written last; holds the colab-package-digest/1 value
```

The assembler's own `verify` demands its exact file set, so `verify` runs it on a temporary byte-identical projection of those files. It also recomputes every colab file from the packaged request and snapshots and compares bytes.

## Limits

- Multi-commit or multi-repository bindings refuse; they are not split across packs.
- `colab-request.json` is packaged verbatim. So a blind method carries no rubric text in the request: it names committed `evaluator_sources` only, and those paths are visible to the candidate as names. An open scored method carries `rubric` and `meaning` in the request and the ENTRY.
- The package carries no `verification.json`, so a ZIP-only recipient cannot cite the digest. Prime binds it at intake.
- Intake reports which return headings are present as a fact. It does not grade them.
- Review and find (0411 operations 4 and 5) are not built.
