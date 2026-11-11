//! The compute's books: bootstrap (kernel-design 7), reads (format 4.2) and the
//! one write path, proposals (format 1.2, 4.1). Only this module writes book files.

use seqaddr_core::addr::{Address, BookId, FacePart, PageAddr};
use seqaddr_core::cards::{parse_face, title_form};
use seqaddr_core::log::{self, BookLog, Entry, Op};
use seqaddr_core::resolve::{Found, Resolution};
use seqaddr_core::state::{BookState, FaceState, PageState};
use seqaddr_core::{validate, Policy, Proposal, SeqError, World};
use serde_json::{json, Map, Value};
use std::collections::{BTreeMap, BTreeSet, VecDeque};
use std::path::{Path, PathBuf};

/// The format version this compute reads (format 3.2 header `seqbook`).
pub const FORMAT_VERSION: u32 = 1;

/// Approval check for seating a face on every path (`promote`, bare `put`, a
/// draft moved to bare). Director ruling R2. Checked here first (403, axiom 1:
/// authority), then the core checks the same record again (E7/R2).
#[derive(Debug, Clone)]
pub struct ApprovalGate {
    /// Seating must carry `approved_by`.
    pub require: bool,
    /// R2 build stage: `approved_by: "build-stage (R2)"` with a `trial` reference is valid.
    pub allow_build_stage_r2: bool,
    /// Identity names that are the Director (7: provisional identity design).
    pub director_names: Vec<String>,
}

impl Default for ApprovalGate {
    fn default() -> Self {
        ApprovalGate { require: true, allow_build_stage_r2: true, director_names: vec![crate::identity::DIRECTOR.into()] }
    }
}

#[derive(Debug, Clone)]
pub struct Config {
    /// Folders holding `DD.SS.BB.book` files, first wins for the same address (format 1.2: books/ and kernel/).
    pub dirs: Vec<PathBuf>,
    /// Where a brand-new book file is created.
    pub write_dir: PathBuf,
    pub policy: Policy,
    pub approval: ApprovalGate,
    /// How many proposals /queue keeps in memory (all are kept in `.queue`).
    pub queue_keep: usize,
    /// Who may write. `None`: read `<write_dir>/.identities` at boot (no file: every write is refused).
    pub identities: Option<crate::identity::Identities>,
    /// The repository root: R2 trial references (`docs/trial/...`) are checked under it.
    pub repo_root: PathBuf,
    /// R11 common-questions page number in a book (7: spec silent; 0013 beside the dictionary 0012).
    pub ask_page: u16,
    /// The reader's book when a request names none (/brands, /ask). `None`: kernel only.
    pub default_book: Option<BookId>,
    pub ask: ask::Config,
}

impl Config {
    pub fn for_dirs(dirs: Vec<PathBuf>) -> Config {
        let write_dir = dirs.first().cloned().unwrap_or_else(|| PathBuf::from("books"));
        let repo_root = std::env::var("WORKSHOP_ROOT").map(PathBuf::from).unwrap_or_else(|_| PathBuf::from(concat!(env!("CARGO_MANIFEST_DIR"), "/../..")));
        Config { dirs, write_dir, policy: Policy::default(), approval: ApprovalGate::default(), queue_keep: 200, identities: None, repo_root, ask_page: 13, default_book: None, ask: ask::Config::default() }
    }
}

/// Why the compute refused to start (kernel-design 7.6: report, never guess).
#[derive(Debug, Clone)]
pub struct BootError {
    pub step: &'static str,
    pub detail: String,
    pub refused: Vec<Value>,
}

impl std::fmt::Display for BootError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", json!({"boot": "refused", "step": self.step, "detail": self.detail, "refused": self.refused}))
    }
}

pub struct Store {
    pub cfg: Config,
    pub world: World,
    pub logs: BTreeMap<BookId, BookLog>,
    pub paths: BTreeMap<BookId, PathBuf>,
    pub warnings: BTreeMap<BookId, Vec<String>>,
    pub refused: Vec<Value>,
    pub queue: VecDeque<Value>,
    pub queue_seq: u64,
    pub boot: Vec<Value>,
    pub ids: crate::identity::Identities,
    /// Known-good length of each book file: appends go straight to the end (TRIAL-X #15).
    pub file_len: BTreeMap<BookId, u64>,
}

/// One HTTP-ready answer: status code and JSON body.
pub type Answer = (u16, Value);

/// HTTP code for a core error on a read: a malformed address is 400 everywhere
/// (TRIAL-X #9), elevate is 409 (never a 3xx redirect, #8). 7: contract gives no codes.
pub fn http_code(e: &SeqError) -> u16 {
    match e.code() {
        "invalid" => 400,
        "elevate" => 409,
        _ => e.http_status(),
    }
}

pub fn err_json(e: &SeqError) -> Answer {
    (http_code(e), json!({"error": e.code(), "axiom": e.axiom(), "rule": e.rule(), "detail": e.detail()}))
}

fn bad(detail: impl Into<String>) -> Answer {
    (400, json!({"error": "invalid", "detail": detail.into()}))
}

fn missing(detail: impl Into<String>, extra: Value) -> Answer {
    let mut v = json!({"error": "missing", "axiom": "7", "detail": detail.into()});
    if let (Some(m), Value::Object(x)) = (v.as_object_mut(), extra) {
        m.extend(x);
    }
    (404, v)
}

fn is_book_file(name: &str) -> Option<BookId> {
    let stem = name.strip_suffix(".book")?;
    let b = stem.as_bytes();
    if b.len() == 8 && b[2] == b'.' && b[5] == b'.' && stem.chars().enumerate().all(|(i, c)| i == 2 || i == 5 || c.is_ascii_digit()) {
        BookId::parse(stem).ok()
    } else {
        None
    }
}

/// Level name of a book in the lookup chain of `asked` (seqAddr 2.5: book, shelf, desk, kernel).
pub fn level(asked: BookId, at: BookId) -> &'static str {
    if asked == at {
        "local"
    } else if at == BookId::KERNEL {
        "kernel"
    } else if at.shelf == 0 {
        "desk"
    } else {
        "shelf"
    }
}

/// A face key as the reader shows it: `FF`, `FF.draft`, `FF.retired`, `FF.NN`, `FF.00` (derived board).
#[derive(Debug, Clone)]
pub struct FaceItem {
    pub key: String,
    pub face: u8,
    pub counter: Option<u8>,
    pub body: String,
    pub tail: Option<String>,
    /// Live content is inherited; drafts and retired faces are not (seqAddr 4: draft = "not active").
    pub live: bool,
}

pub fn board_body(st: &BookState, page: u16, face: u8) -> String {
    st.board(page, face).iter().map(|l| format!("{:02}: {}", l.counter, l.tail.board_word())).collect::<Vec<_>>().join("\n")
}

pub fn face_items(st: &BookState, page: u16, f: u8, fs: &FaceState) -> Vec<FaceItem> {
    let mut out = Vec::new();
    let ff = format!("{f:02}");
    if let Some(b) = &fs.seated {
        out.push(FaceItem { key: ff.clone(), face: f, counter: None, body: b.clone(), tail: None, live: true });
    }
    if let Some(d) = &fs.draft {
        out.push(FaceItem { key: format!("{ff}.draft"), face: f, counter: None, body: d.body.clone(), tail: Some("draft".into()), live: false });
    }
    if let Some(r) = &fs.retired {
        out.push(FaceItem { key: format!("{ff}.retired"), face: f, counter: None, body: r.clone(), tail: Some("retired".into()), live: false });
    }
    if !fs.counters.is_empty() {
        // R9: faces have no sentinels, so no `FF.00` board key; the board is in /page `boards`.
        let _ = (st, page);
        for (nn, c) in &fs.counters {
            out.push(FaceItem { key: format!("{ff}.{nn:02}"), face: f, counter: Some(*nn), body: c.bodies.join("\n\n"), tail: c.tail.as_tail().map(|t| t.to_string()), live: true });
        }
    }
    out
}

pub fn page_items(st: &BookState, page: u16, pg: &PageState) -> Vec<FaceItem> {
    pg.faces.iter().flat_map(|(f, fs)| face_items(st, page, *f, fs)).collect()
}

/// Find full page addresses `DD.SS.BB.PPPP` written in a text (face 08 links).
pub fn page_addrs_in(text: &str) -> Vec<String> {
    let b = text.as_bytes();
    let mut out = Vec::new();
    let shape = [2usize, 2, 2, 4];
    let mut i = 0;
    while i < b.len() {
        let prev_ok = i == 0 || !(b[i - 1].is_ascii_alphanumeric() || b[i - 1] == b'.');
        if prev_ok && b[i].is_ascii_digit() {
            let mut j = i;
            let mut ok = true;
            for (k, w) in shape.iter().enumerate() {
                if j + w > b.len() || !b[j..j + w].iter().all(|c| c.is_ascii_digit()) {
                    ok = false;
                    break;
                }
                j += w;
                if k < 3 {
                    if j < b.len() && b[j] == b'.' {
                        j += 1;
                    } else {
                        ok = false;
                        break;
                    }
                }
            }
            if ok && (j == b.len() || !b[j].is_ascii_digit()) {
                out.push(text[i..j].to_string());
                i = j;
                continue;
            }
        }
        i += 1;
    }
    out
}

fn entry_value(e: &Entry, book: BookId) -> Value {
    let mut v = serde_json::to_value(e).unwrap_or(Value::Null);
    if let Some(m) = v.as_object_mut() {
        m.insert("book".into(), json!(book.to_string()));
    }
    v
}

impl Store {
    /// Bootstrap (kernel-design 7): locate the kernel 00.00.00, check the format
    /// version, refuse unsafe material, load, and report failure without guessing.
    /// Nothing is written during boot; a bad file is left as it is.
    pub fn boot(cfg: Config) -> Result<Store, BootError> {
        let mut found: BTreeMap<BookId, PathBuf> = BTreeMap::new();
        let mut boot = Vec::new();
        let mut warnings: BTreeMap<BookId, Vec<String>> = BTreeMap::new();
        for d in &cfg.dirs {
            let Ok(rd) = std::fs::read_dir(d) else {
                boot.push(json!({"step": "locate", "dir": d.display().to_string(), "note": "folder not found"}));
                continue;
            };
            let mut names: Vec<String> = rd.filter_map(|e| e.ok()).map(|e| e.file_name().to_string_lossy().to_string()).collect();
            names.sort();
            for n in names {
                if let Some(b) = is_book_file(&n) {
                    let p = d.join(&n);
                    if let Some(first) = found.get(&b) {
                        warnings.entry(b).or_default().push(format!("{} is shadowed by {} (first folder wins)", p.display(), first.display()));
                    } else {
                        found.insert(b, p);
                    }
                }
            }
        }
        // 7.1 locate the kernel
        let Some(_kernel_path) = found.get(&BookId::KERNEL).cloned() else {
            return Err(BootError { step: "7.1 locate kernel", detail: format!("no 00.00.00.book in {:?}; the compute will not start without its kernel", cfg.dirs), refused: vec![] });
        };
        let mut world = World::new(cfg.policy.clone());
        let mut logs = BTreeMap::new();
        let mut paths = BTreeMap::new();
        let mut refused = Vec::new();
        // kernel first, then the rest
        let mut order: Vec<BookId> = vec![BookId::KERNEL];
        order.extend(found.keys().copied().filter(|b| *b != BookId::KERNEL));
        for b in order {
            let p = found[&b].clone();
            match load_one(&p, b, &cfg.policy) {
                Ok((lg, st, notes)) => {
                    if b == BookId::KERNEL && !st.has_door() {
                        return Err(BootError { step: "7.5 load kernel", detail: format!("{} has no door 00.00.00.0000.00", p.display()), refused });
                    }
                    if !notes.is_empty() {
                        warnings.entry(b).or_default().extend(notes);
                    }
                    boot.push(json!({"step": "load", "book": b.to_string(), "file": p.display().to_string(), "entries": lg.entries.len()}));
                    world.insert(st);
                    logs.insert(b, lg);
                    paths.insert(b, p);
                }
                Err((step, detail)) => {
                    if b == BookId::KERNEL {
                        return Err(BootError { step, detail: format!("{}: {detail}", p.display()), refused });
                    }
                    refused.push(json!({"book": b.to_string(), "file": p.display().to_string(), "step": step, "detail": detail}));
                }
            }
        }
        let keep = cfg.queue_keep;
        let ids = match &cfg.identities {
            Some(i) => i.clone(),
            None => {
                let p = cfg.write_dir.join(".identities");
                if p.exists() {
                    crate::identity::Identities::load(&p).map_err(|e| BootError { step: "identities", detail: e, refused: refused.clone() })?
                } else {
                    boot.push(json!({"step": "identities", "note": format!("{} not found: reads only, every write is refused", p.display())}));
                    crate::identity::Identities::default()
                }
            }
        };
        let file_len = logs.iter().map(|(b, lg): (&BookId, &BookLog)| (*b, lg.valid_len as u64)).collect();
        let (queue, queue_seq) = load_queue(&cfg.write_dir.join(".queue"), keep);
        Ok(Store { cfg, world, logs, paths, warnings, refused, queue, queue_seq, boot, ids, file_len })
    }

    fn st(&self, b: BookId) -> Option<&BookState> {
        self.world.get(b)
    }

    // ---------------- reads ----------------

    pub fn health(&self, pending: usize) -> Answer {
        (200, json!({
            "ok": true, "books": self.world.books.len(), "kernel": "00.00.00", "format": FORMAT_VERSION,
            "from": self.cfg.dirs.iter().map(|d| d.display().to_string()).collect::<Vec<_>>().join(", "),
            "refused": self.refused, "pending": pending,
        }))
    }

    pub fn books(&self) -> Answer {
        let v: Vec<Value> = self.world.books.values().map(|st| json!({"address": st.book.to_string(), "title": st.title(), "pages": st.pages.len()})).collect();
        (200, Value::Array(v))
    }

    pub fn book(&self, arg: &str) -> Answer {
        let Ok(b) = BookId::parse(arg) else { return bad(format!("`{arg}` is not a book address DD.SS.BB")) };
        let Some(st) = self.st(b) else { return missing(format!("no book {arg}"), json!({})) };
        let pages: Vec<Value> = st
            .pages
            .iter()
            .map(|(p, pg)| {
                let faces: Vec<String> = pg.faces.iter().filter(|(_, f)| f.is_present() || f.retired.is_some()).map(|(f, _)| format!("{f:02}")).collect();
                json!({"page": format!("{p:04}"), "title": pg.title(), "state": pg.tail().as_tail().map(|t| t.to_string()), "faces": faces})
            })
            .collect();
        (200, json!({"address": b.to_string(), "title": st.title(), "pages": pages, "warnings": self.warnings.get(&b).cloned().unwrap_or_default()}))
    }

    /// Last log entry for each (page, face, counter) slot of a book.
    fn meta(&self, b: BookId) -> BTreeMap<(u16, u8, Option<u8>), &Entry> {
        let mut m = BTreeMap::new();
        if let Some(lg) = self.logs.get(&b) {
            for e in &lg.entries {
                if let Ok(p) = Address::parse_full_page(&e.addr) {
                    if let Some(fp) = &p.face {
                        m.insert((p.page, fp.face, fp.counter), e);
                    }
                }
            }
        }
        m
    }

    fn parse_page(&self, arg: &str) -> Result<(PageAddr, BookId), Answer> {
        let p = Address::parse_full_page(arg).map_err(|e| err_json(&e))?;
        if p.face.is_some() {
            return Err(bad(format!("`{arg}` names a face; /page takes DD.SS.BB.PPPP")));
        }
        if let Err(e) = self.world.check_title(&p) {
            return Err(err_json(&e));
        }
        let b = p.book_id().unwrap();
        Ok((p.page_only(), b))
    }

    /// The page as the reader shows it: every local face in every state, plus
    /// live faces inherited along book -> shelf -> desk -> kernel.
    pub fn page_view(&self, p: &PageAddr, asked: BookId) -> Option<Value> {
        let mut faces = Map::new();
        let mut inherited = Vec::new();
        let mut filled: BTreeSet<u8> = BTreeSet::new();
        for b in asked.lookup_chain() {
            let Some(st) = self.st(b) else { continue };
            let Some(pg) = st.page(p.page) else { continue };
            let meta = self.meta(b);
            let here = filled.clone();
            for it in page_items(st, p.page, pg) {
                // R5: the first book in the chain holding a face wins; there a seated face
                // beats its draft, and a draft alone is found and inherited (state draft).
                if here.contains(&it.face) || faces.contains_key(&it.key) {
                    continue;
                }
                if b != asked {
                    let fs = pg.face(it.face).unwrap();
                    let keep = match it.tail.as_deref() {
                        Some("retired") if it.counter.is_none() => false,
                        Some("draft") if it.counter.is_none() => fs.seated.is_none(),
                        _ => true,
                    };
                    if !keep {
                        continue;
                    }
                }
                filled.insert(it.face);
                let source = format!("{b}.{:04}.{}", p.page, it.key);
                let mut fv = json!({"body": it.body, "source": source, "resolved_from": level(asked, b)});
                if let Some(t) = &it.tail {
                    fv["tail"] = json!(t);
                }
                let mk = (p.page, it.face, it.counter);
                if let Some(e) = meta.get(&mk) {
                    fv["n"] = json!(e.n);
                    fv["by"] = json!(e.by);
                    fv["at"] = json!(e.at);
                }
                if it.tail.as_deref() == Some("draft") && it.counter.is_none() {
                    fv["state"] = json!("draft");
                    if let Some(d) = pg.face(it.face).and_then(|f| f.draft.as_ref()) {
                        let open: Vec<Value> = d.notes.iter().filter(|n| !n.struck).map(|n| json!({"n": n.n, "by": n.by, "text": n.text})).collect();
                        fv["why_draft"] = json!({"opened_by_entry": d.n, "has_seated": pg.face(it.face).map(|f| f.seated.is_some()).unwrap_or(false), "open_notes": open, "merged_notes": d.notes.iter().filter(|n| n.struck).count()});
                        // R5 follow-up: the `reason` the opening entry carries, same as /face (DraftWhy.reason)
                        if let Some(r) = &d.reason {
                            fv["why_draft"]["reason"] = json!(r);
                        }
                    }
                } else if it.counter.is_none() && it.tail.is_none() {
                    fv["state"] = json!("seated");
                }
                if b != asked {
                    inherited.push(source.clone());
                }
                faces.insert(it.key, fv);
            }
        }
        if faces.is_empty() {
            return None;
        }
        let title = asked.lookup_chain().into_iter().find_map(|b| self.st(b).and_then(|s| s.page(p.page)).and_then(|pg| pg.title()));
        // the derived board of each counted face (A4.4), listed here, not as a face key `FF.00` (R9)
        let mut boards = Map::new();
        for (k, v) in &faces {
            if let Some((ff, nn)) = k.split_once('.') {
                if nn.len() == 2 && nn.bytes().all(|b| b.is_ascii_digit()) {
                    let e = boards.entry(ff.to_string()).or_insert_with(|| json!([]));
                    e.as_array_mut().unwrap().push(json!({"counter": nn, "tail": v.get("tail").cloned().unwrap_or(json!("closed"))}));
                }
            }
        }
        Some(json!({"address": p.to_string(), "title": title, "faces": faces, "inherited": inherited, "boards": boards}))
    }

    pub fn page(&self, arg: &str) -> Answer {
        let (p, b) = match self.parse_page(arg) {
            Ok(x) => x,
            Err(a) => return a,
        };
        match self.page_view(&p, b) {
            Some(v) => (200, v),
            None => missing(format!("no page {arg} in book, shelf, desk or kernel"), json!({"address": arg})),
        }
    }

    fn trace_json(&self, p: &PageAddr, r: &Resolution) -> Vec<Value> {
        let asked = p.book_id().unwrap();
        let chain = if p.face.as_ref().and_then(|f| f.tail).is_some() { vec![asked] } else { asked.lookup_chain() };
        r.trace
            .iter()
            .enumerate()
            .map(|(i, s)| {
                let mut v = serde_json::to_value(s).unwrap();
                if let Some(b) = chain.get(i) {
                    v["level"] = json!(level(asked, *b));
                    v["book_exists"] = json!(self.st(*b).is_some());
                }
                v
            })
            .collect()
    }

    fn resolve_face(&self, arg: &str) -> Result<(PageAddr, Resolution), Answer> {
        let p = Address::parse_full_page(arg).map_err(|e| err_json(&e))?;
        let p = if p.face.is_none() { p.with_face(FacePart::face(0)) } else { p };
        let r = self.world.resolve(&p).map_err(|e| err_json(&e))?;
        Ok((p, r))
    }

    pub fn resolve(&self, arg: &str) -> Answer {
        match self.resolve_face(arg) {
            Ok((p, r)) => (200, Value::Array(self.trace_json(&p, &r))),
            Err(a) => a,
        }
    }

    pub fn face(&self, arg: &str) -> Answer {
        let (p, r) = match self.resolve_face(arg) {
            Ok(x) => x,
            Err(a) => return a,
        };
        let trace = self.trace_json(&p, &r);
        let Some(found) = &r.found else {
            return missing(format!("{arg} was not found in book, shelf, desk or kernel; elevate, never guess"), json!({"address": arg, "resolved_from": "missing", "trace": trace}));
        };
        let (mut body, tail) = match found {
            Found::Face { body } => (body.clone(), None),
            Found::Draft { body } => (body.clone(), Some("draft".to_string())),
            Found::Retired { body } => (body.clone(), Some("retired".to_string())),
            Found::Counter { tail, bodies } => (bodies.join("\n\n"), tail.as_tail().map(|t| t.to_string())),
            Found::Board { lines } => (lines.iter().map(|l| format!("{:02}: {}", l.counter, l.tail.board_word())).collect::<Vec<_>>().join("\n"), None),
        };
        let fp = p.face.clone().unwrap();
        if let Some(key) = &fp.card {
            match parse_face(&body).ok().and_then(|d| d.card(key).cloned()) {
                Some(c) => {
                    let mut t = format!("## {}", c.heading);
                    for (k, v) in &c.fields {
                        t.push_str(&format!("\n{k}: {v}"));
                    }
                    if !c.body.is_empty() {
                        t.push_str("\n\n");
                        t.push_str(&c.body);
                    }
                    body = t;
                }
                None => return missing(format!("face found at {} but it has no card `{key}`", r.source.clone().unwrap_or_default()), json!({"address": arg, "resolved_from": "missing", "trace": trace})),
            }
        }
        let src = r.source.clone().unwrap_or_default();
        let mut v = json!({"address": arg, "body": body, "source": src, "resolved_from": r.origin.as_str(), "state": r.state, "trace": trace});
        if let Some(w) = &r.why_draft {
            v["why_draft"] = serde_json::to_value(w).unwrap_or(Value::Null);
        }
        if let Some(t) = tail {
            v["tail"] = json!(t);
        }
        if let Ok(sp) = Address::parse_full_page(&src) {
            if let Some(b) = sp.book_id() {
                if let Some(e) = self.meta(b).get(&(sp.page, fp.face, fp.counter.filter(|c| *c != 0))) {
                    v["n"] = json!(e.n);
                    v["by"] = json!(e.by);
                    v["at"] = json!(e.at);
                }
            }
        }
        (200, v)
    }

    pub fn history(&self, arg: &str) -> Answer {
        // Parse first (TRIAL-X #10): a book `DD.SS.BB`, or a full page/face address; a title is a label and is dropped.
        let key = match BookId::parse(arg) {
            Ok(b) => b.to_string(),
            Err(_) => match Address::parse_full_page(arg) {
                Ok(p) => {
                    let mut k = p.page_only().to_string();
                    if let Some(fp) = &p.face {
                        k = p.page_only().with_face(FacePart { card: None, brand: None, ..fp.clone() }).to_string();
                    }
                    k
                }
                Err(e) => return err_json(&e),
            },
        };
        let arg = key.as_str();
        let pre = format!("{arg}.");
        let mut out: Vec<(String, String, u64, Value)> = Vec::new();
        for (b, lg) in &self.logs {
            for e in &lg.entries {
                if e.addr == arg || e.addr.starts_with(&pre) {
                    out.push((e.at.clone(), b.to_string(), e.n, entry_value(e, *b)));
                }
            }
        }
        out.sort_by(|a, b| (&a.0, &a.1, a.2).cmp(&(&b.0, &b.1, b.2)));
        (200, Value::Array(out.into_iter().map(|x| x.3).collect()))
    }

    fn face08_texts(&self, view: &Value) -> Vec<String> {
        view["faces"].as_object().map(|m| m.iter().filter(|(k, _)| k.starts_with("08") && !k.ends_with(".retired")).filter_map(|(_, v)| v["body"].as_str().map(|s| s.to_string())).collect()).unwrap_or_default()
    }

    fn view_of(&self, page: &str) -> Option<Value> {
        let p = Address::parse_full_page(page).ok()?;
        self.page_view(&p.page_only(), p.book_id()?)
    }

    /// Face 08 links (seqAddr 7): forward, back (derived), missing (7.8), one-way.
    pub fn links(&self, arg: &str) -> Answer {
        let (p, _) = match self.parse_page(arg) {
            Ok(x) => x,
            Err(a) => return a,
        };
        let me = p.to_string();
        let mut forward: Vec<String> = Vec::new();
        if let Some(v) = self.view_of(&me) {
            for t in self.face08_texts(&v) {
                for a in page_addrs_in(&t) {
                    if a != me && !forward.contains(&a) {
                        forward.push(a);
                    }
                }
            }
        }
        let mut back = BTreeSet::new();
        for st in self.world.books.values() {
            for (pn, pg) in &st.pages {
                let Some(fs) = pg.face(8) else { continue };
                let from = format!("{}.{pn:04}", st.book);
                if from == me {
                    continue;
                }
                if face_items(st, *pn, 8, fs).iter().filter(|it| it.tail.as_deref() != Some("retired")).any(|it| page_addrs_in(&it.body).contains(&me)) {
                    back.insert(from);
                }
            }
        }
        let missing: Vec<String> = forward.iter().filter(|a| self.view_of(a).is_none()).cloned().collect();
        let one_way: Vec<String> = forward
            .iter()
            .filter(|a| match self.view_of(a) {
                Some(v) => !self.face08_texts(&v).iter().any(|t| page_addrs_in(t).contains(&me)),
                None => false,
            })
            .cloned()
            .collect();
        (200, json!({"address": me, "forward": forward, "back": back.into_iter().collect::<Vec<_>>(), "missing": missing, "missing_axiom": "7.8", "one_way": one_way}))
    }

    /// Word -> brand cards (brands.md): dictionary page 0012 face 03, any section,
    /// `word.NNN: address` lines, `default:`. With `book`, only that book's lookup chain.
    pub fn brands(&self, q: &str, book: Option<&str>) -> Answer {
        let word = q.trim();
        if word.is_empty() {
            return (200, json!([]));
        }
        let Ok(key) = title_form(&word.to_lowercase()) else { return (200, json!([])) };
        let books: Vec<BookId> = match book {
            Some(s) => match BookId::parse(s) {
                Ok(b) => b.lookup_chain(),
                Err(e) => return err_json(&e),
            },
            // TRIAL-X #13: no book named -> the configured reader book's chain, else the kernel only.
            None => self.cfg.default_book.map(|b| b.lookup_chain()).unwrap_or_else(|| vec![BookId::KERNEL]),
        };
        let mut out = Vec::new();
        for b in books {
            let Some(st) = self.st(b) else { continue };
            let Some(fs) = st.face(12, 3) else { continue };
            for it in face_items(st, 12, 3, fs) {
                if it.counter == Some(0) {
                    continue;
                }
                let Ok(doc) = parse_face(&it.body) else { continue };
                for c in doc.cards.iter().filter(|c| c.key == key) {
                    let default = c.field("default").map(|s| s.trim().to_string());
                    // brand lines `word.NNN: address` (brands.md); the core card parser keeps
                    // dotted names in the body, so both fields and body lines are read.
                    let mut lines: Vec<(String, String)> = c.fields.clone();
                    for l in c.body.lines() {
                        if let Some((k, v)) = l.split_once(':') {
                            lines.push((k.trim().to_string(), v.trim().to_string()));
                        }
                    }
                    for (k, v) in &lines {
                        let Some((_, num)) = k.rsplit_once('.') else { continue };
                        if num.len() != 3 || !num.chars().all(|ch| ch.is_ascii_digit()) {
                            continue;
                        }
                        out.push(self.brand_entry(c.heading.as_str(), word, k, v.trim(), default.as_deref(), &format!("{b}.0012.{}", it.key), it.tail.clone()));
                    }
                }
            }
        }
        (200, Value::Array(out))
    }

    #[allow(clippy::too_many_arguments)]
    fn brand_entry(&self, heading: &str, typed: &str, brand_id: &str, target: &str, default: Option<&str>, dictionary: &str, dict_tail: Option<String>) -> Value {
        let mut card = None;
        let mut page = None;
        if let Ok(tp) = Address::parse_full_page(target) {
            page = Some(tp.page_only().to_string());
            if let (Some(b), Some(fp)) = (tp.book_id(), tp.face.as_ref()) {
                let ck = fp.card.clone().unwrap_or_else(|| heading.to_lowercase());
                if let Some(fs) = self.st(b).and_then(|s| s.face(tp.page, fp.face)) {
                    for t in [fs.seated.as_deref(), fs.draft.as_ref().map(|d| d.body.as_str())].into_iter().flatten() {
                        if let Some(c) = parse_face(t).ok().and_then(|d| d.card(&ck).cloned()) {
                            card = Some(c);
                            break;
                        }
                    }
                }
            }
        }
        let forms: Vec<String> = card.as_ref().and_then(|c| c.field("forms")).map(|f| f.split(',').map(|s| s.trim().to_string()).filter(|s| !s.is_empty()).collect()).unwrap_or_default();
        json!({
            "word": heading, "brand": target, "brand_id": brand_id, "dictionary": dictionary, "dictionary_tail": dict_tail,
            "is_default": default == Some(brand_id),
            "title": card.as_ref().map(|c| c.heading.clone()),
            "why": card.as_ref().and_then(|c| c.field("means").map(|s| s.to_string())),
            "meters": card.as_ref().and_then(|c| c.field("meters").map(|s| s.to_string())),
            "forms": forms, "exact_form": if forms.is_empty() { Value::Null } else { json!(forms.iter().any(|f| f == typed)) },
            "page": page, "missing": card.is_none(),
        })
    }

    /// Cards matched by title across every face, every state, every book (C2).
    pub fn cards(&self, title: &str) -> Answer {
        let Ok(key) = title_form(&title.to_lowercase()) else { return (200, json!([])) };
        let mut out = Vec::new();
        for st in self.world.books.values() {
            for (pn, pg) in &st.pages {
                for it in page_items(st, *pn, pg) {
                    if it.counter == Some(0) || it.face == 0 {
                        continue;
                    }
                    let Ok(doc) = parse_face(&it.body) else { continue };
                    for c in doc.cards.iter().filter(|c| c.key == key) {
                        let face = format!("{}.{pn:04}.{}", st.book, it.key);
                        let fields: Map<String, Value> = c.fields.iter().map(|(k, v)| (k.clone(), json!(v))).collect();
                        out.push(json!({"address": format!("{face}.{}", c.key), "face": face, "face_no": format!("{:02}", it.face), "page_title": pg.title(), "title": c.heading, "key": c.key, "fields": fields, "body": c.body, "tail": it.tail}));
                    }
                }
            }
        }
        (200, Value::Array(out))
    }

    pub fn queue_view(&self, pending: usize) -> Answer {
        (200, json!({"pending": pending, "serialized": true, "proposals": self.queue.iter().rev().cloned().collect::<Vec<_>>()}))
    }

    // ---------------- the one write path ----------------

    /// Validate one proposal against the current world and, if approved,
    /// append it to its book file and adopt the new state. All or nothing.
    /// `by` comes from the writer's token, never from the body (7 identity design).
    pub fn propose(&mut self, mut raw: Value, by: &str) -> Answer {
        if let Some(m) = raw.as_object_mut() {
            m.insert("by".into(), json!(by));
        }
        self.queue_seq += 1;
        let qid = format!("q{}", self.queue_seq);
        let at = log::now_utc();
        let (code, mut body) = self.propose_inner(&raw, &at);
        body["queue_id"] = json!(qid);
        let rec = json!({
            "id": qid, "at": at, "by": by, "ops": raw.get("ops").and_then(|o| o.as_array()).map(|a| a.len()).unwrap_or(0),
            "book": body.get("book"), "status": body.get("status"), "reasons": body.get("reasons"), "entries": body.get("entries"), "http": code,
        });
        // the queue record is kept on disk so ids never repeat after a restart (TRIAL-X #11)
        let qp = self.cfg.write_dir.join(".queue");
        if let Ok(mut f) = std::fs::OpenOptions::new().create(true).append(true).open(&qp) {
            use std::io::Write;
            let _ = f.write_all(format!("{rec}\n").as_bytes());
        }
        if self.queue.len() >= self.cfg.queue_keep.max(1) {
            self.queue.pop_front();
        }
        self.queue.push_back(rec);
        (code, body)
    }

    /// POST /propose with a `.seq` page (CONTRACT addendum, SEQPAGE lane): import it
    /// against the book, then send its proposal through the same queue.
    pub fn propose_seq(&mut self, text: &str, by: &str) -> Answer {
        let log = seqpage::parse(text).ok().and_then(|sp| self.logs.get(&sp.page.book).cloned());
        match seqpage::import(text, log.as_ref(), by) {
            Err(rep) => (422, serde_json::to_value(&rep).unwrap_or(Value::Null)),
            Ok(imp) => {
                let findings = serde_json::to_value(&imp.findings).unwrap_or(Value::Null);
                let raw = serde_json::to_value(&imp.proposal).unwrap_or(Value::Null);
                let (c, mut v) = self.propose(raw, by);
                v["seq_findings"] = findings;
                v["page"] = json!(imp.page);
                (c, v)
            }
        }
    }

    /// GET /page.seq?addr= : the page as a `.seq` view (text), or an error answer.
    pub fn page_seq(&self, addr: &str) -> Result<(String, String), Answer> {
        let pid = seqpage::PageId::parse(addr).map_err(|e| (400, json!({"error": "invalid", "detail": e})))?;
        let Some(log) = self.logs.get(&pid.book) else { return Err(missing(format!("no book {}", pid.book), json!({}))) };
        let text = seqpage::export(log, pid).map_err(|e| {
            let code = if e.code == "missing" { 404 } else { 422 };
            (code, json!({"error": e.code, "axiom": e.axiom, "rule": e.rule, "detail": e.detail}))
        })?;
        let title = self.world.get(pid.book).and_then(|s| s.page(pid.page)).and_then(|p| p.title());
        Ok((text, seqpage::file_name(pid, title.as_deref())))
    }

    /// POST /check.seq: the import report, nothing written.
    pub fn check_seq(&self, text: &str) -> Answer {
        let log = seqpage::parse(text).ok().and_then(|sp| self.logs.get(&sp.page.book));
        (200, serde_json::to_value(seqpage::check_text(text, None, log)).unwrap_or(Value::Null))
    }

    /// The face maker for a seating op: the author of the draft being promoted, else the proposer.
    fn maker_of(&self, r: &seqaddr_core::OpRequest, by: &str) -> String {
        if r.op == Some(Op::Promote) {
            if let Ok(p) = Address::parse_full_page(&r.addr) {
                if let (Some(b), Some(fp)) = (p.book_id(), p.face.as_ref()) {
                    if let Some(d) = self.world.get(b).and_then(|st| st.face(p.page, fp.face)).and_then(|f| f.draft.as_ref()) {
                        if let Some(e) = self.logs.get(&b).and_then(|lg| lg.entries.iter().find(|e| e.n == d.n)) {
                            return e.by.clone();
                        }
                    }
                }
            }
        }
        by.to_string()
    }

    /// R2 trial reference: `docs/trial/FILE[#anchor]`, the file exists under the
    /// repo, and its author (its first `Lane NAME` or `author: NAME` line) is not the maker.
    fn check_trial(&self, trial: &str, maker: &str, by: &str) -> Result<(), String> {
        let path = trial.split('#').next().unwrap_or("");
        let ok_shape = path.starts_with("docs/trial/") && path.ends_with(".md") && !path.contains("..") && path.bytes().all(|b| b.is_ascii_alphanumeric() || b"/._-".contains(&b));
        if !ok_shape {
            return Err(format!("trial `{trial}` must name a file docs/trial/NAME.md (optionally #anchor)"));
        }
        let full = self.cfg.repo_root.join(path);
        let text = std::fs::read_to_string(&full).map_err(|_| format!("trial file {path} does not exist"))?;
        let author = text.lines().find_map(|l| {
            let l = l.trim();
            l.strip_prefix("Lane ").or_else(|| l.strip_prefix("author: ")).map(|r| r.split(|c: char| c == ',' || c.is_whitespace()).next().unwrap_or("").to_ascii_lowercase())
        });
        let Some(author) = author.filter(|a| !a.is_empty()) else { return Err(format!("trial file {path} names no author (`Lane NAME` or `author: NAME`)")) };
        let maker = maker.to_ascii_lowercase();
        if author == maker || author == by.to_ascii_lowercase() && maker == by.to_ascii_lowercase() {
            return Err(format!("trial {path} is by `{author}`, the face's maker; R2 needs a hostile trial from a different view"));
        }
        Ok(())
    }

    /// Does this op seat a face? The core's rule plus a draft moved to bare by `tail`.
    fn seats(r: &seqaddr_core::OpRequest) -> bool {
        if seqaddr_core::validate::seats_a_face(r) {
            return true;
        }
        if r.op == Some(Op::Tail) && r.from.as_deref() == Some("draft") && r.to.as_deref().map(|t| t.is_empty()).unwrap_or(true) {
            if let Ok(p) = Address::parse_full_page(&r.addr) {
                return p.face.map(|f| f.counter.is_none()).unwrap_or(false);
            }
        }
        false
    }

    fn propose_inner(&mut self, raw: &Value, at: &str) -> Answer {
        let rejected = |code: u16, err: &str, axiom: Option<&str>, reasons: Value, detail: String| -> Answer {
            (code, json!({"status": "rejected", "error": err, "axiom": axiom, "detail": detail, "reasons": reasons, "findings": [], "entries": []}))
        };
        let proposal: Proposal = match serde_json::from_value(raw.clone()) {
            Ok(p) => p,
            Err(e) => return rejected(400, "invalid", None, json!([{"code": "invalid", "rule": "CONTRACT", "detail": e.to_string()}]), format!("not a proposal {{ops}}: {e}")),
        };
        // R2 on every seating path, checked before the core (403, axiom 1: authority).
        let mut gate = Vec::new();
        for (i, r) in proposal.ops.iter().enumerate() {
            let g = &self.cfg.approval;
            let ab = r.approved_by.as_deref();
            let trial = r.trial.as_deref().map(str::trim).filter(|t| !t.is_empty());
            let mut fail = |detail: String| gate.push(json!({"code": "rejected", "rule": "R2", "axiom": "1", "op": i, "detail": detail}));
            match ab {
                None if Self::seats(r) && g.require => fail("seating a face needs `approved_by`: `director` (the Director's own token) or `build-stage (R2)` with a `trial` (drafting.md:20, R2)".into()),
                None => {}
                Some("director") => {
                    if !g.director_names.iter().any(|n| n == &proposal.by) {
                        fail(format!("only the Director's token may record `approved_by: director`; this writer is `{}`", proposal.by));
                    }
                }
                Some("build-stage (R2)") => {
                    if !g.allow_build_stage_r2 {
                        fail("build-stage (R2) approval is switched off on this compute".into());
                    } else if let Some(t) = trial {
                        let maker = self.maker_of(r, &proposal.by);
                        if let Err(e) = self.check_trial(t, &maker, &proposal.by) {
                            fail(e);
                        }
                    } else {
                        fail("`build-stage (R2)` needs a `trial` reference to a hostile trial file".into());
                    }
                }
                Some(other) => fail(format!("approval `{other}` is not known; use `director` or `build-stage (R2)` (exact words)")),
            }
        }
        if !gate.is_empty() {
            return rejected(403, "authority", Some("1"), Value::Array(gate), "seating needs a granted approval (Axioms: authority is granted, never claimed; R2)".into());
        }
        let out = validate(&self.world, &proposal, at);
        let book = proposal.ops.first().and_then(|r| Address::parse_full_page(&r.addr).ok()).and_then(|p| p.book_id());
        let mut body = serde_json::to_value(&out).unwrap();
        body["book"] = json!(book.map(|b| b.to_string()));
        if !out.approved() {
            let first = out.reasons.first();
            let (code, err) = match out.first_error_code() {
                Some("conflict") => (409, "conflict"),
                Some("missing") => (404, "missing"),
                Some("invalid") => (422, "invalid"),
                Some("elevate") => (409, "elevate"),
                _ => (422, "rejected"),
            };
            body["error"] = json!(err);
            body["axiom"] = json!(first.and_then(|r| r.axiom.clone()));
            body["detail"] = json!(first.map(|r| r.detail.clone()));
            return (code, body);
        }
        let book = book.expect("approved proposals name a book");
        let entries = out.entries.clone();
        if let Err(e) = self.append(book, &entries) {
            // Nothing adopted: memory keeps the prior state (kernel-design 7.6).
            return (500, json!({"status": "rejected", "error": "io", "detail": e, "reasons": [], "entries": []}));
        }
        let lg = self.logs.entry(book).or_insert_with(|| BookLog::new(book));
        lg.entries.extend(entries);
        self.world.insert(out.state.clone().unwrap());
        (200, body)
    }

    /// Append whole lines at the known end of the book file and fsync (TRIAL-X #15):
    /// no re-read of the book. A partly written tail left by a crash is cut first;
    /// a file shorter than expected was changed outside the compute and is refused.
    fn append(&mut self, book: BookId, entries: &[Entry]) -> Result<(), String> {
        use std::io::{Seek, SeekFrom, Write};
        for e in entries {
            e.check_plain().map_err(|e| e.detail())?;
        }
        let path = match self.paths.get(&book) {
            Some(p) => p.clone(),
            None => {
                let p = self.cfg.write_dir.join(book.file_name());
                std::fs::create_dir_all(&self.cfg.write_dir).map_err(|e| e.to_string())?;
                log::file::create(&p, book).map_err(|e| format!("could not create {}: {}", p.display(), e.detail()))?;
                let len = std::fs::metadata(&p).map_err(|e| e.to_string())?.len();
                self.paths.insert(book, p.clone());
                self.file_len.insert(book, len);
                p
            }
        };
        let want = *self.file_len.get(&book).ok_or("book length unknown")?;
        let mut f = std::fs::OpenOptions::new().write(true).open(&path).map_err(|e| e.to_string())?;
        let have = f.metadata().map_err(|e| e.to_string())?.len();
        if have < want {
            return Err(format!("{} is shorter than the compute wrote it ({have} < {want} bytes); changed outside the compute, refusing to write", path.display()));
        }
        if have > want {
            f.set_len(want).map_err(|e| e.to_string())?; // cut a partial tail (format 3.1)
        }
        let mut buf = String::new();
        if want > 0 {
            // a whole last line with its newline cut off still counts (format 3.1): end it first
            use std::io::Read;
            let mut last = [0u8; 1];
            f.seek(SeekFrom::Start(want - 1)).map_err(|e| e.to_string())?;
            let mut r = std::fs::File::open(&path).map_err(|e| e.to_string())?;
            r.seek(SeekFrom::Start(want - 1)).map_err(|e| e.to_string())?;
            r.read_exact(&mut last).map_err(|e| e.to_string())?;
            if last[0] != b'\n' {
                buf.push('\n');
            }
        }
        for e in entries {
            buf.push_str(&e.to_line());
            buf.push('\n');
        }
        f.seek(SeekFrom::Start(want)).map_err(|e| e.to_string())?;
        f.write_all(buf.as_bytes()).map_err(|e| e.to_string())?;
        f.sync_data().map_err(|e| e.to_string())?;
        self.file_len.insert(book, want + buf.len() as u64);
        Ok(())
    }

    /// POST /close {addr, outcome}: only the compute closes a review (workflow-loop.003 6;
    /// core `compute_only_steps`). The compute closes it for the counter's reviewer (7).
    pub fn close(&mut self, raw: &Value, by: &str) -> Answer {
        let (Some(addr), Some(outcome)) = (raw.get("addr").and_then(|v| v.as_str()), raw.get("outcome").and_then(|v| v.as_str())) else {
            return (400, json!({"error": "invalid", "detail": "send {\"addr\": counter address, \"outcome\": passed|failed|blocked|needs-authority}"}));
        };
        let p = match Address::parse_full_page(addr) {
            Ok(p) => p,
            Err(e) => return err_json(&e),
        };
        let (Some(b), Some(fp)) = (p.book_id(), p.face.as_ref()) else { return bad("name a counter DD.SS.BB.PPPP.FF.NN") };
        let Some(c) = fp.counter.and_then(|nn| self.world.get(b).and_then(|st| st.counter(p.page, fp.face, nn))) else {
            return missing(format!("no counter {addr}"), json!({}));
        };
        if c.reviewer.as_deref() != Some(by) {
            return (403, json!({"status": "rejected", "error": "authority", "axiom": "1", "detail": format!("only the reviewer ({:?}) may ask the compute to close {addr}", c.reviewer)}));
        }
        let name = self.cfg.policy.compute_name.clone();
        self.propose(json!({"ops": [{"op": "tail", "addr": addr, "from": "review", "outcome": outcome}], "for": by}), &name)
    }
}

fn load_queue(path: &Path, keep: usize) -> (VecDeque<Value>, u64) {
    let mut q = VecDeque::new();
    let mut seq = 0;
    if let Ok(text) = std::fs::read_to_string(path) {
        for l in text.lines() {
            let Ok(v) = serde_json::from_str::<Value>(l) else { continue };
            if let Some(n) = v["id"].as_str().and_then(|s| s.strip_prefix('q')).and_then(|s| s.parse::<u64>().ok()) {
                seq = seq.max(n);
            }
            if q.len() >= keep.max(1) {
                q.pop_front();
            }
            q.push_back(v);
        }
    }
    (q, seq)
}

type LoadErr = (&'static str, String);

fn load_one(p: &Path, b: BookId, policy: &Policy) -> Result<(BookLog, BookState, Vec<String>), LoadErr> {
    let text = std::fs::read_to_string(p).map_err(|e| ("7.2 open", e.to_string()))?;
    let first = text.lines().next().unwrap_or("");
    let hv: Value = serde_json::from_str(first).map_err(|e| ("7.2 header", format!("line 1 is not a header: {e}")))?;
    match hv.get("seqbook").and_then(|v| v.as_u64()) {
        Some(v) if v == FORMAT_VERSION as u64 => {}
        Some(v) => return Err(("7.2 version", format!("seqbook version {v} is not supported (this compute reads {FORMAT_VERSION})"))),
        None => return Err(("7.2 header", "line 1 has no seqbook version".into())),
    }
    let lg = BookLog::parse(&text).map_err(|e| ("7.4 integrity", e.detail()))?;
    let hb = lg.book().map_err(|e| ("7.3 address", e.detail()))?;
    if hb != b {
        return Err(("7.3 address", format!("header says {hb} but the file is named {b}")));
    }
    let st = BookState::replay(&lg, policy).map_err(|e| ("7.4 integrity", format!("replay failed: {}", e.detail())))?;
    let mut notes = Vec::new();
    if lg.dropped_partial {
        notes.push("a partly written last line was dropped on load (format 3.1); it is cut off before the next write".into());
    }
    Ok((lg, st, notes))
}
