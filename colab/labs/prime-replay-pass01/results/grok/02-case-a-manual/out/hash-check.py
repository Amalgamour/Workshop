"""Manual-route hash check. Does not call the Prime assistance bundle."""
import hashlib
import json
from pathlib import Path

root = Path(r"D:\Git\lib-build\colab\labs\prime-replay-pass01\runs\grok\02-case-a-manual\repository")

def digest(path: Path):
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest(), len(data)

claimed = {
    "00.kernel/00.00.10.work/0163.prime-bench-harness-0501/return.md": "742beefbf856429ce3dfcf59e675a06f618c1b75b74f8f09b87c67dc6575198e",
    "00.kernel/00.00.10.work/0163.prime-bench-harness-0501/receipt.json": None,
    "labs/prime-bench-pass01/bench.json": "f00c6f29f35edd27465b2bbf5e4023323d8f028c4c6d8291ef1fe85db39fe9d1",
    "labs/prime-bench-pass01/prime_bench.py": "258727eef76693583ab0b88813c1b5afbded0009561f43c9bb61797b9d4dd650",
    "labs/prime-bench-pass01/cases/design-fork-a/evaluator/key.json": None,
    "labs/prime-bench-pass01/cases/complete-a/evaluator/key.json": None,
}
for rel, want in claimed.items():
    path = root / rel
    if not path.is_file():
        print("MISSING", rel)
        continue
    got, n = digest(path)
    flag = "UNCOMPARED" if want is None else ("MATCH" if got == want else "DIFFER")
    print(flag, got, n, rel)

receipt = json.loads((root / "00.kernel/00.00.10.work/0163.prime-bench-harness-0501/receipt.json").read_text(encoding="utf-8"))
print("RECEIPT_FIELDS", receipt.get("submission_id"), receipt.get("manifest_sha256"))
print("METHOD_LIVE", (root / "00.kernel/00.00.10.work/0414.bench/01.md").is_file())
print("SUPPORT_LIVE", (root / "labs/prime-review-pass01/prime_review.py").is_file())
