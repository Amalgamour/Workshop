# Proposed job preparation design

Status: discussion draft. No governing changes requested by the presence of this document.

## The division of work

Model: notice work, understand its why, reopen governing sources, decide what request is needed, supply evidence and recommend a bounded next act.

Compute: expose the command requirements, validate the structure, resolve an explicitly configured destination, allocate a batch filename, and render a consistent review surface.

Director: resolve the questions, change recommendations, release specific acts, or hold them.

Worker: reopen the recorded decision and current sources, check scope and authority, carry out the released act, and record evidence. This prototype does not implement that worker.

## Preparation pseudocode

```text
when a model notices work requiring Director review:
    identify the book being worked from current context
    identify the bounded problem and its why
    read the behavior door and named command member
    consult job.py describe for request requirements

    if the intended verb is unknown:
        report the missing contract; do not substitute a familiar verb

    reopen the target and governing sources
    prepare issue, recommendation, exact ask, source/section, and done
    supply the verb's additional parameters
    name dependencies on other requests, if any

    resolve explicit route: this book -> its existing designated job page
    if missing, ambiguous, reserved, or outside the declared work range:
        explain the missing routing decision; write no batch

    validate all items before opening an output file
    preview the batch
    create next 05.NN exclusively; never overwrite another batch
    leave reply blank and receipt pending

after the Director replies:
    execution is a separate governed operation
    do not infer release from a nonblank reply
    do not infer release from a >token in quoted text or a proposal
    resolve changes to intent and scope against the item
    if the reply is ambiguous or changes dependencies:
        return a bounded question before the dependent act
```

## Proposed law placement

The behavior band should define each verb's permitted effect, required actor, release conditions, holds, and completion evidence. This prototype's `commands.json` is a candidate interface to those definitions, not a competing authority. Ultimately compute should consume an approved, versioned contract or validated export with a source pointer.

The structure band should define the job page's class/location, the `05.NN` envelope, item markers and fields, routing configuration, allocation limits, history preservation, and receipts. Law `0005.ticket` should distinguish batch files, item markers, and its internal/outward labels explicitly. Law `0015.grammar` still identifies syntax; it must not silently become an execution engine.

Whether the route points to a central job page or the current subject page is a Director design decision. Starting with an explicit map lets us test preparation without settling band allocation by accident. Page creation must use the eventual approved builder and preserve address/proof rules.

## Where examples teach better than a command name

A weak `>fix` request says: "Mapping is broken. Fix it." It lacks a target, the contradictory relationship, a governing section, desired behavior, and evidence of completion. `job.py` stops on missing fields instead of presenting it as ready for review.

A useful request identifies the exact map entry, explains its mismatch with the named source section, proposes the corrected relationship, states which draft will change, holds unrelated entries, and says how the resulting pointer and representations will be checked.

A complete form is still only a complete proposal. Text saying "patch allowed" does not establish permission; the worker must open the actual governing rule before execution. The current dev exceptions, the signed point test, and note/notes usage are precisely where that check matters.

## Completion receipt proposal

```text
decision_source: exact batch and #NN, with the Director reply preserved
released_scope: files/sections and excluded work
result: completed | partial | blocked
changed: exact resulting files/versions
verified: criteria, command/result, and relevant before/after evidence
unresolved: explicit missing decisions or failed checks
preserve: why that belongs in long-term notes
```

Receipt format and closure are proposals only. The prototype leaves a pending receipt rather than asserting any of these steps occurred.
