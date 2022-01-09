from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from strings import Strings
from pathlib import Path
from user_interface.folder_view_window import FolderViewWindow
from user_interface.image_view_window import ImageViewWindow

from user_interface.welcome_window import WelcomeWindow


class Application():
    def __init__(self, root) -> None:
        self.strings = Strings()
        self.root = root

        self.filetypes = [
            ("Common Formats", ".png .jpg .jpeg .gif .bmp"),
            ("PNG Images", ".png"),
            ("JPEG Images", ".jpg .jpeg .jfif"),
            ("JPEG 2000 Images", ".j2k .jpx"),
            ("GIF Images", ".gif"),
            ("TIFF Images", ".tiff"),
            ("Bitmap Images", ".bmp"),
            ("Icon Files", ".ico"),
            ("All Files", ".*"),
        ]

        self.windows = {}

    def open_image(self):
        file = filedialog.askopenfilename(filetypes=self.filetypes)
        if not file:
            return

        file = Path(file)

        if file.is_dir():
            messagebox.showwarning(
                self.strings.error_messages["image_expected"]
            )
            return

        self.windows[file] = ImageViewWindow(
            self.root, file.resolve(), app=self)
        self.windows["welcome"].iconify()

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

        self.windows["welcome"].iconify()


root = Tk()

app = Application(root)

root.option_add('*tearOff', FALSE)
root.withdraw()

welcome_window = WelcomeWindow(root, app=app)

app.windows["welcome"] = welcome_window

root.mainloop()
