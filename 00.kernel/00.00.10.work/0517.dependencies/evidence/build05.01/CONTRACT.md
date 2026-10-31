# CONTRACT — module dependency declarations prototype (labs/module-dependencies-pass01)

Written before the code. This is a prototype contract for 0517.dependencies 05.01, under the 0316.dependencies module home. It seats nothing and adopts no global schema. The tool reads declarations and answers dependency questions. It is not a readiness checker, dispatcher, workflow engine, installer or loader. It never imports, executes or follows anything a declaration names.

## 1. Identity (prototype scheme `repo-path/1`)

A module is `{"repository": LABEL, "path": REL}`:
- `repository` is a label (`^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$`), for example `lib-build`;
- `path` is a repository-relative entry file: `/` separators, no empty, `.` or `..` segment, no backslash, no colon.

The key is the exact pair, so the same path in another repository is another module. The scheme maps onto existing lab files and replaces no kernel module identity rule.

A workflow address is `{"repository", "book", "page", "face_or_pass", "file"}`, all exact strings, for example book `00.00.10.work`, page `0515.prime-cycle`, pass `05.03`, file `05.03.md`. A bare page or pass number is never an address.

## 2. Declaration `module-declaration/1` (strict JSON, exact keys, no duplicates, no NaN)

```
{"schema", "declaration_id" (label), "version" (int ≥ 1), "status": "prototype"|"experimental"|"partial",
 "module": {"repository", "path", "name", "purpose", "interface": [str], "limits": [str], "home": ADDRESS|null},
 "implementation": {"sha256" (64 hex), "bytes" (int), "basis": {"kind": "git-blob", "repository", "commit" (40 hex), "path"}},
 "coverage": {"entry_points": [str], "method": str, "complete_claim": false},
 "no_requirements": bool,
 "requirements": [REQUIREMENT],
 "withheld": [{"what": str, "reason": str}],
 "provenance": {"links": [LINK], "unknown": [str]},
 "supersedes": {"declaration_id", "version"}|null}
```

- **`no_requirements`:**
  - true needs `requirements == []`: an explicitly dependency-free module, within its coverage;
  - false with `[]` is refused as **ambiguous**, because the tool cannot tell "declared none" from "not filled in".
- **`coverage.complete_claim`** must be false in this prototype. A declaration lists the edges its author found for the covered entry points; it is not proof of runtime closure.

**REQUIREMENT:**
```
{"id" (label, unique in the record), "kind": "runtime-code"|"runtime-resource"|"environment"|"evidence"|"task-context",
 "target": {"module": {"repository","path"}} | {"external": {"name": str, "sha256": hex|null}} | {"environment": {"name": str, "detail": str}}
          | {"address": ADDRESS},
 "pin": {"sha256", "bytes"}|null, "pin_required": bool,
 "mechanism": "subprocess"|"import"|"dynamic-import"|"hash-check"|"path-reference"|"read"|"document",
 "condition": {"applies": "always"|"conditional", "id": label|null, "statement": str|null,
               "status": "applicable"|"inapplicable"|"unknown"},
 "availability": "not-applicable"|"unverified"|"declared-unavailable",
 "reason": str, "source_ref": {"path": str, "lines": str}|null}
```

- **Direction is stated once:** this record's module requires `target`. Reverse edges are derived, never stored.
- **`pin_required: true`** needs a pin. A missing pin is refused.
- **A conditional requirement** needs an `id` and a `statement`. An `always` requirement has `status: applicable`.
- **Environment** requirements have `availability` `unverified` or `declared-unavailable`; nothing probes this machine. All other kinds use `not-applicable`.

**LINK:**
```
{"role": "design"|"assignment"|"return"|"review"|"source-stated", "address": ADDRESS, "sha256": hex|null,
 "commit": hex|null, "status": "pinned"|"unpinned", "note": str}
```
- `source-stated` means the module's own text names the page; it is not a verified link.
- A link proves no release, acceptance or runtime dependency.
- An empty `links` list needs a non-empty `unknown`.

## 3. Set `module-declaration-set/1`

```
{"schema", "set_id", "coverage": str,
 "declarations": [{"file": REL, "sha256"}],
 "fixtures": [{"module": {"repository","path"}, "file": REL, "sha256"}],
 "select": [{"module": {...}, "declaration_id", "version"}],
 "bounds": {"max_records": ≤ 500, "max_file_bytes": ≤ 1048576, "max_depth": ≤ 64, "max_output_bytes": ≤ 4194304}}
```

- `REL` is relative to the set file's folder, with no link anywhere in the path.
- Every listed file must hash to its listed sha, or the set is refused (`set-pin-mismatch`). Nothing unlisted is read.
- Fixtures are disposable copies used only for `identity`: they are hashed, never parsed or run.

## 4. Index (derived)

The tool builds the following and holds them in memory; `index --out` writes them as JSON to a new folder (exclusive-create, refused if the folder exists, `partial` kept on a failed write):
- declarations by module key;
- the edges `(module, requirement) → target`;
- reverse edges, derived from those;
- a pin map `sha256 → declarations`.

**Identity problems are findings, not choices:**
- `identity-conflict`: two records with one `declaration_id`/`version` and different bytes, or one module and implementation sha in two non-superseding records with different content;
- `duplicate`: an identical record listed twice, kept once.

## 5. Resolving a module requirement target

Taken in order:
1. **No declaration of the target module:** `record-missing`. The target is not traversed.
2. **The requirement has a pin:** take the declarations whose implementation sha equals the pin.
   - exactly one: resolved;
   - none, while other versions exist: `pin-differs`, listing the pinned sha and the declared shas;
   - more than one, conflicting: `identity-conflict`.
3. **No pin:** an explicit `select` entry for the module resolves it. One declared version resolves as `single-unpinned`. More than one is `ambiguous-version`. The highest version is never chosen.

## 6. Queries (results are `module-dependency-result/1`)

All take `--set ABS` and are read-only. `--condition ID=applicable|inapplicable|unknown` (repeatable) lets the caller state applicability. Caller statements are recorded in the result and override the record's status for that query only.

| command | answer |
|---|---|
| `validate` | per-file validity and set findings |
| `requires --module R:PATH [--transitive] [--depth N]` | the requirements, each with its resolution, path from the root, kind, condition and findings |
| `explain --module R:PATH --to R:PATH` | every declared path from the module to the target, bounded |
| `impacted --module R:PATH [--implementation SHA]` | derived consumers, direct and transitive. For each edge: the consumer's pin and whether it equals `--implementation` (`pin-matches`, `pin-differs`, `unpinned`), plus the consumer's provenance links. "Candidates for Prime review"; nothing is changed or invalidated. |
| `identity` | each fixture file hashed against its module's declarations: `identical-to <decl>`, or `changed` (no declaration has these bytes) |
| `delta --old FILE --new FILE --change FILE` | completion seam, §8 |
| `index --out ABS` | the written index |

**Root states** (the `root` field): `declared` (with requirements), `declared-dependency-free`, `undeclared` (no record), `ambiguous-version`.
- `undeclared` returns `requirements: null`, never `[]`.

**Traversal:**
- An inapplicable condition is listed and not followed.
- An unknown condition is followed and marked `condition-unknown`.
- A revisit within the current path is a `cycle` finding, with the edge path; the edge is not expanded again.
- A shared node reached by two paths is listed once with both paths (`shared`).
- Depth beyond `max_depth` gives `depth-limit`, and the rest is not walked.

**Result:**
- `status: "complete-for-declared-coverage"` only when there are no findings other than `shared`, `environment-unverified` and `condition-inapplicable`; otherwise `"incomplete"`.
- `coverage` repeats each visited record's entry points and method, and `complete_claim: false`.
- An output over `max_output_bytes` is refused.

**Findings:**
- `record-missing`, `pin-differs`, `ambiguous-version`, `identity-conflict`, `cycle`, `depth-limit`;
- `condition-unknown`, `condition-inapplicable`;
- `environment-unverified`, `environment-unavailable`, `external-unverified`;
- `withheld`, `provenance-unknown` (no links), `provenance-unpinned` (a link without a sha);
- `address-unresolved` (an address target; it is listed, not opened), `shared`.

## 7. Exits

| exit | meaning |
|---|---|
| 0 | complete for the declared coverage |
| 1 | answered, with findings, or `incomplete` |
| 2 | refused: malformed or ambiguous input, unsafe path, a set pin mismatch, an over-bound or occupied output |
| 3 | partial index write, kept |

## 8. Workflow completion seam (proposal plus prototype check)

When a builder adds or changes a module, the return carries a `module-change/1` record:

```
{"schema": "module-change/1", "module": {...}, "authorized_by": {"address": ADDRESS, "item": "#NN"},
 "old": {"declaration_id","version","sha256"}|null, "new": {"declaration_id","version","sha256"},
 "implementation": {"sha256","bytes"}, "evidence": [{"role": "return"|"test"|"demo", "address": ADDRESS|null, "sha256": hex|null, "note"}],
 "relationships": {"introduced": [{"requirement_id","reason"}], "changed": [{"requirement_id","fields": [str],"reason"}],
                   "removed": [{"requirement_id","reason"}]}}
```

**`delta` verifies mechanically:**
- the old and new files are valid declarations of the same module;
- `new.supersedes` names the old;
- the hashes equal the change record;
- the implementation equals the new declaration's;
- the computed added, removed and changed requirement ids equal the submitted ones (each mismatch is a finding);
- every requirement and provenance address is a full address;
- `authorized_by` is a full address with a `#NN` item.

**Prime reviews:**
- whether the relationships are true and sufficient;
- the reasons;
- the conditions;
- whether the module is ready for reuse.

An experimental or partial status is recordable. The old declaration is kept.

**Selecting an accepted version.** A later delivery checker consumes an explicit selection: a set's `select` entries, each naming `declaration_id`, `version` and the file sha. Prime writes them after review; the checker reads that set by hash. The declaration schema is not duplicated into the checker, and no authority is inferred from a file being present.

## 9. Limits

- Declarations are model-authored and may miss edges. String content is never interpreted as meaning.
- An implementation sha proves byte identity, not compatibility.
- There is no OS sandbox and no race safety.
- Remote links are never followed.
