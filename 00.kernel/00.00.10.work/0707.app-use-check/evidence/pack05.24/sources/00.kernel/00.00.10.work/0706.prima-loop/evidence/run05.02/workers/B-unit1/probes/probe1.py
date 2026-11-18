import json, sys
sys.path.insert(0, "/workspace/prima/run0502/workers/B/probes")
from extract import load
p1, p2, p3, hashes = load()
H = "a" * 64; H2 = "b" * 64
def insp(rows, measurement="complete", findings=None):
    return {"measurement": measurement, "form": {"bindings": {"rows": rows}}, "findings": findings or []}
def show(label, body):
    keep = {k: body.get(k) for k in ("count", "count_state", "bytes", "bytes_state", "provenance", "scope")}
    keep["addressed"] = body["addressed_sources"]; keep["content"] = body["content_blobs"]
    keep["intake_roles"] = {k: body["intake_roles"].get(k) for k in ("count", "bytes", "bytes_state")}
    keep["rows_kept"] = None if body.get("rows") is None else len(body["rows"])
    print("##", label); print(json.dumps(keep, indent=1, sort_keys=True))
art = lambda **k: dict({"role": "artifact", "root": "R", "path": "a.txt", "sha256": H, "bytes": 10, "declared_sha256": H, "declared_bytes": 10}, **k)
cases = {
 "P1 baseline one row": [art()],
 "P2 bytes missing (null) single row": [art(bytes=None)],
 "P3 non-dict row mixed in": [art(), "garbage", 7, None],
 "P4 empty rows, measurement complete": [],
 "P5 negative bytes": [art(bytes=-10, declared_bytes=-10)],
 "P6 uppercase sha": [art(sha256=H.upper(), declared_sha256=H.upper())],
 "P7 same path, two roots differing only in slash": [art(root="D:\\Git\\lib-build"), art(root="D:/Git/lib-build")],
 "P8 bool bytes": [art(bytes=True, declared_bytes=True)],
 "P9 declared counts from intake rows only (no artifact role)": [art(role="source")],
}
for k, rows in cases.items():
    show(k, p3.artifacts_of(insp(rows)))
print("## P10 measurement not str (True)"); b = p3.artifacts_of({"measurement": True, "form": {"bindings": {"rows": [art()]}}}); print(b["measurement"], b["addressed_sources"]["count_state"], b["addressed_sources"].get("reason"))
print("## P11 same(): NaN"); print(p1.same(float("nan"), float("nan")))
print("## P12 apply_envelope copies arbitrary types");
r = {}; e = {k: None for k in p1.ENVELOPE}; e.update(authority="Director", accepted="yes", releases_action={"x": 1})
print(p1.apply_envelope(r, dict(e), dict(e), dict(e)), json.dumps(r, sort_keys=True), "word:", p1.word(r["authority"]), p1.word(r["action_released"]))
print("## hashes", json.dumps(hashes, indent=1))
