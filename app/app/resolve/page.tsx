import Link from "next/link";
import { get, type TraceStep } from "@/lib/compute";
import { Addr, Header, Hole, NotOk, Raw } from "@/components/ui";

export const dynamic = "force-dynamic";

const LEVEL: Record<string, string> = { local: "this book", shelf: "the shelf's own book", desk: "the desk's own book", kernel: "the kernel" };

export default async function Resolve({ searchParams }: { searchParams: Promise<{ addr?: string }> }) {
  const { addr } = await searchParams;
  const head = <Header title="Resolve trace" lede="Step by step: where the compute looked for an address, and where it found it. The first match wins: book, then shelf, then desk, then kernel. If nothing is found, it stays missing and comes to you." />;
  const form = (
    <form className="row" action="/resolve" style={{ marginBottom: 22 }}>
      <input className="big mono" style={{ flex: 1 }} name="addr" defaultValue={addr ?? ""} placeholder="Full address, for example 10.11.21.0021.04" aria-label="address" />
      <button className="go">Trace</button>
    </form>
  );
  if (!addr) return <>{head}{form}</>;
  const r = await get<TraceStep[]>(`/resolve/${addr}`);
  if (r.kind !== "ok") return <>{head}{form}<NotOk r={r} what={addr} /></>;
  const hit = r.data.find((s) => s.found);
  return (
    <>
      {head}{form}
      <div className="panel">
        <h3>Looking for <Addr a={addr} /></h3>
        <ol className="steps">
          {r.data.map((s, i) => (
            <li key={i}>
              <span className={`dot ${s.found ? "yes" : "no"}`}>{s.found ? "✓" : i + 1}</span>
              <div>
                <strong>Step {s.step}: looked in {LEVEL[s.level ?? ""] ?? s.level ?? "the next place"}</strong>
                <div><code>{s.checked}</code> — {s.found ? <b style={{ color: "var(--good)" }}>found here. Stop.</b> : "not here, go up one level."}</div>
              </div>
            </li>
          ))}
        </ol>
        {hit ? <p>Answer: <Link href={`/page/${hit.checked.split(".").slice(0, 4).join(".")}?face=${hit.checked.split(".")[4] ?? ""}`}>open <code>{hit.checked}</code></Link></p>
          : <Hole what={addr} why="Not found at any level. The compute does not guess: this is raised to you." />}
      </div>
      <Raw data={r.data} url={r.url} />
    </>
  );
}
