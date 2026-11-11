// Read-only pass-through so the browser word box can ask the compute. GET only.
import { COMPUTE_URL } from "@/lib/compute";

const ALLOWED = new Set(["brands", "links", "page", "face", "cards", "history", "queue", "book", "books"]);

export async function GET(req: Request, { params }: { params: Promise<{ path: string[] }> }) {
  const { path } = await params;
  if (!ALLOWED.has(path[0])) return Response.json({ error: "route", detail: "not passed through" }, { status: 404 });
  const q = new URL(req.url).search;
  try {
    const res = await fetch(`${COMPUTE_URL}/${path.map(encodeURIComponent).join("/")}${q}`, { cache: "no-store" });
    return new Response(await res.text(), { status: res.status, headers: { "content-type": "application/json" } });
  } catch (err) {
    return Response.json({ error: "down", detail: String((err as Error).message) }, { status: 503 });
  }
}
