#!/usr/bin/env python3
"""0510/05.06 pass02: NONPRODUCTION in-memory model of the PROPOSED workflow connectors.

It models what labs/colab-workflow-pass02 does not have today (06.07 S1-S4):
  open-pass          add a later pass slot on an existing N7NN page, only when the
                     prior pass's recorded review route is request-next naming it
  seal-return-local  fill a pass's return slot from supplied return bytes, page-local,
                     with no N1NN member; exact bytes; occupied-different refuses
  transitions        an append-only, hash-chained list inside the page record; a new
                     record must extend the old list unchanged (prefix rule)
It writes nothing. The real workflow is not imported or changed.
"""

from __future__ import annotations

import copy
import hashlib
import json

LOCAL_RETURN = "colab-exchange-local-return/1"


class Refuse(Exception):
    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _append(record: dict, action: str, pass_id: str, **facts) -> dict:
    chain = record["transitions"]
    t = {"seq": len(chain) + 1, "action": action, "pass": pass_id, "prev": chain[-1]["sha256"] if chain else None, **facts}
    t["sha256"] = sha(canonical(t))
    chain.append(t)
    return t


def open_page(book: str, page: str, pass_id: str) -> dict:
    record = {"book": book, "page": page, "passes": {pass_id: {"package": None, "return": None, "review": None}}, "transitions": []}
    _append(record, "open", pass_id)
    return record


def attach(record: dict, pass_id: str, digest: str) -> dict:
    r = copy.deepcopy(record)
    slot = r["passes"].get(pass_id)
    if slot is None:
        raise Refuse("missing investigation")
    if slot["package"] is not None:
        if slot["package"] == {"digest": digest}:
            return record
        raise Refuse("occupied different content")
    slot["package"] = {"digest": digest}
    _append(r, "attach", pass_id, digest=digest)
    return r


def seal_return_local(record: dict, pass_id: str, raw: bytes, declared_transport: str) -> dict:
    r = copy.deepcopy(record)
    slot = r["passes"].get(pass_id)
    if slot is None or slot["package"] is None:
        raise Refuse("missing investigation")
    placed = {"schema": LOCAL_RETURN, "return_sha256": sha(raw), "return_bytes": len(raw),
              "declared_transport": declared_transport, "package_digest": slot["package"]["digest"]}
    if slot["return"] is not None:
        if slot["return"] == placed:
            return record
        raise Refuse("occupied different content")
    slot["return"] = placed
    _append(r, "seal-return", pass_id, return_sha256=placed["return_sha256"], return_bytes=placed["return_bytes"])
    return r


def review(record: dict, pass_id: str, route: str, next_pass: str | None, review_bytes: bytes) -> dict:
    r = copy.deepcopy(record)
    slot = r["passes"].get(pass_id)
    if slot is None or slot["package"] is None:
        raise Refuse("missing investigation")
    if slot["return"] is None:
        raise Refuse("review before return")
    if slot["review"] is not None:
        if slot["review"] == {"route": route, "next_pass": next_pass, "sha256": sha(review_bytes)}:
            return record
        raise Refuse("occupied different content")
    slot["review"] = {"route": route, "next_pass": next_pass, "sha256": sha(review_bytes)}
    _append(r, "review", pass_id, route=route, next_pass=next_pass, review_sha256=sha(review_bytes))
    return r


def open_pass(record: dict, pass_id: str) -> dict:
    r = copy.deepcopy(record)
    if pass_id in r["passes"]:
        raise Refuse("occupied pass")
    asking = [t for t in r["transitions"] if t["action"] == "review" and t.get("route") == "request-next" and t.get("next_pass") == pass_id]
    if len(asking) != 1:
        raise Refuse("next pass not requested")
    r["passes"][pass_id] = {"package": None, "return": None, "review": None}
    _append(r, "open-pass", pass_id, requested_by_seq=asking[0]["seq"])
    return r


def extends(old: dict, new: dict) -> None:
    """Prefix rule: a write may only append transitions."""
    o, n = old["transitions"], new["transitions"]
    if len(n) < len(o) or n[: len(o)] != o:
        raise Refuse("history rewritten")
