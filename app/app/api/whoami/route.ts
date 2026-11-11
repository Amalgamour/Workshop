// GET pass-through to the compute's GET /whoami (CONTRACT addendum, FOLLOWUPS). Read-only.
// It forwards the person's token (Authorization) unchanged; the compute answers with the name only, never the token.
import { COMPUTE_URL } from "@/lib/compute";

export async function GET(req: Request) {
  const headers: Record<string, string> = {};
  const auth = req.headers.get("authorization");
  if (auth) headers.authorization = auth;
  try {
    const res = await fetch(`${COMPUTE_URL}/whoami`, { headers, cache: "no-store" });
    return new Response(await res.text(), { status: res.status, headers: { "content-type": "application/json" } });
  } catch (err) {
    return Response.json({ error: "down", detail: String((err as Error).message) }, { status: 503 });
  }
}
