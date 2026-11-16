//! Record the next three dev pages, then the build pages once the files exist.
//!
//! `cargo run --example stand_next -- plan <temp.book>`
//! `cargo run --example stand_next -- built <temp.book>`

use std::env;
use std::path::Path;
use std::process::Command;

use seqbook::{Error, Tail, Writer};

const AT: &str = "2026-11-11T19:41:00Z";
const BY: &str = "cursor";

struct Subject {
    page: &'static str,
    title: &'static str,
    law: &'static str,
    why: &'static str,
    explanation: &'static str,
    pack: &'static str,
    module: &'static str,
    files: &'static str,
    files_why: &'static str,
}

const SUBJECTS: &[Subject] = &[
    Subject {
        page: "0402",
        title: "read",
        law: "MVP: print one face from a book file.\n\nDone: seqbook read on the timer fixture prints the why sentence, and a missing address exits without inventing a face. The writer can append to an existing book, so this plan is recorded by the same path as any later put.",
        why: "A why buried in a JSON line is still a file, but a person should be able to ask for one face and see only that face.",
        explanation: "The first build proved the log replays. It did not give a person a way to name an address and read that face alone. This page is that step. Printing the face is the whole MVP. It is not a reader for links, and it is not the Next.js app.\n\nDone looks like the timer why appearing as Markdown. Done does not look like a search, a page list, or a second book format.",
        pack: "by: cursor\nauthorized: person-2026-11-11-next-pages\nlead: M\naxioms: 5.4\noutcome: seqbook read prints one face, and Writer::open appends to an existing book.\noverview: A person names a book file and an address and sees that face's Markdown.\nstop if: The work needs the compute, the Next.js app, or an edit to seqAddr.md or decisions.md.\ngrant: core/src/book.rs, core/src/bin/seqbook.rs, core/tests/next_pages.rs, and appends to cursor/temp.book.\nframe: read\nrisk: 2\npredecessor: 10.10.10.0401\n\n## w01\ntype: work\ntitle: Open an existing book and append\naxioms: 6\nreason: These pages have to be written by the writer, or the core grows a second way to append.\npath: core/src/book.rs\n\n## w02\ntype: work\ntitle: Print one face\naxioms: 5.4\nreason: The timer why has to be readable as the face, not as a JSON line.\npath: core/src/bin/seqbook.rs\n",
        module: "This build page is the read command. It prints one face and can append to a book that already exists.",
        files: "core/src/bin/seqbook.rs prints one face from a book file.\n\ncore/src/book.rs Writer::open loads a book and appends. It refuses a file whose last line is torn.",
        files_why: "The read command is the piece a person runs. The open path is how the book grows without a second writer.",
    },
    Subject {
        page: "0403",
        title: "why-check",
        law: "MVP: reject a 01 or 02 card that has no 04 card with the same key, a why line, and a body.\n\nDone: the timer fixture passes, and a page whose purpose card has no 04 twin fails the check. A 04 body that copies the 01 body is a finding, not a failure.",
        why: "The why is the part that has to survive after the recipe rots, so a missing why is not a style nit.",
        explanation: "C3.2 already calls the missing twin, the missing why line, and the missing body a hard refusal. This page puts that rule in the core as a check a person can run. It does not decide the open keyword rule, and it does not turn the check into the compute.",
        pack: "by: cursor\nauthorized: person-2026-11-11-next-pages\nlead: M\naxioms: 4.5\noutcome: seqbook check fails a 01 card with no 04 why, and the timer fixture passes.\noverview: The why rule from C3.2 runs against a book file.\nstop if: The work needs the compute, keyword branding, or an edit to decisions.md.\ngrant: core/src/check.rs, core/src/bin/seqbook.rs, core/tests/next_pages.rs, and appends to cursor/temp.book.\nframe: why-check\nrisk: 2\npredecessor: 10.10.10.0402\n\n## w01\ntype: work\ntitle: Check the why rule\naxioms: 4\nreason: A fixture that happens to contain a why is not the same as a check that refuses a missing one.\npath: core/src/check.rs\n",
        module: "This build page is the why check. A 01 or 02 card without a 04 why is a hard gap.",
        files: "core/src/check.rs why_gaps reads faces 01, 02, and 04.\n\nA missing twin, a missing why line, or a missing body is hard. A 04 body copied from face 01 is a finding.",
        files_why: "The check has to name the card and the page, or a person cannot find the gap in the file.",
    },
    Subject {
        page: "0404",
        title: "page-shape",
        law: "MVP: reject a page that has faces but no face 00, or no content face in 01-06 or 08.\n\nDone: the timer fixture passes. A page with only face 07 fails. A page with only face 01 fails because face 00 is missing.",
        why: "A page with no stamp, or a stamp with nothing a person or a model can read, is not a page yet.",
        explanation: "C1 says a page needs face 00 and at least one of 01-06 or 08. Face 07 does not count. This check makes that visible before a later compute refuses the write. Draft faces count, because a page is allowed to start as a draft.",
        pack: "by: cursor\nauthorized: person-2026-11-11-next-pages\nlead: M\naxioms: 5.2\noutcome: seqbook check fails a page of only face 07, and fails a page with no face 00.\noverview: The page-shape rule from C1 runs against a book file.\nstop if: The work needs the compute, or a change to which faces count.\ngrant: core/src/check.rs, core/src/bin/seqbook.rs, core/tests/next_pages.rs, and appends to cursor/temp.book.\nframe: page-shape\nrisk: 2\npredecessor: 10.10.10.0403\n\n## w01\ntype: work\ntitle: Check the page shape\naxioms: 5.2\nreason: Face 00 and a content face are what make an address a page rather than a loose note.\npath: core/src/check.rs\n",
        module: "This build page is the page-shape check. Face 00 and a content face are both required once a page has any face.",
        files: "core/src/check.rs page_gaps groups stored faces by page.\n\nFace 07 does not count as content. Faces 01-06 and 08 do. Draft faces count.",
        files_why: "The shape check is separate from the why check so a missing stamp is not reported as a missing why.",
    },
];

fn main() {
    let mut args = env::args().skip(1);
    let mode = args.next().unwrap_or_else(|| "plan".into());
    let path = args.next().expect("book path");
    let mut writer = Writer::open(Path::new(&path)).unwrap_or_else(|err| {
        eprintln!("{err}");
        std::process::exit(1);
    });
    match mode.as_str() {
        "plan" => {
            for subject in SUBJECTS {
                stand_plan(&mut writer, subject);
            }
        }
        "built" => {
            let revision = revision();
            for subject in SUBJECTS {
                stand_built(&mut writer, subject, &revision);
            }
            put(
                &mut writer,
                "10.10.10.0302.06.01",
                "## copied\ntype: note\naxioms: 4.9\nby: cursor\nrefs: 10.10.10.0302.04, 10.10.10.0303.04, 10.10.10.0304.04\nwhy: A finding that stays in the chat is not on the page that has it.\n\nseqbook check reports a finding on 0302, 0303, and 0304. The face 04 card module repeats the face 01 body. That is the C3.2 finding, not a hard gap. The faces cannot be rewritten from here. A later draft is how the wording gets replaced.\n",
                None,
            );
        }
        other => {
            eprintln!("mode is plan or built, not {other}");
            std::process::exit(2);
        }
    }
    println!("{} {}", mode, writer.book().len());
}

fn stand_plan(writer: &mut Writer, subject: &Subject) {
    let dev = subject.page;
    let jobs = band(dev, '5');
    put(
        writer,
        &format!("10.10.10.{dev}.00"),
        &format!(
            "address: {dev}\ntitle: {}\nstate: draft\ntype: workflow\naxioms: 5\nband: dev\nthousands: 0\nmvp: {}\n",
            subject.title, subject.title
        ),
        None,
    );
    put(
        writer,
        &format!("10.10.10.{dev}.01"),
        &format!(
            "## frame\ntype: rule\naxioms: 5\n\n{}\n",
            subject.law
        ),
        None,
    );
    put(
        writer,
        &format!("10.10.10.{dev}.04"),
        &format!(
            "## frame\ntype: why\nsource: [01 / frame]\naxioms: 4.5\nwhy: {}\n\n{}\n",
            subject.why, subject.explanation
        ),
        None,
    );
    put(
        writer,
        &format!("10.10.10.{dev}.08"),
        &format!(
            "## frame\ntype: link\naxioms: 8.7\nkind: 7\nwhy: The set is written both ways. Link kinds are not settled.\n\nDev {dev}.{}. Build {}.{} . Jobs {}.{}.\n",
            subject.title,
            band(dev, '3'),
            subject.title,
            jobs,
            subject.title
        ),
        None,
    );
    put(
        writer,
        &format!("10.10.10.{jobs}.00"),
        &format!(
            "address: {jobs}\ntitle: {}\nstate: draft\ntype: workflow\naxioms: 5\nband: jobs\nthousands: 0\n",
            subject.title
        ),
        None,
    );
    put(
        writer,
        &format!("10.10.10.{jobs}.01"),
        &format!(
            "## frame\ntype: rule\naxioms: 5\n\nPacks for {} live here. The first pack is {jobs}.05.01 and stays draft until something lints it.\n",
            subject.title
        ),
        None,
    );
    put(
        writer,
        &format!("10.10.10.{jobs}.04"),
        &format!(
            "## frame\ntype: why\nsource: [01 / frame]\naxioms: 5.4\nwhy: The pack is the grant a builder can point at, separate from the design page.\n\n{jobs} holds the work cards for {}. Writing the pack is not a claim, and the tail stays draft because no compute linted it.\n",
            subject.title
        ),
        None,
    );
    put(
        writer,
        &format!("10.10.10.{jobs}.08"),
        &format!(
            "## frame\ntype: link\naxioms: 8.7\nkind: 7\nwhy: The jobs page points back at the dev page it packs.\n\nDev page: {dev}.{}.\n",
            subject.title
        ),
        None,
    );
    put(
        writer,
        &format!("10.10.10.{jobs}.05.01"),
        subject.pack,
        Some(Tail::Draft),
    );
}

fn stand_built(writer: &mut Writer, subject: &Subject, revision: &str) {
    let dev = subject.page;
    let build = band(dev, '3');
    put(
        writer,
        &format!("10.10.10.{build}.00"),
        &format!(
            "address: {build}\ntitle: {}\nstate: draft\ntype: workflow\naxioms: 8.6\nband: build\nthousands: 0\n",
            subject.title
        ),
        None,
    );
    put(
        writer,
        &format!("10.10.10.{build}.01"),
        &format!("## module\ntype: rule\naxioms: 8.6\n\n{}\n", subject.module),
        None,
    );
    put(
        writer,
        &format!("10.10.10.{build}.02"),
        &format!("## files\ntype: schema\naxioms: 8.6\n\n{}\n", subject.files),
        None,
    );
    put(
        writer,
        &format!("10.10.10.{build}.04"),
        &format!(
            "## module\ntype: why\nsource: [01 / module]\naxioms: 8.6.4\nwhy: The book keeps what the module is for. The repo keeps the code.\n\nFace 01 names the module. This face is the reason that name stays in the book after the source in the repo has changed.\n\n## files\ntype: why\nsource: [02 / files]\naxioms: 8.4\nwhy: {}\n\nChecked against revision {revision}. The paths are the files this page names. A missing path would be a gap, not a renamed guess.\n",
            subject.files_why
        ),
        None,
    );
    put(
        writer,
        &format!("10.10.10.{build}.08"),
        &format!(
            "## module\ntype: link\naxioms: 8.6.7\nkind: 7\nwhy: The build page points at the dev page and at the repo paths.\n\nDev page: {dev}.{}.\nRevision: {revision}.\nPaths: core/src/check.rs, core/src/bin/seqbook.rs, core/src/book.rs.\n",
            subject.title
        ),
        None,
    );
    put(
        writer,
        &format!("10.10.10.{dev}.06.01"),
        &format!(
            "## ran\ntype: note\naxioms: 9.6\nby: cursor\nrefs: 10.10.10.{}.05.01\nwhy: The run has to sit next to the MVP, not only in the test output.\n\nThe MVP on this page was run on 2026-11-11. cargo test next_pages passed with the read, why, and page-shape checks. Pack {}.05.01 stays draft. This note is not a review.\n",
            band(dev, '5'),
            band(dev, '5')
        ),
        None,
    );
}

fn band(page: &str, digit: char) -> String {
    let mut chars: Vec<char> = page.chars().collect();
    chars[1] = digit;
    chars.into_iter().collect()
}

fn put(writer: &mut Writer, addr: &str, body: &str, tail: Option<Tail>) {
    match writer.put(AT, BY, addr, body, tail) {
        Ok(()) => {}
        Err(Error::Exists { .. }) => {}
        Err(err) => {
            eprintln!("{addr}: {err}");
            std::process::exit(1);
        }
    }
}

fn revision() -> String {
    match Command::new("git")
        .args(["rev-parse", "--short", "HEAD"])
        .output()
    {
        Ok(output) if output.status.success() => {
            String::from_utf8_lossy(&output.stdout).trim().to_string()
        }
        _ => "uncommitted".into(),
    }
}
