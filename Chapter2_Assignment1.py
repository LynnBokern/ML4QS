
# Import the relevant classes.
from Chapter2.CreateDataset import CreateDataset
from util.VisualizeDataset import VisualizeDataset
from util import util
from pathlib import Path
import copy
import os
import sys

# Chapter 2: Initial exploration of the dataset.

"""
First, we set some module-level constants to store our data locations. These are saved as a pathlib.Path object, the
preferred way to handle OS paths in Python 3 (https://docs.python.org/3/library/pathlib.html). Using the Path's methods,
you can execute most path-related operations such as making directories.

sys.argv contains a list of keywords entered in the command line, and can be used to specify a file path when running
a script from the command line. For example:

$ python3 crowdsignals_ch2.py my/proj/data/folder my_dataset.csv

If no location is specified, the default locations in the else statement are chosen, which are set to load each script's
output into the next by default.
"""

DATASET_PATH = Path(sys.argv[1] if len(sys.argv) > 1 else './datasets/crowdsignals/own-dataset/')
RESULT_PATH = Path('./intermediate_datafiles/')
RESULT_FNAME = sys.argv[2] if len(sys.argv) > 2 else 'own-dataset-result.csv'

# Set a granularity (the discrete step size of our time series data). We'll use a course-grained granularity of one
# instance per minute, and a fine-grained one with four instances per second.
GRANULARITIES = [1000,15000]

# We can call Path.mkdir(exist_ok=True) to make any required directories if they don't already exist.
[path.mkdir(exist_ok=True, parents=True) for path in [DATASET_PATH, RESULT_PATH]]


datasets = []
for milliseconds_per_instance in GRANULARITIES:
    print(f'Creating numerical datasets from files in {DATASET_PATH} using granularity {milliseconds_per_instance}.')

    # Create an initial dataset object with the base directory for our data and a granularity
    dataset = CreateDataset(DATASET_PATH, milliseconds_per_instance)

    # Add the selected measurements to it.
    # We add the accelerometer data (continuous numerical measurements) of the phone and the smartwatch
    # and aggregate the values per timestep by averaging the values
    dataset.add_numerical_dataset('Accelerometer.csv', 'timestamps', ['x','y','z'], 'avg', 'acc_')

    # We add the gyroscope data (continuous numerical measurements) of the phone and the smartwatch
    # and aggregate the values per timestep by averaging the values
    dataset.add_numerical_dataset('Gyroscope.csv', 'timestamps', ['x','y','z'], 'avg', 'gyr_')

    # We add the heart rate (continuous numerical measurements) and aggregate by averaging again

    # We add the labels provided by the users. These are categorical events that might overlap. We add them
    # as binary attributes (i.e. add a one to the attribute representing the specific value for the label if it
    # occurs within an interval).
    dataset.add_event_dataset('labels.csv', 'label_start', 'label_end', 'label', 'binary')

    # We add the magnetometer data (continuous numerical measurements) of the phone and the smartwatch
    # and aggregate the values per timestep by averaging the values
    dataset.add_numerical_dataset('Magnetometer.csv', 'timestamps', ['x','y','z'], 'avg', 'mag_')

    # We add the pressure sensed by the phone (continuous numerical measurements) and aggregate by averaging again
    dataset.add_numerical_dataset('Barometer.csv', 'timestamps', 'x', 'avg', 'bar_')

    #Add linear accelerometer
    dataset.add_numerical_dataset('Linear Accelerometer.csv', 'timestamps', ['x', 'y', 'z'], 'avg', 'lin_acc_')

    #Add location
    ##dataset.add_numerical_dataset('Location.csv', 'timestamps', ['lat', 'lon', 'height', 'velocity', 'direction', 'horizontal', 'vertical'], 'avg', 'loc_')
    ##dataset.add_numerical_dataset('Location.csv', 'timestamps', ['height', 'velocity', 'horizontal', 'vertical'], 'avg', 'loc_')
    dataset.add_numerical_dataset('Location.csv', 'timestamps', ['height', 'velocity'], 'avg', 'loc_')

    # Get the resulting pandas data table
    dataset = dataset.data_table
    print(dataset)

    # Plot the data
    DataViz = VisualizeDataset(__file__)

    # Boxplot
    DataViz.plot_dataset_boxplot(dataset, ['acc_x','acc_y','acc_z'])
    DataViz.plot_dataset_boxplot(dataset, ['gyr_x','gyr_y','gyr_z'])    
    DataViz.plot_dataset_boxplot(dataset, ['bar_x'])    
    DataViz.plot_dataset_boxplot(dataset, ['mag_x','mag_y','mag_z'])    
    ##DataViz.plot_dataset_boxplot(dataset, ['acc_x','acc_y','acc_z',])




    # Plot all data
    DataViz.plot_dataset(dataset, ['acc_', 'gyr_', 'bar_', 'mag_', 'lin_acc_', 'loc_' ,'label'],
                                  ['like', 'like', 'like', 'like', 'like', 'like','like'],
                                  ['line', 'line', 'line', 'line', 'line', 'line', 'points'])


    # And print a summary of the dataset.
    #util.print_statistics(dataset)
    datasets.append(copy.deepcopy(dataset))

    # If needed, we could save the various versions of the dataset we create in the loop with logical filenames:
    # dataset.to_csv(RESULT_PATH / f'chapter2_result_{milliseconds_per_instance}')


# Make a table like the one shown in the book, comparing the two datasets produced.
util.print_latex_table_statistics_two_datasets(datasets[0], datasets[1])

# Finally, store the last dataset we generated (250 ms).
dataset.to_csv(RESULT_PATH / RESULT_FNAME)
