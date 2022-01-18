from tkinter import *
from tkinter import ttk
import sys


class ViewPort(Canvas):
    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, **kwargs)

        self.mainframe = ttk.Frame(self, padding=5)
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        self.parent = parent
        self.scrollbar = None

        self.create_window(
            0, 0, window=self.mainframe, anchor=NW, tags="main"
        )

        self.scroll_active = True

        self.mainframe.bind("<Configure>", self.on_frame_configure)
        self.mainframe.bind("<Enter>", self.on_enter)
        self.mainframe.bind("<Leave>", self.on_leave)

        self.items = []

    def on_enter(self, event):
        self.scroll_active = True

    def on_leave(self, event):
        self.scroll_active = False

    def on_mousewheel(self, event):
        if not self.scroll_active:
            return
        if not self.parent.focus_displayof():
            return

        x, y = (self.winfo_pointerx(),
                self.winfo_pointery())

        first, last = self.scrollbar.get()
        if first <= 0 and last >= 1:
            return "break"

        if sys.platform.startswith("win32"):
            scroll_amount = round((-event.delta / 120) * 2)
        elif sys.platform.startswith("darwin"):
            scroll_amount = -event.delta

        if self.winfo_containing(x, y) != self.scrollbar:
            self.yview_scroll(scroll_amount, "units")

    def on_frame_configure(self, event):
        self.configure(scrollregion=self.bbox("all"))

    def clear(self):
        widget: Widget
        for widget in self.mainframe.winfo_children():
            widget.destroy()
