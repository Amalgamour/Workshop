from pathlib import Path
import json

root=Path(r'D:\Git\Librarian\colab').resolve()
assert root.is_dir()
manifest=json.loads(Path(r'D:\librarian\temp\law-design-build\payload\manifest.json').read_text(encoding='utf-8'))
targets=[]
for name,body in manifest.items():
    target=(root/'designs'/name).resolve()
    assert target.is_relative_to(root/'designs') or target.is_relative_to(root/'notes'),target
    assert not target.exists(),f'Existing file would be overwritten: {target}'
    targets.append((target,body))
# Capture working notes first, then install the reviewable design.
targets.sort(key=lambda item: 0 if item[0].is_relative_to(root/'notes') else 1)
for target,body in targets:
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(body.encode('utf-8'))
for target,body in targets:
    assert target.read_bytes()==body.encode('utf-8'),target
print(f'Created and verified {len(targets)} files; no existing files overwritten.')
print(root/'designs'/'law.draft')
