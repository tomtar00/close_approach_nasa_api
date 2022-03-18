import traceback
from util import sys
from tkinter import *
from tkinter import ttk
from gui import main_window
from util import api_utils as au
from functools import partial
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

focus_bodies = {
    'Mercury': {'key': 'Merc', 'downloaded': False},
    'Venus': {'key': 'Venus', 'downloaded': False},
    'Earth': {'key': 'Earth', 'downloaded': False},
    'Mars': {'key': 'Mars', 'downloaded': False},
    'Jupiter': {'key': 'Juptr', 'downloaded': False},
    'Saturn': {'key': 'Satrn', 'downloaded': False},
    'Neptune': {'key': 'Neptn', 'downloaded': False},
}

all_bodies_df = None


class BodiesList:

    def __init__(self, root, bg_color, supply_info_func, change_focus_func):
        self.frame = Frame(root, bg=bg_color, borderwidth=10)
        self.frame.pack(expand=True, fill=BOTH)

        self.supply_func = supply_info_func
        self.change_focus = change_focus_func
        self.bodies_btn = []

        self.alertText = StringVar()
        self.loading_label = Label(
            self.frame, textvariable=self.alertText, bg=main_window.panels_color, fg='white')
        self.loading_label.pack_forget()

        focus_bodies_keys = list(focus_bodies.keys())
        self.focus_name = StringVar(self.frame)
        self.focus_name.set(focus_bodies_keys[2])  # default value

        focus_frame = Frame(self.frame, bg=main_window.panels_color)
        focus_frame.pack(fill=X, pady=(0, 15))

        style = ttk.Style(self.frame)
        style.theme_use('classic')
        style.configure('TCombobox')
        style.map('TCombobox', fieldbackground=[('readonly','white')])
        style.map('TCombobox', selectbackground=[('readonly', 'white')])
        style.map('TCombobox', selectforeground=[('readonly', 'black')])
        focus_options = ttk.Combobox(
            focus_frame, textvariable=self.focus_name, values=focus_bodies_keys, state='readonly')
        focus_options.pack(side=RIGHT)

        self.option_value = focus_bodies.get(self.focus_name.get()).get('key')
        button = Button(focus_frame, text="OK",
                        command=self.handle_change_focus, width=7)
        button.pack(side=RIGHT, padx=5)

        self.update_list(self.option_value)

    def handle_change_focus(self):
        self.option_value = focus_bodies.get(self.focus_name.get()).get('key')
        self.change_focus(self.focus_name.get())
        return self.update_list(self.option_value) 

    def supply_list_from_web(self, data, click_func):
        # create buttons for all objects in data and assing command for each button

        _columns = list(self.bodies_json['fields'])
        _columns.append('body')
        once = True

        # if all_dobies_df doesnt exist, create it
        global all_bodies_df
        

        # for each body in data add it to dataframe and create button 
        for i in range(len(data['data'])):
            obj_name = data['data'][i][0]
            row = data['data'][i]
            row.append(self.focus_name.get())

            orbit_values = []
            orbit_names = []
            orbit_json = au.get_json_from_url(
                    f'https://ssd-api.jpl.nasa.gov/sbdb.api?des={obj_name}&full-prec=true')['orbit']
            for element in orbit_json['elements']:
                el_name = element['name']
                orbit_names.append(el_name)
                orbit_names.append(f'{el_name}_sigma')
                orbit_values.append(element['value'])
                orbit_values.append(element['sigma'])
    
            row += orbit_values

            if once == True:
                _columns += orbit_names
                once = False
            if all_bodies_df is None:
                all_bodies_df = pd.DataFrame(columns=_columns)
            df = pd.DataFrame([row], columns=_columns)
            all_bodies_df = pd.concat([all_bodies_df, df], ignore_index=True)

            action_with_arg = partial(click_func, df.iloc[0])
            button = Button(
                self.frame, text=f"{obj_name}", command=action_with_arg)
            button.pack(fill=X)
            self.bodies_btn.append(button)
        
        focus_bodies[self.focus_name.get()]['downloaded'] = True

    def supply_list_from_df(self, click_func):
        # create buttons for all objects in data and assing command for each button

        df = all_bodies_df[all_bodies_df['body'] == self.focus_name.get()]

        # for each body in data create button
        for row in df.iloc:
            action_with_arg = partial(click_func, row)
            button = Button(
                self.frame, text=f"{str(row['des'])}", command=action_with_arg)
            button.pack(fill=X)
            self.bodies_btn.append(button)

    def request_bodies_data(self, focus_body_name):
        # download data for given focused body and supply list of buttons

        try:
            download_data = focus_bodies[self.focus_name.get()]['downloaded'] == False

            if download_data:
                self.alertText.set('Loading...')
                print(f'downloading data of {focus_body_name}\'s close bodies...')
                self.bodies_json = au.get_json_from_url(
                    f'https://ssd-api.jpl.nasa.gov/cad.api?body={focus_body_name}&limit=5')
                self.supply_list_from_web(self.bodies_json, self.supply_func)
                print('data downloaded successfuly')
            else:
                self.supply_list_from_df(self.supply_func)

        except Exception as e:

            self.alertText.set('No results')
            print('<------------------------------------')
            print(f'Failed to download bodies list for {focus_body_name}')
            sys.print_traceback()
            #print(traceback.format_exc())
            print('Reason: ', e)
            print('------------------------------------>')

        else:  
            self.loading_label.pack_forget()

    def update_list(self, focus_body_name):
        # destroy previous buttons and start downloading data on other thread

        if self.bodies_btn:
            for btn in self.bodies_btn:
                btn.destroy()

        # Read data from NASA API
        # ########################
        self.loading_label.pack()
        executor = ThreadPoolExecutor(max_workers=1)
        executor.submit(self.request_bodies_data, focus_body_name)
        # ########################

        # Local data (for testing)
        # ########################
        # self.bodies_json = {
        #     'data': [
        #         ['Body 1', '', '', 'Yesterday'],
        #         ['Body 2', '', '', 'Today'],
        #         ['Body 3', '', '', 'Tomorrow']
        #     ]
        # }
        # self.supply_list(self.bodies_json, self.supply_func)
        # ########################
