# Draft pack, 90.50.10.0418 (seated-05 in seqaddr-core)

Not published to packs. Not inited. 23 Nov 2026, Prima, t517u-t520u.

Why this draft stays here: seqaddr-core lives on prima/build. It is not in the work/returns repo at a823ee28, so `wf pack` with `repo: work` cannot start this page there. A later pack needs a repo that holds the crate (or the crate brought into work). Suggested address 0418 is unused; Prima sets it at init.

Suggested grant (disjoint from wave 1's 0407, 0408, 0419 and from 0702): `crates/seqaddr-core/src/state.rs`, `resolve.rs`, `validate.rs`, `face.rs`. Grant-ref to confirm: t512 approved the rule change; t517u asked Grok builders to build the core's local infrastructure. There is no path grant like t461u for this crate yet.

Builder for wave 1, when packed: Grok-4. Checker: Grok-Check (`wf check --as Grok-Check`).
