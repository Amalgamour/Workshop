import Link from "next/link";
import { get, type BookSummary } from "@/lib/compute";
import { Header, NotOk, Raw } from "@/components/ui";

export const dynamic = "force-dynamic";

export default async function Desks() {
  const r = await get<BookSummary[]>("/books");
  const head = <Header title="Desks" lede="Pick a desk to work on." />;
  if (r.kind !== "ok") return <>{head}<NotOk r={r} what="desks" /></>;
  const desks = [...new Set(r.data.map((b) => b.address.slice(0, 2)))].sort();
  return (
    <>{head}
      <div className="cols">{desks.map((d) => (
        <Link key={d} href={`/desk/${d}`} className="panel" style={{ textDecoration: "none", color: "inherit" }}>
          <h3><code>{d}</code> {r.data.find((b) => b.address === `${d}.00.00`)?.title ?? "7 no door book"}</h3>
          <p className="note">{r.data.filter((b) => b.address.startsWith(d + ".")).length} book(s){d === "00" ? " · the kernel" : ""}</p>
        </Link>))}
      </div>
      <Raw data={r.data} url={r.url} />
    </>
  );
}
