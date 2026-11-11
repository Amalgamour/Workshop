"use client";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { clearDone, showDone, propose, post, type Op } from "@/lib/propose";
import { useAuth } from "@/components/WhoAmI";
import { Outcome } from "@/components/Outcome";
import { LOOP, NEXT, OUTCOMES, type ProposeResult } from "@/lib/rules";
import { TAIL_PLAIN, parseCards } from "@/lib/seq";
import { FACE_TEMPLATE } from "@/lib/drafting";

export type Job = { nn: string; addr: string; tail: string; body: string; claimBy?: string; reviewer?: string; outcome?: string; history: { n: number; at: string; by: string; op: string; from?: string; to?: string; outcome?: string }[] };

export function WorkBoard({ page, jobs, initial, board }: { page: string; jobs: Job[]; initial: string | null; board: string | null }) {
  const auth = useAuth();
  const who = auth.name ?? "you";
  const router = useRouter();
  const [sel, setSel] = useState<string | null>(initial ?? jobs[0]?.nn ?? null);
  const [text, setText] = useState("");
  const [outcome, setOutcome] = useState("passed");
  const [newBody, setNewBody] = useState(FACE_TEMPLATE["05"]);
  const [res, setRes] = useState<ProposeResult | null>(null);
  const [busy, setBusy] = useState(false);
  const job = jobs.find((j) => j.nn === sel) ?? null;
  const used = jobs.map((j) => Number(j.nn));
  const nextNN = String((used.length ? Math.max(...used) : 0) + 1).padStart(2, "0");
  const step = job ? NEXT[job.tail] : undefined;

  const moveOps: Op[] = job && step ? [{
    op: "tail", addr: job.addr, from: job.tail,
    ...(step.to ? { to: step.to } : {}),
    ...(step.needs === "body" ? { body: text } : {}),
    ...(step.needs === "outcome" ? { outcome } : {}),
  }] : [];
  const newOps: Op[] = [{ op: "put", addr: `${page}.05.${nextNN}`, tail: "draft", body: newBody }];

  async function send(ops: Op[], select?: string) {
    setBusy(true); setRes(null);
    // Closing a review goes through POST /close: the compute writes the close for the counter's reviewer (COMPUTE addendum).
    const isClose = ops.length === 1 && ops[0].op === "tail" && ops[0].from === "review";
    const r = isClose ? await post("close", JSON.stringify({ addr: ops[0].addr, outcome: ops[0].outcome })) : await propose(ops);
    setBusy(false);
    if (r.status === "approved") { setRes(null); setText(""); if (select) setSel(select); showDone(router, r.queue_id); } else { setRes(r); clearDone(router); }
  }

  const idx = job ? LOOP.findIndex((l) => l.tail === job.tail) : -1;
  return (
    <>
      <div className="panel">
        <h3>The board <span className="note">(a view the compute derives from the log; never written. R9: faces have no door, so it is not a stored face)</span></h3>
        <div className="board">
          {LOOP.map((l) => (
            <div className="col" key={l.tail}>
              <h4>{l.tail}</h4><div className="note">{l.step} · {l.who}</div>
              {jobs.filter((j) => j.tail === l.tail).map((j) => (
                <div key={j.nn} className={`job ${j.nn === sel ? "sel" : ""}`} onClick={() => { setSel(j.nn); setRes(null); }} style={{ cursor: "pointer" }}>
                  <b>05.{j.nn}</b> {parseCards(j.body).cards[0]?.title ?? ""}{j.outcome ? <div className="note">outcome: {j.outcome}</div> : null}
                </div>
              ))}
            </div>
          ))}
        </div>
        {board ? <p className="note">Board text from the compute: <code>{board.replace(/\n/g, " · ")}</code></p> : null}
      </div>

      {job ? (
        <div className="panel">
          <h3>Job 05.{job.nn}: {parseCards(job.body).cards[0]?.title ?? ""}</h3>
          <div className="loop">{LOOP.map((l, i) => <span key={l.tail} className={`st ${i === idx ? "now" : i < idx ? "done" : ""}`}>{l.tail}</span>)}</div>
          <p style={{ margin: "0 0 6px" }}><b>Now: {job.tail}</b> — {TAIL_PLAIN[job.tail] ?? ""}. {LOOP[idx]?.plain}</p>
          <p className="note" style={{ marginTop: 0 }}>
            {job.claimBy ? <>Claimed by <b>{job.claimBy}</b>. </> : null}
            {job.reviewer ? <>Reviewed by <b>{job.reviewer}</b>. </> : null}
            {job.outcome ? <>Outcome: <b>{job.outcome}</b>. </> : null}
            You are signed in as <b>{who}</b>.
          </p>
          <pre className="body mono card">{job.body}</pre>
          {step ? (
            <div className="card" style={{ borderLeftColor: "var(--warn)" }}>
              <h4>Next step: {step.label}</h4>
              <p className="note" style={{ marginTop: 0 }}>Rule: {step.rule} Usually done by: <b>{step.who}</b>.</p>
              {step.needs === "body" ? <div className="field"><label htmlFor="ret">The return <small>(per work card: ## w01, then result: done | blocked | need, and the evidence)</small></label><textarea id="ret" className="big mono" rows={6} value={text} onChange={(e) => setText(e.target.value)} placeholder={"## w01\nresult: done\nevidence: ..."} /></div> : null}
              {step.needs === "outcome" ? <div className="field"><label htmlFor="oc">Outcome</label><select id="oc" className="big" value={outcome} onChange={(e) => setOutcome(e.target.value)}>{OUTCOMES.map((o) => <option key={o}>{o}</option>)}</select></div> : null}
              <details className="preview"><summary>Check before sending: the exact request</summary><pre>{job.tail === "review" ? `POST /close\n${JSON.stringify({ addr: job.addr, outcome }, null, 2)}` : `POST /propose\n${JSON.stringify({ ops: moveOps }, null, 2)}`}</pre></details>
              <button className="go" style={{ marginTop: 10 }} disabled={busy} onClick={() => send(moveOps)}>{busy ? "Sending…" : step.label}</button>
            </div>
          ) : <p><b>This job is closed.</b> Rework gets a new job with a link back to this one.</p>}
          <details style={{ marginTop: 12 }}><summary>Every stage of this job (its history)</summary>
            <table className="log"><tbody>{job.history.map((e) => <tr key={e.n}><td>#{e.n}</td><td>{e.by}</td><td>{e.op} {e.from ? `${e.from} → ${e.to ?? "closed"}` : ""}{e.outcome ? ` (${e.outcome})` : ""}</td><td className="note">{e.at}</td></tr>)}</tbody></table>
          </details>
        </div>
      ) : null}
      {res ? <Outcome res={res} /> : null}

      <div className="panel">
        <h3>Start a new job <span className="note">(it becomes 05.{nextNN}, as a draft)</span></h3>
        <textarea className="big mono" rows={5} value={newBody} onChange={(e) => setNewBody(e.target.value)} aria-label="new job" />
        <details className="preview"><summary>Check before sending: the exact proposal</summary><pre>{JSON.stringify({ ops: newOps }, null, 2)}</pre></details>
        <button className="go" style={{ marginTop: 10 }} disabled={busy} onClick={() => send(newOps, nextNN)}>Write the job as a draft</button>
      </div>
    </>
  );
}
