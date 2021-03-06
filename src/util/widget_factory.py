from tkinter import *
from tkinter import ttk

def create_info_label(root, string_var, label_text, bg, r, label_width=30, _pady=0):
    string_var.set("")
    Label(root, text=label_text,
          background=bg, foreground='white', width=label_width, anchor=NW)\
        .grid(row=r, column=0, sticky=NW, pady=_pady)
    Label(root, textvariable=string_var,
          background=bg, foreground='white')\
        .grid(row=r, column=1, sticky=NW, pady=_pady)


def create_info_label_stretched(root, string_var, label_text, bg, r, _pady=0):
    string_var.set('---')
    Label(root, text=label_text,
          background=bg, foreground='white', anchor=W)\
        .grid(row=r, column=0, sticky=EW, pady=_pady)
    Label(root, textvariable=string_var,
          background=bg, foreground='white', anchor=E)\
        .grid(row=r, column=1, sticky=E, pady=_pady)


def create_info_button_stretched(root, btn_label_text, btn_func, label_text, bg, r, _pady=0):
    Label(root, text=label_text,
          background=bg, foreground='white', anchor=W)\
        .grid(row=r, column=0, sticky=EW, pady=_pady)
    Button(root, text=btn_label_text, command=btn_func, anchor=E)\
        .grid(row=r, column=1, sticky=E, pady=_pady)


def create_checkbox(root, var, label_text, bg, on_value, _anchor=W):
    Checkbutton(root, text=label_text, variable=var,
                width=20, anchor=_anchor, selectcolor=bg, background=bg, fg='white',
                activebackground=bg, activeforeground='white',
                onvalue=on_value, offvalue=-1)\
        .pack(fill=X)

def create_checkbox_grid(root, var, label_text, bg, on_value, r, _anchor=W, cspan=1, _pady=0):
    Checkbutton(root, text=label_text, variable=var,
                width=45, anchor=_anchor, selectcolor=bg, background=bg, fg='white',
                activebackground=bg, activeforeground='white',
                onvalue=on_value, offvalue=-1)\
        .grid(row=r, column=0, columnspan=cspan, sticky=_anchor, pady=_pady)


def create_info_label_combo(root, text_var, values, label_text, bg, r, combo_width=30):
    Label(root, text=label_text,
          background=bg, foreground='white', anchor=W)\
        .grid(row=r, column=0, sticky=W)
    ttk.Combobox(root, textvariable=text_var, values=values, width=combo_width-3, state="readonly")\
        .grid(row=r, column=1, sticky=W)

def create_info_label_entry(root, entry_var, label_text, bg, r, entry_width=30, _pady=0, _padx=0, entry_sticky=E):
    Label(root, text=label_text,
          background=bg, foreground='white', anchor=W)\
        .grid(row=r, column=0, sticky=W, pady=_pady, padx=_padx)
    Entry(root, width=entry_width, textvariable=entry_var)\
        .grid(row=r, column=1, sticky=entry_sticky, pady=_pady)