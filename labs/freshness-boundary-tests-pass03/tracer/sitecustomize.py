"""LAB AUDIT TRACER (0707/05.25). Test-environment instrumentation, NOT candidate code.
Loaded only when the test equipment prepends this directory to PYTHONPATH and sets LAB_AUDIT_LOG and LAB_AUDIT_ROOT.
Records audit events whose path lies under LAB_AUDIT_ROOT (the disposable candidate copy), one JSON line each:
  run_file  cpython.run_file (a script executed as __main__)
  exec      exec of a code object compiled from a file (module import / spec.loader.exec_module / runpy)
  compile   compile() of source attributed to a file
  open      a file opened (read or write)
  popen     subprocess.Popen (all, with argv), to bind evidence to the probe command
It never changes behaviour: every failure inside the hook is swallowed.
"""
import json
import os
import sys

_LOG = os.environ.get("LAB_AUDIT_LOG")
_ROOT = os.environ.get("LAB_AUDIT_ROOT")


def _norm(p):
    try:
        return os.path.normcase(os.path.abspath(os.fspath(p)))
    except Exception:
        return None


if _LOG and _ROOT:
    _R = _norm(_ROOT)
    _PID = os.getpid()
    _ARGV = list(sys.argv)

    def _under(p):
        if isinstance(p, str) and p.startswith("<"):        # <frozen ...>, <string>: not files
            return None
        n = _norm(p) if isinstance(p, (str, bytes, os.PathLike)) else None
        return n if n and (n == _R or n.startswith(_R + os.sep)) else None

    _LOGN = _norm(_LOG)
    _BUSY = [False]       # audit-check run01: writing the log re-entered the 'open' hook (self-logging loop)

    def _w(kind, path, extra=None):
        if path is not None and path == _LOGN:
            return
        _BUSY[0] = True
        try:
            with open(_LOG, "a", encoding="utf-8") as f:
                f.write(json.dumps({"pid": _PID, "argv": list(sys.argv) or _ARGV, "event": kind, "path": path, "extra": extra}) + "\n")
        except Exception:
            pass
        finally:
            _BUSY[0] = False

    def _hook(event, args):
        if _BUSY[0]:
            return
        try:
            if event == "cpython.run_file":
                p = _under(args[0])
                if p:
                    _w("run_file", p)
            elif event == "exec":
                co = args[0]
                p = _under(getattr(co, "co_filename", None))
                if p:
                    _w("exec", p)
            elif event == "compile":
                p = _under(args[1]) if len(args) > 1 and isinstance(args[1], (str, bytes)) else None
                if p:
                    _w("compile", p)
            elif event == "open":
                p = _under(args[0]) if isinstance(args[0], (str, bytes, os.PathLike)) else None
                if p:
                    _w("open", p, {"mode": str(args[1])})
            elif event == "subprocess.Popen":
                a = args[1]
                _w("popen", None, {"argv": a[:400] if isinstance(a, str) else [str(x) for x in (a or [])][:12]})
        except Exception:
            pass

    sys.addaudithook(_hook)
