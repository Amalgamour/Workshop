// POST pass-through to the compute for the few POST routes it has. The app never writes books.
// It forwards the person's token (Authorization) and the content type unchanged; the compute decides.
import { COMPUTE_URL } from "@/lib/compute";

const ALLOWED = new Set(["propose", "ask", "ask/link", "close", "check.seq"]);

export async function POST(req: Request, { params }: { params: Promise<{ path: string[] }> }) {
  const { path } = await params;
  const route = path.join("/");
  if (!ALLOWED.has(route)) return Response.json({ error: "route", detail: `not passed through: ${route}` }, { status: 404 });
  const headers: Record<string, string> = { "content-type": req.headers.get("content-type") ?? "application/json" };
  const auth = req.headers.get("authorization");
  if (auth) headers.authorization = auth;
  try {
    const res = await fetch(`${COMPUTE_URL}/${route}`, { method: "POST", headers, body: await req.text(), cache: "no-store" });
    return new Response(await res.text(), { status: res.status, headers: { "content-type": res.headers.get("content-type") ?? "application/json" } });
  } catch (err) {
    return Response.json({ status: "rejected", error: "down", detail: `The compute is not answering: ${String((err as Error).message)}` }, { status: 503 });
  }
}
