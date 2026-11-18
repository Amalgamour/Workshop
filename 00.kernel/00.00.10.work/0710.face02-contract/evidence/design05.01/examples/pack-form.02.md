# 02

version: 001
Authorization: draft — 2026-11-02
who: claude-opus-5-5
state: draft. **EXAMPLE ONLY**, 0710/05.01 design evidence. It shows how a template sits on a face 02 under draft law 0002 v004. Not seated, not a release, not Grok-1's template.
Face: 02
PPPP: PPPP (the page whose face 01 governs pack shape; **not identified in the inputs**, finding F4)
book: 00.00.10.work
keyword: (that page's keyword)
why: Template for an N5NN work pass built from its N4NN source.

## Pack

kind: template
source: face 01, section `Pack`, of this page. **The heading is assumed for the example;** the real one is the governing 01 heading.
encoding: UTF-8
machine form: `pack-form.template.json` (beside this example; a proposed format, not kernel language)

Who fills each part: **[C]** compute derives it, **[S]** a declared source supplies it, **[I]** intelligence supplies the meaning.

```text
[C] Header: page/pass identity, draft stamp, date of record, template identity and version
[S] Source: the N4NN page and pass, retrieved through the registered source→work relation (never by swapping a digit)
[S] Notes: the declared note inventory, with attribution
[I] Goal                                   required
[I] Scope: included / excluded / allowed writes   required
[I] Finish criteria                        required
[S|I] Executor, reviewer                   from the source if stated; otherwise asked for
[I] For each declared note: disposition (integrated #NN | deferred, with why | rejected, with why | unresolved)

repeat item  (identity: #NN, assigned by compute in order, never renumbered silently)
  [I] Title                                required
  [I] Purpose and change                   required
  [I] Requirements and boundaries          required
  [I] Interfaces and dependency references optional
  [I] Observable acceptance and evidence   required
  [I] Note/decision references             optional
  [I] Open choices                         optional; may be declared not applicable
  [C] Resolved references, pins, validation feedback
end

[S] Dependencies: resolver results (resolved | missing | stale | conditional | ambiguous)
[I] A missing relationship or environment detail, only when the resolver asks
[I] Review: the assessment of the exact whole draft
[C] Draft and review digests; frozen source manifest; output path; return intent derived from the N5NN→N1NN / N7NN rule
[C] Footer: release is separate; nothing is approved or launched
```

**Requirement grounds** (law Requirements):
- **Goal, scope, finish and acceptance:** condition ground. Each needs a governing 01 sentence on the owning page. **If none exists, they are findings,** not checks.
- **The `#NN` scheme, the field order and UTF-8:** structure ground.
