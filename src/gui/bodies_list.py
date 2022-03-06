from tkinter import *
from gui import main_window
from util import api_utils as ut
from functools import partial

class BodiesList:
    def __init__(self, root, bg_color, supply_info_func):
        bg_frame = Frame(root, bg=main_window.bg_color, borderwidth=10)
        bg_frame.place(relwidth=.3, relheight=.8, rely=.2)
        self.frame = Frame(bg_frame, bg=bg_color, borderwidth=10)
        self.frame.place(relwidth=1, relheight=1)

        # Uncomment this line to get data from nasa api...
        # bodies_json = self.download_bodies('https://ssd-api.jpl.nasa.gov/cad.api')

        # ... and comment this lines
        bodies_json = {
            'data': [
                ['Body 1', '', '', 'Yesterday'],
                ['Body 2', '', '', 'Today'],
                ['Body 3', '', '', 'Tomorrow']
            ]
        }

        # USE LOCAL DATA FOR TESTING!
    
        self.supply_list(bodies_json, supply_info_func)

    def download_bodies(self, url):
        return ut.get_json_from_url(url)

    def supply_list(self, data, click_func):
        for i in range(len(data['data'])):
            action_with_arg = partial(click_func, data['data'][i])
            label = Button(self.frame, text=f"{data['data'][i][0]}", width=40, command=action_with_arg)
            label.pack()
