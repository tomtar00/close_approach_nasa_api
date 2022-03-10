from util import sys
from tkinter import *
from gui import main_window
from util import api_utils as au
from functools import partial
from concurrent.futures import ThreadPoolExecutor


class BodiesList:

    def __init__(self, root, bg_color, supply_info_func):
        bg_frame = Frame(root, bg=main_window.bg_color, borderwidth=10)
        bg_frame.place(relwidth=.3, relheight=.8, rely=.2)
        self.frame = Frame(bg_frame, bg=bg_color, borderwidth=10)
        self.frame.place(relwidth=1, relheight=1)
        self.supply_func = supply_info_func
        self.bodies_btn = []
        self.focus_bodies = {
            'Mercury': 'Merc',
            'Venus': 'Venus',
            'Earth': 'Earth',
            'Mars': 'Mars',
            'Jupiter': 'Juptr',
            'Saturn': 'Satrn',
            'Neptune': 'Neptn',
            'Pluto': 'Pluto',
            'Moon': 'Moon'
        }

        focus_bodies_keys = list(self.focus_bodies.keys())
        self.focus_name = StringVar(self.frame)
        self.focus_name.set(focus_bodies_keys[2])  # default value

        focus_options = OptionMenu(
            self.frame, self.focus_name, *focus_bodies_keys)
        focus_options.pack()

        self.option_value = self.focus_bodies.get(self.focus_name.get())
        button = Button(self.frame, text="OK",
                        command=self.handle_change_focus)
        button.pack()

        self.update_list(self.option_value)

    def handle_change_focus(self):
        self.option_value = self.focus_bodies.get(self.focus_name.get())
        return self.update_list(self.option_value)

    def supply_list(self, data, click_func):
        # create buttons for all objects in data and assing command for each button

        for i in range(len(data['data'])):
            action_with_arg = partial(click_func, data['data'][i])
            button = Button(
                self.frame, text=f"{data['data'][i][0]}", width=40, command=action_with_arg)
            button.pack()
            self.bodies_btn.append(button)

    def request_bodies_data(self, focus_body_name):
        # download data for given focused body and supply list of buttons

        try:

            print(f'downloading data of {focus_body_name}\'s close bodies...')
            self.bodies_json = au.get_json_from_url(
                f'https://ssd-api.jpl.nasa.gov/cad.api?body={focus_body_name}&limit=5')
            print('data downloaded successfuly')
            self.loading_label.destroy()
            self.supply_list(self.bodies_json, self.supply_func)

        except Exception as e:

            print('<------------------------------------')
            print(f'Failed to download bodies list for {focus_body_name}')
            sys.print_traceback()
            print('Reason: ', e)
            print('------------------------------------>')

    def update_list(self, focus_body_name):
        # destroy previous buttons and start downloading data on other thread

        if self.bodies_btn:
            for btn in self.bodies_btn:
                btn.destroy()

        # Read data from NASA API
        # ########################
        # self.loading_label = Label(
        #     self.frame, text='Loading...', bg=main_window.bg_color, fg='white')
        # self.loading_label.pack()
        # executor = ThreadPoolExecutor(max_workers=1)
        # executor.submit(self.request_bodies_data, focus_body_name)
        # ########################

        # Local data (for testing)
        # ########################
        self.bodies_json = {
            'data': [
                ['Body 1', '', '', 'Yesterday'],
                ['Body 2', '', '', 'Today'],
                ['Body 3', '', '', 'Tomorrow']
            ]
        }
        self.supply_list(self.bodies_json, self.supply_func)
        # ########################
