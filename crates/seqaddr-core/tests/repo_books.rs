//! Replays the repository's real book files (written by other lanes), if any.
//! Director ruling R4: a book holding a non-ASCII byte is reported as damaged;
//! this test accepts that report (printed) but nothing else.
use seqaddr_core::{BookLog, BookState, Policy};

#[test]
fn format_3_1_repo_books_replay_cleanly_or_are_r4_damaged() {
    let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../..");
    for dir in ["books"] {
        let Ok(rd) = std::fs::read_dir(root.join(dir)) else { continue };
        for ent in rd.flatten() {
            let p = ent.path();
            if p.extension().and_then(|x| x.to_str()) != Some("book") {
                continue;
            }
            let bytes = std::fs::read(&p).unwrap();
            let text = String::from_utf8_lossy(&bytes);
            match BookLog::parse(&text) {
                Ok(log) => {
                    BookState::replay(&log, &Policy::default()).unwrap_or_else(|e| panic!("{}: {e}", p.display()));
                }
                Err(e) if e.detail().contains("R4") => eprintln!("R4 damaged (non-ASCII): {}: {e}", p.display()),
                Err(e) => panic!("{}: {e}", p.display()),
            }
        }
    }
}
