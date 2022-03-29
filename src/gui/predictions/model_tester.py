from tkinter import *
from tkinter import ttk
from util import api_utils as au
import threading
from util import sys

class ModelTester():
    def __init__(self, root, bg_color) -> None:
        self.frame = Frame(root, bg=bg_color, borderwidth=10)
        self.frame.pack(expand=True, fill=BOTH)