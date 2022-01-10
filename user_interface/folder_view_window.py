from tkinter import *
from tkinter import ttk
from pathlib import Path

from PIL import Image, ImageTk

from user_interface.default_window import DefaultWindow
from user_interface.viewport import ViewPort


class FolderViewWindow(DefaultWindow):
    def __init__(self, root, path: Path, **kwargs):
        super().__init__(root, **kwargs)

        self.title(f"{path}")

        self.viewport = ViewPort(self)

        self.path = path

        self.viewport.grid(column=0, row=0, sticky=NSEW)

        self.scrollbar = self.setup_scrollbar()

        self.scrollbar.grid(column=1, row=0, sticky=NSEW)

        self.thumb_size = (200, 200)

        self.images = []
        self.icons = []

        self.view_size = (0, 0)

        # self.fill_placeholders(path)

        self.update_folder(path)

        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        new_size = (event.width, event.height)
        if new_size == self.view_size or new_size[0] < self.thumb_size[0] or new_size[1] < self.thumb_size[1]:
            return

        self.update_layout()

    def setup_scrollbar(self) -> Scrollbar:
        scrollbar = ttk.Scrollbar(
            self, orient=VERTICAL, command=self.viewport.yview)

        self.viewport.configure(yscrollcommand=scrollbar.set)

        return scrollbar

    def fill_placeholders(self, folder: Path) -> None:
        count = len([file for file in folder.glob("*.*") if file.is_file()])

        for i in range(0, count):
            im = Image.new(mode="RGB", size=self.thumb_size, color="#222")
            placeholder = ImageTk.PhotoImage(im)
            self.icons.append(ttk.Label(
                self.viewport.mainframe,
                image=placeholder,
                anchor=NW,
            ))

            self.icons[i].image = placeholder

    def update_folder(self, folder: Path) -> None:
        thumb_size = self.thumb_size

        self.images: Image = []
        self.icons = []

        self.viewport.clear()

        assert folder.is_dir()

        for file in folder.glob("*.*"):
            try:
                image: Image = Image.open(file)
            except OSError:
                continue

            thumbnail = image.copy()
            thumbnail.thumbnail(size=thumb_size)
            self.images.append(thumbnail)

        i: int = 0
        for image in self.images:
            photoimage = ImageTk.PhotoImage(image=image)
            self.icons.append(ttk.Label(
                self.viewport.mainframe,
                image=photoimage,
                anchor=NW
            ))

            label = self.icons[i]
            i += 1

            label.image = photoimage

    def update_layout(self) -> None:
        max_width = self.winfo_width()
        col_count = max_width // self.thumb_size[0]

        if col_count <= 0:
            col_count = 1

        row: int = 0
        col: int = 0
        for label in self.icons:

            label.grid(column=col, row=row, sticky=NSEW)

            col += 1

            if col >= col_count:
                col = 0
                row += 1
