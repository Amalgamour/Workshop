# Coverage — 0525.app-dependencies/05.02

The successor reader answers the same commands as labs/module-dependencies-pass01/depdecl.py. module-declaration/1 output on the unchanged app set and the prime-cycle chain set matches that reader. The corrected app set is module-declaration-set/2, review-loop-entry-2.

## What changed in the machine record

D-04. Nine modules use basis.kind observed-file, form working-tree. context_head is 960d20c5290656095df8457b1740d2d5e586b111 and does not identify the bytes. Three modules whose working-tree git object equals that HEAD use basis.kind git-blob with verification supplied-unverified. The reader accepts no other kind and refuses a verification value of verified. It does not fetch Git.

D-05. return-inspect-pass01 requirement return-capture is digest-only: sha256 8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac, bytes null. requires resolves it. identity lists it as digest-matches on the helper fixture and does not call it a pair match. impacted depth 1 and depth 8 list it as digest-matches. With --implementation set to that sha, against_implementation is pin-matches. A missing pin length did not become unpinned and did not become a size match.

The other edges stay as they were. Pair pins stay pairs. Null pins stay unpinned. The JSON declaration still stores hashes and does not open the files, so those edges stay unpinned document edges.

## What the corrected graph answered

validate exit 0, status valid. requires --transitive exit 0, status complete-for-declared-coverage, findings condition-inapplicable 1, environment-unverified 21, shared 33. requires --depth 2 exit 1, status incomplete, findings depth-limit 9, environment-unverified 5. identity exit 0, 12 fixture copies identical. explain exit 0, three paths, the same door-first routes as the /1 set. The inspect path is now resolved rather than an unpinned selection. impacted --depth 1 exit 1, status truncated. Unexpanded direct consumers: return_lines.py 5, return_placement.py 7, return_inspect.py 6. impacted --depth 8 exit 0, status candidates-for-review, 29 consumers, finding_counts empty. Librarian is at depth 3, pin_form unpinned. The disposable set that drops the capture record exits 1, status incomplete, record-missing 3.

complete-for-declared-coverage is not closure.

## Limits kept on purpose

1. Face tokens with an extra segment. 0512.prime-review/05.01.002 still does not fit the address form. It stays in provenance.unknown. The grammar was not expanded.
2. The loop's contract path stays a provenance link. An address target would be address-unresolved, and a document edge would claim a load the loop does not perform. The reader still does not open addresses.
3. Environment rows stay unverified. The caller book and the fixture root were not probed.
4. run, reproduce, and the old facade stay outside this set.
5. The placement custody load stays conditional and inapplicable for the route command the entry calls. requires lists it and does not follow it. impacted still shows the consumer.

## Tests

Predecessor tests were run and left unchanged: test_depdecl.py 15 OK, test_repair.py 7 OK. Successor tests: 8 OK, including the stdout comparison on the unchanged /1 fixtures. Raw logs are in evidence/build05.02/tests. No unexpected refusal occurred. The exit 1 command results are the depth bounds and the missing capture record.
