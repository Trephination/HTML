import math
import matplotlib
import sys


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


def auto_input(filename):
    """
    Collect well data from txt or xls file
    :param filename: filename to strip
    :return: 
    """


