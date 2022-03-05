from tkinter import *

class InfoPanel:
    def __init__(self, root, bg_color):
        self.frame = Frame(root, bg=bg_color, borderwidth=10)
        self.frame.place(relwidth=.7, relheight=.8, relx=.3, rely=.2)

        # To create a label, which text may be changed we need to create this object
        self.text = StringVar()
        self.text.set("Test")

        label = Label(self.frame, textvariable=self.text, anchor=CENTER, background=bg_color, foreground='white')
        label.place(relx=0.5, rely=0.5, anchor=CENTER)
        #label.pack()


    def supply_body_info(self, body_data):
        self.text.set(f"Name: {body_data[0]}     Closest approach: {body_data[3]}")
        print(body_data)