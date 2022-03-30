from tkinter import *


def create_info_label(root, string_var, label_text, bg, r, label_width=30):
    string_var.set("")
    Label(root, text=label_text,
          background=bg, foreground='white', width=label_width, anchor=NW)\
        .grid(row=r, column=0, sticky=NW)
    Label(root, textvariable=string_var,
          background=bg, foreground='white')\
        .grid(row=r, column=1, sticky=NW)


def create_info_label_stretched(root, string_var, label_text, bg, r):
    string_var.set('---')
    Label(root, text=label_text,
          background=bg, foreground='white', anchor=W)\
        .grid(row=r, column=0, sticky=EW)
    Label(root, textvariable=string_var,
          background=bg, foreground='white', anchor=E)\
        .grid(row=r, column=1, sticky=E)


def create_info_button_stretched(root, btn_label_text, btn_func, label_text, bg, r):
    Label(root, text=label_text,
          background=bg, foreground='white', anchor=W)\
        .grid(row=r, column=0, sticky=EW)
    Button(root, text=btn_label_text, command=btn_func, anchor=E)\
        .grid(row=r, column=1, sticky=E)


def create_checkbox(root, var, label_text, bg, on_value, _anchor=W):
    Checkbutton(root, text=label_text, variable=var,
                width=20, anchor=_anchor, selectcolor=bg, background=bg, fg='white',
                activebackground=bg, activeforeground='white',
                onvalue=on_value, offvalue=-1)\
        .pack(fill=X)
