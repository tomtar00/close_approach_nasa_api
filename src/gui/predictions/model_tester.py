from tkinter import *

import numpy as np
from util import api_utils as au
import threading
from util import sys

classes = {
    1 : 'pha',
    0 : 'non-pha'
}

class ModelTester():
    def __init__(self, root, bg_color, trainer, sampler) -> None:
        self.frame = Frame(root, bg=bg_color, borderwidth=10)
        self.frame.pack(expand=True, fill=BOTH)
        self.trainer = trainer
        self.sampler = sampler

        self.entry = Entry(self.frame)
        self.entry.pack()
        Button(self.frame, text="OK", command=self.download_object).pack()

    def predict_object_hazardous(self, elements_array):
        classes_prob = self.trainer.classifier.predict_proba([elements_array])[0]
        max_value = np.max(classes_prob)
        max_idx = np.argmax(classes_prob)
        print(classes.get(max_idx), f'{max_value * 100} %')

    def download_object(self):
        try:
            obj_name = self.entry.get()
            elements = []
            orbit_json = au.get_json_from_url(
                    f'https://ssd-api.jpl.nasa.gov/sbdb.api?des={obj_name}&full-prec=true')['orbit']

            elem_idx = self.sampler.get_query_params_indexes()
            for idx in elem_idx:
                elements.append(float(orbit_json['elements'][idx]['value']))

            self.predict_object_hazardous(elements)
        except Exception as e:
            print('Failed to download object. Reason: ', e)
            sys.print_traceback()
        else:
            self.t = None

    def start_downloading_thread(self):
        if self.t is None:
            self.t = threading.Thread(target=self.download_object)
            self.t.daemon = True
            self.t.start()