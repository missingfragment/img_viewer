from configparser import ConfigParser
from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont
from pathlib import Path

from PIL import Image, ImageTk
from strings import Strings

from user_interface.default_window import DefaultWindow
from user_interface.viewport import ViewPort


class FolderViewWindow(DefaultWindow):
    def __init__(self, root, path: Path, **kwargs):
        super().__init__(root, **kwargs)

        self.title(f"{path}")

        self.viewport = ViewPort(self, borderwidth=0)

        self.path = path
        self.files = []

        config: ConfigParser = self.app.config
        self.batch_count = config.getint("FolderView", "folder batch count")

        self.page = 0
        self.max_pages = 0

        self.thumb_size = (200, 200)

        self.viewport.grid(column=0, row=0, sticky=NSEW)

        self.scrollbar = self.setup_scrollbar()

        self.scrollbar.grid(column=1, row=0, sticky=NSEW)

        self.viewport.scrollbar = self.scrollbar

        self.navigation_panel = self.setup_navigation_panel()
        self.navigation_panel.grid(column=0, row=1, sticky=NSEW)

        self.loading_font = tkFont.Font(size=24)

        self.style = ttk.Style()
        self.style.configure("Loading.TLabel", font=self.loading_font)
        self.style.configure("Img.TButton", highlightthickness=0, bd=0)

        self.loading_panel = ttk.Frame(self)
        self.loading_text = ttk.Label(
            self.loading_panel, text=self.app.strings.loading,
            justify="center",
            style="Loading.TLabel",
            anchor=CENTER
        ).place(relx=.5, rely=.5, anchor=CENTER)

        self.loading_panel.grid(column=0, row=0, sticky=NSEW)

        self.images = []
        self.icons = []

        self.view_size = (0, 0)

        self.bind("<Configure>", self.on_resize)
        self.update_idletasks()

        self.after(1, self.update_folder, path)

    def on_resize(self, event):
        new_size = (event.width, event.height)
        if new_size == self.view_size or new_size[0] < self.thumb_size[0] or new_size[1] < self.thumb_size[1]:
            return

        self.update_layout()

    def setup_navigation_panel(self) -> Widget:
        strings: Strings = self.app.strings
        nav_panel = ttk.Frame(self, padding=5)

        self.back_button = ttk.Button(
            nav_panel,
            text=strings.previous,
            command=self.prev_page
        )
        self.next_button = ttk.Button(
            nav_panel,
            text=strings.next,
            command=self.next_page
        )

        self.page_label = ttk.Label(
            nav_panel,
            text="",
        )

        self.back_button.grid(column=0, row=0, sticky=W)
        self.page_label.grid(column=1, row=0, sticky=NSEW)
        self.next_button.grid(column=2, row=0, sticky=E)

        nav_panel.columnconfigure(0, weight=1)
        nav_panel.columnconfigure(2, weight=1)

        return nav_panel

    def setup_scrollbar(self) -> Scrollbar:
        scrollbar = ttk.Scrollbar(
            self, orient=VERTICAL, command=self.viewport.yview)

        self.viewport.configure(yscrollcommand=scrollbar.set)

        return scrollbar

    def update_folder(self, folder: Path, offset=0) -> None:
        self.page = 0

        assert folder.is_dir()

        self.path = folder
        all_files = folder.glob("*.*")

        all_files = [str(file) for file in all_files]

        self.files = list(
            [
                Path(file)
                for file in all_files
                if self.app.has_valid_extention(file)
            ]
        )

        self.max_pages = len(self.files) // self.batch_count

        self.reload_page()

    def next_page(self):
        self.page += 1
        self.reload_page()

    def prev_page(self):
        self.page -= 1
        self.reload_page()

    def reload_page(self):
        files_to_load = self.get_page(self.page)

        self.viewport.grid_remove()
        self.loading_panel.grid()

        self.update_idletasks()

        def reload():

            self.update_images(files_to_load)
            self.update_layout()

            self.viewport.grid()
            self.loading_panel.grid_remove()

            self.back_button.configure(
                state="disabled" if self.page <= 0 else "normal"
            )
            self.next_button.configure(
                state="disabled" if self.page >= self.max_pages else "normal"
            )
            self.page_label.configure(
                text=f"{self.page+1}/{self.max_pages+1}"
            )

        self.after(1, reload)

    def get_page(self, index: int):
        page_number = index
        page_size = self.batch_count

        files = self.files

        offset = page_number * page_size
        endpoint = min(offset + page_size, len(self.files))

        return files[offset:endpoint]

    def update_images(self, files: list[Path]):
        self.images: Image = []
        self.icons = []

        self.viewport.clear()

        self.file_dict = {}

        thumb_size = self.thumb_size
        batch_count = self.batch_count

        for file in files:
            try:
                image: Image = Image.open(file)
            except OSError:
                continue

            thumbnail = image.copy()
            thumbnail.thumbnail(size=thumb_size)
            self.images.append(thumbnail)

            self.file_dict[file] = thumbnail

            if len(self.images) >= batch_count:
                break

        i: int = 0
        for file in self.file_dict.keys():
            image = self.file_dict[file]
            photoimage = ImageTk.PhotoImage(image=image)
            self.icons.append(Button(
                self.viewport.mainframe,
                image=photoimage,
                command=lambda f=file: self.app.open_image(f),
                borderwidth=0,
                cursor="hand2"
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
        label: Widget
        for label in self.icons:

            label.grid(column=col, row=row, sticky=NSEW)

            col += 1

            if col >= col_count:
                col = 0
                row += 1
