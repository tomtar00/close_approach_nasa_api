import tkinter as tk
from gui import bodies_list, info_panel

bg_color = '#010021'
panels_color = '#100f26'

class MainWindow:
    def __init__(self, name):
        window = tk.Tk()
        window.title(name)

        main_frame = tk.Frame(window, height=720, width=1280, bg=bg_color, borderwidth=10)
        main_frame.pack()

        # App label/logo
        #tk.Label(main_frame, text=name, font=("Arial", 25))

        # Info panel
        info = info_panel.InfoPanel(main_frame, panels_color)

        # Bodies list
        bodies_list.BodiesList(main_frame, panels_color, info.supply_body_info)     

        window.mainloop()