import matplotlib.pyplot as plt
import sys
import matplotlib
import pandas as pd
import numpy.random as np


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
    :param filename_location: filename to strip
    :return: Dictionary with all well data for the experiment
    """
    ds = pd.read_excel(filename_location, header=None, names=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])
    print(ds.head(5))


auto_input(r"C:\Users\Andres\Documents\HTML\TestData1.xlsx")

# location = r'C:\Users\Andres\Documents\HTML\Lesson3.xlsx'

# df = pd.read_excel(location, 0, index_col='StatusDate')
# print(df.dtypes)
# print(df.index)
# print(df.head())

