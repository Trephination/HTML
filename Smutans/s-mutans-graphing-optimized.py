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
    :return: print statements for out of date/missing libraries
    """
    libraries = (sys, pd, openpyxl, matplotlib, pip)
    for i in libraries:
        try:
            print(i.__version__)
        except ModuleNotFoundError:
            print('You do not have', str(i), 'installed.')
            print('You can do so via your interpreter or: ')
            print('py -m pip install', '-' + str(i))
            print('in command prompt.')


def manual_input():
    """
    Collect data from user input, can be used to record any form of data
    :return: Two lists where indices map relation between lists
    """
    label, data = [], []

    complete_input = False
    print('Enter data label and data. For example, 1f 56, is a record of 56 labeled 1f.')
    print('To erase last input type "cancel", to finish type "done"')

    while not complete_input:
        x = input('Enter label and data:')
        if str.lower(x) == 'done':
            complete_input = True
            print('Okay thank you.')
            print('Processing...')
        elif str.lower(x) == 'cancel':
            label.pop()
            data.pop()
        else:
            name, number = x.split(' ')
            label.append(name)
            data.append(int(number))
    return label, data


def auto_input(filename_location):
    """
    Collect well data from txt or xls file
    :param filename_location: str of filename/location to read
    :return: tuple of lists with data labels and names
    """
    ds = pd.read_excel(filename_location, header=None, names=[])
    print(ds.head(5))
    # TODO: make work


class BiofilmCfuCount(object):
    """
    Protocol from Caroline that counts biofilm formation across several well conditions
    relative to planktonic cell growth by count colony forming units of every plated well.
    """
    def __init__(self, data_info, conditions):
        self.data_labels = data_info[0]
        self.data_counts = data_info[1]
        self.counterpart_data = data_info[2]
        self.total_conditions = conditions[0]
        self.plate_volume = conditions[1]

        self.cell_count, self.organized_names, self.organized_data, self.proportional_count, self.organized_proportions = [], [], [], [], []

    def raw_processing(self):
        """
        Take raw CFU count per condition and dilution and convert it to CFUs/mL
        """
        well_dilution_code = {'e': 5, 'f': 6, 'g': 7, 'h': 8}

        for well in self.data_labels:
            x = 10 ** well_dilution_code[well[-1]]
            y = self.data_counts[self.data_labels.index(well)] * 5 * x * (20 / self.plate_volume)
            z = self.counterpart_data[self.data_labels.index(well)] * 5 * x * (20 / self.plate_volume)

            self.cell_count.append(y)
            self.proportional_count.append(z)

    def data_grouping(self):
        """
        Group wells and well names by condition
        :return: list of well names and data grouped by condition
        """
        group_container, data_container, proportion_container = [[] for a in range(self.total_conditions)], [[] for a in range(self.total_conditions)],[[] for a in range(self.total_conditions)]

        for i in self.data_labels:
            group = int(i[:-1])
            group_container[group - 1].append(i)
            data_container[group - 1].append(self.cell_count[self.data_labels.index(i)])
            proportion_container[group - 1].append(self.proportional_count[self.data_labels.index(i)])

        return group_container, data_container, proportion_container

    def data_averaging_and_cleaning(self):
        """
        Find averages across wells for every condition, create specific, user determined names for every condition
        """
        groups, numbers, counter_numbers = self.data_grouping()

        for i in groups:
            self.organized_names.append(input('Enter label name for condition ' + str(i)))
            try:
                self.organized_data.append(sum(numbers[groups.index(i)]) / len(numbers[groups.index(i)]))
            except ZeroDivisionError:
                print(len(numbers[groups.index(i)]))
                self.organized_data.append(sum(numbers[groups.index(i)]) / 1)
            try:
                self.organized_proportions.append(sum(numbers[groups.index(i)]) / (sum(numbers[groups.index(i)]) + sum(counter_numbers[groups.index(i)])))
            except ZeroDivisionError:
                self.organized_proportions.append(sum(numbers[groups.index(i)]) / 1)

    def run_and_plot(self):
        """
        Plot all organized data in a bar plot
        """
        self.raw_processing()
        self.data_averaging_and_cleaning()

        print(self.organized_names)
        print(self.organized_data)
        print(self.organized_proportions)

        height = self.organized_data
        bars = tuple(self.organized_names.copy())
        y_pos = np.arange(len(bars))

        plt.bar(y_pos, height)
        plt.xticks(y_pos, bars)
        plt.xlabel('TH% in 100ul water/TH mixture')
        plt.ylabel('CFU/mL count')
        plt.title('Experiment 2.5 (Sucrose Concentration) 7 Aug 2018')

        plt.show()

        height2 = self.organized_proportions

        plt.bar(y_pos, height2)
        plt.xticks(y_pos, bars)
        plt.xlabel('TH% in 100ul water/TH mixture')
        plt.ylabel('Proportion of Biofilm CFUs to Planktonic CFUs')
        plt.title('Experiment 2.5 (Sucrose Concentration) 7 Aug 2018')

        plt.show()


if __name__ == '__main__':
    # (a, b) = manual_input()
    experiment_2_5 = [['1e', '1f', '1g', '1h', '2e', '2f', '2g', '2h', '3e', '3f', '3g', '3h',
                       '4e', '4f', '4g', '4h', '5e', '5f', '5g', '5h', '6e', '6f', '6g', '6h'],
            [0, 0, 0, 0, 127, 5, 9, 0, 22, 0, 0, 0, 25, 27, 0, 0, 20, 3, 0, 0, 35, 2, 0, 0],
            [0, 0, 0, 0, 21, 1, 0, 0, 32, 3, 0, 0, 54, 5, 0, 0, 42, 2, 0, 0, 17, 1, 1, 0]]
    c = (6, 15)
    wao = BiofilmCfuCount(experiment_2_5, c)
    wao.run_and_plot()
