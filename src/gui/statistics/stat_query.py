from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from util import api_utils as au
from gui.current import bodies_list as bl
import threading
from util import sys

class StatQuery():
    def __init__(self, root, bg_color) -> None:
        self.frame = Frame(root, bg=bg_color, borderwidth=10)
        self.frame.pack(expand=True, fill=BOTH)
        self.t = None

        Button(self.frame, text='Download data', command=self.download_data).pack(side=BOTTOM, pady=5)

        query_frame = Frame(self.frame, bg=bg_color)
        query_frame.pack()

        Label(query_frame, text='Min date:', bg=bg_color, fg='white').grid(row=0, column=0, pady=5)
        self.min_entry = DateEntry(query_frame, width=30, year=2022, locale='en_US', date_pattern='yyyy-MM-dd')
        self.min_entry.grid(row=0, column=1, pady=5)

        Label(query_frame, text='Max date:', bg=bg_color, fg='white').grid(row=1, column=0, pady=5)
        self.max_entry = DateEntry(query_frame, width=30, year=2022, locale='en_US', date_pattern='yyyy-MM-dd')
        self.max_entry.grid(row=1, column=1, pady=5)

        Label(query_frame, text='Planet:', bg=bg_color, fg='white').grid(row=2, column=0, pady=5)
        planets = list(bl.focus_bodies.keys())
        self.planet_name = StringVar()
        self.planet_name.set(planets[2])  # default value
        planets_options = ttk.Combobox(
            query_frame, textvariable=self.planet_name, values=planets, state='readonly')
        planets_options.grid(row=2, column=1, pady=5)

    def set_view_summary(self, df_view, summary):
        self.df_view = df_view
        self.summary = summary

    def supply_dataframe(self):
        try:
            min_date = self.min_entry.get_date().strftime('%Y-%m-%d')
            max_date = self.max_entry.get_date().strftime('%Y-%m-%d')
            self.df_view.show_loading()
            self.df = au.getDataFromApi(min_date, max_date, self.planet_name.get())
            self.summary.handle_data_downloaded()        
            if self.df is not None:
                self.df_view.dataframe_to_treeview(self.df)
        except Exception as e:
            self.df_view.clear_treeview()
            self.df_view.show_no_result()
            print('<------------------------------------')
            print(f'Failed to supply dataframe')
            sys.print_traceback()
            #print(traceback.format_exc())
            print('Reason: ', e)
            print('------------------------------------>')
        
        self.t = None

    def download_data(self):
        if self.t is None:
            self.t = threading.Thread(target=self.supply_dataframe)
            self.t.daemon = True
            self.t.start()