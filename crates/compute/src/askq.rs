//! /ask and /ask/link (Director ruling R11): gather question cards and brand
//! cards from the books, hand them to the `ask` crate, and fill each piece with
//! the card it points at (found by the R5 resolver: drafts count).

use crate::store::{Answer, Store};
use seqaddr_core::addr::{Address, BookId};
use seqaddr_core::cards::{parse_face, title_form, Card};
use seqaddr_core::state::FaceState;
use serde_json::{json, Map, Value};

fn split_forms(v: Option<&str>) -> Vec<String> {
    v.map(|f| f.split(',').map(|s| s.trim().to_string()).filter(|s| !s.is_empty()).collect()).unwrap_or_default()
}

/// Seated wins over its draft; a draft alone counts (R5).
fn face_text(fs: &FaceState) -> Option<(&str, &'static str)> {
    fs.seated.as_deref().map(|s| (s, "seated")).or_else(|| fs.draft.as_ref().map(|d| (d.body.as_str(), "draft")))
}

fn card_json(c: &Card, address: &str, state: &str) -> Value {
    let fields: Map<String, Value> = c.fields.iter().map(|(k, v)| (k.clone(), json!(v))).collect();
    json!({"address": address, "title": c.heading, "key": c.key, "fields": fields, "body": c.body, "state": state})
}

impl Store {
    fn ask_books(&self, book: Option<BookId>) -> Vec<BookId> {
        match book.or(self.cfg.default_book) {
            Some(b) => b.lookup_chain(),
            None => vec![BookId::KERNEL],
        }
    }

    /// Question cards (type: question) on the common-questions page, nearest book first; a nearer card with the same key wins.
    pub fn question_cards(&self, books: &[BookId]) -> Vec<ask::QuestionCard> {
        let mut out: Vec<ask::QuestionCard> = Vec::new();
        let pg = self.cfg.ask_page;
        for b in books {
            let Some(st) = self.world.get(*b) else { continue };
            let Some(page) = st.page(pg) else { continue };
            for (f, fs) in &page.faces {
                let Some((text, state)) = face_text(fs) else { continue };
                let Ok(doc) = parse_face(text) else { continue };
                for c in doc.cards.iter().filter(|c| c.field("type") == Some("question")) {
                    if out.iter().any(|q| q.address.ends_with(&format!(".{}", c.key))) {
                        continue;
                    }
                    let mut forms = vec![c.heading.clone()];
                    forms.extend(split_forms(c.field("forms")));
                    let answer = c.field("answer").map(|s| s.trim().to_string()).filter(|s| !s.is_empty() && s != "7");
                    out.push(ask::QuestionCard {
                        address: format!("{b}.{pg:04}.{f:02}.{}", c.key),
                        title: c.heading.clone(),
                        forms,
                        hole: if answer.is_none() { Some(c.field("hole").unwrap_or("nothing answers this question yet (7)").to_string()) } else { None },
                        answer,
                        state: Some(state.into()),
                    });
                }
            }
        }
        out
    }

    /// Brand cards (type: brand) on any face of the chain's books.
    pub fn brand_cards(&self, books: &[BookId]) -> Vec<ask::BrandCard> {
        let mut out = Vec::new();
        for b in books {
            let Some(st) = self.world.get(*b) else { continue };
            for (pn, page) in &st.pages {
                for (f, fs) in &page.faces {
                    let Some((text, state)) = face_text(fs) else { continue };
                    let Ok(doc) = parse_face(text) else { continue };
                    for c in doc.cards.iter().filter(|c| c.field("type") == Some("brand")) {
                        out.push(ask::BrandCard { address: format!("{b}.{pn:04}.{f:02}.{}", c.key), title: c.heading.clone(), forms: split_forms(c.field("forms")), means: c.field("means").map(|s| s.to_string()), state: Some(state.into()) });
                    }
                }
            }
        }
        out
    }

    /// The card a piece points at, through the resolver (R5: a draft is found, and says so).
    fn target_card(&self, addr: &str) -> Value {
        let Ok(p) = Address::parse_full_page(addr) else { return json!({"address": addr, "missing": true, "why": "not a full card address"}) };
        let Some(key) = p.face.as_ref().and_then(|f| f.card.clone()) else { return json!({"address": addr, "missing": true, "why": "names no card"}) };
        let Ok(r) = self.world.resolve(&p) else { return json!({"address": addr, "missing": true}) };
        let body = match &r.found {
            Some(seqaddr_core::resolve::Found::Face { body }) | Some(seqaddr_core::resolve::Found::Draft { body }) => body.clone(),
            _ => return json!({"address": addr, "missing": true, "axiom": "7", "trace": r.trace}),
        };
        match parse_face(&body).ok().and_then(|d| d.card(&key).cloned()) {
            Some(c) => {
                let mut v = card_json(&c, addr, r.state.as_deref().unwrap_or("seated"));
                v["source"] = json!(r.source);
                v["resolved_from"] = json!(r.origin.as_str());
                v
            }
            None => json!({"address": addr, "missing": true, "axiom": "7", "why": format!("the face has no card `{key}`")}),
        }
    }

    /// POST /ask {prompt, book?} -> {pieces:[...]} or {probe:{question}}.
    pub fn ask(&self, raw: &Value) -> Answer {
        let Some(prompt) = raw.get("prompt").and_then(|v| v.as_str()) else { return (400, json!({"error": "invalid", "detail": "send {\"prompt\": \"...\", \"book\": \"DD.SS.BB\"}"})) };
        let book = match raw.get("book").and_then(|v| v.as_str()) {
            Some(s) => match BookId::parse(s) {
                Ok(b) => Some(b),
                Err(e) => return (400, json!({"error": "invalid", "rule": e.rule(), "detail": e.detail()})),
            },
            None => None,
        };
        let books = self.ask_books(book);
        let qs = self.question_cards(&books);
        let bs = self.brand_cards(&books);
        let solved = match ask::solve(prompt, &qs, &bs, &self.cfg.ask) {
            Ok(s) => s,
            Err(e) => return (422, json!({"error": e.error, "rule": e.rule, "detail": e.detail})),
        };
        let mut v = json!({"heard": solved.heard, "ranked": solved.ranked, "threshold": solved.threshold, "formula": solved.formula, "books": books.iter().map(|b| b.to_string()).collect::<Vec<_>>()});
        match &solved.outcome {
            ask::Outcome::Pieces(ps) => {
                let pieces: Vec<Value> = ps
                    .iter()
                    .map(|c| {
                        let t = c.target.clone().unwrap_or_default();
                        json!({"address": t, "card": self.target_card(&t), "matched": c.matched, "score": c.score, "why": c.why, "via": {"kind": c.kind, "address": c.via, "title": c.via_title, "phrasing": c.phrasing}})
                    })
                    .collect();
                v["pieces"] = json!(pieces);
            }
            ask::Outcome::Probe { question, near } => {
                v["probe"] = json!({"question": question, "near": near});
            }
        }
        (200, v)
    }

    /// POST /ask/link {question: card address, phrasing}: a new phrasing linked to a
    /// known question, through drafting (copy if seated, note, merge) and the queue.
    pub fn ask_link(&mut self, raw: &Value, by: &str) -> Answer {
        let (Some(q), Some(ph)) = (raw.get("question").and_then(|v| v.as_str()), raw.get("phrasing").and_then(|v| v.as_str())) else {
            return (400, json!({"error": "invalid", "detail": "send {\"question\": \"DD.SS.BB.PPPP.FF.key\", \"phrasing\": \"...\"}"}));
        };
        if let Err(e) = ask::check_ascii(ph) {
            return (422, json!({"error": e.error, "rule": e.rule, "detail": e.detail}));
        }
        let ph = ph.trim();
        if ask::words(ph).is_empty() || ph.contains(',') || ph.contains('\n') {
            return (422, json!({"error": "invalid", "rule": "R11", "detail": "a phrasing needs at least one important word, and no comma or newline"}));
        }
        let p = match Address::parse_full_page(q) {
            Ok(p) => p,
            Err(e) => return (400, json!({"error": "invalid", "rule": e.rule(), "detail": e.detail()})),
        };
        let (Some(b), Some(fp)) = (p.book_id(), p.face.clone()) else { return (400, json!({"error": "invalid", "detail": "the question is a card address DD.SS.BB.PPPP.FF.key"})) };
        let Some(key) = fp.card.clone() else { return (400, json!({"error": "invalid", "detail": "the question address names no card"})) };
        let Some(fs) = self.world.get(b).and_then(|st| st.face(p.page, fp.face)).cloned() else {
            return (404, json!({"error": "missing", "axiom": "7", "detail": format!("no face {b}.{:04}.{:02}", p.page, fp.face)}));
        };
        let Some((text, _)) = face_text(&fs) else { return (404, json!({"error": "missing", "axiom": "7", "detail": "the face is retired"})) };
        let is_question = parse_face(text).ok().and_then(|d| d.card(&key).map(|c| c.field("type") == Some("question"))).unwrap_or(false);
        if !is_question {
            return (404, json!({"error": "missing", "axiom": "7", "detail": format!("no question card `{key}` on that face")}));
        }
        let base = fs.draft.as_ref().map(|d| d.body.clone()).or(fs.seated.clone()).unwrap();
        let tf = |h: &str| title_form(h).unwrap_or_default();
        let new_body = match ask::add_form(&base, &key, ph, tf) {
            Ok(x) => x,
            Err("already linked") => return (409, json!({"error": "conflict", "axiom": "1", "detail": format!("`{ph}` is already a phrasing of `{key}`")})),
            Err(e) => return (404, json!({"error": "missing", "axiom": "7", "detail": e})),
        };
        let face_addr = format!("{b}.{:04}.{:02}", p.page, fp.face);
        let last = self.world.get(b).map(|s| s.last_n).unwrap_or(0);
        let mut ops = Vec::new();
        if fs.draft.is_none() {
            ops.push(json!({"op": "copy", "addr": face_addr, "reason": format!("link a new phrasing to question {key} (R11)")}));
        }
        let note_n = last + ops.len() as u64 + 1;
        ops.push(json!({"op": "note", "addr": format!("{face_addr}.draft"), "body": format!("R11: link the phrasing \"{ph}\" to the question `{key}`")}));
        ops.push(json!({"op": "merge", "addr": format!("{face_addr}.draft"), "cites": note_n, "body": new_body}));
        let (c, mut v) = self.propose(json!({"ops": ops}), by);
        v["linked"] = json!({"question": q, "phrasing": ph, "draft": format!("{face_addr}.draft"), "note": "the phrasing is on the draft; it is found now (R5) and is seated by a promote with approval (R2)"});
        (c, v)
    }
}
