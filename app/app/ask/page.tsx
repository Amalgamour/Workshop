import { get, withDraftReasons, type PageDetail } from "@/lib/compute";
import { Header } from "@/components/ui";
import { AskBox, type QuestionCard } from "@/components/AskBox";
import { QueueResult } from "@/components/QueueResult";
import { parseCards } from "@/lib/seq";

export const dynamic = "force-dynamic";

// 7: the common-questions page is 0013 in the reader book (COMPUTE choice); READER_BOOK default 10.11.21 as in scripts/dev.sh.
const BOOK = process.env.READER_BOOK ?? "10.11.21";

export default async function Ask({ searchParams }: { searchParams: Promise<{ q?: string; done?: string }> }) {
  const sp = await searchParams;
  const pr = await get<PageDetail>(`/page/${BOOK}.0013`);
  const questions: QuestionCard[] = [];
  if (pr.kind === "ok") {
    const p = await withDraftReasons(pr.data);
    for (const [k, f] of Object.entries(p.faces)) {
      if (!/^01(\.draft)?$/.test(k)) continue;
      for (const c of parseCards(f.body).cards) {
        const fields = Object.fromEntries(c.fields);
        if (fields.type !== "question") continue;
        questions.push({ address: `${BOOK}.0013.01.${c.key}`, title: c.title, forms: fields.forms ?? "", answer: fields.answer ?? "", draft: k.endsWith(".draft") });
      }
    }
  }
  const byAddr = new Map(questions.map((q) => [q.address, q]));
  return (
    <>
      <Header title="Ask" lede="Type a question the way you would say it. The compute picks out the few important words, matches them to your common questions and your words, and hands back 1 to 3 pieces. If nothing fits, it asks you to say more (R11)." />
      <QueueResult id={sp.done} />
      <AskBox initial={sp.q ?? "what is my name"} questions={[...byAddr.values()]} book={BOOK} />
    </>
  );
}
