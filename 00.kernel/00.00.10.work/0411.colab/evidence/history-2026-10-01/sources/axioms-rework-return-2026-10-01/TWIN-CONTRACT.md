# TWIN CONTRACT — candidate design

## Principle

> A twin is not equality.

A twin is a declared agreement between two representations that have different jobs.

Every meaningful twin should be interpretable through four questions.

## 1. twin

What representations are related?

```text
twin:
  /src <-> /lib
```

## 2. authority

Which side governs which dimension?

```text
authority:
  runtime: /src
  design: /lib
```

Authority may be split by dimension.

Do not assume one side globally outranks the other unless the contract says so.

## 3. why

Why do both sides exist?

```text
why:
  /src executes
  /lib preserves readable design and reasoning
```

The why prevents a future model from collapsing one side simply because the other appears sufficient.

## 4. how

What must agree?

```text
how:
  executable behavior must agree with documented design
  implementation detail need not be duplicated
```

`how` is the actual agreement boundary.

## Fractal rule

> Inherit agreement. Write difference.

A parent contract should not be copied into every child.

Resolution:

1. read local contract;
2. use locally written difference;
3. climb for missing inherited fields;
4. stop at first lawful governing value;
5. if no lawful value exists, remain unresolved;
6. never invent.

## Example — page twin

```text
twin:
  face01+02+03 <-> face04

authority:
  governing-law: face01

why:
  01-03 provide operational structure
  04 provides the readable whole/check

how:
  governing meaning must agree
  04 adds no new law
```

## Example — work/lineage relationship

This is not strict equality.

```text
twin:
  face05 <-> face06

authority:
  active-work: face05
  recorded-reason: face06

why:
  05 makes work resumable
  06 preserves the intelligence behind it

how:
  active work must have recoverable reason when reason matters
  notes do not automatically become tasks
```

## Example — code twin

```text
twin:
  /src <-> /lib

authority:
  runtime: /src
  design: /lib

why:
  /src executes
  /lib explains and preserves design intent

how:
  implementation and documented design must agree
  implementation detail does not need duplication
```
