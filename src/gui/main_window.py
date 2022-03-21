from cmath import inf
from tkinter import *
from tkinter import ttk
from gui.current import info_panel
from gui.current import bodies_list
from gui.statistics import dataframe_view, stat_summary, stat_query

bg_color = '#23272A'
panels_color = '#2C2F33'
accent_color = '#99AAB5'


class MainWindow:

    def __init__(self, name):
        window = Tk()
        window.title(name)
        window.geometry('1280x720')
        window.configure(background=bg_color)
        window.columnconfigure(0, weight=1)
        window.rowconfigure((1, 2, 3, 4, 5), weight=1, uniform='row')

        top_frame = Frame(window, bg=bg_color, borderwidth=10)
        top_frame.grid(row=0, sticky=NW)

        # App label/logo
        logo = Label(top_frame, text=name, font=('Arial', 20),
                     background=bg_color, foreground='white')
        logo.pack()

        # Notebook (tabs)
        noteStyle = ttk.Style()
        noteStyle.theme_use('classic')
        noteStyle.configure('TNotebook', background=bg_color,
                            foreground='white', borderwidth=3)
        noteStyle.configure(
            'TNotebook.Tab', background=panels_color, foreground='white')
        noteStyle.map('TNotebook.Tab', background=[
                      ('selected', accent_color)], foreground=[('selected', 'black')])
        notebook = ttk.Notebook(window)
        notebook.grid(row=1, rowspan=5, sticky=(N, E, W, S), padx=15, pady=15)

        ##### Current
        current_frame = Frame(window, bg=bg_color, borderwidth=10)

        bodies_frame = Frame(current_frame, bg=bg_color,
                             borderwidth=10, width=300)
        bodies_frame.pack(side=LEFT, fill=BOTH)
        bodies_frame.pack_propagate(0)
        info_frame = Frame(current_frame, bg=bg_color, borderwidth=10)
        info_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        info = info_panel.InfoPanel(info_frame, panels_color)
        bodies_list.BodiesList(bodies_frame, panels_color, info)

        ##### Statistics
        statistics_frame = Frame(window, bg=bg_color, borderwidth=10)

        left_frame = Frame(statistics_frame, bg=bg_color,
                              borderwidth=10, width=300)
        left_frame.pack(side=LEFT, fill=BOTH)
        left_frame.pack_propagate(0)
        query_frame = Frame(left_frame, bg=bg_color)
        query_frame.pack(fill=BOTH, expand=True, pady=(0, 5))
        summary_frame = Frame(left_frame, bg=bg_color)
        summary_frame.pack(fill=BOTH, expand=True, pady=(5, 0))
        dataframe_frame = Frame(statistics_frame, bg=bg_color, borderwidth=10)
        dataframe_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        stat_query.StatQuery(query_frame, panels_color)
        stat_summary.StatSummary(summary_frame, panels_color)
        dataframe_view.DataframeView(dataframe_frame, panels_color)

        ##### Predictions
        predictions_frame = Frame(window, bg=bg_color, borderwidth=10)

        # Add frames to notebook
        notebook.add(current_frame, text='Current')
        notebook.add(statistics_frame, text='Statistics')
        notebook.add(predictions_frame, text='Predictions')

        window.mainloop()
