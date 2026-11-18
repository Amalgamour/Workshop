# 06.01.review - Face 02 law draft, critical discussion pass
date: 2026-11-02
who: Codex Prime
state: useful design return; changes/decisions required; NOT ready for kernel-update execution

## Evidence and scope
Read the complete return, proposed 0002 draft, preservation/impact map, hostile analysis, kernel pack draft, notes and all six human/machine/input examples. Read current law 0001/0002 and additionally 0005.ticket, 0018.seqaddr and 0022.approve for ownership/lifecycle context. All 14 artifact rows and all 16 original input snapshots verify. Only live 0526/05.01 differs; its assignment bytes before Return pointer remain identical. Preserve that attributable in-flight record drift; do not silently refresh its snapshot. Four JSON examples parse; no schema/template/runtime conformance was established. No kernel files changed or staged by this review.

## What I support
M01. Replacing compact-only with declared working forms is substantive and useful. 0001 Correspondence explicitly limits 02 to forms shorter than the rule, so the change must include that clause, not only 0002. Keep shortness specific to cards, not a requirement on complete templates/schemas. The three cited 0001 references are a reasonable minimal starting impact set; they are not the entire impact set if executable files themselves become canonical faces.
M02. Separate kind/purpose, suppliers, optionality, explicit encoding, source/dependency identity and whole-artifact inspectability. Preserve 01 authority, 03 routing, 04 explanation and 08 relationships. Template examples must never impersonate a Director decision or approval.
M03. Exact source section correspondence and no silent removal are retained. The section map is valuable; keep it with the next revision rather than rewrite the old draft.
M04. Keep pack operations and module filenames out of general kernel law. The implementation and operator pilot still have to prove the intended behavior. Law does not make serialization mistakes impossible.

## R01 - Structure-versus-condition test is not sufficiently discriminating
Draft Requirements says a failed requirement is structure if the artifact could carry the same meaning in another representation. Many genuine conditions can be restated in another representation. Conversely, mandatory information can be present in prose while the required typed field is missing. The test does not reliably separate a semantic obligation from its encoding.

Example: a pack containing finish criteria in prose but not in a finish_criteria list violates a format requirement; a pack with no finish criteria anywhere violates an information/completeness requirement IF an authorized subject/task rule requires them. Both obligations need their appropriate source, but they are not the same condition. A required flag or count can also change meaning or scope; type/count alone does not make it mechanical.

Proposed direction: distinguish (a) required meaning/authority/behavior, from an owning 01 or recorded applicable task grant, and (b) the representational constraint implementing it, from the authorized form contract. Both name their grounds; a form must not narrow allowed meanings or introduce new permission/approval gates. Compute verifies source/shape; intelligence judges whether the claimed ground actually supports the requirement. Do not require the kernel itself to list every field of every local template.

## R02 - Staleness needs the governing selected revision, not a hidden newest rule
Sources says a copy whose form has changed is stale and is not used. This is too absolute. A new draft at the source must not automatically invalidate an approved explicitly selected predecessor; immutable historical copies remain valid evidence. A changed source actually governing this task can invalidate readiness, but existence of newer bytes elsewhere is not sufficient.

Use exact selected form/source identity and existing lifecycle/supersession rules. Changed bound bytes or lawful governing selection requires revalidation. Report historical/replay status separately. No auto-latest discovery and no universal ban on using preserved evidence.

## R03 - One subject can need several forms; selection is underspecified
Kind distinction is good, but the draft does not say whether the same source section can offer a card, template and schema together, or how compute/03 chooses one without duplicate section headings. Preserve one exact source heading; allow an explicitly identified internal form set OR decide the one-form limitation deliberately. Kind alone may not distinguish two templates of the same subject (e.g. initial creation versus revision).

Proposed direction: one subject section can expose named forms with kind/purpose/version/source; 03/profile selects the exact one. Internal form labels do not become a new seqaddr axis or conflicting 01 headings. Decide this before machine field identities are frozen.

## R04 - Compute forms involve an additional existing law, and execution is separate
Claude correctly reports no permission in its input set, rather than claiming draft code proves seated law. The Director has previously described module artifacts as 02.filename.VVV.filetype in this conversation; preserve that design intent rather than ask as if the idea were new. It is not proof that current law already encodes it.

Additional read: 0018.seqaddr Coordinate explicitly says a face is currently a .md file, later a row. Therefore admitting executable/config files AS canonical face-02 files may also require 0018 amendment, not just 0001/0002. Distinguish a 02 face declaring/owning a pinned implementation asset from the implementation file itself being the face. Either can be designed, but they have different naming/stamp/heading/retirement implications. A declared runner and kind never confer execution authority by themselves; existing runtime/lifecycle rules still apply.

## R05 - Pack form owner must be concrete without making all subject rules kernel law
The example honestly marks its owner and governing Pack heading unresolved; it is therefore illustrative, not an installable template. 0005.ticket has generic Task/Ticket rules, while dev workflow-specific requirements need their own lawful subject/source scope. Identify the generic face mechanics and the local pack-authoring subject owner separately. Do not automatically seat the current 0423 draft as law, or put every pack field on universal 0002. The present construction module remains a Director-invoked development experiment, not rejected retroactively because its kernel home is unfinished.

## R06 - Examples need actual form/input validation and clearer boundaries
Parsing four JSON files proves syntax only. The pack input gives open_choices as the string not-applicable while its shape says text-list with optional-or-not-applicable presence; the representation of that special state is not defined. Specify tagged/typed not-applicable handling before calling the pair conformant. Explicit null is absent from Fields' state list despite the pilot's nullable boolean being central; define field-specific distinction among not supplied, null, empty and not applicable where relevant.

HOSTILE H9's blanket prohibition of model-supplied paths conflicts with legitimate source/dependency selections and the person example's first_appearance address. Distinguish model-chosen semantic references from compute-generated output locations/numbering/hashes. The same care applies to identity: choosing what person/work is meant is intelligence/source work; assigning a collision-free representation is mechanical.

The person example computes a heading from the name but does not fully specify where/how it sits against the governing Person section. Clarify the output artifact/section relation and actual valid references before using it as correspondence evidence. Do not repair this by applying pack #NN rules to persons.

Construction obligations should be explicitly scoped to kinds that construct. A retrieval card and a validation schema do not necessarily build a whole new artifact. Law should not promise that every code bug disappears just because serialization is compute-owned. Preserve raw source bytes and declare permissible serialization transforms separately from semantic changes.

## R07 - Kernel-update draft is not executable lifecycle instruction
Read current 0018.seqaddr and 0022.approve. 0022 requires predecessor rename with retired stamp and relocation into this book's 00.retire.09 in the same seating act. Claude's exact target table/rollback is incomplete because it omits the warehouse and confirmation of lifecycle tools. Preserve Director approval versus compute/Prime execution; do not turn the change into manual Director file copying or assume re-seating bypasses the normal checks.

Before any implementation pack: determine actual current kernel/law draft lifecycle and tool support, stage candidates without touching seats, check current destination/version occupancy, review/sign/approve exact candidate identities, then use the authorized seating/retirement path. Rollback must preserve both versions and authority/history. No direct selected-file overwrite is released.

## R08 - This is a proposed amendment, not mostly wording cleanup
Four new kernel-only sections impose new obligations (field ownership, grounds, bindings/dependencies, construction/error behavior). They may be good rules, but should be reviewed as rules. Do not label all except compactness mere clarification or assume every old draft already complies. Classify implementation gaps against the prospective contract and preserve existing artifact status.

## Proposed discussion sequence
First settle the construction/meaning boundary (R01), then forms per subject and code/assets (R03/R04), then selected-revision semantics and field state/examples (R02/R06), then concrete ownership and lifecycle (R05/R07). Keep the positive 0001/0002 amendment direction. Write a successor Colab draft only after discussion; preserve all Claude return bytes. Compare that revision against Grok-1's returned module without changing either side silently. Do not seat or release the kernel update now.

## Did / Blocked / Need
Did: full artifact/source analysis and integrity checks, extra lifecycle/ownership source reads, explicit critique and proposed directions.
Blocked: exact law wording/examples/home/lifecycle are not yet ready for execution.
Need: Prime/Director discussion of the identified semantics, then a bounded Claude revision with actual validation examples and impact accounting. No runtime test, model launch, kernel edit, Git write, approval or seating was performed.
