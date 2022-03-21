import os
import sys
import datetime
import math
from astropy.time import Time

def print_traceback():
    exc_type, _, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(f'{exc_type} in file: {fname} at line: {exc_tb.tb_lineno}')

def get_julian_datetime(date):
    t = Time(date, format='iso')
    t.format = 'jd'
    return t.jd

def get_gregorian_datetime(julian_date):
    t = Time(julian_date, format='jd')
    t.format = 'iso'
    return t.iso