# RETURN — 00.axioms.002-draft — Colab Pass 02
date: 2026-10-01
mode: colab pass 02
state reviewed: draft only
promotion: **do not promote from this return**

## Overall call

**Pass 02 is materially better.**

The rework now has a coherent kernel shape:

> axioms are reasons  
> faces are local expressions  
> `02` carries compact structural contracts  
> `04` is readable check, not storage  
> twin is declared agreement, not equality  
> Fractal minimizes duplication  
> Missing blocks invention

The remaining issues are now mostly **wording precision and tired-model failure modes**, not architectural collapse.

I would continue to Pass 03 after tightening the points below.

---

# 1 — Authority

## Question
Does “authority may split by dimension” hold, or does one side have to win? Where does this break?

## Assessment

**It holds. Keep it.**

One side does not need to win globally.

`/src` can govern executable behavior while `/lib` governs documented design intent.

The important requirement is that the dimensions themselves are explicit and non-overlapping enough to resolve conflict.

Where this breaks:

1. two sides claim the same dimension;
2. a dimension is unnamed;
3. a local child silently changes the dimension split;
4. “design” and “runtime” disagree about behavior and no reconciliation rule exists;
5. a model treats one authority win as universal precedence.

### Needed guard

Add or preserve the concept:

> **Authority may split by dimension; overlap requires resolution before either side may silently win.**

That is the failure boundary.

---

# 2 — Fractal

## Question
Is “inherit agreement, write difference” enough to stop a child from copying the parent? Where does the climb invent?

## Assessment

The phrase is strong enough as the axiom.

But the implementation rule still needs one more edge:

> **absence means climb only when inheritance is legal here.**

Otherwise a model can treat every missing field as permission to search upward indefinitely.

The climb invents when:

- the parent does not own that field,
- the relationship is not inherited across that boundary,
- several ancestors provide incompatible values,
- the model guesses a parent because the expected one is missing.

So the full behavior is:

> inherit agreement; write difference; climb only through lawful inheritance; if no lawful source exists, remain missing.

That last clause is what keeps Fractal from becoming “search until something fits.”

---

# 3 — Dance

## Question
Is a menu the right face for the seat split? There is no Clerk yet. Prime fills that function. Does that leak?

## Assessment

**Menu is a good local expression of Dance.**

Face 03 says:

> this points; it does not become what it points to.

That is role separation in miniature.

The current risk is this sentence:

> “Clerk opens the face.”

It is more implementation-specific than the rest of the axiom and could age badly.

Since there is no Clerk yet, a cold model may over-read it as a required actor rather than an eventual division of labor.

I would prefer the axiom to stay role-level:

> human directs; model reasons; compute maintains.

Then the local current implementation can say:

> no Clerk yet; Prime temporarily performs required compute-maintenance work.

That keeps the axiom durable while allowing the present architecture to be honest.

---

# 4 — Why

## Question
Is face 04 safe as the readable whole, or will it become storage? What would you refuse to put there?

## Assessment

It is safe **if “adds no new law” remains absolute.**

I would refuse to put any of these in 04 unless they already exist in 01–03:

- new authority
- new exception
- new command behavior
- new lifecycle state
- new task
- new map relationship
- new unresolved research fact

04 can explain.
04 can synthesize.
04 can make the whole readable.

04 cannot originate governing meaning.

This is one of the strongest parts of the draft now.

A useful tired-model test is:

> If deleting 04 would remove a rule not recoverable from 01–03, 04 has become storage.

---

# 5 — Narrow

## Question
Is “size of the work” distinct from Fractal? A clock was pulled out of this axiom. Did that leave a hole?

## Assessment

**Yes, they are distinct. Keep the split.**

Fractal answers:

> how much structure must be restated?

Narrow answers:

> how much work should be attempted?

The clock was correctly removed.

Time budget is an execution envelope or scheduling constraint, not a foundational definition of narrowness.

No kernel hole was created by removing the clock.

A narrow task may take a long time.
A broad task may be given five minutes.

Those are independent dimensions.

---

# 6 — Lineage

## Question
Is “a note does not mint a task” the right direction? What active work has no recoverable why, and should it be allowed?

## Assessment

**The direction is right.**

Not every note should become work.

But I would slightly sharpen:

> important active work must have a recoverable reason **unless the work is itself a direct primitive instruction whose reason is the instruction.**

Examples:

- “rename this file exactly” may not need a separate explanatory 06;
- “change authority precedence” absolutely does.

Otherwise the system risks inventing ceremonial notes for trivial mechanical tasks.

The principle is not:

> every 05 requires prose in 06.

It is:

> **the reason for consequential work must remain recoverable.**

That keeps Lineage strong without bureaucracy.

---

# 7 — Missing

## Question
Is a hole a valid structure? Is the inferred-on-draft bound enough? What would you still fill?

## Assessment

**Yes. This is now one of the strongest axioms.**

A hole is valid structure.

The inferred-on-draft rule is good, but I would attack one phrase:

> “Inferred meaning may sit on a draft, marked inferred”

This is useful, but the model needs to understand that inferred material is not inherited as though it were fact.

Otherwise a child can climb into an inferred parent and accidentally harden speculation.

Potential guard:

> **Inferred may inform draft reasoning; it does not become inherited agreement until lawfully resolved.**

I would still fill:
- explicit required structural metadata whose absence makes the object malformed.

I would not fill:
- semantic content merely because a seat exists.

That distinction matters.

---

# 8 — Record

## Question
Map points. Memory is not authority. Is that enough for a cold boot, or does the boot still need a jam?

## Assessment

The axiom is strong enough.

Coldboot still needs an **entry procedure**, but that is not a missing axiom.

Record answers:

> where can maintained truth be recovered?

Coldboot procedure answers:

> in what order should a fresh Prime recover enough of it to operate?

Those should remain separate.

The sentence:

> “This is the same live box as Authority. The split is the route, not a second rule.”

is intellectually correct but probably the most cognitively dense line in the whole draft.

A tired model may not know what “same live box” means operationally.

I would simplify.

Something like:

> Authority decides what governs. Record makes that governing source recoverable.

That says the same thing with much less interpretive load.

---

# 9 — Hostile

## Question
Does demotion of “take the best” lose a guard?

## Assessment

No important kernel guard is lost.

“Take the best, invent the rest” is a useful research heuristic.

It is not a safe invariant because “best” is evaluative and context-dependent, and “invent the rest” can conflict directly with Missing.

Demoting it was correct.

The new Hostile axiom is stronger kernel material because it constrains authority transition.

The part still needing polish is the relationship to face 09.

Current wording solves most of it by saying:

> Primary: the transition. Promotion enters. Retirement leaves.

That is better than pretending Hostile *is* face 09.

Keep that distinction.

---

# Hostile pass

## Sentence that fails first

> **“This is the same live box as Authority. The split is the route, not a second rule.”**

Reason:

It is compact but ambiguous.

A tired model can interpret:
- Authority and Record are identical,
- Record is only a pointer,
- or Record has no independent operational consequence.

The idea is good.
The sentence is not yet robust enough.

Suggested concept:

> Authority determines what governs. Record ensures the governing source remains recoverable.

---

## Sentence a tired model may obey as law when it is only draft

The highest-risk line is not inside an axiom.

It is:

> **“A one-digit axis is an axiom. `1` through `9` are the only valid one-digit axis.”**

Because it appears repeatedly and categorically, a model may begin treating it as live syntax despite every file saying draft.

This is a useful hostile result.

The content may be correct, but the draft is already demonstrating Axiom 1:

> written repeatedly is not the same as governing.

Before promotion, make sure the live syntax does not conflict and that coldboot cannot absorb this draft as live grammar.

---

# Structural cracks still visible

## 1. “Primary face” language risks re-coupling axiom and face

The draft now correctly says axioms are not faces.

But repeated:

> `Primary: face XX`

may still cause a tired model to infer a one-to-one identity.

I would keep “primary expression” or equivalent wording wherever possible.

The distinction should remain:

> axiom = invariant reason  
> face = local expression

not:

> axiom 2 means face02.

That difference will matter if a future page uses several axioms at once.

---

## 2. 02 is becoming important enough to overgrow

The current card is excellent because it is small.

Protect that.

Do not let 02 become:
- schema dump,
- rule mirror,
- metadata registry,
- or a second 04.

Its power comes from compact structural ties.

The best line in the whole pass may be:

> **Inherit agreement. Write difference.**

Apply that to 02 itself.

---

## 3. `src <-> lib` needs scope

The example is useful, but it risks becoming universally assumed.

Not every object necessarily has `/src` and `/lib`.

Keep it clearly as a declared twin pattern, not a mandatory repository law unless that is explicitly intended elsewhere.

---

# Pass 02 result

I would mark this:

**ARCHITECTURE: PASS**  
**WORDING: NOT YET LOCK**  
**PROMOTION: NO**  
**NEXT: PASS 03 hostile wording / contract precision**

The draft now survives the important conceptual attacks.

Pass 03 should be smaller.

Do not redesign the nine again unless a hostile test actually breaks one.

Focus on:
- tired-model ambiguity,
- inheritance boundary,
- inferred-draft behavior,
- Record wording,
- primary-expression wording,
- authority overlap.

That is craftsmanship territory now.
