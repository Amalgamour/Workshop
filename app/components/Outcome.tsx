import Link from "next/link";
import { AXIOM_PLAIN, RULE_PLAIN, type ProposeResult, type Reason } from "@/lib/rules";

export function ReasonLine({ r, flag }: { r: Reason; flag?: boolean }) {
  return (
    <li style={{ marginBottom: 8 }}>
      <strong>{(r.rule && RULE_PLAIN[r.rule]) ?? (flag ? "Flagged" : "Refused")}</strong>
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

const DOOR: Record<number, { title: string; plain: string }> = {
  401: { title: "✗ Not signed in", plain: "The compute does not know who you are. Paste your token in the sidebar under Signed in, then try again. Nothing was written." },
  403: { title: "✗ Not allowed for your name", plain: "The compute knows who you are, but this needs authority your name does not hold (axiom 1). Nothing was written." },
  415: { title: "✗ Wrong kind of request", plain: "The compute only takes JSON (or a .seq file on import). This is an app fault; nothing was written." },
  0: { title: "✗ The compute is not answering", plain: "Nothing was written. Start the compute and try again." },
  503: { title: "✗ The compute is not answering", plain: "Nothing was written. Start the compute and try again." },
};

export function Outcome({ res }: { res: ProposeResult }) {
  const ok = res.status === "approved";
  const door = !ok && res.http !== undefined ? DOOR[res.http] : undefined;
  return (
    <div className={ok ? "ok-box" : "no-box"} role="status">
      <div className="big-word">{ok ? "✓ Approved and written" : door?.title ?? "✗ Not written"}</div>
      {door ? <p style={{ margin: "6px 0", fontSize: "1.05rem" }}>{door.plain}</p> : null}
      {ok ? (
        <p style={{ margin: "6px 0" }}>The compute checked it and added {res.entries?.length ?? 0} entr{res.entries?.length === 1 ? "y" : "ies"} to book <code>{res.book}</code>: {res.entries?.map((n) => <code key={n}>#{n} </code>)}</p>
      ) : (
        <>
          {!door ? <p style={{ margin: "6px 0" }}>Nothing was changed. All or nothing: if one step fails, no step is written.</p> : null}
          <ul style={{ paddingLeft: 20 }}>{(res.reasons?.length ? res.reasons : res.errors?.length ? res.errors.map((e) => ({ ...e, detail: `${e.line ? `line ${e.line}: ` : ""}${e.detail ?? ""}` })) : [{ rule: (res as { rule?: string }).rule, detail: res.detail, axiom: res.axiom, code: res.error }]).map((r, i) => <ReasonLine key={i} r={r} />)}</ul>
        </>
      )}
      {res.linked ? <p style={{ margin: "6px 0" }}>Linked <b>&ldquo;{res.linked.phrasing}&rdquo;</b> to <code>{res.linked.question}</code>. {res.linked.note}</p> : null}
      {res.seq_findings?.length ? <><strong>Findings from the .seq file:</strong><ul>{res.seq_findings.map((r, i) => <ReasonLine key={i} r={r} flag />)}</ul></> : null}
      {res.findings?.length ? <><strong>Findings (flagged for review, not blocking):</strong><ul>{res.findings.map((r, i) => <ReasonLine key={i} r={r} flag />)}</ul></> : null}
      <p className="note" style={{ margin: 0 }}>Queue id <code>{res.queue_id ?? "?"}</code> · HTTP {res.http} · <Link href="/queue">see the queue</Link></p>
    </div>
  );
}
