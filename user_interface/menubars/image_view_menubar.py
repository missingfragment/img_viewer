from tkinter import *
from tkinter import ttk


class ImageViewMenubar(Menu):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.parent = parent

        self.file_menu = self.setup_file_menu()
        self.view_menu = self.setup_view_menu()

    def setup_file_menu(self) -> Menu:
        app = self.parent.app

        file_menu = Menu(self)
        self.add_cascade(menu=file_menu, label=app.strings.file)

        file_menu.add_command(
            label=app.strings.open_image,
            command=app.open_image
        )
        file_menu.add_command(
            label=app.strings.open_folder, command=app.open_folder
        )

        file_menu.add_separator()

        file_menu.add_command(
            label=app.strings.close, command=self.parent.on_destroy
        )

        file_menu.add_command(
            label=app.strings.close_all, command=app.close_all_windows
        )

        return file_menu

    def setup_view_menu(self) -> Menu:
        app = self.parent.app

        view_menu = Menu(self)
        self.add_cascade(menu=view_menu, label=app.strings.view)

        view_menu.add_command(
            label=app.strings.fullscreen,
            command=self.parent.toggle_fullscreen
        )

        return view_menu
