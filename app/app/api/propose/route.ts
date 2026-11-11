// POST pass-through to the compute's queue. The app never writes books; the compute validates and writes.
import { COMPUTE_URL } from "@/lib/compute";

export async function POST(req: Request) {
  const body = await req.text();
  // Same-origin only: a cross-site page may not write through the app (TRIAL-X #3).
  const origin = req.headers.get("origin");
  if (origin && origin !== new URL(req.url).origin) {
    return Response.json({ status: "rejected", error: "origin", detail: "cross-site writes are refused" }, { status: 403 });
  }
  const ct = (req.headers.get("content-type") ?? "").split(";")[0].trim().toLowerCase();
  if (ct !== "application/json" && ct !== "text/x-seqpage") {
    return Response.json({ status: "rejected", error: "media", detail: "send application/json or text/x-seqpage" }, { status: 415 });
  }
  const headers: Record<string, string> = { "content-type": ct };
  const auth = req.headers.get("authorization");
  if (auth) headers.authorization = auth;
  try {
    const res = await fetch(`${COMPUTE_URL}/propose`, { method: "POST", headers, body, cache: "no-store" });
    return new Response(await res.text(), { status: res.status, headers: { "content-type": "application/json" } });
  } catch (err) {
    return Response.json({ status: "rejected", error: "down", detail: String((err as Error).message) }, { status: 503 });
  }
}
