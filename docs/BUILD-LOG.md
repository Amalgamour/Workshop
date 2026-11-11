# Build log

Every build choice, its why, and the spec line it follows. A choice the spec does not settle is marked 7 (missing) and raised, not invented.

[APP] Reader is Next.js 15 App Router + TypeScript, plain CSS (no Tailwind) to keep the build small. Why: AGENTS.md "Use NextJS ... clean and smooth design"; Design.md App = TypeScript, Next.js.
[APP] The app reads only through lib/compute.ts -> COMPUTE_URL (default http://127.0.0.1:7700). The browser word box goes through a GET-only pass-through (/api/compute/brands|links|page|face|cards). Why: format.md 1.2, only the compute owns books.
[APP] Core-as-WebAssembly (Design.md "uses the core as WebAssembly") is not done: the reader does no validation of its own, it only displays the compute's answers. 7 until the core crate exports wasm.
[APP] Mock compute app/mock/server.mjs: read-only replay of books/*.book (+ kernel/*.book), fixtures if none. Replays put, tail (checks from), copy (to FF.draft), promote; note/merge/use/snapshot are shown in history only. POST /propose always rejects ("mock is read-only").
[APP] Finding: CONTRACT.md says "local face wins, else go up to kernel"; spec seqAddr.md 2.5 says book -> shelf -> desk -> kernel. Spec wins: the mock walks all four, and resolved_from may be "shelf" or "desk" as well as local/kernel/missing.
[APP] 7 provisional: /page faces map keys are face part only ("01", "01.draft", "05.00", "05.01"). Contract shows only "01". Chose this so drafts and counters are visible; isolated in mock pageView().
[APP] 7 provisional: /links forward = full page addresses (DD.SS.BB.PPPP) written in face 08; back = other pages whose face 08 names this page; also returns one_way (target exists but no back-link, seqAddr 7). Spec C4 (how 08 links are held) is open.
[APP] 7 provisional: /brands returns brand = card address (contract) plus brand_id (ham.001), is_default, forms, exact_form, dictionary. The word box states back: the one brand whose forms hold the exact typed form, else the dictionary default. Why: brands.md steps 1-2 need meters and session history the reader does not have.
[APP] Times are shown in Toronto time with the raw UTC beside them. Why: the Director's zone; "trust but verify" keeps the raw value visible.
[APP] Missing faces show as a dashed hole with a 7, "a hole nothing requires stays empty: a header and a why" (Axioms 7), and a link to the resolve trace. Missing board with counters is shown as a defect (seqAddr 5.7).
[APP] Card matching asks /face/{page}.04 when a page has a 01/02 card but no own 04 card, so an inherited why is shown instead of a false hole.
[KERNEL] 2026-11-11 Seeded kernel/00.00.00: pages 0000, 0050 axioms, 0051 seqaddr, 0052 faces, 0053 tails, 0054 types, 0055 brands, 0056 drafting, 0057 workflow-loop (from workflow-loop.003.md). Text copied from docs/spec with line sources in kernel/MAP.md.
[KERNEL] All content faces are FF.draft; none seated. Why: drafting.md:20 (a new face starts as a draft), axiom 9, no Director approval.
[KERNEL] 7: axioms page number open (decisions.md E8); chose 0050, first structural page (seqAddr.md:223). Order of 0050-0099 pages spec-silent; chose brief order.
[KERNEL] 7: stamp state values and whether face 00 takes a tail spec-silent; chose bare 00 file with state: draft inside.
[KERNEL] 7: kernel base dictionary (C8.5) has no listed words; page 0012 not seated in the kernel.
[KERNEL] 7: missing whys written as `why: 4.7`; missing person-facing 04 bodies written as a 7 hole. Required by C3.2, so raised, not filled.
[KERNEL] Finding: brief asked for a stamp on every face; decisions.md:176 says faces carry no stamp. Spec followed.
[KERNEL] Finding: boards FF.00 are required (decisions.md:196) but never written (format.md:102); builder writes counters without boards. See kernel/CONFLICTS.md K02.
[KERNEL] 7: seed timestamp fixed at 2026-11-11T19:30:00Z for determinism; one proposal id per page.
[KERNEL] kernel/build.mjs writes books/00.00.00.book plus samples 10.00.00, 10.11.00, 10.11.21 (inheritance override at 0056.04; Bob test brand cards at 1001.01, dictionary 0012.03.14/16).
[KERNEL] kernel/CONFLICTS.md: 15 spec-vs-spec conflicts (K01-K15) and 15 workflow-loop .002 vs .003 differences (W01-W15). None resolved.
