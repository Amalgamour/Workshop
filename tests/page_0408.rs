mod common;

use common::{Env, PG};

/// Withdraw at pack, with no claim. The pass stays in the log and no longer holds its files.
#[test]
fn withdraw_at_pack_with_no_claim_keeps_the_pass() {
    let e = Env::ready("wd-pack");
    let help = e.ok(&["help"]);
    assert!(help.contains("withdraw <page> <NN>"), "{help}");
    e.draft("src/a.rs", "cargo --version");
    e.no(&["withdraw", PG, "1", "--as", "pri"], "is at 'draft'");
    e.held("05", "pri", &["pack", PG, "1", "--as", "pri"]);
    e.no(&["withdraw", PG, "1", "--as", "bob"], "only the prime");
    let out = e.ok(&["withdraw", PG, "1", "--as", "pri"]);
    assert!(out.contains("withdrew 05.01"), "{out}");
    let log = e.log();
    assert!(log.contains("\"kind\":\"draft\""), "{log}");
    assert!(log.contains("\"kind\":\"pack\""), "{log}");
    assert!(log.contains("\"kind\":\"withdraw\""), "{log}");
    let p = wf::page::Page::load(&e.page()).unwrap();
    let x = p.pass(1).unwrap();
    assert_eq!(x.tail, "withdrawn");
    assert!(x.claim.is_none());
    assert!(!x.is_open_tail());
    let status = e.ok(&["status", PG]);
    assert!(status.contains("05.01 withdrawn"), "{status}");
    let before = e.log();
    e.no(&["withdraw", PG, "1", "--as", "pri"], "is at 'withdrawn'");
    assert_eq!(e.log(), before);
    e.ok(&["halt", PG, "--note", "packed pass withdrawn (t0408)", "--as", "pri"]);
}

/// Open, return, review and closed are past pack, so withdraw is refused and writes nothing.
#[test]
fn withdraw_is_refused_at_open_or_later() {
    let e = Env::ready("wd-open");
    e.open("src/a.rs", "cargo --version");
    let before = e.log();
    e.no(&["withdraw", PG, "1", "--as", "pri"], "is at 'open'");
    assert_eq!(e.log(), before);

    let e = Env::ready("wd-return");
    e.open("src/a.rs", "cargo --version");
    let sha = e.work(1, &[("src/a.rs", "a = 2\n")], "w01: done - a");
    assert!(e.ret(1, &sha, "bob").0, "return");
    e.no(&["withdraw", PG, "1", "--as", "pri"], "is at 'return'");

    let e = Env::checked("wd-review");
    e.no(&["withdraw", PG, "1", "--as", "pri"], "is at 'review'");

    let e = Env::checked("wd-closed");
    e.lock("05", "pri");
    e.ok(&["signoff", PG, "1", "--outcome", "passed", "--as", "pri"]);
    e.ok(&["close", PG, "1", "--as", "pri"]);
    e.unlock("pri");
    let before = e.log();
    e.no(&["withdraw", PG, "1", "--as", "pri"], "is at 'closed'");
    assert_eq!(e.log(), before);
    assert!(wf::page::Page::load(&e.page()).unwrap().pass(1).is_ok());
}

/// After withdraw, a builder cannot claim the pass, and the log is unchanged.
#[test]
fn a_later_claim_is_refused() {
    let e = Env::ready("wd-claim");
    e.draft("src/a.rs", "cargo --version");
    e.held("05", "pri", &["pack", PG, "1", "--as", "pri"]);
    e.ok(&["withdraw", PG, "1", "--as", "pri"]);
    e.lock("05", "bob");
    let before = e.log();
    e.no(&["claim", PG, "1", "--as", "bob"], "is at 'withdrawn'");
    assert_eq!(e.log(), before);
    let p = wf::page::Page::load(&e.page()).unwrap();
    let x = p.pass(1).unwrap();
    assert_eq!(x.tail, "withdrawn");
    assert!(x.claim.is_none());
    assert!(before.lines().any(|l| l.contains("\"kind\":\"withdraw\"") && l.contains("\"pass\":1")));
    e.unlock("bob");
}
