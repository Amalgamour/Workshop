// The only way the app reads data: the compute HTTP API (docs/CONTRACT.md).
export const COMPUTE_URL = (process.env.COMPUTE_URL ?? "http://127.0.0.1:7700").replace(/\/$/, "");

export type Result<T> =
  | { kind: "ok"; data: T; url: string }
  | { kind: "missing"; detail?: string; body?: unknown; url: string }
  | { kind: "error"; status: number; detail: string; url: string }
  | { kind: "down"; detail: string; url: string };

export async function get<T>(path: string): Promise<Result<T>> {
  const url = `${COMPUTE_URL}${path}`;
  try {
    const res = await fetch(url, { cache: "no-store" });
    const body = await res.json().catch(() => null);
    if (res.ok) return { kind: "ok", data: body as T, url };
    if (res.status === 404 && body?.error === "missing") return { kind: "missing", detail: body?.detail, body, url };
    return { kind: "error", status: res.status, detail: body?.detail ?? body?.error ?? res.statusText, url };
  } catch (err) {
    return { kind: "down", detail: String((err as Error)?.message ?? err), url };
  }
}

export type BookSummary = { address: string; title: string | null; pages: number };
export type BookDetail = { address: string; title: string | null; pages: { page: string; title: string | null; faces: string[] }[]; warnings?: string[] };
export type DraftWhy = { opened_by_entry?: number; reason?: string; has_seated?: boolean; open_notes?: { n: number; by: string; text: string }[]; merged_notes?: number };
export type FaceView = { body: string; tail?: string; source: string; resolved_from?: string; n?: number; by?: string; at?: string; state?: string; why_draft?: DraftWhy; derived?: string };
export type PageDetail = { address: string; title: string | null; faces: Record<string, FaceView>; inherited: string[]; boards?: Record<string, { counter: string; tail: string | null }[]> };
export type TraceStep = { step: number | string; checked: string; found: boolean; level?: string };
export type LogEntry = { n: number; at: string; by: string; op: string; addr: string; tail?: string; from?: string; to?: string; body?: string; proposal?: string; book?: string; cites?: number; outcome?: string; reason?: string; "approved-by"?: string; trial?: string };
export type Links = { forward: string[]; back: string[]; missing: string[]; one_way?: string[] };
export type Brand = { word: string; brand: string; brand_id?: string; title: string | null; why: string | null; page?: string; is_default?: boolean; exact_form?: boolean | null; missing?: boolean; dictionary?: string; forms?: string[] };
export type CardHit = { address: string; face: string; face_no?: string; page_title?: string | null; title: string; key: string; fields: Record<string, string>; body: string; tail?: string | null };

/** R5: a draft must show why it is a draft. /page gives why_draft without the opening entry's reason, so read it from history. */
export async function withDraftReasons(p: PageDetail): Promise<PageDetail> {
  const need = Object.entries(p.faces).filter(([, f]) => f.why_draft && !f.why_draft.reason && f.why_draft.opened_by_entry);
  const pages = [...new Set(need.map(([, f]) => f.source.split(".").slice(0, 4).join(".")))];
  const hist = new Map<string, LogEntry[]>();
  await Promise.all(pages.map(async (pa) => { const h = await get<LogEntry[]>(`/history/${pa}`); if (h.kind === "ok") hist.set(pa, h.data); }));
  for (const [, f] of need) {
    const pa = f.source.split(".").slice(0, 4).join(".");
    const book = f.source.split(".").slice(0, 3).join(".");
    const e = hist.get(pa)?.find((x) => x.n === f.why_draft!.opened_by_entry && (!x.book || x.book === book));
    if (e?.reason) f.why_draft = { ...f.why_draft, reason: e.reason };
  }
  return p;
}
