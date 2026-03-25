# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Screen Location Saver is a Windows desktop application that captures and restores window positions and monitor layouts. It runs as a system tray icon and can automatically restore saved layouts on system startup.

**Tech Stack:** Python 3.14, Tkinter (GUI), pywin32 (Windows API), pystray (system tray), PyInstaller (packaging)

**Platform:** Windows-only (uses Win32 API extensively)

## Build and Run Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run directly (development)
python main.py

# Run in startup mode (minimized to tray, auto-restores "default" layout)
python main.py --startup

# Build standalone .exe (outputs to dist/)
build.bat

# Install to %LOCALAPPDATA%\ScreenLocSaver (includes Start Menu shortcut + startup registry)
install.bat

# Uninstall (removes app, optionally keeps layouts)
uninstall.bat
```

**Install Location:** `%LOCALAPPDATA%\ScreenLocSaver\`
- Language selection during install (Turkish/English)
- Upgrades preserve existing user layouts and language preference
- Uninstall asks whether to keep layout files

## Architecture

### Core Modules

- **main.py** - Entry point. Sets DPI awareness before GUI initialization, handles `--startup` flag for auto-restore mode
- **app.py** - Tkinter GUI with layout management (save/restore/delete)
- **localization.py** - Bilingual support (Turkish/English). Use `t("key")` for translated strings
- **config.py** - User preferences storage (language setting in `config.json`)
- **window_manager.py** - Win32 API window capture/restore logic:
  - `capture_layout()` - Enumerates windows, captures positions, exe paths, window classes
  - `restore_layout(data)` - Matches windows by exe_path + window_class, applies saved placements
  - `launch_and_restore(data)` - Launches saved apps, waits for windows to appear, then restores (used on startup)
- **monitor_manager.py** - Multi-monitor detection, determines which monitor each window belongs to
- **layout_storage.py** - JSON persistence in `layouts/` directory
- **tray_icon.py** - System tray icon using pystray (runs in daemon thread)
- **feedback.py** - Toast notification UI with fade-out animation
- **constants.py** - Configuration: window class blacklist, min window dimensions, paths

### Key Implementation Details

**Window Matching:** Windows are matched by `exe_path` + `window_class` primarily, with fallback to `window_class` only. This allows multiple windows from the same app to be positioned correctly.

**Window Filtering:** Captures only visible, non-cloaked windows that aren't system windows (taskbar, desktop, etc.). Uses `WINDOW_CLASS_BLACKLIST` in constants.py.

**DPI Awareness:** Must be set before any GUI/win32 calls. Uses per-monitor DPI aware v2 with fallback for older Windows.

**Auto-Restore on Startup:** Loads "default" layout, launches missing apps via subprocess, polls every 5s for up to 60s until 80% of windows appear, then restores positions.

**Localization:** All UI strings go in `localization.py` STRINGS dict. Use `t("key")` or `t("key", name=value)` for formatted strings. Add both `tr` and `en` entries for new strings.

### Data Format

Layouts are stored as JSON in `layouts/` directory (relative to exe or source). When installed: `%LOCALAPPDATA%\ScreenLocSaver\layouts\`

Layout structure:
```json
{
  "timestamp": "ISO datetime",
  "monitors": [{"device_name": "...", "rect": [...], "is_primary": bool}],
  "windows": [{
    "title": "...",
    "exe_path": "...",
    "command_line": "...",
    "window_class": "...",
    "placement": {"show_cmd": int, "normal_position": [...], ...},
    "rect": [x, y, w, h],
    "monitor_index": int
  }]
}
```

Config file (`config.json`):
```json
{"language": "tr"}
```

## Dependencies

- `pywin32` - Windows API bindings (window/monitor enumeration, registry)
- `pystray` - System tray integration
- `Pillow` - Icon generation
- `psutil` - Process info (exe paths across processes)
