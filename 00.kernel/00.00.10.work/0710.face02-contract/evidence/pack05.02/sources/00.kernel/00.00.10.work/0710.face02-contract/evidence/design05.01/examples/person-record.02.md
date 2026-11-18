# 02

version: 001
Authorization: draft — 2026-11-02
who: claude-opus-5-5
state: draft. **EXAMPLE ONLY**, 0710/05.01 design evidence, for an ordinary subject book. The book, page and content are synthetic.
Face: 02
PPPP: 0201
book: 10.00.01.people (synthetic)
keyword: person
why: Template for one person record in this book.

## Person

kind: template
source: face 01, section `Person`, of this page (synthetic). It states one condition: "a record names one person and the page where that person first appears."
encoding: UTF-8
machine form: `person-record.template.json` (a proposed format)

```text
[C] Header: record identity (book, page, the section heading derived from the name), draft stamp, date of record, template identity
[I] Name                                   required   (condition ground: the 01 sentence above)
[I] First appearance: which page; [C] checks that the address resolves   required (condition ground: the same sentence)
[I] Role, in a few words                   optional
[I] Description                            optional
[I] Aliases                                optional, a list; each entry is a plain value, no numbering
[I] Relations: (relation word, other record)   optional; the other record must resolve
[C] Relation addresses resolved; face 08 rows proposed for page relationships (not written by this form)
```

**What this form does not inherit from the pack form:**
- **No `#NN`, no passes, no N5NN/N1NN route, no review digest, no freeze.**
- Aliases repeat, but this form declares no identity scheme for them, so compute assigns none.

**Requirement grounds:**
- **Name and first appearance:** condition ground (the stated 01 sentence).
- **Field order and UTF-8:** structure ground.
- **"Role must be one of hero/villain/minor":** if added here, that would be a new condition. It must go to face 01 first (law Requirements).
