//! Record the four pack runs. The return sits on face 06 because a return
//! op on the same counter is not in the core yet. Tails move draft to return.

use std::env;
use std::path::Path;

use seqbook::Writer;

const AT: &str = "2026-11-11T19:55:00Z";
const BY: &str = "cursor";

fn main() {
    let path = env::args().nth(1).expect("book path");
    let mut writer = Writer::open(Path::new(&path)).expect("open book");
    for (page, body) in RETURNS {
        writer
            .put(AT, BY, &format!("10.10.10.{page}.06.01"), body, None)
            .expect(page);
        let addr = format!("10.10.10.{page}.05.01");
        for (from, to) in [("draft", "pack"), ("pack", "open"), ("open", "return")] {
            writer.tail(AT, BY, &addr, from, to).expect(from);
        }
    }
    println!("len {}", writer.book().len());
}

const RETURNS: &[(&str, &str)] = &[
    (
        "0501",
        "## ran\ntype: note\naxioms: 5.6.9\nby: cursor\nrefs: 10.10.10.0501.05.01\nclaim: 1bf41aaf-03d9-4f17-b080-b551fe3e6781\nwhy: The pack was draft, and the page now has an AGENTS.md, so the run has a place to be recorded.\n\nBuilder read cursor/pages/10.10.10.0501/AGENTS.md and ran the pack.\n\n## w01\nresult: done\ncommand: cargo test --test first_build -- full_address bad_width leading_dot\nevidence: test result: ok. 3 passed; 0 failed.\n\n## w02\nresult: done\ncommand: cargo test --test first_build put_creates_tail_moves_from_current_and_torn_line_drops\nevidence: test result: ok. 1 passed; 0 failed.\n\n## w03\nresult: done\nevidence: Append is only Writer::create, Writer::open, Writer::put, and Writer::tail.\n\n## w04\nresult: done\nevidence: core/fixtures/10.11.21.book has title: timer on page 1001.\n\n## w05\nresult: done\nevidence: why: The first fixture has to show a why in the file itself, so a person can check the record without a reader program.\n\n## notes\nThe w01 ask needed the test names after --. Why: cargo accepts one filter before that mark.\n\n## unprompted\nThe builder also read core/src/bin/seqbook.rs. Why: the binary is under core/ and the append check names the writer.\n\n## overflow\nnone. Why: the five asks finished and no file was edited.\n\nLint finding: the work cards have no ask line. The page AGENTS.md held the ask. The person ordered this drafted pack to run, so the tail moved. The pack body was not rewritten. This note is the return. It is not a review, and the tail stops at return.\n",
    ),
    (
        "0502",
        "## ran\ntype: note\naxioms: 5.6.9\nby: cursor\nrefs: 10.10.10.0502.05.01\nclaim: 0b18358d-8d4b-428f-a032-cc53f51956f1\nwhy: The pack was draft, and the page now has an AGENTS.md, so the run has a place to be recorded.\n\nBuilder read cursor/pages/10.10.10.0502/AGENTS.md and ran the pack.\n\n## w01\nresult: done\ncommand: cargo test --test next_pages open_appends_to_an_existing_book\nevidence: test open_appends_to_an_existing_book ... ok\n\n## w02\nresult: done\ncommand: cargo run --quiet -- read fixtures/10.11.21.book 10.11.21.1001.04\nevidence: why: The first fixture has to show a why in the file itself, so a person can check the record without a reader program.\nmissing: missing 10.11.21.1001.09\n\n## notes\nNo file was edited. Why: both commands passed on the code already in the grant.\n\n## unprompted\nThe test filter could have been exact. Why: it is a substring, and this run still selected the one named test.\n\n## overflow\nThe work cards have no ask line. Why: the page AGENTS.md already records that finding, and the pack body stays as written.\n\nThe person ordered this drafted pack to run, so the tail moved. This note is the return. It is not a review, and the tail stops at return.\n",
    ),
    (
        "0503",
        "## ran\ntype: note\naxioms: 5.6.9\nby: cursor\nrefs: 10.10.10.0503.05.01\nclaim: 52a68f1b-6495-457b-b16d-84c7c0ac6f3f\nwhy: The pack was draft, and the page now has an AGENTS.md, so the run has a place to be recorded.\n\nBuilder read cursor/pages/10.10.10.0503/AGENTS.md and ran the pack.\n\n## w01\nresult: done\ncommand: cargo test --test next_pages -- missing_why_is_a_hard_gap copied_why_is_a_finding timer_fixture_passes_both_checks\nevidence: test result: ok. 3 passed; 0 failed.\n\n## notes\nnone. Why: the three tests passed on the check already in core/, and nothing was edited.\n\n## unprompted\nOne cargo run per test name. Why: the first form of the ask was not a command cargo accepts.\n\n## overflow\nThe tests call why_gaps in process. They do not run seqbook check. Keyword branding stayed untouched. Why: both sit outside the ask, and keyword branding is a stop.\n\nLint finding: the work card has no ask line. The page AGENTS.md held the ask. The person ordered this drafted pack to run, so the tail moved. This note is the return. It is not a review, and the tail stops at return.\n",
    ),
    (
        "0504",
        "## ran\ntype: note\naxioms: 5.6.9\nby: cursor\nrefs: 10.10.10.0504.05.01\nclaim: f13de36c-7b36-4084-aa10-64ab5e38f63e\nwhy: The pack was draft, and the page now has an AGENTS.md, so the run has a place to be recorded.\n\nBuilder read cursor/pages/10.10.10.0504/AGENTS.md. The first ask was not a command cargo accepts, so the page ask was corrected and the pack was run again.\n\n## w01\nresult: done\ncommand: cargo test --test next_pages -- page_shape_rejects_a_stamp_with_only_face_07 timer_fixture_passes_both_checks\nevidence: test result: ok. 2 passed; 0 failed.\n\n## notes\nNo file in the grant was edited. Why: both named tests passed.\n\n## unprompted\nAlso run seqbook check on a page of only face 07 and a page with no face 00. Why: the pack outcome names seqbook check, and these tests call page_gaps in process. That extra command was not part of the ask, so it was not run.\n\n## overflow\nFive other tests in next_pages were filtered out. Why: they were not on this ask.\n\nLint finding: the work card has no ask line. The page AGENTS.md held the ask. The person ordered this drafted pack to run, so the tail moved. This note is the return. It is not a review, and the tail stops at return.\n",
    ),
];
