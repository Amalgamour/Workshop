import Link from "next/link";
import { get, type LogEntry } from "@/lib/compute";
import { Addr, Header, NotOk, Raw } from "@/components/ui";
import { opPlain, torontoTime } from "@/lib/seq";

export const dynamic = "force-dynamic";

export default async function History({ params }: { params: Promise<{ addr: string }> }) {
  const { addr } = await params;
  const r = await get<LogEntry[]>(`/history/${addr}`);
  const pageAddr = addr.split(".").slice(0, 4).join(".");
  const head = <Header title="History" lede={<>Every approved write that touched this address, oldest first. Nothing is edited in place, so this is the whole line back (axiom 6, Lineage). <Addr a={addr} /> {addr.split(".").length >= 4 ? <Link href={`/page/${pageAddr}`}>open the page</Link> : null}</>} />;
  if (r.kind !== "ok") return <>{head}<NotOk r={r} what={`history for ${addr}`} /></>;
  return (
    <>
      {head}
      <div className="panel">
        {r.data.length === 0 ? <p className="note">No entries. Pages inherited from the kernel have their history in the kernel book.</p> : (
          <table className="log">
            <thead><tr><th>When</th><th>Who</th><th>What</th><th>Where</th><th>Entry</th></tr></thead>
            <tbody>
              {r.data.map((e) => (
                <tr key={`${e.book}-${e.n}`}>
                  <td>{torontoTime(e.at)}<div className="note mono">{e.at}</div></td>
                  <td><strong>{e.by}</strong></td>
                  <td>{opPlain(e)}{e.proposal ? <div className="note">proposal {e.proposal}</div> : null}
                    {e.body ? <details><summary className="note">what was written</summary><pre className="body mono" style={{ fontSize: "0.8rem" }}>{e.body}</pre></details> : null}
                  </td>
                  <td><Link href={`/history/${e.addr}`}><code>{e.addr}</code></Link></td>
                  <td>{e.book ? <code className="note">{e.book}</code> : null} #{e.n}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
      <Raw data={r.data} url={r.url} />
    </>
  );
}
