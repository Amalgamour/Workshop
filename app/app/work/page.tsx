import Link from "next/link";
import { get, type LogEntry, type PageDetail } from "@/lib/compute";
import { QueueResult } from "@/components/QueueResult";
import { Addr, Header, Raw } from "@/components/ui";
import { WorkBoard, type Job } from "@/components/WorkBoard";

export const dynamic = "force-dynamic";

export default async function Work({ searchParams }: { searchParams: Promise<{ page?: string; job?: string; done?: string }> }) {
  const sp = await searchParams;
  const head = <Header title="Work loop" lede="Jobs live on face 05 of a page, as numbered counters (05.01, 05.02, ...). Each job walks one loop: draft → pack → open → return → review → closed. The compute checks every move." />;
  if (!sp.page || !/^\d\d\.\d\d\.\d\d\.\d{4}$/.test(sp.page))
    return <>{head}<form className="panel" action="/work"><div className="field"><label>Page address <small>(desk.shelf.book.page)</small></label><input className="big mono" name="page" defaultValue={sp.page ?? ""} placeholder="10.11.21.1100" /></div><button className="go">Open</button></form></>;
  const page = sp.page;
  const [pr, hr] = await Promise.all([get<PageDetail>(`/page/${page}`), get<LogEntry[]>(`/history/${page}.05`)]);
  const pd = pr.kind === "ok" ? pr.data : null;
  const hist = hr.kind === "ok" ? hr.data : [];
  const jobs: Job[] = Object.entries(pd?.faces ?? {})
    .filter(([k]) => /^05\.\d\d$/.test(k) && k !== "05.00")
    .map(([k, v]) => {
      const addr = `${page}.${k}`;
      const h = hist.filter((e) => e.addr === addr || e.addr.startsWith(addr + "."));
      const claim = [...h].reverse().find((e) => e.op === "tail" && e.from === "pack" && e.to === "open");
      const review = [...h].reverse().find((e) => e.op === "tail" && e.from === "return" && e.to === "review");
      const close = [...h].reverse().find((e) => e.op === "tail" && e.from === "review");
      return { nn: k.slice(3), addr, tail: v.tail ?? "closed", body: v.body, claimBy: claim?.by, reviewer: review?.by, outcome: close?.outcome, history: h.map((e) => ({ n: e.n, at: e.at, by: e.by, op: e.op, from: e.from, to: e.to, outcome: e.outcome })) };
    })
    .sort((a, b) => a.nn.localeCompare(b.nn));
  return (
    <>
      {head}
      <QueueResult id={sp.done} />
      <div className="panel row"><strong>{pd?.title ?? "7 page not found"}</strong> <Addr a={`${page}.05`} /> {pd ? <Link href={`/page/${page}?face=05`}>open the page</Link> : null}</div>
      {pd ? <WorkBoard page={page} jobs={jobs} initial={sp.job ?? null} board={pd.boards?.["05"] ? pd.boards["05"].map((b) => `${b.counter}: ${b.tail ?? "closed"}`).join("\n") : pd.faces["05.00"]?.body ?? null} /> : <p>Make the page first on <Link href={`/draft?page=${page}&face=04`}>Draft a face</Link>.</p>}
      <Raw data={{ page: pd, history: hist }} url={pr.url} />
    </>
  );
}
