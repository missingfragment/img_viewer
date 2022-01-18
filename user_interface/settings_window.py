from tkinter import *
from tkinter import ttk
from configparser import ConfigParser
from typing import Dict
from user_interface.default_window import DefaultWindow
from user_interface.viewport import ViewPort


class SettingsWindow(DefaultWindow):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)

        self.title("Settings")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.config: ConfigParser = self.app.config

        self.config_vars = {}

        self.viewport = ViewPort(self, borderwidth=0, bd=0)

        self.button_frame = ttk.Frame(self, padding=15)

        self.mainframe = self.setup_layout()

        self.scrollbar = ttk.Scrollbar(
            self,
            orient=VERTICAL,
            command=self.viewport.yview,
        )

        self.viewport.configure(yscrollcommand=self.scrollbar.set)
        self.viewport.scrollbar = self.scrollbar

        self.viewport.grid(column=0, row=0, sticky=NSEW)
        self.button_frame.grid(column=0, row=1, sticky=NSEW)
        self.scrollbar.grid(column=1, row=0, sticky=NSEW)

    def setup_layout(self) -> Widget:
        strings = self.app.strings
        mainframe = self.viewport.mainframe

        self.labels = {}
        self.controls = {}
        self.buttons = {}

        rows: int = 0

        section: dict
        for section in self.config.sections():
            self.labels[section] = ttk.Label(mainframe, text=section)
            for option in self.config.options(section):
                self.labels[f"{section}-{option}"] = ttk.Label(
                    mainframe, text=option
                ).grid(column=0, row=rows)

                bool_value: bool = None

                try:
                    bool_value = self.config.getboolean(section, option)
                except ValueError:
                    pass

                if bool_value:
                    b = BooleanVar()
                    self.config_vars[option] = b
                    self.controls[f"{section}-{option}"] = ttk.Checkbutton(
                        mainframe, variable=b
                    ).grid(column=1, row=rows)
                else:
                    v = StringVar()
                    self.config_vars[option] = v
                    self.controls[f"{section}-{option}"] = ttk.Entry(
                        mainframe
                    ).grid(column=1, row=rows)

            rows += 1

        apply_button = ttk.Button(
            self.button_frame,
            text=strings.apply
        ).grid(column=0, row=0)
        cancel_button = ttk.Button(
            self.button_frame,
            text=strings.cancel
        ).grid(column=1, row=0)

        self.buttons["apply"] = apply_button
        self.buttons["cancel"] = cancel_button

        return mainframe
