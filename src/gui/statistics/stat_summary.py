from tkinter import *
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt

class StatSummary():
    def __init__(self, root, bg_color, query) -> None:
        self.frame = Frame(root, bg=bg_color, borderwidth=10)
        self.frame.pack(expand=True, fill=BOTH)
        self.query = query

        l = Label(self.frame, text='Summary', bg=bg_color, fg='white')
        l.pack()

        Button(self.frame, text='Hexbin', command=self.hexbin).pack()
    
    def hexbin(self):
        self.query.df.plot.hexbin(x="orbit_id", y="h", gridsize=25, cmap="coolwarm")
        plt.show()