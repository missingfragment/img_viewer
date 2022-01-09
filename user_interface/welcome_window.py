from tkinter import *
from tkinter import ttk

from user_interface.default_window import DefaultWindow


class WelcomeWindow(DefaultWindow):
    def __init__(self, root, **kwargs) -> None:
        super().__init__(root, **kwargs)

        self.mainframe = self.setup_layout()

    def setup_layout(self) -> ttk.Frame:
        strings = self.app.strings
        mainframe = ttk.Frame(self, padding=15)

        welcome_label = ttk.Label(
            mainframe, text=strings.welcome_prompt, anchor=CENTER)
        button_frame = ttk.Frame(mainframe, padding=0)
        open_image_button = ttk.Button(
            button_frame, text=strings.open_image, command=self.app.open_image
        )
        open_folder_button = ttk.Button(
            button_frame, text=strings.open_folder, command=self.app.open_folder
        )

        mainframe.grid(row=0, column=0, sticky=(N, S, E, W))
        #mainframe.rowconfigure(0, weight=1)
        mainframe.columnconfigure(0, weight=1)

        # Main Layout
        welcome_label.grid(row=0, column=0, sticky=(E, W))
        button_frame.grid(row=1, column=0, sticky=(E, W))
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        # Button Frame
        open_image_button.grid(row=0, column=0, sticky=E)
        open_folder_button.grid(row=0, column=1, sticky=W)

        return mainframe
