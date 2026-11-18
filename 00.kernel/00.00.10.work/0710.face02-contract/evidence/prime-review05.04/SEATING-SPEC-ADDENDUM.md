# Mandatory additions to the bounded seating-tool specification
date: 2026-11-02
source: 0710/06.04.review, independent P1/P2 and specification P3
state: Prime review requirements for a future build, no implementation or execution release

1. Bind plan to exact qualified release/page/face and independently selected approval/source identities; validate plan/images on every run/resume. A swapped valid plan from another page must hold, not verify that other page.
2. Revalidate exact rollback decision and its applicability on every resume; changed/missing/swapped decisions after R1 must hold without additional writes.
3. State-specific write accounting: zero-write preflight refusal; preserved journaled partial execution; zero additional writes on a held recovery. Never promise all-or-nothing across two faces.
4. Explicit bounded target-book and work-page evidence roots. Version/who preserved; only reviewed stamp lines mutable. Raw image and ledger/record write scope is declared.
5. Preserve the original 35 fixtures and Prime's four current probes. Add plan/image/decision misbinding and state-boundary cases, with exact expected source/destination hashes, first failures and reported writes.
6. One bounded CLI first; no active app selection, kernel seating or layout adoption without the subsequent named review and Director releases.
