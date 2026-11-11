"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { clearDone, showDone, propose, type Op } from "@/lib/propose";
import { useAuth } from "@/components/WhoAmI";
import { Outcome } from "@/components/Outcome";
import type { ProposeResult } from "@/lib/rules";
import { FACE_TEMPLATE, type DraftNote } from "@/lib/drafting";
import { nonAscii } from "@/lib/seq";

type Props = {
  override?: string | null;
  page: string; face: string; mode: "new-page" | "new-face" | "inherited" | "seated" | "draft"; pageTitle: string | null;
  live: { body: string; source: string; from: string } | null; draft: { body: string } | null; notes: DraftNote[];
};

const STEP_TEXT: Record<Props["mode"], { title: string; plain: string }> = {
  "new-page": { title: "This page does not exist yet", plain: "You are making a new page. It gets a door (face 00, its stamp with the title) and this face. Both are written as drafts, in one proposal: all or nothing." },
  "new-face": { title: "This face is empty on this page", plain: "You are writing a new face. It is written as a draft (not live)." },
  inherited: { title: "This face is inherited from above", plain: "This book does not write it; it comes from the shelf, desk or kernel. Director ruling R7: a local override is not written over the face. It is its own page in this book's reserved pages 0001-0009, saying what it changes, why it is there, why it is needed, and what it should achieve." },
  seated: { title: "This face is live", plain: "A live face is never edited in place. Step 1: copy it into a draft. Step 2: add notes. Step 3: merge each note into the draft. Step 4: seat it." },
  draft: { title: "This face has a draft", plain: "Add notes for what should change, then merge each note into the draft. When every note is merged, the draft can be seated." },
};

export function DraftForm(p: Props) {
  const auth = useAuth();
  const router = useRouter();
  const [title, setTitle] = useState(p.pageTitle ?? "");
  const [body, setBody] = useState(p.override ? `## Override\nchanges: ${p.override}\nwhy: \nneeded-because: \nshould-achieve: \n\nWhat this override does, in plain words.` : FACE_TEMPLATE[p.face] ?? "## Card Title\n\n");
  const [note, setNote] = useState("");
  const open = p.notes.filter((n) => !n.struck);
  const [cite, setCite] = useState<number | null>(open[0]?.n ?? null);
  const [merged, setMerged] = useState(p.draft?.body ?? "");
  const [action, setAction] = useState<"note" | "merge">(open.length ? "merge" : "note");
  const [res, setRes] = useState<ProposeResult | null>(null);
  const [busy, setBusy] = useState(false);
  const [reason, setReason] = useState("");
  const fa = `${p.page}.${p.face}`;
  useEffect(() => { setMerged(p.draft?.body ?? ""); }, [p.draft?.body]);
  const openKey = open.map((n) => n.n).join(",");
  useEffect(() => { setCite(open[0]?.n ?? null); setAction(open.length ? "merge" : "note"); setNote(""); }, [openKey]); // eslint-disable-line react-hooks/exhaustive-deps

  const ops: Op[] = useMemo(() => {
    switch (p.mode) {
      case "new-page": return [
        { op: "put", addr: `${p.page}.00`, tail: "draft", body: `---\ntitle: ${title}\n---` },
        { op: "put", addr: fa, tail: "draft", body, ...(reason.trim() ? { reason: reason.trim() } : {}) },
      ];
      case "new-face": return [{ op: "put", addr: fa, tail: "draft", body, ...(reason.trim() ? { reason: reason.trim() } : {}) }];
      case "inherited": return [];
      case "seated": return [{ op: "copy", addr: fa, ...(reason.trim() ? { reason: reason.trim() } : {}) }];
      case "draft": return action === "note" ? [{ op: "note", addr: `${fa}.draft`, body: note }] : [{ op: "merge", addr: `${fa}.draft`, cites: cite ?? undefined, body: merged }];
    }
  }, [p.mode, p.page, fa, title, body, note, cite, merged, action, reason]);

  async function send() {
    setBusy(true); setRes(null);
    const r = await propose(ops);
    setBusy(false);
    if (r.status === "approved") { setRes(null); showDone(router, r.queue_id); } else { setRes(r); clearDone(router); }
  }

  const s = STEP_TEXT[p.mode];
  return (
    <>
      <div className="panel">
        <h3>{s.title}</h3>
        <p style={{ marginTop: 0 }}>{s.plain}</p>
        {p.mode === "seated" || p.mode === "draft" ? (
          <div className="loop">
            {["1 Copy to draft", "2 Add notes", "3 Merge notes", "4 Seat it"].map((t, i) => {
              const now = p.mode === "seated" ? 0 : open.length ? 2 : p.notes.length ? 3 : 1;
              return <span key={t} className={`st ${i === now ? "now" : i < now ? "done" : ""}`}>{t}</span>;
            })}
          </div>
        ) : null}

        {p.mode === "new-page" ? (
          <div className="field"><label htmlFor="t">Page title <small>(lowercase letters, digits and hyphens; pages 1000 and up need one)</small></label>
            <input id="t" className="big" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="clock" /></div>
        ) : null}

        {p.mode === "inherited" ? (
          <>
            {p.live ? <><strong>Inherited from <code>{p.live.source}</code> ({p.live.from}):</strong><pre className="body mono card">{p.live.body}</pre></> : null}
            <Link className="tab" href={`/draft?page=${p.page.slice(0, 8)}.0001&face=04&override=${fa}`}>Write an override page in 0001 →</Link>
            <p className="note">7: which of 0001-0009 to use, and its exact faces, are not settled. 0001 is offered; change the address if it is taken.</p>
          </>
        ) : null}
        {p.mode === "new-page" || p.mode === "new-face" ? (
          <div className="field"><label htmlFor="b">What the face says <small>(cards start with ## and a title, then lines like why: ...)</small></label>
            <textarea id="b" className="big mono" rows={10} value={body} onChange={(e) => setBody(e.target.value)} /></div>
        ) : null}

        {p.mode === "seated" && p.live ? (
          <><strong>The live face, as it is now:</strong><pre className="body mono card">{p.live.body}</pre>
            <p className="note">The compute makes the copy itself; you send no text (drafting D0).</p></>
        ) : null}

        {p.mode === "new-page" || p.mode === "new-face" || p.mode === "seated" ? (
          <div className="field"><label htmlFor="why">Why is this a draft? <span className="note">(kept with the draft and shown wherever it appears, R5)</span></label>
            <input id="why" className="big" value={reason} onChange={(e) => setReason(e.target.value)} placeholder="waiting for a trial" /></div>
        ) : null}

        {p.mode === "draft" ? (
          <>
            <div className="cols">
              {p.live ? <div><strong>Live now</strong><pre className="body mono card">{p.live.body}</pre></div> : null}
              <div><strong>The draft</strong><pre className="body mono card">{p.draft?.body}</pre></div>
            </div>
            <h3>Notes on this draft</h3>
            {p.notes.length === 0 ? <p className="note">No notes yet.</p> : (
              <ul>{p.notes.map((n) => <li key={n.n} style={{ textDecoration: n.struck ? "line-through" : "none" }}><code>#{n.n}</code> {n.body} <span className="note">— {n.by}{n.struck ? `, merged in #${n.struckBy}` : ", not merged yet"}</span></li>)}</ul>
            )}
            <div className="choice">
              <button className={action === "note" ? "on" : ""} onClick={() => setAction("note")}>Add a note</button>
              <button className={action === "merge" ? "on" : ""} onClick={() => setAction("merge")} disabled={!open.length}>Merge a note {open.length ? `(${open.length} open)` : "(none open)"}</button>
              {!open.length ? <Link className="tab" href={`/seat?addr=${fa}`}>Ready: seat this draft →</Link> : null}
            </div>
            {action === "note" ? (
              <div className="field"><label htmlFor="n">Your note <small>(what should change, and why)</small></label>
                <textarea id="n" className="big" rows={3} value={note} onChange={(e) => setNote(e.target.value)} /></div>
            ) : (
              <>
                <div className="field"><label htmlFor="c">Which note this change comes from</label>
                  <select id="c" className="big" value={cite ?? ""} onChange={(e) => setCite(Number(e.target.value))}>{open.map((n) => <option key={n.n} value={n.n}>#{n.n} {n.body.slice(0, 60)}</option>)}</select></div>
                <div className="field"><label htmlFor="m">The draft after this change</label>
                  <textarea id="m" className="big mono" rows={10} value={merged} onChange={(e) => setMerged(e.target.value)} /></div>
              </>
            )}
          </>
        ) : null}

        <details className="preview" open>
          <summary>Check before sending: the exact proposal <span className="note">(your name comes from your token{auth.name ? `: ${auth.name}` : ""})</span></summary>
          <pre>{JSON.stringify({ ops }, null, 2)}</pre>
        </details>
        {(() => { const bad = nonAscii(JSON.stringify(ops.map((o) => o.body ?? ""))); return bad.length ? <p className="no-box" style={{ padding: "8px 14px" }}><b>Plain characters only (Director ruling R4).</b> The compute will refuse: {bad.map((c) => <code key={c}>{JSON.stringify(c)} </code>)}</p> : null; })()}
        <div className="row" style={{ marginTop: 12 }}>
          <button className="go" onClick={send} disabled={busy || ops.length === 0}>{busy ? "Sending…" : p.mode === "seated" ? "Copy into a draft" : p.mode === "draft" ? (action === "note" ? "Add the note" : "Merge it") : "Send the draft"}</button>
          <span className="note">The compute checks it. If any step breaks a rule, nothing is written.</span>
        </div>
      </div>
      {res ? <Outcome res={res} /> : null}
    </>
  );
}
