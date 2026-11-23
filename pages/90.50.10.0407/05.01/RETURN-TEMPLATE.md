# Return 90.50.10.0407.05.01
pack: 7ac8e94417e60349fb1c5d2cda794ab6aa5f4db8d07ea71a26dd52109787f387
done: <what you did, in plain words>
changed: <your summary of creates, modifies and deletes; the tool takes the list from git>
noticed: <what you noticed, or none>
w01: <done | need | blocked> - In src/render.rs face00 (line 355 at a823ee28), when this page is a band head (page_kind BandHead, src/addr.rs:73), print a line type: band and a contents list. Build the list by reading the other page folders of the same band under the run folder's pages directory. Do not hand-write the list. Each line names the page address and the state that page's log already has. A page that is not a band head gets no type: band line and no contents list.
w02: <done | need | blocked> - Add tests/page_0407.rs. It must build on Windows: no std::os::unix, and no check command that is only true, grep, or test (stage plan 11.7). Show a band door listing each page in its band with its state, and a non-door page with no list. Do not add a dropped state. If a test cannot show dropped from the log as it is, stop and say so.
proof: <commits, tests run and what they showed>
design review: <the design files you compared your work against (at least docs/AXIOMS.md and docs/DESIGN.md in the kit), what matched, and any place it differs; t416u>
not done: <what you did not do, and why, or none>
unprompted: <anything you did that was not asked, or none>
overflow: <ideas past this job, or none>
