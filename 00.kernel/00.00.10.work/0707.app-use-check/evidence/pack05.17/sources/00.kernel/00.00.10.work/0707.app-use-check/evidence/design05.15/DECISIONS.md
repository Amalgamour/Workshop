# J1–J3 and compatibility dispositions (0707/05.15)
who: claude-opus-5-5 · **Prime's 06.14 findings are technical directions, not Director quotations.** No Director decision is needed for these mechanical corrections.

| Item | Disposition | Evidence | Owner |
|---|---|---|---|
| **J1 fences** | **fixed** with a bounded grammar (backtick and tilde, length, indent ≤3, closing rule). An unclosed fence or an ambiguous indented heading is **refused**. The pack cut and block extraction use the same scanner | KR-tilde, KR-long_backtick, KR-indented, KR-pointer; A-unclosed, A-longer-close, A-indented-heading | technical |
| **J2 binding paths** | **fixed:** full binding validation on inspect, compare and reconcile, through one checked resolver before any read; old schema versions refused | KR-binding-path; A-pack-path; A-binding-shape; A-junction (source) | technical |
| **J3 output room** | **fixed in the lab:** a required `--lab-root`, with markers, links, containment, in-book and occupancy all checked before creation. **Not OS confinement;** a production host must enforce its own write scope | A-room, A-mock-checkout, A-junction (output) | technical; a host write scope is a builder item |
| **Compatibility** | **confirmed by observation, not approximated:** an exact frozen-helper observation as `legacy_observation`; the helper defects are reported (CRLF, fenced Goal, empty versus absent, dropped bullets) | C-* cases; `COMPAT.md` | technical; **a fix to the CRLF and fence behavior of the core is Prime's choice** in a core successor |
| Passive and R1–R5 safeguards | **kept** | compat16 (16/16) + W-flow | — |
| A mandatory block or a new release rule | **not introduced** | — | would be a Director decision if ever wanted |
