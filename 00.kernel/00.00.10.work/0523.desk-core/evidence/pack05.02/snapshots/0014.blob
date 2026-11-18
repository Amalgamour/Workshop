# Prime review - 0523/05.01

date: 2026-10-31
who: Codex Prime
reviewed_commit: e94ca6985789c503e3d4f37019042068eef6e8f4
disposition: repair required; no live app integration

### Scope and preservation verified
The cloud builder produced a coherent CLI prototype: task/page creation,
release/claim, matching return line, captured artifacts, readable in-page review,
pending view and restart recovery. It kept all changed files inside the assigned
app/desk_core and 0523 paths. No existing app module was edited on the branch.
Four commits provide notes, implementation and delivery checkpoints. All 33
source pins and 19 declared artifact rows match the exact reviewed Git commit.
The reported nine passing tests were on Linux/Python 3.11.2. Those reported
results are not independently reproduced on that platform by this review.

### CC-01 - native Windows compatibility blocks the loop
Prime ran the exact submitted source in a separate review export on Windows with
the available Python 3.12 runtime. Nine tests ran: one passed and eight failed.
The demo failed. Write operations import fcntl, unavailable on Windows.
bookio also uses os.open/os.write without binary mode, which converts LF bytes
to CRLF on Windows and invalidates byte assumptions. A serial unit probe with
only the lock substituted failed to find the Release heading for this reason.
Repair locking and byte writes portably, preserve existing tmp/partial evidence,
and avoid truncating a pre-existing .tmp file. Prime must verify the unmodified
candidate on Windows before integration. A lock substitute is not that verification.

### Qualified supplemental logic probes
To inspect logic beyond the native platform failure, Prime ran serial unit probes
with file_lock replaced by nullcontext and low-level writes replaced by binary
Python writes IN MEMORY. No submitted source file was edited. These probes are
not native CLI, process recovery, locking or concurrency proof. Exact script,
fixture state and qualification are preserved in independent-review/.

### CC-02 - task revision loses history
revise_task overwrites the selected task JSON and face assignment without saving
the previous revision. In the qualified probe, the original task wording appeared
in no remaining book file after revision. A previous hash alone cannot recover
the old work. Preserve immutable old task AND face bytes, reason/authorizing task
reference, before/after hashes and a durable selected-version transition before
replacement. Replay and interruption must not erase or invent revision history.

### CC-03 - an old return can be reviewed as fresh against a changed task
The probe captured a return for task A, revised to task B, then supplied a new
review. review accepted it; recover reported state reviewed, review_fresh true,
complete true, despite release-stale and claim-stale conflicts. The stored receipt
still refers to task A. Validate origin/page/pass and captured task binding against
the reviewed task. Preserve old returns as historical/stale, but do not silently
rebind them to a new task. Authoritative next action must not outrank unresolved
identity/authority conflicts. Review should name the exact evidence it judges.

### CC-04 - address scope and task binding
place accepts only leading 0. Task binding omits origin page/subject/pass, so equal
task text at 0523 and 0524 has the same binding. Enforce the declared N5NN/N1NN
relationship preserving N and subject, keep N7NN local, and bind the exact task
identity. Update/version preimages rather than silently changing existing hashes.

### Protocol and runtime deviation
The assignment requested Python 3.12+ and STOP-NNN at an unexpected environment
block. The builder found only 3.11/3.10, continued, and recorded no stop. Its report
is honest about that runtime, but the stop protocol was not followed. For the
repair, 3.11 may be used for supplementary cloud checks; Windows Python 3.12+
remains the acceptance target. No install or paid CI run is required/authorized.
Unexpected failures must produce preserved stop evidence and wait for instruction.
Prime should also have made the Windows acceptance target more explicit initially.

### Architecture and limits
This is a separate synthetic-book prototype with its own versioned records, not
an integrated Clerk deployment. No real model routing or live matching-line
migration occurred. Do not merge it just because a synthetic demo is possible.
Its structured refusals are a useful start. Inspectability is now an explicit
deliverable (0416/01.003): preserve input/partial work, expose applicable contract,
observed failure and correction/escalation route. Do not infer semantic quality
from format checks or discard conflicting model work. Build a minimal trace for
this core's transitions; no broad logging platform or scheduler is required.

### Next
05.02 is the bounded repair. Keep the prototype, fix native I/O, history and exact
task/return/review identity, then rerun the existing suite and new counterexamples.
No live app merge, return migration, old allocation, Claude work or paid calls.
Full review lives on this batch; supporting evidence is under prime-review05.01.
Executable source remains on the cloud branch and in review evidence; it was not
copied into the live local app. Matching return custody remains pending 0123.
