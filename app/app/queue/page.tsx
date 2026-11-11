import Link from "next/link";
import { get } from "@/lib/compute";
import { Header, NotOk, Raw } from "@/components/ui";
import { ReasonLine } from "@/components/Outcome";
import { torontoTime } from "@/lib/seq";
import type { Reason } from "@/lib/rules";

export const dynamic = "force-dynamic";

type Q = { pending: number; serialized: boolean; proposals: { id: string; at: string; by: string; book?: string; status: string; http?: number; ops?: number; entries?: number[]; reasons?: Reason[]; findings?: Reason[] }[] };

export default async function Queue({ searchParams }: { searchParams: Promise<{ show?: string }> }) {
  const { show } = await searchParams;
  const r = await get<Q>("/queue");
  const head = <Header title="Queue" lede="Every proposal sent to the compute, newest first, and what happened to it. One at a time: the compute checks each one fully before the next." />;
  if (r.kind !== "ok") return <>{head}<NotOk r={r} what="the queue" /></>;
  const all = r.data.proposals;
  const list = show === "rejected" ? all.filter((p) => p.status !== "approved") : show === "approved" ? all.filter((p) => p.status === "approved") : all;
  const nOk = all.filter((p) => p.status === "approved").length;
  return (
    <>
      {head}
      <div className="panel row">
        <span className="badge local"><b>{nOk}</b> approved</span>
        <span className="badge missing"><b>{all.length - nOk}</b> not written</span>
        <span className="badge seated"><b>{r.data.pending}</b> waiting</span>
        <span className="note">One at a time: {r.data.serialized ? "yes" : "no"} · kept in the compute&apos;s memory only (the last 200), not in a book</span>
        <span style={{ marginLeft: "auto" }} className="row"><Link href="/queue">all</Link><Link href="/queue?show=approved">approved</Link><Link href="/queue?show=rejected">not written</Link><Link href={`/queue${show ? `?show=${show}` : ""}`}>refresh</Link></span>
      </div>
      {list.length === 0 ? <p className="note">Nothing here yet.</p> : null}
      {list.map((p) => (
        <div key={p.id} className="panel" style={{ borderLeft: `6px solid ${p.status === "approved" ? "var(--good)" : "var(--hole)"}` }}>
          <div className="row">
            <strong style={{ fontSize: "1.1rem" }}>{p.status === "approved" ? "✓ Approved and written" : "✗ Not written"}</strong>
            <span className="note">{p.id} · by <b>{p.by}</b> · {torontoTime(p.at)} · {p.ops ?? "?"} step(s) · HTTP {p.http}</span>
          </div>
          {p.book ? <p style={{ margin: "6px 0" }}>Book <Link href={`/book/${p.book}`}><code>{p.book}</code></Link>{p.entries?.length ? <> · entries {p.entries.map((n) => <code key={n}>#{n} </code>)} <Link href={`/history/${p.book}`}>see them in history</Link></> : null}</p> : null}
          {p.reasons?.length ? <ul style={{ paddingLeft: 20 }}>{p.reasons.map((x, i) => <ReasonLine key={i} r={x} />)}</ul> : null}
          {p.findings?.length ? <><strong>Findings:</strong><ul>{p.findings.map((x, i) => <ReasonLine key={i} r={x} />)}</ul></> : null}
        </div>
      ))}
      <Raw data={r.data} url={r.url} />
    </>
  );
}
