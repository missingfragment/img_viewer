class Strings:
    def __init__(self, language="en-us") -> None:
        if language == "en-us":
            self.init_english()

    def init_english(self):
        self.file = "File"
        self.open_image = "Open Image..."
        self.open_folder = "Open Folder..."
        self.welcome_prompt = "Open an image or directory for viewing."
        self.exit = "Exit"
        self.close = "Close Window"
        self.close_all = "Close All Windows"
        self.loading = "Loading..."
        self.preferences = "Preferences..."

        self.apply = "Apply"
        self.cancel = "Cancel"

        self.view = "View"
        self.fullscreen = "Fullscreen"
        self.exit_fullscreen = "Exit Fullscreen"
        self.hide_menubar = "Hide Menubar"

        self.error_messages = {}
        self.error_messages["image_expected"] = '''Please select an image file.
        (Use the "Open Directory" command to browse a directory)'''
        self.error_messages["folder_expected"] = '''
        Please select a directory.
        (Use the "Open Image" command to open a single image.)
        '''

        self.next = "Next"
        self.previous = "Previous"
