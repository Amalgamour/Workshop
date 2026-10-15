# Syntax 0010.about — proof and sentinel are conflated

chain: 2.7.8
severity: conflicting construction instruction
confidence: high

## Chain
0010/01.003 How to read a page -> syntax 0001/01.007 Furniture -> syntax 0014/01.007 00.md -> law 0018/01 Proof.

## Break
The about draft says `00 is the proof of the container, not a face.` The actual proof is address.proof; 00.md is the sentinel and is explicitly not that proof. A reader using this instruction can build or verify the wrong artifact.

The same draft says `It does not list the sections. That is 0011.` Inside this book, 0011 is an intentional hole. The sentence fails to qualify the law-book contents reference. This is an ambiguous local reference, not a request to fill the hole or a defect against a withheld file.

## Repair — difference only
Replace the 00 clause with `00.md is the container sentinel, outside page faces; the container proof is address.proof.` Preserve the shelf-00 exception by pointing to its governing source rather than guessing a second proof.
Qualify the contents pointer as law book 0011.contents. Keep syntax 0011 empty. Do not assign a job to any reserved 07 slot or add an address axis.
