from tkinter import *
from tkinter import ttk
from turtle import width
from sklearn import datasets
import pandas as pd
from pandastable import Table


class DataframeView():
    def __init__(self, root, bg_color) -> None:
        self.frame = Frame(root, bg=bg_color, borderwidth=10)
        self.frame.pack(expand=True, fill=BOTH)

        wine_df = pd.DataFrame(datasets.load_iris().data)
        wine_df.columns = datasets.load_iris().feature_names

        # pt = Table(self.frame, dataframe=wine_data)
        # pt.show()

        self.frame.columnconfigure((0,1), weight=1)
        self.frame.rowconfigure(0, weight=1)
        
        style = ttk.Style(self.frame)
        style.configure('Treeview', background=bg_color,
                        foreground='white', fieldbackground=bg_color, borderwidth=0)
        
        
        tree = self.dataframe_to_treeview(self.frame, wine_df)
        tree.grid(row=0, column=0, columnspan=2, sticky=(N,E,W,S))

        scrollbarX = ttk.Scrollbar(self.frame, orient=HORIZONTAL, command=tree.xview)
        tree.configure(xscroll=scrollbarX.set)
        scrollbarX.grid(row=1, column=0, columnspan=2, sticky=(S,E,W))

        scrollbarY = ttk.Scrollbar(self.frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbarY.set)
        scrollbarY.grid(row=0, column=1, sticky=(E,N,S))
        

    def dataframe_to_treeview(self, root, df):
        tree = ttk.Treeview(root, columns=list(
            df.columns), show='headings')
        for column_name in df.columns:
            tree.heading(column_name, text=column_name)
            tree.column(column_name, minwidth=70, width=100, stretch=NO)
        df_rows = df.to_numpy().tolist()
        for row in df_rows:
            tree.insert('', END, values=row)
        return tree
