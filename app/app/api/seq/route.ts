// Download a page as a .seq file: GET /page.seq?addr= on the compute (CONTRACT addendum, SEQPAGE lane; proposed). Read-only.
import { COMPUTE_URL } from "@/lib/compute";

export async function GET(req: Request) {
  const addr = new URL(req.url).searchParams.get("addr") ?? "";
  try {
    const res = await fetch(`${COMPUTE_URL}/page.seq?addr=${encodeURIComponent(addr)}`, { cache: "no-store" });
    const headers = new Headers({ "content-type": res.headers.get("content-type") ?? "text/plain; charset=us-ascii" });
    const cd = res.headers.get("content-disposition");
    headers.set("content-disposition", cd ?? `attachment; filename="${addr}.seq"`);
    if (!res.ok) headers.delete("content-disposition");
    return new Response(await res.text(), { status: res.status, headers });
  } catch (err) {
    return Response.json({ error: "down", detail: String((err as Error).message) }, { status: 503 });
  }
}
