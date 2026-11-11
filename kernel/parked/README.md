# Parked (not built)

R21 (docs/spec/DIRECTOR-RULINGS.md:82-84): "No overrides for now. we build them in." While the Workshop app itself is built, nothing is changed by an override page. The sample R7 override page `10.11.21.0001` is parked here, unchanged, so it is kept for child desks later but not read by `kernel/build.mjs`.

- `10.11.21/10.11.21.0001.00.draft.md`, `10.11.21/10.11.21.0001.04.draft.md`: the R7 sample (TRIAL-K2 finding 17: its body is chat t42u, not spec; moot while parked). Its face 00 keeps the pass-3 registry layout (not converted to face00.md).
- QUESTIONS Q36 (does an override change what the lookup returns) is moot under R21.

## doors/ (lane PACKS, 2026-11-11)

R22 (docs/spec/DIRECTOR-RULINGS.md:86-88) asks for a face 05 on each page: what was learned (05.01) and the MVP work pack (05.02). R10 (:40-41) says a door page 0000 holds only face 00, and `kernel/build.mjs` refuses any other face there. So the 05 drafts for the four door pages are parked here, unchanged in form, and not built:

- `doors/00.00.00.0000.05.01.draft.md`, `.05.02.draft.md` (kernel door)
- `doors/10.00.00.0000.05.01.draft.md`, `.05.02.draft.md` (desk door)
- `doors/10.11.00.0000.05.01.draft.md`, `.05.02.draft.md` (shelf door)
- `doors/10.11.21.0000.05.01.draft.md`, `.05.02.draft.md` (book door)

Where a door page's lessons and pack belong is QUESTIONS Q39. Nothing here is law.
