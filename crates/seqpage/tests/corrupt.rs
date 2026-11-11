//! Corrupted input: every rule has a case, each error cites its axiom; then
//! a seeded fuzz pass over the examples (no panics; edited history never imports).
mod common;
use common::*;
use seqaddr_core::log::BookLog;
use seqpage::{check_text, import, parse};

fn bob() -> String {
    read("docs/spec/examples/10.11.21.1001.bob.seq")
}
fn bob_book() -> BookLog {
    BookLog::parse(&read("docs/spec/examples/sources/10.11.21.book")).unwrap()
}
fn timer() -> String {
    read("docs/spec/examples/10.11.30.1501.timer.seq")
}

/// The first error of a check (parse or rule), as (code, axiom, rule).
fn first(text: &str) -> (String, Option<String>, String, String) {
    let r = check_text(text, None, None);
    let e = r.errors.first().unwrap_or_else(|| panic!("expected an error, got ok:\n{text}"));
    (e.code.to_string(), e.axiom.map(String::from), e.rule.to_string(), e.detail.clone())
}

fn assert_err(text: &str, code: &str, axiom: Option<&str>) {
    let (c, a, rule, d) = first(text);
    assert_eq!((c.as_str(), a.as_deref()), (code, axiom), "rule {rule}: {d}");
}

// ---- R4: plain ASCII only ----

#[test]
fn r4_rejects_tab() {
    let t = bob().replace("| type: brand", "| type:\tbrand");
    let (c, _, rule, d) = first(&t);
    assert_eq!((c.as_str(), rule.as_str()), ("invalid", "R4"));
    assert!(d.contains("U+0009") && d.contains("tab"), "{d}");
}

#[test]
fn r4_rejects_carriage_return() {
    let t = bob().replace('\n', "\r\n");
    let (_, _, rule, d) = first(&t);
    assert_eq!(rule, "R4");
    assert!(d.contains("carriage return"));
}

#[test]
fn r4_rejects_em_dash_curly_quotes_accents() {
    for (from, to, name) in [("Bob likes cats", "Bob \u{2014} cats", "em dash"), ("\"My name", "\u{201C}My name", "curly"), ("Bob likes", "B\u{00F6}b likes", "U+00F6")] {
        let t = bob().replace(from, to);
        assert_ne!(t, bob());
        let (_, _, rule, d) = first(&t);
        assert_eq!(rule, "R4", "{name}");
        assert!(d.contains(name), "{d}");
    }
}

#[test]
fn r4_reports_line_and_column() {
    let t = bob().replacen("title := bob", "title := b\u{00E9}b", 1);
    let r = check_text(&t, None, None);
    assert_eq!(r.errors[0].line, 3);
    assert!(r.errors[0].detail.contains("column 11"), "{}", r.errors[0].detail);
}

#[test]
fn r4_rejects_json_escapes_that_smuggle_non_ascii() {
    for v in ["\"caf\\u00e9\"", "\"a\\tb\"", "\"a\\rb\""] {
        let t = bob().replacen("by: prima-kernel-seed", &format!("by: {v}"), 1);
        let (_, _, rule, d) = first(&t);
        assert_eq!(rule, "seqpage 6.3", "{v}: {d}");
        assert!(d.contains("R4"), "{d}");
    }
    let t = bob().replacen("proposal: prima-kernel-seed:10.11.21.1001\n| ---", "proposal: prima-kernel-seed:10.11.21.1001\nx: {\"note\":\"\\u2014\"}\n| ---", 1);
    assert_eq!(first(&t).2, "R4");
}

#[test]
fn r4_export_refuses_non_ascii_book_entry() {
    let mut log = bob_book();
    log.entries[7].body = Some("## bob\n\nBob \u{2013} the user".into());
    let e = seqpage::export(&log, seqpage::PageId::parse("10.11.21.1001").unwrap()).unwrap_err();
    assert_eq!(e.rule, "R4");
    assert!(e.detail.contains("@8") && e.detail.contains("en dash"), "{}", e.detail);
}

#[test]
fn r4_rejects_invalid_utf8_bytes_via_cli_path() {
    // bytes outside ASCII never become a valid page, whatever the encoding
    let t = bob().replacen("bob", "b\u{FFFD}b", 1);
    assert_eq!(first(&t).2, "R4");
}

// ---- structure ----

#[test]
fn empty_and_wrong_magic() {
    assert_err("", "missing", Some("7"));
    assert_err("seqpage 2\n", "invalid", None);
    assert_err("hello\n", "invalid", None);
}

#[test]
fn missing_door_is_axiom_7() {
    let t = bob().replacen("= 00 registry 10.11.21.1001.00", "= 01 law 10.11.21.1001.01", 1);
    assert_err(&t, "missing", Some("7"));
}

#[test]
fn second_door_is_axiom_1() {
    let t = bob().replacen("= 01 law", "= 00 registry 10.11.21.1001.00\n\n= 01 law", 1);
    assert_err(&t, "conflict", Some("1"));
}

#[test]
fn cut_off_file_is_axiom_7() {
    let t = bob();
    let cut = &t[..t.len() / 2];
    let (c, _a, _, _) = first(cut);
    assert!(c == "missing" || c == "invalid", "{c}");
    let no_end = t.replace("~ end\n", "");
    assert_err(&no_end, "missing", Some("7"));
}

#[test]
fn text_after_end() {
    assert_err(&format!("{}junk\n", bob()), "invalid", None);
}

#[test]
fn booked_block_without_author_is_axiom_7() {
    let t = bob().replacen("by: prima-kernel-seed\n", "", 1);
    assert_err(&t, "missing", Some("7"));
}

#[test]
fn proposed_block_cannot_claim_compute_stamps_axiom_1() {
    let t = read("docs/spec/examples/proposals/10.11.21.1001.bob.seq").replacen("--- new put 10.11.21.1001.06.01\n", "--- new put 10.11.21.1001.06.01\nat: 2026-11-11T20:00:00Z\n", 1);
    assert_err(&t, "authority", Some("1"));
}

#[test]
fn block_in_wrong_section_is_axiom_8() {
    let t = bob().replacen("--- @9 put 10.11.21.1001.04.draft", "--- @9 put 10.11.21.1001.01.draft", 1);
    let r = check_text(&t, None, None);
    assert!(r.errors.iter().any(|e| e.code == "connection" && e.axiom == Some("8")), "{:?}", r.errors);
}

#[test]
fn block_from_another_page_is_axiom_8() {
    let t = bob().replace("10.11.21.1001.04", "10.11.21.1002.04");
    let r = check_text(&t, None, None);
    assert!(r.errors.iter().any(|e| e.axiom == Some("8")), "{:?}", r.errors);
}

#[test]
fn edited_derived_line_is_axiom_8() {
    for (a, b) in [("title := bob", "title := alice"), ("cards := bob, cats", "cards := bob"), ("state := draft\nwhy-draft := 7\nsource := book 10.11.21 @8", "state := seated\nwhy-draft := 7\nsource := book 10.11.21 @8")] {
        let t = bob().replacen(a, b, 1);
        assert_ne!(t, bob(), "{a}");
        let r = check_text(&t, None, None);
        assert!(r.errors.iter().any(|e| e.code == "connection" && e.axiom == Some("8")), "{a}: {:?}", r.errors);
    }
}

#[test]
fn reordered_history_is_axiom_6() {
    let t = bob().replace("@7 put 10.11.21.1001.00.draft\n@8 put 10.11.21.1001.01.draft\n", "@8 put 10.11.21.1001.01.draft\n@7 put 10.11.21.1001.00.draft\n");
    let r = check_text(&t, None, None);
    assert!(r.errors.iter().any(|e| e.code == "lineage" && e.axiom == Some("6")), "{:?}", r.errors);
}

#[test]
fn history_without_block_and_block_without_history_are_axiom_7() {
    let t = bob().replace("\n@9 put 10.11.21.1001.04.draft\n", "\n");
    assert!(check_text(&t, None, None).errors.iter().any(|e| e.code == "missing" && e.axiom == Some("7")));
    let t = bob().replace("~ end", "@10 put 10.11.21.1001.04.draft\n~ end");
    assert!(check_text(&t, None, None).errors.iter().any(|e| e.code == "missing" && e.axiom == Some("7")));
}

#[test]
fn duplicate_entry_is_axiom_1() {
    let t = timer();
    let blk = "--- @4 put 10.11.30.1501.04";
    let start = t.find(blk).unwrap();
    let end = start + t[start..].find("\n\n").unwrap();
    let dup = format!("{}\n\n{}", &t[..end], &t[start..]);
    let r = check_text(&dup, None, None);
    assert!(r.errors.iter().any(|e| e.code == "conflict" && e.axiom == Some("1")), "{:?}", r.errors);
}

#[test]
fn new_block_before_booked_is_axiom_6() {
    let t = bob().replacen("--- @9 put", "--- new put 10.11.21.1001.04.draft\n| x\n\n--- @9 put", 1);
    assert!(check_text(&t, None, None).errors.iter().any(|e| e.code == "lineage"));
}

#[test]
fn rewritten_past_is_caught_against_the_book_axiom_6() {
    let t = bob().replacen("Bob likes cats.", "Bob likes dogs.", 1);
    assert!(check_text(&t, None, None).ok, "a body edit is well formed on its own");
    let err = import(&t, Some(&bob_book()), "me").unwrap_err();
    assert!(err.errors.iter().any(|e| e.code == "lineage" && e.axiom == Some("6")), "{:?}", err.errors);
}

#[test]
fn booked_entry_not_in_book_is_axiom_7_8() {
    let t = bob().replace("@9", "@99");
    let err = import(&t, Some(&bob_book()), "me").unwrap_err();
    assert!(err.errors.iter().any(|e| e.axiom == Some("7.8")), "{:?}", err.errors);
}

#[test]
fn wrong_book_is_axiom_8() {
    let other = BookLog::parse(&read("docs/spec/examples/sources/10.11.30.book")).unwrap();
    let err = import(&bob(), Some(&other), "me").unwrap_err();
    assert!(err.errors.iter().any(|e| e.axiom == Some("8")));
}

#[test]
fn stale_file_is_a_finding_not_an_error() {
    let mut log = bob_book();
    let mut e = log.entries.last().unwrap().clone();
    e.n += 1;
    e.op = seqaddr_core::Op::Put;
    e.addr = "10.11.21.1001.06.01".into();
    e.body = Some("## Later\n\nlater note".into());
    log.entries.push(e);
    let imp = import(&bob(), Some(&log), "me").unwrap();
    assert!(imp.findings.iter().any(|f| f.detail.contains("behind")));
}

#[test]
fn file_name_title_mismatch_is_elevated() {
    let r = check_text(&bob(), Some("10.11.21.1001.alice.seq"), None);
    assert_eq!(r.errors[0].code, "elevate");
    let r = check_text(&bob(), Some("10.11.21.1002.bob.seq"), None);
    assert_eq!(r.errors[0].axiom, Some("8"));
    assert!(check_text(&bob(), Some("x/10.11.21.1001.bob.seq"), None).ok);
}

#[test]
fn quoted_values_round_trip() {
    let t = timer();
    assert!(t.contains("to: \"\""));
    let sp = parse(&t).unwrap();
    let e = sp.booked().into_iter().find(|e| e.n == 9).unwrap();
    assert_eq!(e.to.as_deref(), Some(""));
    // a plain value must not be quoted (one canonical form)
    let bad = t.replacen("by: user", "by: \"user\"", 1);
    assert_eq!(first(&bad).2, "seqpage 6.3");
}

#[test]
fn text_codec_is_an_exact_inverse() {
    let mut rng = Rng(7);
    let alphabet: Vec<char> = (0x20u8..=0x7e).map(|b| b as char).chain(['\n', '\n', ' ', '"', '|']).collect();
    for _ in 0..3000 {
        let len = rng.below(24);
        let s: String = (0..len).map(|_| alphabet[rng.below(alphabet.len())]).collect();
        let lines = seqpage::text::body_lines(&s);
        let back: Vec<&str> = lines.iter().map(|l| seqpage::text::body_line(l).unwrap().unwrap()).collect();
        assert_eq!(back.join("\n"), s);
        let v = seqpage::text::encode_value(&s);
        assert!(!v.contains('\n'));
        assert_eq!(seqpage::text::decode_value(&v).unwrap(), s, "{v}");
    }
}

// ---- fuzz ----

fn mutate(rng: &mut Rng, text: &str) -> String {
    let mut lines: Vec<String> = text.split('\n').map(String::from).collect();
    let n = lines.len();
    match rng.below(9) {
        0 => {
            lines.remove(rng.below(n));
        }
        1 => {
            let i = rng.below(n);
            let l = lines[i].clone();
            lines.insert(rng.below(n), l);
        }
        2 => {
            let (a, b) = (rng.below(n), rng.below(n));
            lines.swap(a, b);
        }
        3 => {
            let i = rng.below(n);
            let mut b = lines[i].clone().into_bytes();
            if !b.is_empty() {
                let j = rng.below(b.len());
                b[j] = 0x20 + (rng.below(95) as u8);
                lines[i] = String::from_utf8(b).unwrap();
            }
        }
        4 => {
            let cut = rng.below(text.len());
            return text[..cut].to_string();
        }
        5 => {
            let i = rng.below(n);
            let junk = ["\t", "\r", "\u{2014}", "\u{00E9}", "@", "|", "= ", "--- ", ":= ", "~ end", "\"", "new"];
            lines[i].push_str(junk[rng.below(junk.len())]);
        }
        6 => {
            let i = rng.below(n);
            lines[i] = lines[i].replace("@", "@1");
        }
        7 => {
            let i = rng.below(n);
            if let Some(p) = lines[i].find(' ') {
                lines[i].remove(p);
            }
        }
        _ => {
            let i = rng.below(n);
            lines[i] = lines[i].to_uppercase();
        }
    }
    lines.join("\n")
}

#[test]
fn fuzz_no_panic_and_edited_history_never_imports() {
    let cases = [
        (bob(), bob_book()),
        (timer(), BookLog::parse(&read("docs/spec/examples/sources/10.11.30.book")).unwrap()),
        (read("docs/spec/examples/00.00.00.0051.seqaddr.seq"), BookLog::parse(&read("docs/spec/examples/sources/00.00.00.ruled.book")).unwrap()),
    ];
    let mut rng = Rng(_seed());
    let (mut runs, mut caught, mut harmless) = (0, 0, 0);
    for (text, log) in &cases {
        for _ in 0..1500 {
            let mut t = text.clone();
            for _ in 0..(1 + rng.below(3)) {
                t = mutate(&mut rng, &t);
            }
            runs += 1;
            let _ = check_text(&t, None, None); // must not panic
            match import(&t, Some(log), "fuzz") {
                Err(_) => caught += 1,
                Ok(imp) => {
                    // property: whatever imports, its booked history is exactly the book's
                    for e in &imp.entries {
                        let b = log.entries.iter().find(|x| x.n == e.n).expect("booked entry exists");
                        assert_eq!(b, e, "edited history imported:\n{t}");
                    }
                    assert!(t.bytes().all(|b| b == b'\n' || (0x20..=0x7e).contains(&b)), "non-ASCII imported");
                    harmless += 1;
                }
            }
        }
    }
    eprintln!("fuzz: {runs} mutated files, {caught} refused, {harmless} imported with history intact");
    assert!(caught > runs / 2);
}

const fn _seed() -> u64 {
    0x5e9_9a9e
}

#[test]
fn unknown_and_future_fields_round_trip_losslessly() {
    let mut log = bob_book();
    let e = &mut log.entries[8];
    e.extra.insert("approved_by".into(), serde_json::json!("build-stage (R2)"));
    e.extra.insert("trial".into(), serde_json::json!("docs/trial/core-trial.md"));
    e.extra.insert("Weird Key".into(), serde_json::json!({"a": [1, true, null]}));
    e.extra.insert("count".into(), serde_json::json!("12"));
    e.outcome = Some("true".into());
    let page = seqpage::PageId::parse("10.11.21.1001").unwrap();
    let text = seqpage::export(&log, page).unwrap();
    assert!(text.contains("approved_by: build-stage (R2)"), "{text}");
    assert!(text.contains("count: \"12\""), "a string that looks like a number is quoted");
    assert!(text.contains("outcome: \"true\""));
    assert!(text.contains("x: {\"Weird Key\":{\"a\":[1,true,null]}}"));
    let sp = parse(&text).unwrap();
    assert_eq!(sp.booked(), seqpage::page_entries(&log, page));
    assert_eq!(seqpage::render(page, &sp.booked(), &[]), text);
}

#[test]
fn non_canonical_or_lossy_fields_are_refused() {
    for (a, b) in [("by: prima-kernel-seed", "by: null"), ("by: prima-kernel-seed", "by: 5"), ("by: prima-kernel-seed", "by: \"prima-kernel-seed\""), ("by: prima-kernel-seed", "by: prima-kernel-seed "), ("by: prima-kernel-seed", "x: {\"by\":\"prima-kernel-seed\"}")] {
        let t = bob().replacen(a, b, 1);
        let r = check_text(&t, None, None);
        assert!(!r.ok, "`{b}` should be refused");
    }
    let t = read("docs/spec/examples/proposals/10.11.21.1001.bob.seq").replacen("--- new put 10.11.21.1001.06.01\n", "--- new put 10.11.21.1001.06.01\nbogus: 1\n", 1);
    assert!(!check_text(&t, None, None).ok, "unknown field on a proposed block");
}


// ---- rulings R5, R8, R9, R10 ----

fn timer_book() -> BookLog {
    BookLog::parse(&read("docs/spec/examples/sources/10.11.30.book")).unwrap()
}

#[test]
fn r10_face_00_is_the_registry() {
    let t = bob();
    assert!(t.starts_with("seqpage 1\n= 00 registry 10.11.21.1001.00\n"));
    assert!(t.contains("faces := 01 draft, 04 draft"));
    let old = t.replacen("= 00 registry", "= 00 door", 1);
    let r = check_text(&old, None, None);
    assert!(r.errors.iter().any(|e| e.axiom == Some("8") && e.detail.contains("registry")), "{:?}", r.errors);
}

#[test]
fn r10_door_page_has_only_face_00() {
    let mut log = timer_book();
    let mut e = log.entries[0].clone();
    e.n = log.entries.len() as u64 + 1;
    e.addr = "10.11.30.0000.04".into();
    e.body = Some("## Tools\n\nwhy".into());
    log.entries.push(e);
    let err = seqpage::export(&log, seqpage::PageId::parse("10.11.30.0000").unwrap()).unwrap_err();
    assert_eq!(err.rule, "R10", "{err}");
    let ok = seqpage::export(&timer_book(), seqpage::PageId::parse("10.11.30.0000").unwrap()).unwrap();
    assert!(ok.contains("kind := book door (R10: face 00 only)"));
    let bad = ok.replace("~ history", "= 04 user 10.11.30.0000.04\n\n--- new put 10.11.30.0000.04\n| x\n\n~ history");
    let r = check_text(&bad, None, None);
    assert!(r.errors.iter().any(|e| e.rule == "R10"), "{:?}", r.errors);
}

#[test]
fn r9_no_face_sentinels() {
    for nn in ["00", "99"] {
        let t = read("docs/spec/examples/proposals/10.11.21.1001.bob.seq").replace("06.01", &format!("06.{nn}"));
        let r = check_text(&t, None, None);
        assert!(r.errors.iter().any(|e| e.rule == "R9"), "{nn}: {:?}", r.errors);
    }
    let mut log = timer_book();
    let mut e = log.entries.last().unwrap().clone();
    e.n += 1;
    e.op = seqaddr_core::Op::Put;
    e.addr = "10.11.30.1501.05.00".into();
    e.body = Some("board".into());
    e.extra.clear();
    log.entries.push(e);
    // Either the core no longer reads `05.00` as an address on this page (R9 in the
    // grammar), or seqpage refuses it; it never reaches a .seq file.
    match seqpage::export(&log, seqpage::PageId::parse("10.11.30.1501").unwrap()) {
        Err(e) => assert_eq!(e.rule, "R9"),
        Ok(t) => assert!(!t.contains("05.00"), "FF.00 exported"),
    }
    let page = seqpage::PageId::parse("10.11.30.1501").unwrap();
    assert_eq!(seqpage::rulings::check_section(page, seqpage::SectionKey::counter(5, 0), 1).unwrap().rule, "R9");
    assert_eq!(seqpage::rulings::check_section(page, seqpage::SectionKey::counter(5, 99), 1).unwrap().rule, "R9");
}

#[test]
fn r8_draft_is_addressed_ff_draft() {
    let t = bob().replacen("--- @8 put 10.11.21.1001.01.draft\n", "--- @8 put 10.11.21.1001.01\ntail: draft\n", 1).replacen("@8 put 10.11.21.1001.01.draft\n", "@8 put 10.11.21.1001.01\n", 1);
    let r = check_text(&t, None, None);
    assert!(r.errors.iter().any(|e| e.rule == "R8"), "{:?}", r.errors);
    let p = read("docs/spec/examples/proposals/10.11.21.1002.seq").replacen("--- new put 10.11.21.1002.04.draft\n", "--- new put 10.11.21.1002.04\ntail: draft\n", 1);
    assert!(check_text(&p, None, None).errors.iter().any(|e| e.rule == "R8"));
    let mut log = bob_book();
    log.entries[7].addr = "10.11.21.1001.01".into();
    log.entries[7].tail = Some("draft".into());
    assert_eq!(seqpage::export(&log, seqpage::PageId::parse("10.11.21.1001").unwrap()).unwrap_err().rule, "R8");
}

#[test]
fn r5_draft_shows_why() {
    let t = timer();
    assert!(t.contains("why-draft := the 01 wording now says the timer stops; the 04 why must say it too"));
    let r = check_text(&bob(), None, None);
    assert!(r.ok);
    assert!(r.findings.iter().any(|f| f.rule == "R5" && f.axiom == Some("7")), "{:?}", r.findings);
    // a note gives the reason when the opening entry has none
    let mut log = timer_book();
    let n = log.entries.len();
    log.entries[n - 2].extra.clear();
    let txt = seqpage::export(&log, seqpage::PageId::parse("10.11.30.1501").unwrap()).unwrap();
    assert!(txt.contains("why-draft := Add: after the ring the timer stops, matching 01."), "{txt}");
}

#[test]
fn r7_override_pages_are_marked() {
    assert_eq!(seqpage::derive::kind_value(3), Some("override (R7)"));
    assert_eq!(seqpage::derive::kind_value(56), None);
}
