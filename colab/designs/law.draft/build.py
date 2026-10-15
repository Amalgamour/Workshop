from pathlib import Path
import json, re

out = Path(r'D:\librarian\temp\law-design-build\payload')
out.mkdir(exist_ok=True)
files = {}
def put(name, text):
    files[name] = text.strip() + '\n'

sources = Path(r'D:\Git\Librarian\00.00.00.kernel.draft')
law = sources / '00.00.01.law'
syntax = sources / '00.00.00.syntax'
def source(path):
    assert path.exists(), path
    return str(path).replace('\\', '/')

axioms = source(syntax / '00.axioms/01.md')
seqaddr = source(law / '0018.seqaddr/01.md')
walk = source(syntax / '0014.design/01.md')
pages = {}
def page(number, title, sections):
    pages[number] = (title, sections)

page('0000', 'invariant', [
('Read', 'book-local', 'Enter through the book sentinel, then the contents. Open only the sections needed for the job. Page 0000 explains this reading arrangement; it does not replace the sentinel or desk startup.', 'This separates orientation from subject law and prevents every new sitting from reading the whole book.', 'Door -> contents -> named section -> required representation.'),
('Reserved', 'kernel-only', 'Pages 0001 through 0009 explain the face roles in this sample. The wider page reservation and coordinate widths remain owned by seqaddr. This book does not shrink that reservation to nine pages.', 'Face instruction occupies only part of the reserved page region.', 'Face teaching: 0001-0009. Reservation grammar: external seqaddr.'),
('Invariant', 'kernel-only', 'The invariant and its twin retain their syntax meaning. A book 00.md is its sentinel; no page receives a 00 face. Page 0000 is explanatory law about that arrangement, not a second door. The 99 sequence and retirement tail remain different things.', 'Making 0000 useful for reading must not erase its existing invariant job.', '00.md: container door. 0000: explanation. 99 sequence: twin. 09 tail: retirement.'),
('Foundation', 'kernel-only', 'Syntax governs the address grammar, axioms, and container walk. Law describes the face contracts. This design book has no desk or shelf, and cannot prove a working desk by itself.', 'A book sample can demonstrate the contract without inventing its missing enclosing axes.', 'Grammar/axioms/walk -> syntax. Face contracts -> law. Missing enclosure -> report.')])

page('0001', 'law', [
('Authority', 'kernel-only', 'Face 01 holds the normative conditions of its page. It governs those conditions only within the authority and subject scope that page lawfully owns. A filename, a draft stamp, a citation, or a section label grants no authority. This sample proposes a contract; it is not standing kernel law.', 'Without this limit, every local 0001 can accidentally redefine the meaning of every face.', 'Resolve owner + subject + state + lawful tie before treating a rule as binding.'),
('Use', 'kernel-only', 'A reader identifies the needed subject section, resolves its governing source, and opens the available representation needed for the job. Face 03 selects a route; face 01 establishes the rule; face 02 supplies its compact form; face 04 explains it. If a permission or condition is uncertain, reopen the governing file. A menu is not evidence that the rule has been read.', 'This is how a model uses a face, separately from how it constructs one.', 'Need -> section -> source -> representation -> read -> act only within existing permission.'),
('Stamp', 'kernel-only', 'A face begins with its face header and a stamp identifying version, authorization/state, face, page, book, keyword, why, and any relevant intent cite. Values must describe the actual artifact. This proposed complete stamp is not copied blindly from a live face. Draft names carry a three-digit version; seats do not. Exact lifecycle ownership stays with the existing version/approval laws.', 'A complete stamp prevents a copied header from claiming the identity or authority of its predecessor.', 'Proposed fields: version; Authorization; state; Face; PPPP; book; keyword; why; cite when relevant.'),
('Sections', 'kernel-only', 'Each section has a unique heading within its face and a declared job. The heading is the section key within the page, not a new seqaddr axis. In this sample, matching sections keep the exact same heading across faces 01, 02, and 04. A rename is a recorded change to the section and its routes together. Subject sections may be added; the contract does not prescribe one universal list of headings for every page.', 'Stable section keys let a clerk retrieve a precise piece without requiring literal copies of whole faces.', 'Section identity = page + heading. Representation = face. Heading changes require route updates.'),
('Construction', 'kernel-only', 'Write normative conditions on face 01, compact forms on face 02, routes on face 03, and recoverable explanation on face 04. A normative section states its scope, applicable conditions, required or forbidden result, and how a missing or conflicting source is reported. Those elements may be prose; they need not become repetitive field labels. Keep shell commands, routing tables, and extended demonstrations in their owning representations. References establishing a rule source are allowed: they are not executable commands.', 'The current no-address wording prevents the very source pointers required for reliable inheritance. This is an explicit proposed clarification.', 'Rule: scope + condition + consequence + missing/conflict handling. Example/template -> 02; explanation -> 04; route -> 03.'),
('Admission', 'kernel-only', 'A condition belongs in face 01 only if this page owns that subject and the statement changes what is required, allowed, or forbidden. A why, an observation, a proposed change, an unassigned idea, a task, and a navigation hint are not silently admitted as law. When authority is unresolved, retain the proposal and report the uncertainty; do not infer an override.', 'This is the boundary between useful thought and a governing constraint.', 'Owns subject? Normative effect? Lawful state? All required before binding admission.'),
('Scope', 'kernel-only', 'Each proposed section declares one owner class: kernel-only, desk-local, or book-local. These names are design metadata, not new numeric ranks. Kernel-only face mechanics are inherited. Desk-local policy applies within its lawful desk boundary. Book-local subject conditions apply only to their book. A local page 0001 may supply subject law without supplying or replacing the face contract. An approved exception must identify the exact source section and target scope; metadata alone cannot approve it.', 'A single local page may contain both local content and pointers to inherited rules, so whole-file inheritance is too coarse.', 'Resolve each section independently. Ownership class is not a promotion or an override.'),
('Inheritance', 'kernel-only', 'For each requested subject section, use the existing lawful container walk and declared parent proof. A local definition is usable only if it owns that subject and scope and agrees with inherited constraints, or has a lawful named approved exception. A local pointer continues lookup at its named source. An absent optional representation does not start a search. A required unresolved governing section is a defect. Detect loops and conflicting claims, keep the conflicting artifacts, and report the exact section rather than guessing from proximity.', 'Presence of a local 0001 must not stop lookup for every section. At the same time, a missing optional card must not trigger invented recovery.', 'Resolve subject section, then its representation. Reference != parent. Missing required source -> finding; optional face -> no minting.'),
('Correspondence', 'kernel-only', 'A supplied face 02 or 04 identifies the face 01 section it represents. Its conditions must agree with that section, while its form may differ. In this sample face 04 covers all supplied rule/card sections; face 02 is selective where a useful compact form exists. Face 03 inventories the supplied section routes. Face 08 appears only for actual relationships or source custody; it does not have to repeat every content section. A disagreement is recorded for authority review, not settled by majority vote.', 'Coverage can be checked without treating fractal reconstruction as copying.', '01 governs conditions; 02 compacts; 03 routes; 04 preserves why and recoverable meaning; 08 records connections.'),
('Validation', 'kernel-only', 'Before returning a face draft, check its identity, state, unique headings, section ownership, actual route targets, source pointers, and agreement across supplied representations. Check required coverage separately from optional absence. A valid shape is not approval. Automated checks must report structural failures and unresolved meaning separately; neither a successful parse nor a model self-check clears a lock.', 'This makes drift visible without pretending that a linter can decide human intent.', 'Structure check + semantic hostile pass + director review. Passing structure grants no state change.')])

page('0002', 'schema', [
('Job', 'kernel-only', 'Face 02 supplies a compact form of a named subject section: a card, template, or schema appropriate to that subject. It does not add normative conditions absent from face 01. These forms are named separately rather than treating every box as interchangeable.', 'A short usable form can preserve a rule without pretending that all compact forms serve the same job.', 'section: <heading>; source: <face 01 section>; form: card | template | schema.'),
('Coverage', 'kernel-only', 'Create a face 02 section when a compact representation serves the job. Its source section is explicit. This sample supplies useful cards for all teaching sections to exercise correspondence; that choice is not a universal requirement. If no compact form is needed, its face is absent and the menu omits it.', 'This prevents a template requirement from becoming compulsory duplication.', 'Useful compact form -> supply it. Unneeded face -> omit it.'),
('Agreement', 'kernel-only', 'Preserve the governing conditions, exceptions, and limits in the compact form. A card that changes a condition is a conflict even when its heading matches. Report that conflict with both source cuts. Read the actual governing file before a consequential write.', 'Alignment is meaning preserved across forms, not matching text or matching headings alone.', 'Same conditions, different form. Disagreement -> finding, retain both.')])
page('0003', 'operate', [
('Job', 'kernel-only', 'Face 03 is a header and a menu of named sections. A short explanation is optional. Each entry says what the section provides and links to the exact available face-section targets. Selecting a menu entry does not execute a command or establish a permission.', 'Routing should reduce reading without replacing the source.', 'Header -> optional explanation -> section menu -> exact targets.'),
('Selection', 'kernel-only', 'A clerk or model selects the needed representations of a section. A section may offer 01, 02, 04, and a relevant 08 relationship. It does not require all of them to be opened together. A rule question needs its governing 01; a compact use may need 02 plus the governing source when conditions are unclear.', 'The menu is the point at which narrow retrieval becomes possible.', 'Ask rule -> 01. Ask usable form -> 02. Ask reason/rebuild -> 04. Ask relationship -> 08.'),
('Integrity', 'kernel-only', 'Advertise only supplied targets. An absent optional face is omitted. A required missing target is a finding. A source link outside this page is explicitly identified as external. Rebuild the menu after section changes and verify each route; do not preserve an old route merely because its page number still exists.', 'A menu can look healthy while sending the reader to a reassigned page.', 'Existing target + right heading + right subject. Number alone is insufficient.')])
page('0004', 'user', [
('Job', 'kernel-only', 'Face 04 gives a readable account of the supplied rule and card sections. Each section carries its heading, why, and sufficient body to recover the conditions and understand the compact form. A why whose origin is unknown remains unknown.', 'The next model needs recoverable intent, not only a recipe.', 'Heading + why + recoverable conditions + explanation of important compact forms.'),
('Rebuild', 'kernel-only', 'Face 04 supports rebuilding a damaged representation from recorded meaning and the other available evidence. It does not authorize silently replacing face 01. A reconstruction remains draft until the lawful review and state transition occur.', 'Recovery and authority are different jobs.', 'Recover meaning -> mark draft -> review evidence -> lawful transition.'),
('Agreement', 'kernel-only', 'Explanation may expand context but cannot create an unapproved exception or remove a condition. Report a conflict against the governing section, keep both cuts, and explain which meaning is uncertain.', 'Natural language can drift as easily as a compact card.', 'More context is allowed. Changed conditions require review.')])
page('0005', 'ticket', [
('Task', 'kernel-only', 'Face 05 holds work about its page. Internal tasks use 05.01 through 05.49 and name a target plus an instruction. This teaching page describes that work; it is not a work queue for the whole book.', 'Local placement preserves what the work is about.', 'Task: id 05.01-05.49; local target; instruction; completion condition.'),
('Ticket', 'kernel-only', 'Outward tickets use 05.50 through 05.99 and require a path, an instruction, and a return destination. A ticket missing its path is invalid; a path without an instruction is not ready. Task and ticket ranges remain separate.', 'Outward work needs an explicit journey and return.', 'Ticket: id 05.50-05.99; outward path; instruction; return; completion condition.'),
('Boundary', 'kernel-only', 'A work item does not mint permission to edit, approve, lock, or promote law. Work may cite the governing source. Closing and reusing work slots follow the existing work law. This draft does not create live tasks merely by showing their template.', 'Instructions must stay within the authorization actually given.', 'Work record != approval. Example != dispatched job.')])
page('0006', 'note', [
('Placement', 'kernel-only', 'An insight lives with the page or active draft it concerns. A separate working note may capture the sitting before its findings are placed in the return. Face 06 is page-local memory, not a dump of unrelated ideas.', 'Placement makes the next sitting able to find the reason where the work lives.', 'Subject page/draft -> note. Sitting capture -> working notes -> placed findings.'),
('Lineage', 'kernel-only', 'Record what was observed, its source, what changed, why, and what remains unresolved. Do not rewrite past notes into a false history. Marks on an active draft are absorbed visibly into its next version rather than forgotten.', 'The record carries continuity that model memory cannot supply.', 'Observation; source; proposed/change state; why; unresolved.'),
('Boundary', 'kernel-only', 'A note can reveal a missing rule or trigger a proposed task, but does not itself change law or mint a ticket. Overflow belongs with its subject; an unrelated thought is not made binding because it appeared during a lawful write.', 'Unprompted insight is valuable precisely when its state and destination remain visible.', 'Insight -> record -> classify -> authorized next work. No silent law change.')])
page('0007', 'reserved', [
('Reserved', 'kernel-only', 'Face 07 remains absent until a lawful locked rule names its job. Page 0007 teaches that absence; it is not a face 07. No proofs, tests, fixtures, or speculative role are placed into face 07 by this sample.', 'Leaving an unassigned slot empty protects an honest boundary.', '0007 teaching page exists. No 07 face exists.')])
page('0008', 'map', [
('Job', 'kernel-only', 'Face 08 records where a design or relationship is found, with source custody where needed. It does not govern the target. A section route on face 03, a contents listing, and a parent proof are different records, even when they mention the same page.', 'The current maps conflate kinds of connection, allowing an ordinary reference to look like inheritance.', 'Route != membership != continuation != reference != structural parent proof.'),
('Relationships', 'kernel-only', 'This sample proposes typed relationship rows: member-of for idea grouping, continues-from for an immediate work chain, and references for an ordinary dependency or useful pointer. These labels describe connections and grant no authority. A structural parent still requires its existing lawful proof. No global single-parent rule is inferred for ideas.', 'Your example can have both a broader grouping and an immediate predecessor without corrupting the container address.', 'Example: 0015 member-of 0014; 0016 member-of 0014; 0016 continues-from 0015. Neither row changes seqaddr.'),
('Resolution', 'kernel-only', 'Resolve an address with the existing syntax walk and seqaddr grammar. Then inspect the named relationship or subject section. Do not walk every reference as a parent, scan sideways to guess a missing source, or choose by numerical proximity. An explicit source link may be followed for the named retrieval job; that is not an authority climb.', 'An address locates a thing; a relationship explains why the thing is relevant.', 'Locate -> verify identity -> inspect relation. Authority climb uses its own proof.'),
('Overrides', 'kernel-only', 'An exception row needs the exact source section, proposed target scope, difference, reason, and the approving record if one exists. A map row never approves itself. Existing law 0001 assigns an override role to its 08, while law 0008 places similar language on its 01. This sample retains that as a recorded conflict requiring director resolution; it does not create a functioning override registry.', 'Picking a home silently would bake an unresolved authority change into the template.', 'Exception request: source section + scope + difference + reason + approval evidence or pending.')])
page('0009', 'retire', [
('Marker', 'kernel-only', '09 is the retirement tail, not a page face. Page 0009 teaches retirement. A live page has no face 09. A retired artifact never governs current work.', 'The face range and lifecycle tail must stay distinct.', 'Faces: 01-08, with 07 reserved. 09: retirement tail.'),
('Transition', 'kernel-only', 'The current law describes released retirement as flagging and moving in one act into the owning book retirement warehouse, with its statement. This sample performs no retirement, creates no warehouse, and does not replace the existing lifecycle laws or their authorization.', 'A design example must not perform an actual state transition.', 'Released retirement -> flag + move together. Design review -> no transition.'),
('Read', 'kernel-only', 'Ordinary lookups pass over retired material. The syntax hostile axiom permits opening the named predecessor read-only before replacement. Current law also contains repair-only and strongest-version wording that does not cleanly agree with that axiom. The sample reports this conflict rather than inventing a new unified permission.', 'A cold start needs the contradiction visible before it can choose a predecessor lawfully.', 'Retired never governs. Predecessor-read policy conflict remains pending.')])
page('0010', 'about', [
('Identity', 'book-local', 'This is law.draft, a standalone design book showing proposed face and section contracts. It has no assigned desk, shelf, or book axis. Its name is the director-requested design name, not a deployed seqaddr address.', 'Truthful identity prevents a review artifact being mistaken for a kernel book.', 'Design identity: law.draft. Deployment address: unassigned.'),
('Purpose', 'book-local', 'The experiment is whether syntax plus law can explain a basic working environment without remembered layout rules. This sample exercises face construction and retrieval. It does not supply a whole desk, bands, registration, proof, command behavior, or approval machinery.', 'The face foundation must be reviewable before expanding the rest of the kernel.', 'Exercise: face/section contract. Desk completeness: not yet demonstrated.')])
page('0011', 'contents', [
('Contents', 'book-local', 'This page lists the actual pages in this sample, their jobs, and their entry faces. It is navigation, not an override map. It claims no registration authority. The syntax register remains owned by syntax.', 'A book needs a cheap way to discover its pages without moving registration into law.', 'Contents lists available pages; syntax register remains external.'),
('Bands', 'book-local', 'Pages 0001-0009 teach the face roles, 0000 explains the book door/invariant arrangement, 0010 identifies the book, and 0011 lists its contents. These groups are descriptive in this sample, not a replacement for the kernel behavior and structure bands.', 'A small demonstration should not smuggle in a new band allocation.', 'Teaching group + orientation + identity + contents; no new band law.')])

put('law.draft/00.md', 'This is law.draft, a standalone proposal book with no desk or shelf.\nOpen 00.readme.md first, then 0011.contents/03.001.md.\nIt is not standing kernel law and grants no permission to change the kernel.')
put('law.draft/00.readme.md', '''# law.draft — review door

This is a proposed book, dated 2026-10-10. Every face is draft version 001. None is a live seat. There is no enclosing desk or shelf, no invented proof, and no local syntax register.

Start with [the full face 01 contract](0001.law/01.001.md), then [its construction template and lookup examples](0001.law/02.001.md). [Contents](0011.contents/03.001.md) lets you choose the other pages without reading everything.

The field `owner` inside a section is proposed metadata: kernel-only, desk-local, or book-local. It records who should own the rule if adopted. It does not make this sample a kernel. Matching headings are section keys within a page, not new address axes. A local book may have its own subject-law page 0001 while inheriting face mechanics by section.

All links into kernel.draft are external dependencies. This sample is reviewable locally, but is not a self-contained boot pack. The physical folder name law.draft is a design name requested by the director; it has no deployed seqaddr rank.

Proposal boundaries and known conflicts are in [the review report](../law.draft-review-2026-10-10.md). That report contains the hostile findings. No design in this book changes the source kernel.
''')

def stamp(n, title, face):
    cite = {'0001':'1.2.8','0002':'2.8','0003':'3.5','0004':'4.8','0005':'5.8','0006':'6.8','0007':'7.8','0008':'2.6.8','0009':'6.9'}.get(n, '7.8')
    return f'# {face}\n\nversion: 001\nAuthorization: draft — 2026-10-10\nstate: draft\nFace: {face}\nPPPP: {n}\nbook: law.draft\nkeyword: {title}\nwhy: Proposed teaching contract for {title}; not standing law.\ncite: {cite}\n'

for n, (title, sections) in pages.items():
    base = f'law.draft/{n}.{title}'
    bodies = {f:stamp(n,title,f) for f in ('01','02','03','04')}
    bodies['03'] += '\nThis menu advertises supplied sections. Open the selected file and section before relying on it.\n'
    for heading, owner, rule, why, card in sections:
        anchor = heading.lower()
        bodies['01'] += f'\n## {heading}\n\nowner: {owner}\n\n{rule}\n'
        bodies['02'] += f'\n## {heading}\n\nsource: [01 / {heading}](01.001.md#{anchor})\nform: card\n\n{card}\n\nRead the source for its full conditions and limits.\n'
        bodies['03'] += f'\n## {heading}\n\n{why}\n\nMenu: [01 — conditions](01.001.md#{anchor}); [02 — compact form](02.001.md#{anchor}); [04 — why and meaning](04.001.md#{anchor}).\n'
        bodies['04'] += f'\n## {heading}\n\nsource: [01 / {heading}](01.001.md#{anchor}); [02 / {heading}](02.001.md#{anchor})\n\nwhy: {why}\n\n{rule}\n\nThe compact form selects the useful handle: {card}\n'
    for f, body in bodies.items():
        put(f'{base}/{f}.001.md', body)

template = '''

### Face template

This is a proposed construction form, not a live stamp. Replace placeholders with actual identity. Supply only sections this page needs.

```text
# 01
version: <next lawful three-digit version>
Authorization: draft — <date>
state: draft
Face: 01
PPPP: <four-digit page>
book: <actual book identity>
keyword: <page title>
why: <why this face exists; unknown if unknown>
cite: <relevant intent chain, if needed>

## <stable subject heading>
owner: <kernel-only | desk-local | book-local>
<conditions this page lawfully owns>
<source pointer when inherited; exact face and heading>
<missing/conflict handling relevant to these conditions>
```

An inherited section may be a pointer with the local application stated. Do not paste a kernel rule merely to make the face look complete. A source pointer must identify a real source; a placeholder remains a missing design input.

### Section lookup examples

These are hypothetical reader cases, not physical deployment addresses:

| Requested subject | What local 0001 contains | Result |
|---|---|---|
| Face stamp mechanics | A local stamp rule contradicting the kernel contract | Report conflict; file presence does not make the local rule win |
| Workshop intake conditions | A lawful book-local rule agreeing with inherited limits | Use the local subject section |
| Face section construction | A pointer to the inherited contract | Follow the exact named source section |
| A compact intake card | No optional 02 representation | Use the available rule/person form; do not mint a card or start a blind search |
| Required governing conditions | No lawful local or inherited source | Report required missing section; do not reconstruct from memory |
| Approved subject exception | A row with a real approving record and exact scope | Validate that record through the existing authority law; a row alone is insufficient |
| Parent lookup | A reference points back to an already visited source | Report loop and the visited section path |

### Optional-face example

This example demonstrates a menu line for a page with only 01 and 04 supplied. It is deliberately a text example, not an advertised link into a nonexistent fixture:

```text
section Intake: explains the local intake conditions
menu: 01 / Intake; 04 / Intake
02: not supplied because no compact form is needed
08: not supplied because no relationship record is needed
```
'''
put('law.draft/0001.law/02.001.md', files['law.draft/0001.law/02.001.md'] + template)

for n, heading in [('0000','Foundation'), ('0001','Inheritance'), ('0008','Resolution')]:
    title = pages[n][0]
    path = f'law.draft/{n}.{title}/02.001.md'
    put(path, files[path] + f'\n### External foundation\n\n[Syntax axioms]({axioms}); [syntax walk]({walk}); [seqaddr]({seqaddr}). These external sources are real dependencies; this sample does not overwrite them.\n')

put('law.draft/0001.law/08.001.md', stamp('0001','law','08') + f'''
## Scope

job: Source custody for the proposed section contract. These are references, not approval or structural parent proof.

| Section | Relation | Actual source | Design treatment |
|---|---|---|---|
| Authority | references | [syntax axioms / Nine]({axioms}#nine) | Preserve permission boundary |
| Inheritance | references | [syntax walk / Climb]({walk}#climb); [seqaddr / Walk]({seqaddr}#walk) | Use existing walk, resolve requested section separately |
| Sections | references | [current law / no-command]({source(law/'0001.law/01.md')}#no-command) | Propose clarifying rule-source pointers and section ownership |
| Correspondence | references | [current schema / Shape]({source(law/'0002.schema/01.md')}#shape); [current person / Job]({source(law/'0004.user/01.md')}#job) | Exact headings are proposed stronger convention |

## Overrides

No approved exception rows exist in this sample. Current [law 0001 / override]({source(law/'0001.law/01.md')}#override) and [law 0008 / Job]({source(law/'0008.map/01.md')}#job) need reconciliation before a registry home can be adopted.
''')
put('law.draft/0008.map/08.001.md', stamp('0008','map','08') + '''
## Relationships

The following are symbolic examples supplied by the director, not claims that these page subjects exist in this sample. They carry no deployment addresses or permissions.

| From | Relation | To | Meaning |
|---|---|---|---|
| example 0015 | member-of | example 0014 | Part of the broader idea |
| example 0016 | member-of | example 0014 | Also part of the broader idea |
| example 0016 | continues-from | example 0015 | Immediate predecessor in the work chain |
| another example page | references | example 0016 | Uses or cites it; does not become a group member or child |

A grouping may have multiple useful memberships if the eventual law allows them. This design does not silently impose single-parent idea ownership. Structural lineage remains separately proven.

## Overrides

No approved rows. A future request must name source section, target scope, difference, why, and approval evidence. Pending requests never become permission by appearing in a map.
''')

for n, headings in [('0001',['Scope','Overrides']),('0008',['Relationships','Overrides'])]:
    base=f'law.draft/{n}.{pages[n][0]}'
    menu=files[f'{base}/03.001.md']
    for heading in headings:
        if f'## {heading}\n' in menu:
            start=menu.index(f'## {heading}\n')
            stop=menu.find('\n## ',start+1)
            if stop<0: stop=len(menu)
            menu=menu[:stop]+f'\nRelationship/source record: [08 / {heading}](08.001.md#{heading.lower()}).\n'+menu[stop:]
        else:
            menu+=f'\n## {heading}\n\nRelationship/source record only: [08 / {heading}](08.001.md#{heading.lower()}). This is not a new law section.\n'
    put(f'{base}/03.001.md',menu)

listing='\n### Actual pages\n\n| Page | Job | Entry |\n|---|---|---|\n'
for n,(title,sections) in pages.items():
    listing+=f'| {n}.{title} | {sections[0][3]} | [section menu](../{n}.{title}/03.001.md) |\n'
put('law.draft/0011.contents/02.001.md', files['law.draft/0011.contents/02.001.md']+listing)
put('law.draft/0011.contents/03.001.md', files['law.draft/0011.contents/03.001.md']+listing)

put('law.draft-review-2026-10-10.md', f'''# law.draft — review and factfind

This is a new design proposal, not a patch or approval. The director requested a sample book without a desk or shelf. Source kernel files remain unchanged.

## Delivered shape

0000 keeps invariant explanation while adding how to read the book. 0001 separates use, construction, admission, scope, inheritance, correspondence, and validation. 0002-0009 teach the remaining face roles and lifecycle tail. 0010 identifies the book; 0011 is its contents. 01/02/03/04 are supplied as draft files on these teaching pages to make their agreement inspectable. 08 is supplied only where connection records are needed. No 07 or 09 face is created. No desk-only startup, live selector, proof, or register is invented.

The central design choice is per-section ownership and lookup. A local subject rule and an inherited face contract can share page 0001 without the local file replacing everything. Matching headings provide section keys within each page. Menus link exact supplied representations. They do not require opening all representations. Card coverage is optional outside this teaching sample.

## Explicit proposals requiring review

1. `owner` metadata uses kernel-only, desk-local, and book-local. These are ownership descriptions, not rank axes. The kernel needs a canonical section contract before a clerk can resolve them mechanically.
2. Shared headings across 01/02/04 are stronger than current loose correspondence. Renaming must update routes and recorded relationships together. This does not require identical prose.
3. Clarify the current face 01 prohibition on addresses: normative source references should be lawful; executable commands, routing tables, and extended demonstrations belong elsewhere. Without this distinction inheritance cannot be recorded reliably.
4. Proposed relationship kinds separate idea membership, immediate continuation, ordinary reference, and existing structural parent proof. They do not decide a single-parent rule or change seqaddr.
5. The sample specifies a fuller truthful stamp. It does not change lifecycle numbering or approval laws. Its `book: law.draft` is a proposal identity, not an assigned numeric book slot.

## Hostile findings / unresolved connections

- **Override owner conflict.** [Current 0001 / override]({source(law/'0001.law/01.md')}#override) places a heading exception on this page's 08. [Current 0008 / Job]({source(law/'0008.map/01.md')}#job) describes a row on that page. Syntax says maps do not govern. The sample records both; it does not pretend a registry home is settled.
- **Retired predecessor policy conflict.** [Syntax axiom 9]({axioms}#nine) requires opening the predecessor before replacement. [Current retire / Read and trailing patch]({source(law/'0009.retire/01.md')}) contains repair-only and strongest-version restrictions. Those predicates are not equivalent. No retirement or predecessor replacement occurs here.
- **Source contract is incomplete.** Current 0001 no-command bars section charts and addresses while inheritance and exact source references need somewhere to live. This draft explicitly proposes a boundary, not an unnoticed reinterpretation.
- **Existing baseline error.** The current kernel linter exits 1 with one reworked error: `00.00.14.notes` lacks book sentinel `00.md`. This is unrelated to the new design. No source repair was made.
- **Basic desk remains unproven.** This sample demonstrates the face foundation only. A real cold boot also needs syntax registration, container proof, bands, behaviors, and lawful state transitions. Supplying those by memory would hide the next work.

## Validation and limits

All supplied Markdown links are checked against actual files and section headings, including external source anchors. Draft identities, face/page correspondence, duplicate section headings, menu coverage, and reserved-face absence are checked. The assembled payload is checked before writing and the copied files are compared byte-for-byte afterward.

The existing linter was run on kernel.draft as a baseline. It is a desk linter and its standing stamp/seat assumptions do not encode this proposed section ownership contract. The book sample is therefore not claimed as an existing-linter pass. Link and shape checks cannot establish semantic agreement, lawful ownership, or approval; those need the hostile review and director's decision.

## Review cuts

Start with 0001 face 01, inspect its face 02 template and lookup examples, then test the menus on 0003 and the relationship distinction on 0008. Challenge whether each rule really belongs at kernel, desk, or book scope. The next useful step is one real local-book fixture with inherited face mechanics, once this contract is accepted.
''')
put('../notes/codex-law-design-2026-10-10.md', '''# Working notes — law.draft

2026-10-10. Authorized job: build a standalone sample law.draft book under colab/designs using kernel.draft as evidence. Do not patch or promote the kernel.

Finding: file-level inheritance is too coarse. Local subject law and inherited face mechanics need separate section ownership and exact routes. Build 0001 as the complete face contract; use 0002-0009 to demonstrate the representation boundaries. Include 0000 orientation/invariant, 0010 identity, and 0011 contents so the book can be read without imagined furniture.

Preserve: no 00 face on pages; 07 reserved; 09 lifecycle tail; versioned drafts; cards cannot add law; menu cannot govern; person face preserves why; maps do not grant authority; syntax owns grammar and walk.

Do not hide: 0001/0008 override-home conflict; syntax predecessor versus retire repair-only/strongest wording; 0001 no-address wording versus necessary source links. Baseline linter reports one existing notes-book sentinel error. New section metadata and strict shared headings are proposals, not approved rules.

Delivered record: designs/law.draft-review-2026-10-10.md. No kernel changes. Local old-session write root requires a single explicit escalation to place the verified payload in the moved project.
''')

# Validate real link destinations and headings before any write to the actual project.
headings = {}
def anchors(text):
    return {re.sub(r'[^\w\- ]','',h.strip().lower()).replace(' ','-') for h in re.findall(r'^#{1,6} (.+)$',text,re.M)}
for name,body in files.items(): headings[name]=anchors(body)
linkcount=0
for name,body in files.items():
    for target in re.findall(r'\]\(([^)]+)\)',body):
        dest, _, anchor=target.partition('#')
        if re.match(r'^[A-Za-z]:/',dest):
            p=Path(dest); assert p.is_file(),(name,target)
            available=anchors(p.read_text(encoding='utf-8-sig'))
        else:
            # Normalize lexically without using staged layout for actual-relative links.
            parts=[]
            for part in (str(Path(name).parent).replace('\\','/')+'/'+dest).split('/'):
                if part=='..':
                    if parts and parts[-1]!='..': parts.pop()
                    else: parts.append(part)
                elif part not in ('','.'): parts.append(part)
            key='/'.join(parts)
            assert key in files,(name,target,key)
            available=headings[key]
        assert not anchor or anchor in available,(name,target,'missing anchor')
        linkcount+=1
for n,(title,sections) in pages.items():
    for f in ['01','02','03','04']:
        name=f'law.draft/{n}.{title}/{f}.001.md'
        body=files[name]
        assert f'Face: {f}\n' in body and f'PPPP: {n}\n' in body
        assert 'state: draft\n' in body and 'Authorization: draft' in body
        hs=re.findall(r'^## (.+)$',body,re.M)
        assert len(hs)==len(set(hs)),name
        assert set(h[0] for h in sections)<=set(hs),name
assert not any(re.search(r'/(00|07|09)(\.|/)',n) for n in files if re.search(r'/\d{4}\.',n))
for name,body in files.items():
    if name.startswith('../'): continue
    p=out/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(body.encode('utf-8'))
# Keep notes in the manifest without writing outside staging.
(out/'manifest.json').write_text(json.dumps(files,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'files':len(files),'pages':len(pages),'validated_links':linkcount,'draft_faces':sum(bool(re.search(r'/\d{2}\.001\.md$',n)) for n in files)}))
