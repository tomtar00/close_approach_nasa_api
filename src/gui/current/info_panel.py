from tkinter import *
from util import api_utils as au


class InfoPanel:

    def __init__(self, root, bg_color):
        self.frame = Frame(root, bg=bg_color, borderwidth=10)
        self.frame.pack(expand=True, fill=BOTH)

        # To create a label, which text may be changed we need to create StringVar object
        self.text = StringVar()
        self.text.set("Select close approach body")

        label = Label(self.frame, textvariable=self.text,
                      background=bg_color, foreground='white')
        label.place(relx=0.5, rely=0.5, anchor=CENTER)
        label.pack()

    def supply_body_info(self, body_data):
        self.text.set(
            f"Name: {body_data[0]}\nClosest approach: {body_data[3]}")
        print(au.format_json(body_data))
