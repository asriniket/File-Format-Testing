import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot(file_formats, num_datasets, dimensions):
    if not os.path.exists("Data/Plots"):
        os.mkdir("Data/Plots")
    create_time, write_time, open_time, read_time, error = process_csv(file_formats, num_datasets, dimensions)
    width = .25

    plt.figure(1)
    plt_labels = ["Dataset Read Time", "Dataset Write Time"]
    x = np.arange(len(plt_labels))
    offset = -width
    plt.ylabel("Average Time (ms)")
    plt.title(f"{num_datasets} Datasets {dimensions} Elements Dataset Read / Write Times")
    plt.xticks(x, plt_labels)
    for i in range(0, len(file_formats)):
        read_time_round = round(read_time[i], 5)
        write_time_round = round(write_time[i], 5)
        read_error = error[i][3]
        write_error = error[i][1]
        bar_create_open = plt.bar(x + offset, [read_time_round, write_time_round], width, label=file_formats[i],
                                  edgecolor="black", yerr=[read_error, write_error])
        plt.bar_label(bar_create_open, padding=3)
        offset += width
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"Data/Plots/{num_datasets}_{dimensions}_Read_Write.png")
    # plt.show()

    plt.figure(2)
    plt_labels = ["Dataset Create Time", "Dataset Open Time"]
    x = np.arange(len(plt_labels))
    offset = -width
    plt.ylabel("Average Time (ms)")
    plt.title(f"{num_datasets} Datasets {dimensions} Elements Dataset Create / Open Times")
    plt.xticks(x, plt_labels)
    for i in range(0, len(file_formats)):
        create_time_round = round(create_time[i], 5)
        open_time_round = round(open_time[i], 5)
        create_error = error[i][0]
        open_error = error[i][2]
        bar_create_open = plt.bar(x + offset, [create_time_round, open_time_round], width, label=file_formats[i],
                                  edgecolor="black", yerr=[create_error, open_error])
        plt.bar_label(bar_create_open, padding=3)
        offset += width
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"Data/Plots/{num_datasets}_{dimensions}_Create_Open.png")
    # plt.show()

    plt.cla()
    plt.clf()


def process_csv(file_formats, num_datasets, dimensions):
    total_dataset_create_time = []
    total_dataset_write_time = []
    total_dataset_open_time = []
    total_dataset_read_time = []
    error = []
    for file_format in file_formats:
        df = pd.read_csv(f"Data/{file_format}_{num_datasets}_{dimensions}.csv")
        dataset_create_time, dataset_write_time, dataset_open_time, dataset_read_time = df.iloc[:, 1:].mean(axis=0)
        create_deviation, write_deviation, open_deviation, read_deviation = df.iloc[:, 1:].std(axis=0)
        total_dataset_create_time.append(dataset_create_time)
        total_dataset_write_time.append(dataset_write_time)
        total_dataset_open_time.append(dataset_open_time)
        total_dataset_read_time.append(dataset_read_time)
        error.append([create_deviation, write_deviation, open_deviation, read_deviation])
        if df.iloc[-1, 0] == "Average":
            continue
        average_values = pd.DataFrame({
            file_format: "Average",
            "Dataset Creation Time": [dataset_create_time],
            "Dataset Write Time": [dataset_write_time],
            "Dataset Open Time": [dataset_open_time],
            "Dataset Read Time": [dataset_read_time]
        })
        df = pd.concat([df, average_values], ignore_index=True)
        df.to_csv(f"Data/{file_format}_{num_datasets}_{dimensions}.csv", index=False)
    return total_dataset_create_time, total_dataset_write_time, total_dataset_open_time, total_dataset_read_time, error
