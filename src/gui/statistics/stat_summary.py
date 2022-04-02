from tkinter import *
import matplotlib.pyplot as plt
from util import widget_factory as wf

AU = 149597871

class StatSummary():
    def __init__(self, root, bg_color, query) -> None:
        self.frame = Frame(root, bg=bg_color, borderwidth=10)
        self.frame.pack(expand=True, fill=BOTH)
        self.query = query
        self.frame.columnconfigure((0, 1), weight=1)

        space = 2

        # Info
        wf.create_info_button_stretched(root=self.frame, btn_label_text='Hexbin',
                                        btn_func=self.hexbin, label_text='Show hexbin:', bg=bg_color, r=0, _pady=space)

        self.minDstText = StringVar()
        wf.create_info_label_stretched(
            root=self.frame, string_var=self.minDstText, label_text='Min distance:', bg=bg_color, r=1, _pady=(space,0))
        self.maxDstText = StringVar()
        wf.create_info_label_stretched(
            root=self.frame, string_var=self.maxDstText, label_text='Max distance:', bg=bg_color, r=2)
        self.meanDstText = StringVar()
        wf.create_info_label_stretched(
            root=self.frame, string_var=self.meanDstText, label_text='Mean distance:', bg=bg_color, r=3)
        wf.create_info_button_stretched(root=self.frame, btn_label_text='Distances',
                                        btn_func=self.distancesBox, label_text='Show distances:', bg=bg_color, r=4, _pady=(0,space))

        self.minVelText = StringVar()
        wf.create_info_label_stretched(
            root=self.frame, string_var=self.minVelText, label_text='Min relative velocity:', bg=bg_color, r=5, _pady=(space,0))
        self.maxVelText = StringVar()
        wf.create_info_label_stretched(
            root=self.frame, string_var=self.maxVelText, label_text='Max relative velocity:', bg=bg_color, r=6)
        self.meanVelText = StringVar()
        wf.create_info_label_stretched(
            root=self.frame, string_var=self.meanVelText, label_text='Mean relative velocity:', bg=bg_color, r=7)
        wf.create_info_button_stretched(root=self.frame, btn_label_text='Velocity',
                                        btn_func=self.velocityBox, label_text='Show velocities:', bg=bg_color, r=8, _pady=(0,space))

        self.minMagText = StringVar()
        wf.create_info_label_stretched(
            root=self.frame, string_var=self.minMagText, label_text='Min magnitude:', bg=bg_color, r=9, _pady=(space,0))
        self.maxMagText = StringVar()
        wf.create_info_label_stretched(
            root=self.frame, string_var=self.maxMagText, label_text='Max magnitude:', bg=bg_color, r=10)
        self.meanMagText = StringVar()
        wf.create_info_label_stretched(
            root=self.frame, string_var=self.meanMagText, label_text='Mean magnitude:', bg=bg_color, r=11)

        

    def handle_data_downloaded(self):
        # Supply statistic data here

        round4 = lambda x: round(float(x), 4)

        minDst = round4(self.query.df['dist'].min() * AU / 1000000)
        maxDst = round4(self.query.df['dist'].max() * AU / 1000000)
        meanDst = round4(self.query.df['dist'].mean() * AU / 1000000)
        self.minDstText.set(f"{minDst} mln km")
        self.maxDstText.set(f"{maxDst} mln km")
        self.meanDstText.set(f"{meanDst} mln km")

        minVel = round4(self.query.df['v_rel'].min())
        maxVel = round4(self.query.df['v_rel'].max())
        meanVel = round4(self.query.df['v_rel'].mean())
        self.minVelText.set(f"{minVel} km/s")
        self.maxVelText.set(f"{maxVel} km/s")
        self.meanVelText.set(f"{meanVel} km/s")

        minMag = round4(self.query.df['h'].min())
        maxMag = round4(self.query.df['h'].max())
        meanMag = round4(self.query.df['h'].mean())
        self.minMagText.set(minMag)
        self.maxMagText.set(maxMag)
        self.meanMagText.set(meanMag)

    ##### Buttton events #####

    def hexbin(self):
        if hasattr(self.query, 'df'):
            self.query.df.plot.hexbin(
                x="dist", y="h", gridsize=25, cmap="coolwarm")
            plt.show()
        else:
            print('Dataframe is null')

    def distancesBox(self):
        if hasattr(self.query, 'df'):
            boxPlotData = self.query.df[["dist", "dist_min", "dist_max"]]
            boxPlotData.plot.box()
            plt.show()
        else:
            print('Dataframe is null')

    def velocityBox(self):
        if hasattr(self.query, 'df'):
            boxPlotData = self.query.df[["v_rel", "v_inf"]]
            boxPlotData.plot.box()
            plt.show()
        else:
            print('Dataframe is null')
