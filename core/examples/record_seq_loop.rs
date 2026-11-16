//! Record the show pass, the import pass, and what the next pass is waiting on.

use std::env;
use std::path::Path;

use seqbook::{Error, Writer};

const AT: &str = "2026-11-11T21:12:00Z";
const BY: &str = "cursor";

fn main() {
    let path = env::args().nth(1).expect("book");
    let mut writer = Writer::open(Path::new(&path)).expect("open");
    for (addr, body) in NOTES {
        match writer.put(AT, BY, addr, body, None) {
            Ok(()) | Err(Error::Exists { .. }) => {}
            Err(err) => {
                eprintln!("{addr}: {err}");
                std::process::exit(1);
            }
        }
    }
    println!("len {}", writer.book().len());
}

const NOTES: &[(&str, &str)] = &[
    (
        "10.10.10.0405.06.08",
        "## seq-show-check\ntype: note\naxioms: 9.5\nby: cursor\nrefs: 10.10.10.0405.06.07\nwhy: The view has to be seen on the page, not only printed by a command.\n\nCheck: the app at 127.0.0.1:3210, dev band, page 0405. The large pane showed seqpage 1, face 00 first, and title := usable. Title:(usable) stayed above the address. Face .04 still opened the why. The compute served the view and did not write the book. cargo test -p compute a_seq_view_is_served_and_the_book_is_not_written passed.\n\nCloser: yes, to reading the page file in the app.\nNot closer: the pane is a view made at read time. It is not yet a file the person edits and sends back.\n",
    ),
    (
        "10.10.10.0405.06.09",
        "## seq-import\ntype: note\naxioms: 6.1\nby: cursor\nrefs: 10.10.10.0405.06.08, SEQ-GUIDE.md\nwhy: Export without a way back in is only a printout.\n\nMVP: a new block becomes a request. The request does not write the book. The compute then accepts or refuses that one request. A new block placed in front of the past is refused. A request that would stand a new page in one face is refused, and the file stays unchanged.\n",
    ),
    (
        "10.10.10.0405.06.10",
        "## seq-import-check\ntype: note\naxioms: 9.6\nby: cursor\nrefs: 10.10.10.0405.06.09\nwhy: The request is only real if the book stays still until the compute decides.\n\nCheck: cargo test -p seqpage, 5 passed. A file with no new block proposes nothing. A new note after the history mark became one request and the book bytes stayed the same until propose_put. A new block placed before the booked blocks was flagged. cargo test -p compute --test import_book passed: a one-face new page was refused and the file was unchanged, then a note on the existing page was accepted and the line was in the file.\n\nCloser: yes, to sending a page view back as a request the compute can decide.\nNot closer: one request is one face. A new page still cannot be born in one request, because the stamp and its first content face are two writes. The guide's all-or-nothing proposal is not built, and the spec files are still absent, so that batch is not the next invention.\n\nNext pass waits on the spec, or on a person saying a new page may be proposed as several faces that book together or not at all.\n",
    ),
];
