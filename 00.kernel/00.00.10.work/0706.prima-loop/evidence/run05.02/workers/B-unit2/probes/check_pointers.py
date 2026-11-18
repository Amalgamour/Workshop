import hashlib, json, os, sys
W = "/workspace/prima/run0502/source-room/00.kernel/00.00.10.work"
ROOM = "/workspace/prima/run0502/source-room"
claims = [  # (page:line, path, sha256, bytes) copied from Return pointers
 ("0512/05.05.md:33", "0512.prime-review/evidence/build05.05/submission.md", "95c5cc4239a1698711f9f75d367a65018cc4961f60a6777855a2c80d51d57d2f", 10694),
 ("0512/05.05.md:34", "0512.prime-review/evidence/build05.05/artifact-manifest.json", "7e52850f97f89f942b8478293e153ec1922687d5c32d38d1642be6dcafa053af", 4864),
 ("0512/05.06.md:24", "0512.prime-review/evidence/build05.06/submission.md", "dc5b52a7aeed664dae8e798ed37e7c20f7a1bf1f72ea4c4a77e2233e21cbaf53", 12303),
 ("0512/05.06.md:25", "0512.prime-review/evidence/build05.06/artifact-manifest.json", "983efc6a8a236456c76c40161fb2024a977e7c39eda5894f1d689920dc748d0a", 3168),
 ("0512/05.07.md:30", "0512.prime-review/evidence/build05.07/submission.md", "dfefe8754c4153d5a8228adfc0c80725d046bc3dd6df0744f49f2648ebee8a87", 8252),
 ("0512/05.07.md:31", "0512.prime-review/evidence/build05.07/artifact-manifest.json", "dfd5ea00aca3265dd049d04cb101507a18fa5f4db84664fa26ab1ad68f97bef4", 4977),
 ("0521/05.13.md:34", "0521.return-placement/evidence/build05.13/submission.md", "da8fe0640bbd9c95c46a757f973e7fdabcdf70e6a1620a3d4b7d946329c28a50", 1049),
 ("0521/05.13.md:35", "0521.return-placement/evidence/build05.13/artifact-manifest.json", "0a71b39c5165310dab1748efc01dc851683c1845e21a7b03644cb00f8f64e019", 1790),
]
for where, rel, sha, size in claims:
    p = os.path.join(W, rel)
    if not os.path.exists(p):
        print(f"ABSENT   {where} {rel}"); continue
    b = open(p, "rb").read(); h = hashlib.sha256(b).hexdigest()
    print(f"{'MATCH ' if (h, len(b)) == (sha, size) else 'DIFFER'}   {where} {rel} actual {h[:16]} {len(b)}")
for man in ["0512.prime-review/evidence/build05.06/artifact-manifest.json", "0521.return-placement/evidence/build05.13/artifact-manifest.json"]:
    d = json.load(open(os.path.join(W, man)))
    print("== manifest", man, "keys", list(d) if isinstance(d, dict) else type(d))
    rows = d.get("files") or d.get("artifacts") or d.get("entries") if isinstance(d, dict) else d
    for r in rows or []:
        path = r.get("path") or r.get("logical")
        cand = [os.path.join(ROOM, path), os.path.join(W, path), os.path.join(W, os.path.dirname(man), path)]
        hit = next((c for c in cand if os.path.isfile(c)), None)
        if hit is None:
            print("  NOT-IN-ROOM", path, r.get("sha256", "")[:16], r.get("bytes")); continue
        b = open(hit, "rb").read(); ok = hashlib.sha256(b).hexdigest() == r.get("sha256") and len(b) == r.get("bytes")
        print("  ", "MATCH " if ok else "DIFFER", path)
