mod common;

use common::{Env, PG};
use std::fs;

/// Outside trial for 90.50.10.0404. The harness stays in tests/common.
/// These cases go through the wf binary, not the builder's parse_return test.
#[test]
fn template_4_return_without_a_design_review_is_refused_and_a_filled_line_is_accepted() {
    let e = Env::ready("v4");
    e.open("src/a.rs", "cargo --version");
    let printed = fs::read_to_string(e.page().join("05.01/RETURN-TEMPLATE.md")).unwrap();
    assert!(printed.contains("design review:"), "template 4 prints the design review line:\n{printed}");
    let hash = pack_hash(&e, 1);

    let sha = commit_return(&e, 1, &return_text(&hash, false));
    let (ok, out) = e.ret(1, &sha, "bob");
    assert!(!ok, "{out}");
    assert!(out.contains("t416u"), "{out}");
    assert!(out.contains("return refused (recorded)"), "{out}");
    let log = e.log();
    assert!(log.contains("\"kind\":\"return-refused\""), "{log}");
    assert!(log.contains("t416u"), "{log}");

    let sha = commit_return(&e, 1, &return_text(&hash, true));
    let (ok, out) = e.ret(1, &sha, "bob");
    assert!(ok, "{out}");
    assert!(e.log().contains("\"kind\":\"return\""), "{}", e.log());
}

#[test]
fn templates_1_2_and_3_print_no_design_review_line_and_accept_a_return_without_one() {
    for ver in ["1", "2", "3"] {
        let e = Env::ready(&format!("old{ver}"));
        open_old_pack(&e, ver);
        let printed = fs::read_to_string(e.page().join("05.01/RETURN-TEMPLATE.md")).unwrap();
        assert!(!printed.contains("design review:"), "template {ver} still prints without the line:\n{printed}");
        let hash = format!("hash-{ver}");
        let sha = commit_return(&e, 1, &return_text(&hash, false));
        let (ok, out) = e.ret(1, &sha, "bob");
        assert!(ok, "template {ver}: {out}");
    }
}

fn pack_hash(e: &Env, nn: u32) -> String {
    let prompt = fs::read_to_string(e.page().join(format!("05.{nn:02}/PROMPT.md"))).unwrap();
    prompt
        .lines()
        .find_map(|l| l.strip_prefix("Pack hash: "))
        .unwrap()
        .split(' ')
        .next()
        .unwrap()
        .to_string()
}

fn return_text(hash: &str, review: bool) -> String {
    let mut t = format!(
        "pack: {hash}\ndone: set a\nchanged: modify src/a.rs\nnoticed: none\nw01: done - a is 2\nproof: tests\n"
    );
    if review {
        t.push_str("design review: docs/AXIOMS.md and docs/DESIGN.md match; no difference\n");
    }
    t.push_str("not done: none\nunprompted: none\noverflow: none\n");
    t
}

fn commit_return(e: &Env, nn: u32, body: &str) -> String {
    let name = format!("{PG}.05.{nn:02}");
    e.git(&["checkout", "-q", "-B", &format!("pass/{name}"), "main"]);
    fs::write(e.root.join("game/src/a.rs"), format!("a = {nn}\n")).unwrap();
    let rel = format!(".workshop/returns/{name}.md");
    fs::create_dir_all(e.root.join("game/.workshop/returns")).unwrap();
    fs::write(e.root.join("game").join(&rel), body).unwrap();
    e.git(&["add", "--", "src/a.rs", &rel]);
    e.git(&["commit", "-q", "-m", "work"]);
    let sha = e.git(&["rev-parse", "HEAD"]);
    e.git(&["checkout", "-q", "main"]);
    sha
}

/// A pack recorded on an older template. wf pack now writes template 4 only,
/// so the old entry is appended the way a page packed before t416u still sits in a log.
fn open_old_pack(e: &Env, ver: &str) {
    let start = e.git(&["rev-parse", "HEAD"]);
    let name = format!("{PG}.05.01");
    let mut page = wf::page::Page::load(&e.page()).unwrap();
    let mut fields = serde_json::Map::new();
    for (k, v) in [
        ("repo", "game"),
        ("may touch", "src/a.rs"),
        ("w01", "set a to 2"),
        ("checks", "cargo --version"),
        ("stop if", "b must change"),
    ] {
        fields.insert(k.into(), serde_json::json!(v));
    }
    page.add("pri", "prime", "draft", serde_json::json!({"pass": 1, "fields": fields, "pins": {}})).unwrap();
    let seq = page.events.len() as u64 + 1;
    let mut d = serde_json::json!({
        "pass": 1,
        "templates": ver,
        "pack_hash": format!("hash-{ver}"),
        "branch": format!("pass/{name}"),
        "return_file": format!(".workshop/returns/{name}.md"),
        "start": start,
        "seq": seq,
        "time": "2020-01-01T00:00:00Z",
        "face01": "Goal: a.\nDone when: checks pass.",
        "done_when": "Done when: checks pass.",
        "pack_text": format!("pack {ver}\n"),
        "sources": {"01": "v1", "axioms": "h", "design": "h"}
    });
    if ver == "3" {
        d["links"] = serde_json::json!([]);
    }
    if ver == "2" || ver == "3" {
        let mut preview = page.pass(1).unwrap().clone();
        preview.pack = Some(d.clone());
        let agents_hash = sha256(&wf::render::agents(&page, &preview).unwrap());
        d["agents_hash"] = serde_json::json!(agents_hash);
        preview.pack = Some(d.clone());
        let prompt_hash = sha256(&wf::render::prompt(&page, &preview).unwrap());
        d["prompt_hash"] = serde_json::json!(prompt_hash);
    }
    page.add("pri", "prime", "pack", d).unwrap();
    page.add("bob", "builder", "claim", serde_json::json!({"pass": 1})).unwrap();
    wf::render::write(&page).unwrap();
}

fn sha256(s: &str) -> String {
    use sha2::{Digest, Sha256};
    Sha256::digest(s.as_bytes()).iter().map(|b| format!("{b:02x}")).collect()
}
