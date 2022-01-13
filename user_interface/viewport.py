from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


class ViewPort(Canvas):
    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, **kwargs)

        self.mainframe = ttk.Frame(self, padding=5)
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self.configure(borderwidth=0)

        self.create_window(
            0, 0, window=self.mainframe, anchor=NW, tags="main"
        )

        self.mainframe.bind("<Configure>", self.on_frame_configure)

        self.items = []

    def on_frame_configure(self, event):
        self.configure(scrollregion=self.bbox("all"))

    def clear(self):
        widget: Widget
        for widget in self.mainframe.winfo_children():
            widget.destroy()
