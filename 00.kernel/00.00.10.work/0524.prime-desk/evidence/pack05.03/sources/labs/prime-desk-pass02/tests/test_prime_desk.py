#!/usr/bin/env python3
"""Fixture tests for canonical Prime desk selection."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(LAB, "..", ".."))
sys.path.insert(0, LAB)

import prime_desk as pd

PY = sys.executable
PACK = os.path.join(ROOT, "00.kernel", "00.00.10.work", "0524.prime-desk", "evidence", "pack05.02", "source-manifest.json")


def digest(data: bytes) -> tuple[str, int]:
    return hashlib.sha256(data).hexdigest(), len(data)


def snapshot(rel: str) -> bytes:
    with open(PACK, "rb") as handle:
        doc = json.loads(handle.read().decode("utf-8"))
    row = next(item for item in doc["sources"] if item["path"] == rel)
    blob = os.path.join(os.path.dirname(PACK), *row["snapshot"].split("/"))
    with open(blob, "rb") as handle:
        data = handle.read()
    got, size = digest(data)
    if got != row["sha256"] or size != row["bytes"]:
        raise AssertionError(rel)
    return data


def record(page: str, state: str = "returned") -> bytes:
    text = (
        "record: current-assignment\n"
        "schema: 00.kernel/00.00.10.work/0410.imports/01.md#assignment-record version 1\n"
        "desk: 00.kernel\n"
        "book: 00.00.10.work\n"
        "workflow_space: 0\n"
        f"current_work: 00.kernel/00.00.10.work/{page}\n"
        f"pack: 00.kernel/00.00.10.work/{page}\n"
        f"assignment_state: {state}\n"
        "waits_on: none\n"
        "next: review\n"
        "updated: 2026-11-01\n"
    )
    return text.encode("utf-8")


class DeskTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.book = os.path.join(self.tmp.name, "book")
        os.makedirs(self.book)
        self.files: dict[str, bytes] = {}
        with open(os.path.join(ROOT, "app", "development-workspace.json"), "rb") as handle:
            self.workspace = handle.read()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def put(self, rel: str, data: bytes) -> dict:
        path = os.path.join(self.book, *rel.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as handle:
            handle.write(data)
        self.files[rel] = data
        sha, size = digest(data)
        return {"path": rel, "sha256": sha, "bytes": size}

    def pointer(self, rel: str) -> dict:
        sha, size = digest(self.files[rel])
        return {"path": rel, "sha256": sha, "bytes": size}

    def request(self, body: dict) -> str:
        path = os.path.join(self.tmp.name, "request.json")
        with open(path, "wb") as handle:
            handle.write((json.dumps(body, indent=2) + "\n").encode("utf-8"))
        return path

    def base(self, page: str, work_id: str, address: str, page_bytes: bytes, legacy_id: str | None) -> dict:
        self.put("0401.goal/06.01.md", record(page))
        self.put(page, page_bytes)
        self.put("goal.md", b"GOAL\n")
        self.put("checkpoint.md", b"CHECKPOINT\n")
        self.put("verified.md", b"VERIFIED\n")
        self.put("catalog.json", json.dumps({
            "schema": "prime-desk-catalog/2",
            "items": [{
                "work_id": work_id,
                "address": address,
                "label": "index",
                "provenance": "supplied index",
            }],
        }, indent=2).encode("utf-8") + b"\n")
        legacy = None
        if legacy_id is not None:
            self.put("selector.json", json.dumps({
                "schema": "prime-desk-selector/1",
                "selected_work_id": legacy_id,
                "checkpoint": None,
                "verified_result": None,
                "next_route": None,
            }, indent=2).encode("utf-8") + b"\n")
            legacy = self.pointer("selector.json")
        ws_sha, ws_size = digest(self.workspace)
        return {
            "schema": "prime-desk-request/2",
            "instance": {"root": self.book, "book": "00.00.10.work", "role": "prime", "tools_root": ROOT},
            "workspace": {"path": "app/development-workspace.json", "sha256": ws_sha, "bytes": ws_size},
            "assignment": self.pointer("0401.goal/06.01.md"),
            "legacy_selector": legacy,
            "coverage": "declared-paths",
            "references": [
                {"id": "goal", "role": "goal", "label": "goal", "binding": {"scope": "desk"}, **self.pointer("goal.md")},
                {"id": "check", "role": "checkpoint", "label": "checkpoint", "binding": {"scope": "work", "work_id": work_id}, **self.pointer("checkpoint.md")},
                {"id": "ver", "role": "verification", "label": "verification", "binding": {"scope": "work", "work_id": work_id}, **self.pointer("verified.md")},
            ],
            "work": [{"id": work_id, "address": address, "path": page, **self.pointer(page)}],
            "workers": [],
            "supplied": [],
            "attention": [],
            "history": [],
            "catalog": self.pointer("catalog.json"),
            "operations": [],
            "legacy": [],
            "foreign": [],
            "attribution": [],
        }

    def test_n7_identity_can_be_ready(self) -> None:
        page = "0705.sample-check/06.02.review.md"
        body = self.base(page, "work-0705", "0705.sample-check/06.02.review", b"N7-REVIEW-BODY\n", "work-0705")
        doc = pd.assemble(self.request(body), "view", None)
        self.assertEqual(doc["exit"], 0, json.dumps(doc["gaps"], indent=2))
        self.assertEqual(doc["selected"]["id"], "work-0705")
        self.assertEqual(doc["selected"]["rule"], "assignment-record/v1")
        self.assertEqual(doc["selected"]["review_home"]["kind"], "n7")
        self.assertEqual(doc["selected"]["review_home"]["address"], "0705.sample-check/06.02.review")
        self.assertLess(len(pd.render(doc).splitlines()), 80)

    def test_authority_conflict_keeps_canonical_page(self) -> None:
        page_0521 = "0521.return-placement/05.03.md"
        page_0522 = "0522.review-construction/05.04.md"
        body = self.base(
            page_0521,
            "work-0521-0503",
            "0521.return-placement/05.03",
            snapshot("00.kernel/00.00.10.work/" + page_0521),
            "work-0522-0504",
        )
        self.put(page_0522, snapshot("00.kernel/00.00.10.work/" + page_0522))
        body["work"].append({"id": "work-0522-0504", "address": "0522.review-construction/05.04", **self.pointer(page_0522)})
        body["references"].append({
            "id": "crit-0521", "role": "criteria", "label": "0521 task",
            "binding": {"scope": "work", "work_id": "work-0521-0503"}, **self.pointer(page_0521),
        })
        body["references"].append({
            "id": "crit-0522", "role": "criteria", "label": "0522 task",
            "binding": {"scope": "work", "work_id": "work-0522-0504"}, **self.pointer(page_0522),
        })
        body["references"].append({
            "id": "ret-0522", "role": "return", "label": "0522 return",
            "binding": {"scope": "work", "work_id": "work-0522-0504"}, **self.pointer(page_0522),
        })
        self.put("0412.prime-review/06.02.md", snapshot("00.kernel/00.00.10.work/0412.prime-review/06.02.md"))
        body["references"].append({
            "id": "policy", "role": "dependency", "label": "reporting policy",
            "binding": {"scope": "desk"}, **self.pointer("0412.prime-review/06.02.md"),
        })
        catalog = {
            "schema": "prime-desk-catalog/2",
            "items": [{
                "work_id": "work-0522-0504",
                "address": "0522.review-construction/05.04",
                "label": "newer index",
                "provenance": "supplied index",
            }],
        }
        self.put("catalog.json", (json.dumps(catalog, indent=2) + "\n").encode("utf-8"))
        body["catalog"] = self.pointer("catalog.json")
        doc = pd.assemble(self.request(body), "packet", "work-0521-0503")
        self.assertEqual(doc["selected"]["id"], "work-0521-0503")
        self.assertEqual(doc["selected"]["legacy_selector"]["selected_work_id"], "work-0522-0504")
        self.assertFalse(doc["selected"]["legacy_selector"]["agrees"])
        self.assertFalse(doc["catalog"]["used_for_selection"])
        self.assertEqual(doc["selected"]["review_home"]["address"], "0121.return-placement/05.03")
        self.assertIn("Pending custody", doc["selected"]["review_home"]["limit"])
        text = pd.render(doc)
        self.assertIn("The canonical assignment is kept.", text)
        home = text.split("### Review home")[1].split("### Next routes")[0]
        self.assertIn("0121.return-placement/05.03", home)
        self.assertNotIn("0412.prime-review/06.02.md", home)
        self.assertIn("# 05 - Return-line writer, reader and staged migration integration", text)
        self.assertNotIn("# 05 - Real custody into the Prime review loop", text)
        self.assertEqual([item["id"] for item in doc["packet"]["criteria"]], ["crit-0521"])
        self.assertEqual(doc["packet"]["returns"], [])
        other = pd.assemble(self.request(self._retarget(body, page_0522, "work-0522-0504")), "packet", "work-0522-0504")
        other_text = pd.render(other)
        self.assertEqual(other["selected"]["id"], "work-0522-0504")
        self.assertIn("# 05 - Real custody into the Prime review loop", other_text)
        self.assertNotIn("# 05 - Return-line writer, reader and staged migration integration", other_text)

    def _retarget(self, body: dict, page: str, work_id: str) -> dict:
        copied = json.loads(json.dumps(body))
        self.put("0401.goal/06.01.md", record(page))
        copied["assignment"] = self.pointer("0401.goal/06.01.md")
        copied["legacy_selector"] = body["legacy_selector"]
        self.put("selector.json", json.dumps({
            "schema": "prime-desk-selector/1",
            "selected_work_id": "work-0521-0503",
            "checkpoint": None,
            "verified_result": None,
            "next_route": None,
        }, indent=2).encode("utf-8") + b"\n")
        copied["legacy_selector"] = self.pointer("selector.json")
        for item in copied["references"]:
            if item["role"] == "checkpoint":
                item["binding"]["work_id"] = work_id
            if item["role"] == "verification":
                item["binding"]["work_id"] = work_id
        return copied

    def test_missing_and_malformed_selector_do_not_choose(self) -> None:
        page = "0705.sample-check/06.02.review.md"
        body = self.base(page, "work-0705", "0705.sample-check/06.02.review", b"N7-REVIEW-BODY\n", None)
        doc = pd.assemble(self.request(body), "view", None)
        self.assertEqual(doc["selected"]["id"], "work-0705")
        self.assertFalse(doc["selected"]["legacy_selector"]["present"])
        self.put("selector.json", b"{\n")
        body["legacy_selector"] = self.pointer("selector.json")
        broken = pd.assemble(self.request(body), "view", None)
        self.assertEqual(broken["selected"]["id"], "work-0705")
        self.assertTrue(any(item["kind"] == "legacy-selector" for item in broken["gaps"]))
        bad = self.base(page, "work-0705", "0705.sample-check/06.02.review", b"N7-REVIEW-BODY\n", None)
        self.put("0401.goal/06.01.md", b"record: current-assignment\n")
        bad["assignment"] = self.pointer("0401.goal/06.01.md")
        refused = pd.assemble(self.request(bad), "view", None)
        self.assertEqual(refused["exit"], 2)
        self.assertIsNone(refused["selected"])
        self.assertIn("malformed", refused["correction"])

    def test_unsupported_identity_and_coverage_and_wrong_instance(self) -> None:
        page = "0521.return-placement/05.00.md"
        body = self.base(page, "work-zero", "0521.return-placement/05.00", b"ZERO\n", None)
        refused = pd.assemble(self.request(body), "view", None)
        self.assertEqual(refused["exit"], 2)
        self.assertIn("page identity", refused["correction"])
        page = "0705.sample-check/06.02.review.md"
        body = self.base(page, "work-0705", "0705.sample-check/06.02.review", b"N7-REVIEW-BODY\n", None)
        body["coverage"] = "whole-repository"
        covered = pd.assemble(self.request(body), "view", None)
        self.assertEqual(covered["exit"], 2)
        self.assertEqual(covered["check"], "coverage")
        body = self.base(page, "work-0705", "0705.sample-check/06.02.review", b"N7-REVIEW-BODY\n", None)
        text = record("0705.sample-check/06.02.review.md").decode("utf-8").replace(
            "00.kernel/00.00.10.work/0705.sample-check/06.02.review.md",
            "00.kernel/00.00.99.other/0705.sample-check/06.02.review.md",
        )
        self.put("0401.goal/06.01.md", text.encode("utf-8"))
        body["assignment"] = self.pointer("0401.goal/06.01.md")
        foreign = pd.assemble(self.request(body), "view", None)
        self.assertEqual(foreign["exit"], 2)
        self.assertIn("outside the declared book instance", foreign["correction"])

    def test_unregistered_page_is_not_the_catalog(self) -> None:
        page = "0522.review-construction/05.04.md"
        body = self.base(page, "work-0522-0504", "0522.review-construction/05.04", b"OTHER\n", None)
        self.put("0401.goal/06.01.md", record("0521.return-placement/05.03.md"))
        body["assignment"] = self.pointer("0401.goal/06.01.md")
        doc = pd.assemble(self.request(body), "view", None)
        self.assertEqual(doc["exit"], 1)
        self.assertIsNone(doc["selected"])
        self.assertTrue(any(item["kind"] == "unregistered-selection" for item in doc["gaps"]))
        self.assertNotEqual(doc["not_selected"][0]["id"] if doc["not_selected"] else None, "chosen")
        self.assertIn("catalog was not used", pd.render(doc))

    def test_mixed_authors_use_spans(self) -> None:
        page = "0705.sample-check/06.02.review.md"
        body = self.base(page, "work-0705", "0705.sample-check/06.02.review", b"N7-REVIEW-BODY\n", "work-0705")
        source = snapshot("00.kernel/00.00.10.work/0420.prime-desk/06.01.md")
        self.put("0420.prime-desk/06.01.md", source)
        body["attribution"] = [
            {
                "id": "dir", "author": "director", "start": 111, "end": 403,
                "binding": {"scope": "desk"}, **self.pointer("0420.prime-desk/06.01.md"),
            },
            {
                "id": "mod", "author": "model", "start": 430, "end": 834,
                "binding": {"scope": "desk"}, **self.pointer("0420.prime-desk/06.01.md"),
            },
        ]
        doc = pd.assemble(self.request(body), "packet", "work-0705")
        self.assertEqual(doc["exit"], 0, json.dumps(doc["gaps"], indent=2))
        director = doc["packet"]["director"][0]["text"]
        model = doc["packet"]["model"][0]["text"]
        self.assertEqual(director.encode("utf-8"), source[111:403])
        self.assertEqual(model.encode("utf-8"), source[430:834])
        self.assertNotIn("not permission to migrate", director)
        self.assertNotIn("I like it.", model)
        text = pd.render(doc)
        self.assertNotIn("not permission to migrate", text.split("### Director wording")[1].split("### Model explanation")[0])

    def test_stale_source_is_withheld(self) -> None:
        page = "0705.sample-check/06.02.review.md"
        body = self.base(page, "work-0705", "0705.sample-check/06.02.review", b"OLD-PAGE\n", "work-0705")
        path = self.request(body)
        with open(os.path.join(self.book, *page.split("/")), "wb") as handle:
            handle.write(b"NEW-PAGE-SECRET\n")
        doc = pd.assemble(path, "view", None)
        self.assertTrue(any(item["kind"] == "stale" for item in doc["gaps"]))
        self.assertIsNone(doc["selected"])
        self.assertNotIn("NEW-PAGE-SECRET", pd.render(doc))

    def test_open_holds_history_and_supplied_worker(self) -> None:
        page = "0705.sample-check/06.02.review.md"
        body = self.base(page, "work-0705", "0705.sample-check/06.02.review", b"N7-REVIEW-BODY\n", "work-0705")
        self.put("history/long.md", b"HISTORY-SECRET-BODY\n" + b"x" * 5000)
        body["history"] = [{"id": "hist", **self.pointer("history/long.md")}]
        for number in range(3):
            rel = f"hold-{number}.md"
            self.put(rel, f"HOLD-{number}\n".encode("utf-8"))
            body["attention"].append({
                "id": f"hold-{number}", "kind": "hold", "open": True, "label": f"hold {number}",
                **self.pointer(rel),
            })
        self.put("talk.md", b'python -c "print(987654)"\n')
        body["references"].append({
            "id": "talk", "role": "talk", "label": "quoted command",
            "binding": {"scope": "desk"}, **self.pointer("talk.md"),
        })
        body["workers"] = [
            {"id": "grok-2", "work_id": "work-0705", "evidence": None},
        ]
        body["supplied"] = [{
            "id": "sup", "speaker": "codex-prime", "about": "grok-2",
            "text": "Director says the worker is running",
            "limit": "supplied label, not a live process check",
        }]
        doc = pd.assemble(self.request(body), "view", None)
        text = pd.render(doc)
        self.assertEqual(text.count("open hold"), 3)
        self.assertNotIn("HISTORY-SECRET-BODY", text)
        self.assertIn("Not parsed. Not executable.", text)
        self.assertIn("Process activity: unknown.", text)
        self.assertIn("Association basis supplied.", text)
        self.assertFalse(os.path.exists(os.path.join(self.tmp.name, "ran.txt")))

    def test_foreign_book_is_not_read(self) -> None:
        page = "0705.sample-check/06.02.review.md"
        body = self.base(page, "work-0705", "0705.sample-check/06.02.review", b"N7-REVIEW-BODY\n", "work-0705")
        other = os.path.join(self.tmp.name, "other")
        os.makedirs(other)
        with open(os.path.join(other, "secret.md"), "wb") as handle:
            handle.write(b"FOREIGN-SECRET\n")
        body["foreign"] = [{
            "id": "copy", "root": other, "address": "0705.sample-check/06.02.review",
            "note": "same address in another book",
        }]
        doc = pd.assemble(self.request(body), "view", None)
        self.assertEqual(doc["exit"], 0, json.dumps(doc["gaps"], indent=2))
        self.assertFalse(doc["foreign"][0]["read"])
        self.assertNotIn("FOREIGN-SECRET", pd.render(doc))

    def test_packet_rejects_other_id_and_fingerprint_repeats(self) -> None:
        page = "0705.sample-check/06.02.review.md"
        body = self.base(page, "work-0705", "0705.sample-check/06.02.review", b"N7-REVIEW-BODY\n", "work-0705")
        path = self.request(body)
        view = pd.assemble(path, "view", None)
        packet = pd.assemble(path, "packet", "work-0705")
        self.assertEqual(view["inspectability"]["fingerprint"], packet["inspectability"]["fingerprint"])
        refused = pd.assemble(path, "packet", "work-other")
        self.assertEqual(refused["exit"], 1)
        self.assertIsNone(refused["packet"])
        script = (
            "import json,sys\n"
            f"sys.path.insert(0, {LAB!r})\n"
            "import prime_desk as pd\n"
            f"doc = pd.assemble({path!r}, 'view', None)\n"
            "json.dump({'id': doc['selected']['id'], 'fp': doc['inspectability']['fingerprint']}, sys.stdout)\n"
        )
        runs = []
        for _ in range(2):
            proc = subprocess.run([PY, "-B", "-c", script], cwd=ROOT, capture_output=True, check=False)
            self.assertEqual(proc.returncode, 0, proc.stderr.decode("utf-8", "replace"))
            runs.append(json.loads(proc.stdout.decode("utf-8")))
        self.assertEqual(runs[0], runs[1])

    def test_generator_does_not_repin_silently(self) -> None:
        page = "0705.sample-check/06.02.review.md"
        body = self.base(page, "work-0705", "0705.sample-check/06.02.review", b"N7-REVIEW-BODY\n", "work-0705")
        listed = self.request(body)
        out = os.path.join(self.tmp.name, "generated.json")
        proc = subprocess.run(
            [PY, "-B", os.path.join(LAB, "request_index.py"), "--list", listed, "--out", out],
            cwd=ROOT, capture_output=True, check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr.decode("utf-8", "replace"))
        self.assertTrue(os.path.isfile(out))
        with open(os.path.join(self.book, "goal.md"), "wb") as handle:
            handle.write(b"GOAL-CHANGED\n")
        out2 = os.path.join(self.tmp.name, "generated-2.json")
        proc = subprocess.run(
            [PY, "-B", os.path.join(LAB, "request_index.py"), "--list", listed, "--out", out2],
            cwd=ROOT, capture_output=True, check=False,
        )
        self.assertEqual(proc.returncode, 1)
        self.assertFalse(os.path.exists(out2))
        self.assertIn("not proof of corruption", proc.stdout.decode("utf-8"))

    def test_generator_accept_names_one_revision(self) -> None:
        page = "0705.sample-check/06.02.review.md"
        body = self.base(page, "work-0705", "0705.sample-check/06.02.review", b"N7-REVIEW-BODY\n", "work-0705")
        listed = self.request(body)
        with open(os.path.join(self.book, "goal.md"), "wb") as handle:
            handle.write(b"GOAL-CHANGED\n")
        out = os.path.join(self.tmp.name, "accepted.json")
        proc = subprocess.run(
            [PY, "-B", os.path.join(LAB, "request_index.py"), "--list", listed, "--out", out, "--accept", "goal.md"],
            cwd=ROOT, capture_output=True, check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr.decode("utf-8", "replace"))
        self.assertIn("explicit-accept goal.md", proc.stdout.decode("utf-8"))
        with open(out, "rb") as handle:
            doc = json.loads(handle.read().decode("utf-8"))
        goal = next(item for item in doc["references"] if item["id"] == "goal")
        self.assertEqual(goal["bytes"], len(b"GOAL-CHANGED\n"))
        self.assertEqual(doc["assignment"]["sha256"], body["assignment"]["sha256"])

    def test_demo_refuses_existing_output(self) -> None:
        proc = subprocess.run(
            [PY, "-B", os.path.join(LAB, "demo.py"), "--out", self.tmp.name],
            cwd=ROOT, capture_output=True, check=False,
        )
        self.assertEqual(proc.returncode, 2, proc.stderr.decode("utf-8", "replace"))

    def test_cli_does_not_write_live_view(self) -> None:
        page = "0705.sample-check/06.02.review.md"
        body = self.base(page, "work-0705", "0705.sample-check/06.02.review", b"N7-REVIEW-BODY\n", "work-0705")
        path = self.request(body)
        live = os.path.join(ROOT, "00.kernel", "00.live.md")
        with open(live, "rb") as handle:
            before = handle.read()
        proc = subprocess.run(
            [PY, "-B", os.path.join(LAB, "prime_desk.py"), "view", "--request", path, "--json"],
            cwd=ROOT, capture_output=True, check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr.decode("utf-8", "replace"))
        doc = json.loads(proc.stdout.decode("utf-8"))
        self.assertEqual(set(doc), set(pd.RESULT_KEYS))
        with open(live, "rb") as handle:
            self.assertEqual(handle.read(), before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
