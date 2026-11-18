"""Build disposable 0705 pass02 case fixtures from pinned pack05.02 snapshot bytes plus declarative ops.

  python -I -B build_fixture.py --cases ABS --manifest ABS --out ABS [--case ID|all]

--out must not exist, must have an existing parent, and must resolve outside this checkout.
Bytes come only from snapshots listed in --manifest, after their sha256 and length are checked.
Nothing is read from live pages, nothing is removed or reused. Exit 0 built, 2 refused.
"""
import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parent
CHECKOUT = LAB.parents[3]
SCHEMA = "desk-fixture/1"


class Refused(Exception):
    pass


def need(ok, msg):
    if not ok:
        raise Refused(msg)


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def strict_load(path: Path):
    def pairs(items):
        keys = [k for k, _ in items]
        need(len(keys) == len(set(keys)), f"{path.name}: duplicate key")
        return dict(items)
    return json.loads(path.read_bytes().decode("utf-8"), object_pairs_hook=pairs)


def snapshot_bytes(manifest_path: Path, manifest: dict) -> dict:
    out = {}
    for row in manifest["sources"]:
        b = (manifest_path.parent / row["snapshot"]).read_bytes()
        need(sha(b) == row["sha256"] and len(b) == row["bytes"], f"snapshot for {row['path']} does not match its pin")
        out[row["path"]] = b
    return out


def inside(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def write_new(path: Path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "xb") as f:
        f.write(data)


def apply_line_op(data: bytes, op: dict) -> bytes:
    text = data.decode("utf-8")
    lines = text.split("\n")
    if op["op"] == "replace-line":
        hits = [i for i, l in enumerate(lines) if l.startswith(op["key"] + ": ")]
        need(len(hits) == 1, f"replace-line: key {op['key']} occurs {len(hits)} times")
        lines[hits[0]] = f"{op['key']}: {op['value']}"
    elif op["op"] == "duplicate-line":
        hits = [i for i, l in enumerate(lines) if l.startswith(op["key"] + ": ")]
        need(len(hits) == 1, f"duplicate-line: key {op['key']} occurs {len(hits)} times")
        lines.insert(hits[0] + 1, lines[hits[0]])
    elif op["op"] == "append-line":
        if lines and lines[-1] == "":
            lines.insert(len(lines) - 1, op["text"])
        else:
            lines.append(op["text"])
    elif op["op"] == "append-section":
        body = op["text"].rstrip("\n").split("\n")
        if lines and lines[-1] == "":
            lines[-1:-1] = [""] + body
        else:
            lines += [""] + body
    else:
        raise Refused(f"unknown line op {op['op']}")
    return "\n".join(lines).encode("utf-8")


def derive(case: dict, snaps: dict) -> dict:
    out = {}
    for d in case.get("derive", []):
        if d["kind"] == "blockquote-under-heading":
            text = snaps[d["path"]].decode("utf-8")
            start = text.index(d["heading"] + "\n") + len(d["heading"]) + 1
            seg = text[start:].split("\n")
            quote = []
            for l in seg:
                if l.startswith(">"):
                    quote.append(l)
                elif quote:
                    break
            need(quote, f"no blockquote under {d['heading']}")
            out[d["name"]] = sha(("\n".join(quote) + "\n").encode("utf-8"))
        else:
            raise Refused(f"unknown derive kind {d['kind']}")
    return out


def build_case(case: dict, snaps: dict, out: Path, manifest_sha: str) -> dict:
    root = out / case["id"]
    root.mkdir()
    instances = {"instance-A": {}}
    generated, omitted = [], []
    for name in case.get("instances", ["instance-A"]):
        instances.setdefault(name, {})
    for name in instances:
        (root / name).mkdir()
    # copy declared sources into each instance from snapshots
    for name in instances:
        for p in case["copy"]:
            need(p in snaps, f"{case['id']}: source {p} is not a pinned snapshot")
            instances[name][p] = snaps[p]
    for op in case["ops"]:
        inst = op.get("instance", "instance-A")
        if op["op"] in ("replace-line", "duplicate-line", "append-line", "append-section"):
            need(op["path"] in instances[inst], f"{case['id']}: op on uncopied {op['path']}")
            instances[inst][op["path"]] = apply_line_op(instances[inst][op["path"]], op)
            generated.append(f"{inst}/{op['path']}")
        elif op["op"] == "construct":
            need(op["path"] not in instances[inst], f"{case['id']}: construct over a copied file {op['path']}")
            data = op["text"].encode("utf-8") if "text" in op else snaps[op["copy_of"]]
            instances[inst][op["path"]] = data
            generated.append(f"{inst}/{op['path']}")
        elif op["op"] == "omit":
            need(op["path"] not in instances[inst], f"{case['id']}: omit of a copied file")
            omitted.append({"instance": inst, "path": op["path"], "expected_sha256": op["expected_sha256"],
                            "note": "deliberately absent from this bounded fixture; not a claim about the workspace"})
        else:
            raise Refused(f"unknown op {op['op']}")
    files = {}
    for name, fs in instances.items():
        files[name] = {}
        for rel, data in fs.items():
            write_new(root / name / rel, data)
            files[name][rel] = sha(data)
    # catalog: a generated, supplied index for the candidate (not an authority)
    cat = dict(case["catalog"])
    cat["schema"] = "desk-fixture-catalog/1"
    cat["note"] = "GENERATED supplied index for this fixture; not an authority; facts live in the instance files"
    cat["instance_roots"] = {n: str(root / n) for n in instances}
    cat_bytes = (json.dumps(cat, indent=1, ensure_ascii=False) + "\n").encode("utf-8")
    write_new(root / "catalog.json", cat_bytes)
    fm = {"schema": SCHEMA, "case": case["id"], "kind": case["kind"],
          "label": "SYNTHETIC/CONSTRUCTED where listed in generated; copied bytes are pack05.02 snapshots",
          "built_from": {"manifest_sha256": manifest_sha},
          "instances": {n: {"root": str(root / n), "files": files[n]} for n in instances},
          "catalog": {"path": str(root / "catalog.json"), "sha256": sha(cat_bytes)},
          "generated": sorted(set(generated)), "omitted": omitted, "ops": case["ops"],
          "derived": derive(case, snaps)}
    write_new(root / "fixture-manifest.json", (json.dumps(fm, indent=1, ensure_ascii=False) + "\n").encode("utf-8"))
    return fm


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--case", default="all")
    a = ap.parse_args(argv)
    try:
        out = Path(a.out)
        need(out.is_absolute(), "--out must be absolute")
        need(not os.path.lexists(out), f"--out {out} already exists; refusing to reuse or remove it")
        need(out.parent.is_dir(), "--out parent must exist")
        need(not inside(out.parent.resolve(), CHECKOUT.resolve()), f"--out must be outside the checkout {CHECKOUT}")
        man_path = Path(a.manifest)
        manifest = strict_load(man_path)
        snaps = snapshot_bytes(man_path, manifest)
        cases = strict_load(Path(a.cases))
        todo = [c for c in cases["cases"] if c.get("build") and (a.case == "all" or c["id"] == a.case)]
        need(todo, f"no buildable case {a.case}")
        out.mkdir()
        built = [build_case(c, snaps, out, sha(man_path.read_bytes()))["case"] for c in todo]
    except (Refused, OSError, ValueError, KeyError) as e:
        print(f"refused: {type(e).__name__}: {e}", file=sys.stderr)
        return 2
    sys.stdout.buffer.write((json.dumps({"schema": "desk-fixture-build/1", "out": str(out), "built": built}, indent=1) + "\n").encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
