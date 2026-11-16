//! Pass 1 record: the compute reads and refuses, and two packs return.

use std::env;
use std::path::Path;

use seqbook::{Error, Writer};

const AT: &str = "2026-11-11T20:40:00Z";
const BY: &str = "cursor";

fn main() {
    let path = env::args().nth(1).expect("book");
    let mut writer = Writer::open(Path::new(&path)).expect("open");
    for (addr, body) in NOTES {
        put(&mut writer, addr, body);
    }
    for addr in ["10.10.10.0503.05.02", "10.10.10.0504.05.02"] {
        for (from, to) in [("draft", "pack"), ("pack", "open"), ("open", "return")] {
            writer.tail(AT, BY, addr, from, to).expect(addr);
        }
    }
    println!("len {}", writer.book().len());
}

fn put(writer: &mut Writer, addr: &str, body: &str) {
    match writer.put(AT, BY, addr, body, None) {
        Ok(()) | Err(Error::Exists { .. }) => {}
        Err(err) => {
            eprintln!("{addr}: {err}");
            std::process::exit(1);
        }
    }
}

const NOTES: &[(&str, &str)] = &[
    (
        "10.10.10.0405.06.02",
        "## pass-1\ntype: note\naxioms: 5.1\nby: cursor\nrefs: 10.10.10.0503.05.02, 10.10.10.0504.05.02\nwhy: The pass needs a goal written down before the result can be compared with it.\n\nMVP for this pass: one compute command reads a face and refuses a bad write. A refusal does not change the book. An accepted pair of cards does.\n",
        ),
    (
        "10.10.10.0405.06.03",
        "## pass-1-check\ntype: note\naxioms: 9.5\nby: cursor\nrefs: 10.10.10.0405.06.02\nwhy: A pass that feels closer has to say closer to what.\n\nCheck: cargo test -p compute, 5 passed. A missing why is refused and the file bytes stay the same. A page of only face 07 is refused. A 04 why followed by its 01 card is accepted and the book grows. A read does not grow the book.\n\nCloser: yes, to seeing the compute decide. The command prints decision: refuse or decision: accept.\nNot closer: the app is not open, and no model has proposed anything. HTTP against MCP is still open. Where a live model runs is still open. This pass used a command, not a server, so a browser cannot see it yet.\n\nNo new pack. 0502.05.02 and 0505.05.01 were already the next drafts. 0503.05.02 and 0504.05.02 moved to return.\n",
        ),
    (
        "10.10.10.0503.06.03",
        "## ran\ntype: note\naxioms: 5.6\nby: cursor\nrefs: 10.10.10.0503.05.02\nwhy: The refusal has to be on the pack that asked for it.\n\n## w01\nresult: done\ncommand: cargo test -p compute a_missing_why_is_refused_and_the_file_is_unchanged\nevidence: the test passed. The book bytes were unchanged. The reason names the card and face 04.\n\n## notes\nThe compute is compute/. Why: format.md keeps it separate from the core.\n\n## unprompted\nnone. Why: the ask was the refusal, and the refusal is what ran.\n\n## overflow\nHTTP and the model host are still open. Why: this pack did not choose them.\n",
        ),
    (
        "10.10.10.0504.06.03",
        "## ran\ntype: note\naxioms: 5.6\nby: cursor\nrefs: 10.10.10.0504.05.02\nwhy: The shape refusal has to be on the pack that asked for it.\n\n## w01\nresult: done\ncommand: cargo test -p compute a_face_07_page_is_refused the_command_prints_a_refusal\nevidence: both passed. decision: refuse is printed. The file is unchanged.\n\n## notes\nnone. Why: the ask was one refusal, and it happened.\n\n## unprompted\nnone. Why: face 07 was the case the pack named.\n\n## overflow\nThe same command also refuses a missing face 00 when that is the only gap. Why: the page check already reports it, and this pack's ask was face 07.\n",
        ),
];
