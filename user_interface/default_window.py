from tkinter import *
from tkinter import ttk

from user_interface.menubars.default_menubar import DefaultMenubar


class DefaultWindow(Toplevel):
    def __init__(self, root, app, **kwargs) -> None:
        super().__init__(root, **kwargs)

        self.app = app

        self.root = root

        self.minsize(600, 400)
        self.geometry("800x600")

        self.menubar = DefaultMenubar(self)
        self['menu'] = self.menubar

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.protocol("WM_DELETE_WINDOW", self.on_destroy)

    def on_destroy(self):
        self.destroy()
        self.app.on_window_closed(self)
