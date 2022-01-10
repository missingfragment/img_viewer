from tkinter import *
from application import Application

from user_interface.welcome_window import WelcomeWindow

root = Tk()

app = Application(root)

root.option_add('*tearOff', FALSE)
root.withdraw()

welcome_window = WelcomeWindow(root, app=app)

app.windows["welcome"] = welcome_window

root.mainloop()
