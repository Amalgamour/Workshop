//! Replays the repository's real book files (written by other lanes), if any.
use seqaddr_core::{BookLog, BookState, Policy};

#[test]
fn format_3_1_repo_books_replay_cleanly() {
    let dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../../books");
    let Ok(rd) = std::fs::read_dir(&dir) else { return };
    for ent in rd.flatten() {
        let p = ent.path();
        if p.extension().and_then(|x| x.to_str()) != Some("book") {
            continue;
        }
        let text = std::fs::read_to_string(&p).unwrap();
        let log = BookLog::parse(&text).unwrap_or_else(|e| panic!("{}: {e}", p.display()));
        BookState::replay(&log, &Policy::default()).unwrap_or_else(|e| panic!("{}: {e}", p.display()));
    }
}
