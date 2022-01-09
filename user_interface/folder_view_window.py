from tkinter import *
from tkinter import ttk
from pathlib import Path

from PIL import Image, ImageTk

from user_interface.default_window import DefaultWindow
from user_interface.viewport import ViewPort


class FolderViewWindow(DefaultWindow):
    def __init__(self, root, path: Path, **kwargs):
        super().__init__(root, **kwargs)

        self.viewport = ViewPort(self)

        self.path = path

        self.viewport.grid(column=0, row=0, sticky=NSEW)

        self.scrollbar = self.setup_scrollbar()

        self.scrollbar.grid(column=1, row=0, sticky=NSEW)

        self.images = []
        self.icons = []

        self.update_folder(path)

    def setup_scrollbar(self) -> Scrollbar:
        scrollbar = ttk.Scrollbar(
            self, orient=VERTICAL, command=self.viewport.yview)

        self.viewport.configure(yscrollcommand=scrollbar.set)

        return scrollbar

    def update_folder(self, folder: Path) -> None:
        thumb_size = (200, 200)

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

        max_width = self.winfo_width()
        col_count = max_width // thumb_size[0]

        if col_count <= 0:
            col_count = 1

        row: int = 0
        col: int = 0
        i: int = 0
        for image in self.images:
            photoimage = ImageTk.PhotoImage(image=image)
            self.icons.append(ttk.Label(
                self.viewport.mainframe,
                image=photoimage,
                anchor=NW
            ))

            label = self.icons[i]

            label.image = photoimage

            label.grid(column=col, row=row, sticky=NSEW)

            print(f"{col}, {row}")

            i += 1

            col += 1

            if col > col_count:
                col = 0
                row += 1
