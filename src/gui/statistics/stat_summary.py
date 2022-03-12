from tkinter import *
from tkinter import ttk

class StatSummary():
    def __init__(self, root, bg_color) -> None:
        self.frame = Frame(root, bg=bg_color, borderwidth=10)
        self.frame.pack(expand=True, fill=BOTH)

        l = Label(self.frame, text='TEST', bg=bg_color, fg='white')
        l.pack()