"use client";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { clearDone, post, showDone } from "@/lib/propose";
import { Outcome, ReasonLine } from "@/components/Outcome";
import { nonAscii } from "@/lib/seq";
import type { ProposeResult, Reason } from "@/lib/rules";

type Report = { ok?: boolean; errors?: (Reason & { line?: number })[]; findings?: (Reason & { line?: number })[]; error?: string; detail?: string };

/** Export and import one page as a .seq file (R3: the book is the real copy; a .seq file is a view; import is a proposal). */
export function SeqTools({ addr }: { addr: string }) {
  const router = useRouter();
  const [text, setText] = useState("");
  const [report, setReport] = useState<Report | null>(null);
  const [res, setRes] = useState<ProposeResult | null>(null);
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");
  const bad = nonAscii(text);

  async function load() {
    setMsg(""); setReport(null); setRes(null);
    const r = await fetch(`/api/seq?addr=${addr}`);
    if (r.ok) { setText(await r.text()); setMsg("Loaded this page's .seq file from the compute. Change it, check it, then import it."); }
    else setMsg(`The compute could not export it (HTTP ${r.status}).`);
  }
  async function fromFile(f: File | undefined) { if (!f) return; setText(await f.text()); setMsg(`Loaded ${f.name}.`); setReport(null); setRes(null); }
  async function check() {
    setBusy(true); setRes(null);
    try {
      const r = await fetch("/api/post/check.seq", { method: "POST", headers: { "content-type": "text/x-seqpage" }, body: text });
      setReport((await r.json()) as Report);
    } catch (e) { setReport({ ok: false, error: "down", detail: String(e) }); }
    setBusy(false);
  }
  async function importIt() {
    setBusy(true); setReport(null);
    const r = await post("propose", text, "text/x-seqpage");
    setBusy(false);
    if (r.status === "approved") { setRes(null); showDone(router, r.queue_id); } else { setRes(r); clearDone(router); }
  }

  return (
    <div className="panel" id="seq">
      <h3>This page as a .seq file <span className="note">(one file, every face — the book stays the real copy, R3)</span></h3>
      <div className="cols">
        <div>
          <h4 style={{ margin: "0 0 6px" }}>Export</h4>
          <p className="note" style={{ marginTop: 0 }}>Download the page exactly as the compute writes it.</p>
          <div className="row">
            <a className="go linkbtn" href={`/api/seq?addr=${addr}`} download>Export page as .seq ↓</a>
            <a href={`/export?addr=${addr}`}>read it on screen</a>
          </div>
        </div>
        <div>
          <h4 style={{ margin: "0 0 6px" }}>Import</h4>
          <p className="note" style={{ marginTop: 0 }}>Bring a .seq file back. It goes through the queue like any proposal; nothing is written unless the compute approves it.</p>
          <div className="row">
            <button className="quiet" onClick={load}>Start from this page&apos;s .seq</button>
            <label className="quiet filebtn">Choose a .seq file<input type="file" accept=".seq,text/plain" onChange={(e) => fromFile(e.target.files?.[0])} hidden /></label>
          </div>
        </div>
      </div>
      {msg ? <p className="note">{msg}</p> : null}
      {text ? (
        <>
          <textarea className="big mono" rows={14} value={text} onChange={(e) => { setText(e.target.value); setReport(null); }} aria-label=".seq text" style={{ fontSize: "0.85rem", marginTop: 10 }} />
          {bad.length ? <p className="no-box" style={{ padding: "8px 14px" }}><b>Plain characters only (R4).</b> The compute will refuse: {bad.map((c) => <code key={c}>{JSON.stringify(c)} </code>)}</p> : null}
          <div className="row" style={{ marginTop: 10 }}>
            <button className="quiet" onClick={check} disabled={busy}>1 · Check it (writes nothing)</button>
            <button className="go" onClick={importIt} disabled={busy}>2 · Import through the queue</button>
          </div>
        </>
      ) : null}
      {report ? (
        <div className={report.ok ? "ok-box" : "no-box"}>
          <div className="big-word">{report.ok ? "✓ The file is well formed" : "✗ The file has problems"}</div>
          {report.detail ? <p>{report.detail}</p> : null}
          {report.errors?.length ? <ul>{report.errors.map((e, i) => <ReasonLine key={i} r={{ ...e, detail: `${e.line ? `line ${e.line}: ` : ""}${e.detail ?? ""}` }} />)}</ul> : null}
          {report.findings?.length ? <><strong>Findings (not blocking):</strong><ul>{report.findings.map((e, i) => <ReasonLine key={i} r={{ ...e, detail: `${e.line ? `line ${e.line}: ` : ""}${e.detail ?? ""}` }} flag />)}</ul></> : null}
          <details className="raw"><summary>Check it yourself: the raw check report</summary><pre>{JSON.stringify(report, null, 2)}</pre></details>
        </div>
      ) : null}
      {res ? <Outcome res={res} /> : null}
    </div>
  );
}
