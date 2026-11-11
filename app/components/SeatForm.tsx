"use client";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { propose } from "@/lib/propose";
import { useWho } from "@/components/WhoAmI";
import { Outcome } from "@/components/Outcome";
import type { ProposeResult } from "@/lib/rules";

export function SeatForm({ faceAddr, openNotes }: { faceAddr: string; openNotes: number }) {
  const [who] = useWho();
  const router = useRouter();
  const [how, setHow] = useState<"r2" | "director">("r2");
  const [trial, setTrial] = useState("");
  const [checked, setChecked] = useState(false);
  const [res, setRes] = useState<ProposeResult | null>(null);
  const [busy, setBusy] = useState(false);
  const op = how === "r2"
    ? { op: "promote", addr: `${faceAddr}.draft`, approved_by: "build-stage (R2)", trial: trial.trim() }
    : { op: "promote", addr: `${faceAddr}.draft`, approved_by: "director" };
  const ready = how === "director" || (trial.trim().length > 0 && checked);

  async function send() {
    setBusy(true);
    const r = await propose(who, [op]);
    setRes(r); setBusy(false);
    if (r.status === "approved") router.refresh();
  }

  return (
    <div className="panel">
      <h3>Before seating, check</h3>
      <ol>
        <li>{openNotes === 0 ? "✓ Every note on the draft is merged." : <b style={{ color: "var(--hole)" }}>{openNotes} note(s) are not merged yet. The compute will refuse (drafting D0).</b>}</li>
        <li>The draft faced a hostile trial from a different view than its maker (axiom 9). <span className="note">The compute cannot check who ran the trial; you can.</span></li>
      </ol>
      <h3>Who approves it</h3>
      <div className="choice">
        <button className={how === "r2" ? "on" : ""} onClick={() => setHow("r2")}>Build stage (R2) <small className="note">with a trial reference</small></button>
        <button className={how === "director" ? "on" : ""} onClick={() => setHow("director")}>The Director <small className="note">only when you are the Director</small></button>
      </div>
      {how === "r2" ? (
        <>
          <div className="field"><label htmlFor="tr">Trial reference <small>(where the hostile pass is written, for example docs/trial/kernel-trial.md#1002)</small></label>
            <input id="tr" className="big mono" value={trial} onChange={(e) => setTrial(e.target.value)} placeholder="docs/trial/....md#..." /></div>
          <label className="row"><input type="checkbox" checked={checked} onChange={(e) => setChecked(e.target.checked)} style={{ width: 22, height: 22 }} /> The trial was run by a different view than the one that wrote the draft.</label>
          <p className="note">Recorded as <code>approved-by: build-stage (R2)</code> with the trial, so every such seat can be found and re-reviewed later.</p>
        </>
      ) : <p className="note">The compute accepts <code>director</code> only when the writer name is <code>director</code> or <code>user</code>. You are writing as <b>{who}</b>.</p>}
      <details className="preview" open><summary>Check before sending: the exact proposal, as <b>{who}</b></summary><pre>{JSON.stringify({ by: who, ops: [op] }, null, 2)}</pre></details>
      <div className="row" style={{ marginTop: 12 }}>
        <button className="go" disabled={!ready || busy} onClick={send}>{busy ? "Sending…" : "Seat it (make it live)"}</button>
        {!ready ? <span className="note">Add the trial reference and tick the box first.</span> : null}
      </div>
      {res ? <Outcome res={res} /> : null}
    </div>
  );
}
