# Prime report — lib-build proposal pass 02

Date: 2026-10-26  
Reviewer: Codex, Prime  
Return: D:\Git\Librarian\colab\returns\claude-opus-5-5-lib-build-pass02-2026-10-26  
Disposition: useful design package; revise before running preservation/setup tools

## Contribution and alignment

The return now includes a concrete setup proposal, two draft assignments,
preservation and import manifests, collision records, and two draft tools.
It accounts for the existing lab and proposes Git initialization in place instead
of assuming an empty destination. It adopts one desk/three books, separates
behaviour from structural roles, places runtime on law pages using N3NN, preserves
unfinished candidates, and distinguishes dev-mode execution from active modules.

The manifests and collision handling are a substantial improvement: source
identities are explicit rather than reconstructed during migration. This package
is much closer to an executable assignment than pass 01.

No instructions from the return were executed. Prime read proposal.md,
setup-assignment.md, preservation-assignment.md, preserve.py and import.py, then
independently parsed the manifests and verified preservation source hashes.

## Verified facts

- The preservation manifest has 118 files: P1 22, P2 3, P3 9, P4 47, P5 8, P6 1,
  P7 28. All 118 current source files match their recorded SHA-256 at review time.
- The import manifest actually has 890 rows: 688 minimum and 202 later. The
  proposal's 882-row headline is incorrect. No duplicate destinations were found
  in a case-insensitive textual comparison.
- This does not verify every import blob/destination, execute either tool, or
  establish that preservation-copy mode is safe.
- The lab remains a distinct experiment, not adopted authoritative SQLite storage.

## F01 — New law drafts are still written at the seat

setup-assignment S5 says new law role/handoff/compute-door faces are FF.md with
state draft. The Director explicitly changed kernel/syntax/law drafting to start
versioned, including 001. New kernel drafts must follow that decision. Distinguish
ordinary work pages and expected executable cards from the versioned law-draft
rule; do not apply a blanket filename rule without stating the cases.

Acceptance: the assignment's new law candidates are named explicitly and none is
silently installed as active law. Existing seats remain intact.

## F02 — Setup checks require adaptations that the scope excludes

The assignment excludes adapting tool code beyond stamps. Nevertheless A5 requires
candidate code to contain no old kernel.draft or rebuild paths, and the proposal
itself identifies those paths in Clerk and Jobs. S5 also asks for candidate tooling
with --candidate/--sha256/--scope before the entry implementing those options is
built in S6. A4 includes an AGENTS header/cold walk dependent on Director seating
004, but that happens after the proposed checks.

Split the work into honest finish lines:
1. preservation plus exact workspace/import setup, with provenance and no active
   runtime claims;
2. scoped entry and path adaptations, tested in fixtures;
3. Director-reviewed activation and a real cold-model check.

Tests depending on an unimplemented or unseated capability must wait on that
dependency; do not mark them passed or remove them.

## F03 — Preservation copy mode lacks its promised destination safeguard

preserve.py's docstring says it refuses a destination containing different bytes
unless they were committed in destination HEAD. The implementation checks source
hashes and that .git exists, then mkdir/copyfile to each destination. It never
checks destination HEAD, dirty target contents, or resolved destination containment.

The manifests checked today are concrete and have matching sources; the finding
is a gap in the drafted tool's copy guarantees, not a claim that source files have
been overwritten. Do not run copy mode yet.

Before release, preflight all destinations. Allow only the explicitly authorized
clean-base replacement or a new destination; refuse unexpected dirty contents,
path escape and symlink escape. Add isolated tests of refusal leaving all target
bytes unchanged. Verify after copy. A successful --check of source hashes does
not establish those guarantees.

## F04 — Preserve broadly, expose active material selectively

The package now imports both whole books, including retired material, drafts and
notes, into the active book locations. Keeping these versions is correct. Making
all preserved material part of a 'minimum' working tree is a separate choice and
risks recreating the previous ambiguity.

Preserve complete byte-exact snapshots. State which exact references/candidates
the initial entry uses, and how all others remain historical or inactive. Do not
promote old stamps automatically. Whether snapshots live under imports/ or in the
book's declared archive, the runtime and cold reader need an unambiguous selection.

Do not undo the Director's instruction to retain important .VVV material. Improve
selection and custody rather than discard unfinished work.

## F05 — Orientation and meaning selection need one owning record

The proposal correctly says 00.live is a derived view, but the entry description
also says it reads context from 00.live. Resolve context from its authoritative
work/assignment record, or regenerate/validate the view before consuming it. Never
let stale or hand-edited summary text redirect work across books/spaces.

Handoff lab behavior supports this requirement but does not implement the new
file-based production record or authorize changing 'files are truth'.

## Smaller corrections

- Correct 882 to 890 rows; show counts before and after adding P1 import rows.
- The lab has 20 total acceptance tests, not 20 negative tests. Its successful
  route and fixtures establish bounded claims, not general model routing.
- If code/data stamps or paths are adapted, record original and derived hashes
  distinctly so a byte-exact import claim remains true only of the snapshot.
- Different-family review is useful independence, not necessarily a universal
  definition of Colab. Preserve the Director's ability to assign roles deliberately.
- 'Return and routing are one operation' means durably recording the result and
  next delivery obligation. A temporary inability to reach an external recipient
  must not require losing completed work. The lab tested one local transaction;
  delivery across machines remains a later boundary.

## What was learned

Preservation and activation are different operations. Candidate identity, source
history and local authority must survive independently of a clean-looking layout.
Exact manifests make real review possible, but a tool's stated safeguard still
has to be compared with its implementation and failure tests.

The next work should be narrowly executable. Do not combine safe capture, new
layout, new loader features, changed law, and final activation into one pass whose
checks assume all of those already exist.

## Recommended next action

Ask Claude to revise only the blocking assignment/tool contracts and return one
releaseable preservation slice first. Keep the workspace setup staged separately.
Bring the Director a small decision surface naming actual policy changes, not
routine count corrections or implementation details.

The Director requested a temporary notes directory after Claude's manifests were
prepared. D:\Git\lib-build now contains notes/ as well as labs/. Include these
new notes in the workspace baseline and preservation plan. They must not disappear
because an older setup step expected labs/ to be the only untracked content.

Book 04/why is recorded as an open proposal in understanding-and-reuse-2026-10-26.md.
It is not part of the setup scope until its purpose/address is decided.

## Source identity

- proposal.md SHA-256: 1d74f6451dd67681c0f98f914c9ba12c5ca28adb37bd06d8729ba37565d413c4
- setup-assignment.md: e2a83c7e8136940c97544a7bbcf2201d0563e1cfd7a88bf50b78d68b2d1f9e91
- preservation-assignment.md: 830241e80a9d6916656a6a96d1bb733093625575c77eb485513c13a94c64dfc8
- preserve.py: fd34b4655cf792e85d8ff135da2634f8e7e60cbe520a63595fb00284cbfb93ce
- import.py: 238d1d68324c48fefe025b627b31966cfeea5ef8e60c8ebd9ee3a5d781a0646e

These hashes identify reviewed drafts, not approved implementations.
