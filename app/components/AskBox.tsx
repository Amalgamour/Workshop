"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { clearDone, post } from "@/lib/propose";
import { Outcome } from "@/components/Outcome";
import { nonAscii } from "@/lib/seq";
import type { ProposeResult } from "@/lib/rules";

export type QuestionCard = { address: string; title: string; forms: string; answer: string; draft: boolean };
type Heard = { text: string; norm: string; kind: "key" | "link" | "question" };
type Piece = { address: string; card?: { title?: string; fields?: Record<string, string>; body?: string; state?: string; source?: string; resolved_from?: string }; matched: string[]; score: number; why: string; via?: { kind: string; address: string; title?: string; phrasing?: string } };
type AskAnswer = { heard?: Heard[]; pieces?: Piece[]; probe?: { question: string; near?: { title?: string; phrasing?: string; score?: number; via?: string; target?: string }[] }; threshold?: number; formula?: string; books?: string[]; error?: string; rule?: string; detail?: string };

const KIND: Record<Heard["kind"], { label: string; cls: string }> = {
  key: { label: "important word", cls: "w-key" },
  question: { label: "question word", cls: "w-q" },
  link: { label: "linking word", cls: "w-link" },
};

export function AskBox({ initial, questions, book }: { initial: string; questions: QuestionCard[]; book: string }) {
  const router = useRouter();
  const [prompt, setPrompt] = useState(initial);
  const [ans, setAns] = useState<AskAnswer | null>(null);
  const [status, setStatus] = useState(0);
  const [busy, setBusy] = useState(false);
  const [q, setQ] = useState(questions[0]?.address ?? "");
  const [phrasing, setPhrasing] = useState(initial);
  const [res, setRes] = useState<ProposeResult | null>(null);
  const bad = nonAscii(prompt);

  async function ask(text = prompt) {
    setBusy(true); setRes(null);
    try {
      const r = await fetch("/api/post/ask", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ prompt: text }) });
      setStatus(r.status); setAns((await r.json()) as AskAnswer);
    } catch (e) { setStatus(0); setAns({ error: "down", detail: String(e) }); }
    setBusy(false);
    setPhrasing(text);
  }
  useEffect(() => { void ask(initial); }, []); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => {
    const via = ans?.pieces?.find((p) => p.via?.kind === "question")?.via?.address;
    if (via && questions.some((x) => x.address === via)) setQ(via);
  }, [ans, questions]);

  async function link() {
    setBusy(true);
    const r = await post("ask/link", JSON.stringify({ question: q, phrasing }));
    setBusy(false);
    if (r.status === "approved") { setRes(null); router.replace(`/ask?q=${encodeURIComponent(phrasing)}&done=${encodeURIComponent(r.queue_id ?? "")}`); router.refresh(); } else { setRes(r); clearDone(router); }
  }

  return (
    <>
      <div className="panel">
        <form onSubmit={(e) => { e.preventDefault(); void ask(); }} className="row">
          <input className="big" style={{ flex: 1, fontSize: "1.3rem" }} value={prompt} onChange={(e) => setPrompt(e.target.value)} aria-label="your question" placeholder="what is my name" />
          <button className="go" disabled={busy || !prompt.trim()}>{busy ? "Asking…" : "Ask"}</button>
        </form>
        {bad.length ? <p className="note" style={{ color: "var(--hole)" }}>Plain characters only (R4): {bad.map((c) => <code key={c}>{JSON.stringify(c)} </code>)}</p> : null}
      </div>

      {ans?.error ? (
        <div className="no-box"><div className="big-word">✗ The compute could not read that</div><p>{ans.detail}</p>{ans.rule ? <span className="badge seated">rule <b>{ans.rule}</b></span> : null}<p className="note">HTTP {status}</p></div>
      ) : null}

      {ans?.heard ? (
        <div className="panel">
          <h3>1 · What I heard</h3>
          <div className="row">{ans.heard.map((h, i) => <span key={i} className={`word ${KIND[h.kind]?.cls ?? ""}`}>{h.text}<small>{KIND[h.kind]?.label ?? h.kind}</small></span>)}</div>
          {ans.heard.length === 0 ? <p className="note">No words I could use.</p> : null}
        </div>
      ) : null}

      {ans?.pieces?.length ? (
        <div className="panel">
          <h3>2 · What I found <span className="note">({ans.pieces.length} piece{ans.pieces.length === 1 ? "" : "s"} for the model to use)</span></h3>
          {ans.pieces.map((p, i) => (
            <div className="card" key={p.address}>
              <h4><span className="chip">piece {i + 1}</span> {p.card?.title ?? p.address}
                {p.card?.state === "draft" ? <span className="badge tail" style={{ marginLeft: 8 }}><b>Draft</b> not live yet</span> : <span className="badge seated" style={{ marginLeft: 8 }}><b>{p.card?.state ?? "?"}</b></span>}
              </h4>
              {p.card?.fields?.means ? <p style={{ margin: "4px 0", fontSize: "1.15rem" }}><b>Means:</b> {p.card.fields.means}</p> : null}
              {p.card?.body ? <p className="body">{p.card.body}</p> : null}
              <p style={{ margin: "6px 0" }}><b>Why it matched:</b> {p.via?.kind === "question" ? <>your words fit the common question <b>&ldquo;{p.via.phrasing}&rdquo;</b></> : <>a word you typed is one of your words (brand)</>}. Matched: {p.matched.map((m) => <span key={m} className="word w-key mini">{m}</span>)}</p>
              <p className="note" style={{ margin: 0 }}>Score {p.score.toFixed(2)} (needs {ans.threshold ?? 0.5}) · {p.why} · card <Link href={`/page/${p.address.split(".").slice(0, 4).join(".")}?face=${p.address.split(".")[4]}`}><code>{p.address}</code></Link>{p.via ? <> · via <code>{p.via.address}</code></> : null}</p>
            </div>
          ))}
        </div>
      ) : null}

      {ans?.probe ? (
        <div className="panel probe">
          <h3>2 · Nothing fits well enough yet</h3>
          <p className="probe-q">{ans.probe.question}</p>
          {ans.probe.near?.length ? <><p className="note">Close, but below the line:</p><ul>{ans.probe.near.map((n, i) => <li key={i}>{n.title ?? n.phrasing ?? n.target} {typeof n.score === "number" ? <span className="note">({n.score.toFixed(2)})</span> : null}</li>)}</ul></> : null}
        </div>
      ) : null}

      <div className="panel">
        <h3>3 · Teach a new way of asking</h3>
        <p className="note" style={{ marginTop: 0 }}>Link a new phrasing to a common question, the way a new form is added to a word. It goes through the queue and lands on the question&apos;s draft (copy, note, merge). You need to be signed in.</p>
        {questions.length === 0 ? <p className="note"><b>7</b> No common questions found on page {book}.0013.</p> : (
          <>
            <div className="field"><label htmlFor="qq">Common question</label>
              <select id="qq" className="big" value={q} onChange={(e) => setQ(e.target.value)}>{questions.map((x) => <option key={x.address} value={x.address}>{x.title}{x.draft ? " (draft)" : ""} — {x.forms}</option>)}</select></div>
            <div className="field"><label htmlFor="ph">The new phrasing</label>
              <input id="ph" className="big" value={phrasing} onChange={(e) => setPhrasing(e.target.value)} /></div>
            <details className="preview"><summary>Check before sending: the exact request</summary><pre>{`POST /ask/link\n${JSON.stringify({ question: q, phrasing }, null, 2)}`}</pre></details>
            <button className="go" style={{ marginTop: 10 }} disabled={busy || !phrasing.trim() || !q} onClick={link}>Link this phrasing</button>
          </>
        )}
        {res ? <Outcome res={res} /> : null}
      </div>

      {ans ? <details className="raw"><summary>Check it yourself: the raw answer from the compute (POST /ask, HTTP {status})</summary><pre>{JSON.stringify(ans, null, 2)}</pre></details> : null}
    </>
  );
}
