import os
import sys
from tkinter import *
import traceback
from gui import main_window
from util import api_utils as au
from functools import partial

class BodiesList:
    def __init__(self, root, bg_color, supply_info_func):
        bg_frame = Frame(root, bg=main_window.bg_color, borderwidth=10)
        bg_frame.place(relwidth=.3, relheight=.8, rely=.2)
        self.frame = Frame(bg_frame, bg=bg_color, borderwidth=10)
        self.frame.place(relwidth=1, relheight=1)

        try:
            # Read data from NASA API
            #bodies_json = au.get_json_from_url('https://ssd-api.jpl.nasa.gov/cad.api')

            # Local data (for testing)
            bodies_json = {
                'data': [
                    ['Body 1', '', '', 'Yesterday'],
                    ['Body 2', '', '', 'Today'],
                    ['Body 3', '', '', 'Tomorrow']
                ]
            }

            self.supply_list(bodies_json, supply_info_func)

        except Exception as e:
            print('------------------------------------')
            print('Failed to download bodies list')
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(f'{exc_type} in file: {fname} at line: {exc_tb.tb_lineno}')
            print('Reason: ', e)
            print('------------------------------------')

    def supply_list(self, data, click_func):
        for i in range(len(data['data'])):
            action_with_arg = partial(click_func, data['data'][i])
            label = Button(self.frame, text=f"{data['data'][i][0]}", width=40, command=action_with_arg)
            label.pack()
