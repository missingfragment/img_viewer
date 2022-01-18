from tkinter import *
from tkinter import ttk


class DefaultMenubar(Menu):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.parent = parent

        self.file_menu = self.setup_file_menu()

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
            label=app.strings.preferences, command=app.open_settings
        )

        file_menu.add_separator()

        file_menu.add_command(
            label=app.strings.exit, command=app.exit
        )

        return file_menu
