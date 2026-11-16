//! Pass 2 record: the app showed one face, and the next model pack stays draft.

use std::env;
use std::path::Path;

use seqbook::{Error, Tail, Writer};

const AT: &str = "2026-11-11T21:05:00Z";
const BY: &str = "cursor";

fn main() {
    let path = env::args().nth(1).expect("book");
    let mut writer = Writer::open(Path::new(&path)).expect("open");
    for (addr, body, tail) in NOTES {
        put(&mut writer, addr, body, *tail);
    }
    for (from, to) in [("draft", "pack"), ("pack", "open"), ("open", "return")] {
        writer
            .tail(AT, BY, "10.10.10.0502.05.02", from, to)
            .expect("0502.05.02");
    }
    println!("len {}", writer.book().len());
}

fn put(writer: &mut Writer, addr: &str, body: &str, tail: Option<Tail>) {
    match writer.put(AT, BY, addr, body, tail) {
        Ok(()) | Err(Error::Exists { .. }) => {}
        Err(err) => {
            eprintln!("{addr}: {err}");
            std::process::exit(1);
        }
    }
}

const NOTES: &[(&str, &str, Option<Tail>)] = &[
    (
        "10.10.10.0405.06.04",
        "## pass-2-check\ntype: note\naxioms: 9.5\nby: cursor\nrefs: 10.10.10.0502.05.02\nwhy: The face is only closer when a person can read it on the page.\n\nMVP for this pass: open the app, ask for 10.11.21.1001.04, and read the why. The page calls the compute. It does not open the book file.\n\nCheck: the page at 127.0.0.1:3210 showed the timer why, including the line that the first fixture has to show a why in the file itself. Asking for 10.11.21.1001.09 showed decision: refuse and the missing address. cargo test -p compute passed, 7 tests. A face request does not change the file.\n\nCloser: yes, to using the app and seeing the compute answer.\nNot closer: no sentence has been proposed, and no live model was called. No model API key is set in the environment. Local HTTP is still a trial so the browser can see the compute. MCP is still open.\n\n0502.05.02 moved to return. 0505.05.02 is drafted and stays draft until a model host is named.\n",
        None,
    ),
    (
        "10.10.10.0502.06.03",
        "## ran\ntype: note\naxioms: 5.6\nby: cursor\nrefs: 10.10.10.0502.05.02\nwhy: The face on the screen has to be on the pack that asked for it.\n\n## w01\nresult: done\nask: Open the app, ask for 10.11.21.1001.04, and read the why on the screen.\nevidence: The page showed decision: read and the timer why. The compute was serve on port 7040 against core/fixtures/10.11.21.book. The app fetched /face and did not read the file.\n\n## notes\nA missing face, 10.11.21.1001.09, showed decision: refuse. Why: the same page should show a no as well as a yes.\n\n## unprompted\nnone. Why: the ask was one face, and that face is what was read.\n\n## overflow\nThe model host and HTTP or MCP are still open. Why: this pack did not choose them.\n",
        None,
    ),
    (
        "10.10.10.0505.05.02",
        "by: cursor\nauthorized: person-2026-11-11-aim\nlead: M\naxioms: 1.5\noutcome: A named model proposes one write, the compute still accepts or refuses it, and the screen says which model proposed it.\noverview: The next pass after the local proposer. Pass 3 may show a local proposer. This pack does not run until a person names the host.\nstop if: No model host has been named. Or the work would let the model append to the book itself.\ngrant: The proposer behind the existing app and the one compute. Do not add a second writer. Do not edit decisions.md.\nframe: usable\nrisk: 3\npredecessor: 10.10.10.0505.05.01\n\n## w01\ntype: work\ntitle: Propose with a named model\naxioms: 1\nreason: A local proposer shows the shape of the decision. It is not a model the person is talking with.\npath: compute/\nask: Name the model host. Type one sentence. The screen must say which model proposed the write, then show the compute's accept or refusal. The model must not append the book itself.\n",
        Some(Tail::Draft),
    ),
];
