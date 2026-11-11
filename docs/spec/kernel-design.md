# Kernel Architecture — Design Draft

**Project:** Workshop / Librarian / Sequence Address  
**Status:** Proposed architecture — for refinement, not promoted law  
**Root kernel address:** `00.00.00`

## 1. Purpose

The kernel is the shared foundation of the Sequence Address (SeqAddr) environment. It supplies the **operating agreements** that desks, shelves, books, pages, faces, and cards inherit. It should be the smallest sufficient collection of definitions and rules from which more specialized environments can be built.

The kernel does not perform all work and does not contain every project's content. Its job is to make the system's structure, permissible behavior, and recovery procedures understandable and consistent across scales.

**Governing design:** *Inherit the agreement. Write only the difference.*

The Axioms (`Axioms.md`, decisions E1-E7) provide the **shape** of the system's reasoning and responsibilities. SeqAddr provides its **geometry**: how information is located, identified, and connected. The kernel expresses these agreements in reusable forms that different readers can retrieve and apply.

## 2. Separation of Responsibilities

### Person — governing authority

The person establishes goals, delegates permissions, approves governing changes, and resolves matters beyond delegated authority. Leading a task is not the same as holding authority over it.

### Model — reasoning and proposals

The model interprets intent, investigates, drafts, questions, explains, and proposes. It uses kernel guidance and retrieved context to reason, but it must not treat plausible reconstruction or its own memory as authoritative source material.

### Compute — deterministic enforcement

Compute reads and validates the underlying records, resolves addresses and relationships, applies permissions and allowed state transitions, and commits authorized changes. Compute may report conflicts or missing information; it must not invent missing authority or independently decide a disputed human question.

### Database / book storage — persistent record

Storage preserves committed information, relationships, decisions, history, and especially **why** decisions were made. Its contents must be retrievable and inspectable without dependence on a particular LLM.

**Boundary:** The kernel **defines agreements**; compute **enforces machine-checkable agreements**; the model **reasons within them**; the person **governs authority**.

## 3. The Kernel Is Declarative Where Possible

The kernel should define reusable contracts rather than require special-purpose compute code for every new kind of page or work.

Examples of kernel-defined contracts:

- Valid identities, addresses, and inherited context.
- Page and card types and their permitted roles.
- Face responsibilities and requirements.
- Required relationships between face representations.
- Draft, working, review, seated, and retired states and allowable transitions.
- How overrides are declared and authorized.
- Validation rules and conditions requiring elevation to the person.
- How to recognize incomplete or conflicting information without inventing repairs.

Compute can interpret these contracts and enforce the deterministic portions. Richer or newly defined page types should generally be introduced through kernel definitions and authorized specialization, not through unrelated implementations of the same machinery.

**Limit:** A small set of safety-critical primitives must remain fixed in compute so that potentially missing, corrupt, or untrusted kernel content cannot redefine how the system initially reads or protects its own records.

## 4. Three Core Responsibilities

### 4.1 What exists?

Define the shared vocabulary and basic contracts of desks, shelves, books, pages, faces, cards, addresses, references, page types, and state. Establish where identity is recorded and how the correct representation is retrieved.

### 4.2 What is permitted?

Define inheritance, the boundaries of authority, local specialization, explicit overrides, permitted operations, and promotion requirements. The kernel should permit difference where authorized without allowing a child to silently replace a governing agreement.

### 4.3 How do we recover?

Define how to recognize missing, contradictory, stale, or damaged material. Preserve past recorded steps and the why behind changes. Recover from traceable sources and lawful connections, not from apparent similarity or model memory. Where evidence or authority is insufficient, report the gap and stop the affected operation.

## 5. Fractal Inheritance

The shared design grammar repeats through the SeqAddr hierarchy:

`Repository → Desk → Shelf → Book → Page → Face → Card`

The kernel supplies common agreements. Each more local environment inherits the applicable agreements and records only its necessary differences.

| Level | Primary role |
|---|---|
| Kernel (`00.00.00`) | Shared rules, templates, definitions, and defaults |
| Desk | Environment-specific policies and specializations |
| Shelf | Themed working context |
| Book | Localized definitions and persistent work |
| Page | One subject or information object |
| Face | A representation or responsibility within that page |
| Card | An individually retrievable piece of information |

Fractal does **not** mean identical copies at every scale. It means recognizable principles and relationships, applied according to each level's purpose and authority. Parent content should not be duplicated into children merely to make it locally visible.

The kernel may define a task board without storing every task, define a brand-card mechanism without accumulating every user's meanings, and define page types without holding every application-specific page.

## 6. Multi-Faced Kernel Pages

The kernel should use the same SeqAddr page architecture that it governs rather than becoming a separate, incompatible documentation format. Different readers need different representations of the same subject.

- **Face 00 — Identity:** page stamp and identity.
- **Face 01 — Law:** compact model-facing understanding and governing meaning.
- **Face 02 — Schema:** formats, templates, and precise procedures.
- **Face 03 — Operate:** compute-oriented operations, routing/menu, and authority references, where allowed by SeqAddr.
- **Face 04 — User:** readable explanation, design intent, and the preserved *why*.
- **Face 05 — Tasks:** working passes where appropriate.
- **Face 06 — Notes:** attributed observations and unresolved findings.
- **Face 08 — Map:** lawful relationships, dependencies, and navigation.

Not every page needs every face. The selected page type and its inherited contracts determine what is required. Readers should retrieve the relevant face and only the additional governing or connected information needed for the task.

The faces are different representations, **not equal sources of authority**. Conflicts should be identified and resolved by the governing agreements, not averaged into an invented compromise.

## 7. Bootstrap: How Compute Reads the Kernel

The kernel cannot be the sole source of instructions for reading itself. Compute needs a minimal, stable **bootstrap contract** that works before the kernel has loaded.

The bootstrap must know enough to:

1. Locate the repository's kernel at `00.00.00`.
2. Open the physical book format and recognize its supported version.
3. Parse the minimum address and record structure needed to find kernel definitions.
4. Check fundamental record integrity and refuse unsafe or incompatible material.
5. Load the kernel's validated agreements, then enable richer operations.
6. Report failure and retain a recoverable prior state rather than guessing when kernel loading fails.

The bootstrap should be deliberately small. Anything not required for safe initial reading and validation belongs in the kernel or a permitted local specialization.

## 8. Rules for Kernel Growth

Before adding a kernel rule or mechanism:

1. Find the existing agreement and its recorded why.
2. Check whether the requirement is truly shared across environments or belongs in a desk, shelf, book, or page.
3. Prefer extending an established contract over inventing an unrelated one.
4. Record the difference, its reason, its authority, and its links to the predecessor.
5. Test its effect at the local level and at the inherited level.
6. Preserve earlier states and require appropriate review before promotion.

A kernel that grows into a store of ordinary project work becomes harder to load, govern, and maintain. Keep it focused on reusable agreements and the means of understanding them.

## 9. Implementation and Validation Questions

The first prototype should prove that compute can safely bootstrap the kernel, retrieve its applicable contracts, and apply them to an ordinary book without copying all kernel content into that book.

Suggested checks:

- Can a child retrieve an inherited contract without duplicating it?
- Can a local difference be distinguished from an unauthorized contradiction?
- Can readers retrieve only the faces needed for a task?
- Can compute refuse invalid transitions without relying on an LLM's judgment?
- Can a person inspect a kernel rule, its why, its authority, and its revision lineage?
- Can the environment identify missing or stale governing material instead of constructing a plausible substitute?
- Can a previous valid kernel state be recovered after a failed update?

These are **proposed verification goals**, not claims that the implementation currently passes them.

## 10. Open Design Decision — Coordination

**Unresolved:** Should the kernel be strictly an inherited library of agreements, or should it also define how task routing and procedure selection are coordinated?

Two possible boundaries:

- **Structural/reasoning kernel:** Holds agreements, reasoning guidance, contracts, and reusable decision procedures. Compute selects and executes workflows. (The old kernel called this part the clerk; in Workshop it is the compute.)
- **Kernel-directed coordination:** Also defines routing criteria and reusable coordination policies, while the actual selection and enforcement still happen through compute and authorized agents.

A workable compromise may be to store **declarative routing rules and procedures in kernel faces** while keeping the coordinator itself outside the kernel. This is a proposal to test, not a settled rule.

## 11. Principle to Preserve

**The kernel preserves the agreements that make work intelligible and repeatable. It should not become the intelligence, the authority, or the storage of all work.**

The goal is that models and implementations may change while the system's identities, reasoning, decisions, relationships, and whys remain retrievable, inspectable, and recoverable.
