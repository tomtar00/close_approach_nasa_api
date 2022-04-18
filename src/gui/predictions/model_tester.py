from tkinter import *
from util import widget_factory as wf
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
        Label(root, text='Test', font=('Arial', 12, 'bold'),
              background=bg_color, foreground='white').pack(fill=X)
        self.frame = Frame(root, bg=bg_color, borderwidth=10)
        self.frame.pack(expand=True, fill=BOTH)
        self.trainer = trainer
        self.sampler = sampler

        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure((0, 1), weight=1)

        self.pred_frame = Frame(self.frame, bg=bg_color)
        self.pred_frame.grid(row=0, column=0, sticky=(E, W))

        self.des_var = StringVar()
        self.des_var.set('433')
        wf.create_info_label_entry(self.pred_frame, self.des_var,
                                   'Object designation', bg_color, r=0, entry_width=30, _pady=(0, 10), _padx=(0, 20))

        Button(self.pred_frame, text="Predict", command=self.download_object, width=10).grid(sticky=W, pady=10)

        self.result_frame = Frame(self.frame, bg=bg_color)
        self.result_frame.grid(row=0, column=1, sticky=(E, W))
        self.classText = StringVar()
        wf.create_info_label(self.result_frame, self.classText,
                             'Predicted class:', bg_color, r=0, label_width=15)
        self.confidenceText = StringVar()
        wf.create_info_label(self.result_frame, self.confidenceText,
                             'Confidence:', bg_color, r=1, label_width=10)

        self.trueClassText = StringVar()
        wf.create_info_label(self.result_frame, self.trueClassText,
                             'True class:', bg_color, r=2, label_width=15, _pady=5)

    def predict_object_hazardous(self, elements_array):
        try:
            classes_prob = self.trainer.classifier.predict_proba([elements_array])[0]
            max_value = np.max(classes_prob)
            max_idx = np.argmax(classes_prob)
            self.classText.set(classes.get(max_idx))
            self.confidenceText.set(f'{max_value * 100} %')
        except:
            pred = self.trainer.classifier.predict([elements_array])[0]
            self.classText.set(classes.get(pred))
            self.confidenceText.set('??? %')

    def download_object(self):
        try:
            obj_name = self.des_var.get()
            elements = []
            json = au.get_json_from_url(
                    f'https://ssd-api.jpl.nasa.gov/sbdb.api?des={obj_name}&full-prec=true')
            orbit_json = json['orbit']
            pha = json['object']['pha']

            elem_idx = self.sampler.get_query_params_indexes()
            for idx in elem_idx:
                elements.append(float(orbit_json['elements'][idx]['value']))

            self.predict_object_hazardous(elements)
            self.trueClassText.set('pha' if pha else 'non-pha')
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