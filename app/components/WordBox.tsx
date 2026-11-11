"use client";
import Link from "next/link";
import { useEffect, useMemo, useRef, useState } from "react";
import type { Brand, Links } from "@/lib/compute";

type Lookup = { state: "loading" } | { state: "done"; brands: Brand[] } | { state: "down"; detail: string };
const WORD = /[A-Za-z][A-Za-z0-9-]*/g;

export function WordBox({ initial }: { initial: string }) {
  const [text, setText] = useState(initial);
  const [found, setFound] = useState<Record<string, Lookup>>({});
  const [sel, setSel] = useState<string | null>(null);
  const [web, setWeb] = useState<Record<string, Links | "missing">>({});
  const asked = useRef(new Set<string>());
  const askedLinks = useRef(new Set<string>());

  const words = useMemo(() => [...new Set(text.match(WORD) ?? [])].filter((w) => w.length >= 2), [text]);

  useEffect(() => {
    const t = setTimeout(() => {
      for (const w of words) {
        if (asked.current.has(w)) continue;
        asked.current.add(w);
        setFound((f) => ({ ...f, [w]: { state: "loading" } }));
        fetch(`/api/compute/brands?q=${encodeURIComponent(w)}`)
          .then(async (r) => (r.ok ? { state: "done", brands: (await r.json()) as Brand[] } : { state: "down", detail: (await r.json().catch(() => ({})))?.detail ?? r.statusText }))
          .catch((e) => ({ state: "down", detail: String(e) }))
          .then((v) => setFound((f) => ({ ...f, [w]: v as Lookup })));
      }
    }, 250);
    return () => clearTimeout(t);
  }, [words]);

  const special = words.filter((w) => { const l = found[w]; return l?.state === "done" && l.brands.length > 0; });
  const down = Object.values(found).find((l) => l.state === "down") as { detail: string } | undefined;
  const active = sel && special.includes(sel) ? sel : special[0] ?? null;
  const brands = active ? (found[active] as { brands: Brand[] }).brands : [];

  useEffect(() => {
    for (const b of brands) {
      const p = b.page ?? b.brand.split(".").slice(0, 4).join(".");
      if (askedLinks.current.has(p)) continue;
      askedLinks.current.add(p);
      fetch(`/api/compute/links/${p}`)
        .then(async (r) => { const v: Links | "missing" = r.ok ? ((await r.json()) as Links) : "missing"; setWeb((w) => ({ ...w, [p]: v })); })
        .catch(() => {});
    }
  }, [brands]);

  const parts: React.ReactNode[] = [];
  let last = 0;
  for (const m of text.matchAll(WORD)) {
    const w = m[0], i = m.index ?? 0;
    parts.push(text.slice(last, i));
    parts.push(special.includes(w)
      ? <mark key={i} className={`brand ${w === active ? "sel" : ""}`} onClick={() => setSel(w)}>{w}</mark>
      : w);
    last = i + w.length;
  }
  parts.push(text.slice(last));

  // Which brand to state back: one whose forms hold exactly what was typed, else the dictionary default.
  // Provisional (BUILD-LOG 7): brands.md step 1 uses meters and step 2 the session, which the reader does not have.
  const taken = brands.filter((b) => b.exact_form).length === 1 ? brands.find((b) => b.exact_form) : brands.find((b) => b.is_default);

  return (
    <>
      <textarea className="big" rows={3} value={text} onChange={(e) => setText(e.target.value)} aria-label="type here" placeholder="Type a sentence. Your special words light up." />
      {down ? <div className="down" style={{ marginTop: 12 }}><strong>The compute is not answering.</strong> <span className="note">{down.detail}</span></div> : null}
      <div className="panel" style={{ marginTop: 16 }}>
        <h3>What you typed <span className="note">(yellow = a word with your own meaning. Click one.)</span></h3>
        <div className="typed">{parts}</div>
        {special.length === 0 ? <p className="note">No special words found yet. Words with no brand use their ordinary meaning.</p> : null}
      </div>
      {active ? (
        <div className="panel">
          <h3>&ldquo;{active}&rdquo; — {brands.length} meaning{brands.length === 1 ? "" : "s"} on record</h3>
          {taken ? <p>Stated back: <b>{active}</b>, taken as <code>{taken.brand_id}</code>, {taken.why ?? "meaning not written"}.
            <span className="note"> ({taken.exact_form ? "the form you typed matches" : "the dictionary default"})</span></p> : null}
          {brands.map((b) => {
            const p = b.page ?? b.brand.split(".").slice(0, 4).join(".");
            const w = web[p];
            return (
              <div className="card" key={b.brand}>
                <h4><code>{b.brand_id ?? b.brand}</code> {b.title ?? ""}
                  {b.is_default ? <span className="chip">default</span> : null}
                  {b.exact_form ? <span className="chip">form matches</span> : null}
                </h4>
                {b.missing ? <p className="note"><b>7</b> The dictionary points to a card that cannot be opened.</p> : <p style={{ margin: "4px 0" }}><b>Means:</b> {b.why ?? "7 not written"}</p>}
                {b.forms?.length ? <p className="note" style={{ margin: 0 }}>Forms: {b.forms.join(", ")} (case matters)</p> : null}
                <p style={{ margin: "8px 0" }}>Card: <Link href={`/page/${p}?face=01#${active.toLowerCase()}`}><code>{b.brand}</code></Link>{b.dictionary ? <span className="note"> · found through the dictionary <code>{b.dictionary}</code></span> : null}</p>
                <div>
                  <b>Connect web</b> <span className="note">(pages linked to this one)</span>
                  {!w ? <p className="note">loading…</p> : w === "missing" ? <p className="note">7 no links found</p> : (
                    <ul style={{ margin: "4px 0" }}>
                      {w.forward.map((a) => <li key={`f${a}`}>→ {w.missing.includes(a) ? <><code>{a}</code> <span className="badge missing">missing</span></> : <Link href={`/page/${a}`}><code>{a}</code></Link>}</li>)}
                      {w.back.map((a) => <li key={`b${a}`}>← <Link href={`/page/${a}`}><code>{a}</code></Link></li>)}
                      {w.forward.length + w.back.length === 0 ? <li className="note">no links written</li> : null}
                    </ul>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      ) : null}
    </>
  );
}
