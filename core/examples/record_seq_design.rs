//! Record the .seq view design before the export is built.

use std::env;
use std::path::Path;

use seqbook::{Error, Writer};

const AT: &str = "2026-11-11T20:55:00Z";
const BY: &str = "cursor";

fn main() {
    let path = env::args().nth(1).expect("book");
    let mut writer = Writer::open(Path::new(&path)).expect("open");
    let body = "\
## seq-view\n\
type: note\n\
axioms: 5.6\n\
by: cursor\n\
refs: SEQ-GUIDE.md\n\
why: The file type has to be decided before a pass builds it, or the pass will invent a second book.\n\
\n\
SEQ-GUIDE.md is the reader's guide. The book stays the real copy. A .seq file is a view of one page. Export makes it. A check compares booked blocks to the book. Import, when it exists, is a request and does not write.\n\
\n\
The guide points at docs/spec/seqpage.md, face00.md, and crates/seqpage. Those files are not in this repo. This pass follows the guide. It does not claim the missing spec.\n\
\n\
MVP: export one page to text that starts with `seqpage 1`, puts face 00 first, quotes each write with its entry number, and ends with `~ end`. Check refuses a booked block that differs from the book. The book file is unchanged.\n\
\n\
Not this pass: an import queue, `.draft` addresses, the face 00 registry card, and treating this export as proof against the missing spec.\n\
";
    match writer.put(AT, BY, "10.10.10.0405.06.05", body, None) {
        Ok(()) | Err(Error::Exists { .. }) => {}
        Err(err) => {
            eprintln!("{err}");
            std::process::exit(1);
        }
    }
    println!("len {}", writer.book().len());
}
