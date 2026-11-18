# Submission - 0512.prime-review/05.07

date: 2026-11-03
executor: Grok-1
reviewer: Codex Prime
accepted: false
committed_by_this_builder: false
custody: pending
matching line: 0112.prime-review unfiled
readiness: returned for Codex Prime review

This is the builder return for the named invocation of 05.07. It is a claim. It is not acceptance, not custody, and not a release. Notes in 06.11.md were reread after the author suite and integrated there. The contract was not revised after tests. This file does not carry the artifact-manifest hash. That hash is written only on the 05.07 return pointer after the manifest exists.

## Did

Verified evidence/pack05.07/source-manifest.json before the notes. Schema prime-pack-inputs/1. Twenty-seven files. bad 0. missing live 0. missing snapshot 0. live drift 0. snapshot mismatch 0. extra snapshots 0. Manifest sha256 ea2bc5c5f163cfffe558776b9335e60c9f5ac261861d5725f0422e8454d80bd6, 6728 bytes. HEAD 960d20c5290656095df8457b1740d2d5e586b111. Branch workshop. Index empty. The freeze was not repinned.

Read 06.10.md. The pass03 reporter stays accepted within its stated technical scope. This pack does not select an app route. app/librarian.py was not edited.

Built the staged connector app/review_report_tools_v1.py and app/review-report-v1.json. The staged command is python -B app/review_report_tools_v1.py --book ABS --source PAGE --pass 05.NN. It checks arguments, refuses a copied root, checks the twenty-three launch pins, then starts the existing pass03 reporter once and copies stdout, stderr, and the integer exit. It does not record, publish, or approve. Exit 0 is not a release.

The unapplied dispatcher proposal is labs/review-report-app-pass01/librarian.py and labs/review-report-app-pass01/DISPATCHER.diff. The proposed command, after a later review, would be python -B app/librarian.py review-report --book ABS --source PAGE --pass 05.NN. invoke.py runs that source with __file__ set to the installed app/librarian.py and refuses unless the on-disk dispatcher is still the pinned bytes. The exact diff, the rollback, and the pin consequence are in evidence/build05.07/INTEGRATION.md.

app/review_report_tools_v1.py sha256 00489768c33874b282a3732709eb40503d0c3ebfad2826a9b3e8be6d832a5e2c, 13708 bytes. app/review-report-v1.json sha256 5295f98fe22024524bf9059fee24c3a617da73ed3ed58deff8c726080c64445b, 3818 bytes. tests/test_connector.py sha256 e898595547b8fec12600cc3ee83b756184bdcf99cac06229a0d1c6208e7594e1, 24046 bytes. invoke.py sha256 098bfb0763c72222c8a997c355bc0cce8a9e1217abcf731380b80efc91e69caa, 1384 bytes. proposed librarian.py sha256 b253a89751a48b64089bb95c4fde3715de00e6dc3c61dd8bad8653051234f3fa, 12792 bytes. DISPATCHER.diff sha256 59badbc21f7d91444e4e580b1ae4521142179e61dcefca0de09a491ca04ba3c7, 1981 bytes. CONTRACT.md sha256 a2a915e2ab133eb3fb4536d1c7d50361ea33d9a11dca14654a6aeea3d3cedc08, 7879 bytes. 06.11.md sha256 73d574c9f664e77282e4d11042fc961ffbd0546ba1f8eb933380341c956f9ed8, 17530 bytes. INTEGRATION.md sha256 abf94262fc7e9f9af57f6ed53e4d4f76cf8224d35742945f5085a535140fdf14, 5233 bytes. PRIME-USE.md sha256 fc9da59ad3ba764acbdacb8ef4cd137b259a38f41edda56f3aecadd06ae577ef, 1436 bytes.

The recorded author run was 15 tests, 18.090 seconds, OK, exit 0. Python 3.14.0. The log is evidence/build05.07/author-suite.txt. The first failing log is evidence/build05.07/author-suite-first.txt. Repairs stayed in the lab. The contract was not revised. The cases are author cases.

The live observation used three processes on each address. 0512.prime-review pass 05.06: exit 0, state readable, review wbf38837cf0fa9c6b, observation coherent and stable, stale false, publication published and class complete, disposition accepted, custody missing, authority none, work_complete false, action_released false, accepted false, approved false, closes_work false, releases_action false, task_association not-established. tests_passed true is a supplied bounded assessment, and tests_note is present. Declared artifact entries 14, 149885 bytes. Measured artifact rows 14, 149885 bytes. Intake role rows 17, 169310 bytes. Addressed source paths 16, 157007 bytes. Content blobs 15, 127265 bytes. Verified physical files unknown. Artifact hash_match 14, hash_mismatch 0, not_verified 0. Measurement complete. Attention lines 5. Stdout sha256 8a1e16649fd632400c49e6c68171f40df416229a76910eae5c3780c4aab566d0, 22083 bytes. Stderr empty. The three processes matched.

0521.return-placement pass 05.13: exit 0, state readable, review webe8f0a86f3de800, observation coherent and stable, stale false, publication published and class complete, disposition accepted, custody missing, authority none, work_complete false, action_released false. The same release flags are false. tests_passed true is a supplied bounded assessment, and tests_note is present. Declared artifact entries 5, 81671 bytes. Measured artifact rows 5, 81671 bytes. Intake role rows 9, 95759 bytes. Addressed source paths 7, 90980 bytes. Content blobs 7, 90980 bytes. Verified physical files unknown. Artifact hash_match 5, hash_mismatch 0, not_verified 0. Measurement complete. Attention lines 6. Stdout sha256 2fb63cd92c6234a1c9f734629c23cdae2a80ab99c804f604b406f908f74f7a2e, 19894 bytes. Stderr empty. The three processes matched.

Disposable fixtures under D:/librarian/temp/0512-0507-report: missing review state not-recorded, exit 1, stale null; edited note state stale, exit 1; digest mismatch state held, exit 1. Each was byte-identical across the three commands, and the fixture tree matched around the report calls. Setup prepare, record, and publish used the existing review-loop on those disposable books. The connector command did not record or publish.

Frozen source bytes for the dispatcher and the three reporter modules matched the pack05.07 manifest after the suite. app/README.md stayed sha256 3c2125aa0cebd7ddc1604de2a823c1250edf40a8e97bd7dbd2eb09ca91155920, 39687 bytes. app/librarian.py stayed sha256 c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9, 12204 bytes.

## Blocked

Matching line 0112.prime-review is unfiled. This slice does not file it and does not invent a receipt. Custody on the live reviews stays missing. Verified physical-file identity stays unknown. The shared command is not selected. Applying the dispatcher diff would change app/librarian.py and the existing pin would refuse that file. This pack does not update the pin. Codex Prime has not reviewed this pack. This builder does not commit.

Empty authoring, with no subcommand, stops at `unknown authoring command`. The contract sentence that says empty authoring stops with `missing --book` describes the check that follows a known subcommand. `authoring form` without a book stops with `missing --book` before a subprocess. The contract file was left as locked. A file symlink could not be created because the privilege is not held. The linked-pin author case used a directory junction instead.

## Need

Codex Prime review of this return. The staged command, the unapplied diff, and the rollback are in evidence/build05.07/PRIME-USE.md and evidence/build05.07/INTEGRATION.md. Stop here.

## API and ownership

The caller supplies an absolute book, a source page id, and a pass. The connector derives the code root from the installed app. It refuses a second root. It hashes the reporter chain and the pass01 dependency cut, then forwards one pass03 process. Exit 0 means the reporter's readable state. Exit 0 is not approval. Exit 1 is the reporter's stale, held, not-recorded, or identity-mismatch result. A connector refusal is exit 2, empty stdout, and a `stop:` line, before the reporter starts. A reporter refusal is forwarded with the reporter's JSON object and its `refused:` line.

The proposed dispatcher adds only the review-report command and its handler. Rollback restores app/librarian.py to sha256 c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9, 12204 bytes. Until a separate review updates that pin, the staged tool command is the one that passes the pin check.

## Claim, case, result, limit

The table is evidence/build05.07/TEST-TABLE.md. The command hashes are evidence/build05.07/command-log.json. The no-write watch is evidence/build05.07/no-write.json.
