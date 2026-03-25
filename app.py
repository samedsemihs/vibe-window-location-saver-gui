import tkinter as tk
from tkinter import ttk, messagebox

from feedback import SaveFeedback
from layout_storage import list_layouts, save_layout, load_layout, delete_layout
from window_manager import capture_layout, restore_layout
from localization import t


class App:
    def __init__(self, root, on_quit=None):
        self.root = root
        self.on_quit = on_quit
        self.feedback = SaveFeedback()

        root.title(t("app_title"))
        root.geometry("450x420")
        root.minsize(400, 400)

        self._build_ui()
        self._refresh_list()

    def _build_ui(self):
        frame = ttk.Frame(self.root, padding=12)
        frame.pack(fill=tk.BOTH, expand=True)

        # Layout list
        ttk.Label(frame, text=t("saved_layouts")).pack(anchor=tk.W)
        self.listbox = tk.Listbox(frame, height=8, font=("Segoe UI", 10))
        self.listbox.pack(fill=tk.BOTH, expand=True, pady=(4, 8))
        self.listbox.bind("<<ListboxSelect>>", self._on_select)

        # Name entry
        name_frame = ttk.Frame(frame)
        name_frame.pack(fill=tk.X, pady=(0, 8))
        ttk.Label(name_frame, text=t("layout_name")).pack(side=tk.LEFT)
        self.name_var = tk.StringVar(value="default")
        self.name_entry = ttk.Entry(name_frame, textvariable=self.name_var)
        self.name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 0))

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=(8, 0))

        style = ttk.Style()
        style.configure("Action.TButton", padding=(12, 6))

        self.save_btn = ttk.Button(btn_frame, text=t("btn_save"), style="Action.TButton", command=self._on_save)
        self.save_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 4))

        self.restore_btn = ttk.Button(btn_frame, text=t("btn_restore"), style="Action.TButton", command=self._on_restore)
        self.restore_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(4, 4))

        self.delete_btn = ttk.Button(btn_frame, text=t("btn_delete"), style="Action.TButton", command=self._on_delete)
        self.delete_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(4, 0))

    def _refresh_list(self):
        self.listbox.delete(0, tk.END)
        for name in list_layouts():
            self.listbox.insert(tk.END, name)

    def _on_select(self, event):
        sel = self.listbox.curselection()
        if sel:
            self.name_var.set(self.listbox.get(sel[0]))

    def _on_save(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning(t("warning"), t("name_empty"))
            return

        data = capture_layout()
        save_layout(name, data)
        self._refresh_list()
        self.feedback.show(self.root)

    def _on_restore(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning(t("warning"), t("select_layout"))
            return
        try:
            data = load_layout(name)
        except FileNotFoundError:
            messagebox.showerror(t("error"), t("layout_not_found", name=name))
            return
        matched, total = restore_layout(data)
        messagebox.showinfo(t("restore_title"), t("restore_result", matched=matched, total=total))

    def _on_delete(self):
        name = self.name_var.get().strip()
        if not name:
            return
        if messagebox.askyesno(t("delete_confirm_title"), t("delete_confirm", name=name)):
            delete_layout(name)
            self._refresh_list()
            self.name_var.set("")

    def show(self):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def hide(self):
        self.root.withdraw()
        # Ensure it's fully hidden from taskbar
        self.root.update()
