"""PSI-01 and PSI-02 regressions (0507.prime-support/05.03). Disposable repositories only.

  python -B -X dev tests/test_psi.py -v
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_prime_support as tps  # noqa: E402

ENV, PAGE, batch, git, prefix = tps.ENV, tps.PAGE, tps.batch, tps.git, tps.prefix

PAGE_FILE = f"{PAGE}/05.01.md"


def finding(rep, ident, path=PAGE_FILE, lane="fixture"):
    found = next(l for l in rep["lanes"] if l["lane"] == lane)["findings"]
    return found.get(f"{path}#{ident}", found.get(ident))


def review(rid_line, findings, extra=""):
    return f"{rid_line}\nDisposition: REPAIR REQUIRED.\n{extra}findings: {findings}"


class PSI(tps.Fixture):
    """Reuses the original fixture helpers. Its inherited test_ methods are disabled below, so the 19 original
    tests run only from test_prime_support.py."""

    def status_json(self, reg, store=True):
        """Every status call in these regressions is also a read-only check: HEAD, index bytes, refs, status and
        the page bytes must be identical before and after."""
        files = [PAGE_FILE] if (self.repo / PAGE_FILE).exists() else []
        before = self.snapshot(self.repo, files)
        result = super().status_json(reg, store)
        self.assertEqual(before, self.snapshot(self.repo, files), "status changed the inspected repository")
        return result

    def commit_dated(self, files, date, push=True, msg="dated"):
        for rel, text in files.items():
            self.write(self.repo, rel, text)
        env = dict(ENV, GIT_AUTHOR_DATE=date, GIT_COMMITTER_DATE=date)
        subprocess.run(["git", "-C", str(self.repo), "add", "-A"], env=env, check=True, capture_output=True)
        subprocess.run(["git", "-C", str(self.repo), "commit", "-q", "-m", msg], env=env, check=True, capture_output=True)
        if push:
            git(self.repo, "push", "-q", "origin", "main")
        return git(self.repo, "rev-parse", "HEAD")

    def worktree_off(self, **lane):
        return self.registry(repos={"work": {"local": str(self.repo), "branch": "main", "remote_ref": "refs/remotes/origin/main",
                                             "worktree": "off", "history_limit": 50}}, **lane)

    def kinds(self, rep, kind):
        return [a["item"] for a in rep["attention"] if a["kind"] == kind]

    # PSI-01: Prime's exact counterexample, worktree on and off
    def test_psi01_unknown_hash_cannot_close(self):
        ret = "execution: returned\nDid."
        rid = prefix(batch(ret))
        self.commit(self.repo, {PAGE_FILE: batch(ret, review(f"reviewed_return_prefix: {rid}", "PS-X=unresolved"))})
        self.commit(self.repo, {PAGE_FILE: batch(ret, review("reviewed_return_prefix: " + "a" * 64, "PS-X=verified-fixed"))})
        for reg in (self.registry(), self.worktree_off()):
            rep = self.status_json(reg)
            f = finding(rep, "PS-X")
            self.assertEqual((f["resolution"], f["state"], f["passes"]), ("unresolved", "open", 1), f)
            unknown = [a for a in rep["attention"] if "a" * 12 in a["item"] or "unknown-hash" in a["item"]]
            self.assertTrue(unknown, rep["attention"])
            self.assertTrue(any("PS-X=verified-fixed" in a["item"] for a in unknown), unknown)

    # PSI-01: an invalid legacy whole-file hash cannot close either
    def test_psi01_invalid_legacy(self):
        ret = "Did. legacy"
        rid = prefix(batch(ret))
        self.commit(self.repo, {PAGE_FILE: batch(ret, review(f"reviewed_return_prefix: {rid}", "LX-1=unresolved"))})
        self.commit(self.repo, {PAGE_FILE: batch(ret, review("Reviewed return SHA-256: `" + "b" * 64 + "`.", "LX-1=verified-fixed"))})
        rep = self.status_json(self.registry())
        f = finding(rep, "LX-1")
        self.assertEqual((f["state"], f["passes"]), ("open", 1), f)
        self.assertTrue(any("invalid-legacy" in a["item"] for a in rep["attention"]), rep["attention"])

    # PSI-01: review sources bind only to a declared, registered target revision
    def test_psi01_review_source_binding(self):
        ret = "execution: returned\nDid."
        text = batch(ret)
        rid = prefix(text)
        src_ok, src_none, src_other = "notes/review-ok.md", "notes/review-none.md", "notes/review-other.md"
        self.commit(self.repo, {
            PAGE_FILE: text,
            src_ok: f"reviewed_return_path: {PAGE_FILE}\nreviewed_return_prefix: {rid}\nfindings: RS-1=unresolved\n",
            src_none: f"reviewed_return_prefix: {rid}\nfindings: RS-2=verified-fixed\n",
            src_other: f"reviewed_return_path: 00.kernel/elsewhere/05.01.md\nreviewed_return_prefix: {rid}\nfindings: RS-3=verified-fixed\n"})
        reg = self.registry(lanes=[{"lane": "fixture", "project": "w", "owner_label": "b", "repository": "work", "pages": [PAGE],
                                    "return_files": [], "review_sources": [src_ok, src_none, src_other]}])
        rep = self.status_json(reg)
        f = finding(rep, "RS-1")
        self.assertEqual((f["state"], f["passes"]), ("open", 1), f)
        self.assertIsNone(finding(rep, "RS-2"))
        self.assertIsNone(finding(rep, "RS-3"))
        self.assertEqual(len([a for a in rep["attention"] if "invalid-target" in a["item"]]), 2, rep["attention"])
        rev = self.file_entry(rep, "fixture", PAGE_FILE)["revisions"][0]
        self.assertEqual(rev["review"], "reviewed")

    # PSI-01: page-local IDs are scoped to their own return lineage
    def test_psi01_unrelated_ids_not_collapsed(self):
        other = f"{PAGE}/05.02.md"
        ret = "execution: returned\nDid."
        rid = prefix(batch(ret))
        self.commit(self.repo, {PAGE_FILE: batch(ret, review(f"reviewed_return_prefix: {rid}", "F-1=unresolved")),
                                other: batch(ret, review(f"reviewed_return_prefix: {rid}", "F-1=verified-fixed"))})
        rep = self.status_json(self.registry())
        self.assertEqual(finding(rep, "F-1", PAGE_FILE)["state"], "open")
        self.assertEqual(finding(rep, "F-1", other)["state"], "closed")
        self.assertEqual(len(next(l for l in rep["lanes"] if l["lane"] == "fixture")["findings"]), 2)

    # PSI-02: Prime's inverted-timestamp chain with the worktree off
    def test_psi02_inverted_timestamps(self):
        ret = "execution: returned\nDid."
        rid = prefix(batch(ret))
        self.commit_dated({PAGE_FILE: batch(ret, review(f"reviewed_return_prefix: {rid}", "PS-Y=verified-fixed"))}, "2030-01-01T00:00:00Z")
        self.commit_dated({PAGE_FILE: batch(ret, review(f"reviewed_return_prefix: {rid}", "PS-Y=unresolved"))}, "2029-01-01T00:00:00Z")
        rep = self.status_json(self.worktree_off())
        f = finding(rep, "PS-Y")
        self.assertEqual((f["resolution"], f["state"]), ("unresolved", "open"), f)

    # PSI-02: comparable refs (local behind the last-observed remote) resolve by ancestry
    def test_psi02_comparable_branches(self):
        ret = "execution: returned\nDid."
        rid = prefix(batch(ret))
        self.commit(self.repo, {PAGE_FILE: batch(ret, review(f"reviewed_return_prefix: {rid}", "CB-1=unresolved"))})
        self.commit_dated({PAGE_FILE: batch(ret, review(f"reviewed_return_prefix: {rid}", "CB-1=verified-fixed"))}, "2001-01-01T00:00:00Z")
        git(self.repo, "reset", "-q", "--hard", "HEAD~1")  # fixture only: local behind origin/main
        rep = self.status_json(self.worktree_off())
        self.assertEqual(rep["repositories"]["work"]["relation"], "local behind last-observed remote (stale local)")
        f = finding(rep, "CB-1")
        self.assertEqual((f["resolution"], f["state"]), ("verified-fixed", "closed"), f)

    # PSI-02: divergent incomparable resolutions are an explicit conflict
    def test_psi02_divergent_conflict(self):
        ret = "execution: returned\nDid."
        rid = prefix(batch(ret))
        self.commit(self.repo, {PAGE_FILE: batch(ret, review(f"reviewed_return_prefix: {rid}", "DV-1=unresolved"))})
        git(self.repo, "branch", "side")
        self.commit(self.repo, {PAGE_FILE: batch(ret, review(f"reviewed_return_prefix: {rid}", "DV-1=verified-fixed"))}, push=False)
        git(self.repo, "checkout", "-q", "side")
        self.commit(self.repo, {PAGE_FILE: batch(ret, review(f"reviewed_return_prefix: {rid}", "DV-1=director-pending"))}, push=False)
        git(self.repo, "push", "-q", "--force", "origin", "side:main")
        git(self.repo, "fetch", "-q", "origin")  # fixture only: record the divergent remote ref locally
        git(self.repo, "checkout", "-q", "main")
        rep = self.status_json(self.worktree_off())
        self.assertEqual(rep["repositories"]["work"]["relation"], "diverged")
        f = finding(rep, "DV-1")
        self.assertEqual(f["state"], "conflict", f)
        self.assertEqual(sorted(r["resolution"] for r in f["frontier"]), ["director-pending", "verified-fixed"])
        self.assertTrue(any(a["kind"] == "conflict" and "DV-1" in a["item"] for a in rep["attention"]), rep["attention"])

    # PSI-02: an uncommitted draft never conceals a committed open finding
    def test_psi02_worktree_draft(self):
        ret = "execution: returned\nDid."
        rid = prefix(batch(ret))
        self.commit(self.repo, {PAGE_FILE: batch(ret, review(f"reviewed_return_prefix: {rid}", "WD-1=unresolved"))})
        self.write(self.repo, PAGE_FILE, batch(ret, review(f"reviewed_return_prefix: {rid}", "WD-1=verified-fixed")))
        rep = self.status_json(self.registry())
        f = finding(rep, "WD-1")
        self.assertEqual((f["resolution"], f["state"], f.get("draft")), ("unresolved", "open", "verified-fixed"), f)
        self.assertTrue(any("draft differs" in a["item"] for a in rep["attention"]), rep["attention"])
        rep = self.status_json(self.worktree_off())
        f = finding(rep, "WD-1")
        self.assertEqual((f["state"], f.get("draft")), ("open", None))

    # PSI-02: repeated observations of the same review do not add passes
    def test_psi02_repeated_observations(self):
        ret = "execution: returned\nDid."
        rid = prefix(batch(ret))
        for n in range(3):
            self.commit(self.repo, {PAGE_FILE: batch(ret, review(f"reviewed_return_prefix: {rid}", "RP-1=unresolved", extra=f"note {n}\n"))})
        rep = self.status_json(self.registry())
        f = finding(rep, "RP-1")
        self.assertEqual((f["state"], f["passes"], f.get("draft")), ("open", 1, None), f)
        entry = self.file_entry(rep, "fixture", PAGE_FILE)
        self.assertEqual(len({r["revision_id"] for r in entry["revisions"]}), 1)

    # acknowledgement-store deletion leaves a conflict and a bound finding exactly as they were
    def test_psi_ack_deletion(self):
        ret = "execution: returned\nDid."
        text = batch(ret, review(f"reviewed_return_prefix: {prefix(batch(ret))}", "AD-1=unresolved"))
        self.commit(self.repo, {PAGE_FILE: text})
        reg = self.registry()
        rid = prefix(text)
        self.ack(reg, PAGE_FILE, rid, code=0)
        before = finding(self.status_json(reg), "AD-1")
        shutil.rmtree(self.store)
        after = finding(self.status_json(reg), "AD-1")
        self.assertEqual(before, after)
        self.assertEqual(after["state"], "open")


for _name in [n for n in vars(tps.Fixture) if n.startswith("test_")]:
    setattr(PSI, _name, None)

if __name__ == "__main__":
    unittest.main()
