from tkinter import *
from tkinter import ttk

class DataframeView():
    def __init__(self, root, bg_color, query) -> None:
        self.frame = Frame(root, bg=bg_color, borderwidth=10)
        self.frame.pack(expand=True, fill=BOTH) 

        self.loading_frame = Frame(self.frame, bg=bg_color)  
        self.loading_frame.pack(fill=X) 

        self.tree_frame = Frame(self.frame, bg=bg_color)
        self.tree_frame.pack(expand=True, fill=BOTH)

        self.query = query

        self.tree_frame.columnconfigure((0,1), weight=1)
        self.tree_frame.rowconfigure(0, weight=1)       

        self.alertText = StringVar()
        self.loading_label = Label(
            self.loading_frame, textvariable=self.alertText, bg=bg_color, fg='white')
        self.loading_label.pack_forget()

        style = ttk.Style(self.tree_frame)
        style.configure('Treeview', background=bg_color,
                        foreground='white', fieldbackground=bg_color, borderwidth=0)
        
        self.tree = ttk.Treeview(self.tree_frame, show='headings')
        self.tree.grid(row=0, column=0, columnspan=2, sticky=(N,E,W,S))

        scrollbarX = ttk.Scrollbar(self.tree_frame, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscroll=scrollbarX.set)
        scrollbarX.grid(row=1, column=0, columnspan=2, sticky=(S,E,W))

        scrollbarY = ttk.Scrollbar(self.tree_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbarY.set)
        scrollbarY.grid(row=0, column=1, sticky=(E,N,S))
        

    def dataframe_to_treeview(self, df):
        self.clear_treeview()
        self.tree['columns'] = list(df.columns)
        for column_name in df.columns:
            self.tree.heading(column_name, text=column_name)
            self.tree.column(column_name, width=150, stretch=NO, anchor=CENTER)
        df_rows = df.to_numpy().tolist()
        for row in df_rows:
            self.tree.insert('', END, values=row)

        self.loading_label.pack_forget()
        return self.tree

    def clear_treeview(self):
        self.tree.delete(*self.tree.get_children())

    def show_alert(self, text):
        self.loading_label.pack()
        self.alertText.set(text)

    def show_loading(self):
        self.show_alert('Loading...')

    def show_no_result(self):
        self.show_alert('No result')
