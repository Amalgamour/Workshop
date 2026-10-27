# Lab construction notes

2026-10-26. The Director approved building and testing a lab under
`D:\Git\lib-build\labs`. The workspace existed and was otherwise empty; no
applicable AGENTS file was present in the inspected ancestors or lab location.
No Git repository, desk, books, branches, or commits were created by this lab.

## Decisions made for the experiment

- Use a small deterministic route and scripted role processes to isolate compute.
- Use durable event records; derive the inbox and resume view rather than copying
  mutable job content into several inboxes.
- Record role, claim, delivery identity, artifact hash, disposition, and evidence.
- Treat duplicate identical delivery as already recorded; refuse conflicting reuse.
- Store a return and its next action in a single SQLite transaction.
- Require explicit resume of an interrupted claim.
- Bind review to the exact source artifact; reject a changed source.
- Regenerate 00.live from records; never treat its prose as proof of completion.
- Keep this lab independent of the unfinished kernel and old absolute tool paths.

## First failure and correction

The initial verification ran all 20 tests but failed with Windows file-in-use
errors during fixture cleanup. Python's SQLite connection context manages
commit/rollback but does not itself guarantee connection closure on leaving the
block. Database handles remained open.

The lab connection context now explicitly commits or rolls back and always closes
the connection. Initialization and the tampering fixture also explicitly close
their direct connections. The first failed run remains in `runs/initial-failure`.
Its source predates that correction; the log is preserved as historical evidence,
not a claim that current source reproduces the old failure unchanged.

The second staged run passed 20 tests and the eight-process demonstration. After
relocation the same suite and demo were rerun under `runs/local-pass` to check the
actual requested location.

## What the results mean

They support the specific compute contracts exercised. A scripted role can obtain
its next action and return an artifact without receiving hand-copied job paths.
An independent action can be offered while another result awaits review. A failed
return/route transaction does not leave a returned item with a missing successor.

They do not show that an LLM will correctly follow the protocol, that a UI/API can
wake an idle model, or that identifying a role authenticates the caller. The
Director decision test injects a synthetic fixture decision; it is not an
approval system. No timing benchmark or productivity multiplier is claimed.

## Next useful experiment

After the shared role and workspace contracts are agreed, let a real Builder and
Colab each consume an inbox action through the interface. Test resumption and a
required Director decision. Preserve every manual path or workaround. That is
the next boundary to prove rather than enlarging this fixture into the full app.
