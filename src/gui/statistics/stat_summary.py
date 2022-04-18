from tkinter import *
import pandas as pd
import matplotlib.pyplot as plt
from util import widget_factory as wf
from scipy.cluster.hierarchy import linkage, fcluster

AU = 149597871

class StatSummary():
    def __init__(self, root, bg_color, query) -> None:
        self.frame = Frame(root, bg=bg_color, borderwidth=10)
        self.frame.pack(expand=True, fill=BOTH)
        self.query = query
        self.frame.columnconfigure((0, 1), weight=1)

        space = 2

        # Info
        wf.create_info_button_stretched(root=self.frame, btn_label_text='Scatter',
                                        btn_func=self.scatter, label_text='Show Scatter:', bg=bg_color, r=0, _pady=space)

        self.minDstText = StringVar()
        wf.create_info_button_stretched(root=self.frame, btn_label_text='Hexbin',
                                        btn_func=self.hexbin, label_text='Show Hexbin:', bg=bg_color, r=1, _pady=space)

        self.minDstText = StringVar()
        wf.create_info_label_stretched(
            root=self.frame, string_var=self.minDstText, label_text='Min distance:', bg=bg_color, r=2, _pady=(space,0))
        self.maxDstText = StringVar()
        wf.create_info_label_stretched(
            root=self.frame, string_var=self.maxDstText, label_text='Max distance:', bg=bg_color, r=3)
        self.meanDstText = StringVar()
        wf.create_info_label_stretched(
            root=self.frame, string_var=self.meanDstText, label_text='Mean distance:', bg=bg_color, r=4)
        wf.create_info_button_stretched(root=self.frame, btn_label_text='Distances',
                                        btn_func=self.distancesBox, label_text='Show distances:', bg=bg_color, r=5, _pady=(0,space))

        self.minVelText = StringVar()
        wf.create_info_label_stretched(
            root=self.frame, string_var=self.minVelText, label_text='Min relative velocity:', bg=bg_color, r=6, _pady=(space,0))
        self.maxVelText = StringVar()
        wf.create_info_label_stretched(
            root=self.frame, string_var=self.maxVelText, label_text='Max relative velocity:', bg=bg_color, r=7)
        self.meanVelText = StringVar()
        wf.create_info_label_stretched(
            root=self.frame, string_var=self.meanVelText, label_text='Mean relative velocity:', bg=bg_color, r=8)
        wf.create_info_button_stretched(root=self.frame, btn_label_text='Velocity',
                                        btn_func=self.velocityBox, label_text='Show velocities:', bg=bg_color, r=9, _pady=(0,space))

        self.minMagText = StringVar()
        wf.create_info_label_stretched(
            root=self.frame, string_var=self.minMagText, label_text='Min magnitude:', bg=bg_color, r=10, _pady=(space,0))
        self.maxMagText = StringVar()
        wf.create_info_label_stretched(
            root=self.frame, string_var=self.maxMagText, label_text='Max magnitude:', bg=bg_color, r=11)
        self.meanMagText = StringVar()
        wf.create_info_label_stretched(
            root=self.frame, string_var=self.meanMagText, label_text='Mean magnitude:', bg=bg_color, r=12)

        wf.create_info_button_stretched(root=self.frame, btn_label_text='Interval',
                                        btn_func=self.showIntervalFrame, label_text='Show interval:', bg=bg_color, r=13, _pady=(0,space))

        self.cls = StringVar()
        self.cls.set('4')
        wf.create_info_label_entry(root=self.frame, entry_var=self.cls, label_text='Hierarchy count:', bg=bg_color, r=14, entry_width=15, _pady=(0, space))
        wf.create_info_button_stretched(root=self.frame, btn_label_text='Hierarchy',
                                        btn_func=self.showHierarchy, label_text='Show hierarchy:', bg=bg_color, r=15, _pady=(0,space))


        self.xValue = StringVar()
        self.xValue.set('dist')
        wf.create_info_label_entry(root=self.frame, entry_var=self.xValue, label_text='x label:', bg=bg_color, r=16, entry_width=15, _pady=(20, space))

        self.yValue = StringVar()
        self.yValue.set('h')
        wf.create_info_label_entry(root=self.frame, entry_var=self.yValue, label_text='y label:', bg=bg_color, r=17, entry_width=15, _pady=(0, space))
                                        

        

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

    def scatter(self):
        if hasattr(self.query, 'df'):
            self.query.df.plot.scatter(
                x=self.xValue.get(), y=self.yValue.get(), c="v_rel", cmap="coolwarm")
            plt.show()
        else:
            print('Dataframe is null')

    def hexbin(self):
        if hasattr(self.query, 'df'):
            self.query.df.plot.hexbin(
                x=self.xValue.get(), y=self.yValue.get(), gridsize=25, cmap="coolwarm")
            plt.show()
        else:
            print('Dataframe is null')

    def distancesBox(self):
        if hasattr(self.query, 'df'):
            boxPlotData = self.query.df[["dist", "dist_min", "dist_max"]]
            boxPlotData.plot.box()
            plt.ylabel("Distances [AU]")
            plt.show()
        else:
            print('Dataframe is null')

    def velocityBox(self):
        if hasattr(self.query, 'df'):
            boxPlotData = self.query.df[["v_rel", "v_inf"]]
            boxPlotData.plot.box()
            plt.ylabel("Velocity [km/s]")
            plt.show()
        else:
            print('Dataframe is null')

    def countAmountFrame(self,dataFrame,size='7D'):
        dataFrame = dataFrame.set_index("cd")
        frame = dataFrame.resample(size).count()

        returnFrame = frame['des']

        df = pd.DataFrame(returnFrame)
        df = df.reset_index(level=0)
        df.index += 1
        df.columns = ['interval','amount']

        df['interval'] = df['interval'].dt.date

        return df
        

    def showIntervalFrame(self):
        if hasattr(self.query, 'df'):
            intervalFrame = self.countAmountFrame(self.query.df)
            intervalFrame.plot.bar(x="interval",y="amount")
            plt.show()
        else:
            print('Dataframe is null')
        

    def showHierarchy(self):
        cls = int(self.cls.get())
        if (cls > 0):
            if hasattr(self.query, 'df'):
                dataFrame = self.query.df
                array = dataFrame[[self.xValue.get(),self.yValue.get()]].to_numpy()
                z = linkage(array, method="single")
                idx = fcluster(z, cls, 'maxclust')

                clr =  ['#2200CC' ,'#D9007E' ,'#FF6600' ,'#FFCC00' ,'#ACE600',
                        '#0099CC' ,'#8900CC' ,'#FF0000' ,'#FF9900' ,'#FFFF00',
                        '#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6', 
                        '#E6B333', '#3366E6', '#999966', '#99FF99', '#B34D4D',
                        '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A', 
                        '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
                        '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC', 
                        '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399',
                        '#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680', 
                        '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933',
                        '#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3', 
                        '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6', '#6666FF']

                plt.figure()
                plt.xlabel("Orbit id")
                plt.ylabel("Magnitude")
                for i in range(1,cls+1):
                    plt.plot(array[idx==i,0],array[idx==i,1], 'o', color =clr[i])
                plt.show()

            else:
                print('Dataframe is null')
        else:
            print("Wrong cls value")
