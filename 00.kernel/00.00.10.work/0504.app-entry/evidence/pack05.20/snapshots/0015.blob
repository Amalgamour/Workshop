"""Fixture proof for the disposable capture-flow rehearsal.

Expected refusals are counted apart from passes. These checks are not a sandbox.
The accepted app, Clerk, bridge, and handoff files are not edited.
"""

from __future__ import annotations

import os
import sys
import traceback
from pathlib import Path


sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "labs" / "capture-flow-rehearsal-pass01"))
import rehearse  # noqa: E402


class Suite:
    def __init__(self) -> None:
        self.passed: list[str] = []
        self.refusals: list[str] = []
        self.skipped: list[str] = []
        self.failed: list[str] = []

    def ok(self, name: str) -> None:
        self.passed.append(name)
        print(f"PASS {name}", flush=True)

    def refusal(self, name: str) -> None:
        self.refusals.append(name)
        print(f"REFUSAL {name}", flush=True)

    def fail(self, name: str, detail: str) -> None:
        self.failed.append(name)
        print(f"FAIL {name}: {detail}", flush=True)


SUITE = Suite()


def run(name: str, fn, kind: str) -> None:
    try:
        result = fn()
    except Exception as exc:
        SUITE.fail(name, traceback.format_exc())
        return
    if result.get("expected") != kind:
        SUITE.fail(name, f"expected {kind}, got {result.get('expected')}")
        return
    if kind == "refusal":
        SUITE.refusal(name)
    else:
        SUITE.ok(name)


def main() -> int:
    before = rehearse.live_hashes()
    view = rehearse.open_view()
    try:
        run("closure", lambda: rehearse.prove_closure(view), "pass")
        run("malformed-binding", lambda: rehearse.prove_malformed(view), "refusal")
        run("unsafe-path", lambda: rehearse.prove_unsafe(view), "refusal")
        run("failed-pin", lambda: rehearse.prove_bad_pin(view), "refusal")
        success = {}
        try:
            success = rehearse.prove_success(view)
        except Exception:
            SUITE.fail("complete-flow", traceback.format_exc())
        else:
            for name in ("complete", "repetition", "changed-binding", "changed-payload"):
                kind = "pass" if name in ("complete", "repetition") else "refusal"
                run(name if name != "complete" else "complete-flow", lambda item=success[name]: item, kind)
            identities = success["complete"]["identities"]
            print(f"event {identities['returned_event_sha256']}", flush=True)
            print(f"receipt {identities['receipt_sha256']}", flush=True)
            print(f"report {identities['report_sha256']}", flush=True)
            print(f"launches {identities['launches']}", flush=True)
        run("failed-delivery", lambda: rehearse.prove_failed(view), "refusal")
        stopped = {}
        try:
            stopped = rehearse.prove_stop(view)
        except Exception:
            SUITE.fail("stop-after-capture", traceback.format_exc())
        else:
            run("stop-after-capture", lambda: stopped["stop-after-capture"], "refusal")
            run("stop-retry", lambda: stopped["stop-retry"], "refusal")
            print(f"stop-member {stopped['stop-after-capture']['identities']['member']}", flush=True)
            print(f"stop-receipt {stopped['stop-after-capture']['identities']['receipt_sha256']}", flush=True)
    finally:
        rehearse.remove_owned(view.home)
    after = rehearse.live_hashes()
    if before != after:
        changed = [key for key in before if before[key] != after.get(key)]
        SUITE.fail("live-bytes-unchanged", "changed " + ", ".join(changed))
    else:
        SUITE.ok("live-bytes-unchanged")
    print(
        f"summary pass {len(SUITE.passed)} expected-refusal {len(SUITE.refusals)} "
        f"skip {len(SUITE.skipped)} fail {len(SUITE.failed)}",
        flush=True,
    )
    return 1 if SUITE.failed else 0


if __name__ == "__main__":
    sys.exit(main())
