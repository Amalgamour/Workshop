"""Hash the frozen case-b tree. Writes nothing in the repository."""
from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1] / "repository"
LIVE = Path(r"D:\Git\lib-build")
BOOK = REPO / "00.kernel" / "00.00.10.work"
EVID = BOOK / "0514.review-packet" / "evidence" / "build05.01"
PACK = BOOK / "0514.review-packet" / "evidence" / "pack05.01"


def digest(path: Path) -> tuple[str, int]:
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest(), len(data)


def check(label: str, path: Path, expect: str | None, expect_bytes: int | None) -> None:
    if not path.is_file():
        print(f"ABSENT {label} {path}")
        return
    got, size = digest(path)
    mark = "MATCH" if (expect is None or got == expect) and (expect_bytes is None or size == expect_bytes) else "DIFF"
    print(f"{mark} {label} {got} {size}")


def main() -> None:
    claims = {
        "return.md": ("b7c4fe25278f7fe09cc7fc18699bf06ab3034bb38abc6787360365e39d488fef", 2313),
        "06.01.md": ("9faced923ed6f4e300985106127fd8b6866789d2b95e45c8deb00b734ff06771", 5663),
        "CONTRACT.md": ("2d805f84ae9743b38ae07b0b376c1fa008623bbfeac9d594148ad3e6c1d9976a", 8314),
        "verification.json": ("d3f5b1fb6cdf3a4f2ee36e917a034f682c8e27cb70f848837eb98c79993e6e39", 1861),
        "REAL-USE.md": ("8e474e82e71948b4dd9a7c53160a7751eb2d6a8ab980d011421ee8d30709af75", 4065),
        "packet.json": ("bfcd0ee84d2505b06ebea0593bc66dc4504393ea966e357d58fae580ce98d6e4", 8393),
        "PACKET.md": ("83b4d69f95910aaca4af4e4400e0d72551265f3700599f1564305363f86e0f20", 1999),
        "artifact-manifest.json": ("3cdbc0a3b9497756d357fa824bdf67cbc11bcfd33c59c1c8f5117e1cee1daf7f", 4283),
        "specimen-0163/packet.json": ("c6eeaa6bfa5a1c03577152f6d4b4df5a33601fb7f67ef58bbbace23fbb5599ad", 57915),
        "specimen-0163/PACKET.md": ("2443bc01d88d00590adccc47fd6749be75b484e083d6aa7ff3b81edf2dea0c18", 25501),
        "review_packet.py": ("f658cbe48a3a76b908e5af0bcf0b7a68abc90571d983ca785e36667268f6ee72", 42694),
        "test_review_packet.py": ("b438f99bb5576b44c884974fd2e539113a9add16a806abaa726f5a287e691164", 20897),
        "source-manifest.json": ("8b03d471e212e5832c65dec95a7e07975160ed126df20ae01d92e33bbdb96b11", 3190),
    }
    paths = {
        "return.md": BOOK / "0167.review-packet-0501" / "return.md",
        "06.01.md": BOOK / "0514.review-packet" / "06.01.md",
        "CONTRACT.md": EVID / "CONTRACT.md",
        "verification.json": EVID / "verification.json",
        "REAL-USE.md": EVID / "REAL-USE.md",
        "packet.json": EVID / "packet.json",
        "PACKET.md": EVID / "PACKET.md",
        "artifact-manifest.json": EVID / "artifact-manifest.json",
        "specimen-0163/packet.json": EVID / "specimen-0163" / "packet.json",
        "specimen-0163/PACKET.md": EVID / "specimen-0163" / "PACKET.md",
        "review_packet.py": REPO / "labs" / "review-packet-pass01" / "review_packet.py",
        "test_review_packet.py": REPO / "labs" / "review-packet-pass01" / "tests" / "test_review_packet.py",
        "source-manifest.json": PACK / "source-manifest.json",
    }
    for label, (expect, size) in claims.items():
        check(label, paths[label], expect, size)

    receipt = BOOK / "0167.review-packet-0501" / "receipt.json"
    got, size = digest(receipt)
    page = "bf8cef9fe88b09316c69d4f1c37d824bc5b7378403d49ac3dccf486905fe0fff"
    print(f"{'MATCH' if got == page else 'DIFF'} receipt.json file {got} {size} page-pointer {page}")

    manifest = json.loads((BOOK / "0167.review-packet-0501" / "manifest.json").read_text(encoding="utf-8"))
    payload = BOOK / "0167.review-packet-0501" / "payload"
    bad = 0
    for source in manifest["sources"]:
        blob = payload / source["payload"]
        got, size = digest(blob)
        if got != source["sha256"] or size != source["bytes"]:
            bad += 1
            print(f"DIFF payload {source['payload']} {got} {size}")
    print(f"PAYLOADS {len(manifest['sources'])} bad {bad}")

    sources = json.loads((PACK / "source-manifest.json").read_text(encoding="utf-8"))
    bad = 0
    for source in sources["sources"]:
        blob = PACK / source["snapshot"]
        got, size = digest(blob)
        live = REPO / source["path"]
        live_state = "ABSENT"
        if live.is_file():
            live_digest, live_size = digest(live)
            live_state = "LIVE-MATCH" if live_digest == source["sha256"] and live_size == source["bytes"] else "LIVE-DIFF"
        if got != source["sha256"] or size != source["bytes"]:
            bad += 1
            print(f"DIFF snapshot {source['snapshot']} {got} {size}")
        print(f"SNAPSHOT {source['snapshot']} {live_state} {source['path']}")
    print(f"SNAPSHOTS {len(sources['sources'])} bad {bad}")

    art = json.loads((EVID / "artifact-manifest.json").read_text(encoding="utf-8"))
    bad = 0
    for row in art["artifacts"]:
        path = REPO / row["path"]
        if not path.is_file():
            bad += 1
            print(f"ABSENT artifact {row['path']}")
            continue
        got, size = digest(path)
        if got != row["sha256"] or size != row["bytes"]:
            bad += 1
            print(f"DIFF artifact {row['path']} {got} {size}")
    print(f"ARTIFACT_ROWS {len(art['artifacts'])} bad {bad}")

    nominated = json.loads((EVID / "packet.json").read_text(encoding="utf-8"))
    print(
        "NOMINATED",
        "acceptance", nominated["acceptance"],
        "semantic_review", nominated["semantic_review"],
        "next_task", nominated["next_task"],
        "custody", nominated["custody"]["status"],
    )
    specimen = json.loads((EVID / "specimen-0163" / "packet.json").read_text(encoding="utf-8"))
    counts: Counter[str] = Counter()
    for check_item in specimen["artifact_checks"]:
        for row in check_item.get("rows", []):
            counts[row["classification"]] += 1
        print(
            "CHECK",
            check_item["source"],
            check_item["result"],
            "rows", len(check_item.get("rows", [])),
            "schema", check_item.get("observed_schema"),
        )
    print("CLASS_COUNTS", dict(counts))
    absent = next(item for item in specimen["sources"] if item["id"] == "manifest-at-claimed-head")
    print("ABSENT_BLOB", absent["status"], absent["problems"], "live_opened", absent["live_opened"])
    print(
        "SPECIMEN",
        "acceptance", specimen["acceptance"],
        "custody", specimen["custody"]["status"],
        "conflicts", specimen["origin_conflicts"],
    )

    pins = {
        "helper": ("8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac", 45767),
        "inspector": ("947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b", 11402),
    }
    for label, (expect, size) in pins.items():
        name = "return_capture.py" if label == "helper" else "return_inspect.py"
        check(f"frozen-{label}", REPO / "labs" / "return-capture-pass01" / name, expect, size)
        check(f"live-{label}", LIVE / "labs" / "return-capture-pass01" / name, expect, size)

    code = (REPO / "labs" / "review-packet-pass01" / "review_packet.py").read_text(encoding="utf-8")
    print("CORRUPTION_WORD", "corruption" in code.lower())
    for member in ("0163.prime-bench-harness-0501", "0164.prime-entry-pin-repair-0503"):
        print(f"MEMBER_IN_FIXTURE {member} {(BOOK / member).is_dir()}")
    for commit in (
        "749cfd9c670fe77fbedd232c2630f98b0529025d",
        "80f7025425d7bb3fdcf3b0ee56057cd6d8b6b9fe",
    ):
        proc = subprocess.run(
            ["git", "cat-file", "-t", commit],
            cwd=REPO,
            capture_output=True,
            text=True,
        )
        print(f"GIT {commit} exit {proc.returncode} {(proc.stdout or proc.stderr).strip()}")


if __name__ == "__main__":
    main()
