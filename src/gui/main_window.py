from tkinter import *
from gui import bodies_list, info_panel

bg_color = '#010021'
panels_color = '#100f26'


class MainWindow:

    def __init__(self, name):
        window = Tk()
        window.title(name)
        window.geometry("1280x720")

        main_frame = Frame(window, width=1280, height=720,
                           bg=bg_color, borderwidth=10)
        main_frame.pack()
        main_frame.pack_propagate(False)

        # App label/logo
        logo = Label(main_frame, text=name, font=("Arial", 20),
                     background=bg_color, foreground='white')
        logo.pack()

        # Info panel
        info = info_panel.InfoPanel(main_frame, panels_color)

        # Bodies list
        bodies_list.BodiesList(main_frame, panels_color, info.supply_body_info)

        window.mainloop()
