import ctypes
import ctypes.wintypes
import subprocess
import time
from datetime import datetime

import psutil
import win32api
import win32con
import win32gui
import win32process

from constants import WINDOW_CLASS_BLACKLIST, MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT
from monitor_manager import get_monitors, find_monitor_index

# DwmGetWindowAttribute for cloaked check
_dwmapi = ctypes.WinDLL("dwmapi", use_last_error=True)
DWMWA_CLOAKED = 14


def _is_cloaked(hwnd):
    cloaked = ctypes.c_int(0)
    result = _dwmapi.DwmGetWindowAttribute(
        hwnd, DWMWA_CLOAKED, ctypes.byref(cloaked), ctypes.sizeof(cloaked)
    )
    return result == 0 and cloaked.value != 0


def _should_capture(hwnd):
    if not win32gui.IsWindowVisible(hwnd):
        return False

    title = win32gui.GetWindowText(hwnd)
    if not title:
        return False

    cls = win32gui.GetClassName(hwnd)
    if cls in WINDOW_CLASS_BLACKLIST:
        return False

    if _is_cloaked(hwnd):
        return False

    # Skip tool windows that aren't app windows
    ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    if (ex_style & win32con.WS_EX_TOOLWINDOW) and not (ex_style & win32con.WS_EX_APPWINDOW):
        return False

    # Skip tiny windows
    rect = win32gui.GetWindowRect(hwnd)
    w = rect[2] - rect[0]
    h = rect[3] - rect[1]
    if w < MIN_WINDOW_WIDTH or h < MIN_WINDOW_HEIGHT:
        return False

    return True


def _get_process_info(hwnd):
    exe_path = None
    command_line = None
    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        proc = psutil.Process(pid)
        exe_path = proc.exe()
        command_line = " ".join(f'"{a}"' if " " in a else a for a in proc.cmdline())
    except (psutil.AccessDenied, psutil.NoSuchProcess, OSError):
        pass
    return exe_path, command_line


def capture_layout():
    """Capture current window positions and monitor info."""
    monitors = get_monitors()
    windows = []

    def enum_callback(hwnd, _):
        if not _should_capture(hwnd):
            return True

        title = win32gui.GetWindowText(hwnd)
        cls = win32gui.GetClassName(hwnd)
        rect = list(win32gui.GetWindowRect(hwnd))
        placement = win32gui.GetWindowPlacement(hwnd)
        exe_path, command_line = _get_process_info(hwnd)

        mon_idx = find_monitor_index(monitors, rect)

        windows.append({
            "title": title,
            "exe_path": exe_path,
            "command_line": command_line,
            "window_class": cls,
            "placement": {
                "show_cmd": placement[1],
                "normal_position": list(placement[4]),
                "min_position": list(placement[2]),
                "max_position": list(placement[3]),
            },
            "rect": rect,
            "monitor_index": mon_idx,
            "monitor_device": monitors[mon_idx]["device_name"],
        })
        return True

    win32gui.EnumWindows(enum_callback, None)

    return {
        "timestamp": datetime.now().isoformat(),
        "monitors": monitors,
        "windows": windows,
    }


def restore_layout(layout_data):
    """Restore window positions from saved layout data."""
    saved_windows = layout_data.get("windows", [])
    if not saved_windows:
        return 0, 0

    # Build list of current windows
    current = []

    def enum_callback(hwnd, _):
        if not _should_capture(hwnd):
            return True
        cls = win32gui.GetClassName(hwnd)
        exe_path, _ = _get_process_info(hwnd)
        current.append({"hwnd": hwnd, "exe_path": exe_path, "window_class": cls})
        return True

    win32gui.EnumWindows(enum_callback, None)

    matched = 0
    used_hwnds = set()

    for saved in saved_windows:
        best_hwnd = None

        # Try matching by exe_path + window_class
        for cur in current:
            if cur["hwnd"] in used_hwnds:
                continue
            if cur["exe_path"] == saved.get("exe_path") and cur["window_class"] == saved.get("window_class"):
                best_hwnd = cur["hwnd"]
                break

        # Fallback: match by window_class only
        if best_hwnd is None:
            for cur in current:
                if cur["hwnd"] in used_hwnds:
                    continue
                if cur["window_class"] == saved.get("window_class"):
                    best_hwnd = cur["hwnd"]
                    break

        if best_hwnd is None:
            continue

        used_hwnds.add(best_hwnd)

        try:
            p = saved["placement"]
            placement_tuple = (
                0,
                p["show_cmd"],
                tuple(p["min_position"]),
                tuple(p["max_position"]),
                tuple(p["normal_position"]),
            )
            # Restore from minimized first
            if win32gui.IsIconic(best_hwnd):
                win32gui.ShowWindow(best_hwnd, win32con.SW_RESTORE)
            win32gui.SetWindowPlacement(best_hwnd, placement_tuple)
            matched += 1
        except Exception:
            pass

    return matched, len(saved_windows)


def launch_and_restore(layout_data, wait_seconds=10, max_wait=60):
    """Launch saved applications, wait for them to appear, then restore positions.

    Used on system startup to recreate the full desktop layout.
    """
    saved_windows = layout_data.get("windows", [])
    if not saved_windows:
        return 0, 0

    # Collect unique exe paths to launch
    launched = set()
    for win in saved_windows:
        exe = win.get("exe_path")
        if not exe:
            continue
        # Normalize path for dedup
        exe_lower = exe.lower()
        if exe_lower in launched:
            continue
        launched.add(exe_lower)

        # Check if already running
        already_running = False
        for proc in psutil.process_iter(["exe"]):
            try:
                if proc.info["exe"] and proc.info["exe"].lower() == exe_lower:
                    already_running = True
                    break
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                continue

        if already_running:
            continue

        # Launch the application
        try:
            subprocess.Popen(
                [exe],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.DETACHED_PROCESS,
            )
        except OSError:
            pass

    # Wait for windows to appear, then restore positions
    elapsed = 0
    best_matched = 0
    while elapsed < max_wait:
        time.sleep(wait_seconds)
        elapsed += wait_seconds
        matched, total = restore_layout(layout_data)
        best_matched = max(best_matched, matched)
        # If we matched most windows, stop waiting
        if matched >= len(saved_windows) * 0.8:
            break
        # After first attempt, use shorter intervals
        wait_seconds = 5

    return best_matched, len(saved_windows)
