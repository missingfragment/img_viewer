from tkinter import *
from tkinter import ttk
from pathlib import Path

from PIL import Image, ImageTk

from user_interface.default_window import DefaultWindow


class ImageViewWindow(DefaultWindow):
    def __init__(self, root, path: Path, **kwargs):
        super().__init__(root, **kwargs)

        self.title(f"{path}")

        self.mainframe = ttk.Frame(self, padding=10)
        self.mainframe.grid(column=0, row=0, sticky=NSEW)

        label = ttk.Label(self.mainframe, text=f"{path}")
        label.grid(column=0, row=1, sticky=NSEW)

        try:
            self.image = Image.open(path)
        except OSError:
            print("Failed to open image.")
        self.photoimage = ImageTk.PhotoImage(self.image)

        self.image_label = ttk.Label(
            self.mainframe, image=self.photoimage)

        self.image_label.grid(column=0, row=0, sticky=NSEW)
