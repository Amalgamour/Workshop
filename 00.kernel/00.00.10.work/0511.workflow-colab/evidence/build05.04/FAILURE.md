# Failure and recovery — workflow pass03

date: 2026-11-01
who: Grok-2
state: written before labs/colab-workflow-pass03

This plan covers seal-return-local, open-pass, and the mutations pass03 still shares with pass02. It does not add a repair command.

## Write sequence

commit performs these steps in order:

1. Create .write.lock with the bytes 1 and a newline.
2. Write each extra file. For a new return, the extra file is artifacts/<pass>/return.md and it receives the canonical bytes.
3. Write the projections, including 01.md, 08.md, and any 05.NN.return.md that the record now names.
4. Write investigation.json, including the extended transition list.
5. Write seal.json as the sha256 of those investigation bytes.
6. Remove partial.json if it is present and is not a reparse.
7. The finally step removes .write.lock when it is present and is not a reparse.

A Refuse raised by a check propagates and does not write partial.json. Any other exception writes partial.json with schema colab-exchange-partial/1 and reason interrupted write, then raises Refuse interrupted write with wrote true. The lock is still removed in finally.

write_bytes calls WRITE_HOOK before it opens the destination. A hook that raises therefore does not truncate the destination. A crash after truncation has begun is outside this plan. No race-freedom and no power-loss guarantee is claimed. AR-01 stays held. Hard-link probes are not used.

## Visible partial state

require_loaded refuses resume refused when partial.json or .write.lock exists. That check happens before the seal comparison. show does not load such a page. It reports partial true, passes [], and transitions null. The show command’s own result name can still be complete, and that name means only that the read finished. It does not mean the page is a completed exchange.

An interrupted seal is not a successful seal. An orphan artifacts/<pass>/return.md or a projection written before the failing step may remain beside the last sealed investigation.json. The tool does not delete those leftovers and does not delete partial.json.

Boundaries the tests inject, one failure each, are the return artifact, the page-local return projection, investigation.json, and seal.json. The same injection on attach, at the first artifact write, stays as the existing interrupted-write case.

At the seal.json boundary the new investigation.json may already be on disk while seal.json still names the previous bytes. partial.json makes the page refused. If the marker were absent, the seal disagreement would still refuse resume. The tool does not roll either file back.

## What stays

A hook failure before investigation.json is truncated leaves the previous investigation bytes and the previous seal in place. Earlier pass files that commit had not reached stay as they were. Diagnostic facts are the partial marker, the command result reason interrupted write, wrote true, and whatever extra or projection files the sequence had already created. Those facts are kept for a later Prime reading. They are not a successful transition.

## Recovery

There is no automatic restore and no cleanup subcommand. The bounded result is stop. A later command on that page returns resume refused and writes nothing. Removing the marker, replaying a half-written record, or deleting an orphan inside the tool would hide the partial state. That is not done to make a test pass. Recovery, if any, is a later Prime decision on the preserved page.

A refused command that fails before commit, including occupied content, a transport label change, a missing prerequisite, and a hash conflict found on load, has wrote false and does not create partial.json.
