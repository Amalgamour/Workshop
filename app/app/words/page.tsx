import { Header } from "@/components/ui";
import { WordBox } from "@/components/WordBox";

export default function Words() {
  return (
    <>
      <Header title="Word lookup" lede="Type as you normally would. Each word is checked against your dictionaries. Words you have given your own meaning (brands) light up, with the pages they link to." />
      <WordBox initial="Start the timer run in colab, then get ham for lunch with Ham from work." />
    </>
  );
}
