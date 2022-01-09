from tkinter import *
from tkinter import ttk


class WelcomeWindow(Toplevel):
    def __init__(self, root):
        super().__init__(self)

        self.root = root

        self.minsize(400, 400)

        self.setup_layout()

    def setup_layout(self):
        self.mainframe = ttk.Frame(self, padding=5)

        self.mainframe.grid(row=0, column=0)
