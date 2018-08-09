import matplotlib.pyplot as plt
import sys
import matplotlib
import numpy as np
import openpyxl
import pandas as pd
import pip
import string


def troubleshoot():
    """
    Initial troubleshooting to check when script can't run correctly
    :return: None, prints versions numbers
    """
    print(sys.version)
    print(pd.__version__)
    print(openpyxl.__version__)
    print(matplotlib.__version__)
    print(pip.__version__)


# Uncomment line below and run if having issues, check these versions with current
# If one or more of these is missing, script will not run correctly if at all
# May also want to check version compatibility with other libraries
# If one is missing pip install, if pip version is 10 or 18, you will need to download patch as these versions are
# technically broken
# Can ask Andres for help
# troubleshoot()

# Manual input for well data, in case auto reading is not set up in time, or not worth the effort
def manual_input():
    """
    Collect well data from user input
    :return: Dictionary with all well data for the experiment
    """
    well_label = []
    well_count = []

    complete_input = False
    while not complete_input:
        x = input('Enter well and count. For example: 1f56')
        if x == 'done' or x == 'Done':
            complete_input = True
            print('Okay thank you.')
            print('Processing...')
        else:
            if x[2] not in string.ascii_letters:
                well_label.append(x[0:2])
                well_count.append(int(x[2:]))
            else:
                well_label.append(x[0:3])
                well_count.append(int(x[3:]))

    return well_label, well_count


# When using auto input, remember that reading excel files IS NOT dynamic
# You must make sure changes to an excel are saved before the py script can detect them
def auto_input(filename_location):
    """
    Collect well data from txt or xls file
    :param filename_location: filename to strip
    :return: Dictionary with all well data for the experiment
    """
    ds = pd.read_excel(filename_location, header=None, names=['1', '2', '3', '4', '5', '6',
                                                              '7', '8', '9', '10', '11', '12'])
    print(ds.head(5))


# C for laptop, D for Desktop, specific to Andres's computers
# If using for your own computer, make sure that this is updated to reflect ur own location,
# just add a 3rd comment line here, don't forget the r
# location = r'C:\Users\Andres\Documents\HTML\Smutans\TestData1.xlsx'
# location = r'D:\Users\Andres\Documents\HTML\Smutans\TestData1.xlsx'
# auto_input(location)


def raw_data_processing(raw_data, plated_volume):
    """
    Take raw CFU data and convert to cell/biofilm count
    :param raw_data: CFU count
    :param plated_volume: amount of liquid dilution we plated per well (ul)
    :return: cell/biofilm count
    """
    well_dilution_code = {'e': 5, 'f': 6, 'g': 7, 'h': 8}
    cell_count = []
    well_label = raw_data[0]
    cfu_count = raw_data[1]

    for i in well_label:
        x = 10 ** int(well_dilution_code[i[-1]])

        if plated_volume == 20:
            y = cfu_count[well_label.index(i)] * 5 * x
        else:
            y = cfu_count[well_label.index(i)] * 5 * 1.333 * x

        cell_count.append(y)

    return well_label, cell_count


def data_grouping(well_labels, well_data, total_wells):
    """
    Take well data and group well dilutions together regardless of whether or not data
    is CFU or individual bacteria count
    :param well_labels: string of well name of length 4 to 5
    :param well_data: unknown data type for every well
    :param total_wells: int representing total number of wells/groups to make
    """
    group_container, data_container = [[] for a in range(total_wells)], [[] for b in range(total_wells)]

    for i in well_labels:
        group = int(i[:-1])
        group_container[group - 1].append(i)
        data_container[group - 1].append(well_data[well_labels.index(i)])

    return group_container, data_container


def bar_plot_setup(plate_data):
    """
    Take plate data and graph it on a bar graph
    :param plate_data: tuple of two lists containing plate data
    :return: bar plot
    """
    objects = np.array(plate_data[0])
    values = plate_data[1]

    plt.bar(objects, values, align='center', alpha=0.5)
    plt.xticks(values, objects)
    plt.ylabel('CFu Count')
    plt.title('Colony forming units of different well conditions and dilutions')

    plt.show()


if __name__ == '__main__':
    # results = manual_input()
    test_results = (['1e', '1f', '1g', '1h', '2e', '2f', '2g', '2h', '3e', '3f', '3g', '3h'],
                    [35, 22, 16, 9, 58, 46, 31, 19, 86, 62, 44, 29])
    well_names, well_info = raw_data_processing(test_results, 20)
    data_grouping(well_names, well_info, 3)
