#!/usr/bin/env python3
"""Fixture tests for the read-only Prime desk view."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
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


def digest(data: bytes) -> tuple[str, int]:
    return hashlib.sha256(data).hexdigest(), len(data)


def tree_rows(root: str) -> list[tuple[str, str, int]]:
    rows = []
    for dirpath, _dirs, names in os.walk(root):
        for name in sorted(names):
            path = os.path.join(dirpath, name)
            with open(path, "rb") as handle:
                data = handle.read()
            rows.append((os.path.relpath(path, root).replace("\\", "/"), hashlib.sha256(data).hexdigest(), len(data)))
    return rows


class DeskTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.book = os.path.join(self.tmp.name, "book")
        self.other = os.path.join(self.tmp.name, "other-book")
        os.makedirs(self.book)
        os.makedirs(self.other)
        self.files: dict[str, bytes] = {}

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def put(self, rel: str, text: str, root: str | None = None) -> dict:
        data = text.encode("utf-8")
        base = self.book if root is None else root
        path = os.path.join(base, *rel.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as handle:
            handle.write(data)
        sha, size = digest(data)
        self.files[rel] = data
        return {"path": rel, "sha256": sha, "bytes": size}

    def request(self, **overrides) -> str:
        selected = self.put("work/0522.review-construction/05.04.md", "ASSIGNMENT-ALPHA\nfinish the review loop\n")
        newer = self.put("work/0524.prime-desk/05.01.md", "NEWER-UNRELATED-PAGE\n")
        goal = self.put("0401.goal/01.md", "GOAL TEXT\n")
        scope = self.put("0408.seats/01.md", "SCOPE TEXT\n")
        authority = self.put("0416.desk-app/01.003.md", "AUTHORITY TEXT\n")
        director = self.put("0420.prime-desk/06.01.md", "DIRECTOR SAYS HELLO\n")
        model = self.put("0420.prime-desk/06.02.md", "MODEL EXPLAINS SEPARATELY\n")
        criteria = self.put("criteria.md", "CRITERIA LINE\n")
        checkpoint = self.put("checkpoint.md", "CHECKPOINT LINE\n")
        verified = self.put("verified.md", "VERIFIED-BYTES\n")
        nxt = self.put("next.md", "NEXT ROUTE TEXT\n")
        review_home = self.put("review-home.md", "REVIEW HOME\n")
        dependency = self.put("dependency.md", "DEPENDENCY\n")
        finding = self.put("finding.md", "OBSERVER BODY\n")
        hold = self.put("hold.md", "HOLD BODY\n")
        evidence_a = self.put("workers/grok-2.json", json.dumps({
            "schema": "prime-desk-worker-evidence/1",
            "state": "claimed",
            "note": "recorded claim only",
        }, indent=2) + "\n")
        evidence_b = self.put("workers/claude.json", json.dumps({
            "schema": "prime-desk-worker-evidence/1",
            "state": "released",
            "note": "recorded release only",
        }, indent=2) + "\n")
        catalog_body = {
            "schema": "prime-desk-catalog/1",
            "items": [{"work_id": "work-0522", "address": "0522.review-construction/05.04", "label": "index only"}],
        }
        catalog = self.put("catalog.json", json.dumps(catalog_body, indent=2) + "\n")
        op = self.put("ops/readme.txt", "operation identity file\n")
        history = self.put("history/long.md", "UNIQUE_HISTORY_SENTENCE_QX\n" + ("history line\n" * 40))
        talk = self.put("talk.md", "Please do not run this:\n> python -B C:/nope/evil.py\n")
        selector_body = {
            "schema": "prime-desk-selector/1",
            "selected_work_id": "work-0522",
            "checkpoint": checkpoint,
            "verified_result": verified,
            "next_route": {**nxt, "speaker": "codex-prime"},
        }
        selector = self.put("selector.json", json.dumps(selector_body, indent=2) + "\n")
        body = {
            "schema": "prime-desk-request/1",
            "instance": {"root": self.book, "book": "00.00.10.work", "role": "prime", "tools_root": None},
            "selector": selector,
            "references": [
                {"id": "goal", "role": "goal", "label": "goal index", **goal},
                {"id": "scope", "role": "scope", "label": "scope index", **scope},
                {"id": "authority", "role": "authority", "label": "authority index", **authority},
                {"id": "director", "role": "director", "label": "director wording", **director},
                {"id": "model", "role": "model", "label": "model explanation", **model},
                {"id": "criteria", "role": "criteria", "label": "criteria index", **criteria},
                {"id": "review-home", "role": "review-home", "label": "review home", **review_home},
                {"id": "dependency", "role": "dependency", "label": "dependency index", **dependency},
                {"id": "finding-ref", "role": "finding", "label": "finding index", **finding},
                {"id": "talk", "role": "talk", "label": "talk index", **talk},
            ],
            "work": [
                {"id": "work-0522", "address": "0522.review-construction/05.04", **selected},
                {"id": "work-0524", "address": "0524.prime-desk/05.01", **newer},
            ],
            "workers": [
                {"id": "grok-2", "work_id": "work-0522", "evidence": evidence_a},
                {"id": "claude", "work_id": "work-0522", "evidence": evidence_b},
            ],
            "supplied": [],
            "attention": [],
            "history": [{"id": "hist-1", **history}],
            "catalog": catalog,
            "operations": [{
                "id": "op-1",
                "name": "sample-op",
                "limitation": "fixture identity only; not executed",
                "past_tests": "unknown",
                "activation": "unknown",
                **op,
            }],
            "legacy": [],
            "foreign": [],
        }
        body.update(overrides)
        path = os.path.join(self.tmp.name, "request.json")
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(body, handle, indent=2)
            handle.write("\n")
        self.body = body
        return path

    def view(self, path: str | None = None, work_id: str | None = None, command: str = "view") -> dict:
        target = path or self.request()
        return pd.assemble(target, command, work_id)

    def test_two_workers_and_newer_page_not_selected(self) -> None:
        doc = self.view()
        self.assertEqual(doc["exit"], 0, doc["gaps"])
        self.assertEqual(doc["selected"]["id"], "work-0522")
        self.assertEqual(doc["selected"]["address"], "0522.review-construction/05.04")
        self.assertEqual([item["id"] for item in doc["not_selected"]], ["work-0524"])
        self.assertEqual(len(doc["workers"]), 2)
        self.assertEqual(doc["workers"][0]["evidence"]["recorded_state"], "claimed")
        self.assertEqual(doc["workers"][1]["evidence"]["recorded_state"], "released")
        self.assertTrue(all(item["process_activity"] == "unknown" for item in doc["workers"]))
        text = pd.render(doc)
        self.assertIn("Selected: work-0522", text)
        self.assertIn("work-0524", text)
        self.assertNotIn("NEWER-UNRELATED-PAGE", text)
        self.assertNotIn("UNIQUE_HISTORY_SENTENCE_QX", text)
        self.assertIn("History records: 1", text)
        self.assertLess(len(text.splitlines()), 80)

    def test_missing_and_conflicting_selector(self) -> None:
        path = self.request()
        os.remove(os.path.join(self.book, "selector.json"))
        missing = self.view(path)
        self.assertEqual(missing["state"], "partial")
        self.assertIsNone(missing["selected"])
        self.assertTrue(any(gap["kind"] == "missing" for gap in missing["gaps"]))
        path = self.request()
        body = self.body
        body["work"].append({
            "id": "work-copy",
            "address": "0522.review-construction/05.04",
            "path": "work/0524.prime-desk/05.01.md",
            "sha256": body["work"][1]["sha256"],
            "bytes": body["work"][1]["bytes"],
        })
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(body, handle, indent=2)
            handle.write("\n")
        conflict = pd.assemble(path, "view", None)
        self.assertEqual(conflict["selected"]["id"], "work-0522")
        self.assertTrue(any(gap["kind"] == "same-address" for gap in conflict["gaps"]))
        self.assertIn("work-copy", [item["id"] for item in conflict["not_selected"]])

    def test_stale_catalog_is_not_selection(self) -> None:
        path = self.request()
        catalog = os.path.join(self.book, "catalog.json")
        with open(catalog, "wb") as handle:
            handle.write(b'{"schema":"prime-desk-catalog/1","items":[{"work_id":"work-0524","address":"0524.prime-desk/05.01","label":"do not pick"}]}\n')
        doc = pd.assemble(path, "view", None)
        self.assertEqual(doc["selected"]["id"], "work-0522")
        self.assertTrue(any(gap["kind"] == "stale" and gap["path"] == "catalog.json" for gap in doc["gaps"]))
        self.assertIsNone(doc["catalog"])
        rendered = pd.render(doc)
        self.assertNotIn("do not pick", rendered)

    def test_absent_return_and_receipt(self) -> None:
        path = self.request()
        body = self.body
        body["references"].append({
            "id": "ret", "role": "return", "label": "return index",
            "path": "missing-return.md", "sha256": "a" * 64, "bytes": 1,
        })
        body["references"].append({
            "id": "rcp", "role": "receipt", "label": "receipt index",
            "path": "missing-receipt.md", "sha256": "b" * 64, "bytes": 1,
        })
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(body, handle, indent=2)
            handle.write("\n")
        doc = pd.assemble(path, "packet", "work-0522")
        kinds = {gap["kind"] for gap in doc["gaps"]}
        self.assertIn("return", kinds)
        self.assertIn("receipt", kinds)
        text = pd.render(doc)
        self.assertIn("return is missing", text)
        self.assertNotIn("clean bill", text.lower())

    def test_unknown_worker_versus_supplied_running(self) -> None:
        path = self.request()
        body = self.body
        body["workers"][1]["evidence"] = None
        body["supplied"] = [{
            "id": "sup-1",
            "speaker": "codex-prime",
            "about": "claude",
            "text": "Director reported Claude running",
            "limit": "recorded report, not a live process check",
        }]
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(body, handle, indent=2)
            handle.write("\n")
        doc = pd.assemble(path, "view", None)
        claude = doc["workers"][1]
        self.assertIsNone(claude["evidence"]["recorded_state"])
        self.assertEqual(claude["process_activity"], "unknown")
        self.assertEqual(claude["supplied"][0]["basis"], "supplied")
        text = pd.render(doc)
        self.assertIn("Director reported Claude running", text)
        self.assertIn("Process activity: unknown", text)
        self.assertIn("not a live process check", text)

    def test_hold_and_observer_are_listed_without_history_body(self) -> None:
        path = self.request()
        body = self.body
        hold = self.put("holds/h.md", "HOLD FILE BODY THAT SHOULD STAY ON DISK\n")
        obs = self.put("holds/o.md", "OBSERVER FILE BODY\n")
        body["attention"] = [
            {"id": f"hold-{i}", "kind": "hold", "open": True, "label": f"hold-label-{i}", **hold}
            for i in range(12)
        ]
        body["attention"].append({
            "id": "obs-1", "kind": "observer-finding", "open": True, "label": "observer-label", **obs,
        })
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(body, handle, indent=2)
            handle.write("\n")
        doc = pd.assemble(path, "view", None)
        text = pd.render(doc)
        for i in range(12):
            self.assertIn(f"hold-label-{i}", text)
        self.assertIn("observer-label", text)
        self.assertIn("Open declared attention: 13", text)
        self.assertNotIn("UNIQUE_HISTORY_SENTENCE_QX", text)
        self.assertNotIn("HOLD FILE BODY", text)

    def test_same_address_in_two_books_is_not_mixed(self) -> None:
        secret = self.put("secret.md", "OTHER-BOOK-SECRET\n", root=self.other)
        path = self.request()
        body = self.body
        body["foreign"] = [{
            "id": "copy-2",
            "root": self.other,
            "address": "0522.review-construction/05.04",
            "note": "other instance",
        }]
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(body, handle, indent=2)
            handle.write("\n")
        doc = pd.assemble(path, "view", None)
        blob = json.dumps(doc)
        self.assertNotIn("OTHER-BOOK-SECRET", blob)
        self.assertFalse(doc["foreign"][0]["read"])
        self.assertTrue(doc["foreign"][0]["same_address_as_selected"])
        self.assertNotEqual(secret["sha256"], doc["selected"]["source"]["sha256"])

    def test_supplied_label_is_not_verified_evidence(self) -> None:
        path = self.request()
        body = self.body
        body["operations"][0]["past_tests"] = "passed"
        body["selector"] = self.body["selector"]
        # Drop the verified file by nulling it inside the selector bytes.
        selector = {
            "schema": "prime-desk-selector/1",
            "selected_work_id": "work-0522",
            "checkpoint": body["work"][0] and self.body["selector"],
            "verified_result": None,
            "next_route": None,
        }
        # Rebuild selector from the on-disk checkpoint already stored in the first request's selector file.
        with open(os.path.join(self.book, "selector.json"), encoding="utf-8") as handle:
            raw = json.loads(handle.read())
        raw["verified_result"] = None
        pointer = self.put("selector.json", json.dumps(raw, indent=2) + "\n")
        body["selector"] = pointer
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(body, handle, indent=2)
            handle.write("\n")
        doc = pd.assemble(path, "view", None)
        self.assertEqual(doc["selected"]["verified_result"]["basis"], "unknown")
        self.assertTrue(any(gap["kind"] == "verification" for gap in doc["gaps"]))
        self.assertTrue(any(gap["kind"] == "operation-label" for gap in doc["gaps"]))
        self.assertFalse(doc["operations"][0]["executed"])

    def test_talk_command_is_not_executable(self) -> None:
        sentinel = os.path.join(self.book, "evil-ran")
        doc = self.view()
        self.assertFalse(os.path.exists(sentinel))
        text = pd.render(doc)
        self.assertIn("Not parsed. Not executable.", text)
        self.assertNotIn("evil.py", text)
        self.assertNotIn("python -B", text)

    def test_wrong_path_and_bad_root(self) -> None:
        path = self.request()
        outside = os.path.join(self.tmp.name, "outside.txt")
        with open(outside, "wb") as handle:
            handle.write(b"OUTSIDE-SECRET\n")
        body = self.body
        body["references"].append({
            "id": "bad", "role": "other", "label": "bad path",
            "path": "../outside.txt", "sha256": "c" * 64, "bytes": 15,
        })
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(body, handle, indent=2)
            handle.write("\n")
        doc = pd.assemble(path, "view", None)
        self.assertTrue(any(gap["kind"] == "outside-path" for gap in doc["gaps"]))
        self.assertNotIn("OUTSIDE-SECRET", json.dumps(doc))
        body["instance"]["root"] = os.path.join(self.tmp.name, "missing-root")
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(body, handle, indent=2)
            handle.write("\n")
        refused = pd.assemble(path, "view", None)
        self.assertEqual(refused["exit"], 2)
        self.assertEqual(refused["state"], "refused")
        self.assertIn("instance.root", refused["check"])

    def test_fingerprint_is_stable_and_sources_unchanged(self) -> None:
        path = self.request()
        before = tree_rows(self.book)
        first = pd.assemble(path, "view", None)
        packet = pd.assemble(path, "packet", "work-0522")
        after = tree_rows(self.book)
        self.assertEqual(before, after)
        self.assertEqual(first["inspectability"]["fingerprint"], packet["inspectability"]["fingerprint"])
        self.assertNotIn("ASSIGNMENT-ALPHA", pd.render(first))
        packet_text = pd.render(packet)
        self.assertIn("DIRECTOR SAYS HELLO", packet_text)
        self.assertIn("MODEL EXPLAINS SEPARATELY", packet_text)
        director = packet_text.split("### Director wording")[1].split("### Model explanation")[0]
        model = packet_text.split("### Model explanation")[1].split("### Returns")[0]
        self.assertIn("DIRECTOR SAYS HELLO", director)
        self.assertNotIn("MODEL EXPLAINS SEPARATELY", director)
        self.assertIn("MODEL EXPLAINS SEPARATELY", model)
        self.assertIn("ASSIGNMENT-ALPHA", packet_text)

    def test_new_process_recovers_the_same_identity(self) -> None:
        path = self.request()
        script = (
            "import json,sys\n"
            f"sys.path.insert(0, {LAB!r})\n"
            "import prime_desk as pd\n"
            f"doc = pd.assemble({path!r}, 'view', None)\n"
            "json.dump({'id': doc['selected']['id'], 'fp': doc['inspectability']['fingerprint'],"
            "'open': [a['id'] for a in doc['attention'] if a['open']], 'gaps': [g['kind'] for g in doc['gaps']]}, sys.stdout)\n"
        )
        runs = []
        for _ in range(2):
            proc = subprocess.run([PY, "-B", "-c", script], cwd=ROOT, capture_output=True, check=False)
            self.assertEqual(proc.returncode, 0, proc.stderr.decode("utf-8", "replace"))
            runs.append(json.loads(proc.stdout.decode("utf-8")))
        self.assertEqual(runs[0], runs[1])
        self.assertEqual(runs[0]["id"], "work-0522")

    def test_changed_bytes_are_withheld(self) -> None:
        path = self.request()
        original = pd.read_twice

        def changed(target: str):
            status, first, second = original(target)
            if target.endswith("0401.goal" + os.sep + "01.md") or target.endswith("0401.goal/01.md"):
                return "changed", b"OLD-GOAL", b"NEW-GOAL"
            return status, first, second

        pd.read_twice = changed
        try:
            doc = pd.assemble(path, "view", None)
        finally:
            pd.read_twice = original
        self.assertTrue(any(gap["kind"] == "changed" for gap in doc["gaps"]))
        self.assertNotIn("NEW-GOAL", json.dumps(doc))
        self.assertNotIn("OLD-GOAL", pd.render(doc))

    def test_packet_rejects_unselected_id(self) -> None:
        path = self.request()
        doc = pd.assemble(path, "packet", "work-0524")
        self.assertEqual(doc["exit"], 1)
        self.assertIsNone(doc["packet"])
        self.assertEqual(doc["selected"]["id"], "work-0522")
        self.assertIn("not the canonical selection", pd.render(doc))

    def test_malformed_request_is_a_precise_refusal(self) -> None:
        path = os.path.join(self.tmp.name, "bad.json")
        with open(path, "wb") as handle:
            handle.write(b'{"schema":"prime-desk-request/1"}\n')
        doc = pd.assemble(path, "view", None)
        self.assertEqual(doc["exit"], 2)
        self.assertEqual(doc["check"], "prime-desk-request/1")
        self.assertIn("exact keys", doc["correction"])

    def test_legacy_limits_stay_visible_and_do_not_select(self) -> None:
        path = self.request()
        body = self.body
        body["instance"]["tools_root"] = ROOT
        brief = self.put("legacy/brief.json", '{"schema":"prime-brief-input/1"}\n')
        projection = self.put("legacy/projection.json", '{"schema":"state-observations/1"}\n')
        desk = self.put("legacy/desk.json", '{"schema":"desk-state/1"}\n')
        support = self.put("legacy/support.json", '{"schema":"prime-support-registry"}\n')
        context = self.put("legacy/context.json", '{"schema":"librarian-development-workspace"}\n')
        assignment = (
            "record: current-assignment\n"
            "schema: 00.kernel/00.00.10.work/0410.imports/01.md#assignment-record version 1\n"
            "desk: 00.kernel\n"
            "book: 00.00.10.work\n"
            "workflow_space: 0\n"
            "current_work: 00.kernel/00.00.10.work/0522.review-construction/05.04.md\n"
            "pack: 00.kernel/00.00.10.work/0522.review-construction/05.04.md\n"
            "assignment_state: running\n"
            "waits_on: none\n"
            "next: review\n"
            "updated: 2026-11-01\n"
        )
        record = self.put("assignment-record.md", assignment)
        body["references"].append({
            "id": "assign", "role": "assignment", "label": "assignment record", **record,
        })
        body["legacy"] = [
            {"id": "leg-brief", "reader": "prime-brief", **brief},
            {"id": "leg-proj", "reader": "state-projection", **projection},
            {"id": "leg-desk", "reader": "desk-state", **desk},
            {"id": "leg-support", "reader": "prime-support", **support},
            {"id": "leg-context", "reader": "app-context", **context},
        ]
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(body, handle, indent=2)
            handle.write("\n")
        doc = pd.assemble(path, "view", None)
        self.assertEqual(doc["selected"]["id"], "work-0522")
        limits = {item["reader"]: item["limit"] for item in doc["legacy"]}
        self.assertIn("build was not called", limits["prime-brief"])
        self.assertIn("project and inspect were not called", limits["state-projection"])
        self.assertIn("build_view was not called", limits["desk-state"])
        self.assertIn("Git", limits["prime-support"])
        self.assertIn("validate_context was not called", limits["app-context"])
        self.assertFalse(any(item["executed"] for item in doc["legacy"]))
        reader = doc["record"]["assignment_reader"][0]
        self.assertEqual(reader["fields"]["assignment_state"], "running")
        self.assertIn("not a live process check", reader["limit"])
        text = pd.render(doc)
        self.assertIn("Pending. Successor modules were not imported.", text)
        self.assertNotIn("import review_loop", text)

    def test_cli_json_and_no_source_write(self) -> None:
        path = self.request()
        before = tree_rows(self.book)
        live = os.path.join(ROOT, "00.kernel", "00.live.md")
        with open(live, "rb") as handle:
            live_before = handle.read()
        proc = subprocess.run(
            [PY, "-B", os.path.join(LAB, "prime_desk.py"), "view", "--request", path, "--json"],
            cwd=ROOT,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr.decode("utf-8", "replace"))
        doc = json.loads(proc.stdout.decode("utf-8"))
        self.assertEqual(set(doc), set(pd.RESULT_KEYS))
        self.assertEqual(doc["selected"]["id"], "work-0522")
        self.assertEqual(tree_rows(self.book), before)
        with open(live, "rb") as handle:
            self.assertEqual(handle.read(), live_before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
