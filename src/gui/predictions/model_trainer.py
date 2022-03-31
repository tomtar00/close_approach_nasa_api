from tkinter import *
from tkinter import ttk
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# from keras.models import Sequential
# from keras.layers import Dense

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import CategoricalNB, GaussianNB, MultinomialNB
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn import svm
from util import api_utils as au
from util import widget_factory as wf
import threading
from util import sys


class ModelTrainer():
    def __init__(self, root, bg_color, sampler) -> None:
        Label(root, text='Train', font=('Arial', 12, 'bold'),
              background=bg_color, foreground='white').pack(fill=X)
        self.frame = Frame(root, bg=bg_color, borderwidth=10)
        self.frame.pack(expand=True, fill=BOTH)
        self.sampler = sampler
        self.t = None

        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure((0, 1), weight=1)

        self.train_frame = Frame(self.frame, bg=bg_color)
        self.train_frame.grid(row=0, column=0, sticky=(E, W))

        self.model_names = ['Logistic Regression',
                            'Random Forest Classifier',
                            'SVM',
                            'Naive Bayes']
        self.model_name = StringVar(self.frame)
        self.model_name.set(self.model_names[1])  # default value

        wf.create_info_label_combo(
            self.train_frame, self.model_name, self.model_names, 'Model', bg_color, r=0)

        self.noise_var = IntVar()
        self.noise_var.set(-1)
        wf.create_checkbox_grid(self.train_frame, self.noise_var,
                                'Generate noise to reduce imbalance', bg_color, 1, 1, W, 2, _pady=(10, 0))
        self.noise_mag_var = StringVar()
        self.noise_mag_var.set('0.05')
        wf.create_info_label_entry(self.train_frame, self.noise_mag_var,
                                   'Noise magnitude', bg_color, r=2, entry_width=30, _pady=(0, 10))

        Button(self.train_frame, text='Train',
               command=self.start_train_thread, width=10).grid(row=3, column=0, pady=20)
        self.training_label = Label(self.train_frame, text='Training...', bg=bg_color, fg='white')
        self.training_label.grid_forget()

        self.result_frame = Frame(self.frame, bg=bg_color)
        self.result_frame.grid(row=0, column=1, sticky=(E, W))
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

        Button(self.result_frame, text='Confusion Matrix',
               command=self.confusion_matrix).grid(row=4, column=0, pady=10)

    def get_chosen_model(self):
        chosen_model_name = self.model_name.get()

        if chosen_model_name == self.model_names[0]:
            return LogisticRegression()
        elif chosen_model_name == self.model_names[1]:
            return RandomForestClassifier()
        elif chosen_model_name == self.model_names[2]:
            return svm.SVC()
        elif chosen_model_name == self.model_names[3]:
            return MultinomialNB()
        else:
            raise Exception('Wrong model chosen')

    def get_bodies_ml_data(self, _test_size):
        if self.sampler.df is not None:
            self.df_ML = self.sampler.df.copy()
            self.df_ML.replace({'N': 0, 'Y': 1}, inplace=True)
            self.df_ML.dropna(inplace=True)
            self.df_ML = self.df_ML.apply(
                lambda x: pd.to_numeric(x, errors='ignore'))

            gen_noise = self.noise_var.get() > 0

            if gen_noise:
                pha_df = self.df_ML[self.df_ML['pha'] == 1]
                iters = int(len(self.df_ML.index) / len(pha_df.index)) - 1

            y = self.df_ML.iloc[:, -1]
            y = y.astype(int)
            if gen_noise:
                for _ in range(iters):
                    y = pd.concat([y, pha_df.iloc[:, -1]], ignore_index=True)

            X = self.df_ML.iloc[:, :-1]
            X = X.astype(float)
            if gen_noise:
                noise_mag = float(self.noise_mag_var.get())
                for _ in range(iters):
                    noise = np.random.normal(-noise_mag,
                                             noise_mag, pha_df.shape)
                    new_pha_df = pha_df.iloc[:, :-1] + noise[:, :-1]
                    X = pd.concat([X, new_pha_df], ignore_index=True)

            return train_test_split(X, y, test_size=_test_size)
        else:
            raise Exception('Data needs to be firstly downloaded')

    def train_model(self):
        try:
            self.training_label.grid(row=3, column=1, pady=20)
            self.X_train, self.X_test, self.y_train, self.y_test = self.get_bodies_ml_data(
                _test_size=.2)

            scaler = MinMaxScaler().fit(self.X_train)
            self.X_train = scaler.transform(self.X_train)
            self.X_test = scaler.transform(self.X_test)

            self.classifier = self.get_chosen_model()

            self.classifier.fit(self.X_train, self.y_train)
            self.y_pred = self.classifier.predict(self.X_test)

            # dl_model = Sequential()
            # dl_model.add(Dense(20, activation='relu', input_shape=X_train.shape))
            # dl_model.add(Dense(50, activation='relu'))
            # dl_model.add(Dense(50, activation='relu'))
            # dl_model.add(Dense(1, activation='sigmoid'))

            # dl_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

            # dl_model_history = dl_model.fit(X_train, y_train, epochs = 50, validation_split = 0.1)

            # dl_model_preds = dl_model.predict(X_test)
            # print(classification_report(y_test,dl_model_preds.round()))

            def to_prec(x): return f"{round(x*100, 2)} %"

            self.accuracyText.set(
                to_prec(accuracy_score(self.y_test, self.y_pred)))
            self.precisionText.set(
                to_prec(precision_score(self.y_test, self.y_pred, average='macro')))
            self.recallText.set(
                to_prec(recall_score(self.y_test, self.y_pred, average='macro')))
            self.F1_score.set(
                to_prec(f1_score(self.y_test, self.y_pred, average='macro')))
        except Exception as e:
            print(f'Failed to train model. Reason: {e}')
            sys.print_traceback()
        else:
            self.training_label.grid_forget()
            self.t = None

    def start_train_thread(self):
        if self.t is None:
            self.t = threading.Thread(target=self.train_model)
            self.t.daemon = True
            self.t.start()

    def confusion_matrix(self):
        if self.sampler.df is not None:
            cm = confusion_matrix(self.y_test, self.y_pred)
            ax = sns.heatmap(cm, square=True, annot=True, cbar=False, fmt='g')
            ax.xaxis.set_ticklabels(['non-pha', 'pha'], fontsize=8)
            ax.yaxis.set_ticklabels(['non-pha', 'pha'], fontsize=8, rotation=0)
            ax.set_xlabel('Predicted Labels', fontsize=10)
            ax.set_ylabel('True Labels', fontsize=10)
            plt.show()
