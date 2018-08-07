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
                well_count.append(x[2:])
            else:
                well_label.append(x[0:3])
                well_count.append(x[3:])

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
location = r'D:\Users\Andres\Documents\HTML\Smutans\TestData1.xlsx'
# auto_input(location)


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


results = manual_input()
bar_plot_setup(results)
