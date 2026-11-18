//! wf: the Workshop workflow tool. One page per piece of work.
//! The log (pages/<page>/log.jsonl) is the only truth; every other page file is a view
//! printed from it. People and models never edit page files; they run wf.

fn main() {
    let raw: Vec<String> = std::env::args().skip(1).collect();
    if let Err(e) = wf::run(&raw) {
        eprintln!("wf: {e}");
        std::process::exit(1);
    }
}
