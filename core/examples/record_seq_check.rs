//! Pass result for the .seq export, and the design of the next pass.

use std::env;
use std::path::Path;

use seqbook::{Error, Writer};

const AT: &str = "2026-11-11T21:00:00Z";
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
        "10.10.10.0405.06.06",
        "## seq-view-check\ntype: note\naxioms: 9.6\nby: cursor\nrefs: 10.10.10.0405.06.05\nwhy: A pass that is not checked against its own goal is only a claim.\n\nCheck: cargo test -p seqpage, 4 passed. Export of 10.10.10.0405 starts with seqpage 1, puts face 00 first, and says title := usable. The tool wrote the file and seqpage check returned ok. The book hash was unchanged. A booked line that was edited was refused. A file name whose title was cats, against a stamp of timer, was reported and not rewritten.\n\nA copy saved with a carriage return was refused. The guide allows a plain newline only. The tool's --out writes that newline.\n\nCloser: yes, to a page file a person can read and check against the book.\nNot closer: there is no import queue, the spec files named by the guide are still absent, and this export is not a draft address or a face 00 registry card.\n",
    ),
    (
        "10.10.10.0405.06.07",
        "## seq-show\ntype: note\naxioms: 5.4\nby: cursor\nrefs: 10.10.10.0405.06.06\nwhy: The export is only a file type a person can use if the page can show it.\n\nMVP for the next pass: open a page in the app and read its .seq view in the large pane. The compute makes the view. It does not write the book. A face in the menu still opens that face.\n",
    ),
];
