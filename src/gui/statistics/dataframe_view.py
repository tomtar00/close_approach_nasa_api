from tkinter import *
from tkinter import ttk
from sklearn import datasets
import pandas as pd
#from pandastable import Table


class DataframeView():
    def __init__(self, root, bg_color, query) -> None:
        self.frame = Frame(root, bg=bg_color, borderwidth=10)
        self.frame.pack(expand=True, fill=BOTH)
        self.query = query

        self.frame.columnconfigure((0,1), weight=1)
        self.frame.rowconfigure(0, weight=1)
        
        style = ttk.Style(self.frame)
        style.configure('Treeview', background=bg_color,
                        foreground='white', fieldbackground=bg_color, borderwidth=0)
        
        self.tree = ttk.Treeview(self.frame, show='headings')
        self.tree.grid(row=0, column=0, columnspan=2, sticky=(N,E,W,S))

        scrollbarX = ttk.Scrollbar(self.frame, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscroll=scrollbarX.set)
        scrollbarX.grid(row=1, column=0, columnspan=2, sticky=(S,E,W))

        scrollbarY = ttk.Scrollbar(self.frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbarY.set)
        scrollbarY.grid(row=0, column=1, sticky=(E,N,S))
        

    def dataframe_to_treeview(self, df):
        self.tree.delete(*self.tree.get_children())
        self.tree['columns'] = list(df.columns)
        for column_name in df.columns:
            self.tree.heading(column_name, text=column_name)
            self.tree.column(column_name, width=150, stretch=YES, anchor=CENTER)
        df_rows = df.to_numpy().tolist()
        for row in df_rows:
            self.tree.insert('', END, values=row)
        return self.tree
