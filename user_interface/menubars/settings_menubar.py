from tkinter import *
from tkinter import ttk

from strings import Strings


class SettingsMenubar(Menu):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.parent = parent

        self.file_menu = self.setup_file_menu()

    def setup_file_menu(self) -> Menu:
        app = self.parent.app
        strings: Strings = app.strings
        file_menu = Menu(self)
        self.add_cascade(menu=file_menu, label=app.strings.file)

        file_menu.add_command(
            label=strings.apply,
            command=self.parent.apply
        )

        file_menu.add_separator()

        file_menu.add_command(
            label=strings.save_close,
            command=self.parent.save_close
        )

        file_menu.add_command(
            label=strings.discard_close,
            command=self.parent.cancel
        )

        return file_menu
