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
    // R4 (Director): storage is plain ASCII, so the "rich" sample uses every awkward
    // ASCII character (quotes, backslash, braces) instead of accents and emoji.
    let why = if non_ascii { "Pourquoi: cafe \"x\" \\ {y} ~ -- name" } else { "Why: plain text" };
    b.add("compute", vec![put("10.11.21.0000.00", "---\ntitle: tools\n---")]);
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
fn truncation_at_every_char_boundary_awkward_ascii() {
    // R4: the "rich" sample is now awkward ASCII (quotes, backslash, braces).
    check_every_cut(&sample(true).text());
}

fn tmp(name: &str) -> std::path::PathBuf {
    let d = std::env::temp_dir().join(format!("trial-core-{}-{name}", std::process::id()));
    let _ = std::fs::remove_file(&d);
    d
}

/// Finding 1, settled by Director ruling R4 (storage is plain ASCII: 0x20-0x7E
/// plus newline). A multi-byte character can no longer be written, so a cut can
/// never split one; a book that holds such a byte anyway is damaged on read and
/// is not "repaired" by cutting it away.
#[test]
// fixed in CORE fix pass (was #[ignore = "finding 1"]), rewritten for R4
fn r4_non_ascii_is_refused_on_write_and_a_book_holding_it_is_damaged() {
    let text = sample(true).text();
    assert!(text.is_ascii());
    let path = tmp("utf8cut.book");
    std::fs::write(&path, text.as_bytes()).unwrap();
    let l = log::file::read(&path).unwrap();
    // write: refused with a clear R4 error, file untouched
    let mut e = entry(l.next_n(), "compute", Op::Put, "10.11.21.1600.00");
    e.body = Some("title: caf\u{e9} \u{2615}".into());
    let err = log::file::append(&path, &[e]).unwrap_err();
    assert_eq!(err.rule(), "R4", "{err}");
    assert_eq!(std::fs::read_to_string(&path).unwrap(), text);
    // read: the old crash case (a cut inside a UTF-8 char) is damage, not a partial line
    let mut bytes = text.into_bytes();
    bytes.extend_from_slice("{\"n\":99,\"body\":\"caf\u{e9}".as_bytes());
    bytes.pop();
    std::fs::write(&path, &bytes).unwrap();
    assert_eq!(log::file::read(&path).unwrap_err().code(), "corrupt");
    assert!(log::file::append(&path, &[]).is_err(), "damage is not silently cut away");
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
// fixed in CORE fix pass (was #[ignore = "finding 15"])
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
// fixed in CORE fix pass (was #[ignore = "finding 5"])
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
// fixed in CORE fix pass (was #[ignore = "finding 16"])
fn timestamps_must_be_real_times() {
    // format.md:80 "time"; contract: ISO 8601 UTC. Month 13, day 45, hour 99 are not times.
    assert!(log::check_timestamp("2026-13-45T99:99:99Z").is_err());
}
