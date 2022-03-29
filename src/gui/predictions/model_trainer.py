from tkinter import *
from tkinter import ttk
import traceback
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# from keras.models import Sequential
# from keras.layers import Dense

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from util import api_utils as au
from util import widget_factory as wf
import threading
from util import sys


class ModelTrainer():
    def __init__(self, root, bg_color, sampler) -> None:
        self.frame = Frame(root, bg=bg_color, borderwidth=10)
        self.frame.pack(expand=True, fill=BOTH)
        self.sampler = sampler

        Button(self.frame, text='Train', command=self.train_model).pack()

        Button(self.frame, text='Correlation', command=self.correlation).pack()

        Button(self.frame, text='Confusion Matrix',
               command=self.confusion_matrix).pack()

        self.result_frame = Frame(self.frame, bg=bg_color)
        self.result_frame.pack(expand=True)
        self.accuracyText = StringVar()
        wf.create_info_label(self.result_frame, self.accuracyText,
                             'Accuracy:', bg_color, r=0, label_width=10)
        self.precisionText = StringVar()
        wf.create_info_label(self.result_frame, self.precisionText,
                             'Precision:', bg_color, r=1, label_width=10)
        self.recallText = StringVar()
        wf.create_info_label(self.result_frame, self.recallText,
                             'Recall:', bg_color, r=2, label_width=10)
        self.F1_score = StringVar()
        wf.create_info_label(self.result_frame, self.F1_score,
                             'F1 Score:', bg_color, r=3, label_width=10)

    def get_bodies_ml_data(self, _test_size):
        if self.sampler.df is not None:
            self.df_ML = self.sampler.df.copy()
            self.df_ML.replace({'N': 0, 'Y': 1}, inplace=True)
            self.df_ML.dropna(inplace=True)
            self.df_ML = self.df_ML.apply(
                lambda x: pd.to_numeric(x, errors='ignore'))

            pha_df = self.df_ML[self.df_ML['pha'] == 1]
            iters = int(len(self.df_ML.index) / len(pha_df.index)) - 1

            y = self.df_ML.iloc[:, -1]
            y = y.astype(int)
            for i in range(iters):
                y = pd.concat([y, pha_df.iloc[:, -1]], ignore_index=True)

            X = self.df_ML.iloc[:, :-1]
            X = X.astype(float)
            for i in range(iters):
                noise = np.random.normal(-0.05, 0.05, pha_df.shape)
                new_pha_df = pha_df.iloc[:, :-1] + noise[:, :-1]
                X = pd.concat([X, new_pha_df], ignore_index=True)

            return train_test_split(X, y, test_size=_test_size)
        else:
            raise Exception('Data needs to firstly downloaded')

    def train_model(self):
        try:
            self.X_train, self.X_test, self.y_train, self.y_test = self.get_bodies_ml_data(
                _test_size=.2)

            scaler = StandardScaler().fit(self.X_train)
            self.X_train = scaler.transform(self.X_train)
            self.X_test = scaler.transform(self.X_test)

            #classifier = LogisticRegression()
            classifier = RandomForestClassifier()
            #classifier = svm.LinearSVC()

            classifier.fit(self.X_train, self.y_train)
            self.y_pred = classifier.predict(self.X_test)

            # dl_model = Sequential()
            # dl_model.add(Dense(20, activation='relu', input_shape=X_train.shape))
            # dl_model.add(Dense(50, activation='relu'))
            # dl_model.add(Dense(50, activation='relu'))
            # dl_model.add(Dense(1, activation='sigmoid'))

            # dl_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

            # dl_model_history = dl_model.fit(X_train, y_train, epochs = 50, validation_split = 0.1)

            # dl_model_preds = dl_model.predict(X_test)
            # print(classification_report(y_test,dl_model_preds.round()))

            self.accuracyText.set(accuracy_score(self.y_test, self.y_pred))
            self.precisionText.set(precision_score(
                self.y_test, self.y_pred, average='macro'))
            self.recallText.set(recall_score(
                self.y_test, self.y_pred, average='macro'))
            self.F1_score.set(
                f1_score(self.y_test, self.y_pred, average='macro'))
        except Exception as e:
            print(f'Failed to train model. Reason: {e}')
            sys.print_traceback()
            print(traceback.format_exc())

    def correlation(self):
        if self.sampler.df is not None:
            plt.figure(figsize=(10, 7))
            corr_matrix = self.df_ML.corr(method='pearson')
            sns.heatmap(corr_matrix, annot=True)
            plt.show()

    def confusion_matrix(self):
        cm = confusion_matrix(self.y_test, self.y_pred)
        ax = sns.heatmap(cm, square=True, annot=True, cbar=False, fmt='g')
        ax.xaxis.set_ticklabels(['non-pha', 'pha'], fontsize=8)
        ax.yaxis.set_ticklabels(['non-pha', 'pha'], fontsize=8, rotation=0)
        ax.set_xlabel('Predicted Labels', fontsize=10)
        ax.set_ylabel('True Labels', fontsize=10)
        plt.show()
