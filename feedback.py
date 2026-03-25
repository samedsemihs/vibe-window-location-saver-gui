import tkinter as tk

from localization import t


class SaveFeedback:
    """Shows a floating toast notification when a layout is saved."""

    def __init__(self):
        self._overlay = None

    def show(self, parent):
        """Show a green checkmark toast centered over the parent window."""
        # Destroy existing overlay if any
        if self._overlay is not None:
            try:
                self._overlay.destroy()
            except tk.TclError:
                pass
            self._overlay = None

        overlay = tk.Toplevel(parent)
        overlay.overrideredirect(True)
        overlay.attributes("-topmost", True)
        overlay.attributes("-alpha", 1.0)
        overlay.configure(bg="#4CAF50")

        label = tk.Label(
            overlay,
            text=t("saved"),
            font=("Segoe UI", 16, "bold"),
            fg="white",
            bg="#4CAF50",
            padx=24,
            pady=12,
        )
        label.pack()

        # Center over parent
        overlay.update_idletasks()
        ow = overlay.winfo_reqwidth()
        oh = overlay.winfo_reqheight()
        px = parent.winfo_x() + (parent.winfo_width() - ow) // 2
        py = parent.winfo_y() + (parent.winfo_height() - oh) // 2
        overlay.geometry(f"+{px}+{py}")

        self._overlay = overlay

        # Start fade-out after 1.5 seconds
        parent.after(1500, lambda: self._fade_out(overlay, parent))

    def _fade_out(self, overlay, parent, alpha=1.0):
        if overlay != self._overlay:
            return
        if alpha <= 0:
            try:
                overlay.destroy()
            except tk.TclError:
                pass
            if self._overlay == overlay:
                self._overlay = None
            return
        try:
            overlay.attributes("-alpha", alpha)
        except tk.TclError:
            return
        parent.after(30, lambda: self._fade_out(overlay, parent, alpha - 0.05))
