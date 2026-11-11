// Read-only mock of the compute HTTP API (docs/CONTRACT.md).
// Replays books/*.book JSON Lines files. Never writes to disk.
// Run: node mock/server.mjs   (PORT default 7700, BOOKS_DIR default ../../books, falls back to ./fixtures)
import { createServer } from "node:http";
import { readdirSync, readFileSync, existsSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const PORT = Number(process.env.PORT ?? 7700);
const repoRoot = resolve(here, "..", "..");

function bookFiles(dir) {
  if (!dir || !existsSync(dir)) return [];
  return readdirSync(dir).filter((f) => /^\d\d\.\d\d\.\d\d\.book$/.test(f)).map((f) => join(dir, f));
}
function findBooks() {
  const dirs = process.env.BOOKS_DIR ? [process.env.BOOKS_DIR] : [join(repoRoot, "books"), join(repoRoot, "kernel")];
  let files = dirs.flatMap(bookFiles);
  let from = dirs.join(", ");
  if (files.length === 0) { files = bookFiles(join(here, "fixtures")); from = "app/mock/fixtures (no books found)"; }
  // a book in books/ wins over the same address in kernel/
  const seen = new Map();
  for (const f of files) { const a = f.split("/").pop().replace(/\.book$/, ""); if (!seen.has(a)) seen.set(a, f); }
  return { files: [...seen.values()], from };
}

const TAILS = new Set(["draft", "retired", "pack", "open", "return", "review"]);

// ---------- replay ----------
function loadBook(file) {
  const raw = readFileSync(file, "utf8").split("\n");
  const header = JSON.parse(raw[0]);
  const book = { address: header.address, entries: [], faces: new Map(), warnings: [] };
  for (let i = 1; i < raw.length; i++) {
    const line = raw[i].trim();
    if (!line) continue;
    let e;
    try { e = JSON.parse(line); } catch { book.warnings.push(`line ${i + 1} is not whole JSON; dropped (crash safety, format.md 3.1)`); continue; }
    e.book = book.address;
    book.entries.push(e);
    apply(book, e);
  }
  return book;
}
// faceKey: "PPPP.FF" | "PPPP.FF.NN" | "PPPP.FF.draft"
function split(addr) {
  const parts = addr.split(".");
  const book = parts.slice(0, 3).join(".");
  const page = parts[3];
  const rest = parts.slice(4);
  return { book, page, rest };
}
function faceKeyOf(e) {
  const { page, rest } = split(e.addr);
  const nums = rest.filter((p) => /^\d\d$/.test(p));
  let key = [page, ...nums].join(".");
  const tail = e.tail ?? (e.op === "tail" ? undefined : undefined);
  if (nums.length === 1 && (tail === "draft")) key += ".draft";
  return key;
}
function apply(book, e) {
  const key = faceKeyOf(e);
  const f = book.faces.get(key);
  switch (e.op) {
    case "put":
      book.faces.set(key, { body: e.body ?? "", tail: e.tail, n: e.n, by: e.by, at: e.at });
      break;
    case "tail":
      if (!f) { book.warnings.push(`entry ${e.n}: tail on missing ${e.addr}`); break; }
      if (e.from && f.tail !== e.from) { book.warnings.push(`entry ${e.n}: tail from ${e.from} but current is ${f.tail}`); break; }
      f.tail = e.to; f.n = e.n; f.by = e.by; f.at = e.at;
      break;
    case "copy": {
      const seated = book.faces.get(key.replace(/\.draft$/, ""));
      book.faces.set(key, { body: seated?.body ?? "", tail: "draft", n: e.n, by: e.by, at: e.at });
      break;
    }
    case "promote": {
      const d = book.faces.get(key.replace(/\.draft$/, "") + ".draft");
      if (d) { book.faces.set(key.replace(/\.draft$/, ""), { ...d, tail: undefined, n: e.n }); book.faces.delete(key.replace(/\.draft$/, "") + ".draft"); }
      break;
    }
    default: // note, merge, use, snapshot: kept in history, not replayed by the mock
      break;
  }
}

let state = { books: new Map(), from: "" };
function reload() {
  const { files, from } = findBooks();
  const books = new Map();
  for (const f of files) { try { const b = loadBook(f); books.set(b.address, b); } catch (err) { console.error("cannot read", f, err.message); } }
  state = { books, from };
}
reload();

// ---------- helpers ----------
const fm = (body) => {
  const m = /^---\n([\s\S]*?)\n---/.exec(body ?? "");
  const out = {};
  if (m) for (const l of m[1].split("\n")) { const i = l.indexOf(":"); if (i > 0) out[l.slice(0, i).trim()] = l.slice(i + 1).trim(); }
  return out;
};
const titleOfBook = (b) => fm(b?.faces.get("0000.00")?.body).title ?? null;
const titleOfPage = (b, p) => fm(b?.faces.get(`${p}.00`)?.body).title ?? null;
function chain(bookAddr) {
  const [d, s] = bookAddr.split(".");
  const c = [bookAddr, `${d}.${s}.00`, `${d}.00.00`, "00.00.00"];
  return [...new Set(c)];
}
const levelName = (i, addr) => (i === 0 ? "local" : addr === "00.00.00" ? "kernel" : addr.endsWith(".00.00") ? "desk" : "shelf");

function parseCards(body) {
  const cards = [];
  const lines = (body ?? "").split("\n");
  let cur = null, inFields = false;
  for (const l of lines) {
    const h = /^##\s+(.+)$/.exec(l);
    if (h) {
      cur = { title: h[1].trim(), key: h[1].trim().toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, ""), fields: {}, body: "" };
      cards.push(cur); inFields = true; continue;
    }
    if (!cur) continue;
    if (inFields) {
      const f = /^([a-z][a-z0-9_.-]*):\s?(.*)$/i.exec(l);
      if (f && l.trim()) { cur.fields[f[1]] = f[2]; continue; }
      inFields = false;
      if (!l.trim()) continue;
    }
    cur.body += (cur.body ? "\n" : "") + l;
  }
  return cards;
}

function resolveFace(full) {
  const p = full.split(".");
  if (p.length < 5) return { trace: [], hit: null };
  const bookAddr = p.slice(0, 3).join(".");
  const key = p.slice(3).join(".");
  const trace = [];
  let hit = null;
  chain(bookAddr).forEach((ba) => {
    if (hit) return;
    const b = state.books.get(ba);
    const checked = `${ba}.${key}`;
    const f = b?.faces.get(key);
    trace.push({ step: trace.length + 1, checked, found: !!f, level: levelName(trace.length, ba), book_exists: !!b });
    if (f) hit = { ba, f, level: levelName(trace.length - 1, ba) };
  });
  return { trace, hit };
}

function pageView(pageAddr) {
  const p = pageAddr.split(".");
  const bookAddr = p.slice(0, 3).join("."), page = p[3];
  const faces = {}, inherited = [];
  const own = state.books.get(bookAddr);
  chain(bookAddr).forEach((ba, i) => {
    const b = state.books.get(ba);
    if (!b) return;
    for (const [k, f] of b.faces) {
      if (!k.startsWith(page + ".")) continue;
      const fk = k.slice(page.length + 1);
      if (faces[fk]) continue;
      faces[fk] = { body: f.body, ...(f.tail ? { tail: f.tail } : {}), source: `${ba}.${k}`, resolved_from: levelName(i, ba), n: f.n, by: f.by, at: f.at };
      if (i > 0) inherited.push(`${ba}.${k}`);
    }
  });
  if (Object.keys(faces).length === 0) return null;
  let title = titleOfPage(own, page);
  if (!title) for (const ba of chain(bookAddr)) { title = titleOfPage(state.books.get(ba), page); if (title) break; }
  return { address: pageAddr, title, faces, inherited };
}

const ADDR_RE = /\b\d\d\.\d\d\.\d\d\.\d{4}\b/g;
function pageExists(pa) { return !!pageView(pa); }
function links(pageAddr) {
  const v = pageView(pageAddr);
  const forward = new Set();
  if (v) for (const [fk, f] of Object.entries(v.faces)) if (fk.startsWith("08")) for (const m of f.body.matchAll(ADDR_RE)) if (m[0] !== pageAddr) forward.add(m[0]);
  const back = new Set();
  for (const b of state.books.values()) for (const [k, f] of b.faces) {
    if (!/^\d{4}\.08/.test(k)) continue;
    const from = `${b.address}.${k.slice(0, 4)}`;
    if (from === pageAddr) continue;
    if ((f.body ?? "").includes(pageAddr)) back.add(from);
  }
  const fwd = [...forward];
  return { forward: fwd, back: [...back], missing: fwd.filter((a) => !pageExists(a)), one_way: fwd.filter((a) => pageExists(a) && !links1way(a, pageAddr)) };
}
function links1way(target, source) {
  const v = pageView(target);
  return v && Object.entries(v.faces).some(([fk, f]) => fk.startsWith("08") && f.body.includes(source));
}

function brands(q) {
  const word = (q ?? "").trim();
  if (!word) return [];
  const out = [];
  for (const b of state.books.values()) {
    const dict = b.faces.get("0012.03");
    if (!dict) continue;
    for (const c of parseCards(dict.body)) {
      if (c.key !== word.toLowerCase()) continue;
      for (const [k, v] of Object.entries(c.fields)) {
        if (!/^[a-z0-9-]+\.\d{3}$/.test(k)) continue;
        const target = v.trim();
        const tp = target.split(".");
        const cardKey = tp.slice(5).join(".") || c.key;
        const r = resolveFace(tp.slice(0, 5).join("."));
        const card = r.hit ? parseCards(r.hit.f.body).find((x) => x.key === cardKey) : null;
        const forms = (card?.fields.forms ?? "").split(",").map((s) => s.trim()).filter(Boolean);
        out.push({ word: c.title, brand: target, brand_id: k, dictionary: `${b.address}.0012.03`, is_default: c.fields.default === k, title: card?.title ?? null, why: card?.fields.means ?? null, forms, exact_form: forms.length ? forms.includes(word) : null, page: tp.slice(0, 4).join("."), missing: !card });
      }
    }
  }
  return out;
}

function cards(title) {
  const key = (title ?? "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  const out = [];
  for (const b of state.books.values()) for (const [k, f] of b.faces) {
    for (const c of parseCards(f.body)) if (c.key === key) out.push({ address: `${b.address}.${k}.${c.key}`, face: `${b.address}.${k}`, face_no: k.split(".")[1], page_title: titleOfPage(b, k.slice(0, 4)), title: c.title, key: c.key, fields: c.fields, body: c.body, tail: f.tail ?? null });
  }
  return out;
}

function history(addr) {
  const out = [];
  for (const b of state.books.values()) for (const e of b.entries) if (e.addr === addr || e.addr.startsWith(addr + ".")) out.push(e);
  return out.sort((a, b) => (a.at < b.at ? -1 : 1));
}

// ---------- http ----------
function send(res, code, obj) {
  res.writeHead(code, { "content-type": "application/json; charset=utf-8", "access-control-allow-origin": "*" });
  res.end(JSON.stringify(obj));
}
const missing = (res, detail) => send(res, 404, { error: "missing", axiom: "7", detail });

createServer((req, res) => {
  const url = new URL(req.url, "http://x");
  const [, route, ...restParts] = url.pathname.split("/");
  const arg = decodeURIComponent(restParts.join("/"));
  if (process.env.MOCK_RELOAD !== "0") reload();
  try {
    if (req.method === "POST" && route === "propose") return send(res, 200, { status: "rejected", reasons: ["the mock compute is read-only; run the real compute to write"], entries: [] });
    if (req.method !== "GET") return send(res, 405, { error: "method", detail: "GET only (mock)" });
    switch (route) {
      case "health": return send(res, 200, { ok: true, books: state.books.size, mock: true, from: state.from });
      case "books": return send(res, 200, [...state.books.values()].sort((a, b) => a.address.localeCompare(b.address)).map((b) => ({ address: b.address, title: titleOfBook(b), pages: new Set([...b.faces.keys()].map((k) => k.slice(0, 4))).size })));
      case "book": {
        const b = state.books.get(arg);
        if (!b) return missing(res, `no book ${arg}`);
        const pages = new Map();
        for (const k of [...b.faces.keys()].sort()) { const p = k.slice(0, 4); if (!pages.has(p)) pages.set(p, new Set()); pages.get(p).add(k.slice(5, 7)); }
        return send(res, 200, { address: b.address, title: titleOfBook(b), pages: [...pages].map(([page, fs]) => ({ page, title: titleOfPage(b, page), faces: [...fs].sort() })), warnings: b.warnings });
      }
      case "page": { const v = pageView(arg); return v ? send(res, 200, v) : missing(res, `no page ${arg}`); }
      case "face": {
        const r = resolveFace(arg);
        if (!r.hit) return send(res, 404, { error: "missing", axiom: "7", address: arg, resolved_from: "missing", trace: r.trace });
        return send(res, 200, { address: arg, body: r.hit.f.body, ...(r.hit.f.tail ? { tail: r.hit.f.tail } : {}), source: `${r.hit.ba}.${arg.split(".").slice(3).join(".")}`, resolved_from: r.hit.level });
      }
      case "resolve": {
        if (arg.split(".").length >= 5) return send(res, 200, resolveFace(arg).trace);
        // page address: check page identity face 00 along the chain
        return send(res, 200, resolveFace(arg + ".00").trace);
      }
      case "history": return send(res, 200, history(arg));
      case "links": return send(res, 200, links(arg));
      case "brands": return send(res, 200, brands(url.searchParams.get("q")));
      case "cards": return send(res, 200, cards(url.searchParams.get("title")));
      case "queue": return send(res, 200, []);
      default: return send(res, 404, { error: "route", detail: url.pathname });
    }
  } catch (err) { return send(res, 500, { error: "mock", detail: String(err?.message ?? err) }); }
}).listen(PORT, "127.0.0.1", () => console.log(`mock compute on http://127.0.0.1:${PORT}  books from: ${state.from}  (${state.books.size} books)`));
