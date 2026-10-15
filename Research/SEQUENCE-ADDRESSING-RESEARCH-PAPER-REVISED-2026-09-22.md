# Sequence Addressing as a Structural Interoperability Kernel

## A Revised Design, Security, API, and Research Assessment

**Author and originator:** Matthew John Fisher  
**Revision date:** 2026-09-22  
**Research window assessed:** 2026-09-15 through 2026-09-22  
**Document status:** revised research paper and architecture proposal; not yet a ratified specification

> **Rights notice.** The concepts and original work described in this paper are the work of Matthew John Fisher. Matthew John Fisher retains all legal rights in the United States. AI systems assisted with analysis, adversarial review, research synthesis, and drafting; that assistance does not transfer ownership. This notice records the author's claim and is not legal advice.

## Abstract

Sequence Addressing, or **Seqaddr**, is a proposed structural interoperability kernel for locating and governing objects across software, documents, human workflows, and model contexts. Its current canonical form, `DD.SS.BB.TT.PPPP`, originated as a readable hierarchical address. In one week of iterative colab, Librarian work, hostile fixtures, and successor rewriting, it developed into a broader design: addresses are separated from identity and authority; object roles are separated from presentation faces; searches return bounded evidence while refusal policy owns admission; lifecycle changes are expressed through successors rather than destructive rewriting; and invalid or ambiguous states produce named halts with evidence.

The central thesis is narrow. Seqaddr should not attempt to encode all business logic or become a universal ontology. It should provide a small, deterministic semantic layer—the same kind of stable starting point across otherwise different applications—while leaving domain logic, transport, storage, and user experience open to extension. An application then integrates once through an adapter manifest and exposes a small operation algebra such as `bind`, `resolve`, `find`, `read`, `walk`, `propose`, `commit`, and `why`.

This paper consolidates the architecture, distinguishes the validated observations from the speculative claims, positions Seqaddr against existing standards, presents a threat model, proposes conformance profiles and an experimental program, documents the one-week development delta, and estimates the conventional replacement cost of reaching the current research state. It concludes that Seqaddr is promising as a transport-neutral “narrow waist” and as a model-readable governance environment, but it is not yet a production protocol or security standard. Its next proof must come from a formal grammar, canonical bytes, typed registries, independent adapters, conformance fixtures, measurements, and external review.

## 1. Research question

Most integrations begin by rediscovering the same structural questions:

- What object is being named?
- Where does it live?
- Which representation is being requested?
- Which record is current?
- What evidence supports that answer?
- What may the caller do?
- How does the system refuse ambiguity or conflict?
- How can a person or model understand the decision without loading the entire application?

Existing protocols answer important parts of these questions. URIs provide generic identification syntax; HTTP supplies transport semantics; OpenAPI describes HTTP interfaces; MCP connects model applications to tools and resources; identity and provenance standards support verification and lineage. The repeated gap is not the absence of another transport. It is the absence of a small shared structural contract that applications, people, and models can use before entering application-specific logic.

Seqaddr asks whether a deterministic hierarchical address, typed structural roles, bounded evidence, governed lifecycle, selective faces, and explicit refusal can form that contract.

## 2. Scope and claims

### 2.1 In scope

Seqaddr aims to standardize:

1. canonical structural addresses;
2. schema-bound parsing and comparison;
3. structural roles and presentation faces;
4. registry evidence and bounded traversal;
5. lifecycle and successor relationships;
6. authorization decision inputs and auditable outcomes;
7. deterministic halts and human confer states;
8. model-readable explanation and context packaging;
9. adapter declarations and conformance fixtures.

### 2.2 Out of scope

Seqaddr does not inherently provide:

- transport;
- encryption;
- authentication;
- authorization policy;
- cryptographic identity;
- data integrity;
- business logic;
- a universal semantic ontology;
- distributed consensus;
- storage consistency;
- a user interface;
- protection merely because an object has a Seqaddr.

These must be supplied by profiles, host systems, or complementary standards.

### 2.3 Claim discipline

This paper separates three categories:

- **Observed:** demonstrated inside the examined colab artifacts, such as reduced pack size, named conflict states, or a fixture producing two live registry claims.
- **Designed:** specified behavior not yet independently implemented, such as adapter manifests or capability-bound traversal.
- **Hypothesized:** benefits that require measurement, such as lower integration cost, fewer model tokens, or security-standard potential.

The distinction is essential. Rapid architecture maturation is evidence of a productive research method; it is not evidence that the resulting protocol is universally correct.

## 3. Core address model

### 3.1 Canonical form

The selected working schema is:

```text
lib-addr-1 := DD "." SS "." BB "." TT "." PPPP
```

where `DD`, `SS`, `BB`, and `TT` are fixed-width two-digit axes and `PPPP` is a fixed-width four-digit axis. The present semantic names are desk, shelf, book, page type/face, and local page or object position.

A future normative specification should state the grammar in ABNF, define allowed character encoding, forbid noncanonical alternatives at trust boundaries, and publish valid/invalid test vectors. RFC 3986 demonstrates why generic identifiers require explicit normalization and comparison rules, while RFC 6943 documents the security failures that arise when implementations compare identifiers differently. Seqaddr therefore cannot rely on visual similarity or permissive parsing.

### 3.2 Address as typed tuple

Let an address under schema `S` be:

\[
A_S = (d, s, b, t, p)
\]

Parsing is a total function over accepted canonical strings and a named halt over all others:

\[
parse_S(x) \rightarrow A_S \;|\; HALT_{SYNTAX}
\]

Canonical serialization must be injective within a schema:

\[
serialize_S(A_1)=serialize_S(A_2) \Rightarrow A_1=A_2
\]

No implementation may normalize an invalid external representation into a valid privileged object without recording that transformation. At a security boundary, the preferred rule is **parse canonical or halt**.

### 3.3 START, END, and suffix structure

`0` and `9` are not globally magical digits. They are schema-declared sentinels whose semantics depend on axis and position.

The week-old zero proposal suggested a monotonic rule: once zero began, later components should remain zero unless an exception was named. That was useful as a hostile simplification, but it conflated two distinct structures:

1. **ancestor suffix zeroing**, where a higher-level home is represented by zeroed descendants; and
2. **positional START**, where an individual axis value is a legitimate start/control position while later axes can remain meaningful.

The revised rule is therefore predicate-based, not visually inferred. A mixed-zero address can be legal if the schema says it is. Zero does not automatically create authority.

Similarly, END must be defined per axis and profile. It may represent a local terminus, continuation boundary, retirement face, or range endpoint. A parser cannot infer these semantics from `9` alone.

### 3.4 Canonical bytes

Textual canonicalization is necessary but not sufficient for signatures and digests. The standard should select one or more canonical byte profiles:

- UTF-8 canonical Seqaddr text for the address itself;
- RFC 8785 JSON Canonicalization Scheme for JSON envelopes; or
- deterministic CBOR under RFC 8949 for compact binary envelopes.

Signatures must cover the schema id, canonical address, role, face, object/revision identity, issuer, relevant policy context, and expiry where applicable. Signing a display title alone is insufficient.

## 4. The separation architecture

The most important one-week improvement was not a new address field. It was the decomposition of previously entangled questions.

| Layer | Question | Example | Must not imply |
|---|---|---|---|
| Address | Where is the structural position? | `01.01.01.03.0012` | identity, permission, truth |
| Identity | Which object and revision? | digest + revision + issuer | current authority |
| Role | What structural job? | registry, authority, payload | presentation format |
| Face | Which projection? | model-compact or human-readable | broader permission |
| Title | What human label? | inherited book/page title | role or identity |
| Authorization | May this actor perform this action now? | policy decision | provenance |
| Provenance | Where did this statement come from? | source and successor chain | active instruction |
| Circulation | What is its lifecycle state? | live, retired, successor | deletion of history |

This separation reduces a recurring class of confused-deputy errors: a parser should not treat a label as a role, a location as authority, quoted metadata as an instruction, or a readable face as permission to read the underlying object.

## 5. Roles, faces, titles, and circulation

### 5.1 Structural roles

The current role vocabulary includes:

- `payload`: ordinary governed content;
- `registry`: index of address claims and object metadata;
- `authority`: control or policy object in a schema-reserved position;
- `continuation`: link to an allowed next range or object;
- `gateway`: declared bridge to another schema/system;
- `stub`: a titled structural placeholder that does not manufacture content.

This is a core vocabulary, not a closed universal ontology. Domain roles should use namespaced extensions and cannot redefine core role semantics.

One canonical tuple must not have two live roles inside one authority domain. If the registry presents two live objects for the same canonical tuple, the system must expose the conflict rather than choose whichever record arrived first.

### 5.2 Faces

Faces are selective representations of an object, not separate identities by default. Current working faces include:

- `TT03`: compact model-oriented face;
- `TT04`: human-readable face;
- `TT00`: home/stub/title position;
- `TT09`: retirement/circulation position.

A face may disclose fewer properties, use another media type, or present a different explanation. It must not silently widen authorization or mutate the source object. If a face is separately signed or independently mutable, its relationship to the underlying identity must be explicit.

Faces create a useful security and efficiency opportunity: a model can receive the compact minimum required for a task, while a person receives a fuller narrative view. This is a least-disclosure mechanism only if policy is enforced on every face request.

### 5.3 Titles

Titles live at declared homes and can be inherited by faces. A title aids human navigation and discovery. It does not create a role, grant authority, or resolve an identity collision. Title spoofing must therefore be treated as a presentation attack rather than a change in canonical structure.

### 5.4 Reserved ranges

Pass 04 revealed that one prose phrase—“reserved PPPP”—was covering two different predicates. The executable successor should define them independently:

```text
authority_slot := TT = START and PPPP in 0001..0009
reserved_content_face := TT in {03,04} and PPPP in 0001..0009
```

The first selects structural authority slots. The second reserves early face positions and requires `content_kind`. Title state does not alter either predicate.

The exact `TT00/0001` fixture currently resolves consistently as authority. For `TT00/0002–0009`, the broader rule appears only in a Note in one governing page. Until a successor moves it into the executable body, the correct outcome is `HALT_NOTE_BODY_FIGHT`, not silent interpretation.

## 6. Evidence, refusal, and structural immunity

### 6.1 Find versus refuse

The system now separates discovery from policy:

- `find` returns bounded, ordered registry evidence and completeness metadata;
- `refuse` applies admission policy to that evidence and owns named halts;
- the Director handles defined human dispositions such as `CONFER_DIRECTOR`.

This prevents the search subsystem from quietly becoming an authorization system.

### 6.2 Two-live behavior

For a canonical tuple:

| Evidence state | Required outcome |
|---|---|
| complete, zero live | domain-specific confer such as `CONFER_BRAND_NO_LIVE` |
| complete, one live | proceed to remaining checks |
| observed two or more live | `HALT_TWO_LIVE`; disposition `CONFER_DIRECTOR` |
| incomplete, fewer than two observed | `HALT_FIND_INCOMPLETE` |
| no registry after permitted parent hop | `HALT_FIND_NO_REG` |

Two observed live claims are already enough to prove a conflict even if a capped query might contain more. One observed claim in an incomplete result is not enough to prove uniqueness.

### 6.3 Halt as success

Traditional workflows often treat a halt as failure and pressure the system to return something. Seqaddr treats a correct halt as a valid terminal result. This changes the optimization target from “always answer” to “answer only within known structural law.”

This is the basis of **structural immunity**: hostile or ambiguous input is converted into bounded evidence, a stable code, the laws that fired, and a governed next disposition. The metaphor should not be overstated—Seqaddr does not make software immune to compromise—but it captures an important design property: invalid states become first-class outputs rather than implicit corruption.

### 6.4 Why-visible decisions

“Why-visible” is not a graphical-interface requirement. It is a response contract:

```text
decision
evidence references
laws fired
limits and completeness
schema/profile versions
actor and authorization context
provenance
retryability or required human disposition
```

This contract is especially valuable to models because it reduces the need to reconstruct policy from an unbounded document set.

## 7. Governance and the compilation cycle

### 7.1 Authorization ladder

The current lifecycle is:

```text
draft → signed → approved → lock
```

Only the Director approves or locks. A model, clerk, or imported document may propose and sign within its assigned role, but it cannot promote itself by emitting the word `approved` inside content.

Exactly one active working-copy header is permitted. Quoted source material must be syntactically inert provenance. Pass 03 and pass 04 exposed a concrete failure: origin blocks contained column-zero `Authorization:` and `who:` fields that looked active to a mechanical parser. The semantic instruction “use the outer actor” was not enough because the representations were ambiguous. The documents correctly halt as `HALT_NESTED_AUTH` until flattened successors distinguish instruction from provenance.

### 7.2 Bench, successor, and retirement

Draft-room artifacts remain on the bench. Promotion does not overwrite or delete the old record. Instead it produces:

- a successor object with a new revision identity;
- a `Retired-by` edge from the prior object;
- preserved provenance and review evidence;
- a new coldboot result.

This resembles append-only governance more than ordinary file editing. It improves auditability and allows the system to explain which law was active at a given time.

### 7.3 Notes as patch queue; successors as compiled law

The colab process revealed a useful distinction:

- a **Note** captures a finding, proposed correction, or unsettled interpretation;
- a **successor** rewrites the executable body so runtime behavior no longer depends on note order or reader inference.

The resulting cycle is:

```text
hostile fixture → named finding → Note → Director selection → successor rewrite → coldboot verification
```

This is analogous to compilation. The Note is a patch queue or research journal; the successor is the compiled governing page. A future Clerk should detect when accumulated Notes alter executable behavior and require a successor.

### 7.4 Colab as a refinement environment

The colab system does more than gather model opinions. Each pass presents a smaller adversarial surface, preserves disagreements, assigns decision authority, and converts discoveries into tests or laws. The environment allows models to “overflow”—to surface adjacent implications not explicitly prompted—without allowing that overflow to become authority automatically.

This creates a productive asymmetry:

- generation remains broad;
- admission remains narrow;
- provenance remains visible;
- unresolved states remain haltable;
- accepted insights become fixtures and successor text.

## 8. Seqaddr as an API layer

### 8.1 Not HTTP

Seqaddr is not a transport protocol. HTTP can carry it, but so can MCP, a queue, a database call, a filesystem bundle, local IPC, or an offline signed pack. OpenAPI remains appropriate for documenting HTTP bindings. MCP remains appropriate for model-facing tools and resources. Seqaddr's proposed role is below or beside those interface descriptions: it supplies common structural semantics across bindings.

### 8.2 The narrow waist

The kernel should be deliberately small:

1. address grammar and canonical comparison;
2. schema/profile discovery;
3. role and face declarations;
4. registry lookup and evidence bounds;
5. lifecycle edges;
6. authorization decision interface;
7. provenance envelope;
8. deterministic result/halt/confer envelope;
9. capability and resource-limit negotiation.

Everything else remains application-specific.

This narrow-waist design is what allows Seqaddr to be a “universal starting point” without pretending to be a universal language for all computation.

### 8.3 Integration topology

In a fully pairwise environment, `N` applications can require up to:

\[
\frac{N(N-1)}{2}
\]

pairwise relationships. If each application instead implements one conformant Seqaddr adapter, the structural mapping count can approach `N`, plus profile and transport work. This does not eliminate domain-specific mappings, and it does not prove linear total cost. It identifies the architectural mechanism by which common structural work could be amortized.

### 8.4 Operation algebra

| Operation | Meaning | Required safety properties |
|---|---|---|
| `bind` | Associate a native key/object with a Seqaddr under a schema. | no implicit trust; deterministic mapping; collision detection |
| `resolve` | Select the canonical registered object/revision. | object-level authorization; uniqueness; freshness |
| `find` | Return matching registry evidence. | explicit cap/order/completeness; no admission decision |
| `read` | Return an authorized face. | least disclosure; media/profile negotiation |
| `walk` | Follow declared edges. | hop/depth/byte/time bounds; cycle and scope checks |
| `propose` | Place a mutation on the bench. | provenance; no self-approval; idempotency key |
| `commit` | Promote an authorized successor. | compare-and-swap revision; signed decision; audit event |
| `why` | Explain an outcome. | stable evidence refs; laws fired; sensitive-data filtering |

A context `pack` is a composition of bounded operations, not a separate authority. For example, a pack may resolve a root, read the model face, walk approved continuation edges within a budget, and include why-visible evidence.

### 8.5 Result envelope

Every binding should preserve a common semantic result:

```text
OK(value, evidence, limits, schema, profile, revision)
HALT(code, evidence, laws_fired, retryability)
CONFER(disposition, evidence, required_actor)
```

Transport-specific status codes are secondary. An HTTP `200`, MCP tool result, queue message, or local return value must not erase whether the semantic outcome was OK, HALT, or CONFER.

### 8.6 Adapter manifest

A minimum adapter manifest should declare:

```yaml
adapter_id: reverse-dns-or-uri
adapter_version: semver
seqaddr_schema: lib-addr-1
conformance_profiles: [core-read]
native_types:
  - native_type: example.record
    seqaddr_role: payload
faces:
  "03": {media_type: application/json, purpose: model-compact}
  "04": {media_type: text/markdown, purpose: human-readable}
canonicalization:
  address: strict
  envelope: rfc8785
identity:
  revision_field: etag
  digest: sha-256
operations: [bind, resolve, find, read, why]
limits:
  max_results: 100
  max_hops: 8
  max_bytes: 1048576
authorization:
  policy_binding: implementation-defined-uri
lifecycle:
  retired_state: archived
error_map:
  duplicate_live: HALT_TWO_LIVE
extensions: {}
```

The final schema should require test-vector references, supported signature suites, issuer/audience rules, mutation preconditions, idempotency, freshness behavior, and extension namespaces.

## 9. Security assessment

### 9.1 Security principle

An address names a structural position. It must never be accepted as proof of identity, authority, integrity, or trust. This aligns with zero-trust principles: network or structural location must not produce implicit trust, and authorization is evaluated for access to the resource.

### 9.2 Threat matrix

| Threat | Failure mode | Required mitigation |
|---|---|---|
| Canonicalization collision | two byte strings compare differently across components | strict parser; canonical bytes; shared vectors |
| Title spoofing | attacker imitates trusted human label | bind trust to canonical identity/issuer, never title |
| Registry poisoning | false or duplicate live claim | authenticated writes; append-only log; `HALT_TWO_LIVE`; reconciliation |
| Broken object authorization | caller changes address to access another object | object-level authorization on every operation |
| Confused deputy | trusted adapter uses its privilege for an untrusted caller | bind actor, audience, purpose, operation, and scope |
| Capability replay | old grant reused | nonce/replay cache, expiry, revision and audience binding |
| Revision race | approved object changes before commit | compare-and-swap revision/digest |
| Traversal escape | continuation crosses allowed scope | explicit scope; gateway requirement; fail closed |
| Cycle/resource exhaustion | recursive links consume resources | hop/depth/result/byte/time budgets and visited set |
| Projection escalation | compact face reveals restricted fields or invokes richer face | per-face authorization; field allowlist; tests |
| Enumeration leakage | find reveals existence or metadata | policy-aware discovery; capped and redacted evidence |
| Downgrade | caller selects a weak schema/profile | minimum profile policy; signed negotiation; fail closed |
| Instruction bleed | quoted `Authorization` becomes active | one active header; inert provenance syntax; parser tests |
| Provenance laundering | copied content loses origin or appears newly authoritative | signed provenance chain; successor linkage |
| Adapter escape | native keys inject paths/queries outside declared mapping | typed mapping, escaping, allowlisted scopes |

OWASP's API guidance is directly relevant: any endpoint that receives an object identifier must enforce object-level authorization, and unrestricted resource consumption becomes a vulnerability when result, compute, or traversal limits are missing. Seqaddr's named addresses make these checks easier to state; they do not perform the checks automatically.

### 9.3 Integrity and provenance

High-assurance profiles should borrow established patterns instead of inventing bespoke cryptography:

- deterministic JSON or CBOR before hashing;
- issuer-bound signatures with algorithm agility;
- W3C PROV-compatible lineage for interchange where appropriate;
- in-toto/SLSA-style attestations for build or promotion steps;
- transparency or append-only logs for registry mutations;
- key rotation, revocation, and trust-store rules.

The signed subject should include both object identity and structural context. Otherwise, a valid object could be replayed at a different address or under a different role.

### 9.4 Security profiles

- **Core Read:** authenticated registry, strict parsing, authorization per read, bounded evidence.
- **Mutation:** signed proposal, separation of duties, revision precondition, append-only audit.
- **Federation:** issuer trust, cross-domain gateway, replay/downgrade protection, split-brain handling.
- **Model:** instruction/provenance separation, compact faces, pack budget, tool-output isolation.
- **High Assurance:** canonical signed envelopes, attestations, durable audit retention, independent audit.
- **Offline:** signed snapshot, expiry/freshness policy, reconciliation on reconnect.

### 9.5 Security-standard horizon

Seqaddr could contribute to a future security standard because its refusal semantics and narrow structural vocabulary are testable. A five-to-ten-year path is plausible only if the work progresses through independent implementations, public threat modeling, stable governance, interop events, formal conformance, and adoption. A promising architecture is not itself a security standard.

## 10. Relationship to existing standards

### 10.1 URI and URN

URI standards already provide a federated, extensible naming framework. Seqaddr should not compete for generic global naming syntax. It can appear inside a URI path, URN namespace, query-free resource identifier, or application envelope. The important Seqaddr contribution is schema-bound tuple semantics and governed resolution, not punctuation.

### 10.2 OpenAPI

OpenAPI is a language-agnostic description for HTTP APIs. A Seqaddr HTTP binding should be describable in OpenAPI, including request schemas and semantic result envelopes. OpenAPI does not replace Seqaddr's registry, role, face, lifecycle, or halt semantics.

### 10.3 Model Context Protocol

MCP defines a protocol for connecting model applications to tools, resources, and prompts; its resources use URIs and its tools expose schemas. Seqaddr can be surfaced through MCP resources and tool operations. For example, `seqaddr.resolve` may be a tool and a human or model face may be an MCP resource. Seqaddr's value would be consistent semantics across MCP and non-MCP bindings.

### 10.4 DID and verifiable claims

Decentralized Identifiers and verifiable-credential patterns may be useful for issuers, verification methods, and portable claims. Seqaddr should reference such mechanisms through profiles rather than embedding an unreviewed identity system in its core.

### 10.5 Provenance and supply-chain attestations

PROV-O provides an extensible model for entities, activities, and agents. in-toto and SLSA provide useful patterns for describing and attesting process steps and build provenance. Seqaddr successor and promotion events can map to these models without requiring the kernel to duplicate them.

### 10.6 Differentiating combination

No single Seqaddr element is unprecedented. Its research contribution is the combination of:

- readable fixed hierarchical addresses;
- explicit address/identity/role/face separation;
- bounded evidence separate from refusal policy;
- lifecycle through successors and retirement;
- named halts and human confer states;
- why-visible output;
- a governance workflow designed for human–model collaboration.

The value of that combination must be tested empirically.

## 11. One-week development analysis

### 11.1 Baseline on 2026-09-15

The initial assessment already contained several strong foundations:

- `DD.SS.BB.TT.PPPP` as a candidate canonical form;
- deterministic, schema-versioned parsing;
- START and END sentinels;
- header/path comparison;
- separation of imported body digits from true addresses;
- proposed payload, registry, continuation, gateway, authority, allocation, and tombstone roles;
- proposed specification layers for sentinel law, serialization, object model, storage, and security;
- explicit warning that an address does not grant trust or permission.

It also recorded major unresolved questions:

- how per-axis kinds compose into whole-object role;
- canonical END suffixes;
- schema-specific domains;
- identity, integrity, and authority;
- continuation security and bounded traversal;
- missing records and range rules;
- header/path authority;
- storage and source-code profiles;
- model context packs;
- the legal meaning of mixed-zero sequences.

The zero-sequence handoff favored monotonic zero suffixes and asked for decisions about mixed zeros, width, allocation range, kernel location, registry content, and diary placement.

### 11.2 State on 2026-09-22

Seven days later, the work had advanced in four dimensions.

**Semantic resolution**

- selected `lib-addr-1`;
- separated roles, faces, titles, circulation, identity, and authorization;
- replaced the monotonic-zero assumption with explicit ancestor-suffix and positional-START semantics;
- distinguished authority slots from reserved content faces;
- defined title inheritance without title-created role.

**Governance resolution**

- established draft → signed → approved → lock;
- limited approve/lock to Director authority;
- created bench, promotion, successor, and retirement behavior;
- made one active header a mechanical requirement;
- separated active instruction from origin/provenance;
- treated Notes as patch queue and successors as executable compilation.

**Operational resolution**

- separated `find` evidence from `refuse` policy;
- defined two-live, incomplete-find, missing-registry, nested-auth, role, and note/body halts;
- bounded continuation by hop, cycle, range, and scope;
- defined approved/lock pack admission and coldboot validation;
- established model and human faces.

**Strategic expansion**

- moved from a file-addressing standard toward a transport-neutral integration kernel;
- proposed adapter manifests and an operation algebra;
- identified least-disclosure faces and why-visible output;
- framed structural immunity as a security property;
- established a conformance and research roadmap.

### 11.3 Quantitative process signal

The four examined colab source packs measured:

| Pass | Files | Input bytes |
|---:|---:|---:|
| 01 | 30 | 42,363 |
| 02 | 18 | 30,384 |
| 03 | 15 | 26,260 |
| 04 | 10 | 14,099 |

From pass 01 to pass 04, both file count and input bytes fell by approximately **66.7%**. At the same time, later reviews addressed narrower semantic joints: search/refusal ownership, actor authority, reserved-range predicates, and nested headers.

This supports a limited conclusion: within this project, repeated colab and Librarian refinement reduced the amount of material required to expose the next contradiction. It does **not** yet establish that Seqaddr universally reduces tokens, cost, or errors. The next phase should collect token counts, latency, retry rate, correctness, and coldboot success under controlled baselines.

### 11.4 Speed interpretation

The pace is unusual because several activities normally performed in sequence occurred in a tight loop:

- architecture drafting;
- adversarial review;
- requirements traceability;
- editorial synthesis;
- fixture design;
- governance decisions;
- revision planning.

Models supplied parallel hypothesis generation and criticism; the Librarian preserved addressable state; the Director supplied authority and taste; colab turned disagreement into bounded work. The speed did not come from models replacing judgment. It came from shortening the distance between observation, preservation, challenge, decision, and retest.

## 12. Replacement-cost estimate

### 12.1 What is being estimated

The estimate covers reconstruction of the current documented state:

- core address theory;
- role/face/governance architecture;
- four adversarial refinement passes;
- API and security research framing;
- current handoff and revised paper.

It does not cover a production implementation, completed formal verification, external audit, patent/legal work, standards-body adoption, or commercial value.

### 12.2 Rate model

U.S. Bureau of Labor Statistics May 2025 median annual wages were approximately:

- software developers: **$135,980**;
- computer and information research scientists: **$140,300**;
- information security analysts: **$129,180**.

At 2,080 work hours, those salaries correspond to base hourly wages of roughly $62–$67. BLS employer-cost data for June 2026 reports wages at about 70% and benefit costs at about 30% of total compensation, implying direct compensation near 1.43 times wage. Facilities, management, recruiting, legal review, unbillable time, and organizational overhead raise the practical fully loaded rate further. This paper uses modeled blended rates of approximately **$125–$250 per hour**, with specialized consulting potentially higher.

### 12.3 Scenarios

| Scenario | Team and method | Effort | Replacement cost |
|---|---|---:|---:|
| Brute-force AI | one senior architect/operator repeatedly prompts, reconciles, and rewrites broad model output | 250–600 expert hours | **$35k–$150k** |
| Structured human–AI | architect/director, protocol engineer, security reviewer, research/editorial support using governed AI loops | 600–1,500 hours | **$100k–$375k** |
| Traditional lab / think tank | 4–7 specialists, staged workshops, research, review, documentation over about 3–6 months | 2,000–6,000 hours | **$400k–$1.5m** |
| Production standard candidate | 8–15 contributors, multiple implementations, conformance suite, audits, pilots, governance over 12–24 months | 15,000–40,000 hours | **$3m–$10m+** |

The brute-force AI case is not simply token cost. Model inference may cost hundreds or thousands of dollars, but expert reconciliation, specification consistency, evidence handling, and decision authority dominate. Cheap generation without structure can increase downstream review cost.

The best central range for reproducing the **current conceptual and documented research state** is **$100,000–$500,000** under conventional conditions. The broader traditional-institution range reflects review overhead and multidisciplinary staffing. These are order-of-magnitude planning estimates, not audited costs, valuation, or proof that an organization would reach the same insights.

### 12.4 Value versus cost

Replacement cost is not market value. Seqaddr's value will depend on whether it measurably reduces integration work, model context, defects, or security incidents. Conversely, a week's rapid progress does not eliminate the remaining cost of validation; formalization and independent testing are likely to cost more than the initial conceptual discovery.

## 13. Experimental program

### 13.1 Hypotheses

**H1 — Integration compression.** A conformant Seqaddr adapter reduces person-hours and structural defects compared with pairwise integration.

**H2 — Context compression.** Warm Seqaddr sessions use fewer coldboot and task tokens while maintaining or improving correctness.

**H3 — Resolution improvement.** Models given compact faces plus why-visible evidence cite the correct controlling law more often than models given an unstructured repository dump.

**H4 — Containment.** Hostile fixtures produce deterministic halts before side effects more often than conventional permissive API handling.

**H5 — Portability.** The same semantic operation and fixture results survive multiple transports and independent implementations.

### 13.2 Minimum study design

1. Select three materially different applications, such as a document store, issue tracker, and model knowledge tool.
2. Implement two transports, such as HTTP/OpenAPI and MCP, plus one local/offline binding.
3. Build pairwise or native baseline integrations.
4. Build Seqaddr adapters without allowing shared application-specific shortcuts.
5. Pre-register tasks and hostile fixtures.
6. Measure engineering hours, code changed, defects, tokens, latency, result completeness, halt precision/recall, and explanation quality.
7. Have an independent team implement from the specification alone.
8. Publish failures and incompatible interpretations, not only successful demos.

### 13.3 Required fixtures

- canonical and noncanonical syntax;
- mixed-zero legal and illegal cases;
- `TT00/0001` and `TT00/0002` authority cases;
- title attempting to change role;
- complete and capped two-live registry results;
- no registry after parent hop;
- continuation cycle and scope escape;
- oversized result/byte budgets;
- stale-revision commit;
- replayed capability;
- face escalation;
- imported origin block with active-looking authorization;
- schema/profile downgrade;
- retired object and successor walk;
- cross-adapter native-key ambiguity.

## 14. Specification roadmap

### Phase 0 — Repair current law

- produce flattened successors for zeros and refuse;
- move Note-only executable mappings into bodies;
- name `HALT_ROLE` at the role-fight sentence;
- rerun the four smallest pass-04 fixtures.

### Phase 1 — Core normative draft

- ABNF and canonical serialization;
- schema/version negotiation;
- typed role, face, registry, lifecycle, and result envelopes;
- error/halt registry;
- canonical JSON and/or CBOR profile;
- normative examples and hostile vectors.

### Phase 2 — Reference implementations

- parser/comparator in two languages;
- registry and read-only resolver;
- HTTP/OpenAPI binding;
- MCP binding;
- offline pack implementation;
- conformance runner.

### Phase 3 — Mutation and security

- proposal/commit state machine;
- revision locking and idempotency;
- signature, issuer, capability, and revocation profiles;
- provenance and attestation mapping;
- full threat model and penetration review.

### Phase 4 — Independent interoperability

- two external implementations from the written spec;
- interop event with shared fixtures;
- ambiguity log and incompatible behavior report;
- versioning and extension policy.

### Phase 5 — Standards and governance

- public change-control process;
- reference conformance marks;
- security disclosure process;
- intellectual-property and licensing clarity;
- engagement with an appropriate standards community after implementation evidence exists.

## 15. Open research questions

1. Is a five-axis core sufficient across domains, or should the core define a tuple mechanism with `lib-addr-1` as one profile?
2. Which semantics are universal enough for core roles, and which must be namespaced?
3. How are federated registries reconciled without hiding split brain?
4. What is the minimum identity envelope that prevents address replay while remaining transport-neutral?
5. Can faces be generated deterministically, or are they separately governed artifacts?
6. How should authority be delegated without recreating an overly complex capability language?
7. What evidence can `why` disclose without leaking sensitive policy or object existence?
8. Which halt codes are stable protocol surface and which are profile-specific?
9. How are schema migrations represented when an address maps differently across versions?
10. What are the accessibility and localization consequences of fixed numeric addresses and inherited titles?
11. How much observed token reduction comes from Seqaddr itself versus ordinary session familiarity and editorial compression?
12. What governance prevents the “universal start point” from expanding into an unmaintainable universal ontology?

## 16. Limitations

- Evidence comes from one fast-moving project and its internal colab artifacts.
- The source-pack byte reduction is not a controlled token experiment.
- No independent implementation has tested the current semantics.
- No formal parser, registry schema, reference server, or public conformance suite is complete.
- Security benefits are architectural expectations, not penetration-test results.
- Cost estimates depend on assumptions and do not measure actual expenditures.
- The proposed API and adapter design remain research proposals.
- Legal rights, licensing, trademarks, patents, and standards commitments require qualified counsel.

## 17. Conclusion

Seqaddr began as a compact hierarchical address and is becoming an environment for disciplined interoperability. The meaningful advance is not merely that `DD.SS.BB.TT.PPPP` is readable. It is that the surrounding kernel now separates location from identity, role from face, evidence from refusal, instruction from provenance, and proposal from authority. It preserves failed states as named outcomes and turns discoveries into successor law and fixtures.

That architecture could make integrations easier for both software and models. A common adapter contract may reduce repeated structural work. Compact faces may reduce context. Why-visible results may improve resolution. Named halts may contain attacks and ambiguity earlier. These benefits are credible hypotheses, not completed proofs.

The speed of the one-week advance is itself important. Colab, the Librarian, and Director governance formed a high-frequency research loop in which broad model generation could occur without broad model authority. Pack size fell while semantic precision increased. The process is no longer a coldboot in the ordinary sense: accumulated structure changes what the next pass must rediscover.

The next milestone should therefore not be more vocabulary. It should be executable precision: repair the known successor defects, freeze canonical grammar and bytes, implement the smallest read profile twice, run hostile fixtures, and measure whether Seqaddr actually reduces integration effort, model context, and unsafe ambiguity. If it survives that stage, the claim that Seqaddr is a universal structural starting point will move from an attractive idea toward an engineering result.

## References

1. Berners-Lee, T., Fielding, R., and Masinter, L. [RFC 3986: Uniform Resource Identifier (URI): Generic Syntax](https://www.rfc-editor.org/rfc/rfc3986). IETF, 2005.
2. Thaler, D. [RFC 6943: Issues in Identifier Comparison for Security Purposes](https://www.rfc-editor.org/rfc/rfc6943). IETF, 2013.
3. Rundgren, A., Jordan, B., and Erdtman, S. [RFC 8785: JSON Canonicalization Scheme](https://www.rfc-editor.org/rfc/rfc8785). IETF, 2020.
4. Bormann, C. and Hoffman, P. [RFC 8949: Concise Binary Object Representation](https://www.rfc-editor.org/rfc/rfc8949). IETF, 2020.
5. OpenAPI Initiative. [OpenAPI Specification 3.2.0](https://spec.openapis.org/oas/v3.2.0.html).
6. Model Context Protocol. [Specification](https://modelcontextprotocol.io/specification/latest).
7. W3C. [Decentralized Identifiers (DIDs) v1.0](https://www.w3.org/TR/did-core/).
8. W3C. [PROV-O: The PROV Ontology](https://www.w3.org/TR/prov-o/).
9. NIST. [SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final), 2020.
10. NIST. [SP 800-218: Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final), 2022.
11. OWASP. [API Security Top 10 — API1:2023 Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/).
12. OWASP. [API Security Top 10 — API4:2023 Unrestricted Resource Consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/).
13. in-toto. [A framework to secure the integrity of software supply chains](https://in-toto.io/).
14. SLSA. [Provenance](https://slsa.dev/provenance/).
15. U.S. Bureau of Labor Statistics. [Software Developers, Quality Assurance Analysts, and Testers](https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm), May 2025 wage data.
16. U.S. Bureau of Labor Statistics. [Computer and Information Research Scientists](https://www.bls.gov/ooh/computer-and-information-technology/computer-and-information-research-scientists.htm), May 2025 wage data.
17. U.S. Bureau of Labor Statistics. [Information Security Analysts](https://www.bls.gov/ooh/computer-and-information-technology/information-security-analysts.htm), May 2025 wage data.
18. U.S. Bureau of Labor Statistics. [Employer Costs for Employee Compensation](https://www.bls.gov/news.release/ecec.nr0.htm), June 2026.

