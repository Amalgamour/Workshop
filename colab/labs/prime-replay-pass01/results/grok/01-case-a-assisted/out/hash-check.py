"""Self-reported hash check for case-a. Writes nothing in the repository."""
import hashlib
import json
from pathlib import Path

root = Path(r"D:\Git\lib-build\colab\labs\prime-replay-pass01\runs\grok\01-case-a-assisted\repository")

def digest(path: Path):
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest(), len(data)

claimed = {
    "00.kernel/00.00.10.work/0513.bench-build/06.01.md": ("537480d4c5d8035014d5c68df46b604bdf83348a9a1579af37295307240bbbb3", 10070),
    "00.kernel/00.00.10.work/0513.bench-build/evidence/build05.01/CONTRACT.md": ("68add992c3b3769e6f89286f358138970302d0361884421cf5378d3afc434b3e", 10806),
    "00.kernel/00.00.10.work/0513.bench-build/evidence/build05.01/verification.json": ("d9c2fd4e9a700d13aede26976d4f8ae4a11a9fed50e21564f3a40608ada895d6", 130259),
    "00.kernel/00.00.10.work/0513.bench-build/evidence/build05.01/RUN-GUIDE.md": ("26235db45d4cf00fdfcef6be8e80523ab532e601676c6078a2ce09cf2d4c4627", 4732),
    "00.kernel/00.00.10.work/0513.bench-build/evidence/build05.01/artifact-manifest.json": ("da06ab6cfdee15497c1d19394fb9e22433e5c1db6623a3fd8462d20749274634", 14030),
    "00.kernel/00.00.10.work/0513.bench-build/evidence/build05.01/sample-report.md": ("dcd33eb45b8c2397b9dd2577e636992b2c980a30c669281ed5acca72eb2f0d78", 6028),
    "labs/prime-bench-pass01/prime_bench.py": ("258727eef76693583ab0b88813c1b5afbded0009561f43c9bb61797b9d4dd650", 68800),
    "labs/prime-bench-pass01/tests/test_prime_bench.py": ("5c125c3b4cc8ff5a72838fd83f0f7d88e55903f34b558f5deece187d4ca09ec9", 42700),
    "00.kernel/00.00.10.work/0163.prime-bench-harness-0501/return.md": ("742beefbf856429ce3dfcf59e675a06f618c1b75b74f8f09b87c67dc6575198e", 6655),
}
print("LIVE_VS_CLAIM")
for rel, (want_sha, want_len) in claimed.items():
    path = root / rel
    if not path.is_file():
        print("MISSING", rel)
        continue
    got_sha, got_len = digest(path)
    print(("MATCH" if got_sha == want_sha and got_len == want_len else "DIFFER"), got_sha, got_len, rel)

bench = root / "labs/prime-bench-pass01/bench.json"
bsha, blen = digest(bench)
print("BENCH", bsha, blen, "want f00c6f29f35edd27465b2bbf5e4023323d8f028c4c6d8291ef1fe85db39fe9d1")

manifest = json.loads((root / "00.kernel/00.00.10.work/0513.bench-build/evidence/pack05.01.002/source-manifest.json").read_text(encoding="utf-8"))
print("PACK_SNAPSHOTS")
base = root / "00.kernel/00.00.10.work/0513.bench-build/evidence/pack05.01.002"
for row in manifest["sources"]:
    blob = base / row["snapshot"]
    if not blob.is_file():
        print("MISSING", row["snapshot"], row["path"])
        continue
    got_sha, got_len = digest(blob)
    live = root / row["path"]
    live_state = "absent"
    if live.is_file():
        lsha, llen = digest(live)
        live_state = "live-match" if (lsha, llen) == (got_sha, got_len) else "live-differ"
    print(("PIN-MATCH" if got_sha == row["sha256"] and got_len == row["bytes"] else "PIN-DIFFER"), live_state, row["path"])
print("PACK_COUNT", len(manifest["sources"]))
print("METHOD_PAGE", (root / "00.kernel/00.00.10.work/0414.bench/01.md").is_file())
