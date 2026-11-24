# Report

- Builder: Grok-1
- Page/pass: 90.50.10.0701 05.03
- Kind: repair-prep
- Commands run: git fetch origin packs; git fetch origin returns; git fetch origin prima/build; git show 80f8dfeb:docs/review/0701-LOG-REPAIR.md; git merge-base --is-ancestor for a823ee28, b142884d, and origin/returns; byte compare of the three 0701 logs. No claim, replay, check, pack, or page-log write.
- Results: the published 0701 picture is unchanged. Packs holds the 22-line prefix. Returns holds 24 lines whose last two are the 05.02 claim and return. b71ab3e0 still holds the displaced 05.03 claim and return. a823ee28 is an ancestor of b142884d. b142884d is an ancestor of origin/returns. The old plan's step 4 states that second link in reverse.
- wf entry numbers: none filed. Live 0701 head is still entry 24. This prep does not append.
- Push commits: report only. Cited commits are listed below.
- Findings: below.
- Time taken: filled at the end from the machine clock.

## Cited commits

- Repair note: prima/build `80f8dfeb434e1dc4742abc6305046c5e3fbbfbda`, `docs/review/0701-LOG-REPAIR.md`.
- Returns tip read for this report: `35f246502b3742fca2afdc158216e723539ccac2`.
- Lead assignment that named this prep: `d34fe4963fb68c4c324cfb458e4c9f61a222b7b7` is an ancestor of that tip. The 0701 log blob is the same at both.
- Packs tip read for this report: `49295a68bf01c1e507fe751d4bb7572d4eac6313`.
- Original 05.03 filing: `b71ab3e07376345bc762771367e5c224d1860b31` (`wf: return 90.50.10.0701.05.03 (log)`). It is an ancestor of origin/returns.
- Original 05.03 work: `b142884d6e26f1fa6c823df7c7c03f5a932894e1`.
- Live 05.02 log commit: `a3a0f83a629912bb150dcbf397d1f9ac41a61f54`. Same 0701 log blob as origin/returns.
- Live 05.02 work: `018892bab46ea08c5ee2d36f1b6926e2aa6a4b42`. It is an ancestor of origin/returns.
- 05.03 pack start: `a823ee284574be3d9f6247925b9088137a27a539`.
- 05.03 pack hash, in entry 21 and in the return file: `674d965e08dbb013e4ce8e1e05a3e6d70c74c6a11b80ff4580d8e94b037838dd`.
- 0423.05.01 return that is on returns, later closed failed: `1b0d2c123f7fc8537dcac1e6819f2456a781890f`.
- 0423.05.02 pack hash on the published log, entry 17: `e8e5d3404b3977c26489fce3c30024106142dc6f3d1e81bcee1190887eb8327f`. Start `1fdef9ad49c721a6b9dab5e44a24b1543c1c5dec`. No claim is on that published log. Grok-2 owns the live build.

## Findings

The live 0701 log has not moved since the repair note.

| Log | Where | Lines | Bytes | Git blob |
|---|---|---|---|---|
| Published packs | `origin/packs:pages/90.50.10.0701/log.jsonl` | 22 | 56724 | `4f9d7b7ca587f6dfc3eb0a050bbb24a43929bd12` |
| Live returns | `origin/returns:.workshop/logs/90.50.10.0701/log.jsonl` | 24 | 60426 | `0ec01bbab4c6f480989c3141de94973e43899bc0` |
| Original filing | `b71ab3e0:.workshop/logs/90.50.10.0701/log.jsonl` | 24 | 60426 | `bbddd69ee406f9592bdb12b8169a42b4ae74219c` |

The shared byte prefix is the packs file. Both 24-line logs start with those exact 56724 bytes, which is entries 1 through 22 and the newline after entry 22. Entry 22 is the face write at `2026-11-23T15:29:33Z`. Its line hash, which both later claims use as `prev`, is `03efa4f3f2d81d316537f34b5f09eabe8f8ae67a4a8dad2577024af420b0c831`.

The two 24-line files then share 33 more bytes, `{"actor":"Grok-1","data":{"pass":`, and diverge on the next byte. Live returns has `2`. b71ab3e0 has `3`. Neither file is a prefix of the other.

Entries that must stay, live returns 23 and 24:

- Entry 23: claim, actor Grok-1, pass 2, `2026-11-23T15:47:39Z`, prev `03efa4f3f2d81d316537f34b5f09eabe8f8ae67a4a8dad2577024af420b0c831`.
- Entry 24: return, actor Grok-1, pass 2, `2026-11-23T15:49:46Z`, commit `018892bab46ea08c5ee2d36f1b6926e2aa6a4b42`, file `.workshop/returns/90.50.10.0701.05.02.md`, text hash `c2ae18a4d4823b0777977db6aa82286632dc5099bbd4e6e3fc361d6fea9ef912`.
- The sha256 of that entry 24 line, with no newline, is the live head: `acb1cfb460352374e444ca6ad79dd6b90e531652c6ab315dbb9fe4c61400dc82`. A later append has to chain from whatever the head is on the day of the repair. Today that is this value.

Displaced entries that need replay, b71ab3e0 entries 23 and 24. They are evidence. They are not bytes to paste back:

- Entry 23: claim, actor Grok-1, pass 3, `2026-11-23T15:38:18Z`, same prev as the live claim.
- Entry 24: return, actor Grok-1, pass 3, `2026-11-23T15:41:39Z`, commit `b142884d6e26f1fa6c823df7c7c03f5a932894e1`, file `.workshop/returns/90.50.10.0701.05.03.md`, text hash `895dfabb56d27acb39b1e8a55f47e53253e32ff57a55cf82cbb7f50f59851df9`.
- The sha256 of that original entry 24 line is `a6aab8b50210eca3de779e01fc300af89bba53a3cfc73f7817acc6aa82539300`. The replay must not reuse it as `prev`.

`tests/lab_0415.rs` and `.workshop/returns/90.50.10.0701.05.03.md` are on origin/returns and are the same bytes as in b142884d.

- `tests/lab_0415.rs`: 2402 bytes, sha256 `08a8d84fa5c3c07c512a7868eb1cb668fd94a755d9f11296d162d3acdc5681b3`.
- Return file: 2443 bytes, sha256 `84059c61b31b41eacb35e3ffb3063cf5c52486ae8c5f0fbead9792c63305c61a`.

Ancestry, checked with `git merge-base --is-ancestor`:

- `a823ee284574be3d9f6247925b9088137a27a539` is an ancestor of `b142884d6e26f1fa6c823df7c7c03f5a932894e1`. Exit 0.
- `b142884d6e26f1fa6c823df7c7c03f5a932894e1` is an ancestor of origin/returns. Exit 0.
- `b142884d6e26f1fa6c823df7c7c03f5a932894e1` is not an ancestor of `a823ee28`. Exit 1.

The repair note's step 4 says b142884d is an ancestor of origin/returns and of the 05.03 pack start. The first comparison is true. The second is reversed. The pack start is the ancestor of the work commit.

One other correction. The note says the replay is new entries 25 and 26, a claim and a return. That was written before lockout. On origin/returns, `claim` and `return` call `lock_block` for face 05 (`src/cmd.rs` at the tip). A claim with no lockout is refused with `refused: lockout first`. The replay therefore writes a lockout before the claim. The sequence numbers will be whatever follows the live head that day, not a promise that claim is 25.

The local run folder at `D:\Git\grok1\wf-run\pages\90.50.10.0701\log.jsonl` is still the 22-line packs prefix. It also has dirty page files for 0407 and 0416. The later repair does not use that folder.

0423 on packs and on returns is the same 17-line log. 05.01 is closed failed (entries 11 and 12, `2026-11-24T18:50:30Z`). 05.02 is packed and unclaimed on that published log. The returns tip already contains the failed 05.01 lockout code. The replay waits until 05.02 is closed passed, because that pass is the one that keeps replay and book-Prime succession lawful.

## Blockers

- Do not run the replay with `D:\Git\grok1\wf-bin\bin\wf.exe`. That binary is a823ee28. Its `push_log` copies the local log and, on a lost push, runs `git pull --no-rebase`. That is the overwrite this repair exists to avoid.
- Do not start while 0423.05.02 is only packed, open, returned, or closed failed. Grok-2 owns that build. This report does not claim it.
- Do not paste b71ab3e0's JSON into the live log. Do not edit entries 23 and 24. Do not force-push. Do not hand-edit `log.jsonl` or a view. Do not `wf verify --fix`.
- Do not edit the 05.03 return file so that its `noticed:` line can name b71ab3e0. That file is inside b142884d. A changed file is a different commit, and the replay would no longer be the original work.
- `wf release` appends locally and does not push. `wf return --push` publishes the log through the return, and return does not release the lock. After a successful push, Grok-1 would still hold face 05, and a checker would be refused. There is no wf command on the returns tip that publishes a later release without another return. Stop after the pushed return and raise that gap. Do not publish-pack a run-folder log that has a release returns does not have.
- `wf intake` has no page filter. Use it only in a clean throwaway run folder. Do not publish-pack any page from that folder except 0701, and do not publish-pack 0701 until the replay is on returns.

## Later recovery

Prepare only. Do not run these commands in this turn.

Build wf from the commit 0423.05.02 closed on. Set `WF_AS=Grok-1` and `WF_ROOT` to a clean clone of packs, with `work` fetched at origin/returns. Confirm `wf` help lists `lockout`, `try-out`, and `release`, and that `push_log` refuses a non-prefix with the sentence below. If the closed 05.02 changed that sentence, use the closed sentence and stop if the refusal no longer means "published bytes must be a prefix of the local log".

Stop if any check below fails. Quote the command and the full error. Do not retry a wf failure more than once. Do not splice JSON.

1. Fetch. Record the published blob.

```
git fetch origin returns
git rev-parse origin/returns:.workshop/logs/90.50.10.0701/log.jsonl
git merge-base --is-ancestor a823ee284574be3d9f6247925b9088137a27a539 b142884d6e26f1fa6c823df7c7c03f5a932894e1
git merge-base --is-ancestor b142884d6e26f1fa6c823df7c7c03f5a932894e1 origin/returns
```

Stop if the blob is not `0ec01bbab4c6f480989c3141de94973e43899bc0`, unless a later lawful prefix-extension is already published. If it moved, stop and read the new head before any append. Stop if either ancestry check exits 1. Stop if `tests/lab_0415.rs` or the 05.03 return file on origin/returns differs from b142884d.

2. In the clean run folder, intake. The packs 22-line log is a prefix of the live 24-line log, so intake can take those two 05.02 entries. Confirm the local log is then byte-identical to the published blob, that entries 23 and 24 are the 05.02 claim and return, and that 05.03 is at pack with no claim. Stop if intake refuses 0701. Stop if 05.02's tail is `open` (claimed and not returned): a second claim is refused while that tail is open. Today 05.02 is at return, so that particular refusal does not apply. Do not withdraw 05.02.

3. Save the published bytes to a file outside the repo, `published.bin`. Also save `git show b71ab3e0:.workshop/logs/90.50.10.0701/log.jsonl` as evidence outside the repo. Do not copy either file onto a page log.

4. Lock face 05, then read it back. The reason is the citation. It is a new event. It does not pretend to be the old one.

```
wf lockout 90.50.10.0701 05 --reason "replay 05.03 filing b71ab3e0" --as Grok-1
wf try-out 90.50.10.0701 --as Grok-1
```

`Page::add` appends one lockout after the live head. Its `prev` is the sha256 of the current last line. Its time is the new event time, not `2026-11-23T15:38:18Z`. Try-out must print `lock holds on face 05`, `worker: Grok-1`, the reason above, and `other workers are refused`. Try-out must not change the log. Stop if try-out says anyone else holds the page.

5. Claim. This appends one claim for pass 3. Its `prev` is the sha256 of the new lockout line. Its time is new. Stop if wf refuses. Do not return yet.

```
wf claim 90.50.10.0701 03 --as Grok-1
```

6. Before the return, compare bytes. Fetch again. The local log must start with `published.bin`, and `published.bin` must still equal `git show origin/returns:.workshop/logs/90.50.10.0701/log.jsonl`. The suffix so far must be only the new lockout and the new pass-3 claim. The claim's data is `{"pass":3}`. No line from b71ab3e0's entry 23 or 24 is present. Stop if the published file gained a suffix the local log lacks, or if the two files diverge in the old 24 lines.

7. One return, with the push. Do not file a return without `--push` and then return again. A second return is refused. Do not `git push` the log by hand.

```
wf return 90.50.10.0701 03 --branch returns --commit b142884d6e26f1fa6c823df7c7c03f5a932894e1 --file .workshop/returns/90.50.10.0701.05.03.md --as Grok-1 --push
```

`return` checks that b142884d is on `returns` and that a823ee28 is an ancestor of b142884d, reads the return file from that commit, and appends a return whose `commit` is b142884d and whose text hash is `895dfabb56d27acb39b1e8a55f47e53253e32ff57a55cf82cbb7f50f59851df9`. The line is new. Its time is new. Its `prev` is the sha256 of the new claim line. The same command then checks the published log is a byte prefix of the local log, commits that log by path, and pushes. Stop if wf refuses. A refusal that wf recorded is a `return-refused` line. Do not delete it and do not continue. After a successful push, fetch and confirm the published blob now starts with the old `published.bin` and ends with the lockout, the pass-3 claim, and the pass-3 return.

On the returns tip, a divergent push returns:

```
refused: the published log is not a prefix of this page's log. Intake the published log and return again so new events append.
```

A lost race fetches again and checks the prefix again. It does not pull-merge the log. It does not force-push.

8. Stop while the lockout is still held. Tell Prima the return is published and the release has no push of its own. Do not `wf release` until that push exists. Do not publish-pack 0701 until returns and the run folder name the same log, and a checker has been able to run.

The citation of the original filing is the lockout reason `replay 05.03 filing b71ab3e0`, plus this report. The new claim and return do not carry the old timestamps or the old line hashes.

## Draft scenarios for tests/lab_0423.rs

Implementation waits for the later trial pack, after 0423.05.02 is closed. These are outside trials through the wf binary, in the lab harness, on temporary pages. They do not touch page 90.50.10.0423 or page 90.50.10.0701. They do not init the real book page 90.50.10.0000.

### One writer, named face

Worker A runs `wf lockout <page> 05 --reason trial --as A`. The log gains one lockout naming A, face 05, the reason, and the event time. The command prints `locked face 05. Next: wf try-out <page> before work.` A second lockout by A or by B, on 01, 04, or 05, is refused and writes nothing. The message is `refused: face 05 is locked by A`. A lockout of face 02 is refused with `refused: face '02' cannot be locked; lockout is 01, 04 or 05`. While A holds face 05, A may write face 02, 06, or 08. B may not.

### Reads during the lock

While A holds face 05, `wf try-out`, `wf status`, `wf board`, `wf verify` without `--fix`, and `wf observe` without `--record` write no log line. A's try-out prints `lock holds on face 05`, the worker, the reason, the start time, and `other workers are refused`. B's try-out prints `you would be refused` and `face 05 is locked by A`. B's claim, return, check, draft, pack, and face-write are refused and write nothing. The holder sees `refused: lockout first` only when no lock holds. A non-holder sees `refused: face 05 is locked by A`.

### Work on a different page

A holds page P, face 05. Worker B runs lockout, try-out, and claim on page Q. Those succeed. Q's log has B's lockout. P's log does not. A's hold on P is unchanged. B's claim of P is still refused.

### Builder release and checker handoff

A locks face 05, tries out, claims, and returns. The return succeeds. Try-out still says A holds face 05. Checker C's check is refused while that lock holds, and the message names face 05 and A. A cannot check A's own return. A runs `wf release <page> --as A`. The log gains a release naming face 05 and the lockout entry. Try-out then prints `no lockout holds`. C locks face 05 and the check is accepted when the check command passes. A second checker cannot lock out or check while C holds. A release by B, while A holds, is refused with `refused: face 05 is locked by A`.

### Divergent push

Build a published log and a local log that share a prefix and then differ, the 0701 shape. `wf return --push` refuses with `refused: the published log is not a prefix of this page's log. Intake the published log and return again so new events append.` The published bytes are unchanged. The command does not force-push and does not merge the log. A local log that starts with the published bytes and adds lines is accepted, and the published file becomes that extension. A lost push fetches again and repeats the same byte check.

### Replay after book-Prime succession

On a fixture book page inside the test directory, record a valid override by the book Prime of that moment, with a reason, the holder, the face, and the lockout it closes. Change the book Prime. The old page still loads. `wf verify` prints that the log chain holds and does not change a log byte. A new override by the former Prime is refused. A new override by the current book Prime, with a reason, is accepted and kept. A work-page Prime who is not the book Prime is refused. When the fixture book has no Prime, only the person is accepted, and the message says the book Prime is missing. An override recorded in the older shape still loads. A new release without the live authority check is refused.

## Elapsed

Machine clock is Central. Fetch began 2026-11-24 13:06:25. The report was written at 2026-11-24 13:15.
