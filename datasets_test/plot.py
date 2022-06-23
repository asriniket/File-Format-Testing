import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot(file_formats, num_datasets, dimensions):
    # Generate two plots - one for the read / write times and one for the dataset create / open times
    if not os.path.exists('datasets_test/data/plots'):
        os.mkdir('datasets_test/data/plots')
    create_time, write_time, open_time, read_time, error = process_csv(file_formats, num_datasets, dimensions)
    width = .25

    plt.figure(1)
    plt_labels = ['Dataset Read Time', 'Dataset Write Time']
    x = np.arange(len(plt_labels))
    offset = -width
    plt.ylabel('Time (ms)')
    plt.title(f'{num_datasets} Datasets {dimensions} Elements Dataset Read / Write Times')
    plt.xticks(x, plt_labels)
    for i in range(0, len(file_formats)):
        # Round to 5 decimal places so data shows nicely
        read_time_rounded = round(read_time[i], 5)
        write_time_rounded = round(write_time[i], 5)
        read_error = error[i][3]
        write_error = error[i][1]
        bar_create_open = plt.bar(x=x + offset, height=[read_time_rounded, write_time_rounded], width=width,
                                  label=file_formats[i], edgecolor='black', yerr=[read_error, write_error])
        plt.bar_label(bar_create_open, padding=3)
        offset += width
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'datasets_test/data/plots/{num_datasets}_{dimensions}_read_write.png')
    # plt.show()
    plt.cla()
    plt.clf()

    plt.figure(2)
    plt_labels = ['Dataset Create Time', 'Dataset Open Time']
    x = np.arange(len(plt_labels))
    offset = -width
    plt.ylabel('Time (ms)')
    plt.title(f'{num_datasets} Datasets {dimensions} Elements Dataset Create / Open Times')
    plt.xticks(x, plt_labels)
    for i in range(0, len(file_formats)):
        # Round to 5 decimal places, so that it displays nicely on the plot.
        create_time_rounded = round(create_time[i], 5)
        open_time_rounded = round(open_time[i], 5)
        create_error = error[i][0]
        open_error = error[i][2]
        bar_read_write = plt.bar(x=x + offset, height=[create_time_rounded, open_time_rounded], width=width,
                                 label=file_formats[i], edgecolor='black', yerr=[create_error, open_error])
        plt.bar_label(bar_read_write, padding=3)
        offset += width
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'datasets_test/data/plots/{num_datasets}_{dimensions}_create_open.png')
    # plt.show()
    plt.cla()
    plt.clf()


def process_csv(file_formats, num_datasets, dimensions):
    # Calculate the average value in each column of the provided CSV file.
    # Append it to the file if not already appended.
    # Return these average times to be plotted.
    total_dataset_create_time = []
    total_dataset_write_time = []
    total_dataset_open_time = []
    total_dataset_read_time = []
    error = []
    for file_format in file_formats:
        df = pd.read_csv(f'datasets_test/data/{file_format}_{num_datasets}_{dimensions}.csv')
        dataset_create_time, dataset_write_time, dataset_open_time, dataset_read_time = df.iloc[:, 1:].mean(axis=0)
        create_deviation, write_deviation, open_deviation, read_deviation = df.iloc[:, 1:].std(axis=0)
        total_dataset_create_time.append(dataset_create_time)
        total_dataset_write_time.append(dataset_write_time)
        total_dataset_open_time.append(dataset_open_time)
        total_dataset_read_time.append(dataset_read_time)
        error.append([create_deviation, write_deviation, open_deviation, read_deviation])
        if df.iloc[-1, 0] == 'Average':
            # Go to next iteration if the last column of the CSV file has the average times
            continue
        average_values = pd.DataFrame({
            file_format: 'Average',
            'Dataset Creation Time': [dataset_create_time],
            'Dataset Write Time': [dataset_write_time],
            'Dataset Open Time': [dataset_open_time],
            'Dataset Read Time': [dataset_read_time]
        })
        df = pd.concat([df, average_values], ignore_index=True)
        df.to_csv(f'datasets_test/data/{file_format}_{num_datasets}_{dimensions}.csv', index=False)
    return total_dataset_create_time, total_dataset_write_time, total_dataset_open_time, total_dataset_read_time, error
