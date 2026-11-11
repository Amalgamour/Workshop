import Link from "next/link";
import { AXIOM_PLAIN, RULE_PLAIN, type ProposeResult, type Reason } from "@/lib/rules";

export function ReasonLine({ r }: { r: Reason }) {
  return (
    <li style={{ marginBottom: 8 }}>
      <strong>{(r.rule && RULE_PLAIN[r.rule]) ?? "Rejected"}</strong>
      <div className="note">{r.detail}</div>
      <div className="badges" style={{ margin: "4px 0 0" }}>
        {r.rule ? <span className="badge seated">rule <b>{r.rule}</b></span> : null}
        {r.axiom ? <span className="badge missing">axiom <b>{r.axiom}</b> {AXIOM_PLAIN[r.axiom] ?? ""}</span> : null}
        {r.code ? <span className="badge tail">{r.code}</span> : null}
        {typeof r.op === "number" ? <span className="badge seated">step {r.op + 1} of the proposal</span> : null}
      </div>
    </li>
  );
}

export function Outcome({ res }: { res: ProposeResult }) {
  const ok = res.status === "approved";
  return (
    <div className={ok ? "ok-box" : "no-box"} role="status">
      <div className="big-word">{ok ? "✓ Approved and written" : "✗ Not written"}</div>
      {ok ? (
        <p style={{ margin: "6px 0" }}>The compute checked it and added {res.entries?.length ?? 0} entr{res.entries?.length === 1 ? "y" : "ies"} to book <code>{res.book}</code>: {res.entries?.map((n) => <code key={n}>#{n} </code>)}</p>
      ) : (
        <>
          <p style={{ margin: "6px 0" }}>Nothing was changed. All or nothing: if one step fails, no step is written.</p>
          <ul style={{ paddingLeft: 20 }}>{(res.reasons?.length ? res.reasons : [{ rule: undefined, detail: res.detail, axiom: res.axiom, code: res.error }]).map((r, i) => <ReasonLine key={i} r={r} />)}</ul>
        </>
      )}
      {res.findings?.length ? <><strong>Findings (flagged for review, not blocking):</strong><ul>{res.findings.map((r, i) => <ReasonLine key={i} r={r} />)}</ul></> : null}
      <p className="note" style={{ margin: 0 }}>Queue id <code>{res.queue_id ?? "?"}</code> · HTTP {res.http} · <Link href="/queue">see the queue</Link></p>
    </div>
  );
}
