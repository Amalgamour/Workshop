#!/usr/bin/env python3
"""Fixture tests for Prime desk route identities."""

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
PASS03_SHA = "cd1e74aa0a51b52dcedaa544b4fd1f2de90f84bf69a8c21234ef362ae2a5f812"
PASS03_BYTES = 77622
PASS02_SHA = "481895211f2312fc8f62d57c45c88d28ff1ceb309234db703d8254b08e66c659"
PASS02_BYTES = 69633
PASS01_SHA = "b047a30324b2a764298ec69daafb9621606bdc10fe5fc45e042105f5c1f10b20"
PASS01_BYTES = 57475
ZERO = "0" * 64


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

    def absent(self, rel: str) -> dict:
        return {"path": rel, "sha256": ZERO, "bytes": 0}

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

    def declare_matched_route(self, body: dict, page: str, work_id: str) -> None:
        ident = pd.page_identity(page)
        self.assertIsNotNone(ident)
        assert ident is not None
        if ident["return_path"] != page:
            self.put(ident["return_path"], b"RETURN-BYTES\n")
            body["references"].append({
                "id": "ret-line",
                "role": "return",
                "label": "return line",
                "binding": {"scope": "work", "work_id": work_id},
                **self.pointer(ident["return_path"]),
            })
        if ident["review_path"] != page:
            self.put(ident["review_path"], b"REVIEW-BYTES\n")
            body["references"].append({
                "id": "rev-file",
                "role": "dependency",
                "label": "review file",
                "binding": {"scope": "desk"},
                **self.pointer(ident["review_path"]),
            })

    def ready_pack(self, legacy: str | None = "work-0705") -> dict:
        page = "0705.sample-check/05.02.pack.md"
        body = self.base(page, "work-0705", "0705.sample-check/05.02.pack", b"N7-PACK-BODY\n", legacy)
        self.declare_matched_route(body, page, "work-0705")
        return body

    def test_predecessors_stay_byte_for_byte(self) -> None:
        for rel, sha, size in (
            ("labs/prime-desk-pass03/prime_desk.py", PASS03_SHA, PASS03_BYTES),
            ("labs/prime-desk-pass02/prime_desk.py", PASS02_SHA, PASS02_BYTES),
            ("labs/prime-desk-pass01/prime_desk.py", PASS01_SHA, PASS01_BYTES),
        ):
            with open(os.path.join(ROOT, *rel.split("/")), "rb") as handle:
                data = handle.read()
            self.assertEqual(digest(data), (sha, size), rel)

    def test_route_table(self) -> None:
        cases = [
            (
                "0521.return-placement/05.03.md",
                "0521.return-placement/05.03",
                "work",
                "N5NN",
                "0121.return-placement/05.03.return.md",
                "0521.return-placement/05.03.md",
            ),
            (
                "1599.synth-lab/05.01.md",
                "1599.synth-lab/05.01",
                "work",
                "N5NN",
                "1199.synth-lab/05.01.return.md",
                "1599.synth-lab/05.01.md",
            ),
            (
                "0705.prime-desk-check/05.01.pack.md",
                "0705.prime-desk-check/05.01.pack",
                "pack",
                "N7NN",
                "0705.prime-desk-check/05.01.return.md",
                "0705.prime-desk-check/06.01.review.md",
            ),
            (
                "1705.prime-desk-check/05.01.pack.md",
                "1705.prime-desk-check/05.01.pack",
                "pack",
                "N7NN",
                "1705.prime-desk-check/05.01.return.md",
                "1705.prime-desk-check/06.01.review.md",
            ),
        ]
        for page, address, kind, band, return_path, review_path in cases:
            body = self.base(page, "work-row", address, b"PAGE\n", "work-row")
            doc = pd.assemble(self.request(body), "view", None)
            self.assertEqual(doc["schema"], "prime-desk-view/4", page)
            self.assertEqual(doc["selected"]["id"], "work-row", page)
            self.assertNotIn("review_home", doc["selected"])
            route = doc["selected"]["route"]
            self.assertEqual(route["source_kind"], kind, page)
            self.assertEqual(route["band"], band, page)
            self.assertEqual(route["source_path"], page, page)
            self.assertEqual(route["return_line"]["path"], return_path, page)
            self.assertEqual(route["review"]["path"], review_path, page)
            self.assertEqual(route["review"]["judgment"], "unknown", page)
            if kind == "work":
                self.assertEqual(route["review"]["file"], "matched", page)
            else:
                self.assertEqual(route["review"]["file"], "undeclared", page)
                self.assertIn("not a finding that the review is absent", route["review"]["limit"])
            self.assertEqual(route["return_line"]["file"], "undeclared", page)
            self.assertEqual(route["return_line"]["custody"], "unknown", page)
            self.assertNotIn("Review home", pd.render(doc))

    def test_n7_pack_can_be_ready(self) -> None:
        body = self.ready_pack()
        doc = pd.assemble(self.request(body), "view", None)
        self.assertEqual(doc["exit"], 0, json.dumps(doc["gaps"], indent=2))
        self.assertEqual(doc["selected"]["id"], "work-0705")
        self.assertEqual(doc["selected"]["rule"], "assignment-record/v1")
        route = doc["selected"]["route"]
        self.assertEqual(route["source_kind"], "pack")
        self.assertEqual(route["return_line"]["path"], "0705.sample-check/05.02.return.md")
        self.assertEqual(route["return_line"]["file"], "matched")
        self.assertEqual(route["return_line"]["custody"], "unknown")
        self.assertEqual(route["review"]["path"], "0705.sample-check/06.02.review.md")
        self.assertEqual(route["review"]["file"], "matched")
        self.assertEqual(route["review"]["judgment"], "unknown")
        self.assertNotIn("0121", route["return_line"]["path"])
        self.assertLess(len(pd.render(doc).splitlines()), 80)

    def test_n5_review_stays_while_return_is_pending(self) -> None:
        page = "0521.return-placement/05.03.md"
        body = self.base(
            page,
            "work-0521-0503",
            "0521.return-placement/05.03",
            snapshot("00.kernel/00.00.10.work/" + page),
            "work-0521-0503",
        )
        return_path = "0121.return-placement/05.03.return.md"
        body["references"].append({
            "id": "ret-line",
            "role": "return",
            "label": "0521 return line",
            "binding": {"scope": "work", "work_id": "work-0521-0503"},
            **self.absent(return_path),
        })
        doc = pd.assemble(self.request(body), "packet", "work-0521-0503")
        self.assertEqual(doc["selected"]["id"], "work-0521-0503")
        route = doc["selected"]["route"]
        self.assertEqual(route["review"]["path"], page)
        self.assertEqual(route["review"]["file"], "matched")
        self.assertEqual(route["review"]["judgment"], "unknown")
        self.assertEqual(route["return_line"]["path"], return_path)
        self.assertEqual(route["return_line"]["file"], "missing")
        self.assertEqual(route["return_line"]["custody"], "pending")
        self.assertTrue(any(item["kind"] == "custody-pending" for item in doc["gaps"]))
        self.assertFalse(any(item["kind"] == "review-missing" for item in doc["gaps"]))
        text = pd.render(doc)
        self.assertNotIn("Review home", text)
        review = text.split("### Review")[1].split("### Return line")[0]
        returned = text.split("### Return line")[1].split("### Next routes")[0]
        self.assertIn(page, review)
        self.assertNotIn("0121", review)
        self.assertIn(return_path, returned)
        self.assertIn("Custody pending", returned)
        self.assertFalse(os.path.exists(os.path.join(self.book, *return_path.split("/"))))

    def test_undeclared_return_does_not_hide_review(self) -> None:
        page = "1599.synth-lab/05.01.md"
        body = self.base(page, "work-1599", "1599.synth-lab/05.01", b"SYNTH\n", "work-1599")
        doc = pd.assemble(self.request(body), "view", None)
        route = doc["selected"]["route"]
        self.assertEqual(route["review"]["file"], "matched")
        self.assertEqual(route["review"]["path"], page)
        self.assertIn("review identity is this source page", route["review"]["limit"])
        self.assertEqual(route["return_line"]["file"], "undeclared")
        self.assertEqual(route["return_line"]["custody"], "unknown")
        self.assertEqual(route["return_line"]["path"], "1199.synth-lab/05.01.return.md")
        self.assertTrue(any(item["kind"] == "return-undeclared" for item in doc["gaps"]))
        self.assertFalse(any(item["kind"] == "review-missing" for item in doc["gaps"]))
        self.assertNotIn("review is absent", route["review"]["limit"])

    def test_review_and_return_artifacts_are_not_sources(self) -> None:
        refused_pages = [
            ("1705.prime-desk-check/06.01.review.md", "review artifact"),
            ("0705.prime-desk-check/06.01.review.md", "review artifact"),
            ("0121.return-placement/05.03.md", "return line"),
            ("0521.return-placement/05.03.return.md", "return artifact"),
            ("1705.prime-desk-check/05.01.return.md", "return artifact"),
            ("0521.return-placement/05.03.pack.md", "not an executable source"),
            ("0705.prime-desk-check/05.01.md", "not an executable source"),
            ("0801.other-band/05.01.md", "No alias was chosen"),
            ("0521.return-placement/05.00.md", "page identity is unsupported"),
            ("not-a-page", "page identity is unsupported"),
        ]
        for page, needle in refused_pages:
            address = page[:-3] if page.endswith(".md") else page
            body = self.base(page, "work-bad", address, b"NO\n", None)
            doc = pd.assemble(self.request(body), "view", None)
            self.assertEqual(doc["exit"], 2, page + " " + doc["correction"])
            self.assertIsNone(doc["selected"], page)
            self.assertIn(needle, doc["correction"], page)
            self.assertNotIn("05.01.pack.md", doc["correction"])

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
        body["work"].append({
            "id": "work-0522-0504",
            "address": "0522.review-construction/05.04",
            **self.pointer(page_0522),
        })
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
        body["references"].append({
            "id": "ret-0521", "role": "return", "label": "0521 return line",
            "binding": {"scope": "work", "work_id": "work-0521-0503"},
            **self.absent("0121.return-placement/05.03.return.md"),
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
        self.assertEqual(doc["packet"]["relation"], "current")
        self.assertEqual(doc["packet"]["route"]["review"]["path"], page_0521)
        self.assertEqual(doc["packet"]["route"]["review"]["file"], "matched")
        self.assertEqual(doc["packet"]["route"]["return_line"]["custody"], "pending")
        text = pd.render(doc)
        self.assertIn("The canonical assignment is kept.", text)
        self.assertNotIn("Review home", text)
        review = text.split("### Review")[1].split("### Return line")[0]
        returned = text.split("### Return line")[1].split("### Next routes")[0]
        self.assertIn(page_0521, review)
        self.assertNotIn("0121", review)
        self.assertNotIn("0412.prime-review/06.02.md", review)
        self.assertIn("0121.return-placement/05.03.return.md", returned)
        self.assertIn("Custody pending", returned)
        self.assertIn("# 05 - Return-line writer, reader and staged migration integration", text)
        self.assertNotIn("# 05 - Real custody into the Prime review loop", text)
        self.assertEqual([item["id"] for item in doc["packet"]["criteria"]], ["crit-0521"])
        self.assertEqual([item["id"] for item in doc["packet"]["returns"]], ["ret-0521"])
        other = pd.assemble(self.request(self._retarget(body, page_0522, "work-0522-0504")), "packet", "work-0522-0504")
        other_text = pd.render(other)
        self.assertEqual(other["selected"]["id"], "work-0522-0504")
        self.assertEqual(other["selected"]["route"]["review"]["path"], page_0522)
        self.assertEqual(other["selected"]["route"]["return_line"]["path"], "0122.review-construction/05.04.return.md")
        self.assertEqual([item["id"] for item in other["packet"]["criteria"]], ["crit-0522"])
        self.assertEqual([item["id"] for item in other["packet"]["returns"]], ["ret-0522"])
        self.assertIn("# 05 - Real custody into the Prime review loop", other_text)
        self.assertNotIn("# 05 - Return-line writer, reader and staged migration integration", other_text)

    def _retarget(self, body: dict, page: str, work_id: str) -> dict:
        copied = json.loads(json.dumps(body))
        self.put("0401.goal/06.01.md", record(page))
        copied["assignment"] = self.pointer("0401.goal/06.01.md")
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

    def test_inspection_does_not_change_selection(self) -> None:
        page = "0521.sample-a/05.01.md"
        other = "1599.sample-b/05.01.md"
        body = self.base(page, "work-a", "0521.sample-a/05.01", b"PAGE-A\n", "work-a")
        self.declare_matched_route(body, page, "work-a")
        self.put(other, b"PAGE-B\n")
        body["work"].append({"id": "work-b", "address": "1599.sample-b/05.01", **self.pointer(other)})
        self.put("1199.sample-b/05.01.return.md", b"RETURN-B\n")
        body["references"].append({
            "id": "ret-b", "role": "return", "label": "b return",
            "binding": {"scope": "work", "work_id": "work-b"},
            **self.pointer("1199.sample-b/05.01.return.md"),
        })
        body["references"].append({
            "id": "crit-a", "role": "criteria", "label": "task a",
            "binding": {"scope": "work", "work_id": "work-a"}, **self.pointer(page),
        })
        body["references"].append({
            "id": "crit-b", "role": "criteria", "label": "task b",
            "binding": {"scope": "work", "work_id": "work-b"}, **self.pointer(other),
        })
        path = self.request(body)
        viewed = pd.assemble(path, "view", None)
        self.assertEqual(viewed["exit"], 0, json.dumps(viewed["gaps"], indent=2))
        inspected = pd.assemble(path, "packet", "work-b")
        self.assertEqual(inspected["selected"]["id"], "work-a")
        self.assertEqual(inspected["selected"]["route"]["source_path"], page)
        self.assertEqual(inspected["packet"]["relation"], "inspection")
        self.assertEqual(inspected["packet"]["canonical_id"], "work-a")
        self.assertEqual(inspected["packet"]["work_id"], "work-b")
        self.assertEqual(inspected["packet"]["route"]["return_line"]["path"], "1199.sample-b/05.01.return.md")
        self.assertEqual(inspected["packet"]["route"]["review"]["path"], other)
        self.assertEqual([item["id"] for item in inspected["packet"]["criteria"]], ["crit-b"])
        self.assertEqual([item["kind"] for item in inspected["gaps"]], ["inspection"])
        self.assertEqual(inspected["exit"], 1)
        self.assertIn("PAGE-B", pd.render(inspected))
        self.assertNotIn("PAGE-A", pd.render(inspected).split("## Packet")[1])

    def test_packet_kind_and_unknown_id_stay_unexpanded(self) -> None:
        page = "0521.sample-work/05.01.md"
        body = self.base(page, "work-src", "0521.sample-work/05.01", b"SRC\n", "work-src")
        review = "0521.sample-work/06.01.review.md"
        returned = "0121.sample-work/05.01.return.md"
        self.put(review, b"REV\n")
        self.put(returned, b"RET\n")
        body["work"].append({"id": "work-rev", "address": "0521.sample-work/06.01.review", **self.pointer(review)})
        body["work"].append({"id": "work-ret", "address": "0121.sample-work/05.01.return", **self.pointer(returned)})
        path = self.request(body)
        view = pd.assemble(path, "view", None)
        current = pd.assemble(path, "packet", "work-src")
        self.assertEqual(view["inspectability"]["fingerprint"], current["inspectability"]["fingerprint"])
        self.assertEqual(current["packet"]["relation"], "current")
        for work_id, kind in (("work-rev", "review"), ("work-ret", "return")):
            refused = pd.assemble(path, "packet", work_id)
            self.assertEqual(refused["selected"]["id"], "work-src")
            self.assertIsNone(refused["packet"])
            self.assertTrue(any(item["kind"] == "packet-kind" and kind in item["message"] for item in refused["gaps"]))
            self.assertIn("Not expanded. The canonical selection was not replaced.", pd.render(refused))
        unknown = pd.assemble(path, "packet", "work-other")
        self.assertEqual(unknown["exit"], 1)
        self.assertIsNone(unknown["packet"])
        self.assertEqual(unknown["selected"]["id"], "work-src")
        self.assertTrue(any(item["kind"] == "packet-selection" for item in unknown["gaps"]))

    def test_mismatched_subject_or_pass_is_not_aliased(self) -> None:
        page = "0521.return-placement/05.03.md"
        for address in ("0521.other-subject/05.03", "0521.return-placement/05.04"):
            body = self.base(page, "work-0521-0503", address, b"PAGE\n", None)
            doc = pd.assemble(self.request(body), "view", None)
            self.assertIsNone(doc["selected"], address)
            self.assertTrue(any(item["kind"] == "identity" for item in doc["gaps"]), address)
            self.assertNotEqual(doc["not_selected"][0]["address"], "0521.return-placement/05.03")

    def test_missing_and_malformed_selector_do_not_choose(self) -> None:
        page = "0705.sample-check/05.02.pack.md"
        body = self.base(page, "work-0705", "0705.sample-check/05.02.pack", b"N7-PACK-BODY\n", None)
        doc = pd.assemble(self.request(body), "view", None)
        self.assertEqual(doc["selected"]["id"], "work-0705")
        self.assertFalse(doc["selected"]["legacy_selector"]["present"])
        self.put("selector.json", b"{\n")
        body["legacy_selector"] = self.pointer("selector.json")
        broken = pd.assemble(self.request(body), "view", None)
        self.assertEqual(broken["selected"]["id"], "work-0705")
        self.assertTrue(any(item["kind"] == "legacy-selector" for item in broken["gaps"]))
        bad = self.base(page, "work-0705", "0705.sample-check/05.02.pack", b"N7-PACK-BODY\n", None)
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
        page = "0705.sample-check/05.02.pack.md"
        body = self.base(page, "work-0705", "0705.sample-check/05.02.pack", b"N7-PACK-BODY\n", None)
        body["coverage"] = "whole-repository"
        covered = pd.assemble(self.request(body), "view", None)
        self.assertEqual(covered["exit"], 2)
        self.assertEqual(covered["check"], "coverage")
        body = self.base(page, "work-0705", "0705.sample-check/05.02.pack", b"N7-PACK-BODY\n", None)
        text = record(page).decode("utf-8").replace(
            "00.kernel/00.00.10.work/" + page,
            "00.kernel/00.00.99.other/" + page,
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
        body = self.ready_pack()
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
        page = "0705.sample-check/05.02.pack.md"
        body = self.base(page, "work-0705", "0705.sample-check/05.02.pack", b"OLD-PAGE\n", "work-0705")
        path = self.request(body)
        with open(os.path.join(self.book, *page.split("/")), "wb") as handle:
            handle.write(b"NEW-PAGE-SECRET\n")
        doc = pd.assemble(path, "view", None)
        self.assertTrue(any(item["kind"] == "stale" for item in doc["gaps"]))
        self.assertIsNone(doc["selected"])
        self.assertNotIn("NEW-PAGE-SECRET", pd.render(doc))

    def test_open_holds_history_and_supplied_worker(self) -> None:
        body = self.ready_pack()
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
        body["workers"] = [{"id": "grok-2", "work_id": "work-0705", "evidence": None}]
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
        body = self.ready_pack()
        other = os.path.join(self.tmp.name, "other")
        os.makedirs(other)
        with open(os.path.join(other, "secret.md"), "wb") as handle:
            handle.write(b"FOREIGN-SECRET\n")
        body["foreign"] = [{
            "id": "copy", "root": other, "address": "0705.sample-check/05.02.pack",
            "note": "same address in another book",
        }]
        doc = pd.assemble(self.request(body), "view", None)
        self.assertEqual(doc["exit"], 0, json.dumps(doc["gaps"], indent=2))
        self.assertFalse(doc["foreign"][0]["read"])
        self.assertNotIn("FOREIGN-SECRET", pd.render(doc))

    def test_generator_does_not_repin_silently(self) -> None:
        body = self.ready_pack()
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
        body = self.ready_pack()
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
        body = self.ready_pack()
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
        self.assertEqual(doc["schema"], "prime-desk-view/4")
        with open(live, "rb") as handle:
            self.assertEqual(handle.read(), before)

    def test_supplied_context_without_workers_is_visible(self) -> None:
        body = self.ready_pack(legacy=None)
        body["supplied"] = [{
            "id": "sup-lanes",
            "speaker": "codex-prime",
            "about": "",
            "text": "Prepared next lanes are not proof a worker has started.",
            "limit": "Supplied checkpoint sentence. Not a live process check.",
        }]
        doc = pd.assemble(self.request(body), "view", None)
        self.assertEqual(doc["workers"], [])
        self.assertEqual(doc["record"]["supplied_without_worker"][0]["id"], "sup-lanes")
        text = pd.render(doc)
        self.assertIn("### Supplied context", text)
        self.assertIn("not a declared worker", text)
        self.assertIn("Prepared next lanes are not proof a worker has started.", text)
        self.assertIn("Supplied checkpoint sentence.", text)
        self.assertIn("None declared. Activity is unknown.", text)
        self.assertNotIn("worker sup-lanes", text)
        self.assertEqual(doc["selected"]["id"], "work-0705")
        self.assertEqual(doc["selected"]["route"]["band"], "N7NN")

    def test_known_verification_and_next_stay_on_the_route(self) -> None:
        body = self.ready_pack(legacy=None)
        self.put("next.md", b"NEXT-STEP\n")
        body["references"].append({
            "id": "nxt",
            "role": "next",
            "label": "next reference",
            "binding": {"scope": "work", "work_id": "work-0705"},
            **self.pointer("next.md"),
        })
        doc = pd.assemble(self.request(body), "view", None)
        self.assertEqual(doc["exit"], 0, json.dumps(doc["gaps"], indent=2))
        self.assertEqual(doc["selected"]["id"], "work-0705")
        self.assertEqual(doc["selected"]["route"]["band"], "N7NN")
        self.assertEqual(doc["selected"]["route"]["return_line"]["path"], "0705.sample-check/05.02.return.md")
        self.assertEqual(doc["selected"]["verified_result"]["basis"], "observed")
        self.assertEqual(doc["selected"]["verified_result"]["source"]["status"], "matched")
        self.assertEqual(doc["selected"]["next_route"]["source"]["path"], "next.md")
        self.assertEqual(doc["selected"]["next_route"]["source"]["status"], "matched")
        self.assertFalse(any(item["kind"] == "verification" for item in doc["gaps"]))
        text = pd.render(doc)
        self.assertIn("next.md", text)
        self.assertIn("Verified result: matched", text)

    def test_missing_verification_stays_unknown(self) -> None:
        body = self.ready_pack(legacy=None)
        body["references"] = [item for item in body["references"] if item["role"] != "verification"]
        body["references"].append({
            "id": "ver",
            "role": "verification",
            "label": "missing verification",
            "binding": {"scope": "work", "work_id": "work-0705"},
            **self.absent("missing-verified.md"),
        })
        doc = pd.assemble(self.request(body), "view", None)
        self.assertEqual(doc["selected"]["id"], "work-0705")
        self.assertEqual(doc["selected"]["verified_result"]["basis"], "unknown")
        self.assertTrue(any(item["kind"] == "verification" for item in doc["gaps"]))
        self.assertIn("missing verification is unknown", pd.render(doc))
        self.assertFalse(os.path.exists(os.path.join(self.book, "missing-verified.md")))

    def test_stale_verification_is_withheld(self) -> None:
        body = self.ready_pack(legacy=None)
        with open(os.path.join(self.book, "verified.md"), "wb") as handle:
            handle.write(b"STALE-VERIFICATION-SECRET\n")
        doc = pd.assemble(self.request(body), "view", None)
        self.assertEqual(doc["selected"]["id"], "work-0705")
        self.assertEqual(doc["selected"]["route"]["source_kind"], "pack")
        self.assertTrue(any(item["kind"] == "stale" for item in doc["gaps"]))
        self.assertTrue(any(item["kind"] == "verification" for item in doc["gaps"]))
        self.assertEqual(doc["selected"]["verified_result"]["basis"], "unknown")
        self.assertNotIn("STALE-VERIFICATION-SECRET", pd.render(doc))

    def test_declared_review_loop_keeps_its_pin(self) -> None:
        body = self.ready_pack(legacy=None)
        rel = "labs/review-loop-pass02/review_loop.py"
        with open(os.path.join(ROOT, *rel.split("/")), "rb") as handle:
            data = handle.read()
        sha, size = digest(data)
        body["operations"] = [{
            "id": "loop",
            "name": "review-loop",
            "limitation": "Reviewed module pin. Not production activation.",
            "past_tests": "unknown",
            "activation": "unknown",
            "path": rel,
            "sha256": sha,
            "bytes": size,
        }]
        doc = pd.assemble(self.request(body), "view", None)
        loops = [item for item in doc["operations"] if item["name"] == "review-loop"]
        self.assertEqual(len(loops), 1)
        self.assertEqual(loops[0]["source"]["status"], "matched")
        self.assertEqual(loops[0]["source"]["sha256"], sha)
        self.assertFalse(loops[0]["executed"])
        self.assertEqual(loops[0]["activation"], "unknown")
        text = pd.render(doc)
        self.assertIn("Reviewed module pin. Not production activation.", text)
        self.assertNotIn("Pending. Successor modules were not imported.", text)
        self.assertEqual(doc["selected"]["id"], "work-0705")

    def test_undeclared_review_loop_stays_pending(self) -> None:
        doc = pd.assemble(self.request(self.ready_pack(legacy=None)), "view", None)
        loops = [item for item in doc["operations"] if item["name"] == "review-loop"]
        self.assertEqual(len(loops), 1)
        self.assertIsNone(loops[0]["source"])
        self.assertIn("Pending. Successor modules were not imported.", loops[0]["limitation"])
        self.assertIn("Pending. Successor modules were not imported.", pd.render(doc))


if __name__ == "__main__":
    unittest.main(verbosity=2)
