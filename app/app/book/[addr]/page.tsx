import Link from "next/link";
import { get, type BookDetail } from "@/lib/compute";
import { Addr, Header, NotOk, Raw } from "@/components/ui";
import { FACE_NAMES } from "@/lib/seq";

export const dynamic = "force-dynamic";

export default async function BookPage({ params }: { params: Promise<{ addr: string }> }) {
  const { addr } = await params;
  const r = await get<BookDetail>(`/book/${addr}`);
  if (r.kind !== "ok") return <><Header title={<>Book <code>{addr}</code></>} /><NotOk r={r} what={`book ${addr}`} /></>;
  const b = r.data;
  return (
    <>
      <Header title={<>{b.title ?? "7 no title"}</>} lede={<>A book. Its address: <Addr a={b.address} /></>} />
      {b.warnings?.length ? <div className="down"><strong>The compute noted:</strong><ul>{b.warnings.map((w) => <li key={w}>{w}</li>)}</ul></div> : null}
      <div className="panel">
        <h3>Pages written in this book</h3>
        <p className="note">Pages this book does not write itself are found in its shelf, desk or kernel when you open them.</p>
        <table className="log">
          <thead><tr><th>Page</th><th>Title</th><th>Faces</th><th></th></tr></thead>
          <tbody>
            {b.pages.map((p) => (
              <tr key={p.page}>
                <td><Link href={`/page/${b.address}.${p.page}`}><code>{p.page}</code></Link></td>
                <td>{p.title ?? <em className="note">no title</em>}</td>
                <td>{p.faces.map((f) => <span key={f} className="chip">{f} {FACE_NAMES[f]?.name}</span>)}</td>
                <td><Link href={`/history/${b.address}.${p.page}`}>history</Link></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <Raw data={b} url={r.url} />
    </>
  );
}
