# Prime review — shared bridge parent race
Date: 2026-10-27. Reviewer: Codex Prime. Disposition: ACCEPTED for CS-02.

The product change is confined to revalidating ordinary shared directories after
a competing creator wins. FileExistsError alone is not accepted. Link/type checks
remain; per-delivery exclusive creation is unchanged. Seven captured outputs and
the dedicated submission match their live source bytes; 0117 freshly verifies and
inspects complete with no captured-byte changes.

Independent disposable-copy reruns: directory checks 2 passes, 4 expected refusals;
seam 44 passes, 19 expected refusals, 1 symlink privilege skip; app bridge 38 passes,
27 expected refusals, 1 symlink privilege skip. No failures. Controlled directory,
file and junction races pass; existing same-delivery overlap/replay passes. The
initial restricted-environment runs could not write temporary fixtures; their
failures remain alongside the successful access-corrected runs, not erased.

This closes the reported shared-parent race, not an exactly-once or OS-sandbox
claim. Different-delivery overlapping launches remain unproved. Next draft is a
bounded integration test for that boundary, without changing product code unless
a later repair is separately authorized. Claude and Grok-2 work remain untouched.
