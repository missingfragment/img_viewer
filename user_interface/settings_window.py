from tkinter import *
from tkinter import font as tkFont
from tkinter import ttk
from tkinter import messagebox
from configparser import ConfigParser
from typing import Dict
from user_interface.default_window import DefaultWindow
from user_interface.viewport import ViewPort
from user_interface.menubars.settings_menubar import SettingsMenubar


class SettingsWindow(DefaultWindow):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)

        self.title("Settings")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.config: ConfigParser = self.app.config

        self.config_vars = {}

        self.header_font = tkFont.Font(
            family="Segoe UI",
            size=12,
            weight="bold"
        )
        self.option_font = tkFont.Font(
            family="Courier New",
            size=10
        )

        style = ttk.Style()
        style.configure("Header.TLabel", font=self.header_font)
        style.configure("Option.Tlabel", font=self.option_font)

        self.viewport = ViewPort(self, borderwidth=0, bd=0)

        self.button_frame = ttk.Frame(self, padding=5)

        self.mainframe = self.setup_layout()

        self.scrollbar = ttk.Scrollbar(
            self,
            orient=VERTICAL,
            command=self.viewport.yview,
        )

        self.viewport.configure(yscrollcommand=self.scrollbar.set)
        self.viewport.scrollbar = self.scrollbar

        self.viewport.grid(column=0, row=0, sticky=NSEW)
        self.button_frame.grid(column=0, row=1, sticky=E)
        self.scrollbar.grid(column=1, row=0, sticky=NSEW)

        self.bindings = {}
        self.bindings["destroy"] = self.bind("<Destroy>", self.on_destroy)

        self.menubar = SettingsMenubar(self)
        self['menu'] = self.menubar

    def setup_layout(self) -> Widget:
        strings = self.app.strings
        mainframe = self.viewport.mainframe

        self.labels = {}
        self.controls = {}
        self.buttons = {}

        rows: int = 0

        section: dict
        for section in self.config.sections():
            self.labels[section] = ttk.Label(
                mainframe,
                text=section,
                style="Header.TLabel"
            )
            self.labels[section].grid(column=0, row=rows, stick=W)
            rows += 1
            for option in self.config.options(section):
                self.labels[f"{section}-{option}"] = ttk.Label(
                    mainframe,
                    text=option,
                    style="Option.TLabel"
                ).grid(column=0, row=rows, ipadx=5)

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
                    v.set(self.config.get(section, option))
                    self.config_vars[option] = v
                    self.controls[f"{section}-{option}"] = ttk.Entry(
                        mainframe, textvariable=v
                    ).grid(column=1, row=rows)

            rows += 1

        apply_button = ttk.Button(
            self.button_frame,
            text=strings.apply,
            command=self.apply
        ).grid(column=0, row=0)
        cancel_button = ttk.Button(
            self.button_frame,
            text=strings.cancel,
            command=self.cancel
        ).grid(column=1, row=0)

        self.buttons["apply"] = apply_button
        self.buttons["cancel"] = cancel_button

        return mainframe

    def apply(self):
        for section in self.config.sections():
            for option in self.config.options(section):
                self.config.set(section, option, str(
                    self.config_vars[option].get()))

        self.app.save_config()

        messagebox.showinfo("Settings", "Settings updated.")

    def save_close(self):
        self.apply()
        self.cancel(ask=False)

    def cancel(self, ask=True):
        if ask:
            confirm = messagebox.askokcancel(
                "Settings",
                "Unsaved changes will be lost.  Exit settings?"
            )
        else:
            confirm = True

        if confirm:
            self.destroy()

    def on_destroy(self, *args):
        try:
            del self.bindings
        except AttributeError:
            pass

        self.destroy()
        return "break"
