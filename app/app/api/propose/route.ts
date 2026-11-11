// POST pass-through to the compute's queue. The app never writes books; the compute validates and writes.
import { COMPUTE_URL } from "@/lib/compute";

export async function POST(req: Request) {
  const body = await req.text();
  try {
    const res = await fetch(`${COMPUTE_URL}/propose`, { method: "POST", headers: { "content-type": "application/json" }, body, cache: "no-store" });
    return new Response(await res.text(), { status: res.status, headers: { "content-type": "application/json" } });
  } catch (err) {
    return Response.json({ status: "rejected", error: "down", detail: String((err as Error).message) }, { status: 503 });
  }
}
