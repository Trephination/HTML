import math
import matplotlib.pyplot as plt
import sys
import matplotlib
import pandas as pd
# need xlrd as well
# also need openpyxl


def manual_input():
    """
    Collect well data from user input
    :return: Dictionary with all well data for the experiment
    """
    temp_d = {}
    complete_input = False
    while not complete_input:
        x = input('Enter well and count. For example: 1f56')
        if x == 'done' or x == 'Done':
            complete_input = True
            print('Okay thank you.')
            print('Processing...')
        else:
            temp_d[x[0:2]] = int(x[2:])

    return temp_d


def auto_input(filename_location):
    """
    Collect well data from txt or xls file
    :param filename: filename to strip
    :return: Dictionary with all well data for the experiment
    """
    df = pd.read_excel(filename_location, 0, index_col='StatusDate')
    df.dtypes


auto_input(r"D:\Users\Andres\Documents\HTML\TestData1.xlsx")

