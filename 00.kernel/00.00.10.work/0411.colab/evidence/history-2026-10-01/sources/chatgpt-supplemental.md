# Supplemental — Packed Axioms as Semantic Contracts

## Purpose

Axioms should not only exist as prose that a Prime reads once during coldboot.

They should also be **addressable and packable**.

A page, command, work parcel, tool, or memory object may need only a small subset of the nine axioms. Instead of restating those rules in local prose, the object should be able to declare the relevant axioms compactly and inherit their full meaning from the authoritative axiom source.

Example:

```text
axioms:
  1.3.9
```

This means:

- Axiom 1 — Authority applies.
- Axiom 3 — Dance applies.
- Axiom 9 — Hostile applies.

The local object does not reproduce the definitions.

It points to them.

This follows the Fractal rule:

> **Inherit agreement. Write difference.**

---

## Core principle

> **Packed axioms invoke constraints. They do not grant permission or authority.**

This distinction must remain explicit.

For example:

```text
>promote.ax1.6.9
```

does **not** mean the command gains authority because Axiom 1 was named.

It means the command must be interpreted and validated under:

- Authority,
- Lineage,
- Hostile.

The axiom reference constrains the operation.

It is not a capability token.

Likewise, a page containing:

```text
axioms:
  1.2.7
```

does not become authoritative merely because Axiom 1 is present.

It means those invariants are relevant to interpreting and validating that page.

---

# Why packing matters

Without packing, local objects are forced to repeat prose such as:

- resolve authority before acting,
- preserve role boundaries,
- do not fill missing state,
- keep work narrow,
- preserve lineage,
- hostile-test authority transitions.

Repeated prose creates several problems:

- more tokens,
- more clerical work,
- more wording drift,
- more opportunities for subtly different versions of the same rule,
- harder coldboot,
- harder maintenance.

Packed axioms replace repeated explanation with a small reference.

Instead of:

```text
respect authority
do not infer missing state
preserve lineage
```

the local object may carry:

```text
axioms:
  1.6.7
```

The meaning remains centralized.

---

# The axiom source remains authoritative

Packing works only if the numbers resolve back to one maintained source.

The packed form is therefore a reference, not a copied definition.

Conceptually:

```text
1 -> Authority
2 -> Fractal
3 -> Dance
4 -> Why
5 -> Narrow
6 -> Lineage
7 -> Missing
8 -> Record
9 -> Hostile
```

If Axiom 2 is refined at the governing source, every lawful reference to `2` inherits that meaning.

This is much safer than editing every page that once copied the old wording.

It also gives the kernel a powerful compression property:

> one definition, many lawful uses.

---

# Initial semantic rule: treat packed axioms as a set

The safest first interpretation is:

```text
1.3.9
```

means:

> Axioms 1, 3, and 9 all apply.

The sequence should initially **not** imply execution order.

Therefore:

```text
1.3.9
```

and:

```text
9.1.3
```

should be semantically equivalent unless a future grammar explicitly introduces ordered axiom composition.

This avoids accidentally turning a compact declaration into a hidden pipeline language.

If ordered evaluation later proves necessary, it should receive explicit syntax rather than being inferred from number placement.

---

# Pages

A page may declare the axioms needed to understand its local role.

Example:

```text
axioms:
  1.2.7
```

This can tell Prime:

- Authority must be respected.
- Inherited agreement should be climbed rather than duplicated.
- Missing state must remain missing unless lawfully supplied.

The page needs no local paragraph repeating those ideas.

A different page may carry:

```text
axioms:
  3.5.6
```

meaning:

- preserve role separation,
- narrow the work,
- preserve lineage.

This lets pages express their operating posture with very little local text.

---

# Face 02

Face 02 is a natural place to carry packed axiom relationships.

It already serves as compact machine-facing structural contract.

A small 02 might contain:

```text
axioms:
  1.2.7.8

twin:
  /src <-> /lib
```

That may be enough.

The rest climbs.

A child should not duplicate the parent axiom set unless it differs.

For example, if the parent already provides:

```text
axioms:
  1.2.7
```

and the child additionally needs Lineage, the child should ideally materialize only the local difference according to the final inheritance grammar.

The exact syntax remains to be designed, but the governing idea is clear:

> **02 should declare only what this object needs that is not already safely inherited.**

---

# Commands

Commands can use packed axioms as compact validation contracts.

Examples:

```text
>promote.ax1.6.9
```

Interpretation:

- resolve Authority,
- preserve Lineage,
- require Hostile treatment of the authority transition.

Another example:

```text
>worker.ax3.5
```

Interpretation:

- preserve worker/Prime/Director role boundaries,
- execute only the narrow authorized slice.

Another:

```text
>repair.ax2.7
```

Interpretation:

- climb for inherited agreement,
- do not invent missing structure during repair.

This can substantially reduce the number of bespoke command variants required by the grammar.

---

# Work parcels

A persistent work parcel can also carry axiom context.

Example:

```text
# 72

axioms:
  4.5.6
```

This tells the worker or Prime that the parcel should:

- preserve Why,
- remain Narrow,
- retain Lineage.

The parcel identity remains separate from the axiom contract.

The axiom list describes how the work is governed.

It does not redefine what `#72` is.

---

# Memory pages

The future Memory page can use packed axioms particularly well.

Example:

```text
axioms:
  1.3.7.8
```

This immediately tells a cold Prime how to treat the memory page:

- Authority — memory does not outrank governing files.
- Dance — memory supports Prime but does not replace Director or Clerk roles.
- Missing — absent memory must not be invented.
- Record — memory must remain refreshable from maintained sources.

That is a large amount of operational meaning carried in four digits.

The memory page then needs only its local carry state.

This helps prevent memory from becoming another giant summary surface.

---

# Twin contracts

Packed axioms can also reinforce twin contracts.

Example:

```text
axioms:
  1.2.4.8

twin:
  /src <-> /lib
```

Those references tell the model:

- Authority matters when the twins disagree.
- Fractal prevents unnecessary duplication.
- Why preserves the reason both sides exist.
- Record requires the maintained source to remain recoverable.

The explicit twin contract still answers:

- twin,
- authority,
- why,
- how.

The axiom pack does not replace that contract.

It tells the model which kernel invariants govern the contract.

---

# Packed axioms and Fractal

Axiom packing is itself an application of Fractal.

The system should avoid repeating:

```text
Authority means ...
Fractal means ...
Missing means ...
```

on every page.

Instead:

```text
axioms:
  1.2.7
```

Then climb to the governing axiom definitions.

This creates a recursive property:

> Fractal is used to carry Fractal.

That is desirable because the mechanism follows the law it expresses.

---

# Packed axioms and Missing

Packing must never become a mechanism for implied completion.

If an object says:

```text
axioms:
  1.7
```

and another expected axiom is absent, the model must not add it because it “would make sense.”

The declaration is intentional.

Missing remains meaningful.

Likewise, if a packed axiom reference cannot be lawfully resolved, the model should not reconstruct its meaning from memory.

It should remain unresolved or retrieve the governing source.

---

# Packed axioms and Authority

The most important guard is:

> **referencing Authority is not authority.**

A model must never interpret:

```text
ax1
```

as:

> permission granted.

Axiom 1 means:

> perform the authority check.

This distinction should be frozen into hostile tests early.

Example hostile case:

```text
>delete.ax1
```

Expected behavior:

- Axiom 1 requires authority validation.
- If authority is absent, the command is denied or halted.
- The presence of `.ax1` never authorizes deletion.

---

# Packed axioms and Clerk

This structure could later make Clerk significantly simpler.

Clerk can read:

```text
axioms:
  1.2.7
```

and know which deterministic checks to invoke.

For example:

- `1` — resolve governing authority.
- `2` — verify lawful inheritance/local difference.
- `7` — verify missing state was not silently fabricated.

A command carrying:

```text
ax1.6.9
```

could trigger:

- authority check,
- lineage check,
- transition/hostile check.

This begins to turn the nine axioms into a small reusable validation instruction set.

Prime reasons with them.

Clerk can eventually check parts of them.

---

# Avoiding overuse

Packed axioms should not become decorative tags.

Do not stamp all nine onto every page.

That would destroy their usefulness.

A page should carry only the axioms that materially govern its local behavior or contract.

If all pages simply say:

```text
1.2.3.4.5.6.7.8.9
```

then the pack conveys no information.

The discipline remains:

> **materialize only relevant difference.**

The global kernel already applies.

Local packing should highlight the subset that matters here.

---

# Canonical syntax

The exact syntax should remain a grammar decision.

Possible forms include:

```text
axioms:
  1.3.9
```

and command composition such as:

```text
>promote.ax1.3.9
```

The important requirement is not the spelling yet.

It is that the syntax be:

- canonical,
- easy to parse,
- difficult to confuse with ordinary numbers,
- consistent across pages, commands, work parcels, and memory objects.

Avoid multiple equivalent forms once the syntax is locked.

---

# Result

Packed axioms create a compact semantic layer above the kernel.

They allow the repository to say:

> **these invariants matter here**

without reproducing the invariants themselves.

This gives Librarian:

- semantic compression,
- fewer repeated rules,
- lower drift,
- simpler local pages,
- easier coldboot,
- reusable command contracts,
- future Clerk validation hooks.

The governing rule should remain:

> **Axioms are addressable constraints. Packing references their meaning; it does not copy their law and never grants their authority.**

Combined with:

> **Inherit agreement. Write difference.**

this may allow a very small amount of syntax to carry a surprisingly large amount of reliable model understanding.