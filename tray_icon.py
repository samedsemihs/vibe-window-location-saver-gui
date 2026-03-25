import threading

from PIL import Image, ImageDraw
import pystray

from localization import t


def _create_icon_image():
    """Create a simple grid icon programmatically."""
    img = Image.new("RGB", (64, 64), "#2196F3")
    draw = ImageDraw.Draw(img)
    # Draw a simple window grid pattern
    draw.rectangle([8, 8, 56, 56], outline="white", width=2)
    draw.line([32, 8, 32, 56], fill="white", width=2)
    draw.line([8, 32, 56, 32], fill="white", width=2)
    return img


class TrayIcon:
    def __init__(self, app):
        self.app = app
        self.icon = None

    def start(self):
        menu = pystray.Menu(
            pystray.MenuItem(t("tray_show"), self._on_show, default=True),
            pystray.MenuItem(t("tray_save"), self._on_save),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(t("tray_quit"), self._on_quit),
        )
        self.icon = pystray.Icon(
            "screen-loc-saver",
            _create_icon_image(),
            t("app_title"),
            menu,
        )
        thread = threading.Thread(target=self.icon.run, daemon=True)
        thread.start()

    def stop(self):
        if self.icon:
            self.icon.stop()

    def _on_show(self, icon, item):
        self.app.root.after(0, self.app.show)

    def _on_save(self, icon, item):
        self.app.root.after(0, self.app._on_save)

    def _on_quit(self, icon, item):
        self.icon.stop()
        self.app.root.after(0, self.app.root.destroy)
