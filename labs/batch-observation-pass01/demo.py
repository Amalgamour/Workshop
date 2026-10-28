"""One real-page observation. Read-only. Prints batch-observation/1 JSON."""

from __future__ import annotations

import sys
from pathlib import Path

LAB = Path(__file__).resolve().parent
sys.path.insert(0, str(LAB))

import batch_observe

ROOT = Path(__file__).resolve().parents[2]
COMMIT = "4cca1d2e9ac845e82a2d44df432f8f7f6584f1e5"
PAGE = "00.kernel/00.00.10.work/0508.return-capture/05.10.md"
BOOK = ROOT / "00.kernel" / "00.00.10.work"


def main() -> int:
    return batch_observe.main(
        [
            "observe",
            "--repo",
            str(ROOT),
            "--commit",
            COMMIT,
            "--path",
            PAGE,
            "--members-book",
            str(BOOK),
            "--json",
        ]
    )


if __name__ == "__main__":
    sys.exit(main())
