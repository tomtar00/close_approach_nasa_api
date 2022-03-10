import os
import sys

def print_traceback():
    exc_type, _, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(f'{exc_type} in file: {fname} at line: {exc_tb.tb_lineno}')