from tkinter import *

from matplotlib import pyplot as plt
from util import widget_factory as wf
from sklearn.model_selection import train_test_split
from util import api_utils as au
import threading
from util import sys
import pandas as pd
import seaborn as sns
from util import widget_factory as wf

orbit_elements = {
    'Eccentricity': 'e',
    'Semimajor axis': 'a',
    'Perihelion distance': 'q',
    'Inclination': 'i',
    'Longitude of the ascending node': 'om',
    'Argument of perihelion': 'w',
    'Mean anomaly': 'ma',
    'Time of perihelion passage': 'tp',
    'Orbital period': 'per',
    'Mean motion': 'n',
    'Aphelion distance': 'ad'
}


class DataSampler():
    def __init__(self, root, bg_color) -> None:
        self.frame = Frame(root, bg=bg_color, borderwidth=10)
        self.frame.pack(expand=True, fill=BOTH)
        self.t = None
        self.df = None

        Label(self.frame, text='Include data:', bg=bg_color,
              fg='white', anchor=W).pack(pady=(10, 0), fill=X)

        self.int_vars = []
        for i, x in enumerate(orbit_elements):
            int_var = IntVar()
            int_var.set(i)
            self.int_vars.append(int_var)
            wf.create_checkbox(self.frame, int_var, x, bg_color, i)

        opt_frame = Frame(self.frame, bg=bg_color, borderwidth=5)
        opt_frame.pack(expand=True, fill=BOTH, pady=10)
        opt_frame.columnconfigure((0, 1), weight=1)
        wf.create_info_button_stretched(opt_frame, 'Correlation', self.correlation, 'Correlation matrix:', bg_color, 0)

        self.alertText = StringVar()
        self.loading_label = Label(
            self.frame, textvariable=self.alertText, bg=bg_color, fg='white')
        self.loading_label.pack_forget()

        Button(self.frame, text='Download data',
               command=self.download_data).pack(side=BOTTOM, pady=10)

    def get_query_params(self):
        on_boxes = list(filter(lambda x: x.get() >= 0, self.int_vars))
        params = []
        values = list(orbit_elements.values())
        for var in on_boxes:
            params.append(values[var.get()])
        params.append('pha')
        return ','.join(params)

    def get_query_params_indexes(self):
        on_boxes = list(filter(lambda x: x.get() >= 0, self.int_vars))
        params_idx = []
        for var in on_boxes:
            params_idx.append(var.get())
        return params_idx

    def supply_data(self):
        try:
            fields = self.get_query_params()
            if fields != 'pha':
                self.loading_label.pack(side=BOTTOM, pady=5)
                self.alertText.set('Loading...')
                bodies_json = au.get_json_from_url(
                    f'https://ssd-api.jpl.nasa.gov/sbdb_query.api?fields={fields}&sb-group=NEO')
                self.df = pd.DataFrame(
                    columns=bodies_json['fields'], data=bodies_json['data'])
            else:
                print('At least one field parameter must be selected!')
            
            self.loading_label.pack_forget()
        except Exception as e:
            self.loading_label.pack(side=BOTTOM, pady=5)
            self.alertText.set('Failed.')
            print('<------------------------------------')
            print(f'Failed to supply dataframe')
            sys.print_traceback()
            #print(traceback.format_exc())
            print('Reason: ', e)
            print('------------------------------------>')
        
        self.t = None

    def download_data(self):
        if self.t is None:
            self.t = threading.Thread(target=self.supply_data)
            self.t.daemon = True
            self.t.start()

    def correlation(self):
        if self.df is not None:
            df_ML = self.df.copy()
            df_ML.replace({'N': 0, 'Y': 1}, inplace=True)
            df_ML.dropna(inplace=True)
            df_ML = df_ML.apply(
                lambda x: pd.to_numeric(x, errors='ignore'))
            plt.figure(figsize=(10, 7))
            corr_matrix = df_ML.corr(method='pearson')
            sns.heatmap(corr_matrix, annot=True)
            plt.show()


