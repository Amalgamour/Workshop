//! Lossless round trip (R3): book -> .seq -> book, for every page of every book.
mod common;
use common::*;
use seqaddr_core::log::BookLog;
use seqpage::write::check_entry_r4;
use seqpage::{check_text, export, file_name, page_entries, pages_in, parse, render};

fn round_trip_dir(dir: &str) -> (usize, usize) {
    let mut ok = 0;
    let mut r4 = 0;
    for (path, _text, log) in books_in(dir) {
        for page in pages_in(&log) {
            let entries = page_entries(&log, page);
            match export(&log, page) {
                Err(e) => {
                    // The only allowed refusal: a book entry that breaks R4 (plain ASCII).
                    assert_eq!(e.rule, "R4", "{path} {page}: {e}");
                    assert!(entries.iter().any(|x| check_entry_r4(x).is_err()));
                    r4 += 1;
                }
                Ok(text) => {
                    assert!(text.bytes().all(|b| b == b'\n' || (0x20..=0x7e).contains(&b)), "{page}: export is not plain ASCII");
                    let sp = parse(&text).unwrap_or_else(|e| panic!("{path} {page}: {e}\n{text}"));
                    assert_eq!(sp.page, page);
                    assert_eq!(sp.booked(), entries, "{path} {page}: entries changed in the round trip");
                    assert!(sp.proposed().is_empty());
                    assert_eq!(render(page, &sp.booked(), &[]), text, "{path} {page}: text is not canonical");
                    let title = seqpage::write::derived_title(page, &entries);
                    let name = file_name(page, title.as_deref());
                    let rep = check_text(&text, Some(&name), Some(&log));
                    assert!(rep.ok, "{path} {page}: {:?}", rep.errors);
                    ok += 1;
                }
            }
        }
    }
    (ok, r4)
}

#[test]
fn every_page_in_repo_books_round_trips_or_is_refused_under_r4() {
    let (ok, r4) = round_trip_dir("books");
    eprintln!("repo books: {ok} pages round-tripped, {r4} refused under R4");
    assert!(ok > 0);
}

#[test]
fn every_page_in_example_sources_round_trips() {
    let (ok, r4) = round_trip_dir("docs/spec/examples/sources");
    assert_eq!(r4, 0, "example sources are R4-clean");
    assert!(ok >= 10, "{ok}");
}

/// Reassemble the whole book from its pages' .seq files plus book-level entries.
fn reassemble(log: &BookLog) -> BookLog {
    let mut entries = Vec::new();
    for page in pages_in(log) {
        let text = export(log, page).unwrap();
        entries.extend(parse(&text).unwrap().booked());
    }
    for e in &log.entries {
        if seqpage::slot_of(&e.addr).is_none() {
            entries.push(e.clone());
        }
    }
    entries.sort_by_key(|e| e.n);
    BookLog { header: log.header.clone(), entries, dropped_partial: false, valid_len: 0 }
}

#[test]
fn whole_book_reassembles_byte_for_byte() {
    for dir in ["books", "docs/spec/examples/sources"] {
        for (path, text, log) in books_in(dir) {
            if log.entries.iter().any(|e| check_entry_r4(e).is_err()) {
                continue; // refused under R4; covered above
            }
            let back = reassemble(&log);
            assert_eq!(back.entries, log.entries, "{path}");
            assert_eq!(back.to_text(), log.to_text(), "{path}");
            if log.to_text() == text {
                assert_eq!(back.to_text(), text, "{path}: bytes");
            }
        }
    }
}

/// A later export only adds lines; only derived `:=` lines may change in place.
#[test]
fn later_exports_only_add_lines() {
    for dir in ["books", "docs/spec/examples/sources"] {
        for (path, _t, log) in books_in(dir) {
            for page in pages_in(&log) {
                let all = page_entries(&log, page);
                if all.iter().any(|e| check_entry_r4(e).is_err()) {
                    continue;
                }
                let mut prev: Option<Vec<String>> = None;
                for k in 1..=all.len() {
                    let text = render(page, &all[..k], &[]);
                    let lines: Vec<String> = text.lines().filter(|l| !l.contains(" := ")).map(String::from).collect();
                    if let Some(p) = &prev {
                        let mut it = lines.iter();
                        for l in p {
                            assert!(it.any(|x| x == l), "{path} {page}: line `{l}` was removed or moved after entry {k}");
                        }
                    }
                    prev = Some(lines);
                }
            }
        }
    }
}
