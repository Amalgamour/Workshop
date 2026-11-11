//! TRIAL-C (2): the book reader under junk and truncation (format.md:60-67),
//! replay determinism and snapshot equivalence (format.md:61, 88, 104-105).
mod common;
use common::*;
use seqaddr_core::log::{self, Op};
use seqaddr_core::{BookLog, BookState, Policy};

/// A realistic log: door, a page with face 00/04, a multi-op proposal, a pack
/// claimed and returned, a drafting cycle, and non-ASCII text in bodies.
fn sample(non_ascii: bool) -> LogBuilder {
    let mut b = LogBuilder::new("10.11.21");
    let why = if non_ascii { "Pourquoi: café ☕ — 名前" } else { "Why: plain text" };
    b.add("compute", vec![put("10.11.21.0000.00", "---\ntitle: tools\n---"), put("10.11.21.0000.04", &format!("## About\nwhy: {why}\n\nThe book."))]);
    b.add("user", vec![put("10.11.21.1523.00", "title: timer"), put("10.11.21.1523.04", &format!("## Timer\nwhy: {why}\n\nCounts."))]);
    b.add("lead", vec![put_t("10.11.21.1523.05.01", "pack", &format!("## w01\ntype: work\n\n{why}"))]);
    b.add("agent-7", vec![mv("10.11.21.1523.05.01", "pack", "open")]);
    let mut r = mv("10.11.21.1523.05.01", "open", "return");
    r.body = Some(format!("## w01\nresult: done\n\n{why}"));
    b.add("agent-7", vec![r]);
    b.add("user", vec![op(Op::Copy, "10.11.21.1523.04")]);
    let mut n = put("10.11.21.1523.04.draft", &format!("note {why}"));
    n.op = Some(Op::Note);
    b.add("user", vec![n]);
    b
}

#[test]
fn fuzz_random_bytes_never_panic() {
    let mut r = Rng(7);
    let base = sample(true).text();
    for i in 0..30_000 {
        let bytes: Vec<u8> = if i % 2 == 0 {
            (0..r.below(300)).map(|_| r.next() as u8).collect()
        } else {
            // mutate a valid log: flip, drop or insert bytes
            let mut b = base.clone().into_bytes();
            for _ in 0..(1 + r.below(4)) {
                let at = r.below(b.len().max(1));
                match r.below(3) {
                    0 => b[at] = r.next() as u8,
                    1 => {
                        b.remove(at);
                    }
                    _ => b.insert(at, *r.pick(b"{}\":,\n0123456789")),
                }
            }
            b
        };
        let text = String::from_utf8_lossy(&bytes);
        if let Ok(l) = BookLog::parse(&text) {
            let _ = BookState::replay(&l, &Policy::default());
            let _ = l.history("10.11.21.1523");
        }
    }
}

/// format.md:67: "A partly written last line is detected and dropped. Nothing earlier can be damaged."
fn check_every_cut(text: &str) {
    let full = BookLog::parse(text).unwrap();
    let line_ends: Vec<usize> = text.match_indices('\n').map(|(i, _)| i + 1).collect();
    for cut in line_ends[0]..=text.len() {
        if !text.is_char_boundary(cut) {
            continue; // &str cannot hold this cut; the file-level test covers it
        }
        let t = &text[..cut];
        let l = BookLog::parse(t).unwrap_or_else(|e| panic!("cut at {cut}: {e:?}"));
        // complete lines kept = lines whose '\n' is inside the cut, plus a complete unterminated last line
        let complete = line_ends.iter().filter(|&&e| e <= cut).count() - 1; // minus header
        let unterminated_complete = !t.ends_with('\n') && serde_json::from_str::<serde_json::Value>(t.rsplit('\n').next().unwrap()).is_ok();
        let mut want = complete + usize::from(unterminated_complete);
        // a trailing proposal group cut short is dropped whole (format.md:100, BUILD-LOG CORE 7)
        if let Some(last) = full.entries.get(want.wrapping_sub(1)) {
            if let (Some(pid), Some(of)) = (&last.proposal, last.of) {
                let have = full.entries[..want].iter().rev().take_while(|e| e.proposal.as_ref() == Some(pid)).count();
                if have < of as usize {
                    want -= have;
                }
            }
        }
        assert_eq!(l.entries.len(), want, "cut at {cut}");
        assert_eq!(l.entries[..], full.entries[..want], "prefix kept intact at cut {cut}");
        assert!(l.valid_len <= cut);
        // the kept state replays
        BookState::replay(&l, &Policy::default()).unwrap_or_else(|e| panic!("cut {cut}: {e:?}"));
    }
}

#[test]
fn truncation_at_every_byte_ascii() {
    check_every_cut(&sample(false).text());
}

#[test]
fn truncation_at_every_char_boundary_non_ascii() {
    check_every_cut(&sample(true).text());
}

fn tmp(name: &str) -> std::path::PathBuf {
    let d = std::env::temp_dir().join(format!("trial-core-{}-{name}", std::process::id()));
    let _ = std::fs::remove_file(&d);
    d
}

/// The real crash case: the file is cut at a byte, which may fall inside a
/// multi-byte UTF-8 character of a body (serde_json writes non-ASCII raw).
#[test]
#[ignore = "finding 1"]
fn crash_cut_inside_utf8_char_is_dropped_by_file_read_and_append() {
    let text = sample(true).text();
    let bytes = text.as_bytes();
    let last_nl = text[..text.len() - 1].rfind('\n').unwrap() + 1;
    // cut somewhere inside the last line where the cut splits a multi-byte char
    let cut = (last_nl..bytes.len()).find(|&i| !text.is_char_boundary(i)).expect("last line has non-ASCII");
    let path = tmp("utf8cut.book");
    std::fs::write(&path, &bytes[..cut]).unwrap();
    let l = log::file::read(&path).expect("format 3.1: a partly written last line is dropped");
    assert!(l.dropped_partial);
    log::file::append(&path, &[]).expect("append repairs the partial tail");
}

#[test]
fn crash_cut_ascii_is_repaired_by_append() {
    let b = sample(false);
    let text = b.text();
    let path = tmp("asciicut.book");
    std::fs::write(&path, &text.as_bytes()[..text.len() - 7]).unwrap();
    let l = log::file::read(&path).unwrap();
    assert!(l.dropped_partial);
    let mut e = entry(l.next_n(), "compute", Op::Put, "10.11.21.1600.00");
    e.body = Some("title: x".into());
    log::file::append(&path, &[e]).unwrap();
    let l2 = log::file::read(&path).unwrap();
    assert!(!l2.dropped_partial);
    assert_eq!(l2.entries.len(), l.entries.len() + 1);
}

#[test]
#[ignore = "finding 15"]
fn crash_during_create_leaves_a_readable_empty_book() {
    // format.md:67 "A partly written last line is detected and dropped" - also when the only line is the header.
    let path = tmp("cuthdr.book");
    std::fs::write(&path, b"{\"seqbook\":1,\"addr").unwrap();
    assert!(log::file::read(&path).is_ok() || log::file::repair_tail(&path).is_ok());
}

#[test]
fn replay_is_deterministic_and_text_round_trips() {
    let b = sample(true);
    let text = b.text();
    let a = BookState::replay(&BookLog::parse(&text).unwrap(), &Policy::default()).unwrap();
    let a2 = BookState::replay(&BookLog::parse(&text).unwrap(), &Policy::default()).unwrap();
    assert_eq!(a, a2);
    assert_eq!(&a, b.state(), "replay equals the state validate produced");
    assert_eq!(BookLog::parse(&text).unwrap().to_text(), text);
}

#[test]
fn snapshot_equivalence_at_every_point() {
    let b = sample(true);
    let base = b.log.clone();
    for k in 1..=base.entries.len() {
        // replay to k, snapshot, then the rest renumbered after the snapshot
        let mut log = BookLog::new(base.book().unwrap());
        log.entries = base.entries[..k].to_vec();
        let st_k = BookState::replay(&log, &Policy::default()).unwrap();
        let snap = st_k.snapshot_entry(AT, "compute");
        log.entries.push(snap);
        let text = log.to_text();
        let from_snap = BookState::replay(&BookLog::parse(&text).unwrap(), &Policy::default()).unwrap();
        let mut want = st_k.clone();
        want.last_n += 1;
        assert_eq!(from_snap, want, "snapshot after entry {k}");
        assert_eq!(BookState::replay_until(&BookLog::parse(&text).unwrap(), k as u64, &Policy::default()).unwrap(), st_k);
    }
}

#[test]
#[ignore = "finding 5"]
fn forged_snapshot_is_not_trusted_over_the_log() {
    // format.md:88 a snapshot is "the full current state". A snapshot that disagrees
    // with the entries before it must not silently replace them (axiom 6: the past is not rewritten).
    let b = sample(false);
    let mut log = b.log.clone();
    let mut forged = b.state().clone();
    forged.pages.remove(&1523); // erase the page, its pack, its claim and its return
    let snap = forged.snapshot_entry(AT, "compute");
    log.entries.push(snap);
    let text = log.to_text();
    let r = BookState::replay(&BookLog::parse(&text).unwrap(), &Policy::default());
    assert!(r.is_err() || r.unwrap().page(1523).is_some(), "forged snapshot replaced history without complaint");
}

#[test]
#[ignore = "finding 16"]
fn timestamps_must_be_real_times() {
    // format.md:80 "time"; contract: ISO 8601 UTC. Month 13, day 45, hour 99 are not times.
    assert!(log::check_timestamp("2026-13-45T99:99:99Z").is_err());
}
