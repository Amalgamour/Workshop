# RETURN — 00.axioms.002-draft
date: 2026-10-01
source: 00.axioms.002-draft.zip
mode: kernel design review
authority: return / candidate guidance only

## call

**KEEP THE REWORK. CONTINUE THE DRAFT.**

This redesign is materially stronger than the prior axiom arrangement.

The important change is not merely that the nine axioms were renamed or reordered.

The change is:

> **the axioms are becoming the invariant reasons that the face grammar exists.**

That gives a fresh Prime two things at once:

1. a rule for what a face does;
2. a reason for why that face must behave that way.

That should improve coldboot because the model no longer has to hold a detached list of principles beside a detached list of faces.

The face becomes the local expression of an axiom.

---

# Main design result

The emerging structure is:

| Axiom | Primary face | Core job |
|---|---:|---|
| 1 Authority | 01 | determine what governs |
| 2 Fractal | 02 | inherit agreement; write difference |
| 3 Dance | 03 | preserve role separation |
| 4 Why | 04 | preserve recoverable meaning |
| 5 Narrow | 05 | bound executable work |
| 6 Lineage | 06 | preserve change and reason |
| 7 Missing | 07 | protect absence; do not infer |
| 8 Record | 08 | recover the maintained source |
| 9 Attack | 09 | challenge authority transitions |

This is not merely numeric symmetry.

The important test is whether each attachment explains actual system behavior.

Most of the mapping is now strong enough to continue.

---

# Axiom 1 — Authority
## Primary face: 01

**Meaning**

A thing does not govern merely because it exists or is remembered.

Authority comes from:
- lawful location,
- lawful state,
- and a lawful tie to the governing source.

A draft, note, park, retired object, copy, model memory, or stale twin does not silently become authority.

**What it protects**

- governing truth
- state
- provenance
- human authority
- promotion boundaries

**How face 01 expresses it**

Face 01 is where binding words live.

It is therefore the natural local seat for:

> what governs here?

Face 01 should never need to explain all authority law locally. It inherits the general rule and materializes only local difference.

**Interaction with twins**

Every twin contract needs authority.

A twin is not equality.

If two representations disagree, the contract must say which representation governs which dimension.

Example:

```text
twin:
  /src <-> /lib

authority:
  runtime: /src
  design: /lib
```

This is stronger than saying one side globally wins.

Different sides may govern different dimensions.

---

# Axiom 2 — Fractal
## Primary face: 02

**Meaning**

> **Inherit agreement. Write difference.**

Structure repeats by level so local work can stay local.

Do not duplicate a parent contract simply because a child exists.

Climb until the needed agreement is found.

Materialize only what changes here.

**What it protects**

- locality
- repairability
- token/work efficiency
- scale
- coherence

**How face 02 expresses it**

Face 02 becomes the small machine-facing structural contract.

It may declare:
- relevant axioms,
- twin relationship,
- local authority difference,
- local why,
- local how.

But it should contain only what is needed.

If the parent already defines the twin contract, the child inherits it.

If the child changes one dimension, write only that dimension.

**Important interaction**

Fractal and Missing work together:

> Fractal says climb.  
> Missing says do not invent while climbing.

If no lawful ancestor supplies the missing value, it remains unresolved.

This is a major anti-bloat and anti-hallucination rule.

---

# Axiom 3 — Dance
## Primary face: 03

**Meaning**

Different participants and representations have different jobs.

Current operational split:

- human/director — intent and authority
- Prime/model — reasoning, design, synthesis, attack
- Clerk — deterministic opening, checking, routing, maintenance
- worker/lab — bounded execution

There is no native Clerk yet; Prime temporarily performs Clerk-like work when required.

Sync does not grant permission.

**What it protects**

- agency
- role clarity
- reliability
- division of uncertainty

**How face 03 expresses it**

Face 03 is menu/routing.

It tells the operator where to go without becoming the thing it points to.

That is Dance in structural form:

> each seat performs its own job.

A menu does not become law.
A model does not become director.
A map does not become record.
A worker does not become architect.

---

# Axiom 4 — Why
## Primary face: 04

**Meaning**

Recover the reason in proportion to the cost of being wrong.

If the why cannot be recovered, keep it unknown.

Do not invent a plausible cause.

**What it protects**

- intent
- design meaning
- interpretability
- continuity

**How face 04 expresses it**

Face 04 is the readable whole/check of the governing structure.

For a normal page:

- 01 governs
- 02 packs
- 03 points
- 04 gives the readable whole

This is why 04 must not become a miscellaneous storage surface.

It preserves the understandable design.

**Page twin**

The relationship should be understood as:

```text
twin:
  face01+02+03 <-> face04

authority:
  governing-law: face01

why:
  01-03 are operational structure
  04 is the readable whole/check

how:
  governing meaning must agree
  04 adds no new law
```

The twin does not require identical text.

It requires agreement on the declared design.

---

# Axiom 5 — Narrow
## Primary face: 05

**Meaning**

Narrow before spending intelligence.

Work should be reduced to the smallest lawful executable slice before expensive reasoning or action is spent.

**What it protects**

- accuracy
- speed
- boundedness
- delegation
- recovery

**How face 05 expresses it**

Face 05 is work/ticket/task state.

A good 05 should be resumable and bounded.

It should answer enough of:

- what is the target?
- what is the next action?
- what is held?
- what is allowed?
- when is this done?

Narrow controls the size of the work.

Fractal controls the amount of structure restated.

These are related but different.

---

# Axiom 6 — Lineage
## Primary face: 06

**Meaning**

Change only through visible transition.

Preserve:
- what changed,
- why it changed,
- and what now governs.

**What it protects**

- design history
- recoverable reasoning
- migration safety
- future repair

**How face 06 expresses it**

Face 06 captures notes, reasoning, overflow, and change context.

This is where the intelligence behind work can survive.

A task without recoverable reason can become mechanical drift.

However:

> **not every 06 must become a 05.**

A note may be valuable without becoming active work.

The stronger direction is:

> every important active 05 should have recoverable why/lineage.

This prevents task inflation.

---

# Axiom 7 — Missing
## Primary face: 07

**Meaning**

Missing is a lawful state.

So are:
- unknown,
- draft,
- parked,
- retired,
- conflict.

Absence is not permission.

A hole must not be filled merely because the model sees an available seat.

**What it protects**

- honesty
- local truth
- unresolved research
- anti-overreach behavior

**How face 07 expresses it**

Face 07 remains reserved.

Its present structural job is the hole itself.

That is important.

The memory discussion tested this axiom directly:

> a new need appeared; an empty face existed; the correct answer was not to occupy it automatically.

Face 07 can change later if stability proves a genuinely orthogonal seventh job.

Until then:

> **protected absence is the job.**

Twin: none.

---

# Axiom 8 — Record
## Primary face: 08

**Meaning**

Memory is temporary.

The maintained source must remain findable.

A pointer, map, memory, summary, or alternate representation does not silently replace the maintained record.

**What it protects**

- coldboot
- recoverability
- maintained truth
- navigation without hidden session knowledge

**How face 08 expresses it**

Face 08 maps relationships and routes to sources.

The map points.

It does not become the page.

This gives Record a natural relationship to face 08:

> Record requires that governing truth be recoverable; Map provides the route without duplicating that truth.

This also gives future model memory a natural relationship to Map.

A memory page may carry working state, but it should be able to point back to the maintained source that refreshes it.

Memory is therefore derived orientation, not hidden authority.

---

# Axiom 9 — Attack
## Primary face: 09 / authority transition

**Meaning**

Exploration is cheap.

Promotion is hard.

A proposal does not clear its own authority boundary merely because its author attacked it.

**What it protects**

- live record
- promotion quality
- retirement/promotion transitions
- resistance to self-certification

**How face 09 relates**

Face 09 is lifecycle exit/retirement.

Attack is broader than retirement, so the strongest shared abstraction is:

> **authority transition must be challenged before state changes across the live boundary.**

Promotion enters governing authority.

Retirement leaves governing authority.

Attack protects the transition.

This attachment should remain under hostile review because it is the least automatic one-to-one face mapping.

Do not force numeric symmetry if later evidence shows a better structural home.

---

# The twin contract

The word `twin` should no longer imply equality.

Use four distinct questions.

## 1. twin
What representations are related?

```text
twin:
  /src <-> /lib
```

## 2. authority
Which side governs which dimension when they disagree?

```text
authority:
  runtime: /src
  design: /lib
```

## 3. why
Why do both representations exist?

```text
why:
  /src executes
  /lib preserves readable design and reasoning
```

## 4. how
What agreement must survive between them?

```text
how:
  executable behavior must agree with documented design
  implementation detail need not be duplicated
```

This is the missing contract that should stop twin from leaking.

The principle is:

> **A twin is a declared agreement between representations, with explicit authority and transformation law.**

---

# Fractal keeps the twin contract small

Do not stamp the full contract everywhere.

A parent may define:

```text
twin:
  /src <-> /lib

authority:
  runtime: /src
  design: /lib

why:
  execute / explain

how:
  behavior and design must agree
```

A child that agrees writes nothing.

A child that differs only in one dimension writes only the difference.

Resolution:

1. read local 02,
2. if needed field is absent, climb,
3. continue until lawful value is found,
4. local explicit difference overrides only that field,
5. if no lawful value exists, remain unresolved,
6. never invent.

This is Axiom 2 + Axiom 7 operating together.

---

# Memory page — parked design direction

The memory idea should be parked for later as a **page**, not placed into face 07.

A book may eventually contain a Memory page.

That page can carry the working orientation needed to operate that book.

Its face 02 can declare which axioms matter locally.

Example:

```text
axioms:
  1 Authority
  3 Dance
  7 Missing
  8 Record
```

A memory page can also declare twins or source relationships where needed.

The important rule remains:

> memory accelerates work; it does not become authority.

A future memory page should climb for inherited memory and write only local memory difference.

That prevents it from becoming a giant summary dump.

---

# How the nine work together

The nine are strongest as a sequence of constraints rather than nine isolated slogans.

## When reading

**Record** finds the maintained source.  
**Authority** determines what governs.  
**Fractal** climbs for inherited agreement.  
**Missing** prevents invented completion.  
**Why** preserves meaning.

## When planning work

**Dance** determines who should do what.  
**Narrow** reduces the problem to the smallest lawful slice.

## When changing

**Lineage** preserves what changed and why.  
**Attack** challenges the transition before authority changes.

Then the cycle repeats.

This gives a fresh Prime a compact operational posture:

> find → determine authority → climb → do not invent → recover why → assign role → narrow → preserve lineage → attack transition

That is much closer to executable grammar than philosophy.

---

# What 02 becomes

Face 02 now has an important unifying role.

It is where a page can cheaply declare the structural contract needed to interpret it.

Possible local contents:

```text
axioms:
  1
  2
  7
  8

twin:
  /src <-> /lib

authority:
  runtime: /src
  design: /lib

why:
  execute / explain

how:
  behavior and design must agree
```

But this is not a required boilerplate block.

Use Fractal:

> **inherit agreement; write difference.**

Most pages should carry much less than this because the parent already supplies the common contract.

That prevents the axiom system from creating the very clerical explosion it is meant to prevent.

---

# Recommended edits to this draft

## 1. Strengthen Axiom 2

Current idea:
> structure repeats so change can stay local.

Add the explicit operational law:

> **Inherit agreement. Write difference.**

And preferably explain:
> climb for inherited structure; do not duplicate what the parent already supplies.

## 2. Replace twin equality language

Avoid treating:

```text
face06 = face05
src = lib
```

as literal equality.

Use relationship language or a twin contract.

The representations have different jobs.

They must agree only on the declared design.

## 3. Make 05/06 directional where needed

Preserve:

> 06 can supply/recover why for 05.

Do not require:

> every 06 creates 05.

This prevents note/overflow from becoming automatic task inflation.

## 4. Keep 07 missing

Do not place memory there.

The design discussion itself demonstrated why this axiom matters.

## 5. Keep Axiom 9 under attack

The promotion/retirement transition interpretation is promising, but it is the weakest face attachment and should earn its final wording rather than being forced for symmetry.

---

# Final assessment

This rework makes the axioms more useful because it binds them to actual operational surfaces.

The strongest new structure is:

> **Axiom = invariant reason**  
> **Face = local operational expression**  
> **02 = compact relationship contract**  
> **Fractal = inherit agreement, write difference**  
> **Twin = relationship, authority, why, how**  
> **Missing = never invent absent local truth**  
> **Map/Record = find the maintained source**  
> **Memory = future derived page, not authority**

This is a stronger kernel model.

It should make future coldboot easier because the model learns not only where information lives, but why each kind of information is allowed to live there.

The draft should continue.
