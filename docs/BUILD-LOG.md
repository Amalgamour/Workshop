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
[TRIAL-K] 2026-11-11 Hostile pass on kernel/ and books/ (axiom 9), judged against the spec plus ruling R1: 2 blockers, 8 majors, 11 minors. See docs/trial/kernel-trial.md. Findings only; the kernel was not touched.
[TRIAL-K] The build is deterministic (two clean builds identical, --check passes). The 54 book entries replay byte for byte to the kernel files. All 01/02 card sentences were found word for word in docs/spec.
[CORE] 2026-11-11 crates/seqaddr-core (Rust): grammar (seqAddr 8), JSONL book log (format 3), tail/claim rules (workflow-loop.003 6), resolver (A1.8), proposal validation (format 4.1), CLI `seqaddr`. API in crates/seqaddr-core/API.md. Every switchable choice below lives in `state::Policy`.
[CORE] R1 applied: the full-zero sentinel is named door in types and errors (Sentinel::Door, AxisRole::Door, PageKind::Door, FaceJob::Door, CounterRole::Door, door_page, has_door).
[CORE] 7 provisional: boards. A4.4 (decisions.md:196, seqAddr.md:197) says a face is counted iff FF.00 exists; format.md:102 says FF.00 is never written. Chose: faces 05/06 always counted, plus Policy.extra_counted (default 0012.03, from C8.3); board derived, `put` to FF.00 rejected.
[CORE] 7 provisional: FF.00 and FF.99 take no tail (spec silent; board is derived, 99 is a pointer "never content" A5.1).
[CORE] 7 provisional: a counter is created bare, `draft` or `pack` only; `put` on a counter still in `draft` replaces its body (a pack being written; lint-fail stays draft). Otherwise put never replaces.
[CORE] 7 provisional: `tail` op names the slot without a tail; bare is absent/"" in from/to (no `closed` word, A2.5). `put` tail may be in the address or the `tail` field; they must agree.
[CORE] 7 provisional: faces retire only from seated (bare -> retired); a retired face blocks a new put (removal op undefined). Pages retire by tail op bare -> retired on the page address; page draft state is derived (only drafts, C1.2), not a tail op.
[CORE] 7 provisional: D0 enforced by default (Policy.enforce_drafting): seated face changes only by copy/note/merge/promote; `merge` cites its note in field `cites` and carries the whole new draft body; `promote` needs every note struck, no review gate (E7 trial not modeled).
[CORE] 7 provisional: claims (S11) - claim id `claim-{n}`, owner = `by` of pack->open. open->return only by owner or Policy.compute_name; return body appended to the same counter. return->review records `by` as reviewer, must differ from builder. review->bare requires `outcome` (S03); `abandoned` only if compute made the return. Heartbeat/lease/fencing not built (wl.003 6.4 says 7).
[CORE] 7 provisional: entries of a multi-op proposal carry `proposal` ("p{first n}") and `of` (count); a trailing proposal cut short is dropped whole on read, so all-or-nothing survives a crash. Snapshot carries full state in field `state`, addr = book address. `use` stored as a record; `by` must be compute.
[CORE] 7 provisional: identity/door first - no write in a book until DD.SS.BB.0000.00 exists (format 4.1 "identity page first"). C1.1 also applies to page 0000 (Policy.c1_on_door_pages). Finding: format.md:74 example writes 0000.00 alone; as a proposal that fails C1.1. Replay does not run page checks, so the example replays.
[CORE] 7 provisional: proposals write one book only (cross-book transactions open, wl.003 10). Faces 07, 09, 10-99 rejected as reserved (A4.3). Face 03 outside kernel/desk books only on 0001-0099 (C6) is hard.
[CORE] 7 provisional: C3.2 checks the newest view (draft if any, else seated) of 01/02 against 04; cards of types rule/schema need a 04 card; unknown card types are findings; bad `axioms:` chains are hard (E3). Back-links (A5.3) checked for face 08 `target:` cards on pointer pages (9999, PP99, any 99 container); the target page's face 08 must name the pointer page.
[CORE] 7 provisional: card key title form - non letters/digits collapse to one hyphen; key must start with a letter and not be a tail word. Stamp = `---` front matter or leading field lines.
[CORE] Finding: seqAddr.md:110 says a word after DD/SS/BB is a title, but the grammar seqAddr.md:266-269 allows a title only at the end. Grammar followed: `10.tools.21.4442` is invalid.
[CORE] Finding: decisions.md:432 calls `0012.03.00` the dictionary menu (content), but format.md:102 says FF.00 is derived and never written. Core treats it as derived.
[CORE] Finding: wl.003:175 says review starts "on a valid reviewer claim" but gives no claim shape; core uses the tail op author as reviewer.
[CORE] wasm32: core has no fs/clock without feature `fs`; `cargo check --target wasm32-unknown-unknown --no-default-features` fails only because the wasm32 std is not installed on the box (no rustup). Not verified. No wasm-bindgen glue yet.
