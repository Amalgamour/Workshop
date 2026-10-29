# Shared Colab/workflow interface v1
Status: Director-approved placement; Prime proposed implementation interface. No code
or live investigation is created by this file. Both builders read these exact bytes.

## Three identities
0411.colab is module DESIGN.0510.colab-tools/05.02 and 0511.workflow-colab/05.01 are
IMPLEMENTATION jobs. Actual design investigations live under the declared N7NN
band, with their own05.NN passes. Their SUBJECTS can be any declared page/file/
section: targets are not the investigation origin or the implementation job.
Example 0701.desk-state is illustrative; it is not an existing investigation or
Director release. The real first investigation opens after Prime uses the tool.

## Binding
binding.schema.json is a data specification; standard-library validators can
implement its rules without installing a JSON-schema dependency. binding.json
contains schema, investigation{book, page, pass}, targets[]. T ids are unique, as are
exact duplicate targets. source.kind is implicitly fixed Git blob in v1: repository
label, full commit, path and sha256. Repository roots are provided by the caller in
local configuration; local paths are not portable recipient access. Include selected
bytes/snapshots in the package. Never silently follow HEAD or retarget changed text.
Each target names book/page/file and optional section; null means whole named file.
No claim of whole-page coverage from a single file. heading.value is the exact
heading line including Markdown markers; occurrence is explicitly1-based when
needed. An omitted/null occurrence is valid only for exactly one match. Duplicate
headings without explicit occurrence refuse. id selects an explicitly declared
section id; do not invent ids or fuzzy-match headings. Keep file hash binding.
Use source path and declared book/page/file consistently. Unresolvable/mismatched
section is attention/refusal, not a choice of a similar section. No new SeqAddr axis.

## Package interface
Claude produces a fresh external package with binding.json, ENTRY.md, 05.NN.md,
06.NN.md (supplied purpose/reason only, not invented findings), RETURN-TEMPLATE.md,
source-manifest.json/snapshots and verification/digest metadata. Existing pack helper
may add files required by its contract. Document exact complete output manifest.
Use a deterministic digest bound to request, binding and selected output/source
bytes. The workflow adapter consumes the VERIFIED directory/package at the expected
digest; don't parse free prose to rediscover identities or grant permission.
Package filenames are canonical, no .colab tail. Named pass drives05.NN/06.NN names.
Optional scoring/evaluator artifacts are separate when a blinded method is chosen.

## Workflow attachment
Grok1 implements opening a declared investigation and attaching a verified package
into that investigation's05.NN/06.NN record without altering package bytes/identity.
No live seat mutation; the draft stays draft until normal release. Returns reuse
0100 capture. The reserved origin is investigation book/page/pass, NEVER the target
subject page or module implementation batch. Claude intake delegates capture with
that explicit reservation; Grok validates a later pointer by inspector and binding.
Neither receipt nor a role/model label releases, accepts or completes work. A pending
review stays visible. Prime supplies judgments/dispositions; deterministic code
records them, source bindings and follow-up/park links without guessing adequacy.
Issue notes and authorized follow-up work link back to the SUBJECT page; preserve
page-local why rather than dumping every reason only on 0700. Return body remains
in its captured member, not a second editable copy on the Colab pass.

## File ownership and parallel work
Prime owns this interface, 0411 design and band 0700 declaration. Claude owns new
labs/colab-support-pass01 and 0510/05.02 outputs. Grok1 owns new labs/colab-workflow-pass01
and 0511/05.01 outputs. Neither edits the other's active files or shared interface.
Grok builds contract-valid SYNTHETIC package fixtures; Claude builds a REAL-source
package. Cross-module integration happens after both returns are reviewed; neither
claims to have run the other's unfinished code. Record interface gaps for Prime.
No accepted app/helpers/law/00.live/assignment/other-lane source changes. Existing
N5NN jobs and historical Colabs remain in place; add links, don't migrate captures.
Face 07 is unallocated for workflow. SoF's 07 media is a different local contract.

## Readability correction — 2026-10-29
New text version of `CONTRACT.md`. Original and any sealed copies remain unchanged. This version corrects spacing; it does not release execution, rewrite captured evidence or grant a new review decision. Current audit/holds: `00.kernel/00.00.10.work/0412.prime-review/evidence/drift-audit-2026-10-29/STATUS.md`.
