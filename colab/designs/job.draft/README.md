# job.draft — request construction proposal

Status: proposal, 2026-10-11. This is a design prototype, not installed behavior law.

`job.py` helps a model prepare one review batch. The model identifies the work and supplies facts. Compute checks the request shape, resolves its designated location, and writes the next unused `05.NN.md`. The Director replies. A later, separately governed worker executes released work. This prototype implements only the first stage.

## Model workflow

1. Read the relevant live behavior/structure sources and the subject files. Do not derive authority from this prototype.
2. Run `python job.py describe` or `python job.py describe --command redraft`. It lists each command's purpose, required information, holds, and basis.
3. Prepare request JSON using `request.example.json`. Give each `#NN` one requested decision or operation. Give coupled items explicit `depends_on` ids. Split a multi-command sequence into dependent requests; this draft deliberately does not interpret a chain of Director commands.
4. Run `prepare` in preview mode. Resolve missing fields or sources before writing. Unknown verbs stop rather than being guessed.
5. Inspect the preview, then use `--write` to create the batch. Creation is not release. Replies remain blank, authorization is draft, receipts say not executed.

## Routing

The caller names the project and a context path inside the book being worked. An explicit policy maps that book to an existing dedicated job page. Exactly one route must match. Context may be a subject file, page, or the book directory. The tool never uses `00.live` as a work destination: the current file selects the law book to climb, which is a different job.

The policy names the existing job page, a permitted work range, and the basis for that routing. It does not prove parentage or grant permission. The prototype checks physical containment, including resolved symlinks/junctions; the enclosing book must carry `00.md`. Reserved and retired output pages are rejected. It creates no desk, shelf, book, page, sentinel, proof, or governing face.

For now the dedicated page must already exist. This is deliberate: live band allocation and page classes are still being settled. The tool should eventually call the approved page-building mechanic rather than invent one. No live policy has been installed. `routing.example.json` operates only on the isolated `example-project`.

`05.NN` is the batch file number. `#NN` is an item marker within that batch. Neither allocates the internal/outward task slot labels described by law `0005.ticket`. The next batch number is one above the highest present `05.NN.md`, never an empty gap. Exclusive file creation protects against concurrent collisions. At 99 it stops. Preserve prior batch files; this prototype has no historical allocation ledger if they are removed.

## Commands

The machine-readable contracts live in `commands.json`; `describe` exposes the same material rather than keeping a second definition in code.

| Request | Purpose | Information beyond the common fields |
|---|---|---|
| `>point` | Establish/correct an exact source relationship | relationship, destination, local difference |
| `>note` | Preserve explanation or decision | exact record text, destination, why it matters |
| `>redraft` | Produce a coherent replacement draft | inputs, decisions, output plan, preservation, alignment checks |
| `>fix` | Correct a demonstrated bounded defect | defect, desired behavior, output plan, verification |
| `>patch` | Propose a minor dated edit | exact change, explicit patch basis, verification |
| `>check` | Inspect and report | criteria, scope, report destination |
| `>strike` | Mark an obsolete sentence while retaining it | exact sentence, reason, replacement reference |
| `>sign` | Ask for a signature decision | exact drafts, readiness evidence, actor |
| `>approve` | Ask the Director for an approval transition | signed files, evidence, transition plan, actor |
| `>clean` | Ask for a bounded cleanup | snapshot, scope, preservation, open-work check |

All requests also need title, issue, recommendation, ask, existing target, scale, source paths with exact existing headings, and an observable done condition. The proposed `point` meaning is broader than the current signed test page; `note`, `redraft`, and `check` need explicit behavior contracts during the law rework. The data marks these as proposals. `>notes` is not silently aliased to `>note`; the Director needs to decide whether they are the same act. Other verbs remain unknown until defined.

## Run the isolated example

From this directory, after `python build_examples.py`:

```powershell
python job.py describe --command point
python job.py prepare --project ./example-project --context ./example-project/10.demo/10.work/10.lib --policy ./routing.example.json --request ./request.example.json
```

Add `--write` to create a fresh demonstration batch. `example-output.md` is the saved preview; it is not a live queue or released instruction. Run `python -m unittest -v test_job.py` for the focused checks.

## What compute can and cannot establish

This writer validates required fields, exact source headings, containment, known commands, dependencies, and file allocation. It does not establish that a statement is true, a source is authoritative, a patch is permitted, the selected book is the right one for the human's intent, or a Director reply authorizes a particular action. A sentence saying an authority exists is evidence to inspect, not an authorization token.

The draft batch uses the familiar issue/recommend/Ask/path/scale/reply shape, with explicit purpose, sources, dependencies, command parameters, done, hold, and pending receipt. Fields cannot introduce new top-level markers through multiline content. Critical items appear first where dependency order permits. Item numbers remain stable.

Future execution should record the exact Director decision, permitted scope, changed files, checks, and unresolved matters beside each item. It should not use a nonblank reply or command token alone as release. It needs separate governing contracts for talk, proposal, release, execution, and completion; request structure is only one part of that chain.

## Questions for the law rework

- Does each work page carry its own batches, or does a designated job page collect book-wide requests? This prototype supports the latter by explicit routing, without deciding the law.
- Who establishes/changes the routing policy, and how should the approved band mechanic allocate a fresh job page?
- Are `>note` and `>notes` distinct? What exact destinations and append mechanics do they request?
- Does `>point` only select a source, or also release a bounded pointer edit? Current practice and the signed test page need reconciliation.
- Which command chains can be released together, and which need a new Director decision between steps?
- What exact receipt closes a job, and where does important reasoning survive a snapshot/cleanup?

No live kernel, existing `05.NN`, or Director replies were edited by this proposal.
