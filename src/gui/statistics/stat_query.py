from tkinter import *
from tkinter import ttk

class StatQuery():
    def __init__(self, root, bg_color) -> None:
        self.frame = Frame(root, bg=bg_color, borderwidth=10)
        self.frame.pack(expand=True, fill=BOTH)

        l = Label(self.frame, text='Query', bg=bg_color, fg='white')
        l.pack()