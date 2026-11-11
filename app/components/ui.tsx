import Link from "next/link";
import { AXES, SOURCE_PLAIN, TAIL_PLAIN } from "@/lib/seq";
import type { Result } from "@/lib/compute";

/** An address, with each part labelled in plain words underneath. */
export function Addr({ a, link }: { a: string; link?: boolean }) {
  const parts = a.split(".");
  const labels = labelParts(parts);
  const inner = (
    <span className="addr" title={a}>
      {parts.map((p, i) => (
        <span key={i}><code>{p}</code><small>{labels[i]}</small></span>
      ))}
    </span>
  );
  if (!link) return inner;
  const pageAddr = parts.slice(0, 4).join(".");
  return <Link href={parts.length >= 4 ? `/page/${pageAddr}${parts[4] ? `?face=${parts[4]}` : ""}` : `/book/${parts.slice(0, 3).join(".")}`} style={{ textDecoration: "none" }}>{inner}</Link>;
}
function labelParts(parts: string[]) {
  let numeric = 0;
  return parts.map((p) => {
    if (/^\d\d$/.test(p) && numeric < 3) return AXES[numeric++];
    if (/^\d{4}$/.test(p)) { numeric = 4; return "page"; }
    if (/^\d\d$/.test(p) && numeric === 4) { numeric = 5; return "face"; }
    if (/^\d\d$/.test(p) && numeric === 5) { numeric = 6; return "counter"; }
    if (/^\d{3}$/.test(p)) return "brand no.";
    if (["draft", "retired", "pack", "open", "return", "review"].includes(p)) return "tail";
    return numeric >= 5 ? "card" : "title";
  });
}

export function SourceBadge({ from, source }: { from?: string; source?: string }) {
  const f = from ?? "local";
  return <span className={`badge ${f}`}><b>{f === "local" ? "Local" : f === "missing" ? "Missing" : `Inherited (${f})`}</b> {SOURCE_PLAIN[f] ?? f}{source && f !== "local" ? <> · from <code>{source}</code></> : null}</span>;
}
export function TailBadge({ tail }: { tail?: string | null }) {
  const t = tail ?? "seated";
  return <span className={`badge ${t === "seated" ? "seated" : "tail"}`}><b>{t}</b> {TAIL_PLAIN[t] ?? ""}</span>;
}

export function Hole({ what, why, traceHref }: { what: string; why?: string; traceHref?: string }) {
  return (
    <div className="hole">
      <span className="seven" aria-label="axiom 7, missing">7</span>
      <div style={{ overflow: "hidden" }}>
        <strong>Missing: {what}</strong>
        <p style={{ margin: "6px 0" }}>{why ?? "Nothing is written here. That is allowed."}</p>
        <p className="note" style={{ margin: 0 }}>Axiom 7 (Missing): a hole nothing requires stays empty, a header and a why. It is shown, never invented.{traceHref ? <> <Link href={traceHref}>See where we looked →</Link></> : null}</p>
      </div>
    </div>
  );
}

export function Raw({ data, url }: { data: unknown; url?: string }) {
  return (
    <details className="raw">
      <summary>Check it yourself: the raw answer from the compute{url ? <> (<code>{url}</code>)</> : null}</summary>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </details>
  );
}

export function NotOk({ r, what }: { r: Exclude<Result<unknown>, { kind: "ok" }>; what: string }) {
  if (r.kind === "missing") return <Hole what={what} why={r.detail ?? "The compute has nothing at this address."} />;
  if (r.kind === "down")
    return (
      <div className="down">
        <strong>The compute is not answering.</strong>
        <p style={{ margin: "6px 0" }}>The reader only shows what the compute gives it, so there is nothing to show yet.</p>
        <p className="note" style={{ margin: 0 }}>Start it, or start the mock: <code>npm run mock</code> in <code>app/</code>. Tried: <code>{r.url}</code></p>
      </div>
    );
  return <div className="down"><strong>The compute said no ({r.status}).</strong><p className="note">{r.detail} · <code>{r.url}</code></p></div>;
}

export function Header({ title, lede }: { title: React.ReactNode; lede?: React.ReactNode }) {
  return <><h2 className="title">{title}</h2>{lede ? <p className="lede">{lede}</p> : null}</>;
}
