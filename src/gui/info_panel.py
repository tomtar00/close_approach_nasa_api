from tkinter import *
from gui import main_window
from util import api_utils as au

class InfoPanel:
    def __init__(self, root, bg_color):
        bg_frame = Frame(root, bg=main_window.bg_color, borderwidth=10)
        bg_frame.place(relwidth=.7, relheight=.8, relx=.3, rely=.2)
        self.frame = Frame(bg_frame, bg=bg_color, borderwidth=10)
        self.frame.place(relwidth=1, relheight=1)

        # To create a label, which text may be changed we need to create StringVar object
        self.text = StringVar()
        self.text.set("Test")

        label = Label(self.frame, textvariable=self.text, background=bg_color, foreground='white')
        label.place(relx=0.5, rely=0.5, anchor=CENTER)

    def supply_body_info(self, body_data):
        self.text.set(f"Name: {body_data[0]}\nClosest approach: {body_data[3]}")
        print(au.format_json(body_data))