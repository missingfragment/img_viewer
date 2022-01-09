from tkinter import *
from tkinter import ttk
from pathlib import Path

from PIL import Image, ImageTk

from user_interface.default_window import DefaultWindow
from user_interface.menubars.image_view_menubar import ImageViewMenubar


class ImageViewWindow(DefaultWindow):
    def __init__(self, root, path: Path, **kwargs):
        super().__init__(root, **kwargs)

        self.title(f"{path}")

        self.fullscreen = False

        self.mainframe = ttk.Frame(self, padding=10)
        self.mainframe.grid(column=0, row=0, sticky=NSEW)
        self.mainframe.bind("<Configure>", self.on_resize)

        self.image_size = (0, 0)

        try:
            self.image = Image.open(path)
        except OSError:
            print("Failed to open image.")

        self.photoimage = ImageTk.PhotoImage(self.image)

        self.image_label = ttk.Label(
            self.mainframe, image=self.photoimage)

        self.image_label.place(relx=.5, rely=.5, anchor=CENTER)

        self.menubar = ImageViewMenubar(self)
        self['menu'] = self.menubar

    def on_resize(self, event):
        new_size = (event.width, event.height)
        if new_size == self.image_size or new_size[0] < 20 or new_size[1] < 20:
            return
        new_image = self.image.copy()
        new_image.thumbnail(new_size)
        self.photoimage = ImageTk.PhotoImage(new_image)

        self.image_size = new_size

        self.update_image()

    def update_image(self):
        self.image_label['image'] = self.photoimage

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen

        self.attributes("-fullscreen", 1 if self.fullscreen else 0)

        strings = self.app.strings
        new_text = strings.exit_fullscreen if self.fullscreen else strings.fullscreen

        self.menubar.view_menu.entryconfigure(0, label=new_text)
