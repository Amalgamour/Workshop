# Field → source map (0707/05.13)
who: claude-opus-5-5 · state: proposal. The sources are those named in 0412/01 "Local work agreement" (T4 in the notes).

| Field | 0412/01 wording | Typical source cut today | New-pack cut (recommended) | Unknown blocks |
|---|---|---|---|---|
| goal | "goal" | pack `## Goal / method` or `## Question / selected evidence` | `## Goal` | `complete` and goal `completed` |
| scope | "authorized scope/resources" | pack `## Outputs / boundaries`, `## Deliverables / boundaries`, `## Scope …` | `## Scope` (included / excluded / allowed writes) | action release |
| prime_discretion | "independent Prime choices" | standing `0412.prime-review/01.md#Local work agreement`; director agreement ("80% … push it forward") | the same, plus an optional pack line narrowing it | a Prime-only release |
| director_required | "Director-required choices" | standing `0412.prime-review/evidence/director-agreement.md` (hard stop on judgment or forks); pack lines such as "genuine design forks remain proposals" | the same | nothing inferred; consequential acts wait |
| finish_criteria | "finish conditions" | pack `## Return …` or `## Deliverables / boundaries` | `## Finish` | pass `finished`, goal `completed` |
| recorded_decisions | "source-bound decisions/replies" | `06.NN` records with `## Director - verbatim` + `## Prime - exact proposal this reply approves` (0412/06.06, 06.08; 0710/06.02, 06.03) | the same pattern | answers cannot close holds |

**Measured design application** (`examples/views/application-0412-06.08.json`), mapping this pack read-only:
| Field | Cut | sha256 (prefix) |
|---|---|---|
| goal | `05.13.pack.md#Question / selected evidence` | 24e711363af1… |
| scope, finish | `05.13.pack.md#Deliverables / boundaries` | dc02be995dc3… |
| prime_discretion | `0412/01.md#Local work agreement` | b03ca6c2627d… |
| director_required | `0412/evidence/director-agreement.md` (whole) | 3b2a6ce8bc7d… (= the pack05.13 pin) |
| decision | `0412/06.08.md#Director - verbatim` ("Ok pack it") | 808e07977214… |

The decision answers `#Prime - exact proposal this reply approves`, limited to that proposal. **This is a design application, not a grant mutation.** Here scope and finish share one cut; a `## Finish` heading would separate them.
