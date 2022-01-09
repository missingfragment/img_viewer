from tkinter import *
from tkinter import ttk

from user_interface.menubars.default_menubar import DefaultMenubar


class DefaultWindow(Toplevel):
    def __init__(self, root, app, **kwargs) -> None:
        super().__init__(root, **kwargs)

        self.app = app

        self.root = root

        self.minsize(400, 400)

        self.menubar = DefaultMenubar(self)
        self['menu'] = self.menubar

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
