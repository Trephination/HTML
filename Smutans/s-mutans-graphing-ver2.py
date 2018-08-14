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
            print('in command prompt')


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
    ds = pd.read_excel(filename_location, header=None)

    for i in range(len(ds.columns)):
        print(ds.values.T[i].tolist())


class BiofilmCfuCount(object):
    """
    Protocol from Caroline that counts biofilm formation across several well conditions relative to planktonic cell
    growth by counting colony forming units of every plated well. This count is then used to find the concentration of
    CFUs (CFUs/mL) for every condition tested. Then raw CFU count of biofilm and proportion of biofilm CFUs to
    planktonic CFUs are both plotted separately.
    """
    def __init__(self, data_info, conditions):
        """
        Necessary information to interpret data effectively
        :param data_info: tuple containing three lists: (well labels, biofilm CFU count, planktonic CFU count)
        :param conditions: tuple containing two ints: (number of conditions tested, volume plated from well)
        """
        self.data_labels, self.film_count, self.plank_count = data_info
        self.tot_conditions, self.plated_volume = conditions

        self.film_conc, self.plank_conc = [], []
        self.organized_names, self.organized_film, self.organized_plank = [], [], []

    def raw_processing(self):
        """
        Take raw CFU count for each condition and dilution and convert it to CFUs/mL
        """
        well_dilution_code = {'e': 5, 'f': 6, 'g': 7, 'h': 8}

        for well in self.data_labels:
            x = 10 ** well_dilution_code[well[-1]]
            y = self.film_count[self.data_labels.index(well)] * 5 * x * (20 / self.plated_volume)
            z = self.plank_count[self.data_labels.index(well)] * 5 * x * (20 / self.plated_volume)

            self.film_conc.append(y)
            self.plank_conc.append(z)

    def data_grouping(self):
        """
        Group and reduce all wells per column into one condition
        """
        group_container, film_container, plank_container = [[] for a in range(self.tot_conditions)], \
                                                           [[] for a in range(self.tot_conditions)], \
                                                           [[] for a in range(self.tot_conditions)]

        for i in self.data_labels:
            group = int(i[:-1])
            group_container[group - 1].append(i)
            film_container[group - 1].append(self.film_count[self.data_labels.index(i)])
            plank_container[group - 1].append(self.plank_count[self.data_labels.index(i)])

        return group_container, film_container, plank_container

    def data_averaging_and_cleaning(self):
        """
        Find averages across wells for every condition, create specific, user determined names for every condition
        """
        groups, film, plank = self.data_grouping()

        for i in groups:
            self.organized_names.append(input('Enter label name for condition ' + str(i)))

            self.organized_film.append(sum(film[groups.index(i)]) / len(film[groups.index(i)]))
            try:
                self.organized_plank.append(sum(film[groups.index(i)]) / (sum(film[groups.index(i)]) +
                                                                          sum(plank[groups.index(i)])))
            except ZeroDivisionError:
                self.organized_plank.append(sum(film[groups.index(i)]) / 1)

    def run_and_plot(self):
            """
            Plot all organized data in a bar plot
            """
            self.raw_processing()
            self.data_averaging_and_cleaning()

            print(self.organized_names)
            print(self.organized_film)
            print(self.organized_plank)

            height = self.organized_film
            bars = tuple(self.organized_names.copy())
            y_pos = np.arange(len(bars))

            plt.bar(y_pos, height)
            plt.xticks(y_pos, bars)
            plt.xlabel('TH% in 100ul water/TH mixture')
            plt.ylabel('CFU/mL count')
            plt.title('Experiment 2.5 (Sucrose Concentration) 7 Aug 2018')

            plt.show()

            height2 = self.organized_plank

            plt.bar(y_pos, height2)
            plt.xticks(y_pos, bars)
            plt.xlabel('TH% in 100ul water/TH mixture')
            plt.ylabel('Proportion of Biofilm CFUs to Planktonic CFUs')
            plt.title('Experiment 2.5 (Sucrose Concentration) 7 Aug 2018')

            plt.show()


def run_program():
    """
    Ask user how they want to input data and run program
    """
    print('Biofilm assay selected.')
    x = input('Enter data manually or automatically?')

    if str.lower(x) == 'manually':
        z = BiofilmCfuCount(manual_input(), (input('Enter number of conditions:'), input('Enter plated volume:')))
        z.run_and_plot()

    elif str.lower(x) == 'automatically':
        y = input('Enter file name with extension:')
        b = r"C:\Users\Andres\Documents\HTML\Smutans" + '\\' + str(y)
        a = BiofilmCfuCount(auto_input(b), (input('Enter number of conditions:'), input('Enter plated volume:')))
        a.run_and_plot()


if __name__ == '__main__':
    troubleshoot()

    # (a, b) = manual_input()
    # experiment_2_5 = [['1e', '1f', '1g', '1h', '2e', '2f', '2g', '2h', '3e', '3f', '3g', '3h',
    #                    '4e', '4f', '4g', '4h', '5e', '5f', '5g', '5h', '6e', '6f', '6g', '6h'],
    #                   [0, 0, 0, 0, 127, 5, 9, 0, 22, 0, 0, 0, 25, 27, 0, 0, 20, 3, 0, 0, 35, 2, 0, 0],
    #                   [0, 0, 0, 0, 21, 1, 0, 0, 32, 3, 0, 0, 54, 5, 0, 0, 42, 2, 0, 0, 17, 1, 1, 0]]
    # c = (6, 15)
    # wao = BiofilmCfuCount(experiment_2_5, c)
    # wao.run_and_plot()

    # auto_input(r"C:\Users\Andres\Documents\HTML\Smutans\formatted experiment 2-5.xlsx")

    run_program()
