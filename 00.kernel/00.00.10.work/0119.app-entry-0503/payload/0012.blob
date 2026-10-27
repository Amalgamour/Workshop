"""execute=False versus execute=True per assignment state, in the disposable copy.
python -B status_probe.py <copy-root> <out-file>"""
import shutil
import sys
from pathlib import Path

WS = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(WS / "app" / "tests"))
sys.path.insert(0, str(WS / "app"))
import test_entry as T  # noqa: E402
import context as C  # noqa: E402

config = C.load_config(WS / "app" / "development-workspace.json")
lines = []
for state in ("released", "running", "returned", "accepted", "stopped", "waiting"):
    root = WS / "app" / "scratch" / f"status-{state}"
    if root.exists():
        shutil.rmtree(root)
    T.make_fixture(root, state)
    row = [state]
    for execute in (False, True):
        try:
            got = C.validate_context(root, config, execute=execute, runner_root=WS)
            row.append(f"execute={execute}: pass ({got.assignment_state})")
        except C.Stop as exc:
            row.append(f"execute={execute}: stop: {exc}")
    # runner_root omitted: the fixture root must then hold its own runner copy
    try:
        C.validate_context(root, config, execute=False)
        row.append("runner_root omitted: pass")
    except C.Stop as exc:
        row.append(f"runner_root omitted: stop: {exc}")
    lines.append(" | ".join(row))
    shutil.rmtree(root)
Path(sys.argv[2]).write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
