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
    ds = pd.read_excel(filename_location, header=None, names=['1', '2', '3', '4', '5', '6',
                                                              '7', '8', '9', '10', '11', '12'])
    print(ds.head(5))


# auto_input(location)

# C for laptop, D for Desktop, specific to Andres's computers
# location = r'C:\Users\Andres\Documents\HTML\Smutans\Lesson3.xlsx'
# location = r'D:\Users\Andres\Documents\HTML\Smutans\Lesson3.xlsx'


def bar_plot_setup(plate_data):
    """
    Take plate data and graph it on a bar graph
    :param plate_data: dictionary containing plate data
    :return: bar plot
    """
