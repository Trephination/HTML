import sys
import pip
import string
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import openpyxl
import pandas as pd


def troubleshoot():
    """
        Initial troubleshooting to check when script can't run correctly
        Print statements for out of date/missing libraries
    """
    libraries = (sys, pd, openpyxl, matplotlib, pip)
    for i in libraries:
        try:
            print(str(i), 'version:', i.__version__)
        except AttributeError:
            pass
        except ModuleNotFoundError:
            print('You do not have', str(i), 'installed.')
            print('You can do so via your interpreter or:')
            print('py -m pip install', '-' + str(i))
            print('in command prompt if using a windows computer.')
            print('If using mac or linux, your best bet is stack overflow, sorry.')


class InputData(object):
    """
    Holds both basic input methods (automatic or manual) that are used to build the input for each protocol in the file.
    Called by CFU and Crystal Violet assay for S mutans characterization.
    """
    def __init__(self):
        self.input_style = str.lower(input("Automatic or manual input?"))
        self.data_labels = []
        self.data_container = []

    def label_grabber(self):
        """
        Collect the different titles for every data point
        """
        done = False

        while not done:
            x = input('Enter new data point name:')
            self.data_labels.append(x)

    def data_grabber(self):
        """
        Grab data for every label
        """
        new_data_list = []

        for i in self.data_labels:
            x = input('Input data for ' + str(i))
            new_data_list.append(x)

        self.data_container.append(new_data_list)

    def automatic_input(self):
        pass


class BioFilmCfuCount(InputData):
    """
    Protocol from Caroline that counts biofilm formation Protocol from Caroline that counts biofilm formation across several well conditions relative to planktonic cell
    growth by counting colony forming units of every plated well. This count is then used to find the concentration of
    CFUs (CFUs/mL) for every condition tested. Then raw CFU count of biofilm and proportion of biofilm CFUs to
    planktonic CFUs are both plotted separately.
    """
    def __init__(self, conditions):
        """
        Necessary information to interpret data effectively
        :param conditions: tuple containing two ints, plate volume and number of conditions
        """
        InputData.__init__(self)
        self.plated_volume = conditions[0]
        self.condition_numbers = conditions[1]

    def data_collection(self):
        """
        Use the data input class to gather relevant information for plotting and extrapolating
        """
        if InputData.input_style == 'automatic':
            self.automatic_input()
        else:
            self.label_grabber()
            print('Input biofilm CFU count.')
            self.data_grabber()
            print('Input planktonic CFU count.')
            self.data_grabber()

    def raw_processing(self):
        """
        Take raw CFU count for each
        """
        well_dilution_code = {'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10}

        for well in self.data_labels:
            x = 10 ** well_dilution_code[well[-1]]


class CrystalVioletAssay(InputData):
    pass


if __name__ == '__main__':
    current_conditions = (15, 6)
    BioFilmCfuCount(current_conditions)
