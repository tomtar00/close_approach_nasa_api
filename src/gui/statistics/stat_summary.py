from tkinter import *
import matplotlib.pyplot as plt
from util import widget_factory as wf


class StatSummary():
    def __init__(self, root, bg_color, query) -> None:
        self.frame = Frame(root, bg=bg_color, borderwidth=10)
        self.frame.pack(expand=True, fill=BOTH)
        self.query = query
        self.frame.columnconfigure((0, 1), weight=1)

        # Info
        wf.create_info_button_stretched(root=self.frame, btn_label_text='Hexbin',
                                        btn_func=self.hexbin, label_text='Show hexbin:', bg=bg_color, r=0)

        self.testText = StringVar()
        wf.create_info_label_stretched(
            root=self.frame, string_var=self.testText, label_text='Test:', bg=bg_color, r=1)

    def handle_data_downloaded(self):
        # Supply statistic data here
        print(self.query.df.head())
        self.testText.set('test')

    ##### Buttton events #####

    def hexbin(self):
        if hasattr(self.query, 'df'):
            self.query.df.plot.hexbin(
                x="orbit_id", y="h", gridsize=25, cmap="coolwarm")
            plt.show()
        else:
            print('Dataframe is null')
