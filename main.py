import ctypes
import sys
import tkinter as tk

# Set DPI awareness before any GUI/win32 calls
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)  # Per-monitor DPI aware v2
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

from config import get
from localization import set_language
from app import App
from tray_icon import TrayIcon
from layout_storage import load_layout
from window_manager import launch_and_restore
from constants import DEFAULT_LAYOUT_NAME


def main():
    # Load language preference
    lang = get("language", "tr")
    set_language(lang)

    startup_mode = "--startup" in sys.argv

    root = tk.Tk()

    app = App(root)
    tray = TrayIcon(app)
    tray.start()

    # Minimize to tray on close
    root.protocol("WM_DELETE_WINDOW", app.hide)

    if startup_mode:
        # Start hidden in tray, launch apps and restore layout
        app.hide()
        root.after(1000, _auto_restore, root)

    root.mainloop()
    tray.stop()


def _auto_restore(root):
    """Background auto-restore on startup."""
    import threading

    def do_restore():
        try:
            data = load_layout(DEFAULT_LAYOUT_NAME)
            launch_and_restore(data)
        except FileNotFoundError:
            pass

    thread = threading.Thread(target=do_restore, daemon=True)
    thread.start()


if __name__ == "__main__":
    main()
