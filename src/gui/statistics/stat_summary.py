from tkinter import *
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt

class StatSummary():
    def __init__(self, root, bg_color) -> None:
        self.frame = Frame(root, bg=bg_color, borderwidth=10)
        self.frame.pack(expand=True, fill=BOTH)

        l = Label(self.frame, text='Summary', bg=bg_color, fg='white')
        l.pack()

        Button(self.frame, text='Graph', command=self.graph).pack()
    
    def graph(self):
        data = np.random.normal(20000, 25000, 5000)
        plt.hist(data)
        plt.show()