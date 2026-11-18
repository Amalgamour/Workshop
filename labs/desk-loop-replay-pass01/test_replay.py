"""Route tests for the desk-loop replay. They call the existing CLIs through replay.py."""

import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import replay  # noqa: E402

TRANSCRIPT = Path(
    r"D:\Git\lib-build\00.kernel\00.00.10.work\0520.desk-loop-lab\evidence\build05.01\transcript.json"
)


class ReplayRoute(unittest.TestCase):
    def test_supported_loop_and_adverse_cases(self):
        report = replay.run_all()
        TRANSCRIPT.write_bytes((json.dumps(report, indent=1) + "\n").encode("utf-8"))
        failed = [item for item in report["checks"] if not item["ok"]]
        self.assertFalse(failed, json.dumps(failed, indent=1))
        self.assertEqual(len(report["checks"]), 16)


if __name__ == "__main__":
    unittest.main()
