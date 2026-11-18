#!/usr/bin/env python3
"""0707/05.05 pass05: contain a launched child and its descendants in a Windows Job Object (H01).

Only processes in the job this harness created are terminated. A descendant that
starts in the moment between process start and job assignment could escape; that
uncertainty is recorded. Non-Windows hosts use a process group (not exercised here).
"""

from __future__ import annotations

import ctypes
import os
import signal
import subprocess
from ctypes import wintypes

KILL_ON_JOB_CLOSE = 0x2000
JOB_EXTENDED = 9
JOB_ACCOUNTING = 1


class IO_COUNTERS(ctypes.Structure):
    _fields_ = [(n, ctypes.c_ulonglong) for n in ("ReadOperationCount", "WriteOperationCount", "OtherOperationCount",
                                                  "ReadTransferCount", "WriteTransferCount", "OtherTransferCount")]


class BASIC_LIMIT(ctypes.Structure):
    _fields_ = [("PerProcessUserTimeLimit", ctypes.c_int64), ("PerJobUserTimeLimit", ctypes.c_int64),
                ("LimitFlags", wintypes.DWORD), ("MinimumWorkingSetSize", ctypes.c_size_t),
                ("MaximumWorkingSetSize", ctypes.c_size_t), ("ActiveProcessLimit", wintypes.DWORD),
                ("Affinity", ctypes.c_size_t), ("PriorityClass", wintypes.DWORD), ("SchedulingClass", wintypes.DWORD)]


class EXTENDED_LIMIT(ctypes.Structure):
    _fields_ = [("BasicLimitInformation", BASIC_LIMIT), ("IoInfo", IO_COUNTERS), ("ProcessMemoryLimit", ctypes.c_size_t),
                ("JobMemoryLimit", ctypes.c_size_t), ("PeakProcessMemoryUsed", ctypes.c_size_t), ("PeakJobMemoryUsed", ctypes.c_size_t)]


class ACCOUNTING(ctypes.Structure):
    _fields_ = [("TotalUserTime", ctypes.c_int64), ("TotalKernelTime", ctypes.c_int64), ("ThisPeriodTotalUserTime", ctypes.c_int64),
                ("ThisPeriodTotalKernelTime", ctypes.c_int64), ("TotalPageFaultCount", wintypes.DWORD),
                ("TotalProcesses", wintypes.DWORD), ("ActiveProcesses", wintypes.DWORD), ("TotalTerminatedProcesses", wintypes.DWORD)]


class Containment:
    """Created per launch. method is 'job', 'taskkill-fallback' or 'process-group'."""

    def __init__(self, proc: subprocess.Popen) -> None:
        self.proc = proc
        self.handle = None
        self.method = "process-group"
        self.note = None
        if os.name != "nt":
            return
        k32 = ctypes.WinDLL("kernel32", use_last_error=True)
        k32.CreateJobObjectW.restype = wintypes.HANDLE
        k32.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
        k32.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
        k32.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
        k32.QueryInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD, ctypes.c_void_p]
        k32.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
        k32.CloseHandle.argtypes = [wintypes.HANDLE]
        self.k32 = k32
        handle = k32.CreateJobObjectW(None, None)
        if not handle:
            self.method, self.note = "taskkill-fallback", f"CreateJobObject failed {ctypes.get_last_error()}"
            return
        info = EXTENDED_LIMIT()
        info.BasicLimitInformation.LimitFlags = KILL_ON_JOB_CLOSE
        ok = k32.SetInformationJobObject(handle, JOB_EXTENDED, ctypes.byref(info), ctypes.sizeof(info))
        ok = ok and k32.AssignProcessToJobObject(handle, int(proc._handle))
        if not ok:
            self.note = f"job setup failed {ctypes.get_last_error()}"
            k32.CloseHandle(handle)
            self.method = "taskkill-fallback"
            return
        self.handle = handle
        self.method = "job"
        self.note = "a descendant started before job assignment could escape (start-to-assign window)"

    def active(self) -> int | None:
        if self.method != "job":
            return None
        acct = ACCOUNTING()
        if not self.k32.QueryInformationJobObject(self.handle, JOB_ACCOUNTING, ctypes.byref(acct), ctypes.sizeof(acct), None):
            return None
        return int(acct.ActiveProcesses)

    def terminate(self) -> dict:
        if self.method == "job":
            ok = bool(self.k32.TerminateJobObject(self.handle, 1))
            return {"method": "TerminateJobObject on this harness's job", "ok": ok}
        if self.method == "taskkill-fallback":
            r = subprocess.run(["taskkill", "/PID", str(self.proc.pid), "/T", "/F"], capture_output=True, timeout=30)
            return {"method": "taskkill /T /F on the launched child pid", "ok": r.returncode == 0, "exit": r.returncode}
        try:
            os.killpg(self.proc.pid, signal.SIGKILL)
            return {"method": "killpg on the child's session", "ok": True}
        except ProcessLookupError:
            return {"method": "killpg", "ok": True, "note": "already exited"}

    def close(self) -> None:
        if self.method == "job" and self.handle:
            self.k32.CloseHandle(self.handle)
            self.handle = None
