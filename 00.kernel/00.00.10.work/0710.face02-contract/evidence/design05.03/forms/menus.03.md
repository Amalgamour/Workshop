# Menus (face 03), one per page — ILLUSTRATIVE, 0710/05.03
who: claude-opus-5-5 · state: draft. This repairs the combined 05.02 menu. A face-03 menu belongs to one page (0003 Job), and a route outside the page is marked external (0003 Integrity).

## `00.00.10.work/0423.dev-authoring/03` — section Pack
- rule: `00.00.10.work/0423.dev-authoring/01#Pack`
- forms at `00.00.10.work/0423.dev-authoring/02#Pack`:
  - `pack-card`: card. What a pack holds.
  - `pack-create`: template. Build a new pack draft from its N4NN source.
  - `pack-revise`: template. Change one item of an unfrozen draft.
  - `pack-check`: schema. Check a built draft before review.
- external: `00.00.01.law/0005.ticket/01#Task` (generic work-item law)

## `10.00.01.people/0201.person/03` — section Person (synthetic book)
- rule: `10.00.01.people/0201.person/01#Person`
- forms at `10.00.01.people/0201.person/02#Person`:
  - `person-card`: card. What a person record holds.
  - `person-create`: template. Create one person record.
- external: `10.00.01.people/0202.register/01` (where created records are written)

**Selection** names the page, the section and the form, for example `00.00.10.work/0423.dev-authoring/02#Pack` + `pack-create`. **That is a route plus a selector, not a new address axis.** A profile may do the same if its mapping names these three plus the revision.

Machine form: `menus.json`. The validation cases M1–M4 check these routes against the fixture.
