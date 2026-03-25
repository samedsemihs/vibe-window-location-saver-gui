import win32api
import win32con


def get_monitors():
    """Enumerate all monitors and return their info matching the JSON schema."""
    monitors = []
    for hmon, hdc, rect in win32api.EnumDisplayMonitors(None, None):
        info = win32api.GetMonitorInfo(hmon)
        device = info["Device"]
        monitor_rect = list(info["Monitor"])  # (left, top, right, bottom)
        work_area = list(info["Work"])

        width = monitor_rect[2] - monitor_rect[0]
        height = monitor_rect[3] - monitor_rect[1]
        orientation = "portrait" if height > width else "landscape"
        is_primary = bool(info["Flags"] & win32con.MONITORINFOF_PRIMARY)

        monitors.append({
            "device_name": device,
            "rect": monitor_rect,
            "work_area": work_area,
            "is_primary": is_primary,
            "orientation": orientation,
            "width": width,
            "height": height,
        })

    # Sort so primary monitor comes first
    monitors.sort(key=lambda m: (not m["is_primary"], m["rect"][0]))
    return monitors


def find_monitor_index(monitors, rect):
    """Find which monitor a window rect belongs to based on overlap area."""
    wx, wy, wr, wb = rect
    best_idx = 0
    best_area = 0

    for i, mon in enumerate(monitors):
        mx, my, mr, mb = mon["rect"]
        # Calculate overlap
        ox = max(0, min(wr, mr) - max(wx, mx))
        oy = max(0, min(wb, mb) - max(wy, my))
        area = ox * oy
        if area > best_area:
            best_area = area
            best_idx = i

    return best_idx
