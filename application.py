from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from strings import Strings
from pathlib import Path
from configparser import ConfigParser
from user_interface.folder_view_window import FolderViewWindow
from user_interface.image_view_window import ImageViewWindow


class Application():
    def __init__(self, root) -> None:
        self.strings = Strings()
        self.root = root

        self.filetypes = [
            ("Common Formats", ".png .jpg .jpeg .gif .bmp .webp"),
            ("PNG Images", ".png"),
            ("WebP Images", ".webp"),
            ("JPEG Images", ".jpg .jpeg .jfif"),
            ("JPEG 2000 Images", ".j2k .jpx"),
            ("GIF Images", ".gif"),
            ("TIFF Images", ".tiff"),
            ("Bitmap Images", ".bmp"),
            ("Icon Files", ".ico"),
            ("All Files", ".*"),
        ]
        self.file_extentions = [
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".bmp",
            ".jfif",
            ".webp",
            ".j2k",
            ".jpx",
            ".gif",
            ".tiff",
            ".bmp",
            ".ico",
        ]

        self.windows = {}

        self.init_config()

    def has_valid_extention(self, filename: str):
        return any(filename.lower().endswith(e) for e in self.file_extentions)

    def init_config(self):
        self.config = ConfigParser()

        config_path = Path("config.ini")

        self.config["FolderView"] = {}
        self.config["FolderView"]["folder batch count"] = "20"

        if config_path.is_file() and config_path.exists():
            self.config.read(config_path)
        else:
            config_path.touch()
            with open(config_path, 'w') as config_file:
                self.config.write(config_file)

    def open_image(self, file=None):
        if file is None:
            file = filedialog.askopenfilename(filetypes=self.filetypes)
            if not file:
                return

            file = Path(file)

            if file.is_dir():
                messagebox.showwarning(
                    self.strings.error_messages["image_expected"]
                )
                return

        if type(file) is str:
            file = Path(file)

        self.windows[file] = ImageViewWindow(
            self.root, file.resolve(), app=self)
        self.windows["welcome"].withdraw()

        win: ImageViewWindow = self.windows[file]
        win.lift()
        win.focus_force()

    def open_folder(self):
        folder = filedialog.askdirectory()

        if not folder:
            return

        folder = Path(folder)

        if not folder.is_dir():
            messagebox.showwarning(
                self.strings.error_messages["folder_expected"]
            )

        if not "folder" in self.windows.keys():
            self.windows["folder"] = FolderViewWindow(
                self.root, folder, app=self)
        else:
            win = self.windows["folder"]

            win.update_folder(folder)

        self.windows["welcome"].withdraw()

    def on_window_closed(self, window):
        window_key = None
        for key in self.windows.keys():
            if self.windows[key] != window:
                continue
            window_key = key

        if window_key != None:
            self.windows.pop(window_key)

        if len(self.windows.keys()) < 2:
            self.windows["welcome"].deiconify()

    def close_all_windows(self):
        keys_to_remove = []
        for key in self.windows.keys():
            if key == "welcome":
                continue
            self.windows[key].destroy()
            keys_to_remove.append(key)

        for key in keys_to_remove:
            self.windows.pop(key)

        self.windows["welcome"].deiconify()

    def exit(self):
        self.root.destroy()
