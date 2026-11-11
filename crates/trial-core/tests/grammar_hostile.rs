//! TRIAL-C (1): adversarial address cases, judged against seqAddr.md 1-4 and 8,
//! decisions A1-A6 / C8.2 / C8.5, and Director ruling R1. Each row cites the line it is judged by.
mod common;
use common::*;
use seqaddr_core::addr::*;
use seqaddr_core::face::face_job;
use seqaddr_core::{Active, Address};

/// (input, valid?, spec line)
const CASES: &[(&str, bool, &str)] = &[
    // forms (seqAddr.md:74-86, 89, 92)
    ("10.11.21.4442.05.03", true, "seqAddr.md:74 full counter"),
    ("4442.01", true, "seqAddr.md:83 short"),
    ("12.2523.04", true, "seqAddr.md:84 book form"),
    ("30.12.2523", true, "seqAddr.md:85 shelf form"),
    ("21", true, "seqAddr.md:89 desk"),
    ("10.11", true, "seqAddr.md:89 shelf"),
    ("10.11.21", true, "seqAddr.md:89 book"),
    ("21.0000", true, "seqAddr.md:89 sibling book through its door"),
    (".04", true, "seqAddr.md:92 active page face"),
    (".05.03", true, "seqAddr.md:92 active page task"),
    (".05.03.open", true, "seqAddr.md:271 active-rel = . face-part (tail allowed)"),
    (".4442.01", false, "seqAddr.md:270 active-rel takes only a face-part"),
    ("10.11.21.22", false, "decisions.md:33 no page = container; at most desk.shelf.book"),
    ("10.11.21.22.4442", false, "seqAddr.md:268 at most three ancestors"),
    ("4442.4443", false, "seqAddr.md:71 the page is the only 4-digit axis, once"),
    // widths (seqAddr.md:14)
    ("4442.1", false, "seqAddr.md:14 4442.1 is invalid"),
    ("44420", false, "seqAddr.md:14 exact widths"),
    ("1.4442", false, "seqAddr.md:293 one-digit mark is an axiom"),
    ("7.8", false, "seqAddr.md:293 a chain is never an address"),
    ("123.4442", false, "seqAddr.md:14 ancestors are 2 digits"),
    ("4442.001", false, "seqAddr.md:279 a 3-digit group is a brand and follows a card"),
    ("4442.05.003", false, "seqAddr.md:277 counter is 2 digits"),
    // titles (seqAddr.md:110-116)
    ("4442.timer", true, "seqAddr.md:110 word after PPPP is a title"),
    ("10.11.21.tools", true, "seqAddr.md:266 container title at the end"),
    ("10.tools", true, "seqAddr.md:266 desk title"),
    ("10.tools.21.4442", false, "seqAddr.md:268 ancestors carry no titles (grammar)"),
    ("4442.timer.01", false, "seqAddr.md:110 faces never have titles; a face follows the page"),
    ("4442.timer.plan", false, "seqAddr.md:122 only a tail may follow a title"),
    ("4442.draft.timer", false, "seqAddr.md:269 page-tail ends the address"),
    ("10.11.21.0000.tools", false, "seqAddr.md:115 page 0000 has none"),
    ("4442.Timer", false, "seqAddr.md:112 lowercase"),
    ("4442.my_timer", false, "seqAddr.md:112 letters digits hyphens"),
    ("4442.-x", false, "seqAddr.md:112 starts with a letter"),
    ("4442.1x", false, "seqAddr.md:112 starts with a letter"),
    ("4442.t\u{e9}", false, "seqAddr.md:112 lowercase ASCII letters"),
    ("4442 .timer", false, "seqAddr.md:112 no spaces"),
    ("4442.draft", true, "seqAddr.md:126 PPPP.tail"),
    ("4442.timer.retired", true, "seqAddr.md:126 PPPP.title.tail"),
    ("4442.pack", false, "seqAddr.md:126 page takes draft/retired only"),
    ("10.11.21.draft", false, "seqAddr.md:129 containers take no tail"),
    ("10.11.21.0000.retired", true, "seqAddr.md:129 state comes from the door page"),
    // faces, counters, tails (seqAddr.md:124-140, 277, 287-289)
    ("4442.01.draft", true, "seqAddr.md:127"),
    ("4442.01.retired", true, "seqAddr.md:127"),
    ("4442.04.pack", false, "seqAddr.md:287 pack/open/return/review only with a counter"),
    ("4442.04.open", false, "seqAddr.md:287"),
    ("4442.04.return", false, "seqAddr.md:287"),
    ("4442.04.review", false, "seqAddr.md:287"),
    ("4442.05.03.draft", true, "seqAddr.md:128"),
    ("4442.05.03.pack", true, "seqAddr.md:128"),
    ("4442.05.03.open", true, "seqAddr.md:128"),
    ("4442.05.03.return", true, "seqAddr.md:128"),
    ("4442.05.03.review", true, "seqAddr.md:128"),
    ("4442.05.03.retired", false, "seqAddr.md:287 retired only without a counter"),
    ("4442.05.03.04", false, "seqAddr.md:24 one counter, not an axis"),
    ("4442.01.draft.retired", false, "seqAddr.md:271 one tail"),
    ("1523.05.00", false, "R9 (fix pass) faces have no sentinels; was seqAddr.md:204 board"),
    ("1523.05.01", true, "seqAddr.md:24 counters 01-98"),
    ("1523.05.98", true, "seqAddr.md:24"),
    ("1523.05.99", false, "R9 (fix pass) counters 01-98; was seqAddr.md:257 FF.99 continuation"),
    // cards and brands (seqAddr.md:111, 279-281; decisions.md:443)
    ("10.10.11.1014.01.ham", true, "seqAddr.md:111 card key"),
    ("4442.01.ham.002", true, "seqAddr.md:111 brand"),
    ("4442.01.ham.02", false, "seqAddr.md:279 brand is 3 digits"),
    ("4442.01.ham.000", false, "decisions.md:443 000 reserved"),
    ("4442.01.ham.999", false, "decisions.md:443 999 reserved"),
    ("4442.01.ham.998", true, "decisions.md:443 001-998"),
    ("4442.01.002", false, "decisions.md:421 a 3-digit group can only follow a card"),
    ("4442.05.03.pack.w01", true, "seqAddr.md:271 tail then card"),
    ("4442.05.03.w01.pack", false, "seqAddr.md:271 tail comes before the card"),
    ("4442.01.review", false, "seqAddr.md:281 card is not a tail word; review is a counter tail"),
    // sentinels / doors on every axis (seqAddr.md:26-31; R1)
    ("00.00.00.0000.00", true, "R1 door on every axis"),
    ("10.00.21.4442.01", true, "seqAddr.md:49 desk book DD.00.BB"),
    ("10.99", true, "decisions.md:218 DD.99 child desks pointer"),
    ("10.11.99", true, "decisions.md:219 shelf pointer"),
    ("10.11.21.9999", true, "seqAddr.md:226 book continuation"),
    ("10.11.21.4442.00", true, "seqAddr.md:149 face 00"),
    // empties
    ("", false, "seqAddr.md:265"),
    ("10..11", false, "seqAddr.md:265"),
    (".", false, "seqAddr.md:270"),
    ("4442.", false, "seqAddr.md:265"),
];

#[test]
fn every_case_matches_the_spec() {
    let mut wrong = vec![];
    for (s, valid, cite) in CASES {
        let got = Address::parse(s);
        if got.is_ok() != *valid {
            wrong.push(format!("{s:?}: spec says {} ({cite}); core says {:?}", if *valid { "valid" } else { "invalid" }, got.map(|a| a.to_string())));
        }
    }
    assert!(wrong.is_empty(), "{}", wrong.join("\n"));
}

#[test]
fn valid_cases_round_trip_through_display() {
    for (s, valid, _) in CASES {
        if *valid {
            assert_eq!(Address::parse(s).unwrap().to_string(), *s);
        }
    }
}

#[test]
fn short_forms_expand_per_seqaddr_2_1() {
    let act = Active { book: bid("10.11.21"), pages: vec![1523] };
    for (s, full) in [
        ("4442.01", "10.11.21.4442.01"),
        ("12.2523.04", "10.11.12.2523.04"),
        ("30.12.2523", "10.30.12.2523"),
        ("10.11.21.4442", "10.11.21.4442"),
        (".05.03", "10.11.21.1523.05.03"),
    ] {
        assert_eq!(Address::parse(s).unwrap().expand(&act).unwrap().to_string(), full, "{s}");
    }
    // A1.3: `21.0000` is book 21 on the active shelf.
    let act2 = Active { book: bid("10.11.30"), pages: vec![] };
    assert_eq!(Address::parse("21.0000").unwrap().expand(&act2).unwrap().to_string(), "10.11.21.0000");
}

#[test]
fn r1_doors_and_pointers_on_every_axis() {
    // seqAddr.md:29-31 + R1: all-zero is the door, all-nine the pointer, on 2- and 4-digit axes.
    for w in [2u8, 4] {
        assert_eq!(sentinel(0, w), Some(Sentinel::Door));
    }
    assert_eq!(sentinel(99, 2), Some(Sentinel::Pointer));
    assert_eq!(sentinel(9999, 4), Some(Sentinel::Pointer));
    assert_eq!(page_kind(0), PageKind::Door);
    assert_eq!(page_kind(9999), PageKind::BookContinuation);
    // R9 (fix pass): faces have no sentinels - 00/99 are not counters; R10: face 00 is the registry.
    assert_eq!(counter_role(0), CounterRole::NotACounter);
    assert_eq!(counter_role(99), CounterRole::NotACounter);
    assert_eq!(face_job(0).name(), "registry");
    for v in [0u8, 99] {
        assert!(is_axis_sentinel(v));
    }
    assert!(!is_axis_sentinel(1) && !is_axis_sentinel(98));
}

#[test]
// fixed in CORE fix pass (was #[ignore = "finding 14"])
fn r1_sentinel_on_a_three_digit_group() {
    // R1 speaks of "a full zero sequence" / full-nine on any group. Brands are 3 digits (seqAddr.md:279);
    // decisions.md:443 reserves 000 and 999. `sentinel(v, 3)` treated 99 as the pointer and 999 as nothing.
    // Fix pass under R9 (sentinels only on desk/shelf/book/page): a 3-digit group has no sentinel at all,
    // the "reject widths other than 2/4" option this finding offered.
    assert_eq!(sentinel(999, 3), None);
    assert_eq!(sentinel(99, 3), None);
    assert_eq!(sentinel(0, 3), None);
}

#[test]
fn page_ranges_per_seqaddr_6() {
    use PageKind::*;
    for (p, k) in [(0, Door), (1, SpecialReserved), (9, SpecialReserved), (10, Required), (19, Required), (20, Localized), (49, Localized), (50, Structural), (99, Structural), (100, BandHead), (199, BandContinuation), (150, StandardBand), (999, BandContinuation), (1000, BandHead), (1001, User), (9998, User), (9999, BookContinuation)] {
        assert_eq!(page_kind(p), k, "{p:04}");
    }
    // 0099 is structural, not a band continuation: bands start at 0100 (seqAddr.md:240-242).
    assert_eq!(band_of(99), None);
}

/// Generate a random address from the grammar (seqAddr.md:264-283).
fn gen(r: &mut Rng) -> String {
    let d2 = |r: &mut Rng| format!("{:02}", r.below(100));
    let titles = ["timer", "a", "x-1", "plan-b9", "tools"];
    let cards = ["ham", "w01", "retry-policy", "z"];
    let mut parts: Vec<String> = vec![];
    match r.below(3) {
        0 => {
            // container
            for _ in 0..(1 + r.below(3)) {
                parts.push(d2(r));
            }
            if r.below(2) == 0 {
                parts.push(r.pick(&titles).to_string());
            }
        }
        _ => {
            for _ in 0..r.below(4) {
                parts.push(d2(r));
            }
            parts.push(format!("{:04}", r.below(10000)));
            match r.below(4) {
                0 => {}
                1 => {
                    if r.below(2) == 0 {
                        parts.push(r.pick(&titles).to_string());
                    }
                    if r.below(2) == 0 {
                        parts.push(r.pick(&["draft", "retired"]).to_string());
                    }
                    if parts.last().map(|s| s.len() == 4 && s.chars().all(|c| c.is_ascii_digit())).unwrap_or(false) && parts.len() > 0 {
                        // 0000 takes no title; keep it simple: nothing added
                    }
                }
                _ => {
                    parts.push(d2(r));
                    let counter = r.below(2) == 0;
                    if counter {
                        parts.push(format!("{:02}", 1 + r.below(98)));
                    }
                    if r.below(2) == 0 {
                        let t = if counter { *r.pick(&["draft", "pack", "open", "return", "review"]) } else { *r.pick(&["draft", "retired"]) };
                        parts.push(t.into());
                    }
                    if r.below(2) == 0 {
                        parts.push(r.pick(&cards).to_string());
                        if r.below(2) == 0 {
                            parts.push(format!("{:03}", 1 + r.below(998)));
                        }
                    }
                }
            }
        }
    }
    parts.join(".")
}

#[test]
fn property_grammar_strings_parse_and_round_trip() {
    let mut r = Rng(0x5eed_c0de);
    let mut n = 0;
    for _ in 0..20_000 {
        let s = gen(&mut r);
        if s.contains(".0000.") && !s.split('.').skip_while(|p| *p != "0000").nth(1).map(|p| p.chars().all(|c| c.is_ascii_digit()) || ["draft", "retired"].contains(&p)).unwrap_or(true) {
            continue; // title after 0000 is invalid by A2.8, skip
        }
        let a = Address::parse(&s).unwrap_or_else(|e| panic!("{s}: {e:?}"));
        assert_eq!(a.to_string(), s);
        assert_eq!(Address::parse(&a.to_string()).unwrap(), a);
        n += 1;
    }
    assert!(n > 15_000);
}

#[test]
fn fuzz_parse_never_panics_and_round_trips_when_ok() {
    let alphabet: Vec<char> = "0123456789.....abdrtfz-_ AÉ\u{0663}\u{ff11}".chars().collect();
    let mut r = Rng(42);
    for _ in 0..200_000 {
        let len = r.below(24);
        let s: String = (0..len).map(|_| *r.pick(&alphabet)).collect();
        if let Ok(a) = Address::parse(&s) {
            // whatever parses must print back to something that parses to the same address
            assert_eq!(Address::parse(&a.to_string()).unwrap(), a, "{s:?}");
            assert!(s.is_ascii(), "non-ASCII accepted: {s:?}");
        }
        let _ = seqaddr_core::AxiomChain::parse(&s);
    }
}
